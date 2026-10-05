---
description: Update CHANGELOG.md [Unreleased] from recent commits or a manual entry
argument-hint: "[entry text]"
disable-model-invocation: true
allowed-tools: "Read, Edit, Bash(git *)"
---

# Changelog

## Context

!`git log $(git describe --tags --abbrev=0 2>/dev/null || echo HEAD~20)..HEAD --oneline`

## Instructions

1. Read `CHANGELOG.md`.
2. If `$ARGUMENTS` is given, add it under the right category in `## [Unreleased]`.
3. Otherwise draft from the commits above into Keep a Changelog buckets:
   - `### Added` - `feat:` commits
   - `### Changed` - `ref:` with API impact, `perf:`
   - `### Fixed` - `fix:` commits
   - `### Removed` - removed features
4. Skip non-user-facing commits (`chore:`, CI, internal refactors).
5. Format: imperative ("Add" not "Added"), code in backticks, under 100 chars, **BREAKING** prefix for API breaks.
6. Present draft, then `Edit`. Never touch released sections.
