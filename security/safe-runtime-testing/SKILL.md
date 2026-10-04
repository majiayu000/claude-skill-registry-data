---
name: safe-runtime-testing
description: "Run authorized, non-destructive security tests against Ouros local or QA services. Use for runtime verification of auth, authorization, API, business-logic or configuration hypotheses when the environment must be left clean and stable afterward."
---

# Safe Runtime Testing

Goal: obtain reproducible security evidence while leaving application state functionally unchanged except for preserved audit logs.

Read `../../references/ouros-security-model.md` when Ouros ownership boundaries are involved.

## Gate before every test

Proceed only when all are true:

- target is local or explicitly authorized QA;
- test identity is known;
- exact resources touched by the test are known;
- pre-existing business/user data will not be destructively modified;
- expected mutation is bounded;
- rollback/cleanup is defined;
- availability impact is negligible.

Otherwise mark the hypothesis `blocked`.

## Isolation

Generate a run ID and track every object created by the test.

Prefer, in order: read-only requests, dedicated fixtures, database transaction + rollback, temporary resources with exact-ID cleanup, and reversible configuration with captured before-state.

Never identify cleanup targets by a broad name pattern alone.

## Execution loop

1. Capture relevant before-state.
2. Perform the smallest probe that can answer the hypothesis.
3. Capture status, response metadata, trace/request ID and affected object IDs.
4. Avoid repeating a successful state-changing probe just for confidence.
5. Restore captured state or delete only resources created by this run.
6. Re-read relevant state to verify cleanup.
7. Preserve normal application/audit logs.

## Authorization test pattern

Use two dedicated principals with dedicated resources: principal A owns resource A; principal B owns resource B. Probe whether A can perform the specific operation on B's test resource. Never substitute real user resources.

## Failure handling

If cleanup fails, stop further mutations, record exact residual resource IDs, do not broaden deletion criteria, and report cleanup failure separately.

If the app becomes unhealthy, stop the campaign. Do not attempt aggressive recovery unless explicitly authorized.

## Result

Return: `run_id`, `target`, `hypothesis`, `result` (`candidate|rejected|blocked`), `evidence`, `created_resources`, `cleanup` (`verified|incomplete|not-needed`), and `residual_state`.

A runtime result is still a `candidate` until the finding verifier confirms it.
