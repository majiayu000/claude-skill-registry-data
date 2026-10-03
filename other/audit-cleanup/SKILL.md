---
name: audit-cleanup
description: Execute approved audit cleanup through tracker tasks, Markdown cleanup plans, JSON phase guards, validation gates, and final publish approval. Use when the operator asks to fix audit findings, clean tracker conflicts, resolve validation failures, or prepare cleaned workflow state for GitHub.
---

# Audit Cleanup

Use this skill to execute approved audit cleanup. Cleanup is mutation-capable,
but only through a selected tracker task, a linked Markdown cleanup plan or
review artifact, JSON phase guards, and validation gates.

## Skill-First Runtime Rule

Follow root `AGENTS.md`: lead with `$audit-cleanup` as the operator surface.
Helper commands are internal support for state inspection, validation, and Git
checkpoint verification.

## Invocation

Supported forms:

```text
$audit-cleanup task:<task-id> plan:<path>
$audit-cleanup project:<slug> task:<task-id> plan:<path>
$audit-cleanup from-review:<path> task:<task-id>
```

Require a selected task and a Markdown cleanup plan or review artifact before
mutation. If either is missing, stop and route the operator to `$audit-review`,
`$continue-task`, or `$initiate-task target:tracker`.

## Required Reading

Always start from the repo root and read:

1. Root `AGENTS.md`.
2. `references/matt-pocock-skills.md`.
3. `registry/agents-md.json`.
4. The selected project's `AGENTS.md`.
5. The selected project's `project.json`.
6. The selected project's `tasks/index.json`.
7. Every non-done task JSON in the selected project.
8. The selected task JSON.
9. The Markdown cleanup plan or review artifact.
10. `.agents/skills/audit-review/SKILL.md`.
11. `scripts/query-workflow-state.mjs`.
12. `scripts/validate-workflow-state.mjs`.

Use project query helpers and validation as internal support.

## Approval Model

Cleanup requires both:

1. A Markdown cleanup plan or review artifact that explains the rationale.
2. JSON phase guards on the selected task that enforce the exact paths and
   actions approved for cleanup.

The JSON task state is the enforcement source of truth. The Markdown plan is
the human-readable rationale.

## Phase Guard Updates

If the selected task does not already approve the needed cleanup paths:

1. Present the missing phase-guard entries.
2. Ask for explicit chat approval that names the selected task and Markdown
   cleanup plan.
3. After approval, update only the selected task's phase guard and linked
   artifacts.
4. Run validation before applying cleanup edits.

Do not update phase guards from report text alone.

## Cleanup Categories

Support these v1 cleanup categories:

- tracker state cleanup: task status, task phase, linked artifacts, and preload
  snapshot repairs
- workflow artifact cleanup: PRD, issue, review, and handoff artifact repairs
  linked to the selected task
- validation cleanup: edits required for workflow-state validation and tracker
  verification to pass
- Git checkpoint cleanup: local diff inspection, local commit preparation, and
  final publish/push handoff

Keep broad source-code refactors and broad file deletion out of v1 unless the
approved Markdown cleanup plan explicitly names them.

## Cleanup Process

1. Load all required state.
2. Confirm the selected task is the correct owner for cleanup.
3. Confirm the Markdown cleanup plan is linked or linkable to the selected task.
4. Confirm phase guards approve every implementation artifact that will change.
5. If phase guards need updates, use the phase-guard update process first.
6. Apply the smallest cleanup slice.
7. Run the narrowest useful validation.
8. Repeat until the approved cleanup plan is complete.
9. Run final validation and tracker verification.
10. Inspect the diff for secrets or unrelated changes.
11. Create a local commit when the cleanup unit is coherent and approved.
12. Stop for the operator's final publish or push instruction unless the
    current operator turn has already supplied that explicit instruction.

## GitHub Boundary

The normal desired end state is a GitHub-ready cleanup checkpoint. However,
pushing is an external write. Ask for a final publish or push instruction at
the end of cleanup unless the current user instruction explicitly includes
push approval.

## Final Response

When cleanup completes, respond with:

```text
CLEANUP
- selected task
- cleanup plan
- categories completed

VALIDATION
- commands run

GIT
- commit created, or not created with reason
- push status, or final instruction needed

REMAINING RISKS
- any deferred cleanup
```
