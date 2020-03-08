import typer

sub_app = typer.Typer()

variable = "Some text"


@sub_app.command()
def hello():
    typer.echo("sub hello")


@sub_app.command()
def bye():
    typer.echo("sub bye")


app = typer.Typer()
app.add_typer(sub_app, name="sub")


@app.command()
def top():
    typer.echo("top")
