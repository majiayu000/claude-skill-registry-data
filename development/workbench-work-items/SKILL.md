---
name: workbench-work-items
description: Work item management for Workbench CLI. Use when creating, updating, linking, or closing work items and tracking execution status.
---

## Key settings

- `.workbench/config.json`: paths.itemsDir, paths.doneDir, ids.width, prefixes, git.branchPattern.
- Status values: draft, ready, in-progress, blocked, done, dropped.

## Core workflows

1. Ensure planning artifacts exist (specs, ADRs, architecture docs) before major work.
2. Create a work item and set its initial status.
3. Link related specs, ADRs, files, PRs, or issues.
4. Update status and close work items when done.

## Commands

Create a task:
```bash
workbench item new --type task --title "Do the thing" --status draft --priority medium --owner platform
```

Update status:
```bash
workbench item status TASK-0001 in-progress --note "started implementation"
```

Close and move to done:
```bash
workbench item close TASK-0001 --move
```

Link docs or PRs:
```bash
workbench item link TASK-0001 --spec /docs/10-product/spec.md --adr /docs/40-decisions/ADR-YYYY-MM-DD-title.md --pr https://github.com/org/repo/pull/1
```

## Output

- Work items in `docs/70-work/items` (active) and `docs/70-work/done` (closed).
- Linked docs and external artifacts tracked in front matter.

## Guardrails

- Use a work item for every meaningful change and link the supporting docs.
- Keep status accurate so reports and boards stay reliable.
- If a decision happens during work, update/create the ADR and link it.
