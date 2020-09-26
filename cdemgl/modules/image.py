import os

import numpy as np
import rasterio
import typer
from rasterio.windows import from_bounds

from .stac import query_stac_api
from .utils import project_point, project_tif

outputs_dir = os.getenv("outputs_dir", "/tmp")


class IMAGE:
    def __init__(self, bounds):
        typer.secho("Creating image object...", fg=typer.colors.MAGENTA)
        self.stac_item = query_stac_api(bounds)
        self.algorithm = "B4,B3,B2"
        self.band_count = len(self.algorithm.split(","))
        self.tif_path = self.apply_algorithm(bounds)

    def apply_algorithm(self, bounds):
        stac_item = self.stac_item
        algorithm = self.algorithm
        subsets = []
        for band_idx, band_name in enumerate(algorithm.split(",")):
            fp = stac_item.get("assets").get(band_name).get("href")

            with rasterio.open(fp) as src:
                src_crs = src.crs.to_epsg()

                dem_proj_bl = project_point(
                    bounds.left,
                    bounds.bottom,
                    from_proj="epsg:4326",
                    to_proj=f"epsg:{src_crs}",
                )
                dem_proj_tr = project_point(
                    bounds.right,
                    bounds.top,
                    from_proj="epsg:4326",
                    to_proj=f"epsg:{src_crs}",
                )

                dem_proj_bounds = [
                    dem_proj_bl[0],
                    dem_proj_bl[1],
                    dem_proj_tr[0],
                    dem_proj_tr[1],
                ]

                wdw = from_bounds(*dem_proj_bounds, src.transform)

                subsets.append(src.read(1, window=wdw))
                clip_width = subsets[band_idx].shape[1]
                clip_height = subsets[band_idx].shape[0]
                clip_transform = rasterio.transform.from_bounds(
                    *dem_proj_bounds, clip_width, clip_height
                )

        img_clip = os.path.join(outputs_dir, "intermediate", "img_orig.tif")
        with rasterio.open(
            img_clip,
            "w",
            driver="GTiff",
            height=clip_height,
            width=clip_width,
            count=3,
            dtype=subsets[0].dtype,
            crs=src_crs,
            transform=clip_transform,
        ) as dst:
            for band_idx in range(self.band_count):
                dst.write(np.squeeze(subsets[band_idx]), band_idx + 1)

        dst_crs = "EPSG:4326"
        img_4326 = os.path.join(outputs_dir, "intermediate", "img_4326.tif")
        project_tif(img_clip, img_4326, dst_crs)
        return img_4326

    def write_png(self):
        with rasterio.open(self.tif_path) as src:
            self.png_bounds = src.bounds
            profile = src.profile
            profile["driver"] = "PNG"
            profile["dtype"] = "uint16"
            png_filename = os.path.join(outputs_dir, "intermediate", "img_4326.png")
            rasters = []
            for i in range(self.band_count):
                rasters.append(src.read(i + 1))
            rasters = np.stack(rasters)

            with rasterio.open(png_filename, "w", **profile) as dst:
                uint16 = rasters.astype(np.uint16)
                percs = np.percentile(np.moveaxis(uint16, 0, -1), [5, 95], axis=[0, 1])
                max_value = np.iinfo(np.uint16).max
                norm = (np.moveaxis(uint16, 0, -1) - percs[0]) / (percs[1] - percs[0])
                clipped = np.clip(norm, 0, 1)
                uint16_scaled = (clipped * max_value).astype(np.uint16)
                uint16_scaled = np.moveaxis(uint16_scaled, -1, 0)
                dst.write(uint16_scaled)
                typer.secho(f"...PNG written to: {png_filename}")

        self.png_path = png_filename
