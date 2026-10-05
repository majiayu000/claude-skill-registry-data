---
name: prompt-to-spec-converter
description: Convert vague product or engineering requests into executable repo-local specs before coding. Use when a task is ambiguous, feature-sized, risky, cross-cutting, or needs acceptance criteria, non-goals, testing plan, rollout notes, or architecture impact.
---

# Prompt To Spec Converter

## Purpose

Turn a user request into a decision-complete spec that an agent or engineer can implement without guessing.

Use `openspec-sdd` instead when the user wants formal spec-driven development, OpenSpec artifacts, proposal/design/tasks, delta specs, or archiveable feature history.

## Inspect First

- user request and conversation context
- product docs, architecture docs, related source modules, tests, schemas, routes, and existing specs
- constraints from `AGENTS.md` and validation scripts

## Procedure

1. Separate facts from assumptions.
   - Keep requirements grounded in user text and repo facts.
   - Ask only for high-impact product intent that cannot be derived.
   - Use `$research-first-change` when the spec depends on current external APIs, package behavior, standards, or security guidance.

2. Draft the spec.
   - Problem
   - Goals
   - Non-goals
   - Requirements
   - Acceptance criteria
   - Architecture impact
   - Testing plan
   - Rollout/risk
   - Assumptions
   - For UI features, include accessible-name expectations for icon-only actions.

3. Save the spec.
   - Use `docs/specs/YYYY-MM-DD-feature-name.md`.
   - Pick a short kebab-case feature name from the request.

4. Link follow-on work.
   - Reference validation commands and affected docs.
   - Use `task-planning-and-pr-protocol` when the spec is ready for implementation planning.
   - Use `openspec-sdd` when the lightweight spec should become a formal OpenSpec change.
   - Use `feature-state-machine` when the spec becomes multi-step implementation work with WIP state and evidence.

## Validation

- Confirm acceptance criteria are testable.
- Confirm assumptions are explicit.
- Confirm affected modules and validation commands are named when known.
- For web UI specs, confirm the testing plan includes a browser-level workflow when a complete user lifecycle changes.

## Completion Criteria

- The implementation task has clear goals, boundaries, tests, and risk notes.
- The spec avoids hidden product decisions.
