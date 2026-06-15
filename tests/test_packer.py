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


def test_pack_project_to_markdown_supports_ignore_rules_size_limits_and_binary_files(tmp_path: Path) -> None:
    source = tmp_path / "project"
    source.mkdir()
    (source / "keep.py").write_text("print('keep me')\n", encoding="utf-8")
    (source / "ignored.log").write_text("debug log\n", encoding="utf-8")
    (source / "big.txt").write_text("x" * 80, encoding="utf-8")
    (source / "logo.png").write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 10)

    output_file = tmp_path / "bundle.md"
    pack_project_to_markdown(
        source,
        output_file,
        ignore_patterns=["*.log", "big.txt"],
        max_file_size_bytes=50,
    )

    content = output_file.read_text(encoding="utf-8")
    assert "## keep.py" in content
    assert "## ignored.log" not in content
    assert "## big.txt" not in content
    assert "## logo.png" in content
    assert "data:image/png;base64" in content
