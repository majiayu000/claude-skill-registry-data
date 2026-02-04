---
name: difit
description: Git diff viewer with web UI and AI prompt generation. Use when "difit" is mentioned, or when reviewing diffs/PRs with AI-friendly output.
---

# difit

Web-based Git diff viewer with AI prompt generation. https://github.com/yoshiko-pg/difit

## Commands

```bash
# Uncommitted changes
git diff | bunx difit

# Staged changes
git diff --staged | bunx difit

# Specific commit
git show <commit-hash> | bunx difit

# Compare branches
git diff main..feature | bunx difit

# Latest commit
git show HEAD | bunx difit
```

## Usage in Claude Code

Run with `run_in_background: true` to keep the server running:

```bash
git diff | bunx difit  # run_in_background: true
```

## Workflow

1. Pipe git diff to `bunx difit` (background)
2. Browser opens with diff view
3. Click lines to add review comments
4. Copy AI prompt with "Copy Prompt" button
5. Paste prompt to AI for code review feedback
