---
name: icaire-roadmap-tasks
description: Suggest and create ICAIRE roadmap tasks from remote brain progress, member responsibilities, blockers, and open questions. Use when the user asks what tasks should be added next, wants a roadmap-to-task pass, or wants ICAIRE next actions generated from the brain.
---

# ICAIRE Roadmap Tasks

Use the remote ICAIRE brain to turn current progress and gaps into assignable
task pages.

## Contract

- Use ICAIRE Cortex MCP for all current context.
- Prefer direct task creation when a recommendation is concrete, useful, and
  assignable to an active member.
- Use `me`, `members/list`, `tasks/list`, `tasks/create`, and `tasks/update`
  when available; use underscore aliases only if slash tool names fail.
- Before creating or updating task pages, call ICAIRE MCP `filing_rules` and
  follow the compiled `FILING.md` guidance it returns. If that tool is
  unavailable, list and read the relevant `FILING.md` files directly; do not
  expect a page named `filing_rules` to exist.
- Do not assign work to arbitrary `people/*` pages. Assignees must be active
  members.
- Keep roadmap reasoning grounded in retrieved ICAIRE pages.
- Before marking any task `done` or `archived`, either create or link the
  successor task and use `Next task: tasks/<slug>` in the timeline entry, or
  state `No successor task needed: <reason>`.

## Workflow

1. Call `me` and `members/list` to identify the requester and active members.
2. Retrieve current context:
   - `filing_rules` for current task-page and routing conventions
   - `tasks/list` for existing open, waiting, and blocked tasks
   - `query` or `search` for initiatives, ops roadmaps, blockers, recent
     meetings, and inbox questions
   - direct `read` on the most relevant pages
3. Identify task candidates:
   - overdue or blocked follow-ups
   - unowned open questions that should become work
   - initiative next steps that are concrete enough to assign
   - dependencies or risks that need active resolution
4. Deduplicate against existing task pages.
5. Create task pages with `tasks/create` when each task has:
   - a clear title
   - status, priority, and source links
   - one or more active member assignees
   - a body that explains why the task exists and what good completion means
6. When closing an existing task, create or identify the next concrete task
   first unless no successor is needed, then include the completion handoff in
   `tasks/update`.
7. Leave non-actionable or unassignable ideas as recommendations only.
8. Verify created tasks with `tasks/list` or direct `read`.

## Output

Return:

- `Created Tasks`: task slugs, assignees, priority, and source
- `Suggested But Not Created`: reason each item was not created
- `Existing Tasks Considered`: relevant duplicates or blockers
- `Verification`: checks performed

## Guardrails

- Do not create speculative tasks that are not grounded in the brain.
- Do not rewrite roadmap or initiative pages unless the user explicitly asks.
- Do not hide missing ownership; report it.
- Do not assign everything to `me` unless the brain or user context supports it.
- Do not bypass the MCP `filing_rules` tool by guessing from stale local
  conventions or by reading a nonexistent `filing_rules` page.
