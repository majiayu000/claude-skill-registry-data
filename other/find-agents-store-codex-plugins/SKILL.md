---
name: find
description: 'Search Plane work items by query, identifier, or filter Arguments: <query> [--project name] [--state name] [--assignee user] [--label name].'
---

# Find

Quick search for Plane work items. Accepts a free-text query, an identifier (`PROJ-42`), or filter flags.

## Arguments

Format: `<query> [flags...]`

- `query`: free text, OR an identifier like `PROJ-42`, OR omit when using only filters
- `--project <name>`: scope to a project
- `--state <name>`: filter by state (e.g. "In Progress")
- `--assignee <user>`: filter by assignee (or `me`)
- `--label <name>`: filter by label
- `--limit <n>`: max results (default 20)

Parse from `"$ARGUMENTS"`.

## Process

1. **Bootstrap connector** — consult `connector-bootstrap`. Probe for the Plane resource tools `workitem`, `member`, `state`, `label` and `get_pql_reference`.
2. **Detect identifier shortcut** — if the query matches `^[A-Z][A-Z0-9]+-\d+$`, call `workitem(action=retrieve_by_identifier, workitem_identifier="PROJ-42")` directly (the full identifier as one string). Render the full item and stop.
3. **Build one PQL filter** from the query and flags, and let the server do the filtering with `workitem(action=list, project_id?, pql=..., per_page=<limit>)` (omit `project_id` to search the whole workspace; call `get_pql_reference` for the syntax; at most 5 conditions):
   - free text → `title ~ "login bug"` (title only) or `text ~ "login bug"` (title and description)
   - `--assignee me` → `assignee = currentUser()`; another user → `assignee = "<member uuid>"` (`member(action=list_project)` resolves the name)
   - `--state <name>` → `state = "<state uuid>"` (`state(action=list)` resolves the name); for "open" or "done" use `stateGroup IN openStates()` / `stateGroup IN closedStates()`
   - `--label <name>` → `label = "<label uuid>"` (`label(action=list)` resolves the name)
   Join the conditions with `AND`. If a flag needs more than 5 conditions, apply the extra ones client-side.
4. **Pure free text, no flags** — `workitem(action=search, query)` is the alternative: it is workspace-scoped (no `project_id`), so filter its results to `--project` client-side.
5. **Page** — follow `next_cursor` only when the user asks for more than `--limit`.
6. **Render** — table with columns: `ID | Title | State | Assignee | Updated`. Truncate titles at 60 chars. Show top `--limit` results.
7. **Suggest next actions** — for any single result, hint at `/work-item get`, `/comment add`, `/assign`.

## Examples

```
/find "login bug"
/find PROJ-148
/find --assignee me --state "In Progress"
/find "checkout" --project "TaskFlow" --label type/bug
/find --label priority/p0 --limit 5
```

## Best Practices

- Reuse a filter by keeping its PQL text, for example "my open p0 bugs": `assignee = currentUser() AND label = "<p0-label-uuid>" AND stateGroup IN openStates()`.
- Search is full-text over title and description on most Plane builds — comments are usually NOT indexed.
- If `search` results feel stale, the workspace search index may be lagging — fall back to `workitem(action=list, pql=...)`, which filters at the source.