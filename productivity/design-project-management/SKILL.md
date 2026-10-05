---
type: Skill
name: design-project-management
description: Manage the NV oOS Pro Toolkit Project Management system — projects, tasks, events, sprints, task plans, task templates, and PM workflow rules. Covers complete project lifecycle (planning → active → completed), task tracking with priorities and effort estimation, sprint planning, event scheduling with attendees, and template-driven task plan generation. Use when managing projects, creating or tracking tasks, planning sprints, scheduling events, generating task plans from templates, assigning work to team members, or troubleshooting project management data.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# NV oOS Pro Toolkit Project Management

The Pro Toolkit Project Management system is a complete project and task management
solution built on WordPress Custom Post Types. It manages the full project delivery
lifecycle: **planning → execution → tracking → completion**. All entities are stored
as CPT records accessible via the `toolkit_cpt` MCP tool.

The system provides seven interlocking entity types: Projects define the scope and
timeline, Tasks break work into trackable units, Events schedule milestones and
meetings, Sprints group tasks into time-boxed iterations, Task Plans capture
template-driven goal-to-task breakdowns, Task Templates define reusable task
blueprints, and PM Workflow Rules automate status transitions and assignments.

## WP-CLI Commands

Key `mcp-ai` WP-CLI commands for project management operations. Run via `terminal`:

| Command | Use for |
|---|---|
| `wp mcp-ai cron` | Check PM automation cron events (deadline reminders, status transitions) |
| `wp mcp-ai queue` | Inspect PM background jobs, retry failed task assignments |
| `wp mcp-ai bulk` | Bulk import/export project tasks or task plans |
| `wp mcp-ai health` | Verify PM system health before running automations |
| `wp mcp-ai log` | View PM workflow rule execution logs |

## When to use this skill

Trigger when ANY of the following is true:

- Creating, updating, or searching projects, tasks, events, sprints, task plans, task templates, or workflow rules.
- Viewing a project dashboard — listing all tasks for a project, checking overdue items, reviewing project status.
- Assigning work: tasks to team members, events with attendees, projects to WP users.
- Planning a sprint — grouping tasks into a time-boxed iteration with a sprint entity.
- Scheduling milestones, deadlines, or meetings as events linked to a project.
- Generating task plans from templates — using `mcp_task_template` placeholders to produce `mcp_task_plan` records.
- Tracking effort — comparing `_task_estimated_effort` vs `_task_actual_effort` to improve estimation accuracy.
- Triaging stale work — identifying projects stuck in planning, overdue tasks, missed milestone dates.
- Setting up PM workflow rules for automatic status transitions or task assignments.
- Filtering tasks by priority, category, status, or assigned user.

## Mental model — projects, tasks, events, sprints

The PM system is organized around a hierarchical structure with cross-connections:

```
PROJECT ──(contains)──→ TASKS ──(grouped into)──→ SPRINTS
   │                       │
   ├── events (milestones) │
   ├── task plans           ├── assigned_to (WP user)
   └── category taxonomy    ├── priority + status + category
                            ├── estimated vs actual effort
                            └── tags (comma-separated)

TASK PLAN ──(generated from)──→ TASK TEMPLATE
   │                                │
   └── _template_id reference       └── _placeholders ({{tokens}})

PM WORKFLOW RULES ── automates status transitions, assignments, and notifications
```

**Relationships:**
- A **Project** (`mcp_ai_project`) is the top-level container. Tasks, events, task plans, and sprints
  all reference their parent project via `_task_project_id`, `_event_project_id`, `_project_id`, etc.
- A **Task** (`mcp_ai_task`) is the unit of work. It belongs to a project, has a priority,
  status, category, assigned user, due date, and effort estimates. Tasks can be tagged
  and categorized via the `mcp_ai_task_category` taxonomy.
- An **Event** (`mcp_ai_event`) represents a scheduled occurrence — meeting, deadline,
  milestone, or reminder. Events can be all-day or time-specific, have a location,
  attendees (array of WP user IDs), and link to a project.
- A **Sprint** (`mcp_ai_sprint`) is a time-boxed work container. Group tasks into sprints
  via `_task_project_id` + filtering.
- A **Task Plan** (`mcp_task_plan`) is a goal-driven task list generated from a
  Task Template. It stores a `_goal`, `_task_count`, and references the source template.
