import ast
from collections import OrderedDict
from itertools import chain

from astboom.visualizers.base import BaseVisualizer


def class_name(value):
    value_cls = value.__class__
    return "<{0}.{1}>".format(value_cls.__module__, value_cls.__name__)


class VisualizeAST(BaseVisualizer):
    def _traverse(self, node):
        result = OrderedDict()

        simple_attrs, list_attrs, object_attrs = [], [], []

        if hasattr(node, "lineno") and not self.options.get("hide_pos", False):
            result[f"lineno: {node.lineno}"] = {}
            result[f"col_offset: {node.col_offset}"] = {}

        for attr, value in sorted(node.__dict__.items(), key=lambda p: p[0]):
            if attr in ("lineno", "col_offset"):
                continue

            if isinstance(value, ast.AST):
                object_attrs += [(attr, {class_name(value): self._traverse(value)})]
            elif isinstance(value, list):
                traversed_items = {
                    f"[{i}] {class_name(item)}": self._traverse(item)
                    for i, item in enumerate(value)
                }
                if traversed_items:
                    list_attrs += [(attr, traversed_items)]
                else:
                    # Moving empty lists to the beginning of the list
                    # helps to prevent breaking up visual consistency.
                    list_attrs.insert(0, (f"{attr}: []", {}))
            elif isinstance(value, dict):
                traversed_items = {
                    f"[{key}] {class_name(value[key])}": self._traverse(value[key])
                    for key in value.keys()
                }
                list_attrs += [(attr, traversed_items)]
            else:
                simple_attrs += [(f"{attr}: {value}", {})]

        for attr, value in chain(simple_attrs, list_attrs, object_attrs):
            result[attr] = value

        return result

    def process(self, source):
        module = ast.parse(source)
        return {class_name(module): self._traverse(module)}
