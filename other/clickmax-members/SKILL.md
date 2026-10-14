---
name: clickmax-members
description: Use when the user wants to inspect, create, update, enable, disable, enroll, or remove member users and their access/progress in Clickmax Members.
---

## When this applies

Use this skill for member-user lifecycle and enrollment: resolve the member from a lead, inspect access/progress, create/update/enable/disable, add/remove from classrooms or portals, send access links, change access windows, or delete a member user.

Not this skill:

- portal metadata/subdomain administration -> use the direct portal tools
- classroom container/content linking -> `clickmax-classrooms`

## Key assumptions

- `member_users_get_by_lead` is the safe bridge when the user only knows the CRM lead
- access windows are scoped per member and `(classroom, content)` pair
- progress exists at overall, lead, and course-drilldown levels
- prefer disable over delete when the user only wants to revoke access temporarily

## Thought process

1. Resolve the member identity first.
2. Distinguish lifecycle status, enrollment, access-window, and progress/certificate operations.
3. Prefer reversible actions when the user intent is operational rather than destructive.

## Execute guide

- When the user starts from a CRM lead, resolve the member first with `mcp__plugin_clickmax_clickmax__member_users_get_by_lead`, passing the lead id. Then inspect progress with `mcp__plugin_clickmax_clickmax__member_users_get_progress`, passing the member-user id. If the request is about release windows or expiration, inspect access times with `mcp__plugin_clickmax_clickmax__member_users_get_access_times`, scoped to the relevant classroom ids.
- Create a new member with `mcp__plugin_clickmax_clickmax__member_users_create`, passing identity fields plus the initial classrooms and portals when the enrollment should exist immediately. After creation, send the access link with `mcp__plugin_clickmax_clickmax__member_users_send_access_link`, using the new member-user id and the target portal id.
- After creating or reassigning a member, offer the access-link email path when the user wants the student invited immediately.
- For bulk classroom changes, use `mcp__plugin_clickmax_clickmax__member_users_bulk_update_classrooms`, passing the member-user ids, the intended action, and the classroom ids. Use `mcp__plugin_clickmax_clickmax__member_users_bulk_update_portals` when the request is about portal access instead of classroom membership.
- For one-off classroom membership changes, prefer `mcp__plugin_clickmax_clickmax__member_users_add_to_classroom` or `mcp__plugin_clickmax_clickmax__member_users_remove_from_classroom` instead of a bulk tool.
- Adjust access duration with `mcp__plugin_clickmax_clickmax__member_users_extend_access` only after confirming the exact `(classroom, content)` pair and the requested unit/window. Use `mcp__plugin_clickmax_clickmax__member_users_reset_access` when the user wants to restart access tracking for that scoped item instead of extending the current window.
- Use `mcp__plugin_clickmax_clickmax__member_users_enable` / `mcp__plugin_clickmax_clickmax__member_users_bulk_enable` to restore access. Use `mcp__plugin_clickmax_clickmax__member_users_disable` / `mcp__plugin_clickmax_clickmax__member_users_bulk_disable` for temporary revocation.
- Use `mcp__plugin_clickmax_clickmax__member_users_delete` only when the user explicitly wants permanent removal.
- For certificates, inspect with `mcp__plugin_clickmax_clickmax__member_users_get_certificate_code`, passing the member-user id.

## Report

- Start with the member identity used for the action or inspection.
- Then report the result type in this order: lifecycle status, classroom/portal enrollment, access-window changes, progress/certificate details.
- For bulk operations, summarize successes first and then list failures; if the failure list is long, cap it and append `+N more`.
- For progress, surface the relevant completion state instead of every raw metric.
- Treat follow-up mutations as opt-in only unless the user already requested the change.

## Warnings

- Deleting a member user cascades enrollment, progress, and access-time data.
- Portal enrollment and classroom enrollment are related but not the same operation.

## Anti-patterns

- Deleting when disable would satisfy the request.
- Guessing the member user instead of resolving from lead/user id.
- Mixing progress inspection with enrollment mutation in one opaque step.

---

Clickmax skill revision: `b8294822a4d6`
