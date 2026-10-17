---
name: aiwf-python310-coding
description: Use for Python 3.10 compatibility, packaging metadata, typing, async behavior, C-extension boundaries, and validation.
---

# AIWF Python 3.10 Coding

## Core Rule

Keep Python 3.10 compatibility real. Inspect packaging metadata and CI first, then avoid Python 3.11+ and 3.12-only syntax, modules, and typing features unless the project already gates them behind version checks or backports.

## Workflow

1. Inspect `pyproject.toml`, `setup.cfg`, `setup.py`, lock files, tox/nox/CI config, Docker files, and any `requires-python` declaration.
2. Confirm the actual interpreter used by the project. Prefer `py -3.10`, `.venv`, `uv`, `poetry`, or the repo-native runner over a global `python`.
3. Keep syntax and stdlib imports compatible with Python 3.10. Use `typing_extensions` or local compatibility helpers when the repo already depends on them.
4. Patch async code with attention to blocking I/O, cancellation, task lifetime, and event-loop ownership.
5. Validate using Python 3.10 when available. If it is not available, say so and run the closest repo-native check without presenting it as 3.10 proof.

## Compatibility Guardrails

- Python 3.10 supports structural pattern matching and `X | Y` type unions, but not Python 3.11/3.12-only features.
- Avoid unguarded use of `tomllib`, `typing.Self`, `ExceptionGroup`, `except*`, `asyncio.TaskGroup`, the Python 3.12 `type` statement, and Python 3.12 generic class/function syntax.
- Do not use PEP 701 f-string edge cases when 3.10 parsing must pass.
- Keep optional dependency imports lazy when they are only needed for optional features.
- For C extensions, verify CPython ABI, wheel tags, compiler settings, and Python include/lib paths before changing build config.

## Validation Defaults

Prefer existing commands. Useful fallbacks:

```powershell
py -3.10 -m compileall <package-or-file>
py -3.10 -m pytest
py -3.10 -m pip check
```

For type checks, use the repo's configured tool and version:

```powershell
py -3.10 -m mypy <package>
py -3.10 -m pyright
```

## Primary Source Anchors

- Python 3.10 documentation: https://docs.python.org/3.10/
- Python 3.10 "What's New": https://docs.python.org/3.10/whatsnew/3.10.html

When current maintenance status, packaging behavior, or stdlib details matter, verify the official Python docs before finalizing.
