import typer
from shapely.geometry import Point


class POI:
    def __init__(self, coords):
        typer.secho(f"Creating POI object at {tuple(coords)}", fg=typer.colors.MAGENTA)
        self.point = Point(*coords)
