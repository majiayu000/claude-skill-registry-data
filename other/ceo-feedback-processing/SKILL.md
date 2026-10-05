---
name: ceo-feedback-processing
description: Use when an Agent is asked to diagnose and repair repository feedback recorded in the local feedback queue. The Skill owns the repository workflow and evidence receipt; the service owns persistence and state transitions.
metadata:
  managed_by: ceo-agent-service
  version: 1
---

# CEO Feedback Processing

Use persisted `feedback_key` as the stable identity. Confirm the repository root,
current branch, and current HEAD; preserve uncommitted user changes. The Console
API is local-only with no auth at
`http://127.0.0.1:8765/api/console/feedback`. Import formatting never calls a
model. No new UI workflow or `service_bugfix` route is allowed. Direct SQLite
writes are forbidden.

## Exact operations

| Purpose | Operation |
| --- | --- |
| pending/detail | `GET /api/console/feedback`; `GET /api/console/feedback/{feedback_key}` |
| claim/detail | `POST /api/console/feedback/batches`; `GET /api/console/feedback/batches/{batch_id}` |
| associate | `PATCH /api/console/feedback/batches/{batch_id}` |
| evidence | `PATCH /api/console/feedback/items/{feedback_key}` |
| reopen | `POST /api/console/feedback/items/{feedback_key}/reopen` |
| resolve | `POST /api/console/feedback/batches/{batch_id}/resolve` |

## Repository workflow

1. Use the brainstorming skill in every processing conversation. Read the
   pending batch and detail for every selected item before claiming the batch.
   Use supplied task, attempt, run, persisted summaries, and references; never
   invent IDs.
2. reproduce before editing. Capture the exact command, failure, and references.
   Add a regression test; run focused tests and relevant broad tests. Record
   each command, `exit_code=0`, run time, and brief output.
3. Claim only requested keys. Associate the supplied Workbench task using
   `workbench_task_id`, `workbench_turn_id`, `attempt_id`, and `agent_run_id`.
   Read batch detail back before editing.
4. Make the smallest repair and `git commit`. Verify `git rev-parse HEAD`
   matches the committed SHA before recording evidence.

## Reopen and current-round rules

Reopen with exactly `{"reason":"<factual reason>"}`. It returns to `pending`
and creates no round. Read back pending, then claim a new batch; claim creates
the new processing round. Never copy or reuse old evidence, green receipts, or
Workbench associations. An existing commit cannot replace fresh current-round
code, test, commit, restart, backlog, and readback evidence. Only the current
round receipt may resolve the item.

## Evidence and resolution

Every feedback-processing resolution requires restarting
`com.ceo-agent-service.main`. Verify `launchctl print`, a new before/after PID,
`/healthz`, and authoritative zero `processing`, `failed`, and `retryable`
failed/processing backlog. Deadlines never waive broad tests or these gates.

Persist per-item evidence through the API: commit SHA, focused/broad tests,
restart evidence, health evidence, associations, and concise note. Read item and
batch back before marking the item resolved. Resolve only after all items
complete. Evidence-free resolve is forbidden; incomplete evidence or any
failure or interruption leaves the item `processing` in the same batch and
Workbench task.
