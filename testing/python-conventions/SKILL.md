---
name: python-conventions
description: "Python rules for tooling, glue and hook scripts: when Python at all, standard library only for hooks, uv with pyproject for projects, src layout, ruff, typed signatures, specific exceptions and unittest or pytest. Use when writing or reviewing Python, or setting up a Python project or a hook script."
---

# Python conventions

Python is for tooling, glue and hook scripts, not the default application language.

## When to use

- Writing or changing a Python script or package.
- Setting up a Python project.
- Writing a hook that runs inside an agent harness.

## Rules

### When Python at all

- Reach for Python for tooling, glue and anything a library makes clearly shorter.
  Prefer the repository's primary language otherwise.
- A hook script is standard library only. A hook needing a dependency is the wrong
  shape, because it must run on every machine with no setup step.

### Project layout and tooling

- `uv` manages the environment and the lock file. Commit both `pyproject.toml` and
  `uv.lock`.
- `src/<package>/` layout, so tests import the installed package, not the working
  directory.
- `requires-python` is set and matches what CI runs.
- `ruff` for linting and formatting. No black, isort or flake8 on top.
- Dependencies get a lower bound and no upper bound unless one is known to break.

### Style

- Type hints on every function signature, including `-> None`.
- `pathlib.Path` over `os.path`. A dataclass over a dictionary passed around.
- f-strings for formatting. No `%` and no `.format`.
- No mutable default arguments, no wildcard imports, no module level side effects on
  import.
- A comprehension where it stays readable, a loop where it does not.

### Errors

- Raise a specific exception, never a bare `Exception`. One base exception per
  package when callers need to catch it.
- A bare `except:` or `except Exception:` carries a comment naming why, and either
  re-raises or logs.
- Never swallow an exception silently. The one documented exception is a hook script
  that catches everything, prints one line and exits zero on purpose.

### Logging

- `logging` configured once in the entry point, never at import time in a library
  module.
- No `print` in library code. A CLI prints to stdout deliberately, diagnostics go to
  stderr.
- Never log a secret, a token or a request body.

### Tests

- `unittest` for a standalone script with no dependencies, `pytest` for a project
  with `uv`, tests next to the package under `tests/`.
- Parametrise instead of copying a test. Fixtures for setup, not module level state.
- A hook script gets tests that feed it a payload on stdin and assert the decision,
  with no network and no git repository required unless the hook needs one.

### License header

- Every source file carries the license header after the shebang, matching the
  repository's license.

## Guardrails

- Python justified over the repository's primary language.
- Hook scripts standard library only, project scripts managed by `uv`.
- `ruff check` and `ruff format` clean, type hints complete.
- Specific exceptions used, nothing swallowed silently outside the hook pattern.
- Logging configured in the entry point, no secret ever logged.
- Tests cover behaviour, named for the behaviour, deterministic.

## References

- `lint` for running `ruff` as part of the repository's checks.
- `testing-conventions` for when a test is written, what earns one and test form.
