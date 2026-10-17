---
name: create-branch
description: Use when creating a branch, starting work on an issue, or checking out a new feature branch. Validates branch naming and links to GitHub issues automatically.
license: MIT
allowed-tools: Read Bash(git:*) Bash(gh:*) Bash(glab:*)
model: haiku
effort: low
compatibility: Requires git; issue-linking uses a GitHub (gh) or GitLab (glab) remote
metadata:
  short-description: Validated branch names linked to issues.
---

You create and checkout git branches with validation.

## Rules Overview

| Rule | Impact | File |
|------|--------|------|
| Branch naming | HIGH | `rules/branch-naming.md` |
| Prefix detection | MEDIUM | `rules/prefix-detection.md` |

## Workflow

1. If an issue number is provided, detect the remote host from `git remote get-url origin` (github.com → gh, gitlab.com → glab; default GitHub). On **GitHub**, use `gh issue develop <number> -c` to create a linked branch and skip to step 4. On **GitLab** (no direct equivalent), include the issue number in the branch name (e.g. `feature/123-description`) so the MR auto-links, then continue through steps 2–4
2. Auto-detect prefix from user input (see `rules/prefix-detection.md`), validate name (see `rules/branch-naming.md`), and check for duplicates locally and remotely
3. Create and checkout from `main` → `master` → current HEAD: `git checkout -b <name> <base>`. **Exception**: when the current branch has an open unmerged PR and the new work builds on it (the user says "on top of this" / "next part", or the change depends on unmerged work), base on the current branch instead — the diff stays scoped to the new layer, and on GitHub the resulting PRs link into a stack automatically
4. Offer remote push: `git push -u origin <name>`
