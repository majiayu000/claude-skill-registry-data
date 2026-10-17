---
name: python-engineering
description: Write production Python — typing, packaging, pytest discipline, stdlib-first, honest error handling.
version: 1
triggers: python, write python, pytest, typing, packaging, python code
category: Engineering & code
blurb: Write production Python — typing, packaging, pytest discipline, stdlib-first, honest error handling.
archetype: knowledge
example: Write this Python the production way, with tests.
---

# Python Engineering

Python is the team's rapid tool — keep it clean enough to trust in production: typed at the edges, tested at the core, packaged properly.

## When to use
- Services, scripts, automation, data tooling, APIs (FastAPI-class).
- Hardening notebook-grade code for production.

## Method
1. **Environment**: one virtualenv per project; dependencies pinned in `pyproject.toml` (+ lock); never install into system Python.
2. **Typing**: annotate public functions; run mypy/pyright in the loop; use `dataclasses`/Pydantic at boundaries for validation.
3. **Style**: ruff + black (or ruff format); no mutable default arguments; f-strings; pathlib over string paths.
4. **Errors**: catch specific exceptions; no bare `except:`; fail loudly with context; log with `logging`, never `print` in libraries.
5. **Resources**: context managers for files/sockets/locks; no orphaned handles.
6. **Async discipline**: no blocking calls in event loops; timeouts on every network call; structured concurrency where possible.
7. **Tests**: pytest + fixtures + parametrize; test error paths; freeze time/randomness; keep unit tests fast.
8. **Packaging**: `pyproject` metadata, console entry points, reproducible builds; pin for prod.

## Quality gates
- [ ] ruff + type-checker clean on the diff.
- [ ] pytest green including error-path tests.
- [ ] No bare excepts; no print-debugging left behind.
- [ ] Dependencies locked; virtualenv reproducible.

## Red lines
- No secrets in code or notebooks; use env/keystore.
- No unpinned `pip install` in production paths.

## Related
`backend-engineering` · `testing-strategy` · `dependency-governance`.
