---
name: reset-epic
description: Reset an epic's test data — close PRs, delete branches, reopen issues, revert code
arguments: "<epic-number>"
---

# /reset-epic - Reset Epic Test Data

Fully resets an epic so it can be re-tested from scratch.

**Arguments:** $ARGUMENTS

## Usage

```
/reset-epic <epic-number>     # e.g. /reset-epic 287, to reset that epic for retesting
```

## What It Does

Given an epic issue number, perform ALL of the following:

1. **Identify stories**: Parse the epic body for linked issue numbers
2. **Close open PRs**: Find all open PRs referencing any story number or the epic number. Close them.
3. **Delete remote branches**: Find and delete any remote branches related to the epic (e.g., `epic/<number>-*`, `feat/<story>-*`, `revert/epic-<number>-*`)
4. **Delete local branches**: Delete any local branches matching the same patterns (skip the current branch)
5. **Reopen issues**: Reopen all story issues and the epic itself if any were closed
6. **Uncheck task lists**: Edit the epic body to uncheck all `- [x]` checkboxes back to `- [ ]`
7. **Clear epic-state memory**: Delete all entries in the `epic-state` memory namespace for this epic and its stories (keys: `epic-<N>`, `story-<N>` for each story). Use `mcp__moflo__memory_list` with namespace `epic-state` to find entries, then `mcp__moflo__memory_delete` for each.
8. **Verify clean state**: Confirm all stories are OPEN, no related PRs are open, no related branches exist, and epic-state memory is empty

## Output

Print a summary table:

```
Epic #<N> Reset Summary
─────────────────────────
Issues reopened: X
PRs closed:     X
Branches deleted: X (remote) / X (local)
Status: CLEAN — ready for retesting
```

## Important

- Never delete `main` or the current branch
- Use `gh` CLI for all GitHub operations
- If a revert of merged code is needed, note it but DO NOT auto-revert (ask the user first)
- This is a destructive operation — confirm with the user before executing if there are merged PRs that might need code reverts
