---
name: Managing Stacked Pull Requests
description: This skill teaches how to manage stacked PRs (pr1 → pr2 → pr3) after the base PR merges. Covers rebasing dependent PRs onto the updated base branch using cherry-pick workflow. Use this when you have a chain of dependent PRs and need to update them after merging earlier PRs in the stack.
allowed-tools: [Bash, Read]
---

# Managing Stacked Pull Requests

When working with PR trains (pr1, pr2 based on pr1, etc.), you need to update the dependent PRs after merging the base PR. This skill shows how to rebase dependent PRs onto the updated base branch.

## What This Skill Does

- Identify commits unique to a dependent PR
- Cherry-pick those commits onto the updated base branch
- Update the remote branch with force-with-lease
- Repeat for entire PR stack
- Handle both `main` and `master` base branches

## Prerequisites

1. **Git CLI** - Already available
2. **Push access** to the repository
3. **Understanding of headless branches** - See Git Workflow in CLAUDE.md

## Core Concept

When you have:
```
pr1 → pr2 → pr3
```

After merging `pr1` to `origin/main`, you need to:
1. Extract the unique commits from `pr2`
2. Apply them onto the updated `origin/main`
3. Force-push to update `pr2`
4. Repeat for `pr3` based on the updated `pr2`

## Basic Workflow: 3-PR Stack

### Scenario

- `pr1` is merged to `origin/master`
- `pr2` and `pr3` are still open
- `pr2` was based on `pr1`
- `pr3` was based on `pr2`

### Step 1: Update pr2

```bash
# Checkout the pr2 branch
git checkout origin/pr2

# Look at git log to identify commits unique to pr2
git log --oneline

# Identify which commits are from pr2 (not from pr1)
# Note the commit hashes

# Checkout the updated base branch
git checkout origin/master

# Cherry-pick the pr2 commits onto master
git cherry-pick <commit-hash1> <commit-hash2> ...

# Push the updated pr2 branch
git push origin HEAD:pr2 --force-with-lease
```

### Step 2: Update pr3

```bash
# Checkout the pr3 branch
git checkout origin/pr3

# Look at git log to identify commits unique to pr3
git log --oneline

# Identify which commits are from pr3 (not from pr2)
# Note the commit hashes

# Checkout the updated pr2 branch
git checkout origin/pr2

# Cherry-pick the pr3 commits onto pr2
git cherry-pick <commit-hash1> <commit-hash2> ...

# Push the updated pr3 branch
git push origin HEAD:pr3 --force-with-lease
```

## Detailed Workflow

### Identifying Unique Commits

When you run `git log --oneline` on a dependent branch, you'll see:
```
abc1234 My pr2 commit 2
def5678 My pr2 commit 1
9ab0cde Commit from pr1 (already merged)
1234567 Another commit from pr1 (already merged)
```

**You want to cherry-pick only the pr2 commits** (`abc1234` and `def5678`).

**Tip**: Look at the PR description or commit messages to identify which commits belong to which PR.

### Using force-with-lease

`--force-with-lease` is safer than `--force` because:
- It only force-pushes if the remote hasn't changed unexpectedly
- Prevents accidentally overwriting someone else's changes
- Still allows you to rewrite history (which we need here)

**Why we need force-push**: After cherry-picking, the branch history has changed (different base), so we must force-push.

## Examples

### Example 1: Simple 2-PR Stack

```bash
# User: "pr1 just merged, please update pr2"

# Current state: pr1 merged to origin/main, pr2 is open

# Checkout pr2
git checkout origin/pr2

# See what commits are unique to pr2
git log --oneline --decorate

# Example output:
# 7a8b9c0 (origin/pr2) Add feature B tests
# 6d7e8f9 Add feature B implementation
# 5c6d7e8 (origin/main) Add feature A (merged)

# The first two commits are pr2-specific
# Checkout updated main
git checkout origin/main

# Cherry-pick pr2 commits
git cherry-pick 6d7e8f9 7a8b9c0

# Update remote pr2
git push origin HEAD:pr2 --force-with-lease
```

### Example 2: 3-PR Stack After First Merge

```bash
# User: "pr1 merged, update pr2 and pr3"

# Update pr2 first
git checkout origin/pr2
git log --oneline  # Identify pr2 commits: aaa1111, bbb2222

git checkout origin/main
git cherry-pick aaa1111 bbb2222
git push origin HEAD:pr2 --force-with-lease

# Now update pr3 based on the NEW pr2
git checkout origin/pr3
git log --oneline  # Identify pr3 commits: ccc3333, ddd4444

git checkout origin/pr2  # Use the UPDATED pr2 as base
git cherry-pick ccc3333 ddd4444
git push origin HEAD:pr3 --force-with-lease
```

### Example 3: Handling main vs master

