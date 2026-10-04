---
name: agents-sync
description: "Layer 10 of the knowledge-sync-loop — the agent definitions surface validator. Use when the user asks 'are all agents registered', 'is the agent fleet healthy', 'what are the NCCA subject specialists', 'does the agent registry match the 12-agent fleet', 'what does sync:agents do'. Per the 2026-08-15-agent-definitions-sync-loop-v1 change. Triggers: 'sync:agents', 'agent_definitions', 'agent-fleet-search', '12-agent fleet', 'NCCA subject specialists', 'agent_registry', 'agents:smoke', 'agents:audit', 'agents:reproduce'."
---

# Agent Definitions Sync (Layer 10 of the knowledge-sync-loop)

> **The Layer 10 of the 10-layer pull-based sync architecture. Validates the 188 agent files + the 12-agent fleet + the 8 NCCA subject specialists.**

## Why Layer 10?

The 9-layer architecture covered 12 of the 14 knowledge surfaces. The
next-biggest remaining gap was the **agent definitions surface** - the
188 .py agent files in 7 subdirs (agents/ + agents/adk/ + agents/agno/ +
agents/api/ + agents/tools/ + agents/tuatha/ + agents/meaisinfhoghlaim/).

Agent definition drift is silent: when a developer adds a new agent
to the 12-agent fleet but doesn't register it in `agent_registry.py`
+ doesn't update the routing keywords + doesn't add an AGENTS.md,
the breakage doesn't surface until the next agent registration
test. The 8 NCCA subject specialists (in agents/tuatha/agents/) are
particularly prone to drift because they were added incrementally.

Layer 10 closes the agent definitions gap.

## What Layer 10 covers

`bash scripts/sync/agents.sh` walks the 7 agent subdirs + produces a
per-subdir report to `stedding/sync-reports/agents-{date}.md` with:
- The per-subdir .py file counts
- The 5 AGENTS.md files
- The 8 NCCA subject specialists (in agents/tuatha/agents/)
- The 12-agent fleet + the 4 NCCA subjects + the remaining subdirs
- Drift detection (unregistered agents + stale model refs)

The orchestrator `mise run sync:agents` runs all 5 sub-layers +
writes a unified report to `stedding/sync-reports/agents-all-{date}.md`.

## The 5 sub-layers

| Sub-layer | Task | What it does |
|:--|:--|:--|
| 1 | `sync:agents-drift` | Detects unregistered agents + stale model refs |
| 2 | `sync:agents-ccc` | Appends the 25th CCC concept guide (`agent-fleet-search`) + reindex |
| 3 | `sync:agents-cognee` | Ingests the 188 agent files into the 14th Cognee cluster (`agent_definitions`) |
| 4 | `sync:agents-test` | Runs the agent registration test + reports pass/fail per agent |
| 5 | `sync:agents-lint` | Per-subdir stats (7 subdirs + 5 AGENTS.md + 8 NCCA subject specialists) |

## The new artifacts

| Artifact | File | Purpose |
|:--|:--|:--|
| `agents-sync` skill | `.agents/skills/agents-sync/SKILL.md` | this file |
| 25th CCC guide | `agent-fleet-search` | surfaces the 188 agent files via CCC |
| 14th Cognee cluster | `agent_definitions` | the 188 agent files |
| `agents_sync_health` asset | `orchestration/defs/sync_assets.py` | Dagster asset |
| `scripts/cognee_ingest_agent_definitions.py` | ingestor | The canonical Cognee cluster ingestor |
| `notebooks/sync_health.py` | dashboard | Agents tab in the grouped sync-health marimo surface |

## Agent definitions evolution feedback loop

The system grows its knowledge surface over time via the agent
definitions evolution feedback loop:

```
agent file modified
  → sync:agents-cognee detects the change
  → re-cognifies the modified agent into the agent_definitions cluster
  → sync:agents-ccc updates the 25th concept guide
  → The deployment control panel (notebook 24) surfaces the change
```

## Quick routing

| If you want to... | Do this |
|:--|:--|
| Check the agent fleet health | `mise run sync:agents` |
| See the per-subdir breakdown | `cat stedding/sync-reports/agents-$(date +%Y-%m-%d).md` |
| Add a new agent | Create the .py file in the right subdir + register it in `agent_registry.py` + add it to routing keywords + update `agents/AGENTS.md` + run `sync:agents` |
| Fix a registration drift | `sync:agents-drift` will list the unregistered agents; register + re-run |
| See the agent definitions dashboard | Open `notebooks/sync_health.py` (Agents tab) |
| Run the agent registration test | `mise run agents:smoke` |

## Cross-references

- `openspec/changes/2026-08-15-knowledge-sync-loop-v1/` (the foundation)
- `openspec/changes/2026-08-15-stacks-sync-loop-v1/` (Layer 8)
- `openspec/changes/2026-08-15-dlt-sync-loop-v1/` (Layer 9)
- `agents/` (the 12-agent fleet + the 188 .py files)
- `agents/AGENTS.md` (the canonical agent documentation)
- `agents/tuatha/` (the 8 NCCA subject specialists)
