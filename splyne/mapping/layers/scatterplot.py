import copy
import functools

import pydeck

from typing import Iterable, Any

from splyne.mapping.common.common import GeoPoint
from splyne.mapping.common.view_state import ViewState
from splyne.mapping.layers.base import BaseLayer
from splyne.utils.transformers import make_pipe


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

        data_tranformer = make_pipe(
            copy.deepcopy,
            functools.partial(self._update_view_state, view_state=view_state),
            self._update_kwargs,
        )
        self.data = data_tranformer(data)

    def _update_kwargs(self, item: Any) -> Any:
        if 'color' in item:
            self.pydeck_kwargs['get_color'] = 'color'
        if 'size' in item:
            self.pydeck_kwargs['get_color'] = 'size'
        return item

    def _update_view_state(self, item: Any, view_state: ViewState) -> Any:
        view_state.update(GeoPoint(item['lat'], item['lon']))
        return item

    def _update_view_state_from_iter(self, data: Iterable[Any], view_state: ViewState):
        for item in data:
            yield self._update_view_state(item, view_state)

    def make_pydeck_layer(self) -> pydeck.Layer:
        return pydeck.Layer("ScatterplotLayer", data=list(self.data), **self.pydeck_kwargs)
