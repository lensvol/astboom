class DictLikeList(object):
    def __init__(self):
        self.__contained = []

    def __setitem__(self, key, value):
        self.__contained.append((key, value))

    def items(self):
        return self.__contained
