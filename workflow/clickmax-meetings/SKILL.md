---
name: clickmax-meetings
description: Use when the user wants to book, reschedule, hand over to another attendant, cancel or look up one booked meeting (agendamento) of a contact in Clickmax.
---

## When this applies

Use for ONE booked meeting at a time: book it for a contact, move it in time, give it to another attendant, close it out (completed / no-show), cancel it, fetch its self-service link, or find meetings by who conducts or who booked them.

Not this skill:

- the team queue of tasks and meetings together, workload, or closing a batch -> `clickmax-activities`
- a follow-up reminder with a deadline (a task, not a slot) -> the task operations; card side in `clickmax-pipelines`
- meeting KPIs: show rate, no-show, self booking, who books x who conducts -> `clickmax-insights-dashboards`
- writing the sales method a meeting follows -> `clickmax-playbooks`

## Key assumptions

- A meeting has TWO people: the attendant who CONDUCTS it (`attendantId`) and the one who BOOKED it (`createdByAttendantId` as a filter, `createdByAttendantName` in the row). They are independent: "meetings Helena scheduled" is the booker filter, "Helena's agenda" is the conductor filter. Public booking, automations and calendar sync have no booker.
- Booking is validated, not a blind insert. With an attendant the window must be inside their agenda (or the chosen agenda), their seat role must accept meetings, and it must not overlap another meeting of theirs. Two explicit overrides exist — off-hours (`allowOutsideAvailability`) and overlap (`allowConflict`); use them only when the user asked for that exact time. A booking with NO attendant, agenda or member skips all of it and lands unassigned.
- Rescheduling and handing over are PATCH edits of the same row: new time and/or new `attendantId`. The new time/attendant is re-checked for agenda availability (overridable), but the edit does NOT check overlap with other meetings — look at the new conductor's day first when a clash matters.
- `attendantId` can be changed but never cleared. A handover moves the calendar event to the new attendant's calendar and, when the meeting has a video room, makes them its host. The calendar copy is best-effort: the meeting can be right in Clickmax while the external calendar lags.
- The method the meeting follows is `playbookId`: omitted on booking = the default of the linked card's pipeline (none without a card), `null` = no method, an id = that one. Changing the card later never changes it. Ids come from `playbooks_list`.
- Cancelling keeps the record (status cancelled, reason stored, calendar event removed); it stays in listings. Do not cancel by setting `status` on the patch. `completed`, `no_show` and `confirmed` are set with the patch; a written result goes in `outcomeNote`.
- A plain attendant session only sees and edits its own meetings and those of its pipeline peers.
- The lead-facing self-service link (`scheduled_calls_manage_link`) lets the CONTACT reschedule, cancel or join; sending it is the user's decision, not a default.

## Thought process

1. Resolve the people first: the contact (`leads_search`) and the attendants (`attendants_list`); never guess ids from names.
2. Classify the ask: book / move in time / hand over / close out / cancel / look up. Only booking needs a contact; the rest need the meeting id from `scheduled_calls_list`.
3. If the ask changes who or when for SEVERAL meetings, do it one by one and confirm the exact list first; there is no bulk edit here.
4. Any change that moves a meeting the contact already knows about (time, person) is worth a confirmation before it is sent.

## Execute guide

- Book: `mcp__plugin_clickmax_clickmax__scheduled_calls_create` with `leadId`, `startAt`, `endAt` and one of `attendantId` | `appointmentScheduleId` | `memberId`; add `opportunityCardId` when the meeting belongs to a deal. A refusal about slot or overlap is information for the user (that time is not free), not something to retry with an override on your own.
- Look up: `mcp__plugin_clickmax_clickmax__scheduled_calls_list` with `attendantId` (conducts), `createdByAttendantId` (booked), `status`, a `startDate`/`endDate` window; `mcp__plugin_clickmax_clickmax__scheduled_calls_get` for one row with booker, agenda, method, card/pipeline and, once processed, recording insights and summary.
- Reschedule: list the conductor's meetings around the new window, then `mcp__plugin_clickmax_clickmax__scheduled_calls_update` with `id`, `startAt`, `endAt` (send both).
- Hand over: check the new attendant is operational and free (`attendants_list`, `scheduled_calls_list` with their `attendantId` on that day), then `mcp__plugin_clickmax_clickmax__scheduled_calls_update` with `id` + `attendantId`. Send `allowOutsideAvailability` only if the user explicitly accepts an off-hours handover.
- Close out: `mcp__plugin_clickmax_clickmax__scheduled_calls_update` with `status: "completed"` or `"no_show"` and, when the user dictates a result, `outcomeNote`.
- Cancel: `mcp__plugin_clickmax_clickmax__scheduled_calls_cancel` with an optional `reason`.

## Report

- After booking: contact, day/time (with time zone as the user knows it), conductor, agenda/method if set, whether a calendar sync or confirmation e-mail went out, and any override that was used.
- After a move or handover: before -> after (time or person) and whether the external calendar was updated or is lagging.
- For lookups: a short list (day, time, contact, conductor, booker, status), up to 10 rows unless the user asked for everything (then list all); when rows are left out, say how many (`+N more`) and offer to continue.
- Mutations beyond what the user asked (sending the self-service link, cancelling, overriding a slot) are offered, never done.

## Warnings

- "No slot / clash" answers are the system protecting the agenda; overrides book on top of real commitments.
- A patch never checks overlap: a successful handover or reschedule does not prove the new time is free.
- Meetings of a lost or deleted card are hidden from listings unless explicitly included.

## Anti-patterns

- Filtering by conductor to answer "who booked" (or the reverse).
- Booking without naming any attendant, agenda or member.
- Setting `status: "cancelled"` on the patch instead of cancelling.
- Retrying a refused booking with `allowConflict` / `allowOutsideAvailability` the user never approved.
- Looping over a batch without showing the list first.

---

Clickmax skill revision: `b8294822a4d6`
