---
name: workbench-architecture
description: Architecture and ADR workflows for Workbench CLI. Use when documenting system design, decisions, tradeoffs, or rationale that must be tracked over time.
---

## Key settings

- `.workbench/config.json`: paths.docsRoot, git.defaultBaseBranch.
- Use `workbench config show --format json` to confirm defaults.

## Core workflows

1. Planning phase: create architecture docs for design intent and scope.
2. When a decision is made or changes, create or update an ADR.
3. Link ADRs and architecture docs to work items and specs.

## Commands

Create an architecture doc:
```bash
workbench doc new --type doc --title "Subsystem overview" --path docs/20-architecture/subsystem-overview.md --work-item TASK-0001
```

Create an ADR:
```bash
workbench doc new --type adr --title "Decision title" --path docs/40-decisions/ADR-YYYY-MM-DD-title.md --work-item TASK-0001
```

Link existing docs to a work item:
```bash
workbench item link TASK-0001 --spec /docs/10-product/spec.md --adr /docs/40-decisions/ADR-YYYY-MM-DD-title.md
```

Sync backlinks:
```bash
workbench doc sync --all
```

## Output

- Architecture docs and ADRs with consistent front matter.
- Work items that reference related specs and ADRs.

## Guardrails

- Use ADRs for decisions, architecture docs for structure and flows.
- Keep ADR status updated (proposed, accepted, superseded, deprecated).
- If an ADR does not exist for a significant decision, create one.
