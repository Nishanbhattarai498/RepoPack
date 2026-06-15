# repopack

[![PyPI version](https://img.shields.io/pypi/v/repopack-tool.svg)](https://pypi.org/project/repopack-tool/)

repopack is a small Python library that packs an entire project into a single markdown file. It walks the project tree, skips common build and virtualenv folders, and writes each included source file into a readable markdown bundle.

## Installation

### Install locally from this folder

```bash
pip install -e .
```

### Install from GitHub

```bash
git clone https://github.com/Nishanbhattarai498/RepoPack.git
cd RepoPack
pip install -e .
```

### Make it available to others

To make it available on PyPI so other people can install it with `pip install repopack-tool`, you need to:

1. Create an account on https://pypi.org/
2. Install build tools:
   ```bash
   python -m pip install --upgrade build twine
   ```
3. Build the package:
   ```bash
   python -m build
   ```
4. Upload it:
   ```bash
   python -m twine upload dist/*
   ```

After that, others can install it with:

```bash
pip install repopack-tool
```

## Usage

```python
from repopack import pack_project_to_markdown

pack_project_to_markdown("./my-project", "./bundle.md")
```

## What it produces

The generated markdown file contains:
- a title section
- one section per included file
- the file path as a heading
- the file contents inside fenced code blocks
