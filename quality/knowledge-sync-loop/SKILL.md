---
name: knowledge-sync-loop
description: "The 6-layer pull-based sync architecture that keeps all 8 knowledge surfaces in the cianfhoghlaim repo in sync — openspec changes/specs, agent skills, MCP servers, code (CCC), docs (Cognee), Dagster, agent definitions, and the lakehouse. Use when the user asks 'how do I keep openspec in sync with the rest of the repo', 'how do I sync skills + MCP + CCC + Cognee', 'what's the knowledge graph of openspec changes', 'how do I grow the knowledge surface over time', or 'where is the sync health dashboard'. Per the 2026-08-15-knowledge-sync-loop-v1 change + the 2026-08-14-firecrawl-mcp-ccc-dual-search-v1 change (Layer 12 — Firecrawl CCC concept guides). Triggers: 'sync:paths', 'sync:ccc', 'sync:cognee', 'sync:skills', 'sync:mcp', 'sync:firecrawl', 'sync:all', 'stedding/sync-reports/', 'deployment control panel', 'notebook 24'."
---

# Knowledge Sync Loop

> **The 5-layer pull-based sync architecture that keeps the 8 knowledge surfaces in the cianfhoghlaim repo in sync — and grows them over time via 3 feedback loops.**

## The 8 knowledge surfaces

The cianfhoghlaim repo has **8 knowledge surfaces** that need to stay
in sync:

1. **openspec changes** (71 specs, 14 pending, 303 archived)
2. **openspec specs** (71 capability specs)
3. **agent skills** (57 SKILL.md files in `.agents/skills/`)
4. **MCP servers** (14 servers wired in `opencode.json`)
5. **Dagster assets** (~833 across the 5-layer defs/ tree)
6. **CCC chunks** (257,957 / 8,845 files via CocoIndex Code)
7. **Cognee docs** (1,743 .md files / 7 typed clusters)
8. **agent definitions** (12-agent fleet + 8 NCCA subject specialists)

## The 5-layer pull-based sync architecture

The new `2026-08-15-knowledge-sync-loop-v1` change establishes a
5-layer sync architecture with 6 `mise run sync:*` tasks + 1
orchestrator. **Pull-based** (per the user's choice) = no Dagster
sensors fire automatically, no GitHub Actions run on every push;
the developer (or the bring-up smoke test) invokes the tasks
explicitly.

| Layer | Task | What it does | Output |
|:--|:--|:--|:--|
| 1. Path | `mise run sync:paths` | Detect pre-v7 path drift in source files (6 patterns) | `stedding/sync-reports/paths-{date}.md` |
| 2. Index | `mise run sync:ccc` | Refresh CCC index + append the 20th concept guide | `stedding/sync-reports/ccc-{date}.md` |
| 3. Graph | `mise run sync:cognee` | Ingest openspec + skills into 3 new Cognee clusters | `stedding/sync-reports/cognee-{date}.md` |
| 4. Skills | `mise run sync:skills` | Run `lint-skills.sh` + `validate_skill_references.py` | `stedding/sync-reports/skills-{date}.md` |
| 5. MCP | `mise run sync:mcp` | List all 14 MCP servers from `opencode.json` | `stedding/sync-reports/mcp-{date}.md` |
| **Orchestrator** | `mise run sync:all` | Runs 1-5 in sequence | `stedding/sync-reports/all-{date}.md` |

Each task writes its report to `stedding/sync-reports/` so the
deployment control panel (notebook 24) can consume it.

## The 3 feedback loops (how the system grows over time)

### Loop 1: Skill evolution

```
SKILL.md updated
  → sync:skills detects the change
  → lint:skills validates the frontmatter
  → validate_skill_references.py checks the references
  → Cognee cognifies the skill into the agent_skills cluster
  → CCC reindexes (the 20th concept guide "openspec-archive-search" can find it)
  → The deployment control panel surfaces the new skill
```

**Growth trigger:** When a skill's `description:` field changes, the
loop automatically re-cognifies it into Cognee. Over time, the
`agent_skills` cluster grows a knowledge graph of all 57+ skills +
their relationships.

### Loop 2: openspec evolution

```
openspec change archived (e.g. via `openspec archive <id> --yes`)
  → sync:openspec-to-ccc updates the 20th concept guide
  → sync:openspec-to-cognee ingests the archived change
  → The Cognee graph adds the change as a new node
  → The deployment control panel shows the new "archived" status
```

**Growth trigger:** When an openspec change is archived, it
automatically becomes part of the knowledge graph. Over time, the
graph accumulates a complete history of every change + spec delta +
implementation.

### Loop 3: MCP evolution

```
MCP server config changes (in opencode.json)
  → sync:mcp detects the new server
  → Validates the server is reachable + responds to a healthcheck
  → Adds the server to the Cognee agent_skills cluster
  → The deployment control panel shows the new server
```

**Growth trigger:** When `opencode.json` is modified with a new MCP
server, the loop validates + cognifies it. Over time, the graph
keeps a complete inventory of all 14+ MCP servers + their health
state.

## Quick routing

| If you want to... | Do this |
|:--|:--|
| Bring the repo's knowledge state up to date | `mise run sync:all` |
| Check just the path drift | `mise run sync:paths` |
| Check just the skills | `mise run sync:skills` |
| Read the latest sync report | `cat stedding/sync-reports/all-$(date +%Y-%m-%d).md` |
| See the canonical sync health | Open `notebooks/24_deployment_control_panel.py` in marimo |
| Add a new MCP server to the loop | Edit `opencode.json` + run `mise run sync:mcp` |
| Add a new openspec change to the loop | `openspec archive <id> --yes` + run `mise run sync:all` |
| Add a new skill to the loop | Edit `.agents/skills/<slug>/SKILL.md` + run `mise run sync:skills` |

## Cross-references

- `openspec/changes/2026-08-15-knowledge-sync-loop-v1/` — the change dir
- `openspec/specs/knowledge-sync-loop/spec.md` — the new spec
- `stedding/sync-reports/` — the canonical per-layer reports dir
- `scripts/sync/` — the 6 standalone shell scripts
- `scripts/sync_openspec_to_ccc.py` — the 20th concept guide appender
- `scripts/validate_skill_references.py` — the skill path validator
- `scripts/cognee_ingest_openspec.py` — the openspec Cognee ingester
- `scripts/cognee_ingest_skills.py` — the skills Cognee ingester
- `orchestration/defs/sync_assets.py` — the Dagster sync_health asset
- `notebooks/24_deployment_control_panel.py` — the sync health dashboard
- `openspec/changes/2026-08-15-centralized-model-schema-registry-and-deployment-control-panel-v1/` — Change B (the model-registry change that consumes the sync reports)