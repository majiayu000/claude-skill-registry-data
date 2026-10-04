---
name: scope-management
category: pm
description: Use when defining a feature - name what is in scope, out of scope, and assumed, and handle mid-flight expansion without corrupting in-progress tasks
---
# Scope Management

## Overview

Scope is defended by what you write DOWN, especially the "out of scope" line. Undocumented scope drifts; a task whose AC quietly grows mid-flight is the classic cause of a blown estimate and a bounced UAT.

**Core principle:** Name the boundary explicitly. New scope becomes a new task, never an edit to an in-progress one.

## For every feature, write

- **In scope:** concrete deliverables in this iteration.
- **Out of scope:** explicitly named items deferred or excluded — this line does the real work.
- **Assumptions:** constraints treated as given.

TaskTrooper has no epic. For a single direct task, this lives in its own `description`. For a feature that spans several tasks via analiz, it lives on the **analiz task** (`description` or `add_task_document`) — never re-written per implementation task.

## Mid-flight expansion

When a request grows while work is in progress: **create a new task** for the expansion. Do NOT edit the AC of an in-progress task — a moving target invalidates the developer's plan and QA's scenarios and silently inflates the estimate.

**Except when the human changes the task themselves.** A comment the task's owner writes ON the task ("also show the logos in the marquee"), or their own edit of its description or criteria, is not mid-flight expansion to push back on — it is the task's requirement now. It outranks the original description and its out-of-scope list; every role builds, reviews, tests and accepts against it. Do not split it into a new task or treat it as creep unless the human asks for that.

## MoSCoW inside a feature

Must → this task's `acceptance_criteria`. Should/Could → separate backlog tasks, never folded into this one. Won't → the Out of scope line, with a reason (see backlog-prioritization).

## Dropping a criterion deliberately

Use `cancel_criterion` with a reason when a criterion is descoped, superseded by a later human comment, or moved to another task — never to get past work that simply wasn't done. `cancel_criterion` says "we're not shipping this here," which is a scope decision; a rejected `review_criterion` says "this doesn't work yet," which is a defect. Don't use one for the other.

## A new idea found during UAT

Something the PM or QA notices in pm_uat/human_uat that nobody asked for is a candidate for a new backlog task (`create_board_task`, priority low, same repository/project) — it is never a gap on the current task and never blocks its approval. Only something that breaks a criterion, a human comment, or the original request is a gap.

## Worked Example

Feature: "task export."
- In scope: CSV export of a project's tasks via the board UI.
- Out of scope: PDF export, scheduled/emailed exports, custom column selection.
- Assumptions: export is on-demand; ≤ 10k tasks per project.

Mid-sprint the stakeholder says "also email it weekly." That's the out-of-scope "scheduled export" — create a new task for it, keep the in-progress CSV task untouched, and tell the stakeholder it's queued separately.

## Common Mistakes

- Omitting the "out of scope" line → scope creeps by default.
- Editing an in-progress task's AC to absorb new asks.
- "We'll figure out scope later" → later is a UAT surprise.

## Red Flags

- A feature with an in-scope list but no out-of-scope list.
- An in-progress task whose AC changed after work started.