```bash
# Some repos use 'main', others use 'master'

# Check which one exists
git branch -r | grep -E "origin/(main|master)"

# If main:
git checkout origin/main
git cherry-pick <commits>
git push origin HEAD:pr2 --force-with-lease

# If master:
git checkout origin/master
git cherry-pick <commits>
git push origin HEAD:pr2 --force-with-lease
```

## Verification

### Verify Branch is Up to Date

```bash
# After updating pr2, verify it's based on the latest main
git checkout origin/pr2
git log --oneline

# Should see pr2 commits on top of recent main commits
# Should NOT see pr1 commits separately
```

### Verify PR Shows Correct Changes

After pushing:
1. Open the PR in GitHub
2. Check the "Files changed" tab
3. Should only show changes from that specific PR, not the merged one

### Verify CI Passes

After force-pushing:
1. Watch for CI to re-run
2. Ensure tests pass with the new base
3. May catch integration issues between merged pr1 and pr2

## Troubleshooting

### Issue: Cherry-pick conflicts

**Cause**: The commits from pr2 conflict with changes merged in pr1

**Solution**:
```bash
# During cherry-pick, you'll see conflicts
git status  # Shows conflicting files

# Resolve conflicts manually
vim <conflicting-file>

# Stage resolved files
git add <conflicting-file>

# Continue the cherry-pick
git cherry-pick --continue

# If multiple commits, repeat for each conflict

# Once done, force-push
git push origin HEAD:pr2 --force-with-lease
```

### Issue: Can't identify which commits belong to pr2

**Cause**: Unclear commit messages or mixed work

**Solution**:
```bash
# Option 1: Check the PR diff in GitHub
# Go to the PR and see which commits were included

# Option 2: Use git log with range
git log origin/pr1..origin/pr2

# This shows commits in pr2 that aren't in pr1

# Option 3: Check commit dates/authors
git log --oneline --author="Your Name" --since="2 days ago"
```

### Issue: force-with-lease fails

**Cause**: Someone else pushed to the branch after you checked it out

**Solution**:
```bash
# Fetch latest
git fetch origin pr2

# Check what changed
git log origin/pr2

# If it's just CI updates or minor changes:
# Use --force (carefully!)
git push origin HEAD:pr2 --force

# If it's significant work from someone else:
# Coordinate with them before force-pushing
```

### Issue: PR shows wrong base branch

**Cause**: GitHub UI hasn't updated after force-push

**Solution**:
- Refresh the GitHub page
- GitHub may take a few seconds to recalculate the diff
- Check the "Files changed" tab to verify

### Issue: CI fails after rebase

**Cause**: Integration issue between merged pr1 and pr2

**Solution**:
1. This is actually good - caught an issue early
2. Fix the integration problem in pr2
3. Add a new commit or amend the cherry-picked commits
4. Push again

## Best Practices

1. **Update PRs immediately after merge**
   - Don't let PR stacks get stale
   - Reduces conflicts and integration issues

2. **Work on one PR at a time when possible**
   - Reduces the need for complex rebasing
   - But sometimes dependencies require stacking

3. **Use descriptive commit messages**
   - Makes identifying unique commits easier
   - Include PR number in commit message: "Add feature X (#123)"

4. **Verify CI passes at each step**
   - Don't update pr3 until pr2's CI is green
   - Catches issues early in the stack

5. **Keep the stack shallow**
   - 2-3 PRs deep is manageable
   - More than that becomes error-prone
   - Consider merging more frequently instead

6. **Communicate with reviewers**
   - Let them know you're updating the stack
   - They may need to re-review after rebase

## Alternative Approaches

### Using git rebase instead of cherry-pick

```bash
# Some prefer rebase over cherry-pick
git checkout origin/pr2
git rebase origin/main
git push origin HEAD:pr2 --force-with-lease
```

**When to use rebase vs cherry-pick:**
- **Rebase**: Simpler if you're confident in the branch history
- **Cherry-pick**: More control over which commits to include
- **User preference**: This guide uses cherry-pick (as specified in CLAUDE.md)

### Using GitHub's "Update branch" button

GitHub offers an "Update branch" button on PRs:
- Uses merge commits (not rebase)
- Creates messy history
- Not recommended for clean PR trains

**Stick with the manual cherry-pick workflow for cleaner history.**

## Quick Reference

```bash
# Update pr2 after pr1 merges
git checkout origin/pr2
git log --oneline                    # Identify pr2 commits
git checkout origin/main
git cherry-pick <hash1> <hash2>      # Apply pr2 commits
git push origin HEAD:pr2 --force-with-lease

# Update pr3 after pr2 is updated
git checkout origin/pr3
git log --oneline                    # Identify pr3 commits
git checkout origin/pr2              # Use updated pr2 as base
git cherry-pick <hash1> <hash2>      # Apply pr3 commits
git push origin HEAD:pr3 --force-with-lease
```

## Related Skills

- **Git Workflow** (CLAUDE.md) - Core git principles and headless branches
- **Using GitHub API with gh CLI** - For programmatic PR management
