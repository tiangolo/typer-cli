import subprocess


def test_script_help():
    result = subprocess.run(
        ["coverage", "run", "-m", "typer_cli", "tests/sample.py", "run", "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "bye" in result.stdout
    assert "Say bye" in result.stdout
    assert "hello" in result.stdout
    assert "Say hi" in result.stdout
