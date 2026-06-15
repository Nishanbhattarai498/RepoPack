# Demo Project

This bundle was generated automatically from the project tree.

## .gitignore

```
__pycache__/
*.py[cod]
*.egg-info/
.venv/
.pytest_cache/
```

## example_usage.py

```
from pathlib import Path

from src.repopack import pack_repository

if __name__ == "__main__":
    source = Path(__file__).resolve().parent
    destination = source / "project_bundle.md"
    pack_repository(source, destination)
    print(f"Packaged files to {destination}")
```

## pyproject.toml

```
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "repopack"
version = "0.1.0"
description = "Copy repository contents into a packaged folder"
readme = "README.md"
requires-python = ">=3.9"

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]
```

## QUICKSTART.md

```
# Quickstart

1. Install the package in editable mode:
   ```bash
   pip install -e .
   ```
2. Run the example:
   ```bash
   python example_usage.py
   ```
```

## README.md

```
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
```

## requirements.txt

```
pytest>=8.0.0
```

## src/repopack/__init__.py

```
"""Public package API for repopack."""

from .packer import pack_project_to_markdown, pack_repository

__all__ = ["pack_project_to_markdown", "pack_repository"]
```

## src/repopack/packer.py

```
"""Core logic for packaging a project into a single markdown bundle."""

from __future__ import annotations

from pathlib import Path

DEFAULT_IGNORED_NAMES = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".idea",
    ".vscode",
    "node_modules",
    "dist",
    "build",
    "site",
    ".next",
    ".coverage",
    "coverage",
    "htmlcov",
    ".DS_Store",
    "Thumbs.db",
}


def _should_ignore(path: Path, root: Path) -> bool:
    parts = {part for part in path.relative_to(root).parts if part not in {".", ""}}
    return any(part in DEFAULT_IGNORED_NAMES for part in parts)


def pack_project_to_markdown(source: str | Path, output_file: str | Path) -> Path:
    """Create a single markdown file that contains the contents of a project tree.

    Each included file is written as a section with its relative path and content.
    Binary or unsupported files are skipped.
    """

    source_path = Path(source).resolve()
    output_path = Path(output_file).resolve()

    if not source_path.exists():
        raise FileNotFoundError(f"Source directory does not exist: {source_path}")
    if not source_path.is_dir():
        raise NotADirectoryError(f"Source path is not a directory: {source_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    sections: list[str] = []
    sections.append("# Demo Project")
    sections.append("")
    sections.append("This bundle was generated automatically from the project tree.")
    sections.append("")

    for path in sorted(source_path.rglob("*")):
        resolved_path = path.resolve()
        if not path.is_file() or _should_ignore(path, source_path):
            continue
        if resolved_path == output_path.resolve():
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        relative_path = path.relative_to(source_path).as_posix()
        sections.append(f"## {relative_path}")
        sections.append("")
        sections.append("```")
        sections.append(content.rstrip())
        sections.append("```")
        sections.append("")

    output_path.write_text("\n".join(sections).rstrip() + "\n", encoding="utf-8")
    return output_path


pack_repository = pack_project_to_markdown
```

## src/repopack.egg-info/dependency_links.txt

```

```

## src/repopack.egg-info/PKG-INFO

```
Metadata-Version: 2.4
Name: repopack
Version: 0.1.0
Summary: Copy repository contents into a packaged folder
Requires-Python: >=3.9
Description-Content-Type: text/markdown

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
```

## src/repopack.egg-info/SOURCES.txt

```
README.md
pyproject.toml
src/repopack/__init__.py
src/repopack/packer.py
src/repopack.egg-info/PKG-INFO
src/repopack.egg-info/SOURCES.txt
src/repopack.egg-info/dependency_links.txt
src/repopack.egg-info/top_level.txt
tests/test_packer.py
```

## src/repopack.egg-info/top_level.txt

```
repopack
```

## tests/test_packer.py

```
from pathlib import Path

from src.repopack import pack_project_to_markdown


def test_pack_project_to_markdown_creates_single_bundle(tmp_path: Path) -> None:
    source = tmp_path / "project"
    source.mkdir()
    (source / "README.md").write_text("# Demo\n", encoding="utf-8")
    (source / "src").mkdir()
    (source / "src" / "main.py").write_text("print('hello')\n", encoding="utf-8")

    output_file = tmp_path / "bundle.md"
    result = pack_project_to_markdown(source, output_file)

    assert result == output_file
    assert output_file.exists()

    content = output_file.read_text(encoding="utf-8")
    assert "# Demo Project" in content
    assert "## README.md" in content
    assert "## src/main.py" in content
    assert "print('hello')" in content
```
