---
name: pm-as-solo-orchestrator
category: pm
description: Use when planning a delivery request as the only orchestration agent - one board-writing subtask, backlog first, one approval question, then move approved tasks to todo
---
# PM as Solo Orchestrator

## Overview

When product-manager is the only enabled orchestration agent, the plan you write for a request is not a multi-agent handoff — it's one subtask that writes the board, followed by columns doing the rest of the work automatically.

**Core principle:** One subtask creates the tasks; the board, not the plan, drives every stage after that.

## Rules

- All subtasks are assigned to product-manager — never to system-architect, backend-developer, frontend-developer, mobile-developer, or qa-agent. Developer work goes through `create_board_task`, not an orchestration subtask.
- Multiple parallel PM subtasks are fine only when every one is read-only (e.g. web research + `list_board_tasks` concurrently). At most one subtask per parallel group may write to the board; a second board writer in the same group rejects the whole plan. Use `depends_on` to sequence when a later subtask needs an earlier one's result.
- Delivery stages (analiz, implementation, QA verification, pm_uat, approval) are board columns the task travels through afterwards — never plan a subtask per stage; that opens one board record per stage for a single piece of work and is rejected before the plan runs.
- Analiz tasks skip approval — they go straight to `todo` (investigation is always safe to start).
- Planner sets `ready=false` only when a product decision blocks creating any board task (max 3 questions, see stakeholder-intake's ask-vs-assume rule). Otherwise `ready=true`.

## Standard flow — one subtask, in order

1. Create the tasks in `backlog` (see implementation-task-spec, acceptance-criteria-gwt).
2. Call `ask_user`, choice mode:
   - `context`: what you asked / what you're assuming (name each assumption so the stakeholder can correct it cheaply) / the task list with assignee and order.
   - options: "Start all (recommended)", "Start only some", "Change something", plus whatever else applies.
3. On approval, move every approved task to `todo` with `move_board_task`. Order lives in `blocked_by` — never hold a task back in `backlog` to fake an order; a blocked task parks itself and starts automatically once its blocker lands.
4. On partial approval, move only the selected tasks; leave the rest in `backlog`.
5. On rejection or requested changes, `update_board_task` the affected fields, or `delete_board_task` + `create_board_task` for `assignee`/`derived_from` (creation-only fields) — and for `task_type` when `update_board_task`'s schema does not list it.
6. Report which tasks moved to `todo` (agents will pick them up) and which stay in `backlog`, and why.

This is ONE subtask calling these tools in order — not three subtasks. Splitting it hands the same board record to several agents that cannot see each other's writes.

If a blocking product decision remains, call `ask_user` within a subtask — never append questions as markdown in the final summary.

## Common Mistakes

- A subtask per delivery stage instead of one subtask that creates the tasks.
- Holding implementation tasks in `backlog` "until analiz is done" instead of using `blocked_by` — the board already enforces that order.
- Two parallel subtasks writing to the board in the same group.
- Approval-question `context` that doesn't separate what you asked from what you assumed.

## Red Flags

- A plan with a subtask named "QA stage" or "pm_uat review" — those are columns, not subtasks.
- More than one board-writing subtask in a parallel group.
- A task left in `backlog` with a "Depends on: …" sentence instead of `blocked_by`.
