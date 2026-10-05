---
name: linear
description: Interact with Linear GraphQL API for issues, teams, projects, and workflow data using LINEAR_PAT environment variable.
---

Linear GraphQL API reference for common operations.

## Prerequisites

- `LINEAR_PAT` environment variable containing a valid Linear Personal API Key (never hardcode it).

**Check before use:**

```bash
[ -z "$LINEAR_PAT" ] && echo "Error: LINEAR_PAT not set" || echo "OK: LINEAR_PAT is set"
```

## Base URL

```
https://api.linear.app/graphql
```

## Authentication

All requests require the `Authorization` header:

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"query { viewer { id name email } }"}'
```

For OAuth, use `Authorization: Bearer <ACCESS_TOKEN>`, but prefer `LINEAR_PAT` for this skill.

## GraphQL Conventions

- Most list fields return connections with `nodes` and `pageInfo`
- Pagination uses `first` and `after`
- Filtering uses `filter`
- Sorting uses `orderBy`
- GraphQL responses may return HTTP 200 with an `errors` array

## Viewer

### Get Current User

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"query { viewer { id name displayName email active } }"}' | jq '.data.viewer'
```

### Get Viewer Organization

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"query { organization { id name urlKey } }"}' | jq '.data.organization'
```

## Teams

### List Teams

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"query { teams { nodes { id key name description } } }"}' | jq '.data.teams.nodes'
```

**Response**:

```json
[
  {
    "id": "team-uuid",
    "key": "ENG",
    "name": "Engineering",
    "description": "Engineering team"
  }
]
```

### Get Team by ID

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"query($id: String!) { team(id: $id) { id key name description } }","variables":{"id":"TEAM_ID"}}' | jq '.data.team'
```

### Get Team States

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"query($id: String!) { team(id: $id) { id name states { nodes { id name type position } } } }","variables":{"id":"TEAM_ID"}}' | jq '.data.team.states.nodes'
```

## Users

### List Users

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"query { users { nodes { id name displayName email active } } }"}' | jq '.data.users.nodes'
```

### Search Users by Name

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"query($name: String!) { users(filter: { name: { containsIgnoreCase: $name } }) { nodes { id name displayName email } } }","variables":{"name":"KEYWORD"}}' | jq '.data.users.nodes'
```

## Projects

### List Projects

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"query { projects { nodes { id name slug state progress targetDate } } }"}' | jq '.data.projects.nodes'
```

### Get Project

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"query($id: String!) { project(id: $id) { id name slug description state progress startDate targetDate url } }","variables":{"id":"PROJECT_ID"}}' | jq '.data.project'
```

### Get Project Issues

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"query($id: String!) { project(id: $id) { id name issues(first: 50) { nodes { id identifier title state { name type } assignee { name } } } } }","variables":{"id":"PROJECT_ID"}}' | jq '.data.project.issues.nodes'
```

## Cycles

### List Cycles

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"query { cycles { nodes { id number name startsAt endsAt completedAt team { id key name } } }"}' | jq '.data.cycles.nodes'
```

### List Cycles for Team

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"query($teamId: ID!) { cycles(filter: { team: { id: { eq: $teamId } } }) { nodes { id number name startsAt endsAt completedAt } } }","variables":{"teamId":"TEAM_ID"}}' | jq '.data.cycles.nodes'
```

## Issues

### Get Issue by ID or Identifier

Linear accepts UUIDs and shorthand identifiers like `ENG-123`.

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"query($id: String!) { issue(id: $id) { id identifier title description state { id name type } priority priorityLabel assignee { id name } project { id name } cycle { id name number } labels { nodes { id name } } url } }","variables":{"id":"ENG-123"}}' | jq '.data.issue'
```

**Response**:

```json
{
  "id": "issue-uuid",
  "identifier": "ENG-123",
  "title": "Task title",
  "description": "Task details",
  "state": { "id": "state-uuid", "name": "In Progress", "type": "started" },
  "priority": 2,
  "priorityLabel": "High",
  "assignee": { "id": "user-uuid", "name": "Jane Doe" },
  "project": { "id": "project-uuid", "name": "Project Name" },
  "cycle": { "id": "cycle-uuid", "name": "Cycle 12", "number": 12 },
  "labels": { "nodes": [{ "id": "label-uuid", "name": "bug" }] },
  "url": "https://linear.app/..."
}
```

### List Issues for a Team

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"query($id: String!) { team(id: $id) { id name issues(first: 50) { nodes { id identifier title state { name type } assignee { name } updatedAt } } } }","variables":{"id":"TEAM_ID"}}' | jq '.data.team.issues.nodes'
```

### List Incomplete Issues for a Team

Prefer this unless completed issues are explicitly requested.

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"query($teamId: ID!) { issues(filter: { team: { id: { eq: $teamId } }, completedAt: { null: true } }) { nodes { id identifier title state { name type } assignee { name } } } }","variables":{"teamId":"TEAM_ID"}}' | jq '.data.issues.nodes'
```

### Search Issues by Text

Use `searchIssues` (`issueSearch` is deprecated).

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"query($term: String!) { searchIssues(term: $term, first: 50) { nodes { id identifier title state { name } assignee { name } team { key name } } } }","variables":{"term":"KEYWORD"}}' | jq '.data.searchIssues.nodes'
```

### List Issues Assigned to Me

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"query { viewer { assignedIssues(first: 50) { nodes { id identifier title state { name type } priorityLabel dueDate team { key } } } } }"}' | jq '.data.viewer.assignedIssues.nodes'
```

