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

app = typer.Typer()


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
    for local_name in dir(mod):
        if local_name.startswith("__"):
            continue
        obj: typer.Typer = getattr(mod, local_name)
        if isinstance(obj, typer.Typer):
            obj._add_completion = False
            click_obj = typer.main.get_command(obj)
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
