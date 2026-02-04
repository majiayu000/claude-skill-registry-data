---
name: clean-gone-branches
description: Clean up local git branches marked as [gone] (deleted on remote but still exist locally). Use when the user wants to clean up stale branches, remove gone branches, or delete branches that no longer exist on remote.
allowed-tools: Bash
---

# Clean Gone Branches

Automatically clean up all local git branches that have been deleted from the remote repository (marked as `[gone]`).

## Instructions

### Step 1 - List Branches to Identify [gone] Status

Execute this command to see all local branches and their status:

```bash
git branch -v
```

**What to look for:**
- Branches marked with `[gone]` have been deleted from the remote
- Branches with a `+` prefix have associated worktrees and will be skipped (must be cleaned up manually)
- Branches without a `+` prefix can be safely deleted
- If no branches show `[gone]`, inform the user that no cleanup is needed and STOP

### Step 2 - Delete [gone] Branches (Skip Those with Worktrees)

Execute this command to clean up [gone] branches without worktrees:

```bash
git branch -v | grep '\[gone\]' | while read line; do
  if [[ $line =~ ^[+] ]]; then
    branch=$(echo "$line" | awk '{print $1}' | sed 's/^+//')
    echo "Skipping $branch (has worktree - remove worktree first)"
  else
    branch=$(echo "$line" | sed 's/^[* ]//' | awk '{print $1}')
    echo "Deleting branch: $branch"
    git branch -D "$branch"
  fi
done
```

**What this does:**
1. Finds all branches marked as `[gone]`
2. For each branch:
   - If it has a `+` prefix (worktree exists), skip it and warn the user
   - Otherwise, delete the branch using `-D` (force delete)
3. Provides clear feedback about which branches were deleted and which were skipped

### Step 3 - Report Results

After execution, inform the user:
- How many branches were deleted
- How many branches were skipped (with worktrees)
- If any branches were skipped, suggest they need manual worktree cleanup
- Confirmation that cleanup is complete

If no branches were marked as `[gone]`, report that no cleanup was needed.

## Important Rules

- **DO NOT** attempt to delete branches with worktrees - skip them and warn the user
- Use `git branch -D` (force delete) because [gone] branches are already merged/deleted remotely
- Show clear feedback for each operation (deleted vs skipped)
- Inform users that skipped branches require manual worktree cleanup first

## Expected Output

**Example with branches to clean:**
```
Deleting branch: fix/obsolete-fix
Skipping feature/old-feature (has worktree - remove worktree first)
Deleting branch: chore/cleanup-task

Cleanup complete:
- Deleted 2 branches marked as [gone]
- Skipped 1 branch with worktree

Note: Branches with worktrees must be cleaned up manually using 'git worktree remove' before the branch can be deleted.
```

**Example with no cleanup needed:**
```
No branches marked as [gone] found. Your local repository is already clean.
```

**Example with only worktree branches:**
```
Skipping feature/old-feature (has worktree - remove worktree first)
Skipping fix/another-branch (has worktree - remove worktree first)

Cleanup complete:
- Deleted 0 branches marked as [gone]
- Skipped 2 branches with worktrees

Note: Branches with worktrees must be cleaned up manually using 'git worktree remove' before the branch can be deleted.
```

## Error Handling

If any command fails:
- Show the error message to the user
- Explain what went wrong
- Continue processing other branches if possible
- Report which branches were successfully cleaned and which failed
