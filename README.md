# astboom
![PyPI](https://img.shields.io/pypi/v/astboom) 
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/astboom)
![GitHub](https://img.shields.io/github/license/lensvol/astboom)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Visualize Python AST/CST/ST in console using ASCII graphics.

AST is displayed as provided by standard `ast` module, CST is displayed as provided by `lib2to3`.

## Example

![Example usage](https://raw.githubusercontent.com/lensvol/astboom/master/docs/example.png)

## Usage

Simply provide a valid Python source code string as an argument
and a corresponding AST/CST/ST will be displayed.

```
Usage: astboom ast [OPTIONS] [SOURCE]

  Display Abstract Syntax Tree for a given source.

Options:
  --no-pos      Hide 'col_offset' and 'lineno' fields.
  --hide-empty  Hide empty fields.
  --help        Show this message and exit.
```

```
Usage: astboom cst [OPTIONS] [SOURCE]

  Display Concrete Source Tree for a given source.

Options:
  --show-prefix  Display value stored in 'prefix' field of the node.
  --help         Show this message and exit.
```

```
Usage: astboom st [OPTIONS] [SOURCE]

  Display parse tree for a given source.

Options:
  --help  Show this message and exit.
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
# poetry install --develop
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Authors

* **Kirill Borisov** ([lensvol@gmail.com](mailto:lensvol@gmail.com))
