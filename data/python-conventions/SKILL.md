---
name: python-conventions
description: Creating or modifying Python code in packages/python_viterbo. Covers directory layout, stage entrypoints, config files, data outputs, tests, lint commands.
---

# Python Conventions

## Example: example-pipeline

Study `src/viterbo/experiments/example_pipeline/` before creating experiments:

```
src/viterbo/experiments/example_pipeline/
├── SPEC.md           # Research question, method, success criteria
├── stage_build.py    # Stage 1: generate data
├── stage_analyze.py  # Stage 2: compute results
└── stage_plot.py     # Stage 3: create figures

config/example-pipeline/
└── default.json      # Parameters for reproducible runs

data/example-pipeline/
├── synthetic_data.json
└── results.json

tests/test_example_pipeline.py
```

Run stages:
```bash
uv run python -m viterbo.experiments.example_pipeline.stage_build
uv run python -m viterbo.experiments.example_pipeline.stage_analyze
uv run python -m viterbo.experiments.example_pipeline.stage_plot
```

## Directory Layout

All paths relative to `packages/python_viterbo/`:

| Artifact | Path |
|----------|------|
| Experiment code | `src/viterbo/experiments/<label>/` |
| Stage entrypoints | `src/viterbo/experiments/<label>/stage_<name>.py` |
| Spec | `src/viterbo/experiments/<label>/SPEC.md` |
| Configs | `config/<label>/<variant>.json` |
| Data artifacts | `data/<label>/` |
| Tests | `tests/test_<label>.py` |
| Thesis assets | `../latex_viterbo/assets/<label>/` |

## Commands

```bash
cd packages/python_viterbo
uv sync --extra dev          # Install dependencies
uv run ruff format .         # Format
uv run ruff check --fix .    # Lint
uv run pyright               # Type check
uv run pytest tests/         # Test
```

## Code Style

- Docstrings: inputs, outputs, shapes/dtypes
- Pure functions preferred
- Comments explain WHY, not WHAT
