import typer

sub_app = typer.Typer()

variable = "Some text"


@sub_app.command()
def hello(name: str = "World"):
    """
    Say Hello
    """
    typer.echo(f"Hello {name}")


@sub_app.command()
def hi(user: str = typer.Argument("User", help="The name of the user to greet")):
    """
    Say Hi
    """
    typer.echo(f"Hello {user}")


@sub_app.command()
def bye():
    """
    Say bye
    """
    typer.echo("sub bye")


app = typer.Typer(help="Demo App", epilog="The end")
app.add_typer(sub_app, name="sub")


@app.command()
def top():
    """
    Top command
    """
    typer.echo("top")
