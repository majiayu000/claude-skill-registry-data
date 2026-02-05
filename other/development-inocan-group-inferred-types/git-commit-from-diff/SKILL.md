---
name: git-commit-from-diff
description: Create git commits by inspecting the current diff and staged changes, then crafting a concise commit message from the diff. Use when the user asks to commit changes, asks for a commit message based on the diff, or wants a commit workflow that stages files and commits in a single pass.
---

# Git Commit From Diff

## Overview

Create a git commit by staging changes (optionally all), inspecting the staged diff, and generating a concise commit message based on what changed.

## Workflow

1. Check status with `git status -sb`.
2. If there are unrelated changes, ask whether to commit everything or only specific paths.
3. Stage changes with `git add -A` for “all changes” or `git add <paths>` for a scoped commit.
4. Inspect the staged diff to craft a message:
   - Preferred: `git diff --cached --stat` for scope summary.
   - If the message is unclear, skim `git diff --cached` for key themes.
5. Propose a concise, imperative commit message based on the diff. Use short subject lines like:
   - `Refine globe layout and sidebar rendering`
   - `Update ingestion flow and cache handling`
6. Commit with `git commit -m "<message>"`.

## Guardrails

- Do not amend unless explicitly requested.
- If there is nothing staged, stop and ask whether to stage changes.
- If the user asks for a message “based on the diff,” always inspect the staged diff before committing.
