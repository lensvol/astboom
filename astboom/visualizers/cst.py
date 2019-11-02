from lib2to3 import pygram, pytree
from lib2to3.pgen2 import driver, token
from lib2to3.pytree import Node, type_repr

from astboom.visualizers.base import BaseVisualizer


class DictLikeList(object):
    def __init__(self):
        self.__contained = []

    def __setitem__(self, key, value):
        self.__contained.append((key, value))

    def items(self):
        return self.__contained


class VisualizeCST(BaseVisualizer):
    def _traverse(self, node):
        result = DictLikeList()

        for child in node.children:
            if isinstance(child, Node):
                result[type_repr(child.type)] = self._traverse(child)
            else:
                result[f"{token.tok_name[child.type]}: {repr(child.value)}"] = {}

        return result

    def process(self, source):
        drv = driver.Driver(pygram.python_grammar_no_print_statement, pytree.convert)
        if "\n" not in source:
            source += "\n"

        tree = drv.parse_string(source)
        return {"file_input": self._traverse(tree)}
