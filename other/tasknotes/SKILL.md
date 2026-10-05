---
name: tasknotes
description: "Manage tasks in an Obsidian TaskNotes vault. Use for creating, reading, updating, or completing tasks; checking what is open or in progress; adding items to a list; marking tasks done or in progress; updating task status or priority; investigating why a task is missing from a view or board; troubleshooting TaskNotes MCP or API connection issues; setting up or configuring TaskNotes; or running a schema diagnostic on task files. Routes automatically to the best available access method: MCP server, HTTP API, or direct file access. Bundled help at references/tasknotes-help.md."
metadata:
  version: "4.3"
---

# TaskNotes

Multi-modal task management for Obsidian TaskNotes vaults. The skill probes the environment first and routes to the best available access method.

---

## Step 0 - Environment probe

**Run before any operation.** Determines which path to take.

**Bundled help:** This skill includes `references/tasknotes-help.md` with step-by-step setup instructions, full API endpoint reference, and troubleshooting for all failure modes. Read it yourself when connection or setup issues arise, and share the relevant sections with the user to guide them through fixes.

### 1. MCP available?

Run `tool_search("tasknotes")`. If `tasknotes:` tools load successfully, the MCP server is live.

If they do not load, do not conclude the server is down. Since plugin v4.13.0 the MCP endpoint requires a bearer token, and a client configured without one fails at connect time, so the tools never appear at all. Check 2 below - a `401` there means the server is running and the client is simply unauthenticated.

### 2. HTTP API available?

Attempt `web_fetch("http://127.0.0.1:8080/api/health")`. Three outcomes, and they mean different things:

| Response | Meaning |
|---|---|
| `{"status":"ok",...}` | HTTP API is live and the request is authenticated |
| `401 {"success":false,"error":"Authentication required"}` | Server is running; the request carries no API token |
| Connection refused or timeout | Server is not running on that port |

**On a `401`:** the surface exists but is unusable until requests carry `Authorization: Bearer <token>` (plugin v4.13.0+). If you can set headers, the token is at Settings → TaskNotes → Integrations → HTTP API → **API authentication token**; ask the user for it and retry. Never read it out of the plugin's `data.json`. If you cannot, tell the user their client config is missing the token and point them at `references/tasknotes-help.md`. **Do not quietly fall through to the filesystem path.** That hides a one-line misconfiguration and silently costs the user filtered queries, time tracking, Pomodoro and per-instance recurring completion. Say what is missing.

**On connection refused or timeout,** ask the user:
- *"What port is your TaskNotes HTTP API configured on? Check Settings → TaskNotes → Integrations → HTTP API."*
- *"Are both the HTTP API toggle and the MCP Server toggle enabled in those settings?"*

Try the user-supplied port before giving up. If still unreachable, HTTP API is unavailable.

### 3. Filesystem available?

Check whether any loaded tool can read and write `.md` files. Do not assume a specific tool name - any filesystem capability qualifies.

### Routing

| MCP | HTTP API | Filesystem | Route |
|---|---|---|---|
| Yes | - | - | MCP for all ops including body reads (fixed in v4.8.0) |
| No | Yes | - | HTTP API for all frontmatter and body ops |
| No | 401 | Yes | Filesystem path, but tell the user the API token is missing first - the richer surface is one config line away |
| No | 401 | No | Stop. The server is up and unauthenticated; only the user can add the token. Link `references/tasknotes-help.md` |
| No | No | Yes | Filesystem path - all workflows below |
| No | No | No | Inform user what is missing; link `references/tasknotes-help.md` for setup |

### What works on which surface

