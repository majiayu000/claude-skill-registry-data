---
name: python-stack
description: Python implementation guidance for project structure, type safety, dependency management, testing, and operational correctness.
compatibility: opencode
metadata:
  audience: engineer
  purpose: stack-guidance
---
## Focus areas

- Use type hints consistently (PEP 484/526/604). Prefer `str | None` over `Optional[str]` in Python 3.10+.
- Structure projects with clear package boundaries: `src/` layout or flat layout, consistent `__init__.py` usage.
- Prefer `pyproject.toml` over `setup.py` / `setup.cfg` for project metadata and build configuration.
- Use virtual environments (`venv`, `uv`, or `poetry`) — never install into the system Python.
- Handle errors explicitly: catch specific exceptions, avoid bare `except:`, use custom exception hierarchies when the domain warrants it.

## Dependency management

- Pin dependencies for applications (lock files via `pip-compile`, `poetry.lock`, or `uv.lock`).
- Use version ranges for libraries.
- Prefer standard library when it covers the need adequately.
- Audit transitive dependencies when adding new packages.

## Testing

- Use `pytest` as the default test runner.
- Prefer fixtures over setup/teardown methods.
- Use `unittest.mock` or `pytest-mock` for mocking — mock at boundaries, not internals.
- Structure tests to mirror source layout: `tests/` parallel to `src/`.
- Use `parametrize` for data-driven tests rather than duplicating test functions.

## Async

- Use `asyncio` for I/O-bound concurrency. Do not use threads for I/O unless interacting with blocking libraries.
- Prefer `async`/`await` over callback patterns.
- Use `asyncio.TaskGroup` (3.11+) or `asyncio.gather` for concurrent tasks.
- Avoid mixing sync and async code — use `asyncio.to_thread` when calling blocking functions from async context.

## Guardrails

- Avoid mutable default arguments (`def f(x=[])` is a classic bug).
- Avoid global mutable state.
- Prefer `dataclasses` or `pydantic` models over raw dicts for structured data.
- Use `pathlib.Path` over `os.path` for file system operations.
- Prefer f-strings over `%` formatting or `.format()`.
- Watch for import cycles — restructure packages rather than using lazy imports as a workaround.
- Use `logging` module, not `print()`, for operational output.
- Be explicit about encoding when reading/writing files (`open(..., encoding="utf-8")`).
