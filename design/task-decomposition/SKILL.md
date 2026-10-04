---
name: task-decomposition
category: architecture
description: Use when an analiz task arrives in done (approved) - turn the approved split into implementation tasks with repository, AC, derived_from and ordering arguments
---
# Task Decomposition

## Overview

After the plan is written and self-reviewed, turn it into implementation board tasks with create_board_task. Decomposition quality decides whether developers can work in parallel without stepping on each other.

## Slicing Rules

- **One repository + one layer per task** (backend / frontend / mobile). Never bundle layers — a task that says "add the API and the UI" is two tasks.
- Each task maps to one or more plan tasks that form an independently deliverable unit: its tests can pass and its code can be reviewed without waiting for a sibling.
- Order by dependency: backend API before the frontend/mobile that consumes it. Declare it in the ARGUMENTS (see "Ordering is an argument" below), and write the human-readable "Depends on: <task title> — consumes POST /api/v1/..." line in the description as well — but never only the line, because prose enforces nothing.
- **New web frontend, no design system yet:** the first frontend task is "Add design system foundation" (tokens, atomic component folders + INVENTORY.md, base atoms, a layout template, ui-guard) and every page/section task is `blocked_by` it — nobody builds UI on a foundation that doesn't exist yet.
- **Size:** a task should land at an estimated ≤ ~400 changed lines including tests, so a reviewer sees the whole diff inside the 24,000-byte cut (review-reads-whole-diff); over ~1,000 is a split. Keep refactors in their own task, separate from feature work.
- **Shared files serialize:** two tasks in one repository that both add a migration (sequence numbers collide), or edit the same router table, locale bundle, DI container, `INVENTORY.md` or OpenAPI file, are chained with `blocked_by` rather than left to collide at review time.

## Each Task Must Contain

Each of these is a separate `create_board_task` field. Never paste one field's content into another — the board renders them in their own sections, and a duplicated copy goes stale the moment the real field is edited.

- **`title`:** action-object format ("Add task export endpoint", not "Export work").
- **`repository`:** required — name from `list_repositories`. Left out, the task falls back to the active repository context or the default repository, not necessarily this analiz task's or the one in your `split` table — a multi-repo split with this omitted on any task is how a web task lands in the backend workspace.
- **`project`:** the initiative this task belongs to, from `list_projects`, when the analysis names one.
- **`component`:** repository-relative path (e.g. `"services/api"`, `"."` for the root) when `repository` is a monorepo — scopes the task's required checks and brief. Check `list_repositories` for valid paths.
- **`priority`:** inherit the analiz task's priority unless the `split` table says otherwise.
- **`description`** (product only): user story ("As [persona], I want [capability], so that [outcome]") + context + which plan tasks it covers + the dependency line ("Depends on: …"). For a frontend UI task, also name the page/section and any responsive behaviour that is not obvious (e.g. "comparison table becomes stacked cards on phone").
- **`technical_description`** (technical only): the title of the analiz task's report (`analiz: …`) and the plan steps this slice implements (`#step-2`, `#step-3`), the endpoints/files/schema this slice touches, and the **interfaces** — the exact names/types it consumes from and produces for its neighbors, copied from the plan's Interfaces blocks. For a frontend UI task, also the components to reuse vs. create, by atomic level (atom/molecule/organism/template), with their names.
- **`acceptance_criteria`:** an array of strings, one observable Given/When/Then per item including error cases — copied or derived from the plan, never aspirational wording. Passing them as an array is what gives the task a real checklist; writing them as prose in `description` leaves it empty and the task can never be verified complete. **Product only:** a criterion is checked against the running system, never against the board — "moved to code_review", "PR opened", "QA notified", "the follow-up task is created" are workflow, and `create_board_task` drops them with the reason in its result.
- **`assignee`:** the matching developer role — backend-developer / frontend-developer / mobile-developer.
- **`derived_from`:** `["A-N"]` — the analiz task this slice came out of. REQUIRED on every task you create from an approved analysis. Your analysis report (spec and plan) is a document on that task and nowhere else; this reference is what feeds it into the developer's run and what makes `list_task_documents A-N` the answer when they need to re-read the plan. Naming the report's title in `technical_description` is not a substitute — a title is not a route.

## Ordering Is an Argument, Not a Sentence

