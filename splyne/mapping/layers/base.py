import abc

import pydeck

from splyne.common.base import SplyneObject


class BaseLayer(SplyneObject):

    def __init__(self):
        super().__init__()

    @abc.abstractmethod
    def make_pydeck_layer() -> pydeck.Layer:
        raise NotImplementedError()
