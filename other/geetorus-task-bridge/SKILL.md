---
name: geetorus-task-bridge
description: Create, comment on, update, and list Geetorus tasks from Hermes using scoped Geetorus API credentials.
---

# Geetorus Task Bridge

Use this skill when a Hermes-originated request needs to create or update Geetorus work directly. This is the Hermes-to-Geetorus direction, separate from Geetorus waking Hermes through the `hermes_local` or `hermes_gateway` adapter.

## Required Environment

Configure these in Hermes env/profile secrets, not in prompt text:

- `GEETORUS_API_URL` - Geetorus base URL, with or without `/api`.
- `GEETORUS_BRIDGE_API_KEY` - a Geetorus agent API key created with `scope.kind = "task_bridge"`.

Optional:

- `GEETORUS_API_KEY` - fallback env var for older profiles; it must still contain a `task_bridge` scoped key, never a full agent key.
- `GEETORUS_COMPANY_ID` - skips one identity lookup when set.
- `GEETORUS_AGENT_ID` - skips one identity lookup when set.
- `GEETORUS_RUN_ID` - sent as `X-Geetorus-Run-Id` on mutating requests when Hermes is running inside a Geetorus heartbeat.

Never print or paste API keys. The helper reads credentials from environment variables and only prints response summaries. Do not put a normal claimed agent API key in an internet-facing Hermes runtime; normal keys can use broad same-company Geetorus routes.

## Create a Bridge Key

Create the key from a board-authenticated Geetorus API session and store the returned token once:

```sh
curl -X POST "$GEETORUS_API_URL/api/agents/$HERMES_AGENT_ID/keys" \
  -H "Authorization: Bearer $BOARD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Hermes task bridge",
    "scope": {
      "kind": "task_bridge",
      "parentIssueId": "00000000-0000-4000-8000-000000000000"
    }
  }'
```

Use `parentIssueId` or `parentIssueIds` when Hermes should only create child tasks under approved work. Use `projectId` or `projectIds` when the approved boundary is a project. A bridge key can create tasks only inside that boundary, can comment/update only bridge-created or assigned issues, and cannot use company-wide issue list/search/read surfaces.

## Helper

Run the helper from this skill directory:

```sh
node ./geetorus-task.mjs --help
```

Commands:

```sh
node ./geetorus-task.mjs list-assigned
node ./geetorus-task.mjs create-task --parent-id "00000000-0000-4000-8000-000000000000" --title "Investigate checkout failures" --description "Capture failing request and root cause."
node ./geetorus-task.mjs comment --issue PAP-123 --body "Found the failing request path."
node ./geetorus-task.mjs update-status --issue PAP-123 --status in_review --comment "Ready for review."
```

`create-task` defaults to assigning the task to the authenticated Hermes agent so the work is immediately actionable. Use `--unassigned` to create backlog work instead. Use `--assignee-agent-id <uuid>` only when the Geetorus API key has permission to assign work to that agent.

For multiline bodies, prefer files or stdin:

```sh
node ./geetorus-task.mjs create-task --title "Write rollout note" --description-file ./task.md
node ./geetorus-task.mjs comment --issue PAP-123 --body-file -
```

## Workflow Expectations

- Keep tasks company-scoped by using the company resolved from the scoped agent key.
- Let Geetorus activity logging come from the normal API endpoints; do not write local logs that include credentials.
- Use comments for durable progress.
- Use `update-status` only when the issue has a real disposition: `done`, `in_review`, `blocked`, `todo`, `in_progress`, `backlog`, or `cancelled`.
- Use `list-assigned` before creating duplicate work when the user asks about current Geetorus assignments.
