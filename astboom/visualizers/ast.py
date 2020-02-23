import ast
from collections import OrderedDict
from itertools import chain

from astboom.visualizers.base import BaseVisualizer
from astboom.visualizers.utils import class_name


class VisualizeAST(BaseVisualizer):
    def _traverse(self, node):
        result = OrderedDict()

        if node is None:
            return {"None": {}}

        simple_attrs, list_attrs, object_attrs = [], [], []
        hide_pos = self.options.get("hide_pos", False)
        hide_empty = self.options.get("hide_empty", False)

        if hasattr(node, "lineno") and not hide_pos:
            result[f"lineno: {node.lineno}"] = {}
            result[f"col_offset: {node.col_offset}"] = {}

        for attr, value in sorted(node.__dict__.items(), key=lambda p: p[0]):
            if attr in ("lineno", "col_offset"):
                continue

            if not value and hide_empty:
                continue

            if isinstance(value, ast.AST):
                object_attrs += [
                    (f"{attr}: {class_name(value)}", self._traverse(value))
                ]
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
                simple_attrs += [(f"{attr}: {repr(value)}", {})]

        for attr, value in chain(simple_attrs, list_attrs, object_attrs):
            result[attr] = value

        return result

    def process(self, source):
        module = ast.parse(source)
        return {class_name(module): self._traverse(module)}
