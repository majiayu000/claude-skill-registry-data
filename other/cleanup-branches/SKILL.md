---
name: cleanup-branches
description: "Git Branch Cleanup"
argument-hint: "[optional branch pattern]"
disable-model-invocation: true
---

# Git Branch Cleanup

Clean up merged/stale local branches and remove orphaned worktrees.

## Instructions

Perform git branch cleanup for this repository:

### Step 1: Update main and fetch remote state
```bash
git fetch --prune origin
git checkout main
git pull origin main
```

### Step 2: List worktrees and remove stale ones
```bash
git worktree list
```
Remove any worktrees that are no longer needed (branches merged or abandoned).

### Step 3: Identify branches to clean up

**Check for truly merged branches:**
```bash
git branch --merged main
```

**Check for squash-merged branches (compare with GitHub PRs):**
```bash
gh pr list --state merged --limit 50 --json headRefName,number,title
```

Cross-reference local branches against merged PRs. If a local branch has a merged PR, it's safe to delete.

**List local branches with their PR status:**
```bash
for branch in $(git branch --format='%(refname:short)' | grep -v main); do
  pr_state=$(gh pr list --head "$branch" --state all --json state --jq '.[0].state // "NO_PR"')
  echo "$branch: $pr_state"
done
```

### Step 4: Delete merged branches

For each branch that has been merged (either via `--merged` or has a MERGED PR):
```bash
git branch -d <branch-name>    # Safe delete (fails if not merged)
git branch -D <branch-name>    # Force delete (for squash-merged)
```

### Step 5: Clean up remote tracking branches
```bash
git remote prune origin
```

### Step 6: Report summary

Report what was cleaned up:
- Number of branches deleted
- Number of worktrees removed
- Any branches kept and why (no PR, open PR, etc.)

## Safety Rules

1. **Never delete `main`**
2. **Confirm before force-deleting** branches without merged PRs
3. **List before deleting** - always show what will be removed first
4. **Keep branches with OPEN PRs**