### List Recently Updated Issues

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"query { issues(first: 50, orderBy: updatedAt) { nodes { id identifier title updatedAt state { name } } } }"}' | jq '.data.issues.nodes'
```

## Comments

### Get Issue Comments

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"query($id: String!) { issue(id: $id) { id identifier comments(first: 50) { nodes { id body createdAt user { id name } } } } }","variables":{"id":"ENG-123"}}' | jq '.data.issue.comments.nodes'
```

## Labels

### List Labels

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"query { issueLabels { nodes { id name color description team { key name } } } }"}' | jq '.data.issueLabels.nodes'
```

## Pagination

### Paginate Through Issues

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"query($after: String) { issues(first: 50, after: $after) { nodes { id identifier title } pageInfo { hasNextPage endCursor } } }","variables":{"after":null}}' | jq '.data.issues'
```

Use the returned `pageInfo.endCursor` as the next `after` value.

## Filtering and Sorting

### Filter Issues by Team + Assignee + Incomplete

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"query($teamId: ID!, $assigneeId: ID!) { issues(filter: { team: { id: { eq: $teamId } }, assignee: { id: { eq: $assigneeId } }, completedAt: { null: true } }, orderBy: updatedAt) { nodes { id identifier title updatedAt state { name } } } }","variables":{"teamId":"TEAM_ID","assigneeId":"USER_ID"}}' | jq '.data.issues.nodes'
```

### Filter Issues by Project

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"query($projectId: ID!) { issues(filter: { project: { id: { eq: $projectId } } }) { nodes { id identifier title state { name } assignee { name } } } }","variables":{"projectId":"PROJECT_ID"}}' | jq '.data.issues.nodes'
```

### Filter Issues by Cycle

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"query($cycleId: String!) { cycle(id: $cycleId) { id name issues(first: 50) { nodes { id identifier title state { name } assignee { name } } } } }","variables":{"cycleId":"CYCLE_ID"}}' | jq '.data.cycle.issues.nodes'
```

## Mutations

### Create Issue

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"mutation($input: IssueCreateInput!) { issueCreate(input: $input) { success issue { id identifier title url } } }","variables":{"input":{"teamId":"TEAM_ID","title":"New issue title","description":"Issue description"}}}' | jq '.data.issueCreate'
```

If `stateId` is omitted, Linear assigns the team default backlog or triage state.

### Update Issue

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"mutation($id: String!, $input: IssueUpdateInput!) { issueUpdate(id: $id, input: $input) { success issue { id identifier title state { name } assignee { name } } } }","variables":{"id":"ENG-123","input":{"title":"Updated title","description":"Updated description"}}}' | jq '.data.issueUpdate'
```

### Move Issue to Another State

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"mutation($id: String!, $input: IssueUpdateInput!) { issueUpdate(id: $id, input: $input) { success issue { id identifier state { id name type } } } }","variables":{"id":"ENG-123","input":{"stateId":"STATE_ID"}}}' | jq '.data.issueUpdate'
```

### Assign Issue

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"mutation($id: String!, $input: IssueUpdateInput!) { issueUpdate(id: $id, input: $input) { success issue { id identifier assignee { id name } } } }","variables":{"id":"ENG-123","input":{"assigneeId":"USER_ID"}}}' | jq '.data.issueUpdate'
```

### Add Comment

```bash
curl -s https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_PAT" \
  -H "Content-Type: application/json" \
  --data '{"query":"mutation($input: CommentCreateInput!) { commentCreate(input: $input) { success comment { id body url } } }","variables":{"input":{"issueId":"ISSUE_ID","body":"Adding a comment from the API."}}}' | jq '.data.commentCreate'
```

## Common ID Patterns

- Most Linear entities use UUIDs (e.g., `80c49302-0141-4911-b464-824a9ae6bd8f`).
- Issues also use shorthand identifiers like `ENG-123`; many queries accept either format.
- Copy UUIDs in the Linear UI with `Cmd/Ctrl+K` → `Copy model UUID`.

## Utility: Extract Issue Identifier from URL

```bash
# From https://linear.app/workspace/issue/ENG-123/fix-api-bug
# Identifier is: ENG-123

echo "https://linear.app/workspace/issue/ENG-123/fix-api-bug" | awk -F'/' '{print $(NF-1)}'
# Output: ENG-123
```

## Error Handling

| Status | Meaning                              |
| ------ | ------------------------------------ |
| `200`  | Success or partial GraphQL success   |
| `400`  | Bad request / invalid GraphQL        |
| `401`  | Unauthorized (invalid token)         |
| `403`  | Forbidden (insufficient permissions) |
| `404`  | Not found                            |
| `429`  | Rate limit exceeded                  |
| `5xx`  | Server error                         |

Also inspect `.errors` in the JSON body, even when HTTP status is `200`.

## Best Practices

1. **Default to incomplete issues**: Use `completedAt: { null: true }` unless completed ones are requested.
2. **Use issue search when IDs are unknown**: Start with `searchIssues`.
3. **Request only needed fields**: Keep GraphQL selections minimal to reduce payload size.
4. **Handle pagination**: Use `first` + `after` for large result sets.
5. **Prefer team-scoped queries**: Linear issues are typically team-centric.
6. **Check `errors` array**: GraphQL can partially succeed even with HTTP 200.
7. **Avoid polling per issue**: Prefer filtering, sorting by `updatedAt`, or webhooks.
