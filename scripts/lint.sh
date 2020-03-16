#!/usr/bin/env bash

set -e
set -x

mypy typer_cli
black typer_cli tests --check
isort --multi-line=3 --trailing-comma --force-grid-wrap=0 --combine-as --line-width 88 --recursive --check-only --thirdparty typer_cli typer_cli tests
