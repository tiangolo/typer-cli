import subprocess


def test_script_help():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "typer_cli",
            "--app",
            "sub_app",
            "tests/assets/multi_app.py",
            "run",
            "--help",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "bye" in result.stdout
    assert "hello" in result.stdout
    assert "top" not in result.stdout


def test_script():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "typer_cli",
            "--app",
            "sub_app",
            "tests/assets/multi_app.py",
            "run",
            "hello",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Hello World" in result.stdout