| Operation | MCP | HTTP API | Filesystem |
|---|---|---|---|
| Create task | `tasknotes_create_task` | `POST /api/tasks` | Workflow 1 |
| Update frontmatter | `tasknotes_update_task` | `PUT /api/tasks/:id` | Workflow 3 |
| Mark done | `tasknotes_update_task` | `PUT /api/tasks/:id` | Workflow 4 |
| Query / filter tasks | `tasknotes_query_tasks` | `POST /api/tasks/query` | Workflow 5 |
| Read task frontmatter | `tasknotes_get_task` | `GET /api/tasks/:id` | Read .md file |
| Read task body / checklist | `tasknotes_get_task` (details field) | `GET /api/tasks/:id` | Read .md file |
| Write task body | `tasknotes_update_task` (details field) | `PUT /api/tasks/:id` | Write .md file |
| Complete recurring instance | `tasknotes_complete_recurring_instance` | `POST /api/tasks/:id/complete-instance` | Not supported (GUI only) |
| Schema diagnostic | ✗ → Workflow 9 | ✗ → Workflow 9 | Workflow 9 |
| Time tracking | `tasknotes_*_time_tracking` | `/api/tasks/:id/time/*` | Manual (complex) |
| Pomodoro | `tasknotes_*_pomodoro` | `/api/pomodoro/*` | Not supported |
| Works when Obsidian closed | ✗ | ✗ | ✓ |

---

## Path: MCP

The `tasknotes:` MCP tools are mostly self-describing - call them directly. Two things agents reliably get wrong are NOT obvious from the tool list and are pinned below: the `query_tasks` argument shape, and per-instance recurring completion.

**Connection:** the MCP client config must carry `Authorization: Bearer <token>` (plugin v4.13.0+). That is client configuration, not something the skill can set at call time - if the tools are absent, the fix belongs to the user and `references/tasknotes-help.md` has the config for each platform.

**Key tools:**
- `tasknotes_create_task` - create a task with frontmatter fields
- `tasknotes_update_task` - update frontmatter fields (including `status`, `priority`, `projects`, `details`)
- `tasknotes_query_tasks` - filter tasks with AND/OR conditions (arg shape below)
- `tasknotes_list_tasks` - unfiltered list with pagination (`limit`/`offset`); prefer `query_tasks` when filtering
- `tasknotes_get_task` - read a single task (frontmatter + `details` body) by file path
- `tasknotes_toggle_status` - cycle status through the configured workflow
- `tasknotes_get_filter_options` - list available statuses, priorities, projects, contexts
- `tasknotes_complete_recurring_instance` / `tasknotes_materialize_occurrence` - recurring tasks (see below)

In deferred-tools environments, load a tool's schema before guessing its args: `tool_search("select:tasknotes_query_tasks")`.

**Querying with `tasknotes_query_tasks` - flattened arg shape.** The MCP tool takes the filter group **flattened to top-level arguments**, NOT the wrapped `{"type":"group", ...}` body documented for the HTTP API in `references/tasknotes-help.md`. Passing the HTTP wrapper fails with a `conjunction`/`children` validation error.

- Required top-level: `conjunction` (`"and"` | `"or"`) and `children` (array). Optional: `sortKey`, `sortDirection` (`"asc"` | `"desc"`), `groupKey`.
- Each child is a condition `{ "type": "condition", "id": "<any stable string>", "property": "<field>", "operator": "<op>", "value": <value> }` - the key is `property`, NOT `field`. Nested groups are allowed as children.
- Common operators: `is`, `is-not`, `contains`, `does-not-contain`, `is-empty`, `is-not-empty` (hyphenated - `is-not`, not `is not`). Full list in `references/tasknotes-help.md`.

```json
{
  "conjunction": "and",
  "children": [
    { "type": "condition", "id": "c1", "property": "projects", "operator": "contains", "value": "[[Project - Home]]" },
    { "type": "condition", "id": "c2", "property": "status", "operator": "is-not", "value": "done" }
  ],
  "sortKey": "status",
  "sortDirection": "asc"
}
```

`tasknotes_get_task` and `tasknotes_update_task` take **`id`** (the vault-relative file path), not `taskId`.

**Recurring tasks (MCP).** To complete a single occurrence without closing the series, call `tasknotes_complete_recurring_instance` (`id` = task file path; optional `date` = `YYYY-MM-DD`, defaults to today). To create a concrete occurrence note for one date, call `tasknotes_materialize_occurrence` (`id`, `date`). Never set `status: done` on the recurring task itself - that closes the whole series. See Workflow 10.

