---
name: git-cleanup
description: "Cleans up stale git branches, merged branches, orphaned remote refs, and identifies large files in history. Use for periodic repository maintenance."
allowed-tools: Bash(git *)
---

# Git Repository Cleanup

## Current State
!`git branch -a 2>/dev/null | head -30`
!`git remote -v 2>/dev/null`
!`git stash list 2>/dev/null`

---

## Cleanup Steps

### Step 1: Identify Merged Branches
List local branches already merged into main/master:
```bash
git branch --merged main 2>/dev/null || git branch --merged master 2>/dev/null
```

**Present the list to the user and ask for confirmation before deleting.**

Safe to delete (already merged):
```bash
git branch -d <branch-name>
```

### Step 2: Identify Stale Remote Branches
Prune remote tracking refs that no longer exist:
```bash
git remote prune origin --dry-run
```

After confirmation:
```bash
git remote prune origin
```

### Step 3: Identify Old Unmerged Branches
List branches with no commits in the last 90 days:
```bash
git for-each-ref --sort=committerdate --format='%(committerdate:short) %(refname:short)' refs/heads/ | head -20
```

**Never delete unmerged branches without explicit user approval.**

### Step 4: Clean Up Stashes
List all stashes:
```bash
git stash list
```

For old stashes (>30 days), suggest review and cleanup.

### Step 5: Repository Size Analysis
Check for large files:
```bash
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | sort -k3 -n -r | head -20
```

### Step 6: Garbage Collection
```bash
git gc --auto
```

---

## Output

### Cleanup Summary
| Action | Count | Status |
|--------|-------|--------|
| Merged branches deleted | X | Done/Pending |
| Stale remote refs pruned | X | Done/Pending |
| Old stashes reviewed | X | Done/Pending |

### Branches NOT Deleted (unmerged)
List branches that were skipped with last commit date.

### Space Recovered
Before and after repository size (if gc was run).

---

## Rules
- **NEVER force-delete** (`git branch -D`) without explicit user confirmation
- **NEVER delete** main, master, develop, or release branches
- Always show what will be deleted before doing it
- Prefer `--dry-run` first, then execute
