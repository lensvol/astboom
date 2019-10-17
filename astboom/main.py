import ast
from collections import OrderedDict
from itertools import chain

import click
from asciitree import LeftAligned
from asciitree.drawing import BOX_HEAVY, BoxStyle

box_tr = LeftAligned(draw=BoxStyle(gfx=BOX_HEAVY, horiz_len=1, indent=2))


def class_name(value):
    return "<{0}.{1}>".format(value.__class__.__module__, value.__class__.__name__)


def traverse(node):
    result = OrderedDict()

    simple_attrs, list_attrs, object_attrs = [], [], []

    if hasattr(node, "lineno"):
        result["lineno: " + str(node.lineno)] = {}
        result["col_offset: " + str(node.col_offset)] = {}

    for attr, value in sorted(node.__dict__.items(), key=lambda p: p[0]):
        if attr in ("lineno", "col_offset"):
            continue

        if isinstance(value, ast.AST):
            object_attrs.append((attr, {class_name(value): traverse(value)}))
        elif isinstance(value, list):
            traversed_items = {
                "[{0}] {1}".format(i, class_name(item)): traverse(item)
                for i, item in enumerate(value)
            }
            list_attrs.append((attr, traversed_items))
        elif isinstance(value, dict):
            traversed_items = {
                "[{0}] {1}".format(key, class_name(value[key])): traverse(value[key])
                for key in value.keys()
            }
            list_attrs.append((attr, traversed_items))
        else:
            simple_attrs.append((attr + ": " + str(value), {}))

    for attr, value in chain(simple_attrs, list_attrs, object_attrs):
        result[attr] = value

    return result


@click.command()
@click.argument("source_file", type=click.File("r"))
def cli(source_file):
    module = ast.parse(source_file.read())

    print(box_tr({module.__class__.__name__: traverse(module)}))


if __name__ == "__main__":
    cli()
