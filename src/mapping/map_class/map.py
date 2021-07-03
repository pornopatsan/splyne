from src.common.base import SplyneObject


class Map(SplyneObject):

    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    chart = Map()
    chart.logger.error('TestFromMap')
