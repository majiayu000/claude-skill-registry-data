---
name: clean-gone-branches
description: Delete local git branches whose remotes are gone, after verifying via gh CLI that each was actually merged.
license: MIT
compatibility: claude cursor opencode
metadata:
  version: "1.0.0"
  languages: all
  audience: developers
  workflow: git
  since: "2026-03-19"
---

## What I do

Clean up orphaned local branches (those whose remote tracking branch is `[gone]`) by:

1. Running `git fetch --prune` to sync remote state.
2. Listing all local branches with `[gone]` remote tracking refs.
3. Verifying each branch's PR status via `gh pr list --state all` to confirm it was merged (or closed).
4. Showing the user a summary table with PR state and merge date.
5. Asking for confirmation before deleting.
6. Force-deleting confirmed branches with `git branch -D`.

## When to use me

- After a sprint or a batch of PRs land and you want to clean up stale local branches.
- Any time `git branch -vv` shows several `[gone]` entries.
- Before switching repos or doing a clean checkout.

## Workflow

### Step 1: Fetch and prune
```bash
git fetch --prune
```

### Step 2: Find orphaned branches
```bash
git branch -vv | grep ': gone]'
```
If nothing found, report "No orphaned branches found." and stop.

### Step 3: Verify PR status via gh CLI
For each orphaned branch, run:
```bash
gh pr list --head "<branch>" --state all --json state,mergedAt,title \
  --jq '.[0] | "\(.state) | merged: \(.mergedAt // "N/A") | \(.title)"'
```

Build a summary table:
| Branch | PR State | Merged At | PR Title |
|--------|----------|-----------|----------|

Flag any branches that are **not MERGED** (e.g. OPEN or CLOSED without merge) — these need user attention before deletion.

### Step 4: Confirm with user
Show the table and ask:
- "Delete all MERGED branches now?"

If any branch has no PR or is not merged, exclude it from the default delete list and call it out explicitly:
- "These branches have no merged PR — skip them or confirm to force-delete anyway?"

### Step 5: Delete
```bash
git branch -D <branch1> <branch2> ...
```

Report each deleted branch with its last commit hash.

---

## Behavior rules

- Never delete without explicit user confirmation.
- Always use `git branch -D` (force) since git's merge check is against the local default branch, not the remote — remote deletion already confirms the work is done.
- If `gh` is not available or returns no results, warn the user and do not auto-delete.
- Prefer deleting all confirmed-merged branches in one command rather than one-by-one.
