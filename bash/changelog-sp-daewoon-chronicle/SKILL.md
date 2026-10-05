---
name: changelog
description: Keep a changelog humans actually read, and never hand-edit version sections again. Use when adding a change entry or promoting unreleased work into a released version. Follows the Keep a Changelog standard, appends entries chronologically, stays merge-conflict-resistant, and runs with zero dependencies on any repo.
license: MIT
---

# Changelog Workflow

Maintain a [Keep a Changelog](https://keepachangelog.com/) formatted file.

## Add an entry

Pick the correct type — one of: Added, Changed, Deprecated, Removed, Fixed, Security.

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/changelog-parse.mjs" add --type Added --text "Describe the change in one line"
```

This inserts the line under `## [Unreleased] > ### <Type>`, creating the file or subsection if needed.

## Promote a version (at release time)

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/changelog-parse.mjs" release --version 1.2.0 --date 2026-05-31
```

This moves everything under `[Unreleased]` into a new `## [1.2.0] - 2026-05-31` section and leaves a fresh empty `[Unreleased]` on top.

## Rules

- One entry = one user-facing line. Write for humans, not commit hashes.
- Use today's real date for `--date` (never guess).
- Run this *before* tagging a release so the `release` skill can read the new section.
