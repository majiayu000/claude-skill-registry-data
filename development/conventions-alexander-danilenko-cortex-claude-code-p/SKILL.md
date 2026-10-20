---
name: conventions
description: "Apply these opinionated Python 3.11+ conventions when writing Python in this codebase: type hints with mypy, async/await, pytest fixtures, dataclasses, Poetry packaging, production patterns."
---

# Python

House conventions for Python 3.11+. Apply them to code you are writing or changing — don't refactor untouched files to match unless asked.

## Conventions

- **Type every public signature** and keep `mypy --strict` green. Types on internals are optional; types at the boundary are what stop a caller passing the wrong thing.
- **Built-in generics and `X | None`** — `list[str]`, `dict[str, int]`, `str | None`. `typing.List` and `Optional[str]` are the pre-3.10 spelling and only cost an import.
- **`Protocol` over ABC inheritance.** Structural typing lets any correctly-shaped object satisfy the contract — including a test double — with no inheritance tree to maintain.
- **Dataclasses for data**, `slots=True` and `frozen=True` where they fit. They generate `__init__`, `__repr__`, and `__eq__` correctly; a hand-written `__init__` is where field drift starts. Pydantic is for validation and (de)serialisation at a boundary, not for plain records.
- **`pathlib`, not `os.path`.** Operator joins can't silently produce a wrong path from a stray separator.
- **Never a mutable default argument.** `def f(items=[])` shares one list across every call — a bug that only appears on the second call. Default to `None` and build inside.
- **`asyncio.TaskGroup` over bare `gather`** (3.11+): it cancels siblings on failure and reports via `ExceptionGroup`, so a crashed task can't leave the rest running detached. Use `async with asyncio.timeout(n)` for deadlines.
- **Hold a reference to every `create_task`.** The event loop only keeps a weak reference, so a fire-and-forget task can be garbage-collected mid-execution and simply vanish — no error, no result. Keep them in a `set` and discard on completion:

  ```python
  _tasks: set[asyncio.Task[None]] = set()

  def spawn(coro: Coroutine[None, None, None]) -> None:
      task = asyncio.create_task(coro)
      _tasks.add(task)
      task.add_done_callback(_tasks.discard)
  ```

- **Never a bare `except:`** — it swallows `KeyboardInterrupt` and `SystemExit`. Catch what you can actually handle.
- **Google-style docstrings** on public functions and classes, carrying intent rather than a restatement of the signature. The `documentation` skill has the full rule.
- **pytest: fixtures for setup, `parametrize` for cases.** A loop inside one test reports a single failure and hides which case broke; `parametrize` names each one.
- **Poetry and `pyproject.toml`** for packaging, ruff for lint and format, and a `py.typed` marker on any package whose types consumers should see. Use a `src/` layout — it stops tests from importing the working directory instead of the installed package, which is how a broken package still passes its own suite.

## Tooling baseline

`strict = true` covers most of it; these add the checks that catch real bugs rather than style. `--strict-markers` matters more than it looks: without it a typo'd `@pytest.mark.integraton` silently does nothing and the test runs where you thought it was excluded.

```toml
[tool.mypy]
strict = true
warn_unreachable = true
warn_redundant_casts = true
warn_unused_ignores = true

[[tool.mypy.overrides]]
module = "untyped_dep.*"
ignore_missing_imports = true

[tool.pytest.ini_options]
addopts = ["-ra", "--strict-markers", "--strict-config"]
```
