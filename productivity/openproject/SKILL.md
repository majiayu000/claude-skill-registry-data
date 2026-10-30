---
name: openproject
description: Use when working with OpenProject — reading or updating projects, work packages, tasks, bugs, features, milestones, sprints/versions, statuses, priorities, due dates, assignees, dependencies, time entries, or progress reports through the OpenProject MCP tools. Triggers on requests to check what is in a project, find overdue or assigned work, create or break down tickets, move tickets between statuses, reschedule or reprioritize, log hours, post progress updates on a task, write status reports, or track progress of a (coding) project in OpenProject.
---

# Working with OpenProject

These tools reach a real project tracker other people rely on. A wrong bulk update is
visible to the whole team and tedious to undo, so the operating rules matter more than
tool trivia.

## Rules that prevent most mistakes

**1. Discover names and IDs; never guess.** Statuses, types, priorities, and versions
differ per project. `get_work_package_options(project_id)` returns all of them in one
call. Tools accept names ("High", "Sprint 4") and reject unknown ones with the valid list.

**2. Lists show OPEN work by default.** `list_work_packages` hides closed items unless
you pass `status="all"`. Use `"all"` whenever you are counting, reporting, or looking
for something that may be done.

**3. Destructive tools are guarded.** Deletes and `bulk_update_work_packages` default to
`dry_run=True`. Run the preview, check the impact — including `permitted`, whether this
user may delete it at all — then re-run with `dry_run=False, confirm=True`. Clearing
`dry_run` alone does nothing.

**4. Read before you write.** Look at an item's current state (`get_work_package`) and
recent history (`list_work_package_activities`) before changing it.

## Start here

```
get_operational_diagnostics()            # reachable? which user do "me"/"mine" mean?
list_projects(search="...")              # project_id
get_work_package_options(project_id)     # statuses, types, priorities, versions, categories
list_project_members(project_id)         # principal_id → assignee_id
```

## Routing

| The user wants | Use |
|---|---|
| What's on my plate | `list_work_packages(assigned_to_me=True, sort_by="due_date:asc")` |
| What's overdue / due soon | `list_work_packages(project_id, overdue=True)` / `due_before=...` |
| What's in a sprint or release | `list_work_packages(project_id, version_ids=[...], status="all")` |
| Start or finish a sprint / release | `create_version` / `update_version(status="closed")` |
| Find a ticket by words | `list_work_packages(search="...")` — across all projects if no project_id |
| One ticket in full | `get_work_package` — description, effort, children, custom fields |
| What happened on a ticket | `list_work_package_activities` — newest first, comments and changes |
| Create one ticket | `create_work_package` — with priority, version, dates, assignee up front |
| Break work down into a hierarchy | `create_work_package_tree` (after `create_project` for a new one) — for *how* to shape it, see the **project-planning** skill |
| Reschedule, reprioritize, reassign, unassign | `update_work_package` — `clear=[...]` unsets fields |
| Move a ticket's status | `update_work_package_status` — enforces the workflow, lists allowed statuses on error |
| Same change on many tickets | `bulk_update_work_packages` — dry run first |
| Dependencies | `create_work_package_relation` (blocks, precedes, ...), `list_work_package_relations` |
| Log hours / see logged hours | `create_time_entry` / `list_time_entries(mine=True, spent_from=...)` |
| Status report | `generate_project_progress_report(project_id, version=...)` |
| Record project health | `update_project(project_id, status="at_risk", status_explanation=...)` |

Recipes: [reference/workflows.md](reference/workflows.md). All tools: [reference/tools.md](reference/tools.md).

Planning a new project, or breaking an initiative into phases, milestones and tasks, is
a different job from operating the tools: the **project-planning** skill carries the
decomposition playbooks, dependency design, estimation, and the build order that avoids
creating a tree that names versions or types the project does not have yet.

## Tracking progress on a task

Pick the mechanism by what the text is for:

| Purpose | Mechanism |
|---|---|
| A timeline entry: what happened, a decision, a handoff | `add_work_package_note` — attributed and timestamped. `notify=False` for routine automated updates. |
| The current state, always up to date | A description section: `update_work_package(wp_id, description_section_heading="Status", description_section_markdown=...)` rewrites only that section. |
| A numeric signal | `update_work_package(wp_id, percentage_done=...)` and `remaining_hours=...` |
| A long document (design, runbook) | `upload_work_package_attachment(wp_id, file_name="design.md", content=...)` — pass content, not a path |
| A project-level living doc (architecture, decisions) | A dedicated work package, maintained through description sections. Project documents are read-only via the API. |

For coding work, a description laid out as `## Plan`, `## Status`, `## Links` works well:
update `Status` and `Links` (branches, PRs) in place as work moves, and post a note for
each milestone reached. The team sees the current state at a glance and the history in
the activity feed.

## Judgment

**Scope bulk operations narrowly.** Build the ID list from an explicit query, show the
user what matched, dry-run, then execute. Do not expand the set beyond what was asked.

**Ambiguous target means ask.** Two similar project names, or a ticket described but not
identified, is a question for the user. Asking costs one turn; editing the wrong record
costs someone else's afternoon.

**Report what changed.** Update tools return `changed_fields`; bulk returns per-item
results. Name the work package IDs and what happened to each. Surface failures.

**Preview uncertain edits.** `update_work_package(..., validate_only=True)` asks
OpenProject whether a change would save — useful for dates, progress, or custom fields
whose rules you do not know.

**Mind notifications.** Every change notifies watchers by default. For frequent,
automated updates pass `notify=False`, and prefer one consolidated note over many.

## Known limitations

- **The server may be confined to certain projects.** If `get_operational_diagnostics`
  shows `project_restriction.active`, only those projects are reachable, and an
  `OutOfScopeError` means the item is off-limits by configuration. Tell the user; do not
  look for another route to it.

- **A work package can have several versions** on OpenProject 17.8+, where the field is
  called "Target versions". Read them from `versions`; `version` is the first of them.
  Writing `version=...` sets exactly one, replacing any others.
- **Documents are read-only via the API** (OpenProject 16.x allows only reading them).
  Read them for context with `get_document`; write living docs as work package
  description sections instead.
- **Wiki pages and forum posts are not writable via the API**, so there are no tools for
  them. Use notes, description sections, attachments, or documents instead.
- **Attachment uploads depend on server storage.** If an upload returns guidance instead
  of a file, fall back to a note or a description section.
- **`percentage_done` may be read-only** on instances that derive progress from status or
  work; the error says so. Set `remaining_hours` instead, or move the status.
- **Deleting projects takes an administrator.** A project admin can create subprojects
  but not delete them; check `permitted` in the dry run before creating throwaway projects.
- Time entries: hours greater than 0 and at most 24; dates are `YYYY-MM-DD`.

## Errors worth recognising

| Symptom | Meaning |
|---|---|
| "not an allowed transition ... Allowed statuses: ..." | Workflow restriction. Use a listed status. |
| "Unknown priority/version/type ... Available ...: ..." | Use one of the listed names. |
| 422 with field messages | The change breaks a rule; the message names the field. |
| 409 | Concurrent edit. Already retried against the latest version; if it persists, re-read. |
| 404 | Wrong ID, or you cannot see it. |
