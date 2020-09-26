import pytest


@pytest.fixture(autouse=True)
def test_stac_query(requests_mock, test_stac_item):
    requests_mock.post(
        "https://sat-api.developmentseed.org/stac/search",
        json=test_stac_item,
        status_code=200,
    )


@pytest.fixture
def test_stac_item():
    return {
        "type": "FeatureCollection",
        "meta": {"page": 1, "limit": 11, "found": 12844196, "returned": 1},
        "features": [
            {
                "type": "Feature",
                "id": "LC80470252020211",
                "bbox": [-123.86872, 49.18142, -120.48831, 51.34815],
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [-123.15340385282063, 51.346625525179384],
                            [-120.49170303088624, 50.90883700870697],
                            [-121.2081252700906, 49.18352447118945],
                            [-123.86513554344056, 49.630774000717594],
                            [-123.15340385282063, 51.346625525179384],
                        ]
                    ],
                },
                "properties": {
                    "collection": "landsat-8-l1",
                    "eo:gsd": 15,
                    "eo:platform": "landsat-8",
                    "eo:instrument": "OLI_TIRS",
                    "eo:off_nadir": 0,
                    "eo:bands": [
                        {
                            "name": "B1",
                            "common_name": "coastal",
                            "gsd": 30,
                            "center_wavelength": 0.44,
                            "full_width_half_max": 0.02,
                        },
                        {
                            "name": "B2",
                            "common_name": "blue",
                            "gsd": 30,
                            "center_wavelength": 0.48,
                            "full_width_half_max": 0.06,
                        },
                        {
                            "name": "B3",
                            "common_name": "green",
                            "gsd": 30,
                            "center_wavelength": 0.56,
                            "full_width_half_max": 0.06,
                        },
                        {
                            "name": "B4",
                            "common_name": "red",
                            "gsd": 30,
                            "center_wavelength": 0.65,
                            "full_width_half_max": 0.04,
                        },
                        {
                            "name": "B5",
                            "common_name": "nir",
                            "gsd": 30,
                            "center_wavelength": 0.86,
                            "full_width_half_max": 0.03,
                        },
                        {
                            "name": "B6",
                            "common_name": "swir16",
                            "gsd": 30,
                            "center_wavelength": 1.6,
                            "full_width_half_max": 0.08,
                        },
                        {
                            "name": "B7",
                            "common_name": "swir22",
                            "gsd": 30,
                            "center_wavelength": 2.2,
                            "full_width_half_max": 0.2,
                        },
                        {
                            "name": "B8",
                            "common_name": "pan",
                            "gsd": 15,
                            "center_wavelength": 0.59,
                            "full_width_half_max": 0.18,
                        },
                        {
                            "name": "B9",
                            "common_name": "cirrus",
                            "gsd": 30,
                            "center_wavelength": 1.37,
                            "full_width_half_max": 0.02,
                        },
                        {
                            "name": "B10",
                            "common_name": "lwir11",
                            "gsd": 100,
                            "center_wavelength": 10.9,
                            "full_width_half_max": 0.8,
                        },
                        {
                            "name": "B11",
                            "common_name": "lwir12",
                            "gsd": 100,
                            "center_wavelength": 12,
                            "full_width_half_max": 1,
                        },
                    ],
                    "datetime": "2020-07-29T19:00:58.552330+00:00",
                    "eo:sun_azimuth": 148.29124577,
                    "eo:sun_elevation": 54.93073772,
                    "eo:cloud_cover": 4,
                    "eo:row": "025",
                    "eo:column": "047",
                    "landsat:product_id": "LC08_L1TP_047025_20200729_20200807_01_T1",
                    "landsat:scene_id": "LC80470252020211LGN00",
                    "landsat:processing_level": "L1TP",
                    "landsat:tier": "T1",
                    "landsat:revision": "00",
                    "eo:epsg": 32610,
                },
                "assets": {
                    "index": {
                        "type": "text/html",
                        "title": "HTML index page",
                        "href": "https://landsat-pds.s3.amazonaws.com/c1/L8/047/025/LC08_L1TP_047025_20200729_20200807_01_T1/LC08_L1TP_047025_20200729_20200807_01_T1_MTL.txt",
                    },
                    "thumbnail": {
                        "title": "Thumbnail image",
                        "type": "image/jpeg",
                        "href": "https://landsat-pds.s3.amazonaws.com/c1/L8/047/025/LC08_L1TP_047025_20200729_20200807_01_T1/LC08_L1TP_047025_20200729_20200807_01_T1_thumb_large.jpg",
                    },
                    "B1": {
                        "type": "image/x.geotiff",
                        "eo:bands": [0],
                        "title": "Band 1 (coastal)",
                        "href": "https://landsat-pds.s3.amazonaws.com/c1/L8/047/025/LC08_L1TP_047025_20200729_20200807_01_T1/LC08_L1TP_047025_20200729_20200807_01_T1_B1.TIF",
                    },
                    "B2": {
                        "type": "image/x.geotiff",
                        "eo:bands": [1],
                        "title": "Band 2 (blue)",
                        "href": "https://landsat-pds.s3.amazonaws.com/c1/L8/047/025/LC08_L1TP_047025_20200729_20200807_01_T1/LC08_L1TP_047025_20200729_20200807_01_T1_B2.TIF",
                    },
                    "B3": {
                        "type": "image/x.geotiff",
                        "eo:bands": [2],
                        "title": "Band 3 (green)",
                        "href": "https://landsat-pds.s3.amazonaws.com/c1/L8/047/025/LC08_L1TP_047025_20200729_20200807_01_T1/LC08_L1TP_047025_20200729_20200807_01_T1_B3.TIF",
                    },
                    "B4": {
                        "type": "image/x.geotiff",
                        "eo:bands": [3],
                        "title": "Band 4 (red)",
                        "href": "https://landsat-pds.s3.amazonaws.com/c1/L8/047/025/LC08_L1TP_047025_20200729_20200807_01_T1/LC08_L1TP_047025_20200729_20200807_01_T1_B4.TIF",
                    },
                    "B5": {
                        "type": "image/x.geotiff",
                        "eo:bands": [4],
                        "title": "Band 5 (nir)",
                        "href": "https://landsat-pds.s3.amazonaws.com/c1/L8/047/025/LC08_L1TP_047025_20200729_20200807_01_T1/LC08_L1TP_047025_20200729_20200807_01_T1_B5.TIF",
                    },
                    "B6": {
                        "type": "image/x.geotiff",
                        "eo:bands": [5],
                        "title": "Band 6 (swir16)",
                        "href": "https://landsat-pds.s3.amazonaws.com/c1/L8/047/025/LC08_L1TP_047025_20200729_20200807_01_T1/LC08_L1TP_047025_20200729_20200807_01_T1_B6.TIF",
                    },
                    "B7": {
                        "type": "image/x.geotiff",
                        "eo:bands": [6],
                        "title": "Band 7 (swir22)",
                        "href": "https://landsat-pds.s3.amazonaws.com/c1/L8/047/025/LC08_L1TP_047025_20200729_20200807_01_T1/LC08_L1TP_047025_20200729_20200807_01_T1_B7.TIF",
                    },
                    "B8": {
                        "type": "image/x.geotiff",
                        "eo:bands": [7],
                        "title": "Band 8 (pan)",
                        "href": "https://landsat-pds.s3.amazonaws.com/c1/L8/047/025/LC08_L1TP_047025_20200729_20200807_01_T1/LC08_L1TP_047025_20200729_20200807_01_T1_B8.TIF",
                    },
                    "B9": {
                        "type": "image/x.geotiff",
                        "eo:bands": [8],
                        "title": "Band 9 (cirrus)",
                        "href": "https://landsat-pds.s3.amazonaws.com/c1/L8/047/025/LC08_L1TP_047025_20200729_20200807_01_T1/LC08_L1TP_047025_20200729_20200807_01_T1_B9.TIF",
                    },
                    "B10": {
                        "type": "image/x.geotiff",
                        "eo:bands": [9],
                        "title": "Band 10 (lwir)",
                        "href": "https://landsat-pds.s3.amazonaws.com/c1/L8/047/025/LC08_L1TP_047025_20200729_20200807_01_T1/LC08_L1TP_047025_20200729_20200807_01_T1_B10.TIF",
                    },
                    "B11": {
                        "type": "image/x.geotiff",
                        "eo:bands": [10],
                        "title": "Band 11 (lwir)",
                        "href": "https://landsat-pds.s3.amazonaws.com/c1/L8/047/025/LC08_L1TP_047025_20200729_20200807_01_T1/LC08_L1TP_047025_20200729_20200807_01_T1_B11.TIF",
                    },
                    "ANG": {
                        "title": "Angle coefficients file",
                        "type": "text/plain",
                        "href": "https://landsat-pds.s3.amazonaws.com/c1/L8/047/025/LC08_L1TP_047025_20200729_20200807_01_T1/LC08_L1TP_047025_20200729_20200807_01_T1_ANG.txt",
                    },
                    "MTL": {
                        "title": "original metadata file",
                        "type": "text/plain",
                        "href": "https://landsat-pds.s3.amazonaws.com/c1/L8/047/025/LC08_L1TP_047025_20200729_20200807_01_T1/LC08_L1TP_047025_20200729_20200807_01_T1_MTL.txt",
                    },
                    "BQA": {
                        "title": "Band quality data",
                        "type": "image/x.geotiff",
                        "href": "https://landsat-pds.s3.amazonaws.com/c1/L8/047/025/LC08_L1TP_047025_20200729_20200807_01_T1/LC08_L1TP_047025_20200729_20200807_01_T1_BQA.TIF",
                    },
                },
                "links": [
                    {
                        "rel": "self",
                        "href": "https://sat-api.developmentseed.org/collections/landsat-8-l1/items/LC80470252020211",
                    },
                    {
                        "rel": "parent",
                        "href": "https://sat-api.developmentseed.org/collections/landsat-8-l1",
                    },
                    {
                        "rel": "collection",
                        "href": "https://sat-api.developmentseed.org/collections/landsat-8-l1",
                    },
                    {"rel": "root", "href": "https://sat-api.developmentseed.org/stac"},
                ],
            }
        ],
    }
