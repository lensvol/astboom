import parser
import symbol
import token

from astboom.visualizers.base import BaseVisualizer
from astboom.visualizers.utils import DictLikeList


def decode(code):
    if code < 256:
        return token.tok_name[code]
    else:
        return symbol.sym_name[code]


class VisualizeST(BaseVisualizer):
    def display(self, nodes):
        result = DictLikeList()

        for node in nodes:
            code, children = node[0], node[1:]
            if code < 256:
                result[f"{decode(code)}: {repr(children[0])}"] = {}
            else:
                result[decode(code)] = self.display(children)
        return result

    def process(self, source):
        st = parser.suite(source)
        source_tree = st.totuple()
        return {decode(source_tree[0]): self.display(source_tree[1:])}
