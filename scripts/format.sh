#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place typer_cli tests --exclude=__init__.py
black typer_cli tests
isort typer_cli tests
