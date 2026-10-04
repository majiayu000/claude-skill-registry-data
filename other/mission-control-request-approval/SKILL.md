---
name: mission-control-request-approval
description: >-
  Requests human or dual-control approval for risky actions through the Convex
  api.approvals.request mutation. Use this skill when an action is YELLOW or
  RED risk tier — YELLOW needs a single approval, RED needs dual control (two
  decisions), and GREEN/LOW actions auto-approve. Poll status before acting.
version: 1.0.0
owner: software-factory
risk: high
capabilities:
  - approval-requests
  - risk-tiering
  - dual-control
  - decision-polling
requires_tools:
  - convex
related_skills:
  - mission-control-task-lifecycle
  - mission-control-heartbeat
---

# Request Approvals

Risky actions must be approved before execution. Approvals are first-class records in Mission Control with an audit trail.

## Risk Tiers

| Tier | Meaning | Decisions required |
|------|---------|--------------------|
| GREEN / LOW | Safe, reversible | 0 — auto-approved on request |
| YELLOW | Needs sign-off | 1 approval |
| RED | High blast radius | 2 approvals (dual control) |

## Request an Approval

```
Mutation: api.approvals.request
Args:
  requestorAgentId: Id<"agents">
  actionType: string          — Machine-readable action kind
  actionSummary: string       — One-line human-readable summary
  riskLevel: string           — "GREEN" | "LOW" | "YELLOW" | "RED"
  justification: string       — Why this action is needed
  projectId?: Id<"projects">
  taskId?: Id<"tasks">        — Related task (if any)
  toolCallId?: Id<"toolCalls">
  actionPayload?: any         — The exact payload you intend to execute
  estimatedCost?: number      — USD estimate
  rollbackPlan?: string       — How the action can be undone
  expiresInMinutes?: number   — Default 60
  idempotencyKey?: string     — Prevent duplicate requests on retries

Returns: { approval: Approval, created: boolean }
```

GREEN/LOW requests come back already `APPROVED`. YELLOW and RED come back `PENDING`; RED sets `requiredDecisionCount: 2`.

## Check the Decision

```
Query: api.approvals.get
Args: { approvalId: Id<"approvals"> }

Query: api.approvals.listPending
Args: { projectId?: Id<"projects">, limit?: number }
```

The heartbeat response (`mission-control-heartbeat`) also includes `pendingApprovals` for your agent.

Approval status values: `PENDING`, `ESCALATED`, `APPROVED`, `DENIED`, `EXPIRED`, `CANCELED`.

## Rules

1. **Never execute the action before the approval status is APPROVED.** Denied or expired means do not proceed.
2. Requests expire (default 60 minutes). Re-request with a new justification rather than acting on a stale approval.
3. Move the related task to `NEEDS_APPROVAL` while waiting (`mission-control-task-lifecycle`).
4. Provide `rollbackPlan` and `estimatedCost` for RED actions — reviewers need them to decide.
