---
name: worktree-isolation
description: Use when implementing features in git worktrees to ensure all changes stay in the correct worktree - prevents "bleeding" of changes back to main branch
---

# Worktree Isolation

## Skill Usage Announcement

**MANDATORY**: When using this skill, announce it at the start with:

```
Using Skill: worktree-isolation | [brief purpose based on context]
```

## Overview

Git worktrees provide isolated workspaces, but Claude Code has characteristics that can cause changes to "bleed" to the wrong worktree:

1. **cwd resets between Bash calls** - Each Bash tool invocation starts in the original working directory
2. **Subagents don't inherit verified context** - They start with zero knowledge of parent's location
3. **No automatic verification** - Nothing enforces you're in the right place before git operations

This skill provides protocols to ensure ALL changes stay in the intended worktree.

## The Problem

### Why Changes Bleed

```bash
# WRONG - This DOES NOT work in Claude Code
cd /path/to/worktree
git status  # This runs in ORIGINAL directory, not worktree!
```

Each Bash tool call is independent. The `cd` command affects only that shell session, which ends immediately. The next Bash call starts fresh in the original working directory.

### Subagent Context Loss

When you spawn a subagent with:
```
Work from: /path/to/worktree
```

This is just text. The subagent has no verified context about which directory it should use. If it runs `git commit`, it commits wherever Claude Code's process is running - likely your main branch.

## The Solution: Verification Protocol

### Rule 1: Always Chain Commands

**WRONG:**
```bash
cd /path/to/worktree
git add .
git commit -m "message"
```

**RIGHT:**
```bash
cd /path/to/worktree && git add . && git commit -m "message"
```

Or use git's `-C` flag:
```bash
git -C /path/to/worktree add .
git -C /path/to/worktree commit -m "message"
```

### Rule 2: Verify Before Every Git Operation

Before ANY git write operation (add, commit, push, merge, etc.), run verification:

```bash
cd /path/to/worktree && \
  echo "=== WORKTREE VERIFICATION ===" && \
  echo "Current directory: $(pwd)" && \
  echo "Git root: $(git rev-parse --show-toplevel)" && \
  echo "Branch: $(git branch --show-current)" && \
  echo "Expected: /path/to/worktree on branch-name" && \
  echo "============================"
```

**STOP if verification fails.** Do not proceed with git operations.

### Rule 3: Use Absolute Paths Everywhere

Never use relative paths in worktree contexts:

**WRONG:**
```bash
git add src/file.ts
```

**RIGHT:**
```bash
git -C /absolute/path/to/worktree add src/file.ts
```

### Rule 4: Subagent Prompts MUST Include Verification

When dispatching subagents for worktree work, include this verification block:

```markdown
## CRITICAL: Working Directory Verification

You are working in worktree: /absolute/path/to/worktree
Expected branch: feature-branch-name

**BEFORE making ANY changes, run this verification:**

```bash
cd /absolute/path/to/worktree && \
  echo "VERIFICATION:" && \
  echo "Directory: $(pwd)" && \
  echo "Git root: $(git rev-parse --show-toplevel)" && \
  echo "Branch: $(git branch --show-current)"
```

**Expected output:**
- Directory: /absolute/path/to/worktree
- Git root: /absolute/path/to/worktree
- Branch: feature-branch-name

**If ANY value doesn't match, STOP immediately and report the mismatch.**

**For ALL git commands, use this pattern:**
```bash
cd /absolute/path/to/worktree && git [command]
```
```

## Implementation Pattern

### Setting Up a Worktree for Implementation

```bash
# 1. Create the worktree
WORKTREE_PATH="$(pwd)/.worktrees/feature-name"
BRANCH_NAME="feature/feature-name"

git worktree add "$WORKTREE_PATH" -b "$BRANCH_NAME"

# 2. Verify creation
git worktree list | grep "$WORKTREE_PATH"

# 3. Install dependencies (chained!)
cd "$WORKTREE_PATH" && npm install && npm test

# 4. Store the absolute path for subagents
echo "Worktree ready at: $WORKTREE_PATH"
```

### Dispatching Subagents for Worktree Work

When using the Task tool for work in a worktree:

