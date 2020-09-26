import os

from rasterio.coords import BoundingBox
from typer.testing import CliRunner

from cdemgl.modules.dem import CLIPPED_DEM, DEM
from cdemgl.modules.image import IMAGE
from cdemgl.modules.poi import POI
from cdemgl.modules.viewer import VIEWER

runner = CliRunner()


def test_poi():
    x, y = (-122.85, 49.75)
    poi = POI((x, y))
    assert poi.point.x == x
    assert poi.point.y == y


def test_dem():
    file_path = os.path.abspath("tests/fixtures/test_clip.tif")
    coords = (-122.85, 49.75)
    poi = POI(coords)
    zfactor = 3
    out_size = 1000
    dem = DEM(file_path, poi, zfactor, out_size)
    assert dem.clip_window == ((0, 1000), (200, 1200))
    assert dem.file_path == file_path
    assert dem.zfactor == zfactor


def test_clipped_dem():
    file_path = os.path.abspath("tests/fixtures/test_clip.tif")
    zfactor = 3
    calc_vertices = False
    clipped_dem = CLIPPED_DEM(file_path, zfactor, calc_vertices)
    assert clipped_dem.data.shape == (1200, 1200)
    assert clipped_dem.crs == "EPSG:4326"
    assert clipped_dem.nodata == -32767


def test_image():
    bounds = BoundingBox(
        -123.00010416666665, 49.500104166666674, -122.75010416666666, 49.75010416666667
    )
    image = IMAGE(bounds)
    assert image.algorithm == "B4,B3,B2"
    assert image.band_count == 3
    assert image.tif_path
    assert image.stac_item


def test_viewer():
    gltf_path = "path/to/model.gltf"
    viewer = VIEWER(gltf_path)
    assert viewer.file_path
    assert viewer.html
