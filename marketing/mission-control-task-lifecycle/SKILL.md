---
name: mission-control-task-lifecycle
description: >-
  Drives tasks through the Mission Control state machine: find INBOX tasks,
  assign yourself, and transition through ASSIGNED, IN_PROGRESS, REVIEW, and
  DONE. Use this skill when claiming, creating, or progressing a task — every
  status change must go through api.tasks.transition with an idempotency key.
version: 1.0.0
owner: software-factory
risk: medium
capabilities:
  - task-claiming
  - task-creation
  - state-transitions
  - idempotent-writes
requires_tools:
  - convex
related_skills:
  - mission-control-heartbeat
  - mission-control-request-approval
  - mission-control-submit-deliverable
---

# Claim and Work on Tasks

## Find Available Tasks

```
Query: api.tasks.listByStatus
Args: { status: "INBOX", projectId?: Id }
— Filter results by your allowedTaskTypes
```

The heartbeat response also surfaces `pendingTasks` (assigned to you) and `claimableTasks` (INBOX tasks matching your types).

## Assign Yourself to a Task

```
Mutation: api.tasks.assign
Args:
  taskId: Id<"tasks">
  assigneeIds: [yourAgentId]
```

## Transition a Task Through States

```
Mutation: api.tasks.transition
Args:
  taskId: Id<"tasks">
  toStatus: string    — Target status
  actorType: "AGENT"
  actorAgentId: Id<"agents">
  idempotencyKey: string   — Unique key to prevent duplicates
  reason?: string
```

## State Machine Flow

```
INBOX → ASSIGNED → IN_PROGRESS → REVIEW → DONE
```

Other states: NEEDS_APPROVAL, BLOCKED, FAILED, CANCELED

**Follow the state machine — don't skip states** (INBOX → ASSIGNED → IN_PROGRESS → ...).

## Create a New Task

```
Mutation: api.tasks.create
Args:
  title: string
  type: "CONTENT" | "SOCIAL" | "EMAIL_MARKETING" | "CUSTOMER_RESEARCH" |
        "SEO_RESEARCH" | "ENGINEERING" | "DOCS" | "OPS"
  priority: 1 (critical) | 2 (high) | 3 (normal) | 4 (low)
  description?: string
  projectId?: Id<"projects">
  creatorAgentId?: Id<"agents">
  assigneeIds?: Id<"agents">[]
  idempotencyKey: string
```

## Rules

1. **Use idempotency keys** on every transition and create — they prevent duplicate writes on retries.
2. When work is done, don't just close the task: submit the deliverable (`mission-control-submit-deliverable`), then transition REVIEW → DONE.
3. If an action needs sign-off, move the task to NEEDS_APPROVAL and request approval (`mission-control-request-approval`).
