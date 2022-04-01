"""
Some shortcut functions for mast common scenario.
Used for bref overview of data.
Supports different input formats.
"""

from typing import Iterable, Dict, Any

from splyne.mapping.map_class.map import Map
from splyne.utils import transformers


def transform_with_format_detection(
    data=None,
    x=None,
    y=None,
    hue=None,
    colors=None,
    sizes=None,
) -> Iterable[Dict[str, Any]]:
    """
    >>> data = [{'lat': 55.7, 'lon': 37.8}, {'lat': 55.8, 'lon': 37.9}]
    >>> list(transform_with_format_detection(data=data))
    [{'lat': 55.7, 'lon': 37.8}, {'lat': 55.8, 'lon': 37.9}]
    >>> data = [{'a': 55.7, 'b': 37.8}, {'a': 55.8, 'b': 37.9}]
    >>> list(transform_with_format_detection(data=data, x='a', y='b'))
    [{'lat': 55.7, 'lon': 37.8}, {'lat': 55.8, 'lon': 37.9}]
    >>> list(transform_with_format_detection(x=[55.7, 55.8], y=[37.8, 37.9]))
    [{'lat': 55.7, 'lon': 37.8}, {'lat': 55.8, 'lon': 37.9}]
    """
    if data is None:
        data = transformers.merge(lat=x, lon=y)
    if isinstance(x, str):
        data = transformers.rename(data, x, 'lat')
    if isinstance(y, str):
        data = transformers.rename(data, y, 'lon')
    if colors is not None:
        data = transformers.zip_into(data, "color", colors)
    if sizes is not None:
        data = transformers.zip_into(data, "size", sizes)
    return data


def scatterplot(
    data=None,
    x=None,
    y=None,
    hue=None,
    colors=None,
    sizes=None,
    **kwargs
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
    `>>> scatterplot(data=data, x='b', y='a')

    2) `x`, `y` = pd.Series or Iterable of float.
    `>>> scatterplot(x=[37.8, 37.9], y=[55.7, 55.8])

    3) `data` = iterable of lists/tuples
    """
    if data is None and x is None and y is None:
        raise ValueError("No data provided.")
    elif data is None and (x is None or y is None):
        raise ValueError("Both `x` and `y` must be provided")

    map = Map()
    data = transform_with_format_detection(data, x, y,  hue, colors, sizes)
    map.add_scatterplot_layer(data, **kwargs)
    map.display()
