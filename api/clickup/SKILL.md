---
name: clickup
description: Interact with the ClickUp HTTP API using a Personal Access Token in CLICKUP_PAT. Covers v2 core resources plus v3 Docs, Chat, attachments, ACLs, and audit logs. Use the API directly, not MCP.
---

Use ClickUp's HTTP API directly, not MCP.

This skill is **PAT-only**:

- Use a ClickUp **Personal Access Token** in `CLICKUP_PAT`
- Send it as `Authorization: $CLICKUP_PAT` (do not use `Bearer` for PAT auth)
- Personal tokens begin with `pk_`

## Canonical references

- Main docs: `https://developer.clickup.com/`
- Authentication: `https://developer.clickup.com/docs/authentication`
- Raw OpenAPI v2: `https://developer.clickup.com/openapi/clickup-api-v2-reference.json`
- Raw OpenAPI v3: `https://developer.clickup.com/openapi/ClickUp_PUBLIC_API_V3.yaml`

## Base URLs

- v2 core API: `https://api.clickup.com/api/v2`
- v3 API: `https://api.clickup.com/api/v3`

## Quick auth check

```bash
[ -z "$CLICKUP_PAT" ] && echo "Error: CLICKUP_PAT not set" || echo "OK: CLICKUP_PAT is set"

curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/user" | jq .
```

## API coverage map

ClickUp exposes two public API surfaces:

### v2: core work management

Use v2 for most existing ClickUp resources:

- Authorized user + workspaces
- Spaces, folders, lists, views
- Tasks, task relationships, checklists, attachments
- Comments
- Members, users, guests, user groups, roles
- Custom fields, tags, custom task types
- Goals
- Time tracking
- Templates
- Shared hierarchy
- Webhooks

### v3: newer resources

Use v3 for the newer resource families:

- Docs
- Chat
- Generic attachments endpoints
- Privacy/access control lists (ACLs)
- Audit logs
- A few workspace-scoped task helpers

## Important ID note

ClickUp uses both `team_id` and `workspace_id` across docs/specs; both refer to the same top-level workspace identifier. The v2 spec also inconsistently uses both `team_id` and `team_Id` in path templates. Treat them as the same value.

## Recommended discovery flow

When IDs are unknown, discover them in this order:

1. Get the authorized user
2. List workspaces
3. List spaces in a workspace
4. List folders and folderless lists in a space
5. List lists in a folder
6. List views if needed
7. Query tasks, comments, docs, chat, time entries, etc.

## Authorized user and workspaces

### Get authorized user

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/user" | jq .
```

### List authorized workspaces

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/team" | jq '.teams'
```

### Get workspace plan

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/team/TEAM_ID/plan" | jq .
```

### Get workspace seats

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/team/TEAM_ID/seats" | jq .
```

## Hierarchy: spaces, folders, lists, views

### List spaces in a workspace

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/team/TEAM_ID/space?archived=false" | jq .
```

### Get a space

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/space/SPACE_ID" | jq .
```

### List folders in a space

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/space/SPACE_ID/folder?archived=false" | jq .
```

### Get a folder

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/folder/FOLDER_ID" | jq .
```

### List folderless lists in a space

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/space/SPACE_ID/list?archived=false" | jq .
```

### List lists in a folder

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/folder/FOLDER_ID/list?archived=false" | jq .
```

### Get a list

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/list/LIST_ID" | jq .
```

### List views

```bash
# Workspace / Everything views
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/team/TEAM_ID/view" | jq .

# Space views
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/space/SPACE_ID/view" | jq .

# Folder views
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/folder/FOLDER_ID/view" | jq .

# List views
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/list/LIST_ID/view" | jq .
```

### Get a view or its tasks

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/view/VIEW_ID" | jq .
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/view/VIEW_ID/task" | jq .
```

## Tasks

### Get a task

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/task/TASK_ID" | jq .
```

Useful query parameters:

- `include_subtasks=true`
- `include_markdown_description=true`
- `custom_fields=true`
- `custom_task_ids=true&team_id=TEAM_ID` when using custom task IDs

Example:

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/task/TASK_ID?include_subtasks=true&include_markdown_description=true" | jq .
```

### List tasks in a list

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/list/LIST_ID/task?archived=false&subtasks=true&include_closed=false" | jq .
```

Common filters supported by `GET /list/{list_id}/task`:

- `page`
- `order_by`
- `reverse`
- `statuses[]`
- `assignees[]`
- `watchers[]`
- `tags[]`
- `subtasks`
- `include_closed`
- `due_date_gt`, `due_date_lt`
- `date_created_gt`, `date_created_lt`
- `date_updated_gt`, `date_updated_lt`
- `date_done_gt`, `date_done_lt`
- `custom_fields`
- `custom_items[]`

### Get filtered workspace tasks

This is the main workspace-level task query in v2. It filters tasks across spaces, folders, and lists.

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/team/TEAM_ID/task?include_closed=false&page=0" | jq .
```

