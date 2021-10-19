import pydeck
import haversine

from collections.abc import Iterable

from splyne.common.base import SplyneObject
from splyne.mapping.common.common import BBox, GeoPoint


class ViewState(SplyneObject):

    # Zoom levels from pydeck in degrees
    ZOOM_LEVELS = [
        360, 180, 90, 45, 22.5, 11.25, 5.625, 2.813, 1.406, 0.703,
        0.352, 0.176, 0.088, 0.044, 0.022, 0.011, 0.005, 0.003, 0.001, 0.0005,
    ]

    def __init__(self):
        """
        View State object.
        Designed to accumulate data, and automatically generate initial pydeck.ViewState,
        which will cover all data in chart.
        """
        super().__init__()
        self.bbox = BBox()

    def get_zoom_level(self):
        """
        Get initial zoom level for pydeck, to cever whole BBox.
        >>> vs = ViewState()
        >>> vs.get_zoom_level()
        0
        >>> vs.update(GeoPoint(55.5, 37.7))
        >>> vs.get_zoom_level()
        19
        >>> vs.update(GeoPoint(55.8, 37.8))
        >>> vs.get_zoom_level()
        9
        >>> vs.update(GeoPoint(90.0, 180.0))
        >>> vs.get_zoom_level()
        3
        >>> vs.update(GeoPoint(-90.0, -180.0))
        >>> vs.get_zoom_level()
        0
        """
        if not self.bbox.initialized:
            return 0

        distance_degrees = self.bbox.length(units=haversine.Unit.DEGREES)
        distance_degrees *= 1.2  # Give some empty space shift in corners
        total_levels = len(ViewState.ZOOM_LEVELS)

        if distance_degrees < ViewState.ZOOM_LEVELS[-1]:
            return total_levels - 1
        for i in range(total_levels - 1):
            if self.ZOOM_LEVELS[i + 1] <= distance_degrees < ViewState.ZOOM_LEVELS[i]:
                return i
        return 0

    def get_view_state(self) -> pydeck.ViewState:
        center = self.bbox.center()
        zoom = self.get_zoom_level()
        return pydeck.ViewState(
            latitude=center.lat,
            longitude=center.lon,
            bearing=0, pitch=0,
            zoom=zoom,
        )

    def update(self, point: GeoPoint):
        self.bbox.update_with_point(point)

    def update_multiple(self, points: Iterable[GeoPoint]):
        for point in points:
            self.update(point)
