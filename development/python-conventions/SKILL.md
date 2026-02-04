---
name: python-conventions
description: Work on Python experiments in packages/python_viterbo. Use for layout conventions, stage entrypoints, lint/test commands, and asset/plot handling.
---

# Python Conventions (python_viterbo)

## Purpose and layout

- Experiments live in `src/viterbo/experiments/<experiment>/`.
- Stage entrypoints: `stage_<stage>.py`.
- Shared helpers: `src/viterbo/common/` (avoid premature abstraction).
- Configs: `configs/experiments/<consumer>/<variant>.json`.
- Data artifacts: `data/experiments/<producer>/<variant>/` (Git LFS).

## Commands

- Lint: `scripts/lint.sh` (`ruff format`, `ruff check --fix`, `pyright`).
- Smoke tests: `scripts/smoke-test.sh` (`pytest tests/smoke`).
- Targeted tests: `uv run pytest <args>`.

## Stage invocation

- `uv run python -m viterbo.experiments.<experiment>.stage_<stage> --config configs/experiments/<experiment>/<variant>.json`

## Conventions

- Follow best practices for ML/data‑science code.
- Docstrings include inputs/outputs, side effects, shapes/dtypes, and contract.
- Prefer pure functions where practical.
- Comments explain the why behind non‑obvious decisions.

## Plots and assets

- LaTeX only includes assets; Python generates layout/style.
- Store outputs under `packages/latex_viterbo/assets/<experiment>/...`.
