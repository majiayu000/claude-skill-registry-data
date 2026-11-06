---
name: speckit-beads-ready
description: Select ready Beads work and restore its linked Spec Kit context
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: Sidekick contributors
  source: beads:commands/speckit.beads.ready.md
---

## User Input

```text
$ARGUMENTS
```

Choose ready implementation work from Beads while preserving the Spec Kit design context. Beads—not `tasks.md`—is authoritative.

1. Verify the repository contains `.specify/` and `.beads/`.
2. Resolve the current feature and run `bd ready --json`. Keep tasks labeled both `speckit` and `speckit:<feature-directory-name>`. If the user supplied a Beads ID, inspect that issue instead.
3. If no matching task is ready, show the relevant blocking dependency tree and stop.
4. Select the highest-priority ready task. When priorities tie, prefer the lowest `metadata.speckit.display_id`. If the choice is genuinely ambiguous, show the small candidate set and ask the user.
5. Run `bd show <id> --json`. Its description, design, acceptance criteria, notes, and `metadata.speckit.source_refs` contain the stored implementation context. Inspect the parent epic for the stored specification, design snapshot, success criteria, artifact hashes, and planned DAG.
6. Use the stored Beads context first. When the source checkout is available, verify cited files against the epic's artifact hashes and load only directly relevant sections. Do not read unrelated feature directories.
7. If the user included `claim`, atomically claim it with `bd update <id> --claim`. Otherwise leave issue state unchanged.
8. Return a compact implementation brief: Beads ID, display ID, task text, phase/story, dependencies, acceptance criteria, relevant sources, and whether it was claimed.

Beads is authoritative for task identity, dependencies, and execution state. Spec Kit files remain authoritative for product intent and implementation design.