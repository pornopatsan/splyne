import haversine

from typing import Callable, Optional

from splyne.common.base import SplyneObject


class GeoPoint(SplyneObject):

    MIN_LAT = -90.0
    MAX_LAT = +90.0
    MIN_LON = -180.0
    MAX_LON = +180.0

    def __init__(self, lat, lon):
        super().__init__()
        if not (GeoPoint.MIN_LAT <= lat <= GeoPoint.MAX_LAT):
            raise ValueError("Latitude must be in [-90.0, 90.0] interval")
        if not (GeoPoint.MIN_LON <= lon <= GeoPoint.MAX_LON):
            raise ValueError("Longitude must be in [-180.0, 180.0] interval")
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return "GeoPoint({lat:.6f}, {lon:6f})".format(lat=self.lat, lon=self.lon)

    @staticmethod
    def axiswise_aggregation(
        first: 'GeoPoint', second: 'GeoPoint',
        func: Callable[[float, float], float]
    ) -> 'GeoPoint':
        """
        Return new GeoPoint, applying `func` to both `lat` and `lon` of inputs
        You may prefet to use shortcuts fuctions such as `axiswise_min` and `axiswise_max`
        >>> GeoPoint.axiswise_aggregation(GeoPoint(55.5, 37.7), GeoPoint(60.0, 40.0), max)
        GeoPoint(60.000000, 40.000000)
        >>> GeoPoint.axiswise_aggregation(GeoPoint(55.5, 37.7), GeoPoint(50.0, 40.0), max)
        GeoPoint(55.500000, 40.000000)
        """
        return GeoPoint(func(first.lat, second.lat), func(first.lon, second.lon))

    @staticmethod
    def axiswise_min(first: 'GeoPoint', second: 'GeoPoint') -> 'GeoPoint':
        return GeoPoint.axiswise_aggregation(first, second, min)

    @staticmethod
    def axiswise_max(first: 'GeoPoint', second: 'GeoPoint') -> 'GeoPoint':
        return GeoPoint.axiswise_aggregation(first, second, max)


class BBox(SplyneObject):

    def __init__(
        self,
        ll_point: Optional[GeoPoint] = None,
        ur_point: Optional[GeoPoint] = None,
    ):
        """
        Initialize BBox with lower left corner and upper right corner.
        By default empty BBox is created, which you can initialize it later, by adding points to it.
        :param ll_point: lower left bound of BBox
        :param ur_point: upper right bound of BBox
        """
        super().__init__()
        if (ll_point is not None) and (ur_point is not None):
            self.ll_point = ll_point
            self.ur_point = ur_point
            self.initialized = True
        elif (ll_point is not None) or (ur_point is not None):
            raise ValueError("Bots BBox cornetts must be either None or GePoint")
        else:
            self.ll_point = GeoPoint(90.0, 180.0)
            self.ur_point = GeoPoint(-90.0, -180.0)
            self.initialized = False

    def __repr__(self):
        return 'BBox({}, {})'.format(self.ll_point, self.ur_point)

    def length(self, units: Optional[haversine.Unit] = haversine.Unit.KILOMETERS) -> float:
        """
        Git distance from lower left corner to upper right corner of bbox
        >>> '%.3f' % BBox(GeoPoint(55.748, 37.611), GeoPoint(55.757, 37.624)).length()
        '1.290'
        >>> '%.3f' % BBox(GeoPoint(-90.0, 0.0), GeoPoint(90.0, 180.0)).length()
        '20015.114'
        >>> '%.3f' % BBox(GeoPoint(0.0, 0.0), GeoPoint(0.0, 180.0)).length()
        '20015.114'
        >>> '%.3f' % BBox(GeoPoint(0.0, -180.0), GeoPoint(0.0, 180.0)).length()
        '0.000'
        """
        if self.initialized:
            return haversine.haversine(
                (self.ll_point.lat, self.ll_point.lon),
                (self.ur_point.lat, self.ur_point.lon),
                units
            )
        else:
            raise ValueError("BBox is uninitialized")

    def center(self) -> GeoPoint:
        """
        Get geometrical center of the BBox.
        >>> bb = BBox(GeoPoint(1.0, 1.0), GeoPoint(3.0, 5.0))
        >>> bb.center()
        GeoPoint(2.000000, 3.000000)
        """
        if self.initialized:
            return GeoPoint(
                (self.ll_point.lat + self.ur_point.lat) / 2,
                (self.ll_point.lon + self.ur_point.lon) / 2,
            )
        else:
            raise ValueError("BBox is uninitialized")

    def update_with_point(self, point: GeoPoint):
        """
        Updates BBox, to contain point inside it.
        If BBox is not initialized, initialize it.
        >>> bb = BBox(GeoPoint(1.0, 1.0), GeoPoint(3.0, 3.0))
        >>> bb.update_with_point(GeoPoint(3.5, 0.5))
        >>> bb
        BBox(GeoPoint(1.000000, 0.500000), GeoPoint(3.500000, 3.000000))
        >>> bb = BBox()
        >>> bb.update_with_point(GeoPoint(3.5, 0.5))
        >>> bb
        BBox(GeoPoint(3.500000, 0.500000), GeoPoint(3.500000, 0.500000))
        """
        self.ll_point = GeoPoint.axiswise_min(self.ll_point, point)
        self.ur_point = GeoPoint.axiswise_max(self.ur_point, point)
        self.initialized = True

    @staticmethod
    def merge(first: 'BBox', second: 'BBox') -> 'BBox':
        """
        Make this bbox bound both `self` and `other`
        >>> bb1 = BBox(GeoPoint(1.0, 1.0), GeoPoint(3.0, 3.0))
        >>> bb2 = BBox(GeoPoint(2.0, 2.0), GeoPoint(4.0, 4.0))
        >>> BBox.merge(bb1, bb2)
        BBox(GeoPoint(1.000000, 1.000000), GeoPoint(4.000000, 4.000000))
        >>> bb3 = BBox(GeoPoint(0.0, 0.0), GeoPoint(5.0, 5.0))
        >>> BBox.merge(bb1, bb3)
        BBox(GeoPoint(0.000000, 0.000000), GeoPoint(5.000000, 5.000000))
        """
        if not first.initialized and not second.initialized:
            raise ValueError("At least one GeoPoint must be initialized to merge them")
        return BBox(
            GeoPoint.axiswise_min(first.ll_point, second.ll_point),
            GeoPoint.axiswise_max(first.ur_point, second.ur_point),
        )
