---
name: commit
description: Create atomic commits from session changes only
allowed-tools: Bash(just, just fmt, git status, git diff*, git add, git commit, git log)
---

# Commit Session Changes

Create atomic commits for **only the changes we made together** in this session.

## Step 1: Format Code

!`just fmt`

## Step 2: Verify Green Build

Run the full check suite **before** doing anything else. This catches broken code
before it gets committed.

!`just`

If this fails, **stop and fix the issues first**. Do not proceed to commit
planning with a failing build. Re-run `just` after fixing until it passes.

## Step 3: Identify Session Changes

Review your tool use history from this conversation. List the files you edited
using Edit or Write tools. These are "our changes."

**Important:** A "session" spans multiple context windows. After compaction, check
the conversation summary for files edited earlier. Don't ignore uncommitted changes
just because they're not in the current tool history.

## Step 4: Cross-Reference with Git

!`git status --short`

!`git diff --stat`

Only consider files that:

- You edited during this session (from step 1)
- Actually have uncommitted changes (from git status)

Ignore any pre-existing uncommitted changes that weren't part of our work.

## Step 5: Propose Atomic Commits

Group related changes into logical commits. For each proposed commit, show:

```
Commit 1: <message>
  - path/to/file1.clj
  - path/to/file2.clj

Commit 2: <message>
  - path/to/other.clj
```

## Step 6: Wait for Approval

Present the plan and ask: "Ready to create these commits?"

**Do not execute git commands until the user approves.**

## Commit Style

- Summary line: imperative mood, capitalised, no trailing period, ~50 chars
- Blank line, then optional body wrapped at 72 chars
- Body explains _why_, not _how_ — only include when it adds value
- No Co-Authored-By trailers

Match style of recent commits:

!`git log --oneline -5`

$ARGUMENTS
