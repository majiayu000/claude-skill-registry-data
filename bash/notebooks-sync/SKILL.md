---
name: notebooks-sync
description: "Layer 11 of the knowledge-sync-loop — the notebooks surface validator. Use when the user asks 'are all notebooks registered', 'is the notebook fleet healthy', 'does the notebook registry match the CI flow', 'what does sync:notebooks do', 'how many notebooks are there'. Per the 2026-08-15-notebooks-sync-loop-v1 change. Triggers: 'sync:notebooks', 'notebooks', 'notebook-search', 'marimo', '@app.cell', 'notebooks/cli.py', 'notebooks/_shared'."
---

# Notebooks Sync (Layer 11 of the knowledge-sync-loop)

> **The Layer 11 of the 11-layer pull-based sync architecture. Validates the 104 notebook files (20+ numeric prefixes) at `notebooks/`.**

## Why Layer 11?

The 10-layer architecture covered 13 of the 14 knowledge surfaces. The last
remaining gap was the **notebooks surface** - the 104 .py notebook files at
`notebooks/` (with 108 `@app.cell` decorators across 20+ numeric
prefixes).

Notebook drift is silent: when a developer adds a new BIEP per-subdir notebook
but doesn't register it in the `notebooks/cli.py` GROUPS tuple, the
`uv run python notebooks/cli.py list` command misses it. The 16 speedrun
+ 12 corpus + 7 educational stages + 6 dev env tools + 11 BIEP per-subdir + 7
official media + ... each have their own patterns, and there's no canonical
check that they all conform.

Layer 11 closes the notebooks gap.

## What Layer 11 covers

`bash scripts/sync/notebooks.sh` walks the 20+ numeric prefixes at
`notebooks/` + produces a per-prefix report to
`stedding/sync-reports/notebooks-{date}.md` with:
- The per-prefix notebook counts
- The @app.cell decorator counts
- The canonical `notebooks/_shared/` helpers + `notebooks/cli.py`

The orchestrator `mise run sync:notebooks` runs all 5 sub-layers +
writes a unified report to `stedding/sync-reports/notebooks-all-{date}.md`.

## The 5 sub-layers

| Sub-layer | Task | What it does |
|:--|:--|:--|
| 1 | `sync:notebooks-drift` | Detects unregistered notebooks + broken @app.cell decorators |
| 2 | `sync:notebooks-ccc` | Appends the 26th CCC concept guide (`notebook-search`) + reindex |
| 3 | `sync:notebooks-cognee` | Ingests the 104 notebook files into the 15th Cognee cluster (`notebooks`) |
| 4 | `sync:notebooks-test` | Runs the notebook import test + reports pass/fail per notebook |
| 5 | `sync:notebooks-lint` | Per-prefix stats (20+ prefixes + 104 notebooks + canonical helpers) |

## The new artifacts

| Artifact | File | Purpose |
|:--|:--|:--|
| `notebooks-sync` skill | `.agents/skills/notebooks-sync/SKILL.md` | this file |
| 26th CCC guide | `notebook-search` | surfaces the 104 notebook files via CCC |
| 15th Cognee cluster | `notebooks` | the 104 notebook files |
| `notebooks_sync_health` asset | `orchestration/defs/sync_assets.py` | Dagster asset |
| `scripts/cognee_ingest_notebooks.py` | ingestor | The canonical Cognee cluster ingestor |
| `notebooks/sync_health.py` | dashboard | Notebooks tab in the grouped sync-health marimo surface |

## Notebooks evolution feedback loop

The system grows its knowledge surface over time via the
notebooks evolution feedback loop:

```
notebook file modified
  → sync:notebooks-cognee detects the change
  → re-cognifies the modified notebook into the notebooks cluster
  → sync:notebooks-ccc updates the 26th concept guide
  → The deployment control panel (notebook 24) surfaces the change
```

## Quick routing

| If you want to... | Do this |
|:--|:--|
| Check the notebook fleet health | `mise run sync:notebooks` |
| See the per-prefix breakdown | `cat stedding/sync-reports/notebooks-$(date +%Y-%m-%d).md` |
| Add a new notebook | Create the .py file in the right prefix dir + register it in `notebooks/cli.py` GROUPS + update `notebooks/AGENTS.md` + run `sync:notebooks` |
| Fix a registration drift | `sync:notebooks-drift` will list the unregistered notebooks; register + re-run |
| See the notebooks dashboard | Open `notebooks/sync_health.py` (Notebooks tab) |
| Run the notebook import test | `uv run python -c "import notebooks.X"` |

## Cross-references

- `openspec/changes/2026-08-15-knowledge-sync-loop-v1/` (the foundation)
- `openspec/changes/2026-08-15-stacks-sync-loop-v1/` (Layer 8)
- `openspec/changes/2026-08-15-dlt-sync-loop-v1/` (Layer 9)
- `openspec/changes/2026-08-15-agent-definitions-sync-loop-v1/` (Layer 10)
- `notebooks/` (the 104 .py files + 108 with @app.cell)
- `notebooks/_shared/` (the canonical notebook helpers)
- `notebooks/cli.py` (the canonical notebook GROUPS)
