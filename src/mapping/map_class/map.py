import pydeck

from src.common.base import SplyneObject
from src.mapping.map_class.view_state import ViewState
from src.mapping.layers import scatterplot


class Map(SplyneObject):

    def __init__(self):
        super().__init__()
        self.viewState = ViewState()
        self.layers = []

    def add_scatterplot_layer(self, data, lat='lat', lon='lon', color='color'):
        data = scatterplot.parse_data(data, lat=lat, lon=lon, color=color)
        layer = scatterplot.scatterplot_layer(data)
        self.layers.append(layer)

    def display(self):
        chart = pydeck.Deck(
            layers=self.layers,
            initial_view_state=self.viewState.get_view_state(),
        )
        chart.to_html('.splyne-tmp.html')


if __name__ == '__main__':
    chart = Map()
    chart.logger.error('TestFromMap')
