---
name: session-continuity-harness
description: Preserve agent state across sessions. Use when a repo needs PROGRESS.md, DECISIONS.md, handoff protocol, rebuild-cost reduction, session start or exit routines, or continuity for long-running Codex tasks.
---

# Session Continuity Harness

## Purpose

Let a fresh agent session resume work without rediscovering project state, design decisions, blockers, or validation status.

## Inspect First

- `PROGRESS.md`, `DECISIONS.md`, handoff docs, feature lists, specs, recent commits, validation logs, and current branch state
- whether the task is likely to span sessions or exceed a comfortable context budget

## Procedure

1. Add durable state artifacts.
   - Create or update `PROGRESS.md`.
   - Create or update `DECISIONS.md`.
   - Create or update `docs/development/session-handoff.md`.
   - Use templates only as starting points, then fill with repo-specific state.

2. Define session routines.
   - Session start: read agent instructions, progress, decisions, feature state, and run a cheap health check.
   - Session exit: update progress, record validation evidence, document blockers, remove temporary artifacts, and leave next actions.

3. Preserve decision context.
   - Record important design decisions with date, choice, reason, rejected alternatives, and constraints.
   - For architecture, dependency, workflow, or product decisions that need a durable record, use `assets/templates/architecture-decision-record.md.tmpl`.
   - Prefer concise entries over long essays.

4. Add advisory validation.
   - Create or recommend `scripts/check-session-handoff`.
   - Use `scripts/check_session_handoff.py` from this plugin.
   - Wire into validation only for repos that require clean handoff discipline.

5. Coordinate with other skills.
   - Use `feature-state-machine` for active work and pass evidence.
   - Use `termination-gatekeeper` before marking work done.
   - Use `entropy-auditor` for stale temporary artifacts.
   - Use `project-local-skill-generator` to create `project-session-handoff` when this repo should expose handoff routines as a local Codex skill.

## Validation

- Run `./scripts/check-session-handoff` when present.
- Confirm progress includes current state, completed work, in-progress work, blockers, validation evidence, and next actions.
- Confirm decisions include at least one durable rationale when meaningful decisions were made.

## Completion Criteria

- A fresh agent can rebuild project state from repo files without verbal context.
- Handoff records what changed, why, what passed or failed, and what to do next.
