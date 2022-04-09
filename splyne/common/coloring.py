import copy
import itertools

from splyne.common.base import SplyneObject


COLORS = {
    'red':    [255, 0, 0],
    'green':  [0, 255, 0],
    'blue':   [0, 0, 255],
    'orange': [255, 255, 0],
    'purple': [255, 0, 255],
    'cyan':   [0, 255, 255],
    'grey':   [200, 200, 200],
}

DEFAULT_COLOR_SCHEMA = 'main'

COLOR_SCHEMAS = {
    'main': {
        'generator': itertools.cycle(copy.deepcopy(COLORS).values()),
        'mapping': COLORS
    }
}


class ColorGenerator(SplyneObject):

    def __init__(self, color_schema=DEFAULT_COLOR_SCHEMA):
        self.generator = COLOR_SCHEMAS[color_schema]['generator']
        self.mapping = COLOR_SCHEMAS[color_schema]['mapping']

    def next_color(self):
        return next(self.generator)

    def get_color(self, key):
        """
        Get color for given key. Remeber key and return same color for same keys
        >>> cgen = ColorGenerator()
        >>> cgen.get_color('k1')
        [255, 0, 0]
        >>> cgen.get_color('k2')
        [0, 255, 0]
        >>> cgen.get_color('k1')
        [255, 0, 0]
        >>> cgen.get_color('purple')
        [255, 0, 255]
        """
        if key in self.mapping:
            return self.mapping[key]
        color = self.next_color()
        self.mapping[key] = color
        return color
