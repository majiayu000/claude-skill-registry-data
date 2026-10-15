---
name: speckit-git-validate
description: Validate current branch follows feature branch naming conventions
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: extension:git
user-invocable: true
disable-model-invocation: false
model: haiku
---

# Git Validate Skill

# Validate Feature Branch

Validate that the current Git branch follows the expected feature branch naming conventions.

## Prerequisites

- Check if Git is available by running `git rev-parse --is-inside-work-tree 2>/dev/null`
- If Git is not available, output a warning and skip validation:
  ```
  [specify] Warning: Git repository not detected; skipped branch validation
  ```

## Validation Rules

Get the current branch name:

```bash
git rev-parse --abbrev-ref HEAD
```

A branch is valid if it matches EITHER of the two shapes below. Check the
ticket shape first — in this repo it is the common one.

1. **Ticket key** (project rule, `.claude/skills/speckit-git-feature/SKILL.md`):
   the Jira key verbatim, `[A-Z]+-[0-9]+` (e.g. `BKP-1310`). The branch name
   then says nothing about which feature is active, by design: the specs
   directory keeps its own `NNN-slug` name and `.specify/feature.json` ties the
   two together. Resolve the feature through that file — every gate in
   `.claude/hooks/` does, via `.claude/scripts/lib/feature.mjs`, and
   `.specify/scripts/python/common.py:149` falls back to it too. Deriving the
   feature from the branch name is the single most common way a command in this
   repo looks at the wrong directory.
2. **Generated name** (ticketless work only): the final path segment starts
   with a feature marker — sequential `[0-9]{3,}-` (`001-feature-name`,
   `jdoe/web/008-guided-tour`) or timestamp `[0-9]{8}-[0-9]{6}-`
   (`20260319-143022-feature-name`).

## Execution

On a **ticket-key branch**:
- Output: `✓ On ticket branch: <branch-name>`
- Read `feature_directory` from `.specify/feature.json`. Resolve nothing from
  the branch name.
- If the file is missing: `⚠ No .specify/feature.json — run /speckit-specify to
  create it, or the gates will not know which feature is active`
- If it names a directory that does not exist:
  `✗ .specify/feature.json points at <path>, which is missing`
- Otherwise: `✓ Active feature: <path>`

On a **generated-name branch**:
- Output: `✓ On feature branch: <branch-name>`
- Prefer `.specify/feature.json` when present; fall back to matching
  `specs/<prefix>-*` against the numeric or `YYYYMMDD-HHMMSS` portion,
  regardless of namespace prefixes.
- If spec directory exists: `✓ Spec directory found: <path>`
- If spec directory missing: `⚠ No spec directory found for prefix <prefix>`

If the branch matches NEITHER shape:
- Output: `✗ Not a feature branch. Current branch: <branch-name>`
- Output: `Use the Jira key verbatim (BKP-1310) for ticketed work, or
  001-feature-name / 20260319-143022-feature-name when there is no ticket`

## Graceful Degradation

If Git is not installed or the directory is not a Git repository:
- Check the `SPECIFY_FEATURE` environment variable as a fallback
- If set, validate that value against the naming patterns
- If not set, skip validation with a warning

## Done When

- [ ] Branch shape identified as ticket key or generated name, and reported
- [ ] Active feature resolved through `.specify/feature.json`, never guessed from the branch
- [ ] Read-only — no branch created or switched

