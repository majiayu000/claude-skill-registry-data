---
name: termination-gatekeeper
description: Prevent premature completion claims. Use when a task needs Definition of Done evidence, three-layer validation, scripts/termination-check, or proof that static, runtime, e2e, docs, and clean-state checks passed.
---

# Termination Gatekeeper

## Purpose

Externalize completion judgment so work is called done only after required evidence exists.

## Inspect First

- task spec, feature list, OpenSpec tasks, changed files, validation scripts, tests, runtime docs, release checklist, and current command output

## Procedure

1. Define done for the task.
   - Create or update `docs/development/definition-of-done.md`.
   - Create or update task-specific `docs/development/termination-evidence.md` when useful.
   - Include static, runtime, e2e or integration, docs, and clean-state evidence as applicable.

2. Classify changed surface.
   - UI/browser changes usually require accessible e2e or browser workflow evidence.
   - API/runtime/data changes usually require runtime and integration evidence.
   - Docs-only changes can use docs/link/placeholder checks.
   - Risky changes should include pre-edit investigation evidence from `$pre-edit-investigation-gate`.
   - Browser-facing lifecycle changes should include click-path evidence from `$click-path-and-browser-qa`.

3. Add advisory validation.
   - Create or recommend `scripts/termination-check`.
   - Use `scripts/check_termination_evidence.py` from this plugin.
   - Do not force heavy e2e on repos where the changed surface does not need it.

4. Block premature completion in instructions.
   - Completion is not "code looks done."
   - Completion requires evidence from commands, runtime checks, or documented blockers.

5. Route evidence.
   - Update `feature-state-machine` evidence for passing features.
   - Include evidence in PR output via `task-planning-and-pr-protocol`.
   - Add final validation or blocked outcome events to `docs/observability/task-trace.jsonl` when the repo uses `$trajectory-risk-supervisor`.
   - Use `project-local-skill-generator` to create `project-definition-of-done` when this repo should expose completion rules as a local Codex skill.

## Validation

- Run `./scripts/termination-check` when present.
- Confirm evidence names exact commands or runtime checks.
- Confirm any skipped layer has a documented reason.

## Completion Criteria

- The task has objective completion evidence or explicit unresolved blockers.
- The agent cannot honestly claim done based only on code inspection.
