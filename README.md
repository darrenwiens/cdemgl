# cdemgl
Tool that creates glTF model from CDEM raster grid.

Elevation source: [CDEM FTP](http://ftp.geogratis.gc.ca/pub/nrcan_rncan/elevation/cdem_mnec/)

Imagery source: [sat-api](https://github.com/sat-utils/sat-api)

## Install
`pip install -r requirements.txt`

`pip install -e .`

## Environment Variables
- `download_dir`: root directory that will hold raw CDEM data
- `outputs_dir`: root directory that will store outputs (intermediate and final model)

`export download_dir='/path/for/cdem/data'`

`export outputs_dir='/path/for/outputs'`

## Usage
```
Usage: main.py [OPTIONS]

Options:
  --coords <FLOAT FLOAT>...       Longitude <space> Latitude  [default: None,
                                  None]

  --zfactor FLOAT                 Elevation stretch factor  [default: 1.0]
  --outsize INTEGER               Square output size, in pixels  [default:
                                  1000]

  --output TEXT                   Output format: gltf|glb  [default: glb]
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.
```

## Outputs
- `<outputs_dir>/intermediate`: various geographic/projected DEMs and images
- `<outputs_dir>/model`: gltf/bin or glb model, html viewer for model

## Examples
`python cdemgl/main.py --coords -118.439 52.135`

`python cdemgl/main.py --coords -118.439 52.135 --zfactor 2`

`python cdemgl/main.py --coords -118.439 52.135 --output gltf`

`python cdemgl/main.py --coords -123.069 49.337 --outsize 2000`

![Example result: Vancouver, BC](img/vancouver.gif)
