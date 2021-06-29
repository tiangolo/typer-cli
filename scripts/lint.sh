#!/usr/bin/env bash

set -e
set -x

mypy typer_cli
black typer_cli tests --check
isort typer_cli tests --check-only
