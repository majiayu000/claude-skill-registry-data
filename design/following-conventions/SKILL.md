---
name: following-conventions
description: Tenzir Python coding standards and tooling setup. Use when writing python code, running ruff/mypy/pytest, encountering pyproject.toml/uv.lock, or setting up a new Python project.
---

# Python Coding Conventions

Coding standards for Python projects at Tenzir.

## Required Tools

All projects use:

- **uv** — Dependency management and virtual environments
- **Ruff** — Linting and formatting
- **Mypy** — Static type checking
- **pytest** — Testing

## Default Libraries

Prefer to use these libraries to ensure uniform codebase across Tenzir
repositories:

- **pydantic** - Defining and validating models
- **FastAPI** - Declaring REST APIs
- **Click** - Providing a CLI interface

## Quality Gates

Run before committing or releasing:

```sh
uv run ruff check \
  && uv run ruff format --check \
  && uv run mypy \
  && uv run pytest \
  && uv build
```

The chain fails fast on the first error.

## Python Version

Target Python 3.12+. Use modern syntax and stdlib features freely—no
backwards-compatibility with older versions.

## Coding Style

### Formatting

- Ruff controls whitespace: 4-space indentation, double-quoted strings
- 88 character line limit (Ruff/Black default)
- Let Ruff order imports automatically

### Type Hints

- All public surfaces must be fully typed
- Strict Mypy settings reject untyped or partial definitions
- Avoid `Any`; fix warnings rather than ignoring them

### Package structure and imports

- Keep `__init__.py` files empty. They are only used to mark a directory as
  importable but do not contain any content, let alone non-trivial code.
- Always use absolute imports from the package top level:
  `from this_package.foo import bar` instead of `from .foo import bar`.
- Never use wildcard imports

### Naming Conventions

| Element   | Convention      | Example             |
| --------- | --------------- | ------------------- |
| Modules   | `snake_case`    | `my_module.py`      |
| Functions | `snake_case`    | `calculate_total()` |
| Variables | `snake_case`    | `user_count`        |
| Classes   | `PascalCase`    | `DataProcessor`     |
| Constants | `CONSTANT_CASE` | `MAX_RETRIES`       |

### CLI Conventions

- Use kebab-case for CLI flags: `--output-file`, not `--output_file`
- Keep user messages concise

## Documentation Style

- Write in active voice; rewrite passive sentences before committing
- Focus on user-facing impact, not implementation details
- Use explicit imports; isolate configuration helpers in `config.py`

### Unit Test Conventions

- Use `pytest` as testing framework
- Use `CliRunner` for end-to-end CLI testing
- Favor `tmp_path` for filesystem tests
- Use parametrization for scenario variation
- Maintain ≥80% coverage when coverage is configured

## Project Setup

Only read the specific file you need when setting up a new project or modifying
that tool's configuration:

- [project-structure.md](./project-structure.md) — Directory layout and testing conventions
- [pyproject.md](./pyproject.md) — Project metadata and build config
- [ruff.md](./ruff.md) — Ruff linting and formatting config
- [mypy.md](./mypy.md) — Mypy type checking config
- [pytest.md](./pytest.md) — Pytest runner config
- [coverage.md](./coverage.md) — Coverage reporting config
- [dev-dependencies.md](./dev-dependencies.md) — Dev dependency group
- [upgrading-dependencies.md](./upgrading-dependencies.md) — Upgrading and committing dependency changes
