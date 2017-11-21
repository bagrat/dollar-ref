# dollar-ref

[![PyPI version](https://badge.fury.io/py/dollar-ref.svg)](https://badge.fury.io/py/dollar-ref)
[![PyPI](https://img.shields.io/pypi/pyversions/dollar-ref.svg)](https://pypi.python.org/pypi/dollar-ref)
[![Build Status](https://travis-ci.org/bagrat/dollar-ref.svg?branch=master)](https://travis-ci.org/bagrat/dollar-ref)
[![Code Coverage](https://api.codacy.com/project/badge/Coverage/0bcd382ae5e944dfab79a0cfe42366cf)](https://www.codacy.com/app/bagrat/dollar-ref?utm_source=github.com&utm_medium=referral&utm_content=bagrat/dollar-ref&utm_campaign=Badge_Coverage)
[![Code Quality](https://api.codacy.com/project/badge/Grade/0bcd382ae5e944dfab79a0cfe42366cf)](https://www.codacy.com/app/bagrat/dollar-ref?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=bagrat/dollar-ref&amp;utm_campaign=Badge_Grade)
[![Join the chat at https://gitter.im/dollar-ref/Lobby](https://badges.gitter.im/dollar-ref/Lobby.svg)](https://gitter.im/dollar-ref/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/bagrat/dollar-ref/master/LICENSE)


# Introduction

If you have JSON/YAML configuration files that have grown huge and you would like to split them for better organization, then this package is definitely for you.

`dollar-ref` is both a command line tool and a Python library module that provides functionality to deal with JSON references.

For instance, if you are developing an API and maintain OpenAPI definition for it, the definition file may grow over time. At some point you might want to split different parts of the definition into separate files and reference them in the root document using JSON References. At that stage, you can use `dollar-ref` to merge them back into one single file for further usage, like feeding into API validators.

# Installation

`dollar-ref` is a Python package, so the installation process is as easy as a single `pip` call:

    $ pip install dollar-ref

# Usage

As already mentioned, `dollar-ref` comes both with a library module and a command line tool. In the following sections we will discuss both in detail.

## Command Line Tool

The command line tool is called `dref`. The name is both short for `dollar-ref` and `dereference`. To get started, just start but looking at the help message of the tool by running:

```bash
$ dref --help
```

As you may see from the help message, `dref` requires two positional arguments:

- `input_uri` - the root document URI containing JSON/YAML data. Any external references in this file will be recursively resolved and replaced with the contents of the referenced document. The URI may be an absolute or relative file path.
- `output_file` - the filename to write the resolved/merged output to. Depending on the provided filename extension, the output format will be different. When the extension is `yaml` or `yml`, the output format will be YAML, otherwise JSON:

```bash
$ dref input.json output.yaml
```

`dref` will print appropriate error messages if it detects any problems with provided information or data, otherwise a success message is shown. In case if you need to see more verbose information (e.g. for reporting a bug), you may append `-v` flag to the command invocation:

```bash
$ dref input.yaml output.json -v
```

## Library Module

The `dollar_ref` module comes with the `dollar-ref` package and can be imported and used by other Python programs to deal with JSON references.

The main product of the `dollar_ref` module is the `pluck` function. You provide is with a Python `dict` and a key path in form of a sequence of strings. The return value is the object at the specified path with all the references inside it resolved.

### Example Code

```python
from dollar_ref import pluck


root_doc = {
    'we-do-not': 'need-this',
    'sub-document': {
        'target': {
            'awesome': 'data',
            'we': {
                '$ref': '#/we-do-not'
            }
        }
    }
}


target = pluck(root_doc, 'sub-document', 'target')

assert target == {
    'awesome': 'data',
    'we': 'need-this'
}
```

# How to Contribute

If you would like to contribute to `dollar-ref`, then you are more than welcome!

You may start by looking at [open issues](https://github.com/bagrat/dollar-ref/issues), especially the ones labeled [`help wanted` and `good first issue`](https://github.com/bagrat/dollar-ref/issues?q=is%3Aopen+is%3Aissue+label%3A%22help+wanted%22+label%3A%22good+first+issue%22). Feel free to join discussions in the comments and share any related ideas.

If you have identified any problems in `dollar-ref` that does not have any open issue associated, you should definitely create one, providing any relevant information that would help to fix it.

Finally, whenever you have a fix (doc, code, whatever!) do not hesitate to create a Pull Request!

# License

See [LICENSE](https://github.com/bagrat/dollar-ref/blob/master/LICENSE).
