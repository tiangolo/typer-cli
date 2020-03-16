import subprocess


def test_help():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "typer_cli",
            "tests/assets/multi_func.py",
            "run",
            "--help",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Say hi to someone, by default to the World." in result.stdout


def test_script():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "typer_cli",
            "tests/assets/multi_func.py",
            "run",
            "--name",
            "Camila",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Hello Camila" in result.stdout


def test_script_func_non_existent():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "typer_cli",
            "--func",
            "non_existent",
            "tests/assets/multi_func.py",
            "run",
            "--name",
            "Camila",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Not a function:" in result.stderr


def test_script_func_not_function():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "typer_cli",
            "--func",
            "message",
            "tests/assets/multi_func.py",
            "run",
            "--name",
            "Camila",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Not a function:" in result.stderr


def test_script_func():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "typer_cli",
            "--func",
            "say_stuff",
            "tests/assets/multi_func.py",
            "run",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Hello" not in result.stdout
    assert "Stuff" in result.stdout
