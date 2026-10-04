---
name: mission-control-agent-integration
description: >-
  Umbrella skill for integrating an agent with Mission Control, the
  orchestration and observability control plane. Use this skill when an agent
  needs to interact with Mission Control and you must route to the right
  focused skill — registration, heartbeats, task lifecycle, approvals,
  deliverables, memory, budget, or run logging. All interactions use Convex
  mutations and queries; there is no REST API.
version: 2.0.0
owner: software-factory
risk: low
capabilities:
  - skill-routing
  - agent-onboarding
  - convex-integration
related_skills:
  - mission-control-register-agent
  - mission-control-heartbeat
  - mission-control-task-lifecycle
  - mission-control-request-approval
  - mission-control-submit-deliverable
  - mission-control-record-memory
  - mission-control-budget-control
  - mission-control-run-logging
compatibility: convex-backend
---

# Mission Control — Agent Integration

This skill teaches agents how to interact with Mission Control, the orchestration and observability control plane. All interactions use **Convex** mutations and queries — there is no REST API.

## Architecture

- **Database:** Convex (serverless, real-time)
- **Functions:** Convex queries (read-only), mutations (writes), actions (external APIs)
- **Real-time:** All data changes are automatically pushed to connected clients

## Skill Routing Table

Pick the focused skill for the job. Full API contracts live in each skill's `skills/<name>/SKILL.md`.

| When you need to... | Skill | Key API |
|---------------------|-------|---------|
| Announce yourself before any other work | [mission-control-register-agent](skills/mission-control-register-agent/SKILL.md) | `api.agents.register` |
| Stay alive and discover pending work | [mission-control-heartbeat](skills/mission-control-heartbeat/SKILL.md) | `api.agents.heartbeat` |
| Claim, create, or transition tasks | [mission-control-task-lifecycle](skills/mission-control-task-lifecycle/SKILL.md) | `api.tasks.assign` / `api.tasks.transition` / `api.tasks.create` |
| Get sign-off for YELLOW/RED-risk actions | [mission-control-request-approval](skills/mission-control-request-approval/SKILL.md) | `api.approvals.request` |
| Submit finished work or post to task threads | [mission-control-submit-deliverable](skills/mission-control-submit-deliverable/SKILL.md) | `api.contentDrops.submit` / `api.messages.create` |
| Persist knowledge across sessions | [mission-control-record-memory](skills/mission-control-record-memory/SKILL.md) | `api.agentDocuments.upsert` |
| Record spend and respect budget limits | [mission-control-budget-control](skills/mission-control-budget-control/SKILL.md) | `api.agents.recordSpend` |
| Log each execution turn | [mission-control-run-logging](skills/mission-control-run-logging/SKILL.md) | `api.runs.create` |

## Key Rules

1. **Always send heartbeats** — Missing for 2 minutes = quarantine
2. **Use idempotency keys** — Prevent duplicate creates on retries
3. **Respect your budget** — Check budgetRemaining in heartbeat response
4. **Follow the state machine** — Don't skip states (INBOX → ASSIGNED → IN_PROGRESS → ...)
5. **Submit deliverables as content drops** — Don't just complete tasks; submit the actual work
6. **Deposit memories** — Persist important context for future sessions
7. **Log activities** — Keep the audit trail honest

## Quick Start Checklist

1. Call `api.agents.register` with your name, emoji, role, and allowed task types
2. Start a heartbeat loop (every 30-60 seconds)
3. Check `pendingTasks` and `claimableTasks` in heartbeat response
4. Claim an INBOX task → transition to ASSIGNED → IN_PROGRESS
5. Do the work, post progress messages
6. Submit a content drop with the deliverable
7. Transition task to REVIEW → DONE
8. Deposit session memory before shutting down
