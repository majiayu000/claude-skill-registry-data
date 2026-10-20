---
name: scaffold-python-library
description: >-
  Load this skill when starting or scaffolding a new distributable Python library: creating the src/
  layout, build metadata, type marker, tests, and .gitignore. Trigger when the user says
  "start/scaffold a Python library", "new Python package/SDK", or sets up a publishable package. For
  a web service use scaffold-python-service.
compatibility: >-
  Requires Python 3.12+ and the `uv` package manager on PATH, plus network access to PyPI for the
  first `uv sync`. `ruff`, `mypy`, and `pytest` are declared as dev dependencies and installed by
  `uv`; none is assumed to be present globally. `git` is needed only to initialise the repo.
---

# Scaffold a Python Library

Use a `src/` layout so tests run against the installed package, not the working tree.

```
your-library/
├── src/
│   └── your_library/
│       ├── __init__.py        # defines the public API (__all__)
│       └── py.typed           # ship type information (PEP 561)
├── tests/
│   ├── unit/
│   └── api/                   # exercise the public API as a consumer
├── pyproject.toml
├── README.md
└── .gitignore
```

## Initial Config

- `pyproject.toml` with an explicit build backend (hatchling), uv, ruff, mypy, pytest config —
  see `ceh-python-library:packaging` and `ceh-python-library:python-library-environment`.
- Keep `dependencies = []` minimal; no web-service deps. Define `__all__` in `__init__.py` from the start.

## Agent instruction file

Claude Code reads `CLAUDE.md`, **not** `AGENTS.md`. If the repo already has an `AGENTS.md` for
other coding agents, do not duplicate it — create a `CLAUDE.md` that imports it, so both tools
read one source:

```markdown
@AGENTS.md
```

Add any Claude-specific instructions below the import. A symlink also works, but on Windows it
needs Administrator or Developer Mode, so prefer the import. If there is no `AGENTS.md`, just
write `CLAUDE.md` directly.

## .gitignore

```
.venv/
.env
.env.*
!.env.example
__pycache__/
*.pyc
*.egg-info/
.coverage
.pytest_cache/
.mypy_cache/
.ruff_cache/
dist/
build/
.DS_Store
```
