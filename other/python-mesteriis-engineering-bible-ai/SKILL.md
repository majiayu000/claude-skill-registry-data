---
name: python
description: "Applies senior Python rules for typing, async, APIs, persistence, tests, packaging, and architecture."
---

# Skill: python

## Purpose

Apply the shared engineering style to Python projects while respecting existing repository conventions.

## Inspect First

Before changing Python code, inspect relevant files when present:

- `pyproject.toml`
- `requirements.txt`
- `setup.py`
- `setup.cfg`
- `tox.ini`
- `pytest.ini`
- `mypy.ini`
- `.ruff.toml`
- `ruff.toml`
- `.pre-commit-config.yaml`
- Docker/CI files
- existing source and test files

Infer:

- Python version;
- dependency manager;
- formatter/linter;
- test runner;
- typing level;
- package structure;
- async/sync conventions.

Do not assume framework, ORM, validator, or test runner without evidence.

## Tooling Defaults

- Use `uv` for environment, dependency, lock, and command execution workflows
  when the project already uses `uv` or the user approves adopting it.
- Use `ruff` for linting and formatting when configured or available locally.
- Use `ty` for type checking when configured, requested, or clearly the
  strongest available local type checker.
- Do not introduce `uv`, `ruff`, or `ty` as project requirements solely because
  this skill prefers them.

## Style

- Follow existing project style first.
- Prefer explicit functions and small modules.
- Avoid dumping code into `utils.py`, `helpers.py`, or `common.py` unless the repository already uses that pattern and the addition is cohesive.
- Keep imports clean and localize optional/heavy imports only when justified.
- Avoid import-time side effects.
- Avoid mutable global state.

## Python Version

Use the configured Python version.

If the project version cannot be confirmed, avoid syntax and stdlib features newer than Python 3.10 unless the user approves.

Do not assume Python 3.12+ without confirmation.

## Typing

Use type hints for new or modified public functions and methods unless this conflicts with project style.

Prefer:

- concrete types where useful;
- `collections.abc` interfaces;
- `Protocol` for structural interfaces;
- `TypedDict` or existing models for structured dictionaries;
- `Literal` for constrained values;
- precise optionality.

Avoid `Any` unless:

- required by a third-party API;
- the value is genuinely dynamic;
- narrowing would add false precision.

If new `Any` is used, justify it briefly.

Do not mass-retrofit typing outside task scope.

## Functions and Classes

- Keep functions cohesive.
- Avoid boolean flags that radically change behavior.
- Prefer returning values over mutating shared state.
- Use classes when they represent state, lifecycle, interface implementation, dependency grouping, or polymorphic behavior.
- Do not create classes just to wrap one function.

## Data Models

Use the established project model approach:

- dataclasses;
- Pydantic;
- attrs;
- ORM models;
- plain typed objects;
- domain entities.

Do not introduce a modeling library unless already used or explicitly requested.

## Error Handling

Do not use bare `except`.

Avoid:

```python
try:
    ...
except Exception:
    pass
```

Use specific exceptions.

Preserve error context.

Do not log and re-raise unless there is a clear reason.

Domain errors should follow existing project patterns.

## Async

For async code:

- never block the event loop with sync I/O;
- use timeouts for external calls where appropriate;
- avoid orphan tasks;
- handle cancellation correctly;
- do not ignore `asyncio.CancelledError`;
- manage task lifecycle when using `asyncio.create_task`;
- protect shared mutable state.

## Database / ORM

Before changing persistence code, inspect:

- models;
- migrations;
- repositories;
- transaction boundaries;
- indexes;
- constraints;
- query style.

Rules:

- do not invent table or column names;
- avoid N+1 queries;
- preserve transactions for multi-step writes;
- do not bury business logic in persistence code unless the project intentionally does so;
- add migrations when schema changes require them.

## API Frameworks

Do not assume a framework.

If a framework is present:

- keep handlers/controllers thin;
- validate inputs;
- use existing dependency injection style;
- keep business logic out of transport layer;
- return consistent response models;
- avoid leaking internals in public errors.

## Tests and Validation

Use the existing test setup.

Common validation commands, only when configured or clearly available:

```bash
uv run pytest
pytest
python -m pytest
ruff check .
ruff format --check .
ty check
mypy .
pyright
```

Report exact commands and results.
## Shared Cross-Ecosystem Style


Apply the shared engineering style from:

- `../../engineering/05_design_principles.md`
- `../../engineering/06_responsibility_model.md`
- `../../engineering/07_complexity_budget.md`
- `../../engineering/12_naming_bible.md`

Language-specific idioms control syntax and ecosystem details, but they must not weaken the core rules: small cohesive units, explicit boundaries, honest validation, no dumping grounds, and no fake placeholders.
