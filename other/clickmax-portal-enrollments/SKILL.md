---
name: clickmax-portal-enrollments
description: Use when the user wants to list, add, bulk add, or remove member enrollments at the portal level in Clickmax Members.
---

## When this applies

Use this skill for portal-scoped enrollment operations: list members in a portal, add one, bulk add many, or remove a member from that portal.

Not this skill:

- member-user identity/progress/access lifecycle -> `clickmax-members`
- portal container administration -> use the direct portal tools

## Key assumptions

- portal enrollment does not auto-enroll classrooms
- this is the portal-side inverse of member-user portal assignment
- bulk add returns aggregate counts plus per-member errors
- removal from a portal cascades classroom enrollments within that portal

## Thought process

1. Resolve the intended portal.
2. Distinguish one-off enrollment from bulk audience mutation.
3. Confirm removal intent when ambiguity exists because it cascades inside the portal.

## Execute guide

- Inspect current membership with `mcp__plugin_clickmax_clickmax__portal_members_list`, passing `portalId` and the needed pagination or filters such as `page`, `perPage`, `search`, and `active`.
- Add one known member with `mcp__plugin_clickmax_clickmax__portal_members_add`, passing `portalId` and `memberUserId`.
- Add a resolved cohort with `mcp__plugin_clickmax_clickmax__portal_members_bulk_add`, passing `portalId` and the `memberUserIds` list.
- Remove one member with `mcp__plugin_clickmax_clickmax__portal_members_remove`, passing `portalId` and `memberUserId`.
- Make the removal cascade explicit: removing portal membership also removes classroom enrollments inside that same portal.

## Report

- Start with the portal assumption used.
- For lists, report the cohort as portal members ordered by the tool response and summarize active/search filters.
- For bulk add, report added count first, then skipped/error counts, then the most relevant per-member failures; use `+N more` if the failure list is long.
- For removals, state that classroom enrollments inside the same portal were also removed.
- Offer follow-up mutation only when the user asks for it.

## Warnings

- Removing from a portal also removes classroom enrollments inside that portal.
- Portal membership is not the same as course/classroom assignment.

## Anti-patterns

- Telling the user a portal add will automatically enroll classrooms.
- Bulk-enrolling an unresolved cohort without clarifying scope.

---

Clickmax skill revision: `b8294822a4d6`