- A **Task Template** (`mcp_task_template`) defines a reusable blueprint with
  `_placeholders` (e.g., `{{project_name}}`, `{{due_date}}`) that get resolved
  when instantiated into a Task Plan.
- **PM Workflow Rules** (`mcp_ai_pm_wf_rule`) define automation logic — status
  transitions, automatic assignments, deadline escalations.

## Entity Types

All PM entities are managed through the **`toolkit_cpt`** MCP tool. Use the appropriate
`post_type` slug for each entity:

| CPT Slug | Label | Supports | Key Meta Fields |
|---|---|---|---|
| `mcp_ai_project` | Projects | title, editor, thumbnail, author | `_project_status`, `_project_start_date`, `_project_end_date`, `_project_assigned_to` |
| `mcp_ai_task` | Tasks | title, editor, author | `_task_status`, `_task_priority`, `_task_category`, `_task_project_id`, `_task_due_date`, `_task_assigned_to`, `_task_tags`, `_task_estimated_effort`, `_task_actual_effort` |
| `mcp_ai_event` | Events | title, editor, author | `_event_start_date`, `_event_end_date`, `_event_start_time`, `_event_end_time`, `_event_all_day`, `_event_type`, `_event_location`, `_event_attendees`, `_event_project_id` |
| `mcp_ai_sprint` | Sprints | title, editor, author | (no declared meta — use content for sprint goal, taxonomy for grouping) |
| `mcp_task_plan` | Task Plans | title, editor, author, custom-fields | `_goal`, `_task_count`, `_project_id`, `_template_id` |
| `mcp_task_template` | Task Templates | title, editor, excerpt, author | `_category`, `_task_count`, `_placeholders` |
| `mcp_ai_pm_wf_rule` | PM Workflow Rules | title, editor, author | (no declared meta — rule logic stored in content or dynamic meta) |

**Taxonomies:** `mcp_ai_project` uses hierarchical `mcp_ai_project_category`. `mcp_ai_task` uses hierarchical `mcp_ai_task_category`.

### Project Meta Fields (detailed)

| Field | Type | Description | Example / Enum |
|---|---|---|---|
| `_project_status` | string | Current project status | `"planning"`, `"active"`, `"on-hold"`, `"completed"`, `"cancelled"` |
| `_project_start_date` | string | Project start date | `"2026-08-01"` (YYYY-MM-DD) |
| `_project_end_date` | string | Target completion date | `"2026-11-15"` (YYYY-MM-DD) |
| `_project_assigned_to` | array | WP user IDs assigned to the project | `[1, 4, 7]` |

### Task Meta Fields (detailed)

| Field | Type | Description | Example / Enum |
|---|---|---|---|
| `_task_status` | string | Current task status | `"todo"`, `"in-progress"`, `"review"`, `"completed"`, `"cancelled"` |
| `_task_priority` | string | Priority level | `"low"`, `"medium"`, `"high"`, `"urgent"` |
| `_task_category` | string | Functional category | `"general"`, `"bug"`, `"feature"`, `"maintenance"`, `"research"`, `"documentation"`, `"design"`, `"testing"` |
| `_task_project_id` | integer | Parent project post ID | `42` |
| `_task_due_date` | string | Due date | `"2026-08-15"` (YYYY-MM-DD) |
| `_task_assigned_to` | integer | WordPress user ID of assignee | `1` |
| `_task_tags` | string | Comma-separated tag list | `"frontend,urgent,client-review"` |
| `_task_estimated_effort` | number | Estimated hours to complete | `4.5` |
| `_task_actual_effort` | number | Actual hours spent | `6.0` |

### Event Meta Fields (detailed)

| Field | Type | Description | Example / Enum |
|---|---|---|---|
| `_event_start_date` | string | Event start date | `"2026-08-14"` (YYYY-MM-DD) |
| `_event_end_date` | string | Event end date | `"2026-08-15"` (YYYY-MM-DD) |
| `_event_start_time` | string | Event start time | `"09:00"` (HH:MM) |
| `_event_end_time` | string | Event end time | `"10:30"` (HH:MM) |
| `_event_all_day` | boolean | All-day event flag | `"1"` (true) or `"0"` (false) — stored as string |
| `_event_type` | string | Event type | `"meeting"`, `"deadline"`, `"milestone"`, `"reminder"`, `"other"` |
| `_event_location` | string | Physical or virtual location | `"Conference Room A"`, `"https://meet.google.com/abc-defg-hij"` |
| `_event_attendees` | array | WP user IDs of attendees | `[1, 4, 7]` |
| `_event_project_id` | integer | Parent project post ID | `42` |

