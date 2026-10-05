---
name: feature-state-machine
description: Add or maintain a machine-readable feature state list for agent work. Use when a repo needs WIP=1 control, feature states, verification commands, pass-state evidence, or docs/features/feature_list.json.
---

# Feature State Machine

## Purpose

Make feature scope executable by tracking one active work item, explicit verification, and evidence-backed state transitions.

## Inspect First

- existing specs, OpenSpec changes, task docs, issue lists, `PROGRESS.md`, validation scripts, and current work-in-progress
- whether the repo has multi-session or multi-feature agent work that justifies a feature state file

## Procedure

1. Define the feature list.
   - Create or update `docs/features/feature_list.json` only when feature tracking adds value.
   - Use `assets/templates/feature-list.json.tmpl` for the initial shape.
   - Preserve existing IDs and evidence.

2. Enforce advisory WIP control.
   - Default `wip_limit` is `1`.
   - Only one feature should be `active`.
   - Do not mark a feature `passing` without executable evidence.

3. Make each feature checkable.
   - Include `id`, `title`, `behavior`, `verification`, `state`, `evidence`, `dependencies`, and `notes`.
   - Verification should be a real command or focused validation path.
   - Link feature IDs to OpenSpec tasks or lightweight specs when present.

4. Add local checks.
   - Create or recommend `scripts/check-feature-state`.
   - Use `scripts/check_feature_state.py` from this plugin for deterministic validation.
   - Wire into `scripts/validate` only when the repo wants feature-state checks in baseline validation.

5. Route implementation.
   - Use `task-planning-and-pr-protocol` for task planning.
   - Use `termination-gatekeeper` before declaring a feature complete.
   - Use `session-continuity-harness` for handoff after partial work.
   - Use `project-local-skill-generator` to create `project-feature-workflow` when this repo should expose feature state as a local Codex skill.

## Validation

- Run `./scripts/check-feature-state` when present.
- Confirm no more than `wip_limit` features are active.
- Confirm every feature has behavior and verification text.
- Confirm every `passing` feature has evidence.

## Completion Criteria

- The repo has a usable feature state surface or a documented reason it is unnecessary.
- Active work, blockers, passing evidence, and next work are unambiguous to a fresh agent session.