```markdown
Tool: Task
Description: "Implement feature X in worktree"
Prompt: |
  You are implementing [task] in an isolated git worktree.

  ## CRITICAL: Working Directory Context

  **Worktree location:** /Users/sam/project/.worktrees/feature-name
  **Branch:** feature/feature-name
  **Main repo:** /Users/sam/project (DO NOT modify)

  ### Verification (RUN FIRST)

  Before ANY work, verify your location:

  ```bash
  cd /Users/sam/project/.worktrees/feature-name && \
    echo "Directory: $(pwd)" && \
    echo "Git root: $(git rev-parse --show-toplevel)" && \
    echo "Branch: $(git branch --show-current)"
  ```

  Expected:
  - Directory: /Users/sam/project/.worktrees/feature-name
  - Git root: /Users/sam/project/.worktrees/feature-name
  - Branch: feature/feature-name

  **If verification fails, STOP and report. Do not proceed.**

  ### Command Pattern

  ALL commands must use this pattern:

  ```bash
  cd /Users/sam/project/.worktrees/feature-name && [your command]
  ```

  Examples:
  - Run tests: `cd /Users/sam/project/.worktrees/feature-name && npm test`
  - Git status: `cd /Users/sam/project/.worktrees/feature-name && git status`
  - Commit: `cd /Users/sam/project/.worktrees/feature-name && git add . && git commit -m "message"`

  ### Your Task

  [Task description here]

  ### Report Back

  Include in your report:
  1. Verification output (proving you worked in correct worktree)
  2. Final git status from worktree
  3. Commit hash of your changes
```

### Verifying Subagent Work

After a subagent completes, verify their work landed in the right place:

```bash
# Check the worktree has the commits
cd /path/to/worktree && git log --oneline -5

# Verify main branch was NOT modified
cd /path/to/main/repo && git log --oneline -5
# Should NOT contain subagent's commits
```

## Common Mistakes

### Mistake 1: Trusting Inherited Context

**Problem:** Assuming subagent is in the right directory
**Solution:** Always include explicit verification in subagent prompts

### Mistake 2: Separate Bash Calls

**Problem:**
```bash
cd /worktree
git status  # WRONG - runs in original directory
```

**Solution:**
```bash
cd /worktree && git status  # RIGHT - chained
```

### Mistake 3: Relative Paths

**Problem:**
```bash
git add src/file.ts  # Where does this run?
```

**Solution:**
```bash
git -C /absolute/worktree/path add src/file.ts
```

### Mistake 4: Missing Verification in Subagent Prompts

**Problem:** `Work from: /path/to/worktree` is just documentation

**Solution:** Include verification commands and expected output in prompt

## Integration with implement Skill

When using the `implement` skill with worktrees:

### Setup Phase Addition

Before dispatching any implementation subagents:

```bash
# Store worktree path as absolute
WORKTREE_PATH="$(cd /path/to/worktree && pwd)"
echo "Using worktree: $WORKTREE_PATH"

# Verify it's actually a worktree
git -C "$WORKTREE_PATH" rev-parse --is-inside-work-tree
git -C "$WORKTREE_PATH" worktree list | grep "$WORKTREE_PATH"
```

### Subagent Prompt Template

Replace the generic `Work from: [current directory]` with:

```markdown
## Working Directory (CRITICAL)

**Worktree:** [ABSOLUTE_WORKTREE_PATH]
**Branch:** [BRANCH_NAME]

### Mandatory Verification (run before any work)

```bash
cd [ABSOLUTE_WORKTREE_PATH] && \
  echo "Location: $(pwd)" && \
  echo "Branch: $(git branch --show-current)" && \
  test "$(pwd)" = "[ABSOLUTE_WORKTREE_PATH]" && \
  echo "VERIFIED" || echo "VERIFICATION FAILED - STOP"
```

### Command Pattern

All commands MUST follow this pattern:
```bash
cd [ABSOLUTE_WORKTREE_PATH] && [command]
```

DO NOT run any git commands without the `cd && ` prefix.
```

### Completion Verification

After all subagents complete, verify isolation was maintained:

```bash
# 1. Check worktree has expected commits
echo "=== Worktree commits ===" && \
cd /path/to/worktree && git log --oneline -10

# 2. Check main branch was NOT modified
echo "=== Main branch commits (should be unchanged) ===" && \
cd /path/to/main && git log --oneline -5

# 3. Verify no uncommitted changes in main
cd /path/to/main && git status --short
```

## Quick Reference

| Scenario | Pattern |
|----------|---------|
| Single git command | `git -C /worktree/path [command]` |
| Multiple commands | `cd /worktree/path && cmd1 && cmd2` |
| Subagent dispatch | Include verification block + expected output |
| After subagent returns | Verify commits in worktree, not main |
| Any uncertainty | Run verification before proceeding |

## Red Flags

**STOP if you see:**

- Subagent prompt says "Work from:" without verification commands
- Git commands without `-C` flag or `cd &&` prefix
- Verification shows wrong directory or branch
- Commits appearing in main branch unexpectedly
- Subagent didn't include verification output in report

**ALWAYS:**

- Use absolute paths
- Chain commands with `&&`
- Include verification in subagent prompts
- Verify subagent work landed in correct worktree
- Check main branch wasn't modified
