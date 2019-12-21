import sys

import click
from asciitree import LeftAligned
from asciitree.drawing import BoxStyle, BOX_LIGHT

from astboom.visualizers.ast import VisualizeAST
from astboom.visualizers.cst import VisualizeCST
from astboom.visualizers.lib_cst import VisualizeLibCST
from astboom.visualizers.st import VisualizeST

SOURCE_READ_PROMPT = (
    "Failed to read source from command line, trying to read it from STDIN:"
)

box_tr = LeftAligned(draw=BoxStyle(gfx=BOX_LIGHT, horiz_len=1, indent=2))


@click.group()
def cli():
    pass


def show_tree(source, engine):
    if source is None:
        print(SOURCE_READ_PROMPT)
        print("=" * 72)

        source = sys.stdin.read()

        print("=" * 72, "")
        print()

    source_tree = engine.process(source)
    print(box_tr(source_tree))


@cli.command()
@click.argument("source", nargs=1, required=False)
@click.option(
    "--no-pos",
    "hide_pos",
    is_flag=True,
    help="Hide 'col_offset' and 'lineno' fields.",
    default=False,
)
@click.option(
    "--hide-empty", "hide_empty", is_flag=True, help="Hide empty fields.", default=False
)
def ast(source, hide_pos, hide_empty):
    """Display Abstract Syntax Tree for a given source."""
    ast_visualizer = VisualizeAST({"hide_pos": hide_pos, "hide_empty": hide_empty})
    show_tree(source, ast_visualizer)


@cli.command()
@click.argument("source", nargs=1, required=False)
@click.option(
    "--show-prefix",
    "show_prefix",
    is_flag=True,
    help="Display value stored in 'prefix' field of the node.",
    default=False,
)
def cst(source, show_prefix):
    """Display Concrete Source Tree for a given source."""
    show_tree(source, VisualizeCST({"show_prefix": show_prefix}))


@cli.command()
@click.argument("source", nargs=1, required=False)
def st(source):
    """Display parse tree for a given source."""
    show_tree(source, VisualizeST())


@cli.command()
@click.argument("source", nargs=1, required=False)
@click.option(
    "--hide-default",
    "hide_default",
    is_flag=True,
    help="Hide fields that contain default value (MaybeSentinel.DEFAULT).",
    default=False,
)
def libcst(source, hide_default):
    """Display parse tree for a given source."""
    show_tree(source, VisualizeLibCST({"hide_default": hide_default}))


if __name__ == "__main__":
    cli()
