---
description: Cut a versioned release via ./release.sh (changelog cut + tag + GitHub release)
argument-hint: "<X.Y.Z> [--dry-run]"
disable-model-invocation: true
allowed-tools: "Read, Bash(git *), Bash(gh *), Bash(./release.sh *)"
---

# Release

## Context

!`git branch --show-current`
!`git status --porcelain`

## Instructions

1. Abort if not on `main` or working tree is dirty.
2. Confirm `## [Unreleased]` has content: `git diff $(git describe --tags --abbrev=0)..HEAD -- CHANGELOG.md`. Warn if empty.
3. Validate `$ARGUMENTS` is `X.Y.Z` (no `v` - the script adds it). Ask if missing.
4. Run:
   ```bash
   ./release.sh <version>          # or with --dry-run first
   ```
   The script handles changelog cut, commit, tag `vX.Y.Z`, push, and GitHub release.
5. Verify: `gh release view v<version>`. Report the URL.
