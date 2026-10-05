---
name: agent-failure-introspection
description: Diagnose failed or unreliable agent workflows by classifying bad assumptions, missing observations, tool misuse, wrapper failures, hidden repair loops, incomplete validation, handoff gaps, and repeated failure patterns. Use after a failed harness run, flaky agent output, or confusing validation loop.
---

# Agent Failure Introspection

## Purpose

Turn an agent failure into evidence, a likely failure class, and the smallest durable fix to the harness or project workflow.

## Inspect First

- failing command output, browser logs, review findings, task plan, changed files, and validation evidence
- `PROGRESS.md`, `DECISIONS.md`, feature state, termination evidence, and sprint/task traces when present
- scripts or wrappers involved in the failure

## Procedure

1. Capture the failure.
   - Record expected behavior, actual behavior, commands run, files inspected, and the first observed failure.
   - Avoid rewriting history with post-hoc assumptions.

2. Classify the failure.
   - Run `scripts/diagnose_agent_failure.py <repo-or-report> --json` when available.
   - Check for missing inspection, wrong tool use, stale instructions, skipped validation, wrapper no-ops, hidden retries, unrecorded assumptions, weak handoff, or premature completion.
   - Use `$trajectory-risk-supervisor` when the failure is a repeated trajectory pattern, such as edit-before-inspection, repeated failures, or finalization without validation.

3. Decide the durable response.
   - Fix project code only when the root cause is project behavior.
   - Promote repeated process failures through `$review-feedback-promoter`.
   - Add missing evidence gates through `$pre-edit-investigation-gate`, `$termination-gatekeeper`, or `$skill-compliance-auditor`.

4. Write a concise report when useful.
   - Use `assets/templates/agent-failure-report.md.tmpl`.
   - Include reproduction, likely cause, evidence, and next validation commands.

## Validation

- Confirm diagnosis cites observed logs, files, or command output.
- Confirm the proposed fix maps to code, docs, tests, scripts, or skill guidance.
- Run the smallest command that proves the failure no longer reproduces, or record the blocker.

## Completion Criteria

- The failure is classified with evidence and a clear next action.
- Repeated failures are promoted into durable harness checks instead of handled as one-off memory.
