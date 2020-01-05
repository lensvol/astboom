# astboom
![PyPI](https://img.shields.io/pypi/v/astboom) 
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/astboom)
![GitHub](https://img.shields.io/github/license/lensvol/astboom)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Visualize Python AST/CST/ST in console using ASCII graphics using various engines.

Engines available:
* **[ast](https://docs.python.org/3/library/ast.html)** module
* **[parser](https://docs.python.org/3/library/parser.html)**  module
* **lib2to3**
* **[LibCST](https://github.com/Instagram/LibCST)**

## Example

![Example usage](https://raw.githubusercontent.com/lensvol/astboom/master/docs/example.png)

## Usage

Simply provide a valid Python source code string as an argument
and a corresponding AST/CST/ST will be displayed.

### AST

```
Usage: astboom ast [OPTIONS] [SOURCE]

  Display Abstract Syntax Tree for a given source.

Options:
  --no-pos      Hide 'col_offset' and 'lineno' fields.
  --hide-empty  Hide empty fields.
```

### lib2to3 CST

```
Usage: astboom cst [OPTIONS] [SOURCE]

  Display Concrete Source Tree for a given source.

Options:
  --show-prefix  Display value stored in 'prefix' field of the node.
```

### Python parse tree

```
Usage: astboom st [OPTIONS] [SOURCE]

  Display Python parse tree for a given source.

```

### LibCST tree

```
Usage: astboom libcst [OPTIONS] [SOURCE]

  Display LibCST tree for a given source.

Options:
  --hide-default   Hide fields that contain default value
                   (MaybeSentinel.DEFAULT).
  --hide-empty     Hide fields that contain empty values ([], (), '').
  --hide-fmt       Hide formatting-related fields and objects (whitespace,
                   newlines).
  --show-children  Show contents of the 'children' attribute.
```

If no source provided as an argument, then tool will attempt to read it
from *STDIN*.

## Installation

```shell script
# pip install astboom
```

## Getting started with development

```shell script
# git clone https://github.com/lensvol/astboom
# poetry install
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Authors

* **Kirill Borisov** ([lensvol@gmail.com](mailto:lensvol@gmail.com))
