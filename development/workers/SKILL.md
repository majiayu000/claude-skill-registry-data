---
name: workers
description: List all active Claude workers and their git worktrees. Shows branch status, commits, and suggests next actions. Use to see what workers are running.
allowed-tools: Bash, Read
---

# Workers Skill

List and manage active Claude workers.

## Usage

```
/workers
```

## Instructions

When the user invokes `/workers`, show the status of all worktrees and workers:

### 1. List Git Worktrees

```bash
git worktree list
```

### 2. Show Worker Details

For each worktree (excluding main):
- Branch name and last commit
- Files changed vs main
- Whether it's ahead/behind main

```bash
# For each worktree branch
git log <branch> --oneline -1
git diff main...<branch> --stat | tail -1
git rev-list --left-right --count main...<branch>
```

### 3. Format Output

Display as a table:

```
| Worktree | Branch | Last Commit | Changes | Status |
|----------|--------|-------------|---------|--------|
| ../artemis-issue-42 | feat/issue-42-retry | abc123 Add retry | 3 files | +2 ahead |
| ../artemis-feat-logging | feat/add-logging | def456 Add logs | 5 files | +1 ahead |
```

### 4. Suggest Actions

Based on status, suggest:
- Workers with commits → "Ready for PR?"
- Stale worktrees (no recent commits) → "Clean up?"
- Workers behind main → "Rebase needed"

### 5. Quick Actions

Offer shortcuts:
- `/worker-cleanup <worktree>` - Remove a specific worktree
- `/worker-pr <branch>` - Create PR from worker branch
- `/worker-continue <worktree> "additional task"` - Send more work

## Notes

- Only shows worktrees in the parent directory (`../artemis-*`)
- Main repo worktree is always excluded from the list
- Worktrees can be filtered by status if needed
