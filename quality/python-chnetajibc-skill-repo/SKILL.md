---
name: python
description: "Python: typing everywhere, async vs sync, Pydantic v2, protocols/composition, packaging with pyproject/uv, pytest, lint/format. Prefer functions/modules over Java-style hierarchies."
---

# python

Typed, tested, packaged Python — modules and functions first, classes where state earns them.

## Activate when

- Writing, reviewing, or testing Python; packaging, typing, async, or tooling decisions.

## Do NOT activate for

- FastAPI specifics (see frameworks/fastapi); ML serving (see ml/model-serving).

## Procedure

1. Version: detect interpreter + dependency pins (pyproject/uv.lock/requirements); research behavior in https://docs.python.org/ for that version.
2. Types everywhere public; `mypy`/`pyright` clean; Pydantic v2 at boundaries (see frameworks/fastapi).
3. Async for I/O-bound with anyio/asyncio discipline; sync for CPU-bound; no blocking calls inside async paths.
4. Structure: `src/` layout, protocols/composition over deep hierarchies; module placement per architecture/language-modularity.
5. Quality: Ruff lint+format, pytest with fixtures/factories, coverage as signal not target.
6. Verify: typecheck + lint + tests green on the pinned interpreter; packaging installs clean (`pip install .` in fresh venv or `uv` equivalent).

## References
- Registry: `../../research/documentation-search/references/framework-registry.yaml` (python, uv, ruff, pytest, pydantic).
