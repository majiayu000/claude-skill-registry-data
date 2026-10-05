---
name: asana
description: Interact with the Asana REST API using a Personal Access Token in ASANA_PAT. Covers core work management plus portfolios, goals, status updates, webhooks, events, audit logs, attachments, batch requests, jobs, and newer API families.
---

Interact with the Asana REST API directly using a Personal Access Token:

- Store the token in `ASANA_PAT`.
- Send it via the `Authorization: Bearer $ASANA_PAT` header.
- Never hardcode credentials.

## Canonical references

- Main REST reference: `https://developers.asana.com/reference/rest-api-reference`
- Raw OpenAPI spec: `https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml`
- Base URL: `https://app.asana.com/api/1.0`

## Quick auth check

```bash
[ -z "$ASANA_PAT" ] && echo "Error: ASANA_PAT not set" || echo "OK: ASANA_PAT is set"

curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/workspaces" | jq .
```

## Core API conventions

### Response shape

Most Asana responses are wrapped in a top-level `data` key:

```json
{ "data": { ... } }
```

For list endpoints:

```json
{ "data": [ ... ], "next_page": { ... } }
```

### Request shape

Most JSON create/update endpoints expect a top-level `data` object:

```json
{
  "data": {
    "name": "Example"
  }
}
```

### IDs

Asana uses string GIDs everywhere:

- user GIDs
- workspace GIDs
- team GIDs
- project GIDs
- task GIDs
- portfolio GIDs
- goal GIDs

### Output options

Common query options:

- `opt_fields=field1,field2,...`
- `pretty=true`

`opt_fields` is recommended since many endpoints return compact objects by default.

### Pagination

Common list pagination params:

- `limit` — page size, 1 to 100
- `offset` — **opaque pagination token**, not a numeric index

Do not guess offsets. Reuse the token returned by the previous page.

## Coverage map

### Commonly used core resources

- Workspaces
- Users
- Teams
- Projects
- Sections
- Tasks
- Subtasks
- Stories/comments
- Tags
- Custom fields
- Attachments

### Higher-level planning / reporting resources

- Portfolios
- Goals
- Goal relationships
- Project statuses
- Status updates
- User task lists
- Time tracking entries
- Jobs

### Eventing / integration resources

- Webhooks
- Events
- Audit log API
- Batch API
- Exports

### Additional API families present in the official spec

The current Asana API also includes these resource families:

- Access requests
- Allocations
- Budgets
- Custom field settings
- Custom types
- Memberships
- Ooo entries
- Organization exports
- Portfolio memberships
- Project briefs
- Project memberships
- Project portfolio settings
- Project templates
- Rates
- Reactions
- Roles
- Rules
- SSPM
- Task templates
- Team memberships
- Time periods
- Time tracking categories
- Timesheet approval statuses
- Typeahead
- Workspace memberships

## Recommended discovery flow

When IDs are unknown, discover them in this order:

1. List workspaces
2. List users and teams in the workspace
3. List projects in the workspace or team
4. List sections in a project
5. List tasks in the project or section
6. Then query stories, tags, custom fields, attachments, portfolios, goals, etc.

## Workspaces, users, teams

### List workspaces

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/workspaces" | jq '.data'
```

### List users

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/users" | jq '.data'
```

### Get a user

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/users/USER_GID" | jq '.data'
```

### List users in a workspace or organization

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/workspaces/WORKSPACE_GID/users" | jq '.data'
```

### List teams in a workspace

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/workspaces/WORKSPACE_GID/teams" | jq '.data'
```

### Get a team

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/teams/TEAM_GID" | jq '.data'
```

### List users in a team

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/teams/TEAM_GID/users" | jq '.data'
```

## Projects and sections

### List projects

```bash
# Workspace-scoped
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/workspaces/WORKSPACE_GID/projects" | jq '.data'

# Team-scoped
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/teams/TEAM_GID/projects" | jq '.data'

# Generic projects endpoint with filters
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/projects?workspace=WORKSPACE_GID" | jq '.data'
```

### Get a project

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/projects/PROJECT_GID" | jq '.data'
```

### Create or update a project

```bash
# Create in workspace
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  -H "Content-Type: application/json" \
  -X POST \
  "https://app.asana.com/api/1.0/workspaces/WORKSPACE_GID/projects" \
  -d '{"data":{"name":"Project Name"}}' | jq '.data'

# Update
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  -H "Content-Type: application/json" \
  -X PUT \
  "https://app.asana.com/api/1.0/projects/PROJECT_GID" \
  -d '{"data":{"name":"Updated Project Name"}}' | jq '.data'
```

