import ast
import sys
from collections import OrderedDict
from itertools import chain

import click
from asciitree import LeftAligned
from asciitree.drawing import BOX_HEAVY, BoxStyle

box_tr = LeftAligned(draw=BoxStyle(gfx=BOX_HEAVY, horiz_len=1, indent=2))


def class_name(value):
    return "<{0}.{1}>".format(value.__class__.__module__, value.__class__.__name__)


def traverse(node, show_pos=True):
    result = OrderedDict()

    simple_attrs, list_attrs, object_attrs = [], [], []

    if hasattr(node, "lineno") and not show_pos:
        result["lineno: " + str(node.lineno)] = {}
        result["col_offset: " + str(node.col_offset)] = {}

    for attr, value in sorted(node.__dict__.items(), key=lambda p: p[0]):
        if attr in ("lineno", "col_offset"):
            continue

        if isinstance(value, ast.AST):
            object_attrs.append(
                (attr, {class_name(value): traverse(value, show_pos=show_pos)})
            )
        elif isinstance(value, list):
            traversed_items = {
                "[{0}] {1}".format(i, class_name(item)): traverse(
                    item, show_pos=show_pos
                )
                for i, item in enumerate(value)
            }
            list_attrs.append((attr, traversed_items))
        elif isinstance(value, dict):
            traversed_items = {
                "[{0}] {1}".format(key, class_name(value[key])): traverse(
                    value[key], show_pos=show_pos
                )
                for key in value.keys()
            }
            list_attrs.append((attr, traversed_items))
        else:
            simple_attrs.append((attr + ": " + str(value), {}))

    for attr, value in chain(simple_attrs, list_attrs, object_attrs):
        result[attr] = value

    return result


@click.command()
@click.argument("source", nargs=1, required=False)
@click.option("--no-pos/--pos", "show_pos", default=False)
def cli(source, show_pos):
    if source is None:
        print("Failed to read source from command line, trying to read it from STDIN:")
        print("=" * 72)

        source = sys.stdin.read()

        print("")
        print(source)
        print("=" * 72, "")
        print()

    module = ast.parse(source)

    source_tree = {class_name(module): traverse(module, show_pos=show_pos)}
    print(box_tr(source_tree))


if __name__ == "__main__":
    cli()
