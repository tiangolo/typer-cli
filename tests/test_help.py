import subprocess


def test_script_help():
    result = subprocess.run(
        ["coverage", "run", "-m", "typer_cli", "tests/assets/sample.py", "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "run" in result.stdout


def test_not_python():
    result = subprocess.run(
        ["coverage", "run", "-m", "typer_cli", "tests/assets/not_python.txt", "run"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Could not import as Python file" in result.stderr
