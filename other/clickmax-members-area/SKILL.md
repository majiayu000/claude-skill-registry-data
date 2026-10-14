---
name: clickmax-members-area
description: Use when the user wants to build/create a full members area — a portal with classrooms, courses, modules, lessons, students, and login links — end to end in one flow.
---

## When this applies

Use this skill to BUILD a members area end to end: create the portal, its classroom(s), the course(s), modules, lessons (incl. video lessons), then create students, enroll them, and email their login link. This is the builder that stitches the fragmented member tools into one canonical sequence — the members-area analog of `clickmax-funnels`.

## Not this skill

Prefer the granular skill when the request is a single narrow op, not a full build:

- ONLY enroll/matriculate an existing member into a portal/classroom → `clickmax-portal-enrollments`
- ONLY member-user lifecycle (enable/disable/delete, progress, access windows, certificates) → `clickmax-members`
- ONLY one isolated classroom op (add content, copy members, rename, delete) → `clickmax-classrooms`
- ONLY module reorder/rename → `clickmax-modules`
- ONLY offer/product edits → `clickmax-offers` / `clickmax-products`

## Build order (canonical)

Hierarchy derived from the tools/models. Two axes meet at the classroom:

```
portal ──< classroom >── content (course, workspace-level) ──< module ──< lesson
                │                         ▲
                │        classroom links an EXISTING content (course) by contentId
                └── member users (students) enroll into the portal, then the classroom
```

Key parenthood (real fields):

- **content (course)** is workspace-level, NOT created inside a classroom. `content_create` takes no parent id; you attach it to a classroom afterward.
- **classroom** belongs to a portal (`portalId`) and holds a `contentsIds` list of course ids.
- **module** belongs to a course (`module_create` → `contentId`).
- **lesson** belongs to a module (`lesson_create` → `moduleId`). Lessons do NOT belong to the course directly.
- **student (member user)** is workspace-level; portal + classroom are assignments, not parents.

Steps (do the whole chain in one continuous flow; ids come from earlier results):

1. **Portal** → `portals_create` (name + `subdomain` + theme). Pre-flight the subdomain.
2. **Classroom (turma)** → `classroom_create` with `portalId`. If courses already exist, pass their ids as `contentsIds` now; otherwise create courses first (step 3) and pass the ids, or link later via `clickmax-classrooms` (`classroom_add_content`).
3. **Course (content/curso)** → `content_create` (workspace-level; no parent). Capture the content id.
4. **Module (módulo)** → `module_create` with `contentId` = the course id.
5. **Lesson (aula)** → `lesson_create` with `moduleId` = the module id. For a YouTube/video lesson set `type: "video"` and `url` = the video URL (`^https?://.+$`).
6. **Student (aluno)** → `member_users_create` (one, by email+name) or `member_users_bulk_create` (many). Assign portal/classroom inline when the body supports it, or enroll in step 7.
7. **Enroll + login link** → `portal_members_add` (`memberUserId` in body, `portalId` in path) to put the student in the portal, then `member_users_send_access_link` (`memberUserId` + `portalId`) to email the login URL.
8. **Sell it as delivery (turma como entrega)** → for each product that should grant this classroom, resolve the product's main `offerId` (via `clickmax-products`/`clickmax-offers`) and call `offers_add_membership_delivery` (`offerId` + `portalId` + `classroomId`). Buyers of that offer then get classroom access. Runs any time after the portal + classroom exist.

## Key assumptions

- Scope = one workspace; never ask for workspace id.
- Course lives at the workspace, is REUSABLE, and is linked into one or more classrooms — creating a course does not put it in a portal by itself.
- Classroom is portal-bound for life; a course is not.
- Lesson parent is the module, not the course — always thread `moduleId`.
- Ids (portal, classroom, content, module, lesson, memberUser) are server-generated; read them back from each create result, never invent.
- Creating a member user does not, by itself, grant portal access — the portal/classroom assignment (inline body or `portal_members_add`) is what unlocks login.
- Sending the access link is a separate, explicit step — creation alone does not email the student.
- Subdomain is unique across the workspace; always pre-flight before creating/renaming a portal.

## Execute guide

Use the tools in dependency order — later ids come from earlier results.