Common filters supported by `GET /team/{team_Id}/task`:

- `page`
- `order_by`
- `reverse`
- `subtasks`
- `space_ids[]`
- `project_ids[]`
- `list_ids[]`
- `statuses[]`
- `assignees[]`
- `tags[]`
- `parent`
- `include_closed`
- `include_markdown_description`
- `custom_fields`
- `custom_items[]`
- `due_date_gt`, `due_date_lt`
- `date_created_gt`, `date_created_lt`
- `date_updated_gt`, `date_updated_lt`
- `date_done_gt`, `date_done_lt`

### Create or update tasks

> **Always use `markdown_content` (create) or `markdown_description` (update) for task descriptions.** The `description` field treats content as plain text and does not render Markdown, whereas `markdown_content` and `markdown_description` render rich text in the ClickUp UI. If both are provided, `markdown_content` takes precedence.

```bash
# Create task in a list (with Markdown description)
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  -H "Content-Type: application/json" \
  -X POST \
  "https://api.clickup.com/api/v2/list/LIST_ID/task" \
  -d '{"name":"New task","markdown_content":"## Overview\nDetails here."}' | jq .

# Update task (with Markdown description)
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  -H "Content-Type: application/json" \
  -X PUT \
  "https://api.clickup.com/api/v2/task/TASK_ID" \
  -d '{"name":"Updated task name","markdown_description":"## Updated\nNew details."}' | jq .
```

### Task relationships

```bash
# Add dependency
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  -H "Content-Type: application/json" \
  -X POST \
  "https://api.clickup.com/api/v2/task/TASK_ID/dependency" \
  -d '{"depends_on":"OTHER_TASK_ID"}' | jq .

# Link tasks
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  -X POST "https://api.clickup.com/api/v2/task/TASK_ID/link/OTHER_TASK_ID" | jq .
```

### Checklists

```bash
# Create checklist
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  -H "Content-Type: application/json" \
  -X POST \
  "https://api.clickup.com/api/v2/task/TASK_ID/checklist" \
  -d '{"name":"Checklist"}' | jq .
```

### Task members

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/task/TASK_ID/member" | jq .
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/list/LIST_ID/member" | jq .
```

### Task attachment upload (v2)

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  -F "attachment=@/path/to/file" \
  "https://api.clickup.com/api/v2/task/TASK_ID/attachment" | jq .
```

## Comments

### Get task comments

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/task/TASK_ID/comment" | jq .
```

Optional pagination-style params:

- `start`
- `start_id`
- `custom_task_ids=true&team_id=TEAM_ID` if using custom task IDs

### Get list comments

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/list/LIST_ID/comment" | jq .
```

### Get view comments

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/view/VIEW_ID/comment" | jq .
```

### Get threaded replies for a comment

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/comment/COMMENT_ID/reply" | jq .
```

### Create comments

```bash
# Task comment
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  -H "Content-Type: application/json" \
  -X POST \
  "https://api.clickup.com/api/v2/task/TASK_ID/comment" \
  -d '{"comment_text":"Hello from the API","notify_all":true}' | jq .

# Threaded reply
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  -H "Content-Type: application/json" \
  -X POST \
  "https://api.clickup.com/api/v2/comment/COMMENT_ID/reply" \
  -d '{"comment_text":"Replying in thread","notify_all":true}' | jq .
```

## Custom fields, tags, custom task types, roles

### Custom fields

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/team/TEAM_ID/field" | jq .
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/space/SPACE_ID/field" | jq .
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/folder/FOLDER_ID/field" | jq .
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/list/LIST_ID/field" | jq .
```

### Set a task custom field value

The body shape depends on the field type. For simple text-like fields:

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  -H "Content-Type: application/json" \
  -X POST \
  "https://api.clickup.com/api/v2/task/TASK_ID/field/FIELD_ID" \
  -d '{"value":"example"}' | jq .
```

### Tags

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/space/SPACE_ID/tag" | jq .
```

```bash
# Add tag to task
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  -X POST "https://api.clickup.com/api/v2/task/TASK_ID/tag/TAG_NAME" | jq .

# Remove tag from task
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  -X DELETE "https://api.clickup.com/api/v2/task/TASK_ID/tag/TAG_NAME" | jq .
```

### Custom task types

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/team/TEAM_ID/custom_item" | jq .
```

