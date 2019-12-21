import inspect
from collections import OrderedDict
from itertools import chain

from astboom.visualizers.base import BaseVisualizer
import libcst as cst

from astboom.visualizers.utils import class_name


class VisualizeLibCST(BaseVisualizer):
    def _traverse(self, node):
        result = OrderedDict()

        simple_attrs, list_attrs, object_attrs = [], [], []

        for attr, value in chain(simple_attrs, list_attrs, object_attrs):
            result[attr] = value

        for attr, value in inspect.getmembers(node):
            if attr.startswith("_"):
                continue

            if callable(value):
                continue

            if isinstance(value, cst.CSTNode):
                object_attrs += [
                    (f"{attr}: {class_name(value)}", self._traverse(value))
                ]
            elif isinstance(value, (list, tuple)):
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
        module = cst.parse_module(source)
        return {class_name(module): self._traverse(module)}
