import pydeck

from splyne.common.base import SplyneObject
from splyne.mapping.common.view_state import ViewState
from splyne.mapping.layers import scatterplot


class Map(SplyneObject):

    def __init__(self):
        super().__init__()
        self.viewState = ViewState()
        self.layers = []

    def add_scatterplot_layer(self, data=None, lat='lat', lon='lon', color='color'):
        data = scatterplot.parse_data(data, lat=lat, lon=lon, color=color)
        scatterplot.update_view_state(self.viewState, data)
        layer = scatterplot.scatterplot_layer(data)
        self.layers.append(layer)

    def display(self):
        chart = pydeck.Deck(
            layers=self.layers,
            initial_view_state=self.viewState.get_view_state(),
            map_style=pydeck.map_styles.LIGHT,
        )
        return chart.to_html('.splyne-tmp.html')
