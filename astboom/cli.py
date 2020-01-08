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


class NaturalOrderGroup(click.Group):
    # Copied this from
    # https://github.com/pallets/click/issues/513#issuecomment-504158316

    def list_commands(self, ctx):
        return self.commands.keys()


@click.group(cls=NaturalOrderGroup)
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
    """Display Python parse tree for a given source."""
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
@click.option(
    "--hide-empty",
    "hide_empty",
    is_flag=True,
    help="Hide fields that contain empty values ([], (), '').",
    default=False,
)
@click.option(
    "--hide-fmt",
    "hide_fmt",
    is_flag=True,
    help="Hide formatting-related fields and objects (whitespace, newlines).",
    default=False,
)
@click.option(
    "--show-children",
    "show_children",
    is_flag=True,
    help="Show contents of the 'children' attribute.",
    default=False,
)
def libcst(source, hide_default, hide_empty, hide_fmt, show_children):
    """Display LibCST tree for a given source."""
    show_tree(
        source,
        VisualizeLibCST(
            {
                "hide_default": hide_default,
                "hide_empty": hide_empty,
                "hide_fmt": hide_fmt,
                "show_children": show_children,
            }
        ),
    )


if __name__ == "__main__":
    cli()
