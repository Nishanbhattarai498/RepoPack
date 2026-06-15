# repopack

repopack is a small Python library that packs an entire project into a single markdown file. It walks the project tree, skips common build and virtualenv folders, and writes each included source file into a readable markdown bundle.

## Installation

```bash
pip install -e .
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
