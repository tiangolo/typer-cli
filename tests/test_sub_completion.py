import os
import subprocess


def test_script_completion_run():
    result = subprocess.run(
        ["coverage", "run", "-m", "typer_cli"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "___MAIN__.PY_COMPLETE": "complete_bash",
            "COMP_WORDS": "typer tests/assets/sample.py run hello --",
            "COMP_CWORD": "4",
        },
    )
    assert "--name" in result.stdout
