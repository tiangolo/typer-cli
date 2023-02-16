#!/usr/bin/env bash

set -e
set -x

# Use xdist-pytest --forked to ensure modified sys.path to import relative modules in examples keeps working
pytest --cov=typer_cli --cov=tests --cov-report=term-missing -o console_output_style=progress --forked --numprocesses=auto ${@}