- Discover existing portals/courses first when the user is vague: `mcp__plugin_clickmax_clickmax__portals_list`, `mcp__plugin_clickmax_clickmax__content_list`. Read one with `mcp__plugin_clickmax_clickmax__portals_get` / `mcp__plugin_clickmax_clickmax__content_get`.
- **Portal**: pre-flight with `mcp__plugin_clickmax_clickmax__portals_check_subdomain` (pass `subdomain`), then `mcp__plugin_clickmax_clickmax__portals_create` with `name` + `subdomain` + theme.
- **Classroom**: `mcp__plugin_clickmax_clickmax__classroom_create` with `portalId` + `name`; pass `contentsIds` (and any `contentsAccessTime`) when the courses already exist.
- **Course**: `mcp__plugin_clickmax_clickmax__content_create` with the course `title` + `description` + `category` (all three required, no defaults); capture the returned content id. It is workspace-level — do not expect a portal/classroom parent field.
- **Module**: `mcp__plugin_clickmax_clickmax__module_create` with `contentId` = the course id.
- **Lesson**: `mcp__plugin_clickmax_clickmax__lesson_create` with `moduleId` = the module id. `releaseType` is ALSO required (no default) — `FIXED_DATE` + `releaseDate`, or `DAYS_AFTER_PURCHASE` + `releaseDays`. For a **YouTube/video lesson**, set `type: "video"` and `url` = the video URL (must match `^https?://.+$`); `name` is required. Add supplementary files via lesson attachments, not the `url` field.
- **Reorder / hide** while building: move a misplaced lesson with `mcp__plugin_clickmax_clickmax__lesson_move` (`targetModuleId` + 1-based `position`); hide-not-delete a lesson with `mcp__plugin_clickmax_clickmax__lesson_toggle_enabled` (`items: [{ id, enabled }]`, `id` = lesson id, NOT `lessonId`) or a course with `mcp__plugin_clickmax_clickmax__content_toggle_enabled` (`items: [{ id, enabled }]`, `id` = content id, NOT `contentId`); rename/adjust a course with `mcp__plugin_clickmax_clickmax__content_update`.
- **Student (one)**: `mcp__plugin_clickmax_clickmax__member_users_create` with email + name (+ optional portal/classroom assignments in the body).
- **Students (many)**: `mcp__plugin_clickmax_clickmax__member_users_bulk_create` — returns `successful`/`failed` counts + per-record `errors`; surface failures, do not assume all landed.
- **Enroll**: `mcp__plugin_clickmax_clickmax__portal_members_add` with `portalId` (path) + `memberUserId` (body). Note it does NOT auto-enroll into classrooms — classroom enrollment comes from the `member_users_create` body assignment or `clickmax-members`/`clickmax-classrooms` tools.
- **Login link**: `mcp__plugin_clickmax_clickmax__member_users_send_access_link` with `memberUserId` + `portalId` to email the portal login URL. Do this after enrollment so the link lands on a portal the student can actually enter.
- **Verify**: read back with `mcp__plugin_clickmax_clickmax__content_get` / `mcp__plugin_clickmax_clickmax__lesson_list` (`moduleId`) / `mcp__plugin_clickmax_clickmax__portals_get` to confirm the tree before reporting done.

Common flow (super-prompt "portal completo"): `portals_check_subdomain` → `portals_create` → `content_create` → `module_create` → `lesson_create` (video, with `url`) → `classroom_create` (with the new `contentsIds`) → `member_users_create` → `portal_members_add` → `member_users_send_access_link`.

## Report

- Lead with the portal name + subdomain, then the built tree: `N classrooms · N courses · N modules · N lessons`.
- When using a visual card for the created members area, the large value/headline must be the portal or classroom name, not the login URL. Show the login URL separately as a markdown link/prose line (for example "Link de login: https://...") or as the final open-page CTA when there is a real app route.
- List created course/module/lesson names compactly; cap long lists with `+N more`.
- For students: report how many were created, how many enrolled, and how many access links were sent (call out bulk `failed`/`errors`).
- When the user wanted the classroom sold as a product's delivery, report which offers were wired to it via `offers_add_membership_delivery` (name the product/offer, not the id).
- Return the real ids the user will need next (portalId, classroomId, contentId).

## Warnings

- **Selling the classroom as a product's delivery ("entrega")** uses `offers_add_membership_delivery` (`offerId` + `portalId` + `classroomId`), which adds an `internal_membership` deliverable to the offer (buyers then get classroom access). It attaches to an OFFER — a product's MAIN offer, not the product directly — so resolve the offer id first via `clickmax-products`/`clickmax-offers`. It ADDS a deliverable (never replaces existing ones); call it once per product/offer that should grant the classroom.
- Resolve real `portalId`, `classroomId`, `contentId`, `moduleId`, `lessonId`, `memberUserId` — never invent them.
- A course created but not linked into any classroom is invisible to students; a classroom with no `contentsIds` is empty.
- `member_users_create` / `portal_members_add` grant access; without them a student cannot log in even after the access link is sent.
- `portal_members_add` enrolls into the portal only — it does not cascade into classrooms.
- Prefer `*_toggle_enabled` over delete while building; delete cascades (portal → assignments/content links; content → modules/lessons; module → lessons; lesson → progress) and is destructive — confirm unless deletion was explicit.
- Video lesson URL goes in the lesson `url` field with `type: "video"`; it validates `^https?://.+$`, so pass a full `https://` URL, not a bare video id.

## Anti-patterns

- Creating a course "inside" a classroom or portal — courses are workspace-level; you LINK them via `contentsIds` / `classroom_add_content`.
- Attaching a lesson to the course instead of a module (`lesson_create` needs `moduleId`, not `contentId`).
- Creating students and stopping before enrollment + access link, leaving members who cannot enter.
- Promising the classroom is "sold with the product" without calling `offers_add_membership_delivery` — building the portal/classroom does not bind it to any offer by itself.
- Deleting a portal/course/module when the user only wants it hidden — use the toggle tools.
- Skipping `portals_check_subdomain` and failing `portals_create` on a taken subdomain.
- Falling back to the granular skills mid-build and losing the end-to-end sequence; stay in this builder until the tree + students + links are done.

---

Clickmax skill revision: `b8294822a4d6`
