---
name: workbench-sync
description: Sync workflows for Workbench CLI. Use when aligning local work items with GitHub issues, creating branches, or reconciling doc backlinks.
---

## Key settings

- `.workbench/config.json`: github.owner, github.repository, github.host, git.defaultBaseBranch.
- Ensure `gh auth login` is complete before syncing issues.

## Core workflows

1. Import missing GitHub issues into local work items.
2. Create missing GitHub issues for active work items.
3. Create branches for active items.
4. Sync doc backlinks and front matter.

## Commands

Dry-run sync:
```bash
workbench.ps1 sync --dry-run
```

Sync a specific item and prefer GitHub content:
```bash
workbench.ps1 item sync --id TASK-0001 --prefer github
```

Bulk sync (local wins on conflicts):
```bash
workbench.ps1 sync --items
```

Import unlinked GitHub issues (slower):
```bash
workbench.ps1 sync --items --import-issues
```

Sync doc backlinks (include done items when needed):
```bash
workbench.ps1 doc sync --all
workbench.ps1 doc sync --all --include-done
```

## Output

- New work items from GitHub issues.
- New GitHub issues and branches for active work items.
- Updated doc backlinks and front matter.

## Guardrails

- Use `--dry-run` before creating issues or branches.
- `workbench.ps1 sync` defaults to linked work items only; use `--import-issues` to pull unlinked GitHub issues.
- Terminal items (done/dropped) do not create issues or branches by default.
- Sync is not a replacement for specs/ADRs; create or update them during planning.
