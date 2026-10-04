---
name: python-best-practices
description: >-
  Modern Python standards (uv, Ruff, strict typing, Pydantic v2, Polars, async I/O).
  Use when writing or reviewing Python, pyproject.toml, FastAPI, scripts, data pipelines,
  or when the user mentions uv, ruff, pydantic, type hints, or Python refactoring.
---

# Python best practices

Project-specific rules: [reference.md](reference.md) (full guide, French).

## Quick rules

1. **Tooling:** `uv` for deps; `ruff check --fix` + `ruff format` after edits. Layout: `src/` package.
2. **Types:** Annotate all parameters and returns; Pydantic v2 for external/config data.
3. **Logic:** Prefer `match` / dict dispatch over deep `if/elif`; generators for large streams.
4. **I/O:** `async`/`await` (AnyIO) for network/DB/files; Polars lazy API for new data work.
5. **Agent-facing:** Google-style docstrings; never `except Exception: pass` — explicit errors.

## Verify before done

From repo root, run what exists in `pyproject.toml` / `Makefile`:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

If commands differ, read project config first — do not invent tooling.
