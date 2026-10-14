---
name: clickmax-activities
description: Use when the user asks about the team's Activities queue (follow-up tasks and booked appointments together), such as what is late, what is scheduled for a day or week, workload per attendant, closing a batch of them, or setting up a multi-step follow-up cadence with automatic WhatsApp steps on an opportunity.
---

## When this applies

Use for the Activities screen's data: the ONE queue of follow-up tasks (a reminder with a deadline, hung on an opportunity card) plus booked appointments (a real slot with start and end). Typical asks: late items, a day/week/month view, workload of an attendant or pipeline, finding an item by contact e-mail or phone, closing a selection.

Not this skill:

- the raw event timeline of a contact or card (things that happened) -> `clickmax-leads-activity-analysis`. Same word, different thing: that is an event log, this is work someone owes or booked
- creating an appointment, or editing one appointment's details -> the `scheduled_calls_*` operations (`clickmax-pipelines` covers the card side); follow-up tasks and cadences ARE covered below
- pipeline/kanban analytics -> `clickmax-pipelines`

## Key assumptions

- `mcp__plugin_clickmax_clickmax__activities_list` items are `{ kind: task | appointment }` with the FULL row of each side; ids of tasks and appointments live in different tables, so identify an item by `kind` + id, never id alone
- `types` mixes both worlds: `call`, `whatsapp`, `meeting`, `task` are TASK types; `appointment` is a booked appointment
- `buckets`: `ongoing` = task open/scheduled or appointment scheduled/confirmed; `done` = task resolved/cancelled or appointment completed/cancelled/no_show
- filters are ANDed. `priorities` and `withoutDeadline` exist only on tasks: filling either EXCLUDES appointments from the result
- date range = task DEADLINE and appointment START. Tasks without a deadline match no range; `withoutDeadline = true` adds them (and drops appointments)
- LATE (`overdue = true`) = still ongoing and its END has passed (task deadline + its duration; appointment end). An all-day task is late only after its day ends. Send the caller clock (`overdueBefore` = now, `allDayStart` = today at local midnight); without it the server uses its own now and all-day tasks due today can be miscounted
- `search` matches task title/description, appointment subject/notes, card title, pipeline, attendant AND the contact name, e-mail or phone (a pasted formatted phone works)
- items of LOST or deleted opportunity cards are excluded; an appointment with no card is included
- a plain attendant only ever gets its OWN items (the filter is overridden); owner/admin see the team and can filter by `attendantIds` (+ `includeUnassigned`, ORed)
- `mcp__plugin_clickmax_clickmax__activities_summary` = `{ total, ongoing, done, overdue }` for the same filters; its task overdue can be lower than `tasks_summary.overdue` (that one compares the bare deadline)
- `mcp__plugin_clickmax_clickmax__activities_calendar` needs `startDate`, `endDate`, `timeZone` (IANA) and `perDay`; it caps items PER DAY, returns only days with activity, and `total` is the real day count. Tasks without deadline never appear there
- there is no bulk endpoint: a batch is one call per item
- automatic follow-up = a `whatsapp` task with `automation` and a deadline: the system sends it to the card's primary contact at the deadline. Sent → task resolved by itself; failed → `automation.status = failed` + reason, task stays OPEN for a person. `stopOnReply` (default on) cancels pending automatic steps when the contact writes on any channel; the task stays as a manual one
- 24h WhatsApp window is checked AT SEND TIME: free text (`message`) only reaches a contact who wrote in the last 24h then; a step days ahead needs an APPROVED template (`templateId` + one value per `positionParams` label)

## Thought process

1. Counting or ranking question -> `activities_summary` (numbers) before `activities_list` (rows).
2. "What is on day/week X" -> `activities_calendar` for the grid; `activities_list` with that range when the full rows of one day matter.
3. "Late" always means the rule above: use `overdue = true` + the clock, not a date range up to now.
4. Batch close/cancel is a write on many people's work: confirm the exact selection first.

## Execute guide

