---
name: python-tooling
description: "When running, packaging, linting, formatting, or type-checking Python — use uv, Ruff, and ty with changes scoped to touched code."
---

# Python Tooling

Use one boring toolchain:

- Run scripts and modules with `uv run`; use `uvx` for one-off tools.
- Add, remove, sync, lock, build, and publish dependencies through `uv`, never pip/venv/poetry by default.
- Lint with Ruff through uv. Fix touched files only; do not create repository-wide format churn.
- Type-check with ty through uv. Fix errors instead of adding blanket ignores; keep config changes narrow.

Read existing `pyproject.toml`, uv lock/config, Ruff config, and ty config before choosing commands. Reuse project commands when they exist.

For inline scripts and packaging details, load `scripts.md` or `build.md` only when needed.

A non-trivial change leaves one runnable check: the narrow Ruff/ty/test command that would fail if the change regressed. Report exact commands and results.
