# Typer CLI

<p align="center">
    <em>Run <strong>Typer</strong> scripts with completion, without having to create a package, using <strong>Typer CLI</strong>.</em>
</p>
<p align="center">
<a href="https://travis-ci.com/tiangolo/typer-cli" target="_blank">
    <img src="https://travis-ci.com/tiangolo/typer-cli.svg?branch=master" alt="Build Status">
</a>
<a href="https://codecov.io/gh/tiangolo/typer-cli" target="_blank">
    <img src="https://codecov.io/gh/tiangolo/typer-cli/branch/master/graph/badge.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/typer-cli" target="_blank">
    <img src="https://badge.fury.io/py/typer-cli.svg" alt="Package version">
</a>
</p>

---

⚠️ **WARNING** ⚠️ If you are building a CLI package you probably need [**Typer**](https://typer.tiangolo.com/), the library itself. This, **Typer CLI**, is a CLI application that simplifies running simple **Typer** scripts, it is not the library itself.

## Description

**Typer** is a library for building CLIs (Command Line Interface applications).

**Typer CLI** (this package) is a CLI application that simplifies running simple programs created with **Typer** with completion. 🚀

**Typer CLI**'s main feature is to provide ✨ completion ✨ in the Terminal for your own small programs built with **Typer**, without you having to create a complete installable Python package with them.

It's probably most useful if you have a small custom Python script using **Typer** (maybe as part of some project), for some small tasks, and it's not complex/important enough to create a whole installable Python package for it (something to be installed with `pip`).

In that case, you can install **Typer CLI**, and run your program with the `typer` command in your Terminal, and it will provide completion for your script.

## Usage

### Install

Install **Typer CLI**:

```console
$ python -m pip install typer-cli
```

That creates a `typer` command.

You can then install completion for it:

```console
$ typer --install-completion
```

### Sample script

Let's say you have a script that uses **Typer** in `my_custom_script.py`:

```Python
import typer

app = typer.Typer()


@app.command()
def hello(name: str = None):
    if name:
        typer.echo(f"Hello {name}")
    else:
        typer.echo("Hello World!")


@app.command()
def bye(name: str = None):
    if name:
        typer.echo(f"Bye {name}")
    else:
        typer.echo("Goodbye!")


if __name__ == "__main__":
    app()
```

### Run with Python

Then you could run your script with normal Python:

```console
$ python my_custom_script.py hello

Hello World!

$ python my_custom_script.py hello --name Camila

Hello Camila!

$ python my_custom_script.py bye --name Camila

Bye Camila
```

There's nothing wrong with running with Python directly. And, in fact, if some other code or program uses your script, that would be the best way to do it.

⛔️ But in your terminal, you won't get completion when hitting <kbd>TAB</kbd> for any of the subcommands or options, like `hello`, `bye`, and `--name`.

### Run with **Typer CLI**

Here's where **Typer CLI** is useful.

You can also run the same script with the `typer` command you get after installing `typer-cli`:

```console
$ typer my_custom_script.py run hello

Hello World!

$ typer my_custom_script.py run hello --name Camila

Hello Camila!

$ typer my_custom_script.py run bye --name Camila

Bye Camila
```

* Instead of using `python` directly you use the `typer` command.
* After the name of the file, add the subcommand `run`.

✔️ If you installed completion for **Typer CLI** (for the `typer` command) as described above, when you hit <kbd>TAB</kbd> you will have completion for everything, including all the subcommands and options of your script, like `hello`, `bye`, and `--name`. 🚀

## If main

Because **Typer CLI** won't use the block with:

```Python
if __name__ == "__main__":
    app()
```

You can also remove it if you are calling that script only with **Typer CLI** (using the `typer` command).

## Run other files

**Typer CLI** can run any script with **Typer**, but the script doesn't even have to use **Typer** at all.

**Typer CLI** could even run a file with a function that could be used with `typer.run()`, even if the script doesn't use `typer.run()` or anything else.

For example, a file `main.py` like this will still work:

```Python
def main(name: str = "World"):
    print(f"Hello {name}")
```

Then you can call it with:

```console
$ typer main.py run --help
Usage: typer run [OPTIONS]

Options:
  --name TEXT
  --help       Show this message and exit.

$ typer main.py run --name Camila

Hello Camila
```

And it will also have completion for things like the `--name` **CLI Option**.

## Run a package or module

Instead of a file path you can pass a module (possibly in a package) to import.

For example:

```console
$ typer my_package.main run --help
Usage: typer run [OPTIONS]

Options:
  --name TEXT
  --help       Show this message and exit.

$ typer my_package.main run --name Camila

Hello Camila
```

## Options

You can specify the following **CLI Options**:

* `--app`: the name of the variable with a `Typer()` object to run as the main app.
* `--func`: the name of the variable with a function that would be used with `typer.run()`.

### Defaults

When your run a script with the **Typer CLI** (the `typer` command) it will use the app from the following priority:

* An app object from the `--app` *CLI Option*.
* A function to convert to a **Typer** app from `--func` *CLI Option* (like when using `typer.run()`).
* A **Typer** app in a variable with a name of `app`, `cli`, or `main`.
* The first **Typer** app available in the file, with any name.
* A function in a variable with a name of `main`, `cli`, or `app`.
* The first function in the file, with any name.

## Generate docs

**Typer CLI** can also generate Markdown documentation for your **Typer** application.

You can use the subcommand `utils`.

And then the subcommand `docs`.

For example:

```console
$ typer some_script.py utils docs
```

**Options**:

* `--name TEXT`: The name of the CLI program to use in docs.
* `--output FILE`: An output file to write docs to, like README.md.

For example:

```console
$ typer my_package.main utils docs --name myapp --output README.md

Docs saved to: README.md
```

## License

This project is licensed under the terms of the MIT license.
