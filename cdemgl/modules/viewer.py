import os

import typer

outputs_dir = os.getenv("outputs_dir", "/tmp")


class VIEWER:
    def __init__(self, gltf_path):
        typer.secho("Creating HTML viewer", fg=typer.colors.MAGENTA)
        self.file_path = os.path.join(outputs_dir, "model", "viewer.html")
        self.html = self.create_html(gltf_path)

    def create_html(self, gltf_path):
        return (
            f"<style>\n"
            f"  model-viewer {{\n"
            f"    height: 100%;\n"
            f"    width: 100%;\n"
            f"    background-color:#064233;\n"
            f"  }}\n"
            f"</style>\n"
            f"<script type='module' "
            f"src='https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js'>"
            f"</script>\n"
            f"<script nomodule "
            f"src=h'ttps://unpkg.com/@google/model-viewer/dist/model-viewer-legacy.js'>"
            f"</script>\n"
            f"<model-viewer src='{os.path.basename(gltf_path)}' "
            f"alt='A 3D model' auto-rotate camera-controls>"
            f"</model-viewer>\n"
        )

    def save(self):
        with open(self.file_path, "w") as f:
            f.write(self.html)
            typer.echo(f"...Viewer written to: {self.file_path}")