**Conventions that apply regardless of path:**
- `projects:` must be a wikilink array - `["[[Domain - Home]]"]` not a plain string; plain strings are silently broken and the task will not appear on any Kanban
- Status cycle: `open` → `in-progress` → `done`
- Always include `tags: ["task"]` - without it the task is invisible to all TaskNotes views
- Task paths in MCP calls are vault-relative (e.g. `Agent Access/TaskNotes/Tasks/filename.md`)

**Schema diagnostic:** Not available via MCP. If the user asks for a schema health check, switch to the Filesystem path → Workflow 9.

---

## Path: HTTP API

Use when the HTTP API is available but MCP is not.

**Base URL:** `http://127.0.0.1:{port}/api` (default port: 8080). Dial `127.0.0.1`, not `localhost` - the listener is IPv4-loopback only, and `localhost` resolves to `::1` first on many systems.

**Every request needs `Authorization: Bearer <token>`** (plugin v4.13.0+), `/api/health` included - no endpoint is exempt. The token is at Settings → TaskNotes → Integrations → HTTP API → **API authentication token**. Without it every call returns `401 {"success":false,"error":"Authentication required"}`.

**Key endpoints:**

| Method | Endpoint | Use |
|---|---|---|
| GET | `/api/health` | Verify server is running |
| GET | `/api/tasks` | List tasks with pagination |
| POST | `/api/tasks` | Create a task |
| GET | `/api/tasks/{id}` | Read a task's frontmatter by path |
| PUT | `/api/tasks/{id}` | Update task fields |
| POST | `/api/tasks/query` | Filter tasks with AND/OR logic |
| POST | `/api/tasks/{id}/toggle-status` | Cycle task status |
| GET | `/api/filter-options` | List valid statuses, priorities, projects |

The `{id}` parameter is the URL-encoded vault-relative file path (e.g. `Agent%20Access%2FTaskNotes%2FTasks%2Ftask.md`).

**Schema diagnostic:** Not available via HTTP API. Switch to Filesystem path → Workflow 9.

**Full endpoint reference:** `references/tasknotes-help.md`

---

## Path: Filesystem

Used when MCP and HTTP API are both unavailable, or when the filesystem is the only available surface.

All workflows below operate by reading and writing `.md` task files directly.

**Note - direct edits while Obsidian is running (plugin v4.9.0+):** the plugin now detects direct file edits to lifecycle fields (`status`, `completedDate`, scheduled/due dates) and runs the matching side-effects - Google Calendar sync and auto-archive. Previously these were silent. Since v4.13.1 this extends to occurrence notes: a direct status edit on one updates the recurring parent's completion history and can create the next occurrence. This only applies when Obsidian is open while you edit files directly; with Obsidian closed there are no side-effects.

---

### Config Discovery (filesystem path)

**Read `tasknotes-config.md` before any filesystem operation.** It carries the task folder path, project routing table, and field defaults.

The skill bundles a default `tasknotes-config.md` at `references/tasknotes-config.md` for first-time deployment.

