---
name: dagster-asset-sync
description: "Layer 6 of the knowledge-sync-loop: validate the ~833 Dagster assets in the 5-layer defs/ tree + ingest them into the dagster_assets Cognee cluster. Use when the user asks 'how do I validate Dagster assets', 'how do I keep the Dagster asset graph in sync', 'what does sync:dagster do', 'how do I write a Dagster asset health check', 'how do I find broken assets', or 'where is the Dagster asset dashboard'. Per the 2026-08-15-retroactive-pre-v7-cleanup-v1 change. Triggers: 'sync:dagster', 'sync_dagster_assets_to_cognee.py', 'dagster_sync_health', 'notebook 25', 'stedding/sync-reports/dagster-{date}.md', 'orchestration/defs/2_materials/...'."
---

# Dagster Asset Sync (Layer 6)

> **The Layer 6 of the knowledge-sync-loop architecture. Validates the 5-layer Dagster asset graph + ingests it into the `dagster_assets` Cognee cluster + emits metadata via the `dagster_sync_health` Dagster asset.**

## Why Layer 6 exists

The 5-layer pull-based sync architecture (from
`2026-08-15-knowledge-sync-loop-v1`) covered:

| Layer | What it syncs |
|:--|:--|
| 1. paths | pre-v7 path drift in source files |
| 2. ccc | the codebase semantic index |
| 3. cognee | openspec changes + specs + skills |
| 4. skills | agent SKILL.md metadata + references |
| 5. mcp | 14 MCP server health |

**The biggest gap**: the **Dagster asset graph** (~833 assets across
the 5-layer `orchestration/defs/` tree) wasn't validated by any of the
5 layers. The `2026-08-15-retroactive-pre-v7-cleanup-v1` change closes
this gap by adding Layer 6.

## What sync:dagster does

```bash
mise run sync:dagster
# → bash scripts/sync/dagster.sh
# → stedding/sync-reports/dagster-{date}.md
```

The script:

1. **Walks the 5-layer `orchestration/defs/` tree**:
   `1_ingestion/`, `2_materials/`, `3_model_lifecycle/`,
   `4_asset_generation/`, `5_agent_ops/`
2. **Counts `@asset`, `@asset_check`, `@sensor` decorators** per layer
3. **Counts YAML defs** (the Cianfhoghlaim Component YAML files)
4. **Counts the Cianfhoghlaim Component classes** at `orchestration/components/`
5. **Writes a per-group report** to
   `stedding/sync-reports/dagster-{date}.md`
6. **Returns 0** if the total asset count is > 0 (suspicious if 0)

## The new Dagster asset: dagster_sync_health

Lives at `orchestration/defs/sync_assets.py`. Emits:

| Metadata | Description |
|:--|:--|
| `asset_count` | Total `@asset` decorators across the 5 layers |
| `sensor_count` | Total `@sensor` decorators across the 5 layers |
| `group_count` | 5 (the canonical 5-layer convention) |
| `broken_asset_count` | 0 if healthy (placeholder for future expansion) |

Plus a `dagster_sync_alert` companion asset that fires when
`broken_asset_count > 0` + a `dagster_assets_sensor` that fires on
every `orchestration/defs/` file change.

## The new Cognee cluster: dagster_assets

Ingested by `scripts/sync_dagster_assets_to_cognee.py`. The script:

1. Walks `orchestration/defs/` + parses each .py file via `ast`
2. Extracts `@asset`, `@asset_check`, `@sensor` decorator usage
3. Renders a per-layer markdown summary
4. Adds the summary to the `dagster_assets` Cognee cluster

After sync, the Cognee graph has **8 typed clusters** (was 7):
- `cognee_docs`, `openspec_changes`, `openspec_specs`, `agent_skills`
- (5 existing) + `dagster_assets` (new)

## The consolidated marimo dashboard: sync_health.py

The Dagster tab in `notebooks/sync_health.py` reads the latest
`stedding/sync-reports/dagster-{date}.md` and surfaces:

- The per-layer breakdown table
- The total asset count vs the expected baseline (~833)
- The health status (OK if `total_assets > 0`)
- A full-report expander

Run via:
```bash
uv run marimo edit notebooks/sync_health.py
```

## The new CCC concept guide: dagster-asset-graph

The 21st concept guide in `.cocoindex_code/guides.yml`. Maps queries
about "Dagster asset graph", "5-layer defs/", "Cianfhoghlaim Components" to the
canonical files (the 5 layer folders + the 5 Cianfhoghlaim Component classes).

## Quick routing

| If you want to... | Do this |
|:--|:--|
| Validate the Dagster asset graph | `mise run sync:dagster` |
| Re-ingest into Cognee | `mise run sync:dagster && uv run python scripts/sync_dagster_assets_to_cognee.py` |
| See the asset health in Dagster UI | Open `dagster_sync_health` asset at `orchestration/defs/sync_assets.py` |
| See the asset sync dashboard | `uv run marimo edit notebooks/sync_health.py` (Dagster tab) |
| Read the latest report | `cat stedding/sync-reports/dagster-{date}.md` |
| Run all 6 sync layers | `mise run sync:all` |

## Cross-references

- `openspec/changes/2026-08-15-retroactive-pre-v7-cleanup-v1/` (this change)
- `openspec/specs/retrospective-cleanup/spec.md` (the capability spec)
- `scripts/sync/dagster.sh` (the Layer 6 sync script)
- `scripts/sync_dagster_assets_to_cognee.py` (the Cognee ingest)
- `orchestration/defs/sync_assets.py` (the `dagster_sync_health` asset)
- `notebooks/sync_health.py` (Dagster tab) (the dashboard)
- `.cocoindex_code/guides.yml` (the 21st CCC concept guide)
- `.agents/skills/knowledge-sync-loop/SKILL.md` (the parent sync loop skill)
- `.agents/skills/dagster/SKILL.md` (the core Dagster skill)
- `openspec/specs/dagster-5-layer-component-architecture/spec.md` (the 5-layer convention spec)
