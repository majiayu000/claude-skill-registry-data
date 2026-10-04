---
name: mission-control-run-logging
description: >-
  Records every agent execution turn as a run in Mission Control. Use this
  skill when starting a run (status RUNNING), completing or failing one
  (COMPLETED / FAILED), and reporting model, token counts, and cost so the
  observability and audit trail stays honest across all agent activity.
version: 1.0.0
owner: software-factory
risk: low
capabilities:
  - run-recording
  - token-accounting
  - audit-trail
requires_tools:
  - convex
related_skills:
  - mission-control-budget-control
  - mission-control-heartbeat
---

# Log Runs

Record each execution turn:

```
Mutation: api.runs.create
Args:
  agentId: Id<"agents">
  taskId?: Id<"tasks">
  sessionKey: string
  model: string           — e.g., "claude-sonnet-4-20250514"
  inputTokens: number
  outputTokens: number
  costUsd: number
  status: "RUNNING" | "COMPLETED" | "FAILED"
  idempotencyKey: string
```

## Rules

1. **Log activities — keep the audit trail honest.** Every execution turn gets a run record.
2. Start with `status: "RUNNING"`, then record the terminal state (`COMPLETED` or `FAILED`) with final token counts and cost.
3. Use `idempotencyKey` so retried creates never duplicate run records.
4. Pass the run's `costUsd` through to spend tracking as well (`mission-control-budget-control`).