1. **Scope check - MANDATORY STOP:** If filesystem scope is a bare drive root (`C:\`, `/`) or user home - stop. Ask the user for their TaskNotes folder path.

2. **Search for `tasknotes-config.md`** recursively within scope (first-match, max 5 levels).
   - **Found and parses cleanly:** extract `tasks_folder`, `default_status`, `default_priority`, `default_tags`, `projects`, `contexts`. Proceed.
   - **Found but malformed:** stop. Report exactly what is malformed. Offer: (a) user fixes and re-invokes, or (b) replace with bundled default (warn this overwrites customisations).
   - **Not found:** go to step 3.

3. **No config found:**
   - Look for an existing `TaskNotes/Tasks` folder as a placement hint.
   - **Found:** *"I found TaskNotes/Tasks at [path]. Deploy `tasknotes-config.md` alongside it at [parent]?"* Wait for confirmation.
   - **Not found:** ask the user for a folder path; deploy config and create `TaskNotes/Tasks/` on confirmation.
   - Remind the user to set Settings → TaskNotes → General → Task folder to match.

**Resolving `tasks_folder`:** Join the value with the config file's directory. If it resolves outside (e.g. uses `../`), stop and ask the user to confirm.


### Data Model

Each task is a `.md` file in `tasks_folder`. Filename: `YYYY-MM-DD-slug.md` (title lowercased, spaces as hyphens).

**Canonical frontmatter field order:**

```yaml
---
title: Task title here
status: open
priority: normal
scheduled: YYYY-MM-DD
completedDate:
projects:
  - "[[Project Note Title]]"
dateCreated: YYYY-MM-DD
dateModified: YYYY-MM-DD
tags:
  - task
contexts:
  - "@context-label"
---
```

Use `default_status`, `default_priority`, and `default_tags` from config. Field order matters for Obsidian Properties rendering.

**Required:** `title`, `status`, `priority`, `dateCreated`, `dateModified`, `tags` (must include `task`).

**Include when relevant:** `scheduled`, `projects` (wikilink only), `contexts`.

**Leave empty until set:** `completedDate`.

**Add only as needed:** `due: YYYY-MM-DD`, `timeEstimate: 30` (minutes).

**Recurring tasks:**

```yaml
recurrence: "DTSTART:YYYYMMDD;FREQ=WEEKLY;BYDAY=MO"
recurrence_anchor: scheduled
scheduled: YYYY-MM-DD
```

`recurrence_anchor`: `scheduled` (from scheduled date) or `completion` (from completion date).

**Dependencies:**

```yaml
blockedBy:
  - uid: "relative/path/to/blocking-task.md"
    reltype: "FINISHTOSTART"
```

**Date format:** `YYYY-MM-DD` for all date fields. No timestamps.

---

### Task Body

Write enough context that any agent or human can resume the task without the originating chat. Include what needs doing and why, acceptance criteria as inline checkboxes, constraints, and links to related notes.

**Suggested structure** (use what applies - simple tasks need only one line):

```markdown
## Context
What triggered this task; which session or conversation.

## Problem or intent
What is broken, missing, or unclear.

## Approach
Shape of the answer. Open questions explicitly listed.

## Acceptance criteria
- [ ] Binary checkable item
- [ ] Another checkable item
```

---

### Organisation: Projects, Contexts, Tags

| Field | Purpose | Drives Relationships Widget | Notes |
|---|---|---|---|
| `projects:` | Links task to a vault note; that note shows a live Kanban of all tasks pointing to it | Yes | Must be a wikilink. Plain strings are silently broken. |
| `contexts:` | Semantic sub-domain label for filtering within a project's views | No | Free-form string. Multiple per task. |
| `tags:` | Identifies the file as a task to the plugin | No | `task` is required. Without it the file is invisible to all views. |

The `projects:` map in `tasknotes-config.md` is the lookup table. Register a project note there before creating tasks for it.

---

### Relationships Widget

The Relationships Widget renders on any vault note. The **Subtasks (Kanban)** tab shows all tasks whose `projects:` field contains a wikilink to that note, grouped by status. Fully automatic - no per-note configuration.

Settings: Settings → TaskNotes → Appearance → UI Elements → Relationships Widget (on/off and position).

---

### Project Routing Discipline

On every task creation:

1. Look up the project note in `tasknotes-config.md`
2. Verify the project note exists in the vault; do not link to a non-existent note
3. If the note does not exist: stop, inform the user, offer to create it first
4. If no matching entry: show the known project list, ask which applies or whether a new entry is needed
5. Never write `projects:` as a plain string - always a wikilink

**Adding a new project:** confirm the note name, create a stub if needed, add to `tasknotes-config.md`, then create the task.

**No projects configured:** tasks can be created without `projects:`. Inform the user the task will not appear in any project view or trigger the Relationships Widget.

---

### Subtask Model

**Tier 1 - Inline checklists:** steps or acceptance criteria within a single task file.

**Tier 2 - Child task files:** when a subtask warrants its own status tracking, create it as a normal task and set its `projects:` to the parent task's wikilink. The Relationships Widget surfaces it in the parent's Subtasks tab.

Rule: inline checklists for steps within one task; separate files for work with independent status.

---

### Quick Reference

| I want to... | Workflow | Key step |
|---|---|---|
| Create a task | 1 | Verify project note exists before linking |
| Read a task | 2 | Read the file; do not rely on memory |
| Update a task | 3 | Read first, surgical edit, update `dateModified` |
| Mark done | 4 | `status: done` + `completedDate: YYYY-MM-DD` |
| List tasks for a project | 5 | Search by project wikilink |
| Fix a GUI-created task | 6 | Adopt workflow |
| Clean up done tasks | 8 | Housekeeping - guide user to plugin archive |
| Schema diagnostic | 9 | Scan for structural problems |
| Recurring task | 10 | Write RRULE; never mark done via agent |


### Workflows

#### 1. Create a task

1. Read `tasknotes-config.md`
2. Identify domain; look up project note and context
3. Verify project note exists (see Project Routing Discipline)
4. Generate filename: `YYYY-MM-DD-<slug>.md`. Append `-2`, `-3` if file exists.
5. Get today's date for `dateCreated` and `dateModified`
6. Write file with required frontmatter + relevant optional fields + body
7. Confirm filename and key fields to the user

**GUI creation note:** Agent creation is the reliable path for correct project assignment. If the user creates tasks via the plugin GUI, the task may be missing `projects:` or `tags:` - use Workflow 6 to repair.

#### 2. Find / read tasks

Search `tasks_folder` for files by project wikilink, status, or keyword. Always read each candidate file in full before acting on it.

When using MCP or HTTP API, task body content (checklists, notes) is returned in the `details` field - no separate file read needed (fixed in v4.8.0).

#### 3. Update a task

Always read the file first. Use surgical edits. Always update `dateModified` alongside any other change.

#### 4. Complete a task

1. Read the task file
2. Set `status: done`
3. Add `completedDate: YYYY-MM-DD`
4. Update `dateModified`

Never delete task files. Done tasks remain on disk; TaskNotes views filter by status.

#### 5. List tasks for a domain

1. Read `tasknotes-config.md` for the project wikilink
2. Search `tasks_folder` for files containing that wikilink. Direct files only; exclude `Archive/`. Paginate to completion - do not stop early.
3. Read frontmatter: title, status, priority, due
4. Present: `in-progress` first, then `open`; skip `done`

**Domain signal:** The project wikilink is the only reliable cross-task domain signal. `contexts:` is a secondary filter, not a substitute.

**Health check:** If more than 150 files and done/archived account for a third or more, flag it and offer Workflow 8.

#### 6. Adopt a GUI-created task

1. Read the task file
2. Check `projects:` - add wikilink if absent; replace path-prefixed wikilinks with bare title
3. Check `tags:` - add `task` if missing
4. Optionally rename to `YYYY-MM-DD-slug.md` (ask before renaming)
5. Update `dateModified`

#### 7. Extend a domain with custom properties

Document custom fields in `tasknotes-config.md` under `domain_extensions:`. Include them when creating tasks in that domain.

On MCP, configured TaskNotes user fields go through the `customProperties` argument of `tasknotes_create_task` and `tasknotes_update_task` (plugin v4.12.0+) rather than being written as raw frontmatter. Query them with `property: "user:<fieldId>"`.

#### 8. Folder housekeeping

**Step 1: Surface done tasks**
1. Scan `tasks_folder` (direct files, excluding `Archive/`) for `status: done`
2. Present sorted by `completedDate` ascending with total count
3. Offer to write a done-tasks Bases view at `TaskNotes/Views/done-tasks.base`

**Step 2: Guide archiving** (plugin handles this, not the skill)
- Settings → TaskNotes → General → Move Archived Tasks to Folder: enable
- Set destination to a subfolder of `tasks_folder` (e.g. `Tasks/Archive/`)
- Archive via plugin GUI; the plugin adds `archived` tag and moves the file

#### 9. Schema diagnostic (filesystem only)

Run when a task search returns nothing for a known project, or a task is missing from views.

Scan `tasks_folder` (direct files, exclude `Archive/`) for:

- `projects:` absent, or a plain string instead of a `[[wikilink]]`
- `projects:` wikilink does not resolve to a real vault page
- `tags:` missing the `task` tag
- `projects:` or `contexts:` is a scalar string instead of a YAML list
- `status:` not one of `open`, `in-progress`, `done`
- `status: done` with no `completedDate`
- `archived` in `tags:` but `status:` still `open`

Report grouped by failure type. Offer to fix each; confirm before writing. Update `dateModified` on every repaired file.

**This workflow requires filesystem access.** MCP and HTTP API cannot perform this scan.

#### 10. Create a recurring task

The skill writes the recurrence pattern; the plugin manages completed instances at runtime. Since v4.13.2, with "Create next after completion" enabled the plugin also creates the first available occurrence note, and occurrence notes link to their parent unambiguously across folders. Never close a recurring task by writing `status: done` (filesystem) or via `update_task` - that ends the entire series permanently. **For per-instance completion, when MCP or the HTTP API is available, use `tasknotes_complete_recurring_instance` (see Path: MCP) or `POST /api/tasks/:id/complete-instance`** - this completes one occurrence without closing the series. On a filesystem-only surface (Obsidian closed), per-instance completion is not possible; completions go through the plugin GUI.

1. Confirm recurrence pattern, anchor (`scheduled` or `completion`), and first occurrence date
2. Build RRULE: `DTSTART:YYYYMMDD;FREQ=...`

   Common patterns:
   ```
   DTSTART:20250804;FREQ=DAILY
   DTSTART:20250804;FREQ=WEEKLY;BYDAY=MO,WE,FR
   DTSTART:20250815;FREQ=MONTHLY;BYMONTHDAY=15
   ```

3. Write the task file with `recurrence`, `recurrence_anchor`, and `scheduled` set to the first occurrence
4. For later per-instance completion: use `tasknotes_complete_recurring_instance` (MCP) or `POST /api/tasks/:id/complete-instance` (HTTP) when available; on a filesystem-only surface, completions go through the plugin GUI

---

### Creating Domain Views

TaskNotes views are `.base` files in `TaskNotes/Views/`. Agents can read and write them but cannot execute them. Ask the user before creating new view files. The default `kanban-default.base` has reusable formula patterns (urgency scoring, overdue detection).

Full reference: https://tasknotes.dev/views/

---

### Safety Rules

1. Never delete task files - use `status: done` + `completedDate` instead
2. Never modify `dateCreated` - set once on creation, never changed
3. Always update `dateModified` on every edit
4. Always include `tags: [task]` - without it the task is invisible to all views
5. `projects:` must be a wikilink - plain strings are silently broken
6. The project note must exist before a task links to it
7. Read before editing - never overwrite from stale context
8. Unknown projects require a config update first
9. Never edit plugin `.json` config files - Obsidian overwrites them silently on close, and since plugin v4.13.0 TaskNotes refuses to start when it cannot safely read its `data.json`, preserving the file for recovery rather than loading defaults

---

### Cloud-Synced Vaults

Files in cloud-synced vaults may be zero-byte placeholders when not locally downloaded. If a file read returns empty unexpectedly, flag it as a possible sync issue before retrying.

---

## What this skill does not do

- Modify Obsidian settings or plugin state
- Edit `.json` plugin config files
- Schedule or manage reminders (runtime-only plugin behavior)
- Convert inline Markdown checkboxes to tasks (GUI-only NLP workflow)
- Validate status transitions against a configured custom workflow (writes status values directly)
- Access event-driven archiving behavior (plugin-only at runtime)

**Environment-dependent capabilities:** Time tracking, Pomodoro, calendar events, and per-instance recurring task completion are available via MCP or HTTP API when those surfaces are present - but not via filesystem writes alone. What the skill can do depends on what the environment provides. See the surface lookup table in Step 0.

If a request cannot be fulfilled by any available path, decline and explain. Point the user to `references/tasknotes-help.md` for setup guidance.
