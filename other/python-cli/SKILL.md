---
name: python-cli
description: Use when writing or changing a Python command-line interface — a CLI tool, or a command added to a service of either family — its commands and their arguments, the exit code each outcome leaves, and the test that invokes them. Owns the thin command that parses its arguments, calls one ordinary typed function and renders its result, the exit-code map written once at the boundary with success alone at zero, every catalogue failure on a non-zero code of its own and an unexpected exception keeping its traceback, commands that never import one another, the command line as the tool's published surface, and the in-process test through the library's runner asserting the exit code and the output as literals; bound to typer. Settings, the output and log streams, the console-script declaration and the error classes stay with `python-settings`, `python-logging`, `python-toolchain` and `exception-catalog`; whether a CLI tool takes an architecture family is `architecture-choice`.
---

# Python CLI — commands, exit codes and their test

A command-line interface is a boundary like any other: arguments come in as strings, a result and an
exit code go out, and everything between is ordinary typed code that knows nothing about the command
line. This skill owns that boundary — the command, the exit-code map and the test that drives it — for
a CLI tool and for a command added to a service. It gives no package layout for a large command tree.

## When to use vs. neighbours

- Whether a CLI tool takes the hex or the flat family → `architecture-choice`; it takes neither, and
  this skill is what binds its commands.
- The settings a command builds, a dotenv file, a tunable's default, an argument versus a setting →
  `python-settings` (rules 2, 5, 13 and 15).
- What goes to stdout and what to stderr, and where logging is configured → `python-logging`.
- Declaring the console script, the src layout, the lint and type-check configuration →
  `python-toolchain`.
- The error classes, their `code` and `context`, and rendering a caught error in one place →
  `exception-catalog`.
- What a test asserts, the substitution ladder, the entrypoint layer's budget → `test-principles`.
- A CLI tool shipped as an image rather than a package → `python-container-image`.
- The run a command triggers in a flat service, or the handler it calls in a hexagonal one → the
  family's own skill, e.g. `flat-entrypoint` (in the `pyhouse-flat` plugin) or `hex-application` (in
  `pyhouse-hex`); the command around it is this skill's.
- What a command, an option or the function behind it is called → `naming`.

## Template — typer

`src/myapp/cli.py`:

```python
from collections.abc import Callable
from functools import wraps
from pathlib import Path

import structlog
import typer

from myapp.exceptions import (
    MyappError,
    NotFoundError,  # only where a caller must tell it apart
)
from myapp.foo_export import export_foos
from myapp.logging import configure_logging

log = structlog.get_logger()

app = typer.Typer(pretty_exceptions_enable=False, add_completion=False)

EXIT_CODE_BY_ERROR: dict[type[MyappError], int] = {
    MyappError: 3,
    NotFoundError: 4,  # only where a caller must tell it apart
}


def exit_code_for(exc: MyappError) -> int:
    return next(
        EXIT_CODE_BY_ERROR[error_class] for error_class in type(exc).__mro__ if error_class in EXIT_CODE_BY_ERROR
    )


def _command_boundary[**P](command: Callable[P, None]) -> Callable[P, None]:
    @wraps(command)
    def run(*args: P.args, **kwargs: P.kwargs) -> None:
        configure_logging()
        try:
            command(*args, **kwargs)
        except MyappError as exc:
            log.error("command_failed", code=exc.code, context=exc.context)
            typer.echo(f"{exc.code}: {exc}", err=True)
            raise typer.Exit(exit_code_for(exc)) from exc

    return run


@app.callback()
def main() -> None:
    """Export foos."""


@app.command()
@_command_boundary
def export(destination: Path) -> None:
    result = export_foos(destination)
    typer.echo(f"{result.exported} foos exported")
```

`EXIT_CODE_BY_ERROR` is the one place a catalogue class meets an exit code, and `exit_code_for` is
`exception-catalog` rule 13's ancestry lookup: a refinement of `NotFoundError` exits `4` with no entry
of its own, and a class nothing else maps exits `3`, the root's own entry. `0`, `1` and `2` are not in
the map — success, the interpreter's exit for an uncaught exception, and the parser's usage error. The
classes mapped are the project's own; `NotFoundError` shows the pattern. A tool that raises no
catalogue error has no map; its boundary only sets up logging.

`_command_boundary` wraps every command. It runs `configure_logging` first — the project's one logging
setup, wherever it writes it (`python-logging` rule 3), routed to stderr (rule 1) — and it is the scope
that stops a catalogue failure: one log event, one message on stderr read off the exception, the mapped
code. Any other exception passes through it to the interpreter. `pretty_exceptions_enable=False` keeps
that traceback the interpreter's own: typer otherwise renders it, where rich is installed, as a boxed
panel quoting the source around each frame.

`@app.callback()` makes the app a group from the start, so `export` is a named subcommand
(`myapp export out/`) and adding a second command does not change how the first is invoked (rule 5);
its docstring is the tool's `--help` text. `add_completion=False` leaves out the
`--install-completion` and `--show-completion` options typer otherwise adds to every app, which would
become published surface the tool never chose; a tool that wants completion turns it on.

`export` is the shape of every command: parameters declared by annotation, so typer parses and rejects
them, and an option is a parameter with a default; one call; one line of output. Where the function
needs a client, the command builds it from its settings, opens it for the call, closes it when the call
returns, and hands it in (`python-settings` rule 13); on a family service, the family's composition
root builds it (rule 7). A coroutine is run with `asyncio.run` inside the command.

