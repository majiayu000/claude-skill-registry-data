---
name: clickmax-team-members
description: Use when the user asks who is on the workspace team, how a specific teammate is doing (open opportunities, recent activity, last access), or needs to resolve a person to the right id before acting on their opportunities, tasks, files or shares.
---

## When this applies

Questions about PEOPLE of the workspace: the roster (roles, pending invitations, deactivated seats), one person's profile and work volume, and turning a name into the id another tool needs.

Not this skill:

- the team's task/appointment queue itself -> `clickmax-activities`
- assigning cards or routing rules -> `clickmax-pipelines`
- inviting, removing or changing a person's role/job roles -> web app only (Members screen); no tool does it

## Key assumptions

- one person, four ids — never interchange them:
  - user id = `id` in `mcp__plugin_clickmax_clickmax__workspace_members_list` = `userId` of `mcp__plugin_clickmax_clickmax__workspace_members_get`, `mcp__plugin_clickmax_clickmax__drive_people_get`, Drive shares/members = `personId` in `mcp__plugin_clickmax_clickmax__attendants_list`
  - attendant id = `attendantId` from `mcp__plugin_clickmax_clickmax__workspace_members_get` = `id` in `mcp__plugin_clickmax_clickmax__attendants_list` -> the only id `cards_list` / `tasks_list` / `activities_list` accept (`attendantIds`)
  - seat id = `seatId`, only identifies the seat
- `attendantId = null` (pending invitation, or management-only person) -> that person has no opportunities/tasks to look up; say so
- `status`: `pending` = invited, not accepted | `active` | `removed` = deactivated (reactivable in the app); people removed for good are not listed at all
- `role` owner | admin | member; `permissionGroups` = job roles, power = union; empty is normal for owner/admin, "reaches nothing" for a member
- profile `stats`: `opportunities` = OPEN cards where the person is the responsible attendant; `leads` = distinct contacts on them; `activities` = timeline actions in the last 8 weeks; `activitySeries` = 8 rolling 7-day buckets, oldest first, last = most recent 7 days
- permissions: roster needs `workspace` read; profile and `withStats` need `seats` read (403 otherwise) -> fall back to the plain roster and say the numbers need the Members permission

## Thought process

1. Name -> `mcp__plugin_clickmax_clickmax__workspace_members_list` with `search` (name, then e-mail if nothing). Several matches -> ask.
2. Headline about one person -> `mcp__plugin_clickmax_clickmax__workspace_members_get`; go deeper only with `attendantId` in the CRM tools.
3. Team comparison -> `mcp__plugin_clickmax_clickmax__workspace_members_list` with `withStats: true`, reading EVERY page `meta.countPages` reports (raise `perPage` to cut round-trips, never to skip pages) — not N profile calls. Compare only after the last page.

## Execute guide

- Roster: `mcp__plugin_clickmax_clickmax__workspace_members_list` (`status` to filter pending/active/removed; `meta.countItens` = total). Read every page `meta.countPages` reports before saying someone is missing.
- One person: `mcp__plugin_clickmax_clickmax__workspace_members_get` with `userId` -> role, member since, invited by, job roles, last access, stats.
- Their work: `attendantId` -> `mcp__plugin_clickmax_clickmax__cards_list` (`attendantIds`, `status = open`), `mcp__plugin_clickmax_clickmax__tasks_list` / `mcp__plugin_clickmax_clickmax__activities_list` (`attendantIds`, plus `overdue` for what is late).
- Their files: `mcp__plugin_clickmax_clickmax__drive_people_get` with the user id (numbers limited to what the caller can see).

## Report

- Person header: name, role, status, "no workspace desde" date, last access (or "sem acesso registrado").
- Work volume: open opportunities, contacts, actions in 8 weeks with the trend of the series (rising/falling, current week vs average); never invent targets.
- Roster: group by status (active, pending, deactivated), up to 20 names, `+N more`.
- Follow-up actions (reassigning cards, closing tasks) are opt-in only.

## Warnings

- `activities` in stats is timeline volume, not the tasks/appointments of `activities_list`; do not mix the two numbers.
- Stats only cover CRM work; automations, pages and funnels have no author tracking.
- A plain attendant session sees only its own items in the CRM tools even with another person's `attendantId`.

## Anti-patterns

- Passing a user id as `attendantIds`, or an attendant id as `userId`.
- Concluding "not in the workspace" from `attendants_list` alone (admins and pending invitations have no attendant profile).
- Calling `workspace_members_get` per row to rank a whole team.

---

Clickmax skill revision: `b8294822a4d6`
