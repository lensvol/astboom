# tokelor

Visualize Python AST in console using ASCII graphics.

## Example

![Example usage](https://raw.githubusercontent.com/lensvol/astboom/master/docs/example.png)

## Usage

Simply provide a valid Python source code string as an argument
and a corresponding AST will be displayed.

```
# astboom --help
Usage: astboom [OPTIONS] [SOURCE]

Options:
  --no-pos  Hide 'col_offset' and 'lineno' fields.
  --help    Show this message and exit.
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
