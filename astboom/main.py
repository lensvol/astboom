import sys

import click
from asciitree import LeftAligned
from asciitree.drawing import BOX_HEAVY, BoxStyle

from astboom.visualizers.ast import VisualizeAST
from astboom.visualizers.cst import VisualizeCST

SOURCE_READ_PROMPT = (
    "Failed to read source from command line, trying to read it from STDIN:"
)

box_tr = LeftAligned(draw=BoxStyle(gfx=BOX_HEAVY, horiz_len=1, indent=2))


@click.command()
@click.argument("source", nargs=1, required=False)
@click.option(
    "--engine",
    type=click.Choice(["AST", "CST"], case_sensitive=False),
    default=None,
    help="Display source code using selected engine.",
)
@click.option(
    "--ast/--cst",
    "show_ast",
    default=True,
    help="Display source code as AST or CST (default: AST) [deprecated].",
)
@click.option(
    "--no-pos",
    "hide_pos",
    is_flag=True,
    help="Hide 'col_offset' and 'lineno' fields.",
    default=False,
)
def cli(source, show_ast, engine, hide_pos):
    if source is None:
        print(SOURCE_READ_PROMPT)
        print("=" * 72)

        source = sys.stdin.read()

        print("=" * 72, "")
        print()

    if (not engine and show_ast) or engine == "ast":
        engine = VisualizeAST({"hide_pos": hide_pos})
    else:
        engine = VisualizeCST()

    source_tree = engine.process(source)
    print(box_tr(source_tree))


if __name__ == "__main__":
    cli()
