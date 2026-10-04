---
name: commit-all
description: Create atomic commits from all unstaged changes
allowed-tools: Bash(just, just fmt, git status, git diff*, git add, git commit, git log)
---

# Commit All Unstaged Changes

Create atomic commits from all unstaged changes.

## Step 1: Format Code

!`just fmt`

## Step 2: Verify Green Build

Run the full check suite **before** doing anything else. This catches broken code
before it gets committed.

!`just`

If this fails, **stop and fix the issues first**. Do not proceed to commit
planning with a failing build. Re-run `just` after fixing until it passes.

## Current State

!`git status --short`

!`git diff --stat`

## Process

1. Group related changes into logical commits
2. For each group, propose:

```
Commit 1: <message>
  - path/to/file.clj (brief description of change)

Commit 2: <message>
  - path/to/other.clj
```

3. Ask "Ready to create these commits?" and wait for approval
4. After approval, for each commit:
   - `git add <files>`
   - `git commit -m "<message>"`

## Commit Style

- Summary line: imperative mood, capitalised, no trailing period, ~50 chars
- Blank line, then optional body wrapped at 72 chars
- Body explains _why_, not _how_ — only include when it adds value
- No Co-Authored-By trailers

Match recent style:

!`git log --oneline -5`

$ARGUMENTS