## Available Tools

All PM operations use the **`toolkit_cpt`** MCP tool. This is the single interface
for all CRUD operations across all seven entity types.

### Discovery

```
# List all available PM post types
toolkit_cpt(action: "list_types")

# Get field schema for any PM type
toolkit_cpt(action: "get_schema", post_type: "mcp_ai_project")
toolkit_cpt(action: "get_schema", post_type: "mcp_ai_task")
toolkit_cpt(action: "get_schema", post_type: "mcp_ai_event")
```

### Reading records

```json
// List active projects (most recent first)
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "list_items",
    "post_type": "mcp_ai_project",
    "orderby": "date",
    "order": "DESC",
    "per_page": 20,
    "page": 1
  }
}

// List all tasks for a specific project
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "list_items",
    "post_type": "mcp_ai_task",
    "filters": [
      { "key": "_task_project_id", "value": "42" }
    ]
  }
}

// Find high-priority overdue tasks for a project
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "list_items",
    "post_type": "mcp_ai_task",
    "filters": [
      { "key": "_task_priority", "value": "urgent" },
      { "key": "_task_status", "value": "todo" },
      { "key": "_task_project_id", "value": "42" }
    ]
  }
}

// Get a single task or project with full details
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "get_item",
    "post_type": "mcp_ai_task",
    "item_id": 567
  }
}
```

### Creating records

```json
// Create a new project
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "create_item",
    "post_type": "mcp_ai_project",
    "fields": {
      "title": "Website Redesign Q3 2026",
      "content": "<h2>Overview</h2><p>Complete redesign of the marketing site...</p>",
      "_project_status": "planning",
      "_project_start_date": "2026-08-01",
      "_project_end_date": "2026-11-15",
      "_project_assigned_to": [1, 4, 7]
    }
  }
}

// Create a task linked to a project
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "create_item",
    "post_type": "mcp_ai_task",
    "fields": {
      "title": "Build homepage hero component",
      "_task_status": "todo",
      "_task_priority": "high",
      "_task_category": "feature",
      "_task_project_id": 42,
      "_task_due_date": "2026-08-15",
      "_task_assigned_to": 4,
      "_task_tags": "frontend,phase-1",
      "_task_estimated_effort": 8
    }
  }
}

// Schedule a milestone event
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "create_item",
    "post_type": "mcp_ai_event",
    "fields": {
      "title": "Sprint 3 Review",
      "_event_start_date": "2026-08-28",
      "_event_end_date": "2026-08-28",
      "_event_start_time": "14:00",
      "_event_end_time": "15:00",
      "_event_all_day": "0",
      "_event_type": "milestone",
      "_event_location": "https://meet.google.com/xyz-abc-def",
      "_event_attendees": [1, 4, 7],
      "_event_project_id": 42
    }
  }
}
```

### Updating records

```json
// Move a task to in-progress and assign
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "update_item",
    "post_type": "mcp_ai_task",
    "item_id": 567,
    "fields": {
      "_task_status": "in-progress",
      "_task_assigned_to": 4
    }
  }
}

// Log actual effort and complete a task
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "update_item",
    "post_type": "mcp_ai_task",
    "item_id": 567,
    "fields": {
      "_task_status": "completed",
      "_task_actual_effort": 10.5
    }
  }
}

// Change project status
{
  "name": "toolkit_cpt",
  "arguments": {
    "action": "update_item",
    "post_type": "mcp_ai_project",
    "item_id": 42,
    "fields": {
      "_project_status": "active",
      "_project_start_date": "2026-08-05"
    }
  }
}
```

**⚠️ Warning:** Deleting is permanent. For tasks, prefer `_task_status: "cancelled"` to preserve history.
For projects, use `_project_status: "cancelled"` rather than deleting.

## Common Workflows

### Project lifecycle management

