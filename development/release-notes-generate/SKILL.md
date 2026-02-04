---
name: release-notes-generate
description: Generate LLM-backed release notes between git tags using the repo release-scripts. Use when asked for changelogs, release notes, or summaries between two tags.
---

# Release Notes Generate

## Overview
Create release notes between git tags using the release-notes CLI and its prompt.

## Workflow
1. Run the CLI from `dev/packages/release-scripts`: `pnpm release:notes --current-tag <tag> --previous-tag <tag> --output <path>`.
2. Review or update the prompt at `dev/packages/release-scripts/scripts/release-notes/prompt.md` when tone or format changes are needed.
3. Confirm the output is based on actual git history and avoid inventing changes.
