import copy

import pandas as pd
import pydeck

from splyne.mapping.common.view_state import ViewState
from splyne.mapping.layers.base import BaseLayer


DEFAULT_RADIUS = 10
DEFAULT_LINE_WIDTH = 1

DEFAULT_PARAMS = {
    'pickable': True,
    'stroked': True,
    'filled': True,
    'radius_min_pixels': DEFAULT_RADIUS,
    'radius_max_pixels': DEFAULT_RADIUS,
    'radius_scale': 10,
    'line_width_min_pixels ': 1,
    'line_width_max_pixels': 1,
    'get_position': ['lon', 'lat'],
    'get_radius': 100,
    'get_fill_color': 'color',
    'get_line_color': 'color',
}


class ScatterplotLayer(BaseLayer):

    def __init__(self):
        super().__init__()

    def make_pydeck_layer() -> pydeck.Layer:
        return None


def apply_common_parsing(data):
    return pd.DataFrame(data)


def add_column(data, name, value):
    data[name] = value


def parse_data(data, lat='lat', lon='lon', color='color', **kwargs):
    result = apply_common_parsing(data).copy()
    args = [('lat', lat), ('lon', lon), ('color', color)] + [(k, v) for k, v in kwargs.items()]

    for name, value in args:
        if isinstance(value, list) or hasattr(value, 'shape'):
            add_column(result, name, value)
        elif isinstance(value, str):
            if value in result:
                result[name] = result[value]
            else:
                if name == 'color':
                    result[name] = [[50, 20, 200] for _ in range(result.shape[0])]
                else:
                    result[name] = None
        else:
            raise ValueError(f'Can`t understand argument {name}')
    return result


def update_view_state(view_state: ViewState, data):
    points = data[['lat', 'lon']].to_dict('records')
    view_state.update(points)


def scatterplot_layer(data, **kwargs):
    pydeck_kwargs = copy.deepcopy(DEFAULT_PARAMS)
    pydeck_kwargs.update(kwargs)
    print(data, pydeck_kwargs)
    layer = pydeck.Layer("ScatterplotLayer", data=data.to_dict('records'), **pydeck_kwargs)
    return layer
