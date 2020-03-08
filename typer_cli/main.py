import importlib.util
import sys
from pathlib import Path
from typing import Any, Iterable, List, Optional, Tuple, cast

import click
import click.core
import click_completion  # type: ignore
import typer
from click import Command, Group, Option
from click._bashcomplete import resolve_ctx  # type: ignore
from click_completion.core import get_choices as original_get_choices  # type: ignore

from . import __version__

default_app_names = ("app", "cli", "main")
default_func_names = ("main", "cli", "app")

app = typer.Typer()


class State:
    def __init__(self) -> None:
        self.app = None
        self.func = None


state = State()


def maybe_update_state(ctx: click.Context) -> None:
    app_name = ctx.params.get("app")
    if app_name:
        state.app = app_name
    func_name = ctx.params.get("func")
    if func_name:
        state.func = func_name


class TyperCLIGroup(click.Group):
    def list_commands(self, ctx: click.Context) -> Iterable[str]:
        self.maybe_add_run(ctx)
        return super().list_commands(ctx)

    def get_command(self, ctx: click.Context, name: str) -> Optional[Command]:
        self.maybe_add_run(ctx)
        return super().get_command(ctx, name)

    def invoke(self, ctx: click.Context) -> Any:
        self.maybe_add_run(ctx)
        return super().invoke(ctx)

    def maybe_add_run(self, ctx: click.Context) -> None:
        file = ctx.params.get("file")
        if file:
            maybe_update_state(ctx)
            sub_cli = generate_cli_from_path(ctx=ctx, file=file)
            if sub_cli:
                self.add_command(sub_cli, "run")


def generate_cli_from_path(*, ctx: click.Context, file: str) -> Optional[Command]:
    file_path = Path(file)
    module_name = file_path.name
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    if spec is None:
        typer.echo(f"Could not import as Python the file: {file}", err=True)
        sys.exit(1)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    # Try to get defined app
    if state.app:
        obj: typer.Typer = getattr(mod, state.app, None)
        if not isinstance(obj, typer.Typer):
            typer.echo(f"Not a Typer object: --app {state.app}", err=True)
            sys.exit(1)
        obj._add_completion = False
        click_obj = typer.main.get_command(obj)
        return click_obj
    # Try to get defined function
    if state.func:
        func_obj = getattr(mod, state.func, None)
        if not callable(func_obj):
            typer.echo(f"Not a function: --func {state.func}", err=True)
            sys.exit(1)
        sub_app = typer.Typer()
        sub_app.command()(func_obj)
        sub_app._add_completion = False
        click_obj = typer.main.get_command(sub_app)
        return click_obj
    # Iterate and get a default object to use as CLI
    local_names = dir(mod)
    local_names_set = set(local_names)
    # Try to get a default Typer app
    for name in default_app_names:
        if name in local_names_set:
            obj = getattr(mod, name, None)
            if isinstance(obj, typer.Typer):
                obj._add_completion = False
                click_obj = typer.main.get_command(obj)
                return click_obj
    # Try to get any Typer app
    for name in local_names_set - set(default_app_names):
        obj = getattr(mod, name)
        if isinstance(obj, typer.Typer):
            obj._add_completion = False
            click_obj = typer.main.get_command(obj)
            return click_obj
    # Try to get a default function
    for func_name in default_func_names:
        func_obj = getattr(mod, func_name, None)
        if callable(func_obj):
            sub_app = typer.Typer()
            sub_app.command()(func_obj)
            sub_app._add_completion = False
            click_obj = typer.main.get_command(sub_app)
            return click_obj
    # Try to get any func app
    for func_name in local_names_set - set(default_func_names):
        func_obj = getattr(mod, func_name)
        if callable(func_obj):
            sub_app = typer.Typer()
            sub_app.command()(func_obj)
            sub_app._add_completion = False
            click_obj = typer.main.get_command(sub_app)
            return click_obj
    return None


def get_choices(
    cli: Command, prog_name: str, args: List[str], incomplete: str
) -> List[Tuple[str, str]]:
    ctx: typer.Context = resolve_ctx(cli, prog_name, args)
    if ctx.parent is None:
        assert isinstance(cli, Group)
        cli = cast(Group, cli)
        file = ctx.params.get("file")
        if file:
            maybe_update_state(ctx)
            sub_cli = generate_cli_from_path(ctx=ctx, file=file)
            if sub_cli:
                cli.add_command(sub_cli, "run")
    return original_get_choices(cli, prog_name, args, incomplete)


def print_version(ctx: click.Context, param: Option, value: bool) -> None:
    if not value or ctx.resilient_parsing:
        return
    typer.echo(f"Typer CLI version: {__version__}")
    raise typer.Exit()


@app.callback(cls=TyperCLIGroup)
def callback(
    ctx: typer.Context,
    *,
    file: Path = typer.Argument(..., exists=True, file_okay=True, dir_okay=True),
    app: str = typer.Option(None, help="The typer app object/variable to use"),
    func: str = typer.Option(None, help="The function to convert to Typer"),
    version: bool = typer.Option(False, "--version", callback=print_version),  # type: ignore
) -> None:
    pass


def main() -> Any:
    click_completion.core.get_choices = get_choices
    click_completion.init()
    return app()
