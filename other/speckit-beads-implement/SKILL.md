---
name: speckit-beads-implement
description: Implement dependency-ready Beads tasks with claim and close semantics
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: Sidekick contributors
  source: beads:commands/speckit.beads.implement.md
---

## User Input

```text
$ARGUMENTS
```

Execute the current Spec Kit feature from Beads. Do not require or update `tasks.md`.

1. Resolve the current `FEATURE_DIR` with `.specify/scripts/bash/check-prerequisites.sh --json --require-spec` and derive the feature label `speckit:<feature-directory-name>`.
2. Inspect every file under `FEATURE_DIR/checklists/` without modifying it. If any checklist contains unchecked items, report the counts and ask before proceeding.
3. Run `bd ready --json`. Keep tasks labeled both `speckit` and the current feature label.
4. Select the highest-priority ready task; break ties by `metadata.speckit.display_id`. If the user supplied a Beads ID, verify that task is ready instead.
5. Inspect it with `bd show <id> --json`. Use its stored description, design context, acceptance criteria, notes, and source references. Inspect the parent epic for the stored specification and technical design; verify source artifacts against their hashes when the checkout is available.
6. Atomically claim it with `bd update <id> --claim` before editing.
7. Implement only that task's scope, respecting its acceptance criteria and the technical plan. Run the relevant focused tests and quality gates.
8. On success, close it with `bd close <id> --reason "Implemented and validated"`. On failure or a blocker, leave it open or in-progress, record the blocker or discovered task in Beads, and report it.
9. Show newly ready tasks with `bd ready`. Continue only when the user's arguments request `all`; otherwise stop after one task.

Rules:

- Never mark work complete solely because files changed; acceptance criteria and validation must pass.
- Create discovered follow-up work in Beads and wire its dependencies.
- Do not maintain a parallel Markdown checklist.
- Do not commit or push unless separately authorized.