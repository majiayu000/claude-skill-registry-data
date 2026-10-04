---
name: task-ledger-mcp
description: Manage canonical task state through the task-ledger MCP server. Use when creating, reading, updating, or transitioning tasks, adding notes or artifact links, or querying task history. The MCP ledger is the authoritative task state system; repo markdown files are derived or legacy surfaces only.
---

# Task Ledger MCP

The MCP ledger is canonical for mutable task state. Do not invent, fork, or maintain task state in markdown files, chat context, or any other ad hoc surface.

## Authority model

| Agent | Write authority |
|---|---|
| Orchestrator | Full write: `task_create`, `task_update`, `task_transition`, `task_invalidate`, `task_add_note`, `task_link_artifact` |
| Spec | Read freely. May call `task_add_note` and `task_link_artifact` only when Orchestrator has included the `project_token` in the task packet for that purpose. This is a per-task grant, not a standing permission. |
| Triage | Read freely. May call `task_add_note` and `task_link_artifact` only when Orchestrator has included the `project_token` in the task packet for that purpose. This is a per-task grant, not a standing permission. |
| Builder | Read freely. No canonical task-state ownership. May call `task_link_artifact` only when Orchestrator has included the `project_token` in the task packet for that purpose. This is a per-task grant, not a standing permission. |
| QA | Read freely. May call `task_add_note` and `task_link_artifact` only when Orchestrator has included the `project_token` in the task packet for that purpose. This is a per-task grant, not a standing permission. |
| Security | Read freely. May call `task_add_note` and `task_link_artifact` only when Orchestrator has included the `project_token` in the task packet for that purpose. This is a per-task grant, not a standing permission. |
| Release Manager | Read freely. May call `task_link_artifact` only when Orchestrator has included the `project_token` in the task packet for that purpose. This is a per-task grant, not a standing permission. |

Only Orchestrator holds the `project_token`. Other agents query task state using the read-only surface — no token required:

- `task_get` — fetch a single task by UUID
- `task_list` — query tasks with filters (project, state, kind, owner, overdue, etc.)
- `task_history` — full event, note, and artifact history for a task
- `project_get` — fetch project metadata by `project_id` or `project_slug`
- `project_list` — list all known projects (tokens never returned)

## Rules

- Do not treat `docs/delivery/task-ledger.md` as canonical mutable state. It is a legacy format and optional human snapshot.
- Read current task state from MCP before mutating it. Never assume state from context or prior messages.
- Use explicit MCP mutations rather than narrative-only bookkeeping.
- Record every lifecycle change as a `task_transition`, not just a note or a chat message.
- Attach artifact references (`task_link_artifact`) when linking issues, PRs, branches, commits, or decision records.
- Use `task_add_note` for diagnostic context, blockers, or explanations that do not change state.
- Treat MCP tool failure as a real failure. Do not silently continue as if the write succeeded.

## Task creation

Mandatory fields: `project_id`, `project_token`, `kind`, `title`.

Recommended fields at creation: `state`, `priority`, `owner_agent_type`, `owner_agent_id`, `next_action`, `issue_number`.

Use `idempotency_key` when there is any risk of duplicate creation (e.g. retried bootstrap steps).

## State transitions

Always supply `from_state` and the current `revision`. If the transition is rejected with `revision_mismatch` or a wrong `from_state`, re-read the task with `task_get` before retrying — the state may have changed concurrently.

Valid states:

```
new → triage → specifying → ready_for_build → building →
reviewing → security_review → qa_review → release_pending → done

any state → blocked
any state → invalid  (via task_invalidate only)
```

## Error handling

All tool failures return `isError=true` with a JSON payload:

```json
{"error_code": "revision_mismatch", "message": "..."}
```

Canonical error codes and required responses:

| Code | Meaning | Response |
|---|---|---|
| `invalid_token` | Wrong or rotated `project_token` | Stop. Report to Orchestrator. Do not guess or cache old tokens. |
| `project_not_found` | Project does not exist in ledger | Stop. Check project_id. May need to run `project_create`. |
| `task_not_found` | No task with that UUID | Stop. Verify task_id. Do not create a replacement silently. |
| `revision_mismatch` | Concurrent write changed state/revision | Re-read with `task_get`, reconcile, then retry if still valid. |
| `already_invalid` | Task already soft-deleted | No action needed; log and continue. |
| `validation_error` | Input outside allowed set | Fix input. Do not retry with the same invalid value. |
| `duplicate_slug` | Project slug already registered | Use existing project. Do not create a duplicate. |

## Fallback when MCP is unavailable

If the MCP server is unreachable:

1. Do **not** fork canonical state into ad hoc markdown files or chat state.
2. Report `BLOCKED` with reason `mcp-unavailable` to whoever dispatched the task.
3. If a task transition was in progress, do not assume it completed.
4. When MCP recovers, re-read current state with `task_get` before resuming.

Silently degrading to a file-based workaround creates split truth that is difficult to reconcile. Explicit blocking is the correct response.

## Project token

- Generated once at `project_create`. Shown only at creation and at each `project_rotate_token` call.
- Stored by Orchestrator in its workspace config. Never passed to other agents.
- If lost, use `project_rotate_token` to issue a new one.
- Rotate the token if it may have been exposed or logged.
