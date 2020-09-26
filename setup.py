from setuptools import find_packages, setup

setup(
    name="cdemgl",
    description="Tool that creates glTF model from CDEM raster grid",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "main=cdemgl.main:app",
        ]
    },
)
