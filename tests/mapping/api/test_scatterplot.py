import enum
import json

import pytest

from splyne import scatterplot

import tests.common as common


def setup_module(module):
    common.mock_prepare_deck_class()


def teardown_module(module):
    pass


@pytest.fixture
def points_example_small():
    return [
        {'lat': 55.7, 'lon': 37.8},
        {'lat': 55.8, 'lon': 37.9},
    ]


@pytest.fixture
def points_example_medium():
    return [
        {'lat': 55.7, 'lon': 37.8, 'key': 1},
        {'lat': 56.4, 'lon': 35.9, 'key': 2},
        {'lat': 55.7, 'lon': 38.9, 'key': 2},
        {'lat': 55.9, 'lon': 34.2, 'key': 1},
        {'lat': 53.3, 'lon': 36.4, 'key': 3},
        {'lat': 55.9, 'lon': 37.7, 'key': 2},
        {'lat': 54.9, 'lon': 38.0, 'key': 1},
    ]


def test_scatterplot_formatted_small(points_example_small):
    expected_result = {
        "initialViewState": {
            "latitude": 55.75, "longitude": 37.849999999999994,
            "bearing": 0, "pitch": 0, "zoom": 11
        },
        "layers": [{
            "@@type": "ScatterplotLayer", "id": "",
            "data": [
                {'lat': 55.7, 'lon': 37.8},
                {'lat': 55.8, 'lon': 37.9}
            ],
            "getColor": [50, 20, 200], "filled": True,
            "getPosition": "@@=[lon, lat]", "lineWidthMaxPixels": 1, "lineWidthMinPixels ": 1,
            "getRadius": 100, "radiusMaxPixels": 10, "radiusMinPixels": 10, "radiusScale": 10,
            "pickable": True, "stroked": True,
        }],
        "mapProvider": "carto",
        "mapStyle": "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
        "views": [{"@@type": "MapView", "controller": True}]
    }
    result = scatterplot(
        data=points_example_small
    )
    common.assert_equal_jsons(json.loads(result), expected_result)


def test_scatterplot_formatted_medium(points_example_medium):
    expected_result = {
        "initialViewState": {
            "latitude": 54.849999999999994, "longitude": 36.55,
            "pitch": 0, "zoom": 6, "bearing": 0,
        }, "layers": [{
            "@@type": "ScatterplotLayer",
            "data": [
                {"color": [0, 0, 255], "key": 1, "lat": 55.7, "lon": 37.8},
                {"color": [255, 255, 0], "key": 2, "lat": 56.4, "lon": 35.9},
                {"color": [255, 255, 0], "key": 2, "lat": 55.7, "lon": 38.9},
                {"color": [0, 0, 255], "key": 1, "lat": 55.9, "lon": 34.2},
                {"color": [255, 0, 255], "key": 3, "lat": 53.3, "lon": 36.4},
                {"color": [255, 255, 0], "key": 2, "lat": 55.9, "lon": 37.7},
                {"color": [0, 0, 255], "key": 1, "lat": 54.9, "lon": 38.0},
            ],
            "id": "", "getPosition": "@@=[lon, lat]",
            "filled": True, "getColor": "@@=color",
            "getRadius": 100, "radiusMaxPixels": 10, "radiusMinPixels": 10, "radiusScale": 10,
            "lineWidthMaxPixels": 1, "lineWidthMinPixels ": 1,
            "pickable": True, "stroked": True,
        }],
        "mapProvider": "carto",
        "mapStyle": "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
        "views": [{"@@type": "MapView", "controller": True}]
    }
    result = scatterplot(
        data=points_example_medium, color='key',
    )
    common.assert_equal_jsons(json.loads(result), expected_result)
