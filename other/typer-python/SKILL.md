---
name: typer-python
description: Use for writing, reviewing, debugging, or testing Python command-line interfaces built with Typer, including typed arguments and options, command groups, callbacks, contexts, exit behavior, help, and CliRunner tests. Do not use merely for terminal styling, arbitrary business logic, a Click-only CLI, shell scripts, or invoking an existing command.
argument-hint: "[Typer CLI task, code, error, or command contract]"
---

# Typer Python

Build a CLI as a stable user-facing protocol: command path, parameter spelling,
types, defaults, streams, exit codes, help, side effects, and tests are its
contract.

## Boundary

Use this skill when the project imports Typer or the user explicitly requests a
Typer CLI. Keep domain operations in ordinary Python functions and let command
functions adapt terminal input/output to them. Do not introduce Typer for a
library API, a Click-only project, a one-off shell invocation, or Rich-only
rendering. Use Rich guidance separately when terminal presentation itself is
the job.

## Know the runtime objects

| Object | Meaning | Responsibility |
|---|---|---|
| `typer.Typer` | Command registry and root/group configuration | Own commands, callbacks, sub-apps, and help behavior. |
| Command function | Type-annotated adapter called after parsing | Validate command-level invariants, call domain code, emit output, map failures. |
| `Annotated[T, typer.Argument(...)]` | Positional CLI field | Required ordered input whose position is natural and stable. |
| `Annotated[T, typer.Option(...)]` | Named CLI field | Optional/configuration input, flags, secrets, repeatable values, or a required named field. |
| `typer.Context` | One invocation's Click/Typer state | Shared object state, invoked subcommand, raw extra arguments only when explicitly allowed. |
| `CliRunner` result | Captured invocation outcome | Assert exit code, stdout/stderr-visible output, exception, and side effects. |

Read [the command object model](references/object-model.md) before changing a
single-command app into groups, adding callbacks, or passing shared state.

## Ordered workflow

1. Recover the public command contract from documentation, entry points,
   existing invocations, completion, and tests. Preserve names and exit behavior
   unless the task explicitly changes them.
2. Separate pure domain work from the command adapter. Do not unit-test domain
   behavior only through terminal text.
3. Choose command topology first: one command, several peer commands, or nested
   sub-apps. Do not add a callback merely to make help look different.
4. Classify every field as argument or option, then specify its Python type,
   required/default state, aliases, validation, environment source, and
   sensitivity.
5. Map expected user errors to concise CLI errors and nonzero exits. Let
   unexpected defects retain useful diagnostics; never print secrets or local
   values in production tracebacks.
6. Test help, success, invalid input, and one side-effect boundary with
   `CliRunner`. Test the domain function directly as well.
7. Run the real installed entry point, not only `python module.py`, before
   declaring completion.

## Parameter decisions

| Condition | Use |
|---|---|
| A value is the primary ordered subject (`FILE`, `NAME`) | `Argument` |
| A value configures behavior or should be self-describing | `Option` |
| Omission means a meaningful default | Option with an explicit default |
| The user must supply a named value | Required option; do not encode a fake sentinel default |
| Exactly two states exist | Boolean flag, with positive/negative spelling when both matter |
| Values come from a closed set | `Enum`/`Literal` supported by the installed Typer version |
| A filesystem precondition is structural | `Path` plus `exists`, file/dir, readable/writable constraints |
| Validation depends on another field or external state | Validate in the command adapter/domain boundary, not an isolated parameter callback |
| Input is secret | Hidden prompt or environment/config source; never echo it |

Prefer `typing.Annotated` metadata on Python 3.11+. Keep Python defaults as the
source of default/required semantics. Do not blindly copy legacy
`name: str = typer.Option(...)` syntax from a prompt; inspect the installed
version when editing older code.

## Canonical anchor

```python
from pathlib import Path
from typing import Annotated

import typer

app = typer.Typer(no_args_is_help=True)


@app.callback()
def main() -> None:
    """File export commands."""


@app.command()
def export(
    source: Annotated[Path, typer.Argument(exists=True, dir_okay=False)],
    output: Annotated[Path, typer.Option("--output", "-o")],
    force: Annotated[bool, typer.Option("--force/--no-force")] = False,
) -> None:
    if output.exists() and not force:
        raise typer.BadParameter("output exists; pass --force", param_hint="--output")
    export_file(source, output)
    typer.echo(str(output))


if __name__ == "__main__":
    app()
```

The callback keeps `export` as a named subcommand; without it, Typer can promote
a sole command function to the root invocation. `typer.Exit(code=...)`
represents an intentional termination, not a returned
process code. `BadParameter` is for actionable user input errors. Do not catch
`Exception` and convert programmer defects into a friendly success-looking
message.

## Groups, callbacks, and state

- Use one root `Typer` and `add_typer` for a coherent noun namespace such as
  `users create`; do not nest a single command without a stable grouping need.
- A group callback runs before its subcommand. Keep it cheap and free of
  irreversible side effects. If `invoke_without_command=True`, branch on
  `ctx.invoked_subcommand is None` when root-only behavior must not also run for
  subcommands.
- Put shared invocation state in a typed object assigned to `ctx.obj`; do not
  use module globals for per-invocation configuration.
- Parameter callbacks also run during completion. They must not print, mutate
  durable state, or perform expensive network work.
- Enable unknown/extra arguments only for an intentional pass-through command;
  otherwise preserve parser rejection.

Read [design and testing rules](references/design-testing.md) for composition,
error handling, entry points, and `CliRunner` assertions.

## Verification

Inspect the installed version with `importlib.metadata.version("typer")` and
the installed signatures when
a parameter or help behavior may drift; read [version grounding](references/version-grounding.md).
Completion requires: the packaged entry point resolves; `--help` and no-args
behavior are intentional; aliases, defaults, env sources, and secret handling
match the contract; invalid input exits nonzero without a traceback; success
uses the correct output stream and exit code; side effects happen exactly once;
and tests invoke the `Typer` app with representative arguments rather than
calling only command functions directly.

## References

- [Command object model](references/object-model.md)
- [CLI design and testing](references/design-testing.md)
- [Version grounding](references/version-grounding.md)
