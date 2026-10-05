---
name: sprint-contract-observability
description: Add process observability for agent work. Use when a task needs sprint contracts, evaluator rubrics, task traces, acceptance evidence, or structured feedback between generator and reviewer roles.
---

# Sprint Contract Observability

## Purpose

Make agent process intent observable through contracts, rubrics, traces, and evidence-backed evaluator feedback.

## Inspect First

- current task plan, specs, feature list, observability docs, review rubric, validation scripts, browser/runtime debugging docs, and recent QA feedback

## Procedure

1. Create a sprint contract.
   - Use `docs/observability/sprint-contract.md`.
   - Define scope, exclusions, touched surfaces, verification standards, runtime signals, and handoff expectations.

2. Create an evaluator rubric.
   - Use `docs/observability/evaluator-rubric.md`.
   - Score correctness, product behavior, architecture, tests, accessibility, observability, and maintainability when relevant.

3. Record task trace when useful.
   - Use `docs/observability/task-trace.jsonl` for task events, checks, failures, fixes, and evidence.
   - Keep entries compact and machine-readable.
   - Use the canonical trajectory event shape: version, timestamp, task id, task type, phase, action, files read, files changed, commands run, validation, risk surfaces, intervention, outcome, and notes.
   - Route trajectory classification and advisory risk scoring to `$trajectory-risk-supervisor`.

4. Add advisory validation.
   - Create or recommend `scripts/check-sprint-contract`.
   - Use `scripts/check_sprint_contract.py` from this plugin.

5. Coordinate runtime observability.
   - Use `observability-harness` for logs, diagnostics, correlation IDs, and health checks.
   - Use `chrome-devtools-runtime-debugger` for live browser evidence.
   - Use `agent-reviewer` for findings-first evaluation.
   - Use `$subagent-review-orchestrator` when explicit reviewer, browser QA, docs research, or trajectory auditor subagents would improve evaluation.

## Validation

- Run `./scripts/check-sprint-contract` when present.
- Confirm scope, exclusions, verification standards, rubric, and trace are consistent.
- Confirm evaluator feedback cites evidence instead of subjective approval.

## Completion Criteria

- The task has observable process intent and structured evaluation criteria.
- Future sessions can see why work was accepted, rejected, or deferred.
