---
name: cursor-git-commit
description: Provide a pre-commit checklist and staging hygiene (review diffs, stage specific files, avoid common noise like dist/ or .env, and fix mistakes with reset/rm --cached/amend). Use when the user is about to commit, asks for a commit workflow, or needs help cleaning up staged files.
---

# Cursor Git Commit

## Overview

Use a consistent commit workflow: inspect changes, stage intentionally, and avoid committing noise.

## Checklist (run before committing)

1. Inspect status: `git status --porcelain`
2. Review diffs:
   - unstaged: `git diff --stat`
   - staged: `git diff --cached --stat`
3. Stage intentionally: `git add path/to/file ...`
4. Verify staged set: `git diff --cached --name-only`
5. Commit and record hash:
   - `git commit -m "..."` then `git rev-parse HEAD`

## Fix common mistakes
- Unstage one file: `git reset HEAD path/to/file`
- Unstage everything: `git reset HEAD`
- Remove noise already committed (keep on disk): `git rm --cached path/to/noise` then add to `.gitignore` and `git commit --amend --no-edit`

## Reference
- Full checklist + ignore guidance: `references/git-commit-instructions.md`.
