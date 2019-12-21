class DictLikeList(object):
    def __init__(self):
        self.__contained = []

    def __setitem__(self, key, value):
        self.__contained.append((key, value))

    def items(self):
        return self.__contained


def class_name(value):
    value_cls = value.__class__
    return "<{0}.{1}>".format(value_cls.__module__, value_cls.__name__)
