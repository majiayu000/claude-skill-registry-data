---
name: python
description: This skill should be used every time you work on Python projects or Python code changes in this repository.
compatibility: opencode
---

# Python Project Rules (uv + msgspec)

This file defines the preferred Python project organization for this repo.

## Core Principles

1. All Python projects must use `uv` for environment, dependency, and run management.
2. All runnable entrypoints must be defined in `pyproject.toml` under `[project.scripts]`.
3. Run entrypoints via `uv run <script>` (example: `uv run main`).
4. All data models must use `msgspec.Struct` (no dataclasses or pydantic).
5. Only create Python files under `src/` (no code outside `src/`).
6. Never use relative imports.

## Project Layout (Typical)

```
pyproject.toml
src/
└── <package_name>/
    ├── __init__.py
    ├── main.py
    ├── core/
    ├── services/
    ├── adapters/
    ├── config/
    └── utils/
```

## Entry Points

All runnable commands must be declared in `pyproject.toml`:

```toml
[project.scripts]
main = "<package_name>.main:main"
```

## Modeling Rules

Use `msgspec.Struct` for all models:

```python
import msgspec

class User(msgspec.Struct):
    id: str
    email: str
```
