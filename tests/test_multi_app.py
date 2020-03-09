import subprocess


def test_script_help():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "typer_cli",
            "tests/assets/multi_app.py",
            "run",
            "--help",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "sub" in result.stdout
    assert "top" in result.stdout


def test_script_app_non_existent():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "typer_cli",
            "--app",
            "non_existent",
            "tests/assets/multi_app.py",
            "run",
            "--help",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Not a Typer object:" in result.stderr


def test_script_sub():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "typer_cli",
            "tests/assets/multi_app.py",
            "run",
            "sub",
            "--help",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "bye" in result.stdout
    assert "hello" in result.stdout


def test_script_top():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "typer_cli",
            "tests/assets/multi_app.py",
            "run",
            "top",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "top" in result.stdout


def test_script_sub_hello():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "typer_cli",
            "tests/assets/multi_app.py",
            "run",
            "sub",
            "hello",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Hello World" in result.stdout


def test_script_sub_bye():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "typer_cli",
            "tests/assets/multi_app.py",
            "run",
            "sub",
            "bye",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "sub bye" in result.stdout
