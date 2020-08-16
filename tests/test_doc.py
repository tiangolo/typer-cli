import subprocess
from pathlib import Path


def test_doc():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "typer_cli",
            "tests.assets.multi_app",
            "utils",
            "docs",
            "--name",
            "multiapp",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    docs_path: Path = Path(__file__).parent / "assets/multiapp-docs.md"
    docs = docs_path.read_text()
    assert docs in result.stdout
    assert "**Arguments**" in result.stdout


def test_doc_output(tmp_path: Path):
    out_file: Path = tmp_path / "out.md"
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "typer_cli",
            "tests.assets.multi_app",
            "utils",
            "docs",
            "--name",
            "multiapp",
            "--output",
            str(out_file),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    docs_path: Path = Path(__file__).parent / "assets/multiapp-docs.md"
    docs = docs_path.read_text()
    written_docs = out_file.read_text()
    assert docs in written_docs
    assert "Docs saved to:" in result.stdout


def test_doc_not_existing():
    result = subprocess.run(
        ["coverage", "run", "-m", "typer_cli", "no_typer", "utils", "docs"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Could not import as Python module:" in result.stderr


def test_doc_no_typer():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "typer_cli",
            "tests/assets/empty_script.py",
            "utils",
            "docs",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "No Typer app found" in result.stderr


def test_doc_file_not_existing():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "typer_cli",
            "assets/not_existing.py",
            "utils",
            "docs",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Not a valid file or Python module:" in result.stderr
