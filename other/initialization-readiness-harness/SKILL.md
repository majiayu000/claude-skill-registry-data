---
name: initialization-readiness-harness
description: Separate repo initialization from implementation. Use when a project needs startup readiness, first passing test evidence, task breakdown, scripts/init-check, or a clean initial checkpoint before feature work.
---

# Initialization Readiness Harness

## Purpose

Make the first agent phase establish a runnable, testable, documented baseline before business implementation begins.

## Inspect First

- manifests, lockfiles, README, startup scripts, test setup, local runtime docs, `AGENTS.md`, CI, and existing task plans
- whether the repo is new, newly scaffolded, or unreliable to start from scratch

## Procedure

1. Define initialization outputs.
   - `docs/development/startup-readiness.md`
   - `docs/development/task-breakdown.md`
   - `scripts/init-check` when a repeatable check is useful.

2. Prove the baseline.
   - Install dependencies using the project-native package manager.
   - Confirm the app or service can start, or document the precise blocker.
   - Confirm at least one test path exists and can pass, or document what must be added first.

3. Separate phases.
   - Do not mix feature implementation into initialization.
   - Initialization completes when a fresh agent can start, test, inspect progress, and pick the first task.

4. Add advisory validation.
   - Use `scripts/check_initialization_readiness.py` from this plugin.
   - Keep `scripts/init-check` focused on readiness, not full release validation.

5. Route follow-up work.
   - Use `feature-state-machine` for the task list when work is multi-feature.
   - Use `quality-gates-installer` for the broader validation interface.
   - Use `local-runtime-harness` for runtime reset, seed, and healthcheck depth.

## Validation

- Run `./scripts/init-check` when present.
- Confirm startup docs list install, dev, test, validation, ports, and current state.
- Confirm task breakdown contains ordered tasks with acceptance criteria.

## Completion Criteria

- The repo has a verified initialization baseline or precise blockers.
- Later sessions can begin implementation without rediscovering setup, test, or task structure.
