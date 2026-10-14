---
name: clickmax-projects
description: Use when the user wants to create, list, inspect, rename, set-default, or delete workspace projects in Clickmax, or when any build needs a target project resolved first.
---

## When this applies

Use this skill for workspace-level project management: creating a project, listing/searching projects, inspecting one project (with dependency counts), renaming, setting the workspace default, and destructive delete.

Project is the top-level container. Almost every build starts "in project X", so resolving or creating the project is step zero before funnels, products, members, or flows work.

## Not this skill

- lightweight project autocomplete/selection -> `projects_filters` (lives in `clickmax-funnels`)
- funnel/page/product/member/flow work once the project is known -> the respective domain skill, passing the resolved project

## Key assumptions

- projects are identified by `slug`, not by numeric id; every tool except create/list takes a `slug`
- `projects_create` takes only `projectName`; the backend generates a unique `slug` automatically
- `projects_update` changes the display name only and preserves the same `slug`
- `projects_set_default` returns `{ applied }`; `applied: false` means the slug was not found
- `projects_delete` returns `{ deleted }` and cascades cleanup across related project assets (pages, funnels, cloakers)
- `projects_get` returns dependency counts (pages, funnels, cloakers) useful before delete or as context
- `projects_list` is paginated with filters (search, active state, import state, ordering); the default project is a workspace-level setting other domains rely on

## Thought process

1. Resolve intent: read/list vs create vs rename vs set-default vs destructive delete.
2. If the user names a project by label, resolve its `slug` via `projects_list` before acting.
3. If no project exists yet for the requested work, create it first, then continue the downstream build.
4. Inspect dependency counts before delete so the cascade impact is explicit.
5. Confirm destructive delete when intent is not already explicit.

## Execute guide

- Use `mcp__plugin_clickmax_clickmax__projects_list` to enumerate or search projects and resolve a label to its `slug`; pass `search`, active/import filters, or ordering as needed. Omitted ordering defaults to newest first (`createdAt desc`).
- Use `mcp__plugin_clickmax_clickmax__projects_get` to inspect one project by `slug`, including dependency counts for pages, funnels, and cloakers.
- Use `mcp__plugin_clickmax_clickmax__projects_create` to create a project from `projectName`; capture the returned `slug` and reuse it for any downstream build.
- Use `mcp__plugin_clickmax_clickmax__projects_update` to rename an existing project by `slug`; the `slug` stays the same.
- Use `mcp__plugin_clickmax_clickmax__projects_set_default` to set the workspace default project by `slug`; treat `applied: false` as "slug not found", not success.
- Use `mcp__plugin_clickmax_clickmax__projects_delete` only for explicit permanent removal; check dependencies first because it cascades across related assets.

## Report

- Start with the project identity: `name` + `slug`.
- For create, state the new `slug` and that downstream work can now target it.
- For list, report the matching projects and which one is the default.
- For get, surface dependency counts (pages/funnels/cloakers).
- For set-default, report `applied` truthfully.
- For rename/delete, state the action result first and keep follow-up actions opt-in.

## Warnings

- `projects_delete` is destructive and cascades across related project assets; require explicit intent and confirm before running.
- Do not treat `projects_set_default` `applied: false` as a completed change; the slug did not resolve.
- Do not invent a `slug`; resolve it from `projects_list` or from a prior create response.
- Do not rename via delete-and-recreate; renaming changes only the display name and keeps the `slug`, whereas recreate mints a new `slug` and orphans downstream references.

## Anti-patterns

- Passing a display name where a `slug` is required.
- Starting a funnel/product/members/flow build without a resolved project.
- Deleting a project without inspecting its dependency counts first.
- Assuming a freshly created project is the default; set it explicitly if needed.

---

Clickmax skill revision: `b8294822a4d6`
