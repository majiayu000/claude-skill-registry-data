---
name: linear
description: This skill should be used when the user asks to read, create, update, or search Linear issues, projects, cycles, or teams.
version: 1.2.0
---

# Linear

Read, create, update, and search issues in Linear using the Linear GraphQL API.

## Configuration

- API endpoint: `https://api.linear.app/graphql`
- Key: a Personal API Key, which the operator stores in the profile home's `credentials.yaml` under `linear.api_key`.
- Send every Linear request through `charliebot linear request`.
  The command is the one reader of the key, so the key stays out of session commands, output and run records.

## API Reference

`charliebot linear request` sends one GraphQL request to Linear and prints Linear's JSON response.
It reads the request body from stdin, or from the file that `--file <path>` names.
The body is a JSON object with a string `query` and an optional `variables` object.

```sh
charliebot linear request <<'JSON'
{"query":"query { viewer { id name email } }"}
JSON
```

| Exit code | Meaning |
|---|---|
| 0 | HTTP 200 and a JSON response without an `errors` key. |
| 1 | Another status, an `errors` key, invalid response JSON or a network failure. |
| 2 | Invalid arguments or request body. |
| 3 | The credentials file cannot be read or `linear.api_key` is missing. |

Pipe the output to `jq` to format it.

### Viewer (who am I)

```graphql
query { viewer { id name email } }
```

### List Teams

```graphql
query { teams { nodes { id name key } } }
```

### List Issues (with filters)

```graphql
query($filter: IssueFilter) {
  issues(filter: $filter, first: 50) {
    nodes {
      id identifier title state { name } priority assignee { name } createdAt updatedAt
    }
  }
}
```

Common filters:
- By team: `{"team": {"key": {"eq": "TEAM_KEY"}}}`
- By assignee: `{"assignee": {"name": {"eq": "Name"}}}`
- By state: `{"state": {"name": {"in": ["Todo", "In Progress"]}}}`
- Combined: nest multiple filters together

### Read a Whole Connection

Linear's pagination docs return 50 items by default when `first` is omitted and do not document an upper bound for `first`.
Each connection response carries `pageInfo { hasNextPage endCursor }`.
Request `pageInfo { hasNextPage endCursor }` in each connection's selection set.
To read the whole result set, pass `pageInfo.endCursor` as `after` on the next request, with the same `filter`, and repeat while `pageInfo.hasNextPage` is true.

Source: Linear developer docs, pagination (https://linear.app/developers/pagination).

### Get Single Issue

```graphql
query($id: String!) {
  issue(id: $id) {
    id identifier title description state { name } priority
    assignee { name } labels { nodes { name } }
    comments { nodes { body user { name } createdAt } }
  }
}
```

You can also look up by identifier (e.g. "ENG-123"); `issue(id:)` accepts the
human identifier and returns one issue:

```graphql
query {
  issue(id: "ENG-123") {
    id identifier title description state { name }
  }
}
```

### Search Issues

```graphql
query($term: String!) {
  searchIssues(term: $term, first: 20) {
    nodes {
      id identifier title state { name } assignee { name } priority
    }
  }
}
```

### Two-path recall

The two paths answer different questions, so run both and deduplicate before
presenting. The semantic path `searchIssues(term:)`
returns hits for unrelated terms, so it answers "does anything look like this"
but cannot prove that no matching issue exists. The structured path
`issues(filter:{or:[{title:{containsIgnoreCase:K}},{description:{containsIgnoreCase:K}}]})`
answers "does an issue containing K exist"; an empty result is a usable negative.
A conclusion of "no matching issue" requires the structured path; present the
deduplicated union of both paths.

### Create Issue

```graphql
mutation($input: IssueCreateInput!) {
  issueCreate(input: $input) {
    success
    issue { id identifier title url }
  }
}
```

Variables:
```json
{
  "input": {
    "teamId": "TEAM_UUID",
    "title": "Issue title",
    "description": "Markdown description",
    "priority": 2,
    "assigneeId": "USER_UUID"
  }
}
```

Priority: 0=No priority, 1=Urgent, 2=High, 3=Medium, 4=Low

### Update Issue

```graphql
mutation($id: String!, $input: IssueUpdateInput!) {
  issueUpdate(id: $id, input: $input) {
    success
    issue { id identifier title state { name } }
  }
}
```

### Add Comment

```graphql
mutation($input: CommentCreateInput!) {
  commentCreate(input: $input) {
    success
    comment { id body }
  }
}
```

Variables: `{"input": {"issueId": "ISSUE_UUID", "body": "Comment text"}}`

A mutation on an archived issue — one with a non-null `archivedAt` — fails with
`Entity not found: Issue`, `commentCreate` included, while queries still return
the issue. Before a write to an issue, read its `archivedAt`; when it is set,
unarchive (`issueUnarchive`), make the write, then archive it again
(`issueArchive`) so the issue ends in its original archive state.

### List Projects

```graphql
query {
  projects(first: 50) {
    nodes { id name state { ... on ProjectState { name } } }
  }
}
```

### List Cycles

```graphql
query($teamId: String!) {
  team(id: $teamId) {
    cycles(first: 10, orderBy: createdAt) {
      nodes { id name startsAt endsAt }
    }
  }
}
```

## Rules

- **English only:** All ticket titles and descriptions must be written in English, regardless of conversation language.
- **Default assignee:** Use the host-configured default assignee if one is set (host-specific skill / MEMORY); otherwise leave unassigned and ask the user.
- **Issue writes:** In a sub session (any session with a parent task, at any depth), issue creation, updates, and
  comment posts proceed directly and are reported with the issue identifier and link; issue and comment deletion
  waits for the user's take off. In a root session (no parent task), show the draft and get user confirmation before
  creating or updating issues. The canonical rule is External System Writes in
  `~/workspace/charlie-bot/prompts/master.md`.
- **Feishu for documentation:** Create a Feishu document for a Linear issue when the user asks for one or when the issue's detail is meant for colleagues to read; otherwise the detail stays in the issue's session artifacts rather than in Linear comments or long descriptions. When a doc exists, each Linear issue maps to **one** Feishu document, subsequent updates append to the same Feishu doc never a new one, the Feishu doc title matches the Linear issue title, and the Feishu doc URL is linked in the Linear issue description.
- **Default Feishu doc sharing:** When creating the Feishu doc associated with a Linear issue, set its public permission following the policy in the Feishu skill (skills/feishu/SKILL.md) after the user explicitly approves that permission write.
- **Permission-write approval:** Any Feishu permission change for an associated Feishu doc, including the default `tenant_readable` setup for a new doc, still requires explicit user approval before sending the Feishu permission write.

## Content conventions

- Issue body: goal and deliverables only. No status updates, no implementation
  detail, no results. When no Feishu doc exists, progress and technical content
  live in the issue's session artifacts; when one exists, they live in the linked
  Feishu doc.
- Externally shared Feishu result docs are written in English, structured as:
  what was done, which optimizations, final results, experiment environment,
  reproducible scripts. No process narrative.
