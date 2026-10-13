---
name: git-prune-branches
description: "Delete merged git branches — local, remote, or both. Use when the user says 'prune branches', 'clean up branches', 'delete merged branches', or stale branches pile up after a round of PR merges."
argument-hint: "[local|remote|both]"
---

# Git Prune Branches

Scope comes from `$ARGUMENTS`: `local`, `remote`, or `both`. If no scope is given, ask with AskUserQuestion (options: both, local, remote) — do not guess.

## Collect candidates

- **Local**: `git branch --merged <main>` — branches merged into the main branch.
- **Remote**: `git fetch --prune` first, then `git branch -r --merged origin/<main>`.

Never delete:

- The currently checked-out branch
- Protected branches: `main`, `master`, `develop`, `development`, `staging`, `production`
- Branches that are not fully merged (unless the user explicitly asks)

## Confirm, then delete

1. Show the deletion list, local and remote separately.
2. Ask for confirmation and wait for a yes. Remote deletion affects every user of the repo and is not easily undone — never skip this.
3. Delete with `git branch -d <branch>` (never `-D`, so unmerged branches are refused) and `git push origin --delete <branch>`.
4. Report what was deleted and anything that failed.
