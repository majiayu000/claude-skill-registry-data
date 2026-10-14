---
name: clickmax-modules
description: Use when the user wants to list, inspect, create, update, reorder, or delete modules and lesson ordering inside a Clickmax Members course.
---

## When this applies

Use this skill for module-level management inside a course: list/get/create/update/delete modules, reorder modules in the course, or reorder lessons inside one module.

Not this skill:

- classroom/container management -> `clickmax-classrooms`
- lesson-level content edits beyond module ordering -> use the direct lesson tools

## Key assumptions

- modules belong to one content/course
- module ordering and lesson ordering are two different full-order operations
- ordering inputs are full target orders with 1-based positions, not small patch operations
- deleting a module cascades to its lessons

## Thought process

1. Resolve the course/module first.
2. Distinguish metadata changes from ordering changes.
3. Confirm destructive deletion when intent is not already explicit.

## Execute guide

- Inspect the current module set before reordering or deleting.
- List modules for a course with `mcp__plugin_clickmax_clickmax__module_list`, passing the course `contentId`.
- Inspect one module with `mcp__plugin_clickmax_clickmax__module_get`, passing only the module `id` (no `contentId` — the module's course is not a path/body param on this tool).
- Create a module with `mcp__plugin_clickmax_clickmax__module_create`, passing the target `contentId`, the module `name`, and the release rule fields that match the requested launch behavior such as `releaseType = FIXED_DATE` with `releaseDate`, or `releaseType = DAYS_AFTER_PURCHASE` with `releaseDays`.
- Update module metadata or release rules with `mcp__plugin_clickmax_clickmax__module_update`, passing only the module `id` (no `contentId`) and the fields the user wants changed.
- Reorder modules with `mcp__plugin_clickmax_clickmax__module_organize_positions`, sending the full final module order as `moduleId + position` pairs with 1-based positions.
- Reorder lessons inside one module with `mcp__plugin_clickmax_clickmax__module_organize_lesson_positions`, passing the module `id` (not `moduleId` — this tool's own param is `id`) plus the full final lesson order as `lessonId + position` pairs.
- Delete a module with `mcp__plugin_clickmax_clickmax__module_delete` only when removal is explicit, passing only the module `id` (no `contentId`).
- After any reorder, report the final ordered list back to the user.

## Report

- Open with the affected course/module scope.
- For ordering, report the resulting order rather than only "success=true".
- For delete, state clearly that lessons were also removed.
- Follow-up mutations should stay opt-in.

## Warnings

- Reordering semantics are full-order replacement.
- Module delete cascades to all lessons.

## Anti-patterns

- Treating reorder as a single-item move patch.
- Using module deletion to hide content temporarily.

---

Clickmax skill revision: `b8294822a4d6`
