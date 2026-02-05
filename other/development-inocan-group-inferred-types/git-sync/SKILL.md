---
name: git-sync
description: Stage all changes, generate a short commit message, commit, and push. Use when asked to sync changes or run git add/commit/push with an auto-generated concise commit message.
---

# Git Sync

## Overview

Sync local changes by staging everything, generating a short commit message from the diff, committing, and pushing.

## Workflow

1. Inspect the repo.
   - Run `git status --short`.
   - Skim `git diff --stat` and `git diff` to understand the main change.
2. If there are no changes, report that the working tree is clean and stop.
3. Generate a concise commit message.
   - Keep it short (roughly <= 50 chars), imperative, no trailing period.
   - Focus on the primary change; add a brief scope only if obvious.
4. Execute the sync.
   - `git add .`
   - `git commit -m "<message>"`
   - `git push`
5. If push fails due to missing upstream, use `git push -u origin <branch>` after confirming the branch name.
