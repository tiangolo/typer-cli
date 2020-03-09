## Latest changes

## 0.0.5

* Add support for [generating Markdown docs](https://github.com/tiangolo/typer-cli#generate-docs) for **Typer** apps. PR [#3](https://github.com/tiangolo/typer-cli/pull/3).

## 0.0.4

* Handle default Typer to extract and run in this priority:
    * App object from `--app` *CLI Option*.
    * Function to convert to a **Typer** app from `--func` *CLI Option*.
    * **Typer** app in a variable with a name of `app`, `cli`, or `main`.
    * The first **Typer** app available in the file, with any name.
    * A function in a variable with a name of `main`, `cli`, or `app`.
    * The first function in the file, with any name.
    * PR [#2](https://github.com/tiangolo/typer-cli/pull/2).

## 0.0.3

* Add Travis CI. PR [#1](https://github.com/tiangolo/typer-cli/pull/1).
