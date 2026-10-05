---
name: trajectory-risk-supervisor
description: Classify task traces, detect risky engineering trajectories, score advisory bad-state risk, and route to the least disruptive intervention. Use when a repo has docs/observability/task-trace.jsonl, trajectory risk policy, repeated agent drift, skipped validation, broad diffs, or needs shadow-mode trajectory supervision.
---

# Trajectory Risk Supervisor

## Purpose

Use observable task traces to detect quality drift before finalization without turning the harness into a blocking daemon.

## Inspect First

- `docs/observability/task-trace.jsonl`
- `docs/observability/trajectory-risk-policy.json`
- `docs/observability/trajectory-risk-report.md`
- feature state, sprint contract, termination evidence, pre-edit evidence, review findings, and recent validation output

## Procedure

1. Collect or inspect trace events.
   - Use `docs/observability/task-trace.jsonl` as newline-delimited JSON.
   - Events should record task id, task type, phase, action, files read, files changed, commands run, validation, risk surfaces, intervention, outcome, and notes.
   - Use `scripts/append_task_trace.py` when a deterministic event append is useful.

2. Classify the current trajectory.
   - Run `scripts/classify_agent_trace.py <repo> --json`.
   - Derive task phase, task type, repo understanding, diff scope, test status, risk surfaces, repeated failure loops, and evidence coverage.

3. Check invariants and score risk.
   - Run `scripts/check_trajectory_invariants.py <repo> --json`.
   - Run `scripts/score_trajectory_risk.py <repo> --json`.
   - Treat scoring as shadow/advisory unless the target repo explicitly wires enforcement through its own wrapper.

4. Recommend the least disruptive intervention.
   - Editing before inspection routes to `$pre-edit-investigation-gate`.
   - Repeated failures route to `$agent-failure-introspection`.
   - Finalization without tests routes to `$termination-gatekeeper`.
   - Dependency choices without sources route to `$research-first-change`.
   - UI lifecycle gaps route to `$click-path-and-browser-qa`.
   - Security, migration, or broad-diff risks route to `$agent-reviewer` or a generated reviewer subagent.

5. Document risk when useful.
   - Use `assets/templates/trajectory-risk-report.md.tmpl`.
   - Keep hooks out of default behavior; plugin hooks are a future opt-in shadow layer only after users trust them.

## Validation

- Run `scripts/classify_agent_trace.py <repo> --json`.
- Run `scripts/score_trajectory_risk.py <repo> --json`.
- Confirm every risk cites trace evidence and maps to a concrete intervention or command.
- Confirm advisory mode does not block unrelated lightweight repos.

## Completion Criteria

- The current task trajectory has a clear state, risk level, evidence list, and recommended intervention.
- The repo can opt into `./scripts/check-trajectory-risk` without changing the stable baseline command interface.
