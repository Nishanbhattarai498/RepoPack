"""Core logic for packaging a project into a single markdown bundle."""

from __future__ import annotations

import base64
import fnmatch
from pathlib import Path
from typing import Iterable

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


def _should_ignore(path: Path, root: Path, ignore_patterns: Iterable[str] | None = None) -> bool:
    relative_path = path.relative_to(root)
    parts = [part for part in relative_path.parts if part not in {".", ""}]

    if any(part in DEFAULT_IGNORED_NAMES for part in parts):
        return True

    if ignore_patterns is None:
        return False

    normalized_path = relative_path.as_posix()
    return any(fnmatch.fnmatch(normalized_path, pattern) or fnmatch.fnmatch(path.name, pattern) for pattern in ignore_patterns)


def pack_project_to_markdown(
    source: str | Path,
    output_file: str | Path,
    ignore_patterns: Iterable[str] | None = None,
    max_file_size_bytes: int | None = None,
    include_binary_as_data_uri: bool = True,
) -> Path:
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
        if not path.is_file() or _should_ignore(path, source_path, ignore_patterns):
            continue
        if resolved_path == output_path.resolve():
            continue

        if max_file_size_bytes is not None and path.stat().st_size > max_file_size_bytes:
            continue

        relative_path = path.relative_to(source_path).as_posix()
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            if include_binary_as_data_uri:
                suffix = path.suffix.lower()
                mime_type = {
                    ".png": "image/png",
                    ".jpg": "image/jpeg",
                    ".jpeg": "image/jpeg",
                    ".gif": "image/gif",
                    ".webp": "image/webp",
                    ".svg": "image/svg+xml",
                }.get(suffix, "application/octet-stream")
                encoded = base64.b64encode(path.read_bytes()).decode("ascii")
                sections.append(f"## {relative_path}")
                sections.append("")
                sections.append(f"![{relative_path}]({mime_type};base64,{encoded})")
                sections.append("")
                continue
            continue

        sections.append(f"## {relative_path}")
        sections.append("")
        sections.append("```")
        sections.append(content.rstrip())
        sections.append("```")
        sections.append("")

    output_path.write_text("\n".join(sections).rstrip() + "\n", encoding="utf-8")
    return output_path


pack_repository = pack_project_to_markdown