### List sections in a project

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/projects/PROJECT_GID/sections" | jq '.data'
```

### Create a section in a project

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  -H "Content-Type: application/json" \
  -X POST \
  "https://app.asana.com/api/1.0/projects/PROJECT_GID/sections" \
  -d '{"data":{"name":"To Do"}}' | jq '.data'
```

## Tasks

### Get a task

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/tasks/TASK_GID" | jq '.data'
```

Use `opt_fields` to request specific fields:

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/tasks/TASK_GID?opt_fields=name,completed,assignee.name,due_on,projects.name,tags.name,custom_fields.name,custom_fields.display_value" | jq '.data'
```

### List tasks in a project or section

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/projects/PROJECT_GID/tasks" | jq '.data'
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/sections/SECTION_GID/tasks" | jq '.data'
```

### Search tasks in a workspace

This is Asana's main workspace-level search endpoint.

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/workspaces/WORKSPACE_GID/tasks/search?completed=false&assignee=me" | jq '.data'
```

Commonly used search filters:

- `text`
- `assignee`
- `project`
- `section`
- `tag`
- `completed`
- `is_subtask`
- `due_on`
- `due_on.before`
- `due_on.after`
- `modified_at.before`
- `modified_at.after`
- `created_at.before`
- `created_at.after`

### Create a task

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  -H "Content-Type: application/json" \
  -X POST \
  "https://app.asana.com/api/1.0/tasks" \
  -d '{"data":{"name":"New task","workspace":"WORKSPACE_GID"}}' | jq '.data'
```

Common task creation fields from the schema:

- `name`
- `workspace`
- `assignee`
- `projects`
- `tags`
- `notes`
- `html_notes`
- `due_on`
- `due_at`
- `start_on`
- `start_at`
- `custom_fields`
- `parent`
- `followers`

### Update a task

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  -H "Content-Type: application/json" \
  -X PUT \
  "https://app.asana.com/api/1.0/tasks/TASK_GID" \
  -d '{"data":{"name":"Updated task","completed":false}}' | jq '.data'
```

### Subtasks

```bash
# List subtasks
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/tasks/TASK_GID/subtasks" | jq '.data'

# Create subtask
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  -H "Content-Type: application/json" \
  -X POST \
  "https://app.asana.com/api/1.0/tasks/TASK_GID/subtasks" \
  -d '{"data":{"name":"Subtask name"}}' | jq '.data'
```

## Stories / comments

In Asana, comments are stories.

### Get task stories

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/tasks/TASK_GID/stories" | jq '.data'
```

### Create a comment on a task

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  -H "Content-Type: application/json" \
  -X POST \
  "https://app.asana.com/api/1.0/tasks/TASK_GID/stories" \
  -d '{"data":{"text":"Hello from the API"}}' | jq '.data'
```

The schema also supports `html_text` for formatted comments.

## Tags and custom fields

### List tags in a workspace

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/workspaces/WORKSPACE_GID/tags" | jq '.data'
```

### Get a tag or its tasks

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/tags/TAG_GID" | jq '.data'
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/tags/TAG_GID/tasks" | jq '.data'
```

### List custom fields in a workspace

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/workspaces/WORKSPACE_GID/custom_fields" | jq '.data'
```

### Get custom field settings for a project

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/projects/PROJECT_GID/custom_field_settings" | jq '.data'
```

Other custom field settings endpoints exist for portfolios, goals, and teams.

## Portfolios, goals, statuses

### Portfolios

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/portfolios?workspace=WORKSPACE_GID" | jq '.data'
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/portfolios/PORTFOLIO_GID" | jq '.data'
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/portfolios/PORTFOLIO_GID/items" | jq '.data'
```

### Goals

```bash
# Filter goals by workspace / team / portfolio / project / task
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/goals?workspace=WORKSPACE_GID" | jq '.data'

# Get goal
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/goals/GOAL_GID" | jq '.data'
```

### Status updates

```bash
# parent can be a project, goal, or portfolio
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/status_updates?parent=PARENT_GID" | jq '.data'
```

### Project statuses

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/projects/PROJECT_GID/project_statuses" | jq '.data'
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/project_statuses/PROJECT_STATUS_GID" | jq '.data'
```

## Attachments

### List attachments on an object

`parent` is required and can point to a task, project, or project brief.

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/attachments?parent=TASK_GID" | jq '.data'
```

### Get an attachment

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/attachments/ATTACHMENT_GID" | jq '.data'
```

### Upload an attachment

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  -F "parent=TASK_GID" \
  -F "file=@/path/to/file.pdf;type=application/pdf" \
  "https://app.asana.com/api/1.0/attachments" | jq '.data'
```

The attachment API also supports external attachments via `resource_subtype=external`, `parent`, `name`, and `url`.

## Webhooks and events

### List webhooks

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/webhooks?workspace=WORKSPACE_GID" | jq '.data'
```

Optional webhook listing filters include `workspace` and `resource`.

