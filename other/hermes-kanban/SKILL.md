---
name: hermes-kanban
description: >-
  Run a persistent Hermes Kanban board with multiple cards, owners, dependencies and worker
  profiles. When heterogeneous tasks span turns or a card stalls, dispatch independent lanes, review
  their results and recover or reassign blocked work. Not for one isolated coding CLI handoff.
metadata:
  revision: "4"
  areas: "work-management,software-development"
  targets: "hermes"
  summary: "multi-card board work: decomposition, parallel dispatch, review gates, stuck-card recovery"
  summary_zh: "多卡片看板工作：拆解、并行派发、评审门禁、卡住任务恢复"
  kind: "entry"
---

# Hermes Kanban

Use a persistent board for heterogeneous work with separate owners,
dependencies or review across turns. Use a resumable runner for uniform
fan-out, `gdd` for one written increment, or a direct handoff for one bounded
assignment. Do not put a one-turn action on the board just for tracking.

1. **Prepare.** Confirm board, tenant, account, profile and tool access.
   Write durable shared inputs before creating cards. Give each card an owner,
   explicit scope, workspace, dependencies, commands and observable finish
   criteria. Calibrate thresholds on a real sample before assigning.
2. **Dispatch.** Designate one orchestrator to route and review, not silently
   take over. Separate concurrent writers by paths or worktrees; link actual
   dependencies. A time limit is not serialization. Use an existing checkout
   only when authorized and required by its publisher. Read the
   [board profile guidance](references/board-profile-2de9f51.md) before changing
   dispatcher topology or relying on defaults.
3. **Work.** Read the card, parent handoffs and prior attempts. Confirm
   workspace and permissions, then execute only its scope. Dispatcher-owned
   workers use task-scoped lifecycle tools and report material progress.
   Block with evidence, the missing input and the smallest unblocking action.
4. **Recover.** Inspect card status, last heartbeat, run history, worker
   PID/session and workspace diff. Preserve logs and partial work before
   requeueing or reassigning; do not create concurrent writers. If only review
   failed, inspect the existing artifact first. Correct a faulty acceptance
   criterion and review against the correction rather than repeating done work.
5. **Close.** Recheck the artifact and actual command results against the card.
   Record the evidence and a nonempty result. A worker summary, stalled
   transition or partial result does not itself justify completion.

Use [discovery lanes](references/discovery-lanes.md) for read-only evidence
fan-out and [goal mode](references/goal-mode.md) for iterative card acceptance
or exhausted budgets.
