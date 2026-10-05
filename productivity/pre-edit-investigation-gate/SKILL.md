---
name: pre-edit-investigation-gate
description: Require inspect-before-edit evidence for risky changes. Use before modifying architecture, data, auth, dependencies, migrations, generated workflows, validation wrappers, or broad UI/API behavior when the agent must prove it inspected relevant files and affected surfaces first.
---

# Pre-Edit Investigation Gate

## Purpose

Prevent blind edits by requiring explicit investigation evidence before high-risk changes.

## Inspect First

- files and manifests likely affected by the task
- docs, specs, feature state, validation wrappers, architecture boundaries, migrations, dependency policy, and recent diffs
- existing `docs/development/pre-edit-investigation.md` if present

## Procedure

1. Decide whether the gate applies.
   - Apply it for broad edits, security/auth/data changes, dependency additions, migrations, CI/validation rewrites, and user-facing UI/API behavior.
   - For trivial one-file edits, record a short skip rationale.

2. Gather evidence before editing.
   - List files read, commands inspected, affected surfaces, known invariants, assumptions, and expected validation.
   - Use `assets/templates/pre-edit-investigation.md.tmpl` when creating a durable artifact.
   - When `docs/observability/task-trace.jsonl` exists, add an inspect or pre-edit event so `$trajectory-risk-supervisor` can see that inspection happened.

3. Validate the evidence.
   - Run `scripts/check_pre_edit_evidence.py <repo>` when an artifact exists.
   - The evidence must be specific enough for another agent to understand why the edit path is justified.

4. Route related work.
   - Use `$task-planning-and-pr-protocol` for implementation planning.
   - Use `$agent-reviewer` and `$termination-gatekeeper` after edits.

## Validation

- Confirm the investigation names real files, commands, affected surfaces, assumptions, and validation commands.
- Confirm any skip rationale is proportional to the risk.

## Completion Criteria

- Risky edits have pre-edit evidence before implementation starts.
- Reviewers can distinguish inspected facts from assumptions.
