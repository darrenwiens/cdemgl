import json
import os
import zipfile
from ftplib import FTP
from pathlib import Path

import typer
from shapely.geometry import shape

# from tqdm import tqdm

ftp_loc = "ftp.geogratis.gc.ca"
download_loc = os.getenv("download_dir", "/tmp")


def download_ftp_file(ftp, file_size, src_file, dst_file):
    with open(dst_file, "wb") as fp:
        with typer.progressbar(
            label="Downloading", length=int(file_size * 1000000)
        ) as progress:

            def callback(data):
                data_len = len(data)
                progress.update(data_len)
                fp.write(data)

            ftp.retrbinary(f"RETR {src_file}", callback)


def download_dem(poi):
    pnt = poi.point

    with open(
        os.path.join(os.path.dirname(__file__), "../data/cdem_grid.geojson"), "r"
    ) as grid_geojson:
        grid = json.load(grid_geojson)
        for i in grid["features"]:
            poly = shape(i["geometry"])
            if pnt.intersects(poly):
                grid_feature = i
                break

    grid_code = grid_feature["properties"]["NTS_SNRC"]
    ftp_dir = f"pub/nrcan_rncan/elevation/cdem_mnec/{grid_code[:3]}"
    zip_name = f"cdem_dem_{grid_code}_tif.zip"
    download_zip_dir = f"{download_loc}/{grid_code[:3]}"
    download_zip_file = f"{download_zip_dir}/{zip_name}"
    download_tif_dir = f"{download_zip_dir}/{os.path.basename(download_zip_file)[:-4]}"
    download_tif_file = (
        f"{download_tif_dir}/{os.path.basename(download_zip_file)[:-8]}.tif"
    )

    typer.secho("Looking for local CDEM file...", fg=typer.colors.MAGENTA)

    if not os.path.isfile(download_tif_file):
        if not os.path.isfile(download_zip_file):
            typer.echo(f"...Local CDEM zip file does not exist: {download_zip_file}")
            typer.echo("...Connecting to CDEM ftp server")
            ftp = FTP(ftp_loc)
            try:
                typer.echo(f"...Connection: {ftp.login()}")
                ftp.cwd(ftp_dir)

                file_size = ftp.size(zip_name) / 1000000

                download = typer.confirm(
                    f"...CDEM zip file size is: {file_size} MB. Continue with download?"
                )

                if download:
                    Path(download_zip_dir).mkdir(parents=True, exist_ok=True)
                    download_ftp_file(ftp, file_size, zip_name, download_zip_file)
                    typer.secho(
                        "...CDEM zip file download complete", fg=typer.colors.GREEN
                    )
                else:
                    typer.secho(
                        "...CDEM zip file download aborted. Exiting...",
                        fg=typer.colors.YELLOW,
                    )
                    raise typer.Exit("CDEM zip file download aborted")
            except Exception as e:
                raise typer.Exit(e)
            finally:
                ftp.quit()
                typer.echo("...FTP connection closed")

        if os.path.isfile(download_zip_file):
            typer.echo(f"...Local CDEM zip exists: {download_zip_file}.")
            Path(download_tif_dir).mkdir(parents=True, exist_ok=True)
            typer.echo(f"...Unzipping CDEM: {download_zip_file}")
            with zipfile.ZipFile(download_zip_file, "r") as zip_ref:
                zip_ref.extractall(download_tif_dir)

    else:
        typer.secho(
            f"...Found local CDEM tif file: {download_tif_file}", fg=typer.colors.GREEN
        )

    return download_tif_file
