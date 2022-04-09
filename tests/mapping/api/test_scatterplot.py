import json

import pytest

from splyne.mapping.api import scatterplot

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
            "data": points_example_small,
            "getColor": [50, 20, 200], "filled": True,
            "getPosition": "@@=[lon, lat]", "getRadius": 100,
            "lineWidthMaxPixels": 1, "lineWidthMinPixels ": 1,
            "radiusMaxPixels": 10, "radiusMinPixels": 10, "radiusScale": 10,
            "pickable": True, "stroked": True,
        }],
        "mapProvider": "carto",
        "mapStyle": "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
        "views": [{"@@type": "MapView", "controller": True}]
    }
    result = scatterplot.scatterplot(
        data=points_example_small
    )
    common.assert_equal_jsons(json.loads(result), expected_result)


def test_scatterplot_formatted_medium(points_example_medium):
    expected_result = {
        "initialViewState": {
            "latitude": 54.849999999999994, "longitude": 36.55,
            "bearing": 0, "pitch": 0, "zoom": 6
        },
        "layers": [{
            "@@type": "ScatterplotLayer", "id": "",
            "data": points_example_medium,
            "getColor": '@@=color', "filled": True,
            "getPosition": "@@=[lon, lat]", "getRadius": 100,
            "lineWidthMaxPixels": 1, "lineWidthMinPixels ": 1,
            "radiusMaxPixels": 10, "radiusMinPixels": 10, "radiusScale": 10,
            "pickable": True, "stroked": True,
        }],
        "mapProvider": "carto",
        "mapStyle": "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
        "views": [{"@@type": "MapView", "controller": True}]
    }
    result = scatterplot.scatterplot(
        data=points_example_medium, hue='key'
    )
    common.assert_equal_jsons(json.loads(result), expected_result)


if __name__ == '__main__':
    scatterplot.scatterplot(
        data=[
            {'lat': 55.7, 'lon': 37.8, 'key': 1},
            {'lat': 56.4, 'lon': 35.9, 'key': 2},
            {'lat': 55.7, 'lon': 38.9, 'key': 2},
            {'lat': 55.9, 'lon': 34.2, 'key': 1},
            {'lat': 53.3, 'lon': 36.4, 'key': 3},
            {'lat': 55.9, 'lon': 37.7, 'key': 2},
            {'lat': 54.9, 'lon': 38.0, 'key': 1},
        ], hue='key'
    )
