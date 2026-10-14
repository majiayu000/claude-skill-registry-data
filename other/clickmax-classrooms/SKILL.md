---
name: clickmax-classrooms
description: Use when the user wants to list, inspect, create, update, link content to, copy members between, or delete classrooms inside Clickmax member portals.
---

## When this applies

Use this skill for classroom/container operations inside portals: list/get/details/create/update classrooms, add content to a classroom, copy members from another classroom, or delete a classroom.

Not this skill:

- portal-wide administration -> use the direct portal tools
- member-user lifecycle/enrollment detail -> `clickmax-members`

## Key assumptions

- classrooms are portal-bound for life
- `classroom_details` is the rich inspection call because it includes contents and lessons
- adding content is idempotent for the same course/content
- deleting a classroom removes enrollments and content links, but members can still retain portal access

## Thought process

1. Resolve the classroom and its parent portal first.
2. Distinguish inspection from content-linking from membership-copy operations.
3. Confirm destructive delete when intent is not already explicit.

## Execute guide

- Use `mcp__plugin_clickmax_clickmax__classroom_list` with the portal id first when the user gives only portal context.
- Use `mcp__plugin_clickmax_clickmax__classroom_get` with the classroom id for basic identity or status checks.
- Use `mcp__plugin_clickmax_clickmax__classroom_details` with the classroom id before editing content or copying members so you can inspect linked contents and lesson structure.
- Use `mcp__plugin_clickmax_clickmax__classroom_create` with the destination portal id, the classroom name, the initial `contentsIds`, and any `contentsAccessTime` entries when the classroom should start with pre-linked content.
- Use `mcp__plugin_clickmax_clickmax__classroom_update` with the classroom id plus only the fields that should change. Common patterns: rename the classroom with `name`; add timed content with `contentsToAdd` entries carrying `contentId`, `accessDuration`, and `accessUnit`; remove linked content with `contentsIdsToRemove`.
- Use `mcp__plugin_clickmax_clickmax__classroom_add_content` with `id` (the classroom's own id — NOT `classroomId`) and `contentId` when the user wants to link one existing content item without a broader classroom update.
- Use `mcp__plugin_clickmax_clickmax__classroom_copy_members_from` with confirmed `sourceId` and `targetId` only for enrollment copying between classrooms.
- Use `mcp__plugin_clickmax_clickmax__classroom_delete` with the classroom id only when the user is clearly asking for removal.
- After any mutation, use `mcp__plugin_clickmax_clickmax__classroom_details` again with the classroom id when the user expects the final linked-content state.

## Report

- Start with the classroom name and portal context.
- For inspection, report linked contents first, then notable lesson/access details.
- For mutations, report exactly what changed: created, renamed, content added/removed, members copied, or deleted.
- When listing multiple classrooms, keep the result as a short cohort and cap long outputs with `+N more`.
- Treat follow-up mutations as opt-in only unless the user already asked for them explicitly.

## Warnings

- Classroom delete is destructive for enrollments/content links.
- Adding content does not author the course; it links an existing course into the classroom.

## Anti-patterns

- Treating classroom creation as portal creation.
- Assuming member access is identical to classroom enrollment.

---

Clickmax skill revision: `b8294822a4d6`