```
1. Create project:     create_item(mcp_ai_project, _project_status: "planning")
2. Add tasks:          create_item(mcp_ai_task, _task_project_id: <project_id>) for each work item
3. Schedule events:    create_item(mcp_ai_event, _event_project_id: <project_id>) for milestones
4. Activate:           update_item(mcp_ai_project, _project_status: "active")
5. Track progress:     list_items(mcp_ai_task, filters by _task_status) to monitor completion
6. Complete:           update_item(mcp_ai_project, _project_status: "completed")
```

### Task management workflow

```
1. Discover tasks:     list_items(mcp_ai_task, filters by assignee or status)
2. Start work:         update_item(mcp_ai_task, _task_status: "in-progress")
3. Submit for review:  update_item(mcp_ai_task, _task_status: "review")
4. Complete:           update_item(mcp_ai_task, _task_status: "completed", _task_actual_effort: <hours>)
5. Cancel if needed:   update_item(mcp_ai_task, _task_status: "cancelled")
```

### Sprint planning

```
1. Define sprint:   create_item(mcp_ai_sprint, title: "Sprint 4 (Aug 25 - Sep 7)")
2. Select tasks:    list_items(mcp_ai_task, filters: [{key: "_task_status", value: "todo"}])
3. Track velocity:  At sprint end, count completed tasks and sum _task_actual_effort.
```

### Scheduling events for a project

```
1. Create milestones:  create_item(mcp_ai_event, _event_type: "milestone", _event_project_id: <id>)
2. Schedule meetings:  create_item(mcp_ai_event, _event_type: "meeting", _event_attendees: [1,4])
3. Set reminders:      create_item(mcp_ai_event, _event_type: "reminder", _event_project_id: <id>)
4. View timeline:      list_items(mcp_ai_event, filters: [{key: "_event_project_id", value: "<id>"}])
```

### Task plan generation from template

```
1. Discover templates: list_items(mcp_task_template)
2. Read a template:    get_item(mcp_task_template, item_id: <id>)
                       → Note the _placeholders array: ["{{project_name}}", "{{launch_date}}", ...]
3. Create task plan:   create_item(mcp_task_plan, fields: {
                         "title": "Launch Plan - Client X",
                         "_goal": "Complete website launch for Client X by Sep 30",
                         "_task_count": 12,
                         "_project_id": 42,
                         "_template_id": <template_id>
                       })
4. Resolve placeholders: Use the template's _placeholders to generate actual tasks
                         via create_item(mcp_ai_task) for each template step.
```

### PM health check / triage

```
1. Stale projects:     list_items(mcp_ai_project, filters: [{key: "_project_status", value: "planning"}])
                       → Projects in planning for 2+ weeks need activation or cancellation.

2. Overdue tasks:      list_items(mcp_ai_task, filters: [
                         {key: "_task_due_date", value: "<today>", compare: "<"},
                         {key: "_task_status", value: "completed", compare: "!="}
                       ])

3. Unassigned tasks:   list_items(mcp_ai_task, filters: [{key: "_task_assigned_to", compare: "NOT EXISTS"}])

4. Effort variance:    Compare _task_estimated_effort vs _task_actual_effort on completed tasks.
                       Tasks where actual > 2x estimated indicate estimation issues.

5. Upcoming deadlines: list_items(mcp_ai_event, filters: [
                         {key: "_event_start_date", value: "<today + 7 days>", compare: "<"},
                         {key: "_event_type", value: "deadline"}
                       ])
```

## Critical Rules

- **Always call `get_schema` first** before creating or updating a record to verify available field keys and types.
- **Tasks belong to a project** — always set `_task_project_id` when creating a task. Orphan tasks (no project) can't be found in project-level views.
- **Events store boolean as string** — `_event_all_day` uses `"1"` / `"0"`, not `true` / `false`.
- **Dates use YYYY-MM-DD format** — `_project_start_date`, `_project_end_date`, `_task_due_date`, `_event_start_date`, `_event_end_date` all expect this format.
- **Times use HH:MM format** — `_event_start_time` and `_event_end_time` expect 24-hour format (e.g., `"14:00"`).
- **`_task_tags` is a comma-separated string** — not a JSON array. Use `"frontend,urgent"` not `["frontend", "urgent"]`.
- **Effort values are numbers** — `_task_estimated_effort` and `_task_actual_effort` are stored as numeric values (hours), not strings.
- **`_project_assigned_to` and `_event_attendees` are arrays of integers** — WordPress user IDs, not display names.
- **Never delete projects or tasks** — use `_project_status: "cancelled"` or `_task_status: "cancelled"` to preserve history and audit trail.
- **Task Plans reference templates by ID** — `_template_id` must point to an existing `mcp_task_template` record.
- **Placeholders use `{{double_braces}}`** — consistent with Pro Workflow Builder template variable syntax.

