---
name: sync-index
description: Keep project documentation (.agentss/project-index.md and sub-skills) in sync with codebase changes.
---

# Documentation Sync

## Overview

Documentation drift is a major problem. Use this skill to ensure that the project index and agent guidance files are always up-to-date with the codebase.

## Workflow

1.  **Detect Changes**:
    *   Ideally run after major feature implementation or refactoring.
    *   Compare current file structure with `project-index.md`.

2.  **Run Indexer**:
    *   Execute the `project-index` skill again.
    *   Verify that new modules/directories are captured.
    *   Ensure deleted files are removed from documentation.

3.  **Update Guidance**:
    *   Check `agent-*.md` files in domain directories.
    *   Update any obsolete instructions.
    *   Add new patterns discovered during implementation.

4.  **Verify Links**:
    *   Ensure all links in `README.md` and `AGENTS.md` point to valid locations.

## Output

*   Updated `project-index.md`.
*   Updated domain-specific agent guides.
*   Confirmation of documentation sync.
