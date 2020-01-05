import inspect
from collections import OrderedDict
from itertools import chain

import libcst as cst
from libcst import MaybeSentinel, TrailingWhitespace, SimpleWhitespace, Newline

from astboom.visualizers.base import BaseVisualizer
from astboom.visualizers.utils import class_name


def is_fmt_node(element):
    return isinstance(element, (Newline, SimpleWhitespace, TrailingWhitespace))


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

            if not self.options["show_children"] and attr == "children":
                continue

            if self.options["hide_empty"] and (
                value in [[], (), "", None] or attr == "empty"
            ):
                continue

            if self.options["hide_fmt"] and "whitespace" in attr:
                continue

            if isinstance(value, cst.CSTNode):
                object_attrs += [
                    (
                        f"{attr}: libcst.{value.__class__.__name__}",
                        self._traverse(value),
                    )
                ]
            elif isinstance(value, (list, tuple)):
                if self.options["hide_fmt"]:
                    value = filter(lambda element: not is_fmt_node(element), value)

                traversed_items = {
                    f"[{i}] libcst.{item.__class__.__name__}": self._traverse(item)
                    for i, item in enumerate(value)
                }
                if traversed_items:
                    list_attrs += [(attr, traversed_items)]
                elif not self.options["hide_empty"]:
                    # Moving empty lists to the beginning of the list
                    # helps to prevent breaking up visual consistency.
                    list_attrs.insert(0, (f"{attr}: []", {}))
            elif isinstance(value, dict):
                traversed_items = {
                    f"[{key}] libcst.{value[key].__class__.__name__}": self._traverse(
                        value[key]
                    )
                    for key in value.keys()
                }
                list_attrs += [(attr, traversed_items)]
            else:
                if self.options["hide_default"] and value is MaybeSentinel.DEFAULT:
                    continue

                simple_attrs += [(f"{attr}: {repr(value)}", {})]

        for attr, value in chain(simple_attrs, list_attrs, object_attrs):
            result[attr] = value

        return result

    def process(self, source):
        module = cst.parse_module(source)
        return {f"libcst.{module.__class__.__name__}": self._traverse(module)}
