---
name: finish-branch
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup
allowed-tools: Bash(git:*), Bash(gh:*), AskUserQuestion
---

# Finishing a Development Branch

## Overview

Guide completion of development work by presenting clear options and handling chosen workflow.

**Core principle:** Verify tests → Present options → Execute choice → Clean up.

**Announce at start:** "I'm using the finish-branch skill to complete this work."

## The Process

### Step 1: Verify Tests

**Before presenting options, verify tests pass:**

```bash
# Run project's test suite
npm test / cargo test / pytest / go test ./...
```

**If tests fail:**

```
Tests failing (<N> failures). Must fix before completing:

[Show failures]

Cannot proceed with merge/PR until tests pass.
```

Stop. Don't proceed to Step 2.

**If tests pass:** Continue to Step 2.

### Step 2: Determine Base Branch

```bash
# Try common base branches
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or ask: "This branch split from main - is that correct?"

### Step 3: Present Options

Present exactly these 4 options:

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**Don't add explanation** - keep options concise.

### Step 4: Execute Choice

#### Option 1: Merge Locally

```bash
# Switch to base branch
git checkout <base-branch>

# Pull latest
git pull

# Merge feature branch
git merge <feature-branch>

# Verify tests on merged result
<test command>
```

Then: Cleanup worktree and branch (Step 5)

#### Option 2: Push and Create PR

```bash
# Push branch
git push -u origin <feature-branch>

# Create PR
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```

Then: Cleanup worktree (Step 5)

#### Option 3: Keep As-Is

Report: "Keeping branch <name>. Worktree preserved at <path>."

**Don't cleanup worktree.**

#### Option 4: Discard

**Confirm first:**

```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for exact confirmation.

If confirmed:

```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

Then: Cleanup worktree (Step 5)

### Step 5: Cleanup Worktree

**For Options 1, 2, 4:**

**CRITICAL: Follow this exact sequence to avoid errors.**

#### 5a. Detect if in worktree

```bash
# Check if current directory is inside a worktree
worktree_path=$(git rev-parse --show-toplevel)
main_repo=$(git rev-parse --path-format=absolute --git-common-dir | sed 's|/\.git$||')

# If worktree_path != main_repo, we're in a worktree
```

#### 5b. Leave worktree FIRST (mandatory)

**Cannot remove a worktree while standing in it (causes "Permission denied").**

```bash
# Change to main repository BEFORE attempting removal
cd "$main_repo"
```

#### 5c. Remove worktree

```bash
# Now safe to remove worktree
git worktree remove "$worktree_path"
```

**If worktree removal fails with "not a working tree":**

```bash
# Directory may have been manually deleted - prune stale entries
git worktree prune
```

#### 5d. Delete branch (after worktree is gone)

**Cannot delete a branch while it's checked out in any worktree.**

```bash
# For merged branches (Options 1, 2)
git branch -d <feature-branch>

# For discarded branches (Option 4)
git branch -D <feature-branch>
```

**If branch deletion fails with "used by worktree":**

```bash
# Worktree removal may not have completed - verify state
git worktree list

# If worktree still listed, force prune then retry
git worktree prune
git branch -d <feature-branch>
```

### Complete Cleanup Script

For reference, the full safe cleanup sequence:

```bash
# 1. Capture paths while still in worktree
worktree_path=$(git rev-parse --show-toplevel)
main_repo=$(git rev-parse --path-format=absolute --git-common-dir | sed 's|/\.git$||')
branch_name=$(git branch --show-current)

# 2. Leave worktree (CRITICAL - must do before removal)
cd "$main_repo"

# 3. Remove worktree
git worktree remove "$worktree_path" || git worktree prune

# 4. Delete branch (only after worktree gone)
git branch -d "$branch_name"  # or -D for force delete
```

**For Option 3:** Keep worktree - skip this entire step.

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | ✓ | - | - | ✓ |
| 2. Create PR | - | ✓ | ✓ | - |
| 3. Keep as-is | - | - | ✓ | - |
| 4. Discard | - | - | - | ✓ (force) |

## Common Mistakes

**Skipping test verification**

- **Problem:** Merge broken code, create failing PR
- **Fix:** Always verify tests before offering options

**Open-ended questions**

- **Problem:** "What should I do next?" → ambiguous
- **Fix:** Present exactly 4 structured options

**Automatic worktree cleanup**

- **Problem:** Remove worktree when might need it (Option 2, 3)
- **Fix:** Only cleanup for Options 1 and 4

**No confirmation for discard**

- **Problem:** Accidentally delete work
- **Fix:** Require typed "discard" confirmation

**Wrong cleanup sequence (deleting branch before worktree)**

- **Problem:** `git branch -d` fails with "used by worktree"
- **Fix:** Always remove worktree FIRST, then delete branch

**Removing worktree while standing in it**

- **Problem:** `git worktree remove` fails with "Permission denied"
- **Fix:** `cd` to main repository BEFORE removing worktree

**Inconsistent worktree state after partial failures**

- **Problem:** "not a working tree" errors after failed removal attempts
- **Fix:** Run `git worktree prune` to clean up stale entries

## Red Flags

**Never:**

- Proceed with failing tests
- Merge without verifying tests on result
- Delete work without confirmation
- Force-push without explicit request
- Delete branch while worktree exists (wrong order)
- Remove worktree while cwd is inside it

**Always:**

- Verify tests before offering options
- Present exactly 4 options
- Get typed confirmation for Option 4
- Clean up worktree for Options 1 & 4 only
- Leave worktree directory before removing it
- Follow cleanup sequence: cd out → remove worktree → delete branch

## Integration

**Called by:**

- **subagent-dev** (Step 7) - After all tasks complete
- **executing-plans** (Step 5) - After all batches complete

**Pairs with:**

- **workflow:git-worktrees** - Cleans up worktree created by that skill
