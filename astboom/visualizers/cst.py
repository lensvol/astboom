from lib2to3 import pygram, pytree
from lib2to3.pgen2 import driver, token
from lib2to3.pytree import Node, type_repr

from astboom.visualizers.base import BaseVisualizer
from astboom.visualizers.utils import DictLikeList


class VisualizeCST(BaseVisualizer):
    def _traverse(self, node):
        result = DictLikeList()

        for child in node.children:
            if isinstance(child, Node):
                result[type_repr(child.type)] = self._traverse(child)
            else:
                if self.options["show_prefix"]:
                    value = f"{repr(child.prefix)} {repr(child.value)}"
                else:
                    value = f"{repr(child.value)}"
                result[f"{token.tok_name[child.type]}: {value}"] = {}
        return result

    def process(self, source):
        drv = driver.Driver(pygram.python_grammar_no_print_statement, pytree.convert)
        if "\n" not in source:
            source += "\n"

        tree = drv.parse_string(source)
        return {"file_input": self._traverse(tree)}
