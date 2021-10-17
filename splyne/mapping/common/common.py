import haversine

from typing import Callable

from splyne.common.base import SplyneObject

class GeoPoint(SplyneObject):

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        super().__init__()

    def __repr__(self):
        return "GeoPoint({lat:.6f}, {lon:6f})".format(lat=self.lat, lon=self.lon)

    @staticmethod
    def axiswise_aggregation(
        first: 'GeoPoint', second: 'GeoPoint', 
        func: Callable[[float, float], float]
    ) -> 'GeoPoint':
        """
        Return new GeoPoint, applying `func` to both `lat` and `lon` of inputs
        You may prefet to use shortcuts fuctions such as 
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

    def __init__(self, ll_point: GeoPoint, ur_point: GeoPoint):
        """
        :param ll_point: lower left bound of BBox
        :param ur_point: upper right bound of BBox
        """
        super().__init__()
        self.ll_point = ll_point
        self.ur_point = ur_point

    def __repr__(self):
        return 'BBox({}, {})'.format(self.ll_point, self.ur_point)

    def length(self) -> float:
        """
        Git distance from lower left corner to upper right corner of bbox
        >>> '%.3f' % BBox(GeoPoint(55.748, 37.611), GeoPoint(55.757, 37.624)).length()
        '1.290'
        >>> '%.3f' % BBox(GeoPoint(-90.0, 0.0), GeoPoint(90.0, 180.0)).length()
        '20015.114'
        >>> '%.3f' % BBox(GeoPoint(0.0, 0.0), GeoPoint(0.0, 180.0)).length()
        '20015.114'
        >>> '%.3f' % BBox(GeoPoint(0.0, 0.0), GeoPoint(0.0, 360.0)).length()
        '0.000'
        """
        return haversine.haversine(
            (self.ll_point.lat, self.ll_point.lon),
            (self.ur_point.lat, self.ur_point.lon),
            haversine.Unit.KILOMETERS
        )
    
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
        return BBox(
            GeoPoint.axiswise_min(first.ll_point, second.ll_point),
            GeoPoint.axiswise_max(first.ur_point, second.ur_point),
        )
