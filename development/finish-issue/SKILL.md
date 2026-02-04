---
schema_version: "1.0.0"
name: finish-issue
title: Finish Issue Workflow
version: "1.0.0"
status: stable
objective: Prepare a GitHub issue branch for PR with quality checks, cleanup, and review recommendations
description: Prepare a GitHub issue branch for PR with quality checks, cleanup, and review recommendations.
  Use when user says "finish issue", "ready for PR", "prepare for review", "submit PR",
  "create PR", "finalize issue", or "wrap up".
authors:
  - name: Dossier Community
checksum:
  algorithm: sha256
  hash: 7f81210beb8488fe5b8c2f3002a48c23331d4cbf726824154d0515b7d25a2d44
---

# Finish Issue Workflow

When the user wants to finalize their work on a GitHub issue and prepare a PR:

## Prerequisites

- dossier-tools installed (`pip install dossier-tools`)
- On a feature/bug branch (not main/master)
- GitHub CLI (`gh`) authenticated

## Steps

1. Verify we're on a feature/bug branch (not main/master)
2. Run the finish workflow:
   ```bash
   dossier run imboard-ai/development/git/finish-issue-workflow
   ```
3. Respond to prompts for each check category
4. Confirm successful PR creation with the user

## What This Does

- **Git prep**: Fetch latest, rebase onto main, check for conflicts
- **Security scans**: Detect secrets, hardcoded paths, files that should be gitignored
- **Code cleanup**: Find debug statements, commented code, unresolved TODOs
- **Project checks**: Run linter, formatter, type checker, tests
- **Review recommendations**: Suggest reviewers based on changed files (security, DB, ops, etc.)
- **PR creation**: Generate description from PLANNING.md + commits, link to issue, push and create PR
