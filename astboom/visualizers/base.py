class BaseVisualizer(object):
    def __init__(self, options=None):
        self.options = options or {}

    def process(self, source):
        raise NotImplemented
