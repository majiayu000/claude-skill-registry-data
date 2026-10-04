---
name: icaire-plan-standup
description: Prepare a concise ICAIRE standup run-through from the authenticated member's recent task timeline updates, completed work, blockers, and follow-up context. Use when the user asks what they achieved in the last 24 hours, wants to plan a standup update, needs a daily progress rundown, or asks what to say in a check-in.
---

# ICAIRE Plan Standup

Prepare a short, evidence-backed standup run-through for the current ICAIRE
member, focused on recent progress they can credibly mention and what they
should do next.

## Contract

- Use ICAIRE Cortex MCP, not local TODO files.
- Start with `me`. If the authenticated user is not an active member, stop and
  explain that ICAIRE membership must be configured before standup planning
  works.
- Treat the default window as the last 24 hours from the current local time
  unless the user gives a different window.
- Fetch tasks with `tasks/list` using `assignee: me`.
- Check `done`, `open`, `waiting`, and `blocked`.
- Treat recent timeline entries on any assigned task as progress evidence, even
  when the task is still open.
- Prefer timeline entries attributed to the authenticated actor. If attribution
  is unavailable, use timeline date and task assignment as evidence, and state
  uncertainty only when it materially affects the standup.
- Prefer slash tool names; use underscore aliases only if needed.
- Output the run-through in chat. Do not write a file unless explicitly asked.
- Do not create, close, update, or reassign tasks unless explicitly asked.

## Workflow

1. Call `me` and confirm `member.person_slug` exists.
2. Determine the reporting window:
   - default: last 24 hours
   - if the user says "today", use the current local calendar day
   - if the user gives a date range, use that exact range
3. Call `tasks/list` with `assignee: me` and `status: done`.
4. Filter completed work to the reporting window when task timestamps, timeline
   entries, or completion notes make that possible.
5. Call `tasks/list` for `assignee: me` and each active status:
   - `open`
   - `waiting`
   - `blocked`
6. Scan task timeline entries across returned `done`, `open`, `waiting`, and
   `blocked` tasks for entries inside the reporting window:
   - Count matching entries as progress, not merely possible mentions.
   - Prefer entries that include the authenticated actor's email/name.
   - Include open-task updates when they show scope changes, deployment,
     verification, handoff, meetings completed, or new implementation context.
   - Do not require a task to be completed before mentioning concrete progress.
7. Read linked `source_slugs` only when a task title/body is too thin to explain
   what was achieved or why it matters.
8. Build a standup run-through that separates progress, blockers, and next
   steps without exposing internal task paths unless the user asks for them.

## Output Requirements

- Start with `Standup run-through`.
- Include the reporting window as an absolute time range when known.
- Use exactly three short bullet lists:
  - `Progress`: recent timeline-backed updates and completed work. Name the
    work in plain language; do not include relative task paths by default.
  - `Blockers`: blocked/waiting items and visible reasons. If none are present,
    include one bullet saying there are no recorded blockers.
  - `Next steps`: the top 1-3 concrete next actions to mention as planned focus.
- Keep the output practical and short enough for a real standup.
- If there are no confirmed achievements, say that directly and surface the
  nearest relevant progress or active focus without pretending it was completed.

## Guardrails

- Do not invent achievements from open tasks.
- Do not ignore authored timeline updates just because the parent task remains
  open.
- Do not include other members' work unless it is clearly tied to the user's
  task or the user asks for a team standup.
- Do not silently fall back to all tasks when `me` cannot resolve.
- Do not overstate uncertain timing; keep wording modest when attribution or
  dates are incomplete.
- Do not treat external people as assignable members.
