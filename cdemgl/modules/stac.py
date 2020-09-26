import json

import requests
import typer
from shapely.geometry import Polygon, box, shape

stac_api = "https://sat-api.developmentseed.org/stac/search"


def query_stac_api(bounds):
    typer.secho("Querying STAC...", fg=typer.colors.MAGENTA)
    bbox = [bounds.left, bounds.bottom, bounds.right, bounds.top]
    typer.echo(f"...Query BBOX: {bbox}")
    search_endpoint = stac_api
    body = {
        "limit": 1000,
        "bbox": bbox,
        "query": {
            "collection": {"eq": "landsat-8-l1"},
            "eo:cloud_cover": {"lt": 5, "gt": 0},
        },
    }
    response = requests.post(search_endpoint, data=json.dumps(body))
    typer.echo(f"...Query returned {len(response.json().get('features'))} features ")

    for feature in response.json().get("features"):
        geom = shape(feature.get("geometry"))
        bounds_geom = Polygon(box(*bounds))

        if geom.contains(bounds_geom):
            links = feature.get("links")
            item_link = [link.get("href") for link in links if link["rel"] == "self"][0]
            typer.echo(f"...Using item: {item_link}")
            typer.echo(
                f"...Thumbnail: {feature.get('assets').get('thumbnail').get('href')}"
            )
            return feature
