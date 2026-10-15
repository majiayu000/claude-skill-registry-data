---
name: TaskFlow
description: Durable multi-step flows that survive process restart, coordinate waits, and expose revision-safe state.
requires:
  bins: []
  env: []
---

# TaskFlow

Use this skill when a job needs to outlive one prompt or one session turn
while keeping a single owner context, single return channel, and a
persistent place to inspect or resume the work. The agent reaches TaskFlow
through the `taskflow` tool; the operator uses `agent flow ...` CLI.

## Use when

- Multi-step background work with one owner (inbox triage, weekly report,
  bible-upload style jobs)
- Work that waits on detached external tasks (agent-to-agent delegation,
  cron-triggered side jobs, external APIs with long SLAs)
- Jobs that must survive process restart — state and progress persist in
  `./data/taskflow.db`
- Jobs that need revision-checked mutations because multiple paths
  (heartbeat, user prompt, external event) may race to advance the same
  flow

## Do not use when

- Single-turn chat — the LLM can answer without any persistence
- Fire-and-forget notifications — heartbeat alone is enough
- Anything that fits comfortably into one tool call
- Business branching logic — keep that in the caller; TaskFlow owns
  identity, state persistence, and waiting semantics, not conditionals

## Tool surface (`taskflow`)

### `start`
- `controller_id` (string, required) — logical caller, e.g. `"kate/inbox-triage"`
- `goal` (string, required) — short human-readable goal
- `current_step` (string, optional, default `"init"`) — first step name
- `state` (object, optional, default `{}`) — initial `state_json`

Auto-transitions Created → Running so the flow is immediately active.
Returns `{flow: {id, status:"running", revision:1, ...}}`.

### `status`
- `flow_id` (string UUID, required)

Returns current flow snapshot or `{ok: false, error: "not_found"}`.

### `advance`
- `flow_id` (string UUID, required)
- `patch` (object, optional) — shallow-merge into `state_json`
- `current_step` (string, optional) — next step label

Rejected when `cancel_requested` is set or the flow is terminal.

### `cancel`
- `flow_id` (string UUID, required)

Forces transition to `Cancelled`. Allowed from any non-terminal status.
Cancel intent is sticky: if a slower path also sets `cancel_requested`,
the flow stays headed to `Cancelled`.

### `list_mine`
No arguments. Returns `{count, flows: [...]}` for the current session only.
Cross-session access is blocked at the tool level.

## Execution guidance

- Start a flow the first time work needs to persist beyond this turn; don't
  wrap every tool call in a flow.
- Pick a stable `controller_id` — it shows up in the operator CLI and in
  the audit log. Format is `<agent>/<purpose>` by convention.
- Use `advance` to record progress between steps. The `state_json` is the
  source of truth; audit events capture the "what happened".
- When a job must wait (timer, external event, manual resume), the host
  invokes `manager.set_waiting` directly — `advance` does not change
  status. Ask the operator if unsure.
- When a flow ends successfully, the host calls `manager.finish`. There is
  no dedicated LLM-facing `finish` action today; when work is done, a
  caller-side handler decides when to finalize.
- If `-32011`/`-32012`-style errors surface from extension tools, the
  owning flow should `fail` with the reason so the audit log is honest.

## Operator inspection

```bash
agent flow list                 # table of all flows
agent flow show <uuid>          # detail + steps
agent flow cancel <uuid>        # sticky cancel intent + flip to Cancelled
agent flow resume <uuid>        # manually resume a Waiting flow
```

All commands read `TASKFLOW_DB_PATH` (default `./data/taskflow.db`).

## Anti-patterns

- Storing user PII inside `state_json` without thinking — the JSON blob is
  checked into the SQLite file on disk.
- Calling `advance` in a tight loop — each call is a revision bump and an
  audit event. If you need bulk updates, batch before calling.
- Hiding branching logic inside the flow runtime — put it in the
  controller (the caller). TaskFlow is flow identity, not business logic.
