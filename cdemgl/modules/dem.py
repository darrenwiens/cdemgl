import os
from pathlib import Path

import numpy as np
import rasterio
import typer
from scipy.spatial import Delaunay

from .utils import project_tif

outputs_dir = os.getenv("outputs_dir", "/tmp")


class DEM:
    def __init__(self, file_path, poi, zfactor, out_size):
        typer.secho("Creating DEM...", fg=typer.colors.MAGENTA)
        self.file_path = file_path
        self.out_size = np.array([out_size / 2, out_size / 2])
        self.clip_window = self.get_clip_window(poi)
        self.zfactor = zfactor

    def get_clip_window(self, poi):
        pnt = poi.point
        window_dims = self.out_size
        with rasterio.open(self.file_path) as src:
            py, px = src.index(pnt.x, pnt.y)
            moved_pnt = np.clip(
                np.array([py, px]),
                window_dims,
                np.array([src.height, src.width]) - window_dims,
            )
            window_ul = moved_pnt - window_dims
            window_br = moved_pnt + window_dims
            return (window_ul[0], window_br[0]), (window_ul[1], window_br[1])

    def clip(self):
        with rasterio.open(self.file_path) as src:
            window = self.clip_window
            subset = src.read(1, window=(window))
            clip_width = subset.shape[1]
            clip_height = subset.shape[0]
            coords_ul = src.xy(window[0][0], window[1][0])
            coords_br = src.xy(window[0][1], window[1][1])
            clip_transform = rasterio.transform.from_bounds(
                coords_ul[0],
                coords_br[1],
                coords_br[0],
                coords_ul[1],
                clip_width,
                clip_height,
            )

            dem_clip_path = os.path.join(outputs_dir, "intermediate", "dem_clip.tif")
            Path(os.path.dirname(dem_clip_path)).mkdir(parents=True, exist_ok=True)
            with rasterio.open(
                dem_clip_path,
                "w",
                driver="GTiff",
                height=clip_height,
                width=clip_width,
                count=1,
                dtype=subset.dtype,
                crs=src.crs,
                transform=clip_transform,
            ) as dst:
                dst.write(subset, 1)

            clipped_dem = CLIPPED_DEM(dem_clip_path, self.zfactor)

            return clipped_dem


class CLIPPED_DEM:
    def __init__(self, file_path, zfactor, calc_vertices=True):
        typer.secho("Clipping DEM...", fg=typer.colors.MAGENTA)
        self.file_path = file_path
        self.zfactor = zfactor

        with rasterio.open(self.file_path) as src:
            self.crs = src.crs

        if "4326" not in self.crs:
            typer.secho("Reprojecting clipped DEM...", fg=typer.colors.MAGENTA)
            src_tif = self.file_path
            dst_tif = os.path.join(outputs_dir, "intermediate", "dem_4326.tif")
            dst_crs = "EPSG:4326"
            project_tif(src_tif, dst_tif, dst_crs)
            self.file_path = dst_tif
            self.crs = dst_crs

        self.get_attrs()

        if calc_vertices:
            self.vertices = self.get_vertices()

    def get_attrs(self):
        with rasterio.open(self.file_path) as src:
            self.data = src.read(1)
            self.bounds = src.bounds
            self.width = src.profile.get("width")
            self.height = src.profile.get("height")
            self.nodata = src.profile.get("nodata")

    def get_vertices(self):
        typer.secho("Triangulating vertices...", fg=typer.colors.MAGENTA)
        rows = self.height
        cols = self.width
        bounds = self.bounds
        data = self.data
        nodata = self.nodata
        scale_factor = 20 / self.zfactor

        xs = np.linspace(bounds.left, bounds.right, cols)
        ys = np.linspace(bounds.bottom, bounds.top, rows)
        xs, ys = np.meshgrid(xs, ys)
        xs = xs.flatten()
        ys = ys.flatten()
        points2D = np.vstack([xs, ys]).T
        tri = Delaunay(points2D)

        indexes = np.array(list(np.ndindex((rows, cols)))).reshape(rows, cols, 2)
        x_values = indexes[:, :, 1]
        y_values = indexes[:, :, 0]
        min_z = np.nanmin(data[data != nodata])
        data[data == nodata] = min_z

        values = data[:rows, :cols] / scale_factor
        points3D = np.dstack([x_values, values, y_values]).reshape([rows * cols, 3])
        tri_vertices = map(lambda index: points3D[index], tri.simplices)

        verts = []
        for i in tri_vertices:
            verts += i.reshape([3, 3]).tolist()

        vert_arr = np.array(verts).astype("float64")

        vertices = {"dem_vertices": vert_arr}

        self.x_idx = xs[:cols]
        self.y_idx = ys.reshape([rows, cols])[:, 0]

        return vertices
