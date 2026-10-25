---
name: kangaplanner-api
description: >
  Read and write KangaPlanner issues (bugs, features, tasks) over its REST API at
  api.kangasuite.com with a kp_ bearer token. Use whenever the user mentions
  KangaPlanner, planner.kangasuite.com, a KangaPlanner ref like B-BUG-69, or wants
  to list, look up, file, update, close, comment on or convert an issue in the
  planner, even if they don't say "API".
---

# KangaPlanner API

Base URL: `https://api.kangasuite.com/api/issues` (the web app is
planner.kangasuite.com; settings > API tokens is where tokens are minted).

Auth: `Authorization: Bearer kp_…`. The token lives at
`~/.claude/secrets/kangaplanner-api-token` (chmod 600). Read it into a shell
variable, never print it or write it into a file:

```sh
T=$(cat ~/.claude/secrets/kangaplanner-api-token)
B=https://api.kangasuite.com/api/issues
curl -s "$B" -H "Authorization: Bearer $T" | jq '.issues | length'
```

The token acts as its owning user, so it sees every company and space that user
can see. Scopes are `issues:read` (GET) and `issues:write` (everything else).
Errors come back as `{"error": "..."}` with 400/401/403/404/409/429; a 400 body is
a stringified Zod issue list.

## Endpoints

| Method | Path | Body / query | Returns |
| --- | --- | --- | --- |
| GET | `/` | `?spaceId= &includeArchived=true &assignedToMe=true &reportedByMe=true` | `{issues: [...]}` |
| GET | `/:id` | | `{issue}` with replies, assignees, followers, attachments |
| POST | `/` | create body below | `{issue}` (201) |
| PATCH | `/:id` | update body below | `{issue}` |
| POST | `/:id/replies` | `{body, audience?}` | `{reply}` (201) |
| GET | `/:id/attachments/:aid` | | raw bytes |
| POST | `/:id/convert` | `{toType}` | `{issue}`, ref changes |

`:id` is always the issue's UUID. Refs like `B-BUG-69` are rejected, so resolve
a ref by listing and filtering:

```sh
curl -s "$B" -H "Authorization: Bearer $T" | jq -r '.issues[] | select(.ref=="B-BUG-69") | .id'
```

The list returns several hundred rows with `description` cut to a 300-char
snippet. Always narrow it with `jq` (`{id, ref, subject, status, priority,
space: .space.name, assignees: [.assignees[].name]}`) rather than dumping it.
There is no spaces endpoint: get space names and ids from the list rows
(`[.issues[] | {spaceId, space: .space.name}] | unique`).

## Bodies

Enums: type `bug|feature|task`; priority `low|medium|high|critical`; status
`open|in_progress|resolved|closed`; blockedReason `waiting_reporter|on_hold`
(only while `in_progress`); closeReason
`fixed|duplicate|not_a_bug|by_design|wont_fix|cant_reproduce` (only while
`closed`). Dates are `YYYY-MM-DD`; start may not be after due.

Create (required: `spaceId`, `subject` ≤255, `description` ≤50k, markdown):

```json
{"spaceId": "<uuid>", "subject": "…", "description": "…", "type": "bug",
 "priority": "medium", "startDate": "2026-10-21", "dueDate": "2026-10-31",
 "assigneeIds": ["<uuid>"], "followerIds": ["<uuid>"]}
```

Update: any subset of `subject`, `description`, `priority`, `status`,
`startDate`, `dueDate`, `blockedReason`, `closeReason`, `reporterEmail`. Omit to
leave unchanged, `null` to clear a date, reason or email.

Reply: `{"body": "…", "audience": "internal"}`. Audience defaults to `internal`
(team-only). `client` emails the portal client and `end_user` emails the
external reporter, so only use those when the user asked to message them.

Convert: `{"toType": "feature"}` renumbers the issue, so re-read the ref.

## Not available over this API

Assigning or unassigning after creation, listing users, and listing spaces
directly. The backend repo (`~/Developer/KangaPlanner`) has an MCP server at
`/mcp` that adds these, but it is not deployed yet (404 as of 2026-10-20).
