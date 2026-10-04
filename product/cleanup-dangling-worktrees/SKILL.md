---
name: cleanup-dangling-worktrees
description: Removes git worktrees for merged PRs while preserving active development. Use when cleaning up after feature merges or when worktree directory accumulates stale branches.
---

# Cleanup Dangling Worktrees

## Overview

Git worktrees accumulate over time as features are developed and merged. This skill safely cleans up worktrees that are no longer needed because their associated feature PRs have been merged.

**Core principle:** Only remove a worktree if its feature PR is CONFIRMED merged. Never remove active development worktrees.

## Safety Rules

**A worktree is ONLY considered dangling if ALL of these are true:**

1. The worktree's branch has an associated PR
2. That PR has been MERGED (not just closed)
3. The worktree has no uncommitted changes
4. The worktree has no unpushed commits

**NEVER remove a worktree if:**

- No PR exists for the branch (might be WIP)
- PR exists but is still open
- PR was closed without merging
- Worktree has uncommitted changes
- Worktree has commits not pushed to remote
- Cannot determine PR status (network issues, etc.)

## Execution Steps

### Step 1: List All Worktrees

```bash
git worktree list --porcelain
```

Parse output to get worktree paths and branches. Skip the main worktree (the bare repository or main checkout).

### Step 2: For Each Worktree, Check Safety

For each worktree (excluding main):

#### 2a. Check for Uncommitted Changes

```bash
cd /path/to/worktree && git status --porcelain
```

If output is non-empty, **SKIP** - worktree has uncommitted changes.

#### 2b. Check for Unpushed Commits

```bash
cd /path/to/worktree && git log @{upstream}..HEAD --oneline 2>/dev/null
```

If output is non-empty, **SKIP** - worktree has unpushed commits.

If upstream doesn't exist, **SKIP** - branch was never pushed.

#### 2c. Find Associated PR

```bash
# Get the branch name
BRANCH=$(cd /path/to/worktree && git branch --show-current)

# Find PR for this branch
gh pr list --head "$BRANCH" --state all --json number,state,mergedAt --jq '.[0]'
```

If no PR found, **SKIP** - no PR means possibly active development.

#### 2d. Check PR Status

Parse the PR info:

- If `state` is not "MERGED", **SKIP**
- If `mergedAt` is null/empty, **SKIP**
- Only if PR is confirmed MERGED, mark for cleanup

### Step 3: Remove Dangling Worktrees

For each worktree confirmed as dangling:

```bash
# Remove the worktree
git worktree remove /path/to/worktree

# Optionally delete the branch (if fully merged)
git branch -d branch-name
```

**Note:** Use `git worktree remove` not `rm -rf` - this properly unregisters the worktree.

### Step 4: Prune Worktree Metadata

After removals, clean up stale worktree metadata:

```bash
git worktree prune
```

## Output Format

Report findings in this format:

```
## Worktree Cleanup Report

### Worktrees Found
- Total worktrees: [N]
- Main/primary: 1 (skipped)
- Feature worktrees checked: [N-1]

### Status by Worktree

| Worktree | Branch | PR | PR Status | Action |
|----------|--------|-----|-----------|--------|
| .worktrees/auth | feature/auth | #42 | MERGED | Removed |
| .worktrees/api | feature/api | #51 | Open | Kept (PR open) |
| .worktrees/fix | bugfix/typo | - | No PR | Kept (no PR) |

### Actions Taken
- Worktrees removed: [count]
- Branches deleted: [count]
- Worktrees kept: [count]

### Kept Worktrees (Active Development)
- .worktrees/api (PR #51 still open)
- .worktrees/fix (no associated PR)
```

## Integration with Housekeeping

This skill is designed to run as a parallel agent during housekeeping (Phase 2).

**When called from housekeeping:**

1. Run the full cleanup process
2. Return the summary report
3. Include metrics for the housekeeping report

**Metrics to report:**

- `worktrees_checked`: Total feature worktrees examined
- `worktrees_removed`: Worktrees successfully removed
- `worktrees_kept`: Worktrees retained (with reasons)
- `branches_deleted`: Branches deleted after worktree removal

## Error Handling

### Network Issues

If `gh` commands fail due to network:

```
Warning: Could not check PR status for branch 'feature/xyz' - keeping worktree
```

**Never remove a worktree if PR status cannot be confirmed.**

### Permission Issues

If worktree removal fails:

```
Error: Could not remove worktree at /path - manual cleanup may be needed
```

Continue with other worktrees, report failures at end.

### Missing gh CLI

If `gh` is not installed:

```
Error: GitHub CLI (gh) not found. Cannot verify PR status.
Worktree cleanup requires gh CLI to verify merged PRs.
Skipping all worktree cleanup.
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| PR merged | Remove worktree + delete branch |
| PR open | Keep worktree |
| PR closed (not merged) | Keep worktree (might reopen) |
| No PR exists | Keep worktree |
| Uncommitted changes | Keep worktree |
| Unpushed commits | Keep worktree |
| Network error | Keep worktree |
| gh CLI missing | Skip all cleanup |

## Common Mistakes

**Removing worktrees without checking PR status**

- Problem: Deletes active development work
- Fix: Always verify PR is MERGED before removal

**Using rm -rf instead of git worktree remove**

- Problem: Leaves stale worktree metadata in git
- Fix: Always use `git worktree remove`

**Checking PR state instead of mergedAt**

- Problem: Closed PRs might not be merged
- Fix: Verify `mergedAt` has a value

**Force-removing worktrees with changes**

- Problem: Loses uncommitted work
- Fix: Never force-remove, always check for changes first

## Example Execution

```bash
# List worktrees
$ git worktree list
/Users/sam/project           abc1234 [main]
/Users/sam/project/.worktrees/auth  def5678 [feature/auth]
/Users/sam/project/.worktrees/api   ghi9012 [feature/api]

# Check PR for auth branch
$ gh pr list --head "feature/auth" --state all --json number,state,mergedAt
[{"number":42,"state":"MERGED","mergedAt":"2024-01-15T10:30:00Z"}]

# PR is merged - safe to remove
$ cd /Users/sam/project/.worktrees/auth && git status --porcelain
# (empty - no uncommitted changes)

$ cd /Users/sam/project/.worktrees/auth && git log @{upstream}..HEAD --oneline
# (empty - no unpushed commits)

# Remove the worktree
$ git worktree remove /Users/sam/project/.worktrees/auth
$ git branch -d feature/auth

# Check PR for api branch
$ gh pr list --head "feature/api" --state all --json number,state,mergedAt
[{"number":51,"state":"OPEN","mergedAt":null}]

# PR is open - keep this worktree
# (no action taken)

# Prune stale metadata
$ git worktree prune
```

## Red Flags

**STOP if you see:**

- About to remove worktree without checking PR status
- PR state is "OPEN" or "CLOSED" (not "MERGED")
- Worktree has uncommitted changes in git status
- Network errors when checking PR - default to KEEP
- Using `rm -rf` on a worktree directory

**ALWAYS:**

- Check PR is MERGED (not just closed)
- Verify no uncommitted changes
- Verify no unpushed commits
- Use `git worktree remove`
- Run `git worktree prune` after cleanup
- Report what was kept and why
