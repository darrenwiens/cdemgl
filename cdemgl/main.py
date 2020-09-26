from typing import Tuple

import typer

from cdemgl.modules.dem import DEM
from cdemgl.modules.ftp import download_dem
from cdemgl.modules.gltf import GLTF_OBJ
from cdemgl.modules.image import IMAGE
from cdemgl.modules.poi import POI
from cdemgl.modules.viewer import VIEWER

app = typer.Typer()


@app.command()
def main(
    coords: Tuple[float, float] = typer.Option(
        (None, None), help="Longitude <space> Latitude"
    ),
    zfactor: float = typer.Option(1.0, help="Elevation stretch factor"),
    outsize: int = typer.Option(1000, help="Square output size, in pixels"),
    output: str = typer.Option("glb", help="Output format: gltf|glb"),
):
    typer.secho(f"Running cdemgl for Point{coords}", fg=typer.colors.GREEN)
    try:
        app_poi = POI(coords)
    except Exception as e:
        typer.secho(f"Exception: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    try:
        dem_file_path = download_dem(app_poi)
        app_dem = DEM(dem_file_path, app_poi, zfactor, outsize)
        app_clipped_dem = app_dem.clip()
    except Exception as e:
        typer.secho(f"Exception: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    try:
        dem_bounds = app_clipped_dem.bounds
        app_image = IMAGE(dem_bounds)
        app_image.write_png()
    except Exception as e:
        typer.secho(f"Exception: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    try:
        app_gltf = GLTF_OBJ(app_clipped_dem, app_image, output)
        app_gltf.save()
    except Exception as e:
        typer.secho(f"Exception: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    try:
        app_viewer = VIEWER(app_gltf.gltf_path)
        app_viewer.save()
    except Exception as e:
        typer.secho(f"Exception: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    typer.secho(f"Finished cdemgl for Point{coords}", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()
