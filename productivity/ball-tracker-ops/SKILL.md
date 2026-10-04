---
name: ball-tracker-ops
description: >-
  Use when working on JhnsonO/ffa-automations' FFA 360 Ball Tracker: planning or implementing a bounded task, reviewing a GitHub Actions run or artifact, diagnosing a failure, or reconciling project state. Enforces summary-first retrieval, one-poll workflow handling, frozen-boundary protection, and concise evidence-based reporting.
---

# FFA 360 Ball Tracker — Lean GitHub Operations

## Mission
Complete one bounded tracker task with the smallest useful evidence set. Prevent wasted context from broad repository reads, repeated polling, and raw-log dumping.

This Skill is an operating layer only. It never overrides `CLAUDE.md`, `docs/ai-project-state.md`, the user's instruction, or safety constraints.

## Scope
Use only for `JhnsonO/ffa-automations` work involving the 360° Ball Tracker: planning, implementation, test execution, GitHub Actions, artifacts, diagnosis, visual-review gates, or state reconciliation.

Do not use it for unrelated FFA operations, general GitHub questions, marketing, or the separate OEV stitcher project.

## Bootstrap — target, do not ingest
1. Read `CLAUDE.md`.
2. Read the **Active gate and next action** section of `docs/ai-project-state.md` first.
3. Retrieve earlier state sections only when the active task depends on a named data contract, frozen boundary, prior finding, artifact, or decision.
4. Identify the current gate and exact files to change in no more than three lines, then proceed.

Do not read the entire change log or request prior chat history by default. The state file remains authoritative even when it is read in targeted sections.

## Evidence retrieval ladder
Use the first sufficient level and stop:

1. The active task, workflow YAML, exact source file(s), and relevant test file(s).
2. Compact outputs: `run_summary.json`, summary TXT/JSON, stage report, manifest, or artifact inventory.
3. Workflow job/step status to identify the failed step.
4. Only the named failed job's small error window from raw logs.

Never open full raw logs for a successful job. Never inspect unrelated workflow logs, download a large artifact, or read broad repository files merely to “get context.”

## Build and run discipline
- Complete one bounded build ticket per chat unless the user explicitly expands scope.
- Reuse established schemas, geometry, constants, and workflow patterns.
- Do not redesign adjacent systems, tune thresholds, refactor frozen production code, or start optional work without a decision-changing reason.
- Preserve `ball_tracker/run_tracker.py` v11, the v6 safe fallback, Stage 1b behaviour, and the separation between Stage 2/experiments and the renderer unless the user explicitly approves a boundary change.
- A green workflow proves execution only; it does not prove tracking quality or product acceptance.
- When a visual decision gate exists, visual evidence outranks aggregate counts.

## Actions workflow policy
- Before dispatching, name the purpose, expected artifact, and acceptance check.
- After dispatching, do one immediate status check only to catch a fast failure.
- Do not repeatedly poll. Mark the run `DISPATCHED — UNVERIFIED` and wait for a supplied completion result or a later explicit review request.
- Do not re-dispatch unless there is a named failure reason or a changed input/code path that makes the retry informative.
- When an expected artifact is missing, report the failed stage and evidence; do not silently label the work pending or successful.

## State discipline
After a meaningful code change, dispatch, run completion, artifact review, failure, or decision:

1. Reconcile `docs/ai-project-state.md` in the same commit or immediately after.
2. Update the current gate/status and next action in place; remove or replace stale active instructions.
3. Record exact run and artifact identifiers only when verified.
4. Keep a dispatched run explicitly `DISPATCHED — UNVERIFIED` until its outcome/artifact is inspected.
5. If the state document contradicts itself or current evidence, flag it as a risk rather than guessing which instruction wins.

## Response contract
Return only:

1. **Changed** — exact files and one-line purpose.
2. **Verified** — exact test, report, or artifact outcome.
3. **Dispatched** — workflow/run/artifact status, if applicable.
4. **Risk** — only a real unresolved risk, blocker, or decision.

No tool-call narration, long handover, generic reassurance, raw-log paste, or repeated restatement of project history.