### Create a webhook

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  -H "Content-Type: application/json" \
  -X POST \
  "https://app.asana.com/api/1.0/webhooks" \
  -d '{"data":{"resource":"PROJECT_GID","target":"https://example.com/asana-webhook"}}' | jq '.data'
```

The schema also supports webhook `filters`.

### Resource events

Asana's events API is for incremental sync using a sync token.

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/events?resource=PROJECT_GID" | jq .
```

Then reuse the returned `sync` token:

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/events?resource=PROJECT_GID&sync=SYNC_TOKEN" | jq .
```

There is also a workspace-scoped events endpoint:

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/workspaces/WORKSPACE_GID/events" | jq .
```

Important notes from the official reference:

- Resource events use a `sync` token for incremental updates; if the token is too old, Asana returns `412`.
- Event streams cap a single sync token at 100 events for resources and 1,000 events for workspaces.

### Audit log events

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/workspaces/WORKSPACE_GID/audit_log_events" | jq '.data'
```

## Batch API

Batch lets you send multiple requests in one HTTP call.

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  -H "Content-Type: application/json" \
  -X POST \
  "https://app.asana.com/api/1.0/batch" \
  -d '{
    "data": {
      "actions": [
        {
          "method": "get",
          "relative_path": "/tasks/TASK_GID_1",
          "options": {"fields": ["name", "completed"]}
        },
        {
          "method": "get",
          "relative_path": "/tasks/TASK_GID_2",
          "options": {"fields": ["name", "completed"]}
        }
      ]
    }
  }' | jq '.data'
```

Batch action parameters:

- `relative_path` is relative to `/api/1.0` and must not contain query parameters.
- Place standard parameters in `data`, and pagination or output configurations in `options`.

## User task lists, time tracking entries, jobs

### User task lists

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/user_task_lists/USER_TASK_LIST_GID" | jq '.data'
```

You can also navigate from a user:

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/users/USER_GID/user_task_list" | jq '.data'
```

### Time tracking entries for a task

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/tasks/TASK_GID/time_tracking_entries" | jq '.data'
```

### Create a time tracking entry for a task

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  -H "Content-Type: application/json" \
  -X POST \
  "https://app.asana.com/api/1.0/tasks/TASK_GID/time_tracking_entries" \
  -d '{"data":{"duration_minutes":30,"description":"API time entry"}}' | jq '.data'
```

The schema also supports `entered_on`, `attributable_to`, `billable_status`, and `categories`.

### Poll long-running jobs

```bash
curl -fsS \
  -H "Authorization: Bearer $ASANA_PAT" \
  "https://app.asana.com/api/1.0/jobs/JOB_GID" | jq '.data'
```

Useful for polling asynchronous APIs like exports and larger operations.

## Exports

The API includes endpoints such as `POST /exports/graph`, `POST /exports/resource`, and `POST /organization_exports`, which typically return asynchronous jobs that should be polled via job or export endpoints.

## Common URL / ID patterns

- In typical resource URLs (`https://app.asana.com/0/PROJECT_GID/TASK_GID`), the Task GID is the last path segment and the Project GID is the second-to-last.

```bash
echo "https://app.asana.com/0/123456789/9876543210" | sed 's#.*/##'
# => 9876543210

echo "https://app.asana.com/0/123456789/9876543210" | awk -F'/' '{print $(NF-1)}'
# => 123456789
```

## Error handling

| Status | Meaning                                  |
| ------ | ---------------------------------------- |
| `200`  | Success                                  |
| `201`  | Created                                  |
| `400`  | Bad request                              |
| `401`  | Unauthorized / invalid PAT               |
| `403`  | Forbidden                                |
| `404`  | Not found                                |
| `412`  | Invalid or expired sync token for events |
| `429`  | Rate limited                             |
| `5xx`  | Server error                             |

Use `curl -fsS` to fail fast and surface HTTP errors immediately.

## Best practices

1. **Use Bearer authentication**: Send `Authorization: Bearer $ASANA_PAT` on every request.
2. **Wrap JSON writes**: Always wrap request payloads in a top-level `data` object.
3. **Use `opt_fields` aggressively**: Request only the specific fields you need to avoid over-fetching.
4. **Treat `offset` as opaque**: Treat pagination offsets as opaque tokens, not numeric indexes.
5. **Default to incomplete tasks** unless the user explicitly requests completed ones.
6. **Use workspace task search** when IDs are unknown and you need to find tasks by text or filters.
7. **Use stories for comments**: Task comments are created and retrieved via the `/tasks/{task_gid}/stories` endpoint.
8. **Use jobs for async workflows**: Poll the jobs endpoint for asynchronous tasks like exports.
9. **Prefer events/webhooks over polling** to sync data without repeatedly requesting large collections.