The tool runs through its console script, which names the app — `myapp = "myapp.cli:app"` under
`[project.scripts]` (`python-toolchain`). `python -m myapp.cli` runs nothing and exits `0`, since the
module only declares the app; a `__main__.py` calling `app()` exists only where the tool is run as
`python -m myapp`.

A tool whose commands outgrow one module keeps `app`, the map and the boundary here, and registers each
command module's function on it — `app.command()(_command_boundary(export))` — rather than having the
command modules import `app`.

The test drives the app through `typer.testing.CliRunner` in process —
`result = CliRunner().invoke(app, ["export", "out/"])`, then `assert result.exit_code == 0` and
`assert result.stdout == "3 foos exported\n"`; a failure asserts its mapped code and that
`result.stderr` ends with the rendered message, a literal — the log event comes before it (rule 6).
The logging setup writes to the stderr current when an event is emitted, not the one present when it
was configured: the runner replaces the streams on every invocation, and a setup kept from the first
one writes to a closed stream in every later test. The test is prose and not a template because
everything around those lines is whatever the function behind the command needs substituted, which
differs per tool.

## Other bindings

- **click** — `@click.command()` or `@click.group()` with `click.argument` and `click.option`
  declarations in place of annotations; the boundary is the same decorator raising
  `click.exceptions.Exit(code)`, and `click.testing.CliRunner` is the runner, with `result.stderr`
  separate from `result.stdout`. The map, the thin command and every rule are unchanged.
- **argparse** — stdlib, no runner: `main(argv: Sequence[str] | None = None) -> int` parses, dispatches
  through `add_subparsers` and `set_defaults`, and returns the exit code from the same map, called as
  `raise SystemExit(main())`; the test calls `main([...])` and reads the output with pytest's `capsys`,
  still in process. Its usage error exits `2` as click's does; the rules are unchanged.

## Rules

1. **A command is thin.** It parses its arguments, calls one ordinary typed function and renders what
   that function returns — no branching on the work, no store or network call, no logic of its own.
   Its parameters carry real types, so a malformed value is a usage error before anything runs and the
   function never re-parses a string. The function takes typed values, returns a declared type
   (`python-style`) and imports nothing from the CLI library, so a test, a second command or another
   entrypoint calls it unchanged. The command is the composition root for its invocation
   (`python-settings` rule 13): it builds the settings and the objects the function needs, and nothing
   else.
2. **The exit code is mapped at `exception-catalog` rule 13's one scope.** Zero means success and
   nothing else; each catalogue class a caller must tell apart gets its own non-zero code, and the
   root's code is neither the interpreter's `1` nor the parser's usage-error code — so a script tells a
   known failure from a bug and from a mistyped command.
3. **An unexpected exception is never hidden behind a bare `1`.** Only the catalogue is caught; anything
   else propagates with its traceback, because an `except Exception` that prints one line and exits
   non-zero turns a bug into something that reads as a known failure. Where the library replaces the
   interpreter's traceback with its own rendering, that rendering is turned off, so the traceback that
   reaches stderr does not depend on which optional packages are installed and does not quote source
   or local values.
4. **Commands never import one another.** What two commands share is a typed function both call. Where
   commands are split across modules, each is its own module and the one module holding the app, the
   map and the boundary registers them; no layout beyond that is given.
5. **The command line is a CLI tool's published surface** — its commands, their options and arguments,
   the output a caller parses and the exit codes. Removing or renaming any of them, or changing how an
   existing command is invoked, breaks the scripts built on it; a rename adds the new name alongside
   the old (`naming`, **Renaming**), and which segment that moves is `python-versioning`'s. An exit code, once shipped, keeps its meaning — scripts and schedulers branch
   on it as dashboards key on an error `code` (`exception-catalog` rule 3): a changed meaning takes a
   new code, and a retired code is not reused.
6. **A CLI is tested in process, through the library's runner** — the exit code and stdout asserted as
   literals for success, and each mapped failure's code and the message that ends its stderr, never
   through a subprocess.
   The function behind the command has its own tests; this one pins parsing, rendering and the map.
   It is `test-principles`' entrypoint layer, under that skill's substitution ladder.
7. **A command on a hex or flat service is one more entrypoint.** It calls the same handler or run
   function the service's other entrypoints call, built the way its composition root builds it, never a
   copy of that work, and every rule here holds, except that where the app, the map and the boundary
   sit, and what builds the objects a command needs, are the family's. A service whose run is started
   both by a command and by a scheduler gives the scheduler the command — the console script is what
   it runs — so one exit contract holds; a process definition's own exit is the family's.

## Inlined typing / import rules

- The result goes to stdout; every log event and the failure message go to stderr (`python-logging`
  rule 1), and logging is configured once before the first event (rule 3).
- A value the user picks per run is an argument, not a setting (`python-settings` rule 15); a CLI tool
  reads no dotenv file (rule 2), and its tunables may carry the documented default it ships with
  (rule 5).
- Nothing is built at import: `app` is a declaration, and settings, clients and connections are built
  inside the command (`python-packaging` rule 8).
- A CLI tool takes the house interpreter floor, not a library's (`python-style`).

## Hard stops

- A CLI tool is being given the hex or flat layout, or a layout for a large command tree, or it is
  unclear whether the program is a CLI tool or a service a command triggers → stop, use
  `architecture-choice`; a CLI tool takes neither family and the catalogue supplies no such layout.
- Asked to add an error class for a command to raise → stop, use `exception-catalog`; the class carries
  no exit code, and its code joins the map here.
- An option is given an environment-variable fallback, or a command reads the environment → stop, use
  `python-settings`; only a settings class reads the environment, and the command builds it
  (`python-settings` rules 3 and 13).
