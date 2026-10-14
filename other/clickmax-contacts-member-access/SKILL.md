---
name: clickmax-contacts-member-access
description: Use when the user wants to give a whole group of CRM contacts (a list, a segment, a filtered selection) access to a community and/or classrooms of the members area in Clickmax.
---

## When this applies

Use when the audience is defined in the CRM (contacts, a list, a segment, a filter) and the goal is to enroll them in the members area: a community with a role, classrooms (which carry their area and their courses), or both.

Not this skill:

- people who are ALREADY members (progress, disable/enable, extend access, remove from a classroom, send the access link) -> `clickmax-members`
- portal-level enrollment of known member users -> `clickmax-portal-enrollments`
- building the audience itself -> `clickmax-list-segments` / `clickmax-leads`

## Key assumptions

- Destinations: `classroomIds` (max 50) and/or `communityId` + `communityRole` (`member`, `moderator`, `mentor`, `instructor`, `owner` = the Administrador role). At least one destination; a community without role is a 400. Ids come from `classroom_list` (per portal) and `communities_list`; never from names.
- Audience: `leadIds` OR `allMatching: true` with a `listId` (manual list or the synced list of a segment) or `filters`. A segment is reached through its synced list; a just-created segment may not have one yet.
- The e-mail is the member login: contacts WITHOUT e-mail are skipped and reported as `skippedWithoutEmail`, everyone else is enrolled (a disabled member is reactivated).
- Per-contact effects: classroom access follows the classroom's own access time (none = lifetime); courses locked for sale inside the classroom stay locked (purchase-only); in the community a new member gets the chosen role, an existing member is moved to it EXCEPT administrators (never demoted), and blocked/muted members stay blocked/muted.
- It only grants: no access e-mail is sent, nothing is revoked, and re-running for the same contacts and destinations duplicates nothing and does not restart access windows.
- Sync up to 200 contacts (`{ mode: "sync", affected, skippedWithoutEmail }`), async above it (`{ mode: "async", jobId }`): an async answer means nothing was granted yet.

## Thought process

1. Resolve the destination ids, then the audience; confirm the community role when the user did not name one (`member` is the safe default, `owner` is admin power).
2. Size the audience first when it is a filter (`segments_preview_count`) — a broad filter enrolls broadly.
3. One call does the whole audience; do not loop per contact.

## Execute guide

- Resolve a classroom with `mcp__plugin_clickmax_clickmax__portals_list` then `mcp__plugin_clickmax_clickmax__classroom_list` (`portalId`); a community with `mcp__plugin_clickmax_clickmax__communities_list` (`search`).
- Resolve the audience: `mcp__plugin_clickmax_clickmax__lists_list` / `mcp__plugin_clickmax_clickmax__segments_list` for the `listId`, or `leadIds` from `mcp__plugin_clickmax_clickmax__leads_search`.
- Grant with `mcp__plugin_clickmax_clickmax__leads_bulk_member_access`. Async answer: poll `mcp__plugin_clickmax_clickmax__leads_bulk_job_status` with `jobId` until `state` is `completed` (or `failed`, with `failedReason`).

## Report

- Destination(s) by name, audience size, `affected`, and `skippedWithoutEmail` when above 0 (with the fix: fill the e-mail on the contact and re-run).
- Async: say the enrollment is running and report `progress` from the job status; only call it done when `state` is `completed`.
- Remind the user that no access e-mail was sent and offer the send-access-link operation of `clickmax-members`, without doing it.

## Warnings

- Giving the `owner` role in a community to a whole list hands out admin power; confirm it explicitly.
- Do not promise a locked-for-sale course was unlocked, or that an administrator's role changed.

## Anti-patterns

- Enrolling contacts one by one when a list/segment/filter describes them.
- Reporting an async answer as done.
- Using this for people already enrolled to extend, disable or remove them (use `clickmax-members`).

---

Clickmax skill revision: `b8294822a4d6`