## Common Mistakes

```
WRONG — creating a task without a project link
{ "action": "create_item", "post_type": "mcp_ai_task",
  "fields": { "title": "Fix login bug", "_task_status": "todo" } }
// Orphan task — no _task_project_id. Can't be surfaced in project views.

RIGHT — always link tasks to their project
{ "action": "create_item", "post_type": "mcp_ai_task",
  "fields": { "title": "Fix login bug", "_task_status": "todo",
  "_task_priority": "urgent", "_task_category": "bug",
  "_task_project_id": 42, "_task_assigned_to": 4 } }

WRONG — using boolean true/false for _event_all_day
{ "fields": { "_event_all_day": true } }
// Stored as "1", not 1. Booleans may serialize inconsistently.

RIGHT — use string "1" or "0"
{ "fields": { "_event_all_day": "1" } }

WRONG — passing _task_tags as a JSON array
{ "fields": { "_task_tags": ["frontend", "phase-1"] } }
// This will serialize to a PHP array in meta, not the expected comma-separated string.

RIGHT — use comma-separated string
{ "fields": { "_task_tags": "frontend,phase-1" } }

WRONG — skipping the get_schema call before creating a record
// Some meta fields may be added dynamically. Always call get_schema first.

WRONG — deleting a completed task instead of archiving
{ "action": "delete_item", "post_type": "mcp_ai_task", "item_id": 567 }
// Destroys effort data and audit trail.

RIGHT — cancel to preserve history
{ "action": "update_item", "post_type": "mcp_ai_task", "item_id": 567,
  "fields": { "_task_status": "cancelled" } }

WRONG — using date format "08/15/2026" or "2026/08/15"
// All date fields expect YYYY-MM-DD format.

WRONG — setting _task_actual_effort as a string
{ "fields": { "_task_actual_effort": "10.5" } }
// Effort fields are numeric. Use 10.5, not "10.5".
```

## Cross-References

- Run `design-crm` to link projects to CRM deals or companies — track billable projects against client accounts.
- Run `design-pro-workflow-builder` to automate PM workflows (auto-assign tasks, escalate overdue items, generate status reports).
- Run `design-pro-schedule-manager` to schedule recurring PM tasks (daily standup reminders, weekly status reports, sprint retrospectives).
- Run `design-document-generation` to create project status reports, sprint summaries, and milestone documents from PM data.
- Run `design-deep-research` to research technical requirements or vendors before creating project plans.
- Run `design-content-calendar` to align content-related tasks with the editorial calendar.
- Run `wp-security-audit` on any PM automation callbacks — task assignment and project access must be capability-controlled.

## What This Skill Does NOT Cover

- CRM integration (linking projects to deals/companies) — use `design-crm` for CRM-side operations.
- Workflow automation design — use `design-pro-workflow-builder` for DAG-based PM automation.
- Recurring schedule management — use `design-pro-schedule-manager` for cron-based PM scheduling.
- Document generation (reports, summaries) — use `design-document-generation` for PDF/DOCX output.
- Remote WordPress PM access — use `nv_oos_console_agent_remote_wp_connection` for multi-site PM.
- Time tracking beyond effort estimates — actual time logging requires a third-party time tracker.
- Gantt charts or Kanban board rendering — the `toolkit_cpt` tool returns structured data; visualization is handled by the Pro Toolkit admin UI.
- WP user management — user IDs referenced by `_task_assigned_to`, `_project_assigned_to`, and `_event_attendees` must exist in WordPress.

## References

- NV oOS Pro Toolkit Project Management admin page: `/wp-admin/admin.php?page=nvoos-pro-toolkit-pm`
- `toolkit_cpt` MCP tool — the primary interface for all PM operations.
- Pro Workflow Builder: `/wp-admin/admin.php?page=nvoos-pro-workflow-builder` (PM automation presets)
- Pro Schedule Manager: `/wp-admin/admin.php?page=nvoos-pro-schedule-manager` (recurring PM tasks)