### Custom roles

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/team/TEAM_ID/customroles?include_members=true" | jq .
```

## Goals

### List goals

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/team/TEAM_ID/goal?include_completed=false" | jq .
```

### Get a goal

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/goal/GOAL_ID" | jq .
```

### Key results

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/key_result/KEY_RESULT_ID" | jq .
```

## Time tracking

### Get time entries in a date range

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/team/TEAM_ID/time_entries?start_date=START_MS&end_date=END_MS" | jq .
```

Useful filters:

- `assignee`
- `space_id`
- `folder_id`
- `list_id`
- `task_id`
- `is_billable`
- `include_task_tags=true`
- `include_location_names=true`
- `include_approval_history=true`
- `include_approval_details=true`

### Get the currently running time entry

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/team/TEAM_ID/time_entries/current" | jq .
```

### Get a single time entry or its history

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/team/TEAM_ID/time_entries/TIMER_ID" | jq .
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/team/TEAM_ID/time_entries/TIMER_ID/history" | jq .
```

### Start or stop a timer

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  -H "Content-Type: application/json" \
  -X POST \
  "https://api.clickup.com/api/v2/team/TEAM_ID/time_entries/start" \
  -d '{"description":"Working on task"}' | jq .

curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  -H "Content-Type: application/json" \
  -X POST \
  "https://api.clickup.com/api/v2/team/TEAM_ID/time_entries/stop" \
  -d '{}' | jq .
```

### Legacy task time tracking endpoints

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/task/TASK_ID/time" | jq .
```

## Templates, shared hierarchy, members, users, guests, groups

### Shared hierarchy

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/team/TEAM_ID/shared" | jq .
```

### Templates

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/team/TEAM_ID/taskTemplate?page=0" | jq .
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/team/TEAM_ID/list_template" | jq .
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/team/TEAM_ID/folder_template" | jq .
```

### Users, guests, groups

```bash
# User details in workspace
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/team/TEAM_ID/user/USER_ID" | jq .

# Guest details in workspace
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/team/TEAM_ID/guest/GUEST_ID" | jq .

# List user groups
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/group" | jq .
```

## Webhooks

### List workspace webhooks

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v2/team/TEAM_ID/webhook" | jq .
```

### Create a webhook

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  -H "Content-Type: application/json" \
  -X POST \
  "https://api.clickup.com/api/v2/team/TEAM_ID/webhook" \
  -d '{"endpoint":"https://example.com/clickup-webhook","events":["taskCreated"]}' | jq .
```

## Docs API (v3)

Docs live in **v3**. Avoid using incorrect `/workflow/.../doc` style URLs, and use workspace-scoped v3 endpoints instead.

### Search docs in a workspace

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v3/workspaces/WORKSPACE_ID/docs?archived=false&deleted=false&limit=50" | jq .
```

Useful filters:

- `id`
- `creator`
- `deleted`
- `archived`
- `parent_id`
- `parent_type`
- `limit`
- `cursor`
- `next_cursor`

### Fetch a doc

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v3/workspaces/WORKSPACE_ID/docs/DOC_ID" | jq .
```

### Get doc page listing

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v3/workspaces/WORKSPACE_ID/docs/DOC_ID/page_listing?max_page_depth=10" | jq .
```

### Get doc pages

`content_format` supports `text/md` and `text/plain`.

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v3/workspaces/WORKSPACE_ID/docs/DOC_ID/pages?content_format=text/md" | jq .
```

### Get a specific page

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v3/workspaces/WORKSPACE_ID/docs/DOC_ID/pages/PAGE_ID?content_format=text/md" | jq .
```

### Create docs/pages

```bash
# Create a doc
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  -H "Content-Type: application/json" \
  -X POST \
  "https://api.clickup.com/api/v3/workspaces/WORKSPACE_ID/docs" \
  -d '{"name":"New doc"}' | jq .

# Create a page
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  -H "Content-Type: application/json" \
  -X POST \
  "https://api.clickup.com/api/v3/workspaces/WORKSPACE_ID/docs/DOC_ID/pages" \
  -d '{"name":"New page"}' | jq .
```

## Chat API (v3)

### List chat channels

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v3/workspaces/WORKSPACE_ID/chat/channels?limit=50" | jq .
```

Useful filters:

- `description_format=text/md|text/plain`
- `cursor`
- `limit`
- `is_follower=true`
- `include_closed=true`
- `with_message_since=<timestamp>`
- `channel_types=<value>`

### Get a channel

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v3/workspaces/WORKSPACE_ID/chat/channels/CHANNEL_ID" | jq .
```

