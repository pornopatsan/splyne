"""
Some shortcut functions for mast common scenario.
Used for bref overview of data.
Supports different input formats.
"""

import copy

import pandas as pd

from typing import Iterable, Dict, Any, Union, Optional

from splyne.common.coloring import ColorGenerator
from splyne.mapping.map_class.map import Map
from splyne.utils import transformers


def transform_with_format_detection(
    data: Optional[Any] = None,
    lat: Optional[Union[str, Iterable]] = None,
    lon: Optional[Union[str, Iterable]] = None,
    color: Optional[Union[str, Iterable]] = None,
    size: Optional[Union[str, Iterable]] = None,
) -> Iterable[Dict[str, Any]]:
    """
    >>> data = [{'lat': 55.7, 'lon': 37.8}, {'lat': 55.8, 'lon': 37.9}]
    >>> list(transform_with_format_detection(data=data))
    [{'lat': 55.7, 'lon': 37.8}, {'lat': 55.8, 'lon': 37.9}]
    >>> data = [{'a': 55.7, 'b': 37.8}, {'a': 55.8, 'b': 37.9}]
    >>> list(transform_with_format_detection(data=data, lat='a', lon='b'))
    [{'lat': 55.7, 'lon': 37.8}, {'lat': 55.8, 'lon': 37.9}]
    >>> list(transform_with_format_detection(lat=[55.7, 55.8], lon=[37.8, 37.9]))
    [{'lat': 55.7, 'lon': 37.8}, {'lat': 55.8, 'lon': 37.9}]
    """
    if data is None:
        data = transformers.merge(lat=lat, lon=lon)
    elif isinstance(data, pd.DataFrame):
        data = data.to_dict('records')
    if isinstance(lat, str):
        data = transformers.rename(data, lat, 'lat')
    if isinstance(lon, str):
        data = transformers.rename(data, lon, 'lon')
    if color is not None:
        if isinstance(color, str):
            color_key = color
            cgen = ColorGenerator()
            color = (cgen.get_color(item[color_key]) for item in data)
        data = transformers.zip_into(data, "color", color)
    if size is not None:
        if isinstance(size, str):
            size_key = size
            size = (item[size_key] for item in data)
        data = transformers.zip_into(data, "size", size)
    return data


def scatterplot(
    data: Optional[Any] = None,
    lat: Optional[Union[str, Iterable]] = None,
    lon: Optional[Union[str, Iterable]] = None,
    color: Optional[Union[str, Iterable]] = None,
    size: Optional[Union[str, Iterable]] = None,
):
    """
    Possible input formats:
    1) `data` = pd.DataFrame or Iterable of Dicts.
    `x`, `y` = column names of Latitude and Longtitude.
    By default, columns names are `lat` and `lon`
    Examples:
    `>>> data = [{'lat': 55.7, 'lon': 37.8}, {'lat': 55.8, 'lon': 37.9}]
    `>>> scatterplot(data=data)
    `>>> data = [{'a': 55.7, 'b': 37.8}, {'a': 55.8, 'b': 37.9}]
    `>>> scatterplot(data=data, lon='b', lat='a')

    2) `lat`, `lon` = Iterable of float.
    `>>> scatterplot(lon=[37.8, 37.9], lat=[55.7, 55.8])
    """
    if data is None and (lat is None and lon is None):
        raise ValueError("No data provided.")
    elif data is None and (lat is None or lon is None):
        raise ValueError("Both `lon` and lat` must be provided (or None of them)")

    map = Map()
    data = copy.deepcopy(data)
    data = transform_with_format_detection(
        data=data, lat=lat, lon=lon,
        color=color, size=size
    )
    map.add_scatterplot_layer(data)
    return map.display()
