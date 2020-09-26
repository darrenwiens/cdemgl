import operator
import os
import struct

import typer
from gltflib import (
    GLTF,
    Accessor,
    AccessorType,
    Asset,
    Attributes,
    Buffer,
    BufferTarget,
    BufferView,
    ComponentType,
    FileResource,
    GLTFModel,
    Image,
    Material,
    Mesh,
    Node,
    PBRMetallicRoughness,
    Primitive,
    Scene,
    Texture,
    TextureInfo,
)

outputs_dir = os.getenv("outputs_dir", "/tmp")


class GLTF_OBJ:
    def __init__(self, app_clipped_dem, app_image, output):
        typer.secho("Creating GLTF/GLB object...", fg=typer.colors.MAGENTA)
        self.gltf_path = os.path.join(outputs_dir, "model", f"map_model.{output}")
        self.data_path = "map_data.bin"
        self.png_path = app_image.png_path
        self.png_bounds = app_image.png_bounds
        self.gltf = self.create_gltf(app_clipped_dem)
        typer.echo(f"...GLTF/GLB object written to: {self.gltf_path}")

    def calc_lng_ratio(self, tile_minx, tile_maxx, x):
        return (x - tile_minx) / (tile_maxx - tile_minx)

    def calc_lat_ratio(self, tile_miny, tile_maxy, y):
        return (y - tile_miny) / (tile_maxy - tile_miny)

    def vertices_to_gltf(
        self,
        vertices,
        gltf_filename,
        data_name,
        rows,
        cols,
        xs,
        ys,
        png_bounds,
        png_filename,
    ):
        vertex_bytearray = bytearray()
        texcoord_bytearray = bytearray()
        buffer_views = []
        accessors = []
        materials = []
        meshes = []
        nodes = []
        node_list = []
        images = []
        textures = []
        index = 0
        for k, v in vertices.items():
            byte_offset = len(vertex_bytearray)

            for vertex in v:
                lnglat = (xs[int(vertex[0])], ys[rows - int(vertex[2]) - 1])
                for value in vertex:
                    vertex_bytearray.extend(struct.pack("f", value))
                texvalue = self.calc_lng_ratio(
                    png_bounds.left, png_bounds.right, lnglat[0]
                )
                texcoord_bytearray.extend(struct.pack("f", texvalue))
                texvalue = 1 - self.calc_lat_ratio(
                    png_bounds.bottom, png_bounds.top, lnglat[1]
                )
                texcoord_bytearray.extend(struct.pack("f", texvalue))

            mins = [
                min([operator.itemgetter(i)(vertex) for vertex in v]) for i in range(3)
            ]
            maxs = [
                max([operator.itemgetter(i)(vertex) for vertex in v]) for i in range(3)
            ]
            vertex_bytelen = len(vertex_bytearray)
            texcoord_bytelen = len(texcoord_bytearray)

            buffer_views.append(
                BufferView(
                    buffer=0,
                    byteOffset=byte_offset,
                    byteLength=vertex_bytelen + texcoord_bytelen,
                    target=BufferTarget.ARRAY_BUFFER.value,
                )
            )

            images.append(Image(uri=png_filename))
            accessors.append(
                Accessor(
                    bufferView=index,
                    byteOffset=0,
                    componentType=ComponentType.FLOAT.value,
                    count=len(v),
                    type=AccessorType.VEC3.value,
                    min=mins,
                    max=maxs,
                )
            )

            accessors.append(
                Accessor(
                    bufferView=index,
                    byteOffset=vertex_bytelen,
                    componentType=ComponentType.FLOAT.value,
                    count=len(v),
                    type=AccessorType.VEC2.value,
                )
            )

            textures.append(Texture(source=0))

            materials.append(
                Material(
                    doubleSided=True,
                    emissiveFactor=[0, 0, 0],
                    name=f"Material.{index}",
                    pbrMetallicRoughness=PBRMetallicRoughness(
                        baseColorTexture=TextureInfo(index=0),
                        metallicFactor=0.0,
                        roughnessFactor=1.0,
                    ),
                )
            )
            meshes.append(
                Mesh(
                    primitives=[
                        Primitive(
                            attributes=Attributes(POSITION=index, TEXCOORD_0=index + 1),
                            material=index,
                        )
                    ]
                )
            )
            nodes.append(Node(mesh=index))
            node_list.append(index)
            index += 1

        model = GLTFModel(
            asset=Asset(version="2.0"),
            scenes=[Scene(nodes=node_list)],
            nodes=nodes,
            materials=materials,
            meshes=meshes,
            buffers=[
                Buffer(byteLength=vertex_bytelen + texcoord_bytelen, uri=data_name)
            ],
            bufferViews=buffer_views,
            accessors=accessors,
            images=images,
            textures=textures,
        )

        resource = FileResource(data_name, data=vertex_bytearray + texcoord_bytearray)
        image_resource = FileResource(png_filename)
        gltf = GLTF(model=model, resources=[resource, image_resource])
        return gltf

    def create_gltf(self, app_clipped_dem):
        return self.vertices_to_gltf(
            app_clipped_dem.vertices,
            self.gltf_path,
            self.data_path,
            app_clipped_dem.height,
            app_clipped_dem.width,
            app_clipped_dem.x_idx,
            app_clipped_dem.y_idx,
            self.png_bounds,
            self.png_path,
        )

    def save(self):
        if self.gltf_path.endswith("glb"):
            self.gltf.export_glb(self.gltf_path)
        if self.gltf_path.endswith("gltf"):
            self.gltf.export_gltf(self.gltf_path)
