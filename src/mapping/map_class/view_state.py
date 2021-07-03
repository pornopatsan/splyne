import pydeck
import haversine

from src.common.base import SplyneObject


class ViewState(SplyneObject):

    # Zoom levels from pydeck in degrees
    ZOOM_LEVELS = [
        360, 180, 90, 45, 22.5, 11.25, 5.625, 2.813, 1.406, 0.703,
        0.352, 0.176, 0.088, 0.044, 0.022, 0.011, 0.005, 0.003, 0.001, 0.0005,
    ]
    EQUATOR_LENGTH = 40000

    def __init__(self):
        super().__init__()

        self.max_lat, self.min_lat = 90, -90
        self.max_lon, self.min_lon = 180, -180

    def get_zoom(self):

        distance_km = haversine.haversine(
            (self.max_lat, self.max_lon), (self.min_lat, self.min_lon)
        )
        distance_degrees = 360 * distance_km / self.EQUATOR_LENGTH
        distance_degrees *= 1.2  # give some empty space shift in corners
        total_levels = len(self.ZOOM_LEVELS)

        if distance_degrees < self.ZOOM_LEVELS[-1]:
            return total_levels - 1

        for i in range(total_levels - 1):
            if self.ZOOM_LEVELS[i + 1] < distance_degrees <= self.ZOOM_LEVELS[i]:
                return i - 1

        return 0

    def get_view_state(self):
        center_lat = (self.max_lat + self.min_lat) / 2
        center_lon = (self.max_lon + self.min_lon) / 2
        zoom = self.get_zoom()

        return pydeck.ViewState(
            latitude=center_lat,
            longitude=center_lon,
            bearing=0, pitch=0,
            zoom=zoom,
        )


if __name__ == '__main__':
    viewState = ViewState()
