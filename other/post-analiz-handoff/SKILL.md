---
name: post-analiz-handoff
category: pm
description: Use when the stakeholder asks about an analysis outcome or its implementation tasks - understand the human approval gate and review the tasks the architect created once the human approved
---
# Post-Analiz Handoff

## Overview

The analiz has a human approval gate. The system-architect does NOT create implementation tasks when it finishes analysis — it presents the plan in the `analiz_review` column, the human approves it, and only then does the architect create the tasks. Your job is to understand this sequence and review the tasks after they appear, not to create them.

## The sequence (who does what)

1. **Architect** writes the spec/plan and moves the analiz task to `analiz_review`, then stops.
2. **Human** reviews the plan in `analiz_review` and moves it to `done` (approve) or `need_revision` (reject). This is the human's decision, not yours — do not move an analiz task out of `analiz_review`.
3. **Architect** (on approval) creates one implementation task per project, lists them in a comment, and moves the analiz task to `released`.

## Your steps

Trigger: the stakeholder asks what an analysis found, or about the tasks it produced. **The board never dispatches you here on its own** — the PM is subscribed only to `pm_uat`, so this skill only runs when a human brings it up in chat.

1. `list_board_tasks` to find the implementation tasks the architect created.
2. Read the architect's spec/plan with `list_task_documents` on the ANALIZ task — they are documents attached to it, never committed to the repository — and read the task comments.
3. Check each created task carries `derived_from` pointing at the analiz task. `update_board_task` **cannot set `derived_from`** — it has no such field and silently ignores it. If the task has not started (backlog/todo/blocked), `delete_board_task` + `create_board_task` it with `derived_from` set, keeping its title, fields and criteria. If work has already started, `add_task_comment`: "Spec and plan: `list_task_documents A-N`" — so the developer can still reach them without touching a task mid-flight.
4. Check the order is declared, not just described. A frontend task that consumes a new endpoint should carry `blocked_by` and `deploy_depends_on` naming the backend task; a "Depends on: …" sentence in the description enforces nothing. `update_board_task` CAN add to `blocked_by`/`deploy_depends_on` (it adds to whatever is already there) — use it for tasks still in backlog/todo/blocked.
5. If stakeholder decisions were logged as questions during analysis, confirm answers exist.
6. Review scope and priority. Edit acceptance criteria with `update_board_task` only on tasks still in `backlog`/`todo`/`blocked` — it replaces the whole array and resets every tick. On a task that has started, use `cancel_criterion` to drop one, or open a new task for added scope (see scope-management); never duplicate or re-create the architect's tasks.
7. Tell the stakeholder which implementation tasks are queued, in what order, and what happens next. A task sitting in `blocked` because its blocker is still open is on schedule, not stuck — it is picked up automatically.

## Common Mistakes

- Creating implementation tasks yourself — the architect owns decomposition, gated on human approval.
- Moving an analiz task from `analiz_review` to `done` — that is the human's approval action.
- Expecting the tasks to exist as soon as the analiz hits `done` — they appear after the architect releases the analiz.
- Trying to fix a missing `derived_from` with `update_board_task` — it silently ignores the field; delete and recreate instead.
- Editing acceptance criteria on a task already in `in_progress` or later — it resets every tick the developer made.

## Red Flags

- You are about to `create_board_task` for work the architect analyzed → stop; the architect creates it after approval.
- You moved an analiz task out of `analiz_review` → that is the human's decision.
- You called `update_board_task(derived_from=...)` expecting it to take effect → it won't; delete + recreate instead.
