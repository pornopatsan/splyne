import copy

import pydeck

from collections.abc import Iterable
from typing import Any

from splyne.mapping.common.common import GeoPoint
from splyne.mapping.common.view_state import ViewState
from splyne.mapping.layers.base import BaseLayer


class ScatterplotLayer(BaseLayer):

    DEFAULT_RADIUS = 10
    DEFAULT_LINE_WIDTH = 1
    DEFAULT_COLOR = [50, 20, 200]

    DEFAULT_PARAMS = {
        'pickable': True,
        'stroked': True,
        'filled': True,
        'radius_min_pixels': DEFAULT_RADIUS,
        'radius_max_pixels': DEFAULT_RADIUS,
        'radius_scale': 10,
        'line_width_min_pixels ': DEFAULT_LINE_WIDTH,
        'line_width_max_pixels': DEFAULT_LINE_WIDTH,
        'get_position': ['lon', 'lat'],
        'get_radius': 100,
        'get_color': DEFAULT_COLOR,
    }

    def __init__(
        self,
        data: Iterable[Any],
        view_state: ViewState,
        **kwargs,
    ):
        super().__init__()
        self.pydeck_kwargs = ScatterplotLayer.DEFAULT_PARAMS
        self.pydeck_kwargs.update(kwargs)

        # Parse Data
        self.data = copy.deepcopy(data)
        self.data = self._update_view_state(self.data, view_state)

    def _update_view_state(self, data: Iterable[Any], view_state: ViewState):
        for item in data:
            view_state.update(GeoPoint(item['lat'], item['lon']))
            yield item

    def make_pydeck_layer(self) -> pydeck.Layer:
        return pydeck.Layer("ScatterplotLayer", data=list(self.data), **self.pydeck_kwargs)
