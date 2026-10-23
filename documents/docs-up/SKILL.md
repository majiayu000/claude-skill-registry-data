---
name: docs-up
description: Audit code changes on the current branch and update docs/ + .claude/rules/ to stay in sync. Run before /pr.
---

# Skill: Sync Docs

Audit all code changes on the current branch vs main, then update documentation files to reflect those changes.

## Steps

### 1. Identify what changed

```bash
git diff main...HEAD --name-only
```

Categorize changed files into impact zones:

| Changed path pattern | Docs impact |
|----------------------|-------------|
| `src/medox/agent/tools/` | `docs/agent/tools.mdx`, `.claude/rules/agent.md` |
| `src/medox/agent/nodes/` | `docs/agent/overview.mdx`, `docs/agent/guardrails.mdx` |
| `src/medox/agent/graph_agent.py` | `docs/agent/overview.mdx` |
| `src/medox/pipeline/assets/` | `docs/pipeline/overview.mdx`, `.claude/rules/pipeline.md` |
| `src/medox/pipeline/io/` | `docs/pipeline/silver.mdx`, `docs/pipeline/bronze.mdx` |
| `dbt/models/silver/` | `docs/dbt/overview.mdx`, `docs/pipeline/silver.mdx`, `.claude/rules/dbt.md` |
| `dbt/models/sources.yml` | `docs/dbt/overview.mdx`, `docs/pipeline/silver.mdx` |
| `tests/e2e/prompts.yaml` | no docs change needed |
| `tests/` (other) | no docs change needed |
| `scripts/` | `docs/development/setup.mdx` (if new script) |

### 2. For each impacted doc, read it and check for staleness

For each doc file identified above:
1. Read the current doc file
2. Read the changed source files
3. Compare: are there new entities (tools, models, assets, nodes) missing from the doc?
4. Compare: are there renamed/removed entities still referenced in the doc?
5. Compare: are there changed behaviors (e.g. new parameters, new strategies) not reflected?

### 3. Apply updates

For each stale doc:
- Add new entries to tables, diagrams, and source lists
- Update descriptions that no longer match the code
- Remove references to deleted entities
- Keep the existing style and structure of each doc file

Also check `.claude/rules/` files:
- `agent.md` — tools table, node list
- `pipeline.md` — asset graph, key files table
- `dbt.md` — current Silver models list

### 4. Report

After all edits, output a summary:

```
Docs synced:
- docs/agent/tools.mdx — updated check_interactions section
- docs/pipeline/overview.mdx — added new asset
- (no changes needed for docs/dbt/overview.mdx)
```

If no docs need updating, report: "All docs are up to date."

## Rules

- Never rewrite entire sections — make minimal, targeted edits
- Keep all docs in English (same as code comments)
- Do not touch `docs/introduction.mdx` or `docs/quickstart.mdx` unless the overall architecture changed
- Do not commit — leave changes staged for the user to review before `/pr`
