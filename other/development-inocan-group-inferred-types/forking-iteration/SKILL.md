---
name: forking-iteration
description: Use when user wants to create new autonomy branch from current commit or specific past iteration
---

# Forking Iteration

## Overview

Create new autonomy branch forked from current commit or any iteration tag in git history. Enables "slime mold strategy" of parallel exploration.

**Core principle:** Branch creation is independent of iteration management. Fork creates branch, start-iteration begins work.

## When to Use

Use this skill when:
- User runs `/fork-iteration` command
- User wants to create new exploration branch
- User wants to try alternative approach from past iteration
- User wants to bootstrap autonomy workflow from non-autonomy branch

**DO NOT use for:**
- Creating non-autonomy branches (use git directly)
- Starting iterations (use starting-an-iteration instead)

## Quick Reference

| Step | Action | Tool |
|------|--------|------|
| 1. Parse arguments | Extract iteration (optional) and strategy-name | Manual |
| 2. Validate strategy-name | Check kebab-case, not already exists | Bash |
| 3. Resolve fork point | Find iteration tag or use HEAD | Bash |
| 4. Create branch | Checkout fork point, create autonomy branch | Bash |
| 5. Report success | Confirm creation with next steps | Direct output |

## Process

### Step 1: Parse and Validate Arguments

Extract arguments from command args:

**Format:** `[iteration] <strategy-name>`

**Parse:**
```
If args contains only one word:
  iteration = None
  strategy_name = args
Else if args contains two words:
  iteration = first word
  strategy_name = second word
Else:
  Error: "Invalid arguments. Usage: /fork-iteration [iteration] <strategy-name>"
```

**Validate strategy-name:**
- Must be kebab-case (lowercase, hyphens, no special chars)
- Must not be empty
- Should be descriptive (warn if too generic like "test" or "new")

**Normalize strategy-name:**
```bash
# Convert to lowercase, replace invalid chars with hyphens
strategy_name=$(echo "$strategy_name" | tr '[:upper:]' '[:lower:]' | tr -cs '[:alnum:]-' '-' | sed 's/^-*//; s/-*$//')
```

### Step 2: Check if Branch Already Exists

Validate that `autonomy/<strategy-name>` doesn't already exist:

```bash
# Check for existing branch (local or remote)
if git branch -a | grep -q "autonomy/$strategy_name\$"; then
  # Error: branch exists
fi
```

**If exists:**
```markdown
Error: Branch 'autonomy/<strategy-name>' already exists.

To work on existing branch:
  git checkout autonomy/<strategy-name>

To create with different name:
  /fork-iteration [iteration] <different-name>

Available autonomy branches:
[List from git branch -a | grep autonomy/]
```

Stop here if branch exists.

### Step 3: Resolve Fork Point

Determine what commit to fork from:

**If iteration specified:**
```bash
# Search for iteration tag in current branch history
matching_tags=$(git tag --merged HEAD | grep "iteration-$(printf '%04d' $iteration)\$")

tag_count=$(echo "$matching_tags" | wc -l)

if [ "$tag_count" -eq 0 ]; then
  # Error: iteration not found
  echo "Error: Iteration $iteration not found in current branch history."
  echo ""
  echo "Most recent iterations in current branch:"
  git tag --merged HEAD | grep 'iteration-' | tail -5
  exit 1
elif [ "$tag_count" -eq 1 ]; then
  # Use the tag
  fork_point="$matching_tags"
else
  # Multiple matches (shouldn't happen with branch-namespaced tags, but handle it)
  echo "Multiple iteration tags found for iteration $iteration:"
  echo "$matching_tags"
  echo ""
  # Use AskUserQuestion to let user choose
  exit 1
fi
```

**If iteration NOT specified:**
```bash
# Fork from current HEAD
fork_point=$(git rev-parse HEAD)
fork_description="current commit (HEAD)"
```

**Validate fork point exists:**
```bash
if ! git rev-parse "$fork_point" >/dev/null 2>&1; then
  echo "Error: Fork point '$fork_point' not found in git history."
  exit 1
fi
```

### Step 4: Create New Branch

Checkout fork point and create new autonomy branch:

```bash
# Checkout fork point (detached HEAD)
git checkout "$fork_point"

# Create and switch to new branch
git checkout -b "autonomy/$strategy_name"

# Confirm creation
current_branch=$(git branch --show-current)
if [ "$current_branch" != "autonomy/$strategy_name" ]; then
  echo "Error: Failed to create branch 'autonomy/$strategy_name'"
  exit 1
fi
```

**On success:**
- Branch created and checked out
- Working directory contains files from fork point
- Ready for `/start-iteration`

### Step 5: Report Success

Announce successful branch creation:

```markdown
✓ Branch `autonomy/<strategy-name>` created

Forked from: [tag or commit hash]
Current branch: autonomy/<strategy-name>

Next step: Run `/start-iteration` to begin work on this branch.
```

## Important Notes

### Branch Creation Only

**This skill ONLY creates branches:**
- Does NOT start iterations
- Does NOT modify journal files
- Does NOT determine iteration numbering
- `start-iteration` will handle iteration logic when user runs it

### Works from Any Starting Point

Can fork from:
- Autonomy branches (e.g., `autonomy/experiment-a`)
- Non-autonomy branches (e.g., `main`, `develop`)
- Detached HEAD
- Any commit with autonomy iteration tags

### No Merge Provisions

**Autonomy branches NEVER merge:**
- Each branch is independent exploration
- Branches learn from each other via `/analyze-branch` (read-only)
- No git merge operations
- No rebase operations
- Branches are peers, not hierarchical

### Strategy Name Matters

Branch name becomes identity:
- Used in tag names: `autonomy/<strategy-name>/iteration-NNNN`
- Appears in branch listings
- Should describe exploration direction
- Can't easily change later (would require tag renaming)

**Good names:**
- `usage-based-pricing`
- `cdn-optimization`
- `react-migration`

**Bad names:**
- `test` (too generic)
- `new` (not descriptive)
- `experiment1` (meaningless)

### Iteration Numbering Continuity

When `start-iteration` runs on new branch:
- If forked from iteration tag: continues numbering (fork from 0015 → next is 0016)
- If forked from non-iteration commit: starts at 0001 (if goal exists)
- If no goal exists: user must run `/create-goal` first

## Common Mistakes

| Mistake | Reality |
|---------|---------|
| "I'll also start the iteration in this skill" | NO. Branch creation is separate. User runs /start-iteration when ready. |
| "User wants to fork, I'll check out the branch for them" | Already doing this. Checkout happens during creation. |
| "Branch name has spaces, I'll keep them" | NO. Normalize to kebab-case. |
| "I'll search all branches for iteration tag" | NO. Only search tags reachable from current HEAD (git tag --merged HEAD). |
| "Branch exists, I'll overwrite it" | NO. Error and show user how to work with existing branch. |
| "No goal found, I'll create one" | NO. User must run /create-goal explicitly. |

## After Forking

Once branch is created:
- User is on new `autonomy/<strategy-name>` branch
- Working directory contains files from fork point
- No iterations started yet
- User runs `/start-iteration` to begin work
- Iteration numbering determined by start-iteration skill
