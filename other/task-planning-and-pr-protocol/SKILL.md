---
name: task-planning-and-pr-protocol
description: Standardize Codex task planning and PR output. Use when work needs a task plan, PR description, validation evidence, risk assessment, rollback notes, docs/test summary, review rubric, or .github/pull_request_template.md.
---

# Task Planning And PR Protocol

## Purpose

Make agent work auditable from plan through PR by standardizing validation, risks, docs, tests, rollback, and follow-ups.

## Inspect First

- existing PR templates, review rubrics, task docs, `AGENTS.md`, validation scripts, release docs, and project-specific contribution rules

## Procedure

1. Define task protocol.
   - Planning expectations.
   - Validation evidence.
   - Test and docs update rules.
   - Risk and rollback notes.
   - For broad, risky, dependency, data, auth, CI, or user-facing behavior changes, route pre-implementation inspection through `$pre-edit-investigation-gate`.

2. Add PR structure.
   - `.github/pull_request_template.md`
   - `docs/development/task-protocol.md`
   - `docs/development/review-rubric.md`

3. Align reviewers.
   - Use `agent-reviewer` categories P0-P3.
   - Use `$agent-reviewer` categories P0-P3.
   - Include release and migration notes when relevant.

4. Keep it usable.
   - Templates should be short enough to fill out honestly.
   - Avoid ceremony for tiny changes unless risk is non-trivial.

## Validation

- Confirm PR template includes summary, validation, tests, docs, risks, rollback, and follow-ups.
- Confirm task protocol points to real commands.

## Completion Criteria

- Agent-generated PRs include enough evidence for review without requiring archaeology.
