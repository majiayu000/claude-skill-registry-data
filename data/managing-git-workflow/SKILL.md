---
name: managing-git-workflow
description: Automates git commits, push, and PR creation with context-aware messages and ticket extraction. Use when performing git operations, creating commits/PRs, or when user mentions git, GitHub, commit, push, or pull request.
---

# Managing Git Workflow

## Overview

Automates git workflows for commit, push, and PR creation with context-aware message generation and automatic ticket number extraction.

## When to Use

- Creating commits with auto-generated messages in project's language
- Pushing changes (with automatic commit if needed)
- Creating PRs (with automatic push and commit if needed)
- When user mentions: git, commit, push, pull request, PR, GitHub

## Workflow Selection

| Task | Reference Document | Auto-includes |
|------|-------------------|---------------|
| Commit only | `managing-git-workflow/reference/commit.md` | - |
| Push to remote | `managing-git-workflow/reference/push.md` | Commit (if uncommitted changes) |
| Create PR | `managing-git-workflow/reference/pr.md` | Push + Commit (if needed) |

## Common Principles

**Commit Messages:**
- Use language specified in project context, prompts, or documentation (default to English if unspecified)
- Follow existing project patterns (analyze with `git log --online -10`)
- Include ticket numbers (FMT-XXXXX, FLEASVR-XXX, etc.) if found in branch name or changes

**Branch Naming:**
- Extract ticket numbers from branch names for PR titles
- Use descriptive, concrete names

**Helper Scripts:**
- Common git operations available in `git-helpers.sh`
- Use `source` to load helpers when needed

## Quick Reference

```bash
# Load helper functions
source $SKILL_DIR/git-helpers.sh

# Check status
has_uncommitted_changes  # returns 0 if true
has_unpushed_commits     # returns 0 if true
get_current_branch       # echoes branch name
check_pr_exists          # returns 0 if PR exists
```

## Implementation

**For commit workflow:** See `managing-git-workflow/reference/commit.md`

**For push workflow:** See `managing-git-workflow/reference/push.md`

**For PR workflow:** See `managing-git-workflow/reference/pr.md`

Each reference document provides step-by-step instructions for that specific operation.