### Get channel followers or members

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v3/workspaces/WORKSPACE_ID/chat/channels/CHANNEL_ID/followers" | jq .
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v3/workspaces/WORKSPACE_ID/chat/channels/CHANNEL_ID/members" | jq .
```

### Get channel messages

`content_format` supports `text/md` and `text/plain`.

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v3/workspaces/WORKSPACE_ID/chat/channels/CHANNEL_ID/messages?limit=50&content_format=text/md" | jq .
```

### Get replies or reactions for a message

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v3/workspaces/WORKSPACE_ID/chat/messages/MESSAGE_ID/replies?content_format=text/md" | jq .
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v3/workspaces/WORKSPACE_ID/chat/messages/MESSAGE_ID/reactions" | jq .
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v3/workspaces/WORKSPACE_ID/chat/messages/MESSAGE_ID/tagged_users" | jq .
```

### Send a message

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  -H "Content-Type: application/json" \
  -X POST \
  "https://api.clickup.com/api/v3/workspaces/WORKSPACE_ID/chat/channels/CHANNEL_ID/messages" \
  -d '{"type":"message","content":"Hello from the API","content_format":"text/plain"}' | jq .
```

## Generic attachments API (v3)

### List attachments for a supported entity

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  "https://api.clickup.com/api/v3/workspaces/WORKSPACE_ID/ENTITY_TYPE/ENTITY_ID/attachments?limit=50" | jq .
```

### Upload an attachment to a supported entity

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  -F "attachment=@/path/to/file" \
  "https://api.clickup.com/api/v3/workspaces/WORKSPACE_ID/ENTITY_TYPE/ENTITY_ID/attachments" | jq .
```

## Privacy / ACLs (v3)

### Update access control on an object or location

The v3 schema supports `private` and `entries`.

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  -H "Content-Type: application/json" \
  -X PATCH \
  "https://api.clickup.com/api/v3/workspaces/WORKSPACE_ID/OBJECT_TYPE/OBJECT_ID/acls" \
  -d '{"private":true}' | jq .
```

See the v3 spec for the exact body shape for the target object type.

## Audit logs (v3)

### Query workspace audit logs

The audit logs endpoint is a `POST` in v3.

```bash
curl -fsS \
  -H "Authorization: $CLICKUP_PAT" \
  -H "Content-Type: application/json" \
  -X POST \
  "https://api.clickup.com/api/v3/workspaces/WORKSPACE_ID/auditlogs" \
  -d '{}' | jq .
```

## Common URL / ID patterns

- Workspace IDs are numeric strings
- Space, folder, list, and view IDs are numeric strings
- Task IDs can be short alphanumeric IDs
- Custom task IDs require `custom_task_ids=true&team_id=TEAM_ID`
- Docs and chat resources use `workspace_id` in v3

### Extract a task ID from a ClickUp task URL

```bash
echo "https://app.clickup.com/t/123456/86abc4d12" | sed 's#.*/##'
# => 86abc4d12
```

## Pagination patterns

### v2

v2 commonly uses page-based pagination:

- `page=0`
- `page=1`
- plus resource-specific filters

### v3

v3 commonly uses cursor pagination:

- `limit`
- `cursor`
- sometimes `next_cursor`

## Error handling

| Status | Meaning                      |
| ------ | ---------------------------- |
| `200`  | Success                      |
| `201`  | Created                      |
| `400`  | Bad request / invalid params |
| `401`  | Unauthorized / invalid PAT   |
| `403`  | Forbidden                    |
| `404`  | Not found                    |
| `429`  | Rate limited                 |
| `5xx`  | Server error                 |

Prefer `curl -fsS` so HTTP failures surface immediately.

## Best practices

1. **Use PAT auth only for this skill**: `Authorization: $CLICKUP_PAT`
2. **Use the HTTP API directly, not MCP**
3. **Start with hierarchy discovery**: workspace → space → folder/list → task/view/doc/channel
4. **Use v2 for core work items** and **v3 for Docs/Chat/ACLs/Audit Logs**
5. **Default to incomplete tasks** unless the user explicitly asks for completed/closed ones
6. **When using custom task IDs**, add `custom_task_ids=true&team_id=TEAM_ID`
7. **Free-text task search is not a general v2 endpoint**: use workspace/list filtering or fetch and filter client-side
8. **Docs content and chat message content support `text/md` and `text/plain`**
9. **Use `markdown_content` (create) or `markdown_description` (update) for task descriptions** — `description` is plain text only and will not render Markdown
10. **Be careful with mutations**: creating, editing, deleting, ACL changes, and webhook changes should only be done when explicitly requested
