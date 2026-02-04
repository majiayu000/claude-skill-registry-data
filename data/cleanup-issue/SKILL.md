---
name: cleanup-issue
description: Clean up after an issue PR is merged. Merges the PR if needed, removes the worktree, deletes the branch, updates main, and starts a fresh session. Use when asked to clean up an issue, finish an issue, or after a PR is approved.
---

# Cleanup Issue

Finalize and clean up after an issue is complete.

## Workflow

### 1. Merge PR (if not already merged)

Check PR status and merge if approved:

```bash
scripts/cleanup-issue.sh $ISSUE_NUMBER
```

This will:
- Find the PR for the issue branch
- Check if it's already merged
- If approved but not merged, merge it
- Remove the worktree
- Delete the local branch
- Update main
- Prune stale worktree references

### 2. Start fresh session

After cleanup completes successfully, output:

```
/new
```

This starts a fresh Claude Code session, ready for the next task.

## Manual Steps

If the script fails or you need manual control:

```bash
# Check PR status
gh pr view issue-$ISSUE_NUMBER --json state,mergeStateStatus

# Merge if ready
gh pr merge issue-$ISSUE_NUMBER --merge --delete-branch

# Remove worktree
git worktree remove .worktrees/issue-$ISSUE_NUMBER

# Delete local branch (if not auto-deleted)
git branch -d issue-$ISSUE_NUMBER

# Update main
git checkout main
git pull --ff-only origin main

# Prune worktree references
git worktree prune
```

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `scripts/cleanup-issue.sh` | Full cleanup: merge, remove worktree, update main |