- Headline: `mcp__plugin_clickmax_clickmax__activities_summary` with the filters (attendant, pipeline, range, types). Do not pass `overdue = true` unless the whole selection should be only late items.
- Rows: `mcp__plugin_clickmax_clickmax__activities_list` (keep `perPage` small — appointment rows are heavy; default 10, max 2000; when `meta` says there are more pages and the answer needs the full set, consume every page). Ordered earliest due/start first, no-deadline last.
- Calendar: `mcp__plugin_clickmax_clickmax__activities_calendar` with a range, the user's IANA `timeZone`, and `perDay` (a month cell needs few, a single day can take up to 200). When a day's `total` exceeds its items, read that day with `activities_list` and a one-day range.
- Find an item by contact: put the e-mail, phone or name in `search`; combine with `types` or `buckets = ongoing` to narrow.
- Close a batch, per item after the selection is confirmed: TASK done -> `mcp__plugin_clickmax_clickmax__tasks_update` with `status = resolved`, `outcome = true`; TASK not done -> same with `outcome = false` and the reason in `outcomeNote`; APPOINTMENT done -> `mcp__plugin_clickmax_clickmax__scheduled_calls_update` with `status = completed`; APPOINTMENT cancelled -> `mcp__plugin_clickmax_clickmax__scheduled_calls_cancel` with `reason` (this also e-mails the participants and removes the calendar event). Run them a few at a time, keep going past a failure (an item outside the caller's scope answers not-found), and report succeeded vs failed.
- Only `ongoing` items are worth closing; `done` ones already have an outcome.
- **Follow-up cadence** ("WhatsApp now, call tomorrow, WhatsApp again in 3 days"): resolve the card (`clickmax-pipelines`), the attendant (`attendants_list`) and, for automatic steps, a live number with `mcp__plugin_clickmax_clickmax__channel_instances_list` + an approved template of THAT number with `mcp__plugin_clickmax_clickmax__gupshup_templates_list` (check `positionParams`). Then ONE call to `mcp__plugin_clickmax_clickmax__tasks_create_cadence`: `steps` 1-20, `waitMinutes` CUMULATIVE from `startAt` (gap since the previous step, not an absolute date), automatic steps need `type = whatsapp`. All-or-nothing: an invalid step or an unreachable number/template saves nothing. Confirm steps, texts and timing with the user before creating — automatic steps message the contact later with nobody clicking.
- Cancel ONE automatic step: `mcp__plugin_clickmax_clickmax__tasks_update` with `automation = null` (task stays as manual). Already `sent`/`running` cannot be changed (409). A single automatic task: `mcp__plugin_clickmax_clickmax__tasks_create_cadence` with ONE step — `tasks_create`, `tasks_update` and the batch tool never arm an automatic send, so every automatic WhatsApp goes through the user's approval.
- Preferred order: summary -> list/calendar -> (confirm) -> per-item close -> re-read summary.

## Report

- Open with the scope assumed: whose items (own vs team, attendant), range and timezone, types.
- Lead with the numbers (`ongoing`, `overdue`, `done`), then the worst offenders: oldest late items first, with contact, attendant, pipeline and how late.
- Group by day for calendar answers; state when a day is truncated (`+N more`).
- For a batch close: selection size split by kind (tasks vs appointments), then succeeded/failed, then any item left open and why.
- For a cadence: list the steps with their computed date/time, channel and whether each is automatic or a manual reminder; then the `cadenceId`.
- Follow-up writes are opt-in only.

## Warnings

- Cancelling an appointment notifies its participants; closing a task as not done records the reason on the card. Neither is silent.
- A failed automatic step does not retry; it is a visible open task with the reason. Free-text automatic steps far in the future are the usual cause (outside the 24h window).
- Mixed selections mean different things per kind: "done" is a positive outcome for a task and status completed for an appointment; say so before acting.
- `mcp__plugin_clickmax_clickmax__activities_list` does not include items whose opportunity is lost or deleted; if a count looks short, that is a likely reason.
- A plain-attendant session cannot see or close colleagues' items.

## Anti-patterns

- Using a date range "up to now" instead of `overdue = true` to find late items.
- Answering a headline question by paging rows.
- Closing a batch without confirming the selection, or stopping at the first failed item.
- Treating the contact event timeline as this queue (or the reverse).
- Reading a truncated calendar day as the full day.

---

Clickmax skill revision: `b8294822a4d6`
