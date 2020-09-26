import rasterio
from pyproj import Transformer
from rasterio.warp import Resampling, calculate_default_transform, reproject


def project_point(x, y, from_proj, to_proj):
    transformer = Transformer.from_crs(from_proj, to_proj, always_xy=True)
    return transformer.transform(x, y)


def project_tif(src_tif, dst_tif, dst_crs):
    with rasterio.open(src_tif) as src:
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds
        )
        kwargs = src.meta.copy()
        kwargs.update(
            {"crs": dst_crs, "transform": transform, "width": width, "height": height}
        )

        with rasterio.open(dst_tif, "w", **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest,
                )
