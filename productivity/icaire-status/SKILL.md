---
name: icaire-status
description: Fetch the authenticated ICAIRE member's tasks from the remote brain and summarize status across open, waiting, blocked, and recently completed work. Use when the user asks for task status, wants an overview of all their ICAIRE tasks, asks what is blocked, or wants a progress snapshot.
---

# ICAIRE Status

Fetch the current member's ICAIRE tasks from the remote brain and summarize the
state of their work.

## Contract

- Use ICAIRE Cortex MCP, not local TODO files.
- Start with `me`. If the authenticated user is not an active member, stop and
  explain that ICAIRE membership must be configured before task status works.
- Fetch tasks with `tasks/list` using `assignee: me`.
- Check at least `open`, `waiting`, and `blocked`. Include `done` only when the
  user asks for completed/recently completed work or a full history.
- When task records include `readiness`, use it to split open tasks into
  `Ready` and `Needs input`.
- Prefer slash tool names; use underscore aliases only if needed.
- Output the status in chat. Do not write a file unless explicitly asked.

## Workflow

1. Call `me` and confirm `member.person_slug` exists.
2. Call `tasks/list` for `assignee: me` and each active status:
   - `open`
   - `waiting`
   - `blocked`
3. If the user asks for completed work, also call `tasks/list` with
   `status: done`.
4. Group tasks by status, then order by priority, due date when available, and
   task order returned by the server.
5. For thin or unclear tasks, read linked `source_slugs` only when needed to
   explain the status accurately.
6. Identify:
   - ready tasks the user can act on now, using `readiness: ready` when present
   - tasks needing input, using `readiness: underspecified` when present
   - waiting tasks and what they appear to be waiting for
   - blocked tasks and the blocking condition
   - high-priority items
   - stale or unclear tasks that need clarification

## Output Requirements

- Start with `Task status`.
- Include a concise summary count by status.
- Then show sections in this order:
  - `Ready`
  - `Needs input`
  - `Waiting`
  - `Blocked`
  - `Done` only when requested
  - `Needs clarification` only when readiness is absent and the task is too
    unclear to classify.
- For each task, include title or human-readable action, priority when useful,
  and the next visible action or blocking reason.
- Do not include task slugs unless the user explicitly asks for paths/slugs or
  two tasks would otherwise be ambiguous.
- For `Needs input`, include the blocking question(s), preferring the task
  page's `## Open Questions` section when present.
- Keep the report scannable; prefer concise bullets over long task bodies.
- End with `Recommended focus` listing the top 1-3 tasks to handle next.

## Guardrails

- Do not invent tasks if `tasks/list` returns none.
- Do not show other members' tasks when the user asked for their own status.
- Do not silently fall back to all tasks when `me` cannot resolve.
- Do not mark tasks done, create tasks, or change status unless explicitly
  asked.
- Do not treat external people as assignable members.
