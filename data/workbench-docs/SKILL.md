---
name: workbench-docs
description: Documentation workflows for Workbench CLI. Use when creating or updating specs, ADRs, runbooks, guides, or general docs, and when syncing backlinks or change notes.
---

## Key settings

- `.workbench/config.json`: paths.docsRoot, paths.templatesDir, ids.width, prefixes, git.defaultBaseBranch, github.owner, github.repository.
- Use `workbench.ps1 config show --format json` to verify effective settings.

## Core workflows

1. Planning phase: create specs and architecture docs before major changes.
2. Doing phase: keep docs updated as implementation decisions change.
3. Keep doc front matter and backlinks in sync.
4. Summarize doc changes when publishing.

## Commands

Create a doc:
```bash
workbench.ps1 doc new --type doc --title "Title" --path docs/10-product/title.md --work-item TASK-0001
```

Create a spec:
```bash
workbench.ps1 doc new --type spec --title "Title" --path docs/10-product/title.md --work-item TASK-0001
```

Create an architecture doc:
```bash
workbench.ps1 doc new --type doc --title "System design" --path docs/20-architecture/system-design.md --work-item TASK-0001
```

Create an ADR:
```bash
workbench.ps1 doc new --type adr --title "Decision" --path docs/40-decisions/ADR-YYYY-MM-DD-title.md --work-item TASK-0001
```

Link a doc to work items:
```bash
workbench.ps1 doc link --type spec --path docs/10-product/title.md --work-item TASK-0001
```

Unlink a doc from work items:
```bash
workbench.ps1 doc unlink --type adr --path docs/40-decisions/ADR-YYYY-MM-DD-title.md --work-item TASK-0001
```

Sync front matter and backlinks:
```bash
workbench.ps1 doc sync --all --dry-run
workbench.ps1 doc sync --all
```

Summarize doc changes:
```bash
workbench.ps1 doc summarize --staged --update-index
```

## Output

- Markdown docs with Workbench front matter and backlinks.
- Updated work item references in docs and work items.

## Guardrails

- Keep doc types aligned with folder intent (product, architecture, decisions, runbooks).
- Always link docs to relevant work items with `--work-item` or `workbench.ps1 item link`.
- For major changes, write a spec before implementation.
- When decisions change, update or create the ADR.
- Prefer `workbench.ps1 doc` commands; `workbench.ps1 spec` and `workbench.ps1 adr` are deprecated.