Three orderings, three arguments, all pointing the same way — **this task comes after the ones you list**:

| Argument | Means | What enforces it |
|---|---|---|
| `blocked_by: ["T-1"]` | nobody starts this task until T-1 is done or released | the dispatcher parks the card in `blocked` with the reason on it, and picks it up automatically the moment T-1 lands |
| `deploy_depends_on: ["T-1"]` | this task may not be RELEASED until T-1 is live in production | the release gate refuses the deploy and comments why; the ordering is also written into this task's `before_deploy` runbook for you |
| a "Depends on: …" line in `description` | a human reading the card understands the shape | nothing |

- The backend task a frontend consumes is usually **both**: the frontend cannot be written before the contract exists, and it must not ship before the API does. Set both arguments.
- Two tasks that were developed in parallel and never blocked each other can still have a hard shipping order — that is `deploy_depends_on` alone.
- A cycle is refused at creation with the chain that causes it. If you hit one, the split is wrong: two tasks that each have to go first are one task.
- Anything that has to happen around the deploy — a migration to run first, a flag to flip, a cache to warm, how to undo it — goes in `before_deploy` / `after_deploy` / `rollback_plan` on the task that owns it. Those fields are posted on the card automatically when the release is dispatched and when it lands. A pre-deploy step written as a comment is one nobody sees at deploy time.

## Board Mechanics

Task creation happens ONLY after the human approves the analysis (see analiz-human-review-gate). The analiz task is in the `done` column when you run this — that column IS the approval signal.

1. Check for answered open questions before creating anything (`list_open_questions` if the context block doesn't already show them; open-questions-protocol). Apply every answer, and an unanswered non-blocking question's `recommended_answer`, to the tasks you create. If an answer contradicts the approved split or plan in a way this decomposition cannot absorb, create nothing — `add_task_comment` naming the conflict and stop.
2. create_board_task per slice, column=todo, with `assignee` set to the matching developer role (REQUIRED — an unassigned task is never dispatched and sits idle) and `derived_from` set to this analiz task. Call `list_team` to confirm the valid role names. Developers pick up their assigned tasks autonomously — no further human gate on implementation tasks.
3. Create them in dependency order — the producer first — so each dependent can name the task it waits for by key in `blocked_by` / `deploy_depends_on`. If you only realise an order after the fact, `update_board_task` with `blocked_by` adds it.
4. Putting every slice in `todo` at once is correct even when they are ordered: a task whose blocker is open is parked automatically and released the moment the blocker lands. Holding tasks back in `backlog` to fake an order is what the arguments replace.
5. add_task_comment on the analiz task listing every created task: title, assignee, project, and its order (what it waits for and what ships after it).
6. Move the analiz task to **released** — you are finished with it. (You never move it to `done`; the human does that as their approval action.)

## Red Flags

- Creating tasks while the analiz task is still in `analiz_review` → you skipped the human gate.
- A created task that comes back with an empty `acceptance_criteria` array → you wrote the criteria as prose; fix it with `update_board_task`.
- A created task that comes back with `dropped_criteria` → you wrote board steps as criteria; replace them with statements about the product, not with the same sentence reworded.
- A task whose AC mention two layers or two repositories.
- A task the assignee cannot start because an interface it consumes is defined nowhere.
- A created task with no `derived_from` → its developer has no route to your analysis report. `update_board_task` has no `derived_from` field — it is create-only and silently ignores one if you pass it. You also hold no `delete_board_task`, so you cannot delete and recreate it either: `add_task_comment` on that task immediately with "Spec and plan: `list_task_documents <this analiz task's key>`" so the developer has a route, and take care to set `derived_from` on every remaining `create_board_task` call this run.
- A created task whose `repository` differs from its row in the `split` table → it lands in the wrong developer's workspace; same immediate-comment workaround as above (`repository` is also create-only).
- An order that exists only as "Depends on: …" prose → nothing enforces it; add `blocked_by` / `deploy_depends_on`.
- A cycle refused at creation → your split is wrong, not the board. Merge the two tasks or move the shared piece into its own task that goes first.
- Moving the analiz task to `done` yourself → `done` is the human's approval move and `analiz_review` is the system's; you move it only to `released`.
- Decomposing while an open question's answer still contradicts the approved split — stop and comment instead (open-questions-protocol).
