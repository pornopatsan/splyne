import logging
import warnings


class SplyneObject(object):
    """
    Base Class for all splyne classes
    """

    def __init__(self):

        formatter = logging.Formatter(u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        handler.setLevel(logging.WARNING)

        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(handler)
        self.warner = warnings