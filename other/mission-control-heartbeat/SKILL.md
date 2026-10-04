---
name: mission-control-heartbeat
description: >-
  Keeps an agent alive in Mission Control by calling the api.agents.heartbeat
  mutation every 30-60 seconds. Use this skill when running any agent session:
  agents that miss heartbeats for 2 minutes get quarantined, and the heartbeat
  response is how you discover pending tasks, approvals, and budget state.
version: 1.0.0
owner: software-factory
risk: low
capabilities:
  - heartbeat-loop
  - quarantine-avoidance
  - task-discovery
  - budget-monitoring
requires_tools:
  - convex
related_skills:
  - mission-control-register-agent
  - mission-control-task-lifecycle
  - mission-control-budget-control
---

# Send Heartbeats

Call this regularly (every 30-60 seconds) to stay alive. Agents that miss heartbeats for 2 minutes get quarantined.

## API

```
Mutation: api.agents.heartbeat
Args:
  agentId: Id<"agents">
  currentTaskId?: Id<"tasks">         — Task you're currently working on
  spendSinceLastHeartbeat?: number    — USD spent since last heartbeat
  soulVersionHash?: string            — Your current soul/config hash
  status?: string                     — Your status if changed
  errorMessage?: string               — Report errors (3 in a row = quarantine warning)

Returns:
  success: boolean
  budgetRemaining: number
  budgetExceeded: boolean
  pendingTasks: Task[]       — Tasks assigned to you
  claimableTasks: Task[]     — INBOX tasks matching your types
  pendingApprovals: Approval[]
  pendingNotifications: Notification[]
```

## Quarantine Rules

1. **Missing heartbeats for 2 minutes = quarantine.** Keep the loop running for the whole session.
2. **3 errors in a row = quarantine warning.** Report errors honestly via `errorMessage`, but fix the root cause fast.
3. Register first (`mission-control-register-agent`) — heartbeats need a valid `agentId`.

## Using the Response

- Check `pendingTasks` and `claimableTasks` on every beat to pick up work (`mission-control-task-lifecycle`).
- Check `budgetRemaining` / `budgetExceeded` before spending (`mission-control-budget-control`).
- Check `pendingApprovals` for decisions you are waiting on (`mission-control-request-approval`).
- Report `spendSinceLastHeartbeat` so budget tracking stays accurate.
