import subprocess


def test_script_hello():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "typer_cli",
            "tests/assets/sample.py",
            "run",
            "hello",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Hello World!" in result.stdout


def test_script_hello_name():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "typer_cli",
            "tests/assets/sample.py",
            "run",
            "hello",
            "--name",
            "Camila",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Hello Camila!" in result.stdout


def test_script_hello_name_formal():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "typer_cli",
            "tests/assets/sample.py",
            "run",
            "hello",
            "--name",
            "Camila",
            "--formal",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Good morning Ms. Camila" in result.stdout


def test_script_bye():
    result = subprocess.run(
        ["coverage", "run", "-m", "typer_cli", "tests/assets/sample.py", "run", "bye"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Goodbye" in result.stdout


def test_script_bye_friend():
    result = subprocess.run(
        [
            "coverage",
            "run",
            "-m",
            "typer_cli",
            "tests/assets/sample.py",
            "run",
            "bye",
            "--friend",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    assert "Goodbye my friend" in result.stdout


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
