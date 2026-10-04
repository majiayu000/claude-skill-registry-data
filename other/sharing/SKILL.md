---
name: sharing
description: Manage sharing permissions (Attio-style) for tables, workflows and agents from the CLI. Use when the user asks to share a table/workflow/agent, restrict who can view or edit a resource, set workspace/team/user access levels, or audit who has access. Covers resolving valid userIds/teamIds, the access levels per resource type, and get/set examples.
---

## Prerequisites

- Authenticate with `frontline auth login <api-key>`.
- All `sharing` commands require a **USER API key**. Any account user can read and change sharing (so everyone can share their own resources); a `GENERAL` key (no user) is rejected.
- The backend always revalidates: the resource must exist and belong to your account, and every `userId`/`teamId` must belong to the account.

## How access works (read this first)

- Sharing is **default-open**: if a resource has no explicit permission rows, everyone in the account has full access (backward compatible).
- Only users with **`FULL_ACCESS`** on a resource (or admins/owners / the resource creator) can **change** sharing via `set`. Users with `VIEW` can read the config (`get`) but get `403` on `set`.
- The **workspace** level is the default for everyone. Set it to `NONE` to lock the resource down so that only the listed teams/users get access.
- **Resolution order** is user > team > workspace. Admins/owners always bypass and have full access (they can view/manage everything regardless of the rows).
- The **resource creator (owner)** is never restricted: whoever created the table/workflow/agent always keeps full access to it, even if the workspace is `NONE` and they are not listed.

## Resolve valid ids first

You must use real `userId`/`teamId` values. List them before calling `set`:

```bash
frontline sharing users   # { results: [{ id, first_name, last_name, email }] }
frontline sharing teams   # { results: [{ id, name }] }
```

## Resource types and access levels

`--entity-type` is one of `table`, `workflow`, `agent`.
`--entity-id` is a **positive integer** for `table`/`workflow`, and a **uuid string** for `agent`.

Levels differ by resource type:

- **table** (aligned with workflows — three levels):
    - `FULL_ACCESS` — view + edit schema (fields, views, etc.) + full CRUD on records
    - `VIEW` — read-only table and records
    - `NONE` — no access
- **workflow**:
    - `FULL_ACCESS` — view + edit/delete
    - `VIEW` — view only
    - `NONE` — no access
- **agent** (two-level model unified into one level):
    - `FULL_ACCESS` — view + edit/delete agent + intervene conversations
    - `CAN_INTERVENE` — view + intervene conversations (interrupt / send response), without editing the agent
    - `VIEW` — view only (cannot intervene)
    - `NONE` — no access

> Intervening in conversations (interrupt, send response, cancel-interrupt) is only available from the app UI — not via Public API or CLI. The CLI `sharing` commands only manage who has permission; they do not perform intervention actions.

> Sharing applies to **data tables** only. Standard CRM objects (people, companies, deals, tickets) are governed by record-type permissions, not this API.

> Sharing is what makes a table's schema editable by a non-admin: `FULL_ACCESS` is required to add, edit, or delete fields and options, and `VIEW` returns `403` on those calls. Admins, owners, and the user who created the table always have edit access regardless of the sharing rows. **Object** schemas (including record types) are admin/owner-only and cannot be delegated this way — custom objects are no exception.

## Get the current configuration

```bash
frontline sharing get --entity-type table --entity-id 42
frontline sharing get --entity-type workflow --entity-id 7
frontline sharing get --entity-type agent --entity-id 1f0b2c3d-....-uuid
```

Output:

```json
{
    "resourceType": "table",
    "resourceId": 42,
    "workspace": "FULL_ACCESS",
    "teams": [{ "teamId": 3, "name": "Sales", "level": "VIEW" }],
    "users": [
        {
            "userId": 5,
            "firstName": "Ada",
            "lastName": "Lovelace",
            "email": "ada@x.com",
            "level": "FULL_ACCESS"
        }
    ],
    "myLevel": "FULL_ACCESS"
}
```

## Set the configuration (full replace)

`set` **replaces** the resource's sharing rows with what you pass. Anything you omit is cleared (workspace falls back to its default-open behavior if you don't include it).

```bash
# Lock a table to specific people/teams (workspace = NONE)
frontline sharing set --entity-type table --entity-id 42 --data '{
  "workspace": "NONE",
  "users": [{ "userId": 5, "level": "FULL_ACCESS" }],
  "teams": [{ "teamId": 3, "level": "VIEW" }]
}'

# Workflow: everyone can view, one user can edit
frontline sharing set --entity-type workflow --entity-id 7 --data '{
  "workspace": "VIEW",
  "users": [{ "userId": 5, "level": "FULL_ACCESS" }]
}'

# Agent: only admins (no workspace/teams/users) — everyone else loses access
frontline sharing set --entity-type agent --entity-id 1f0b2c3d-....-uuid --data '{
  "workspace": "NONE"
}'
```

`--data` keys:

- `workspace`: a single level string (optional).
- `teams`: `[{ "teamId": <number>, "level": "<level>" }]` (optional).
- `users`: `[{ "userId": <number>, "level": "<level>" }]` (optional).

The CLI validates `--entity-type`, the id shape, and that `--data` is valid JSON locally. The backend validates the levels are allowed for the resource type and that the ids exist.

## Common errors

- `bad_entity_type` / `bad_entity_id` / `bad_json`: local validation failed — fix the flag.
- `401` (unauthorized): you used a `GENERAL` key instead of a `USER` key.
- `400` invalid ids: a `userId`/`teamId` does not belong to the account — re-check with `sharing users` / `sharing teams`.
- `400` invalid level: you used a workflow-only level on a table/agent, an agent-only level on a workflow/table, or `CAN_EDIT_RECORDS`/`CAN_EDIT_TABLE` on workflow/agent (legacy table levels are auto-migrated to `FULL_ACCESS` on PUT).
- `403` on `set`: caller lacks `FULL_ACCESS` on the resource (includes self-escalation attempts from `VIEW` / `CAN_INTERVENE`).
- `404` on `get` / `agents describe`: caller has `NONE` (resource is hidden, not just read-only).

## Testing permissions (CLI)

Use two USER keys and named profiles (`user-a` configures, `user-b` is the subject). Resolve ids first:

```bash
frontline auth login <key-a> --profile user-a --base-url http://localhost:7010/public/v1
frontline auth login <key-b> --profile user-b --base-url http://localhost:7010/public/v1
frontline auth whoami --profile user-a --pretty
frontline sharing users --profile user-a --pretty
```

Create a disposable agent as user-a, then lock it down:

```bash
AGENT_ID=$(frontline agents create --profile user-a --name sharing-test | jq -r .id)
USER_B_ID=2

frontline sharing set --profile user-a --entity-type agent --entity-id "$AGENT_ID" \
  --data "{\"workspace\":\"NONE\",\"users\":[{\"userId\":$USER_B_ID,\"level\":\"VIEW\"}]}"
```

Smoke checks for `VIEW` (user-b):

| Command                                             | Expected        |
| --------------------------------------------------- | --------------- |
| `sharing get`                                       | `myLevel: VIEW` |
| `sharing set`                                       | 403 (exit 4)    |
| `agents describe --agent-id $AGENT_ID`              | 200             |
| `agents update --agent-id $AGENT_ID --name x`       | 403             |
| `agents flows list --agent-id $AGENT_ID`            | 200             |
| `agents flows create --agent-id $AGENT_ID --name x` | 403             |

Repeat after changing the level (`NONE`, `CAN_INTERVENE`, `FULL_ACCESS`). `sharing set` **replaces** the whole config — always include `workspace` plus the full `users` / `teams` arrays you want to keep.

Notes:

- `agents list` does **not** filter by sharing; test access with `describe` / `sharing get` using a known id.
- Account **OWNER/ADMIN** bypass sharing rows; use a plain **USER** as the subject.
- The resource **creator** always keeps `FULL_ACCESS`, even when `workspace: NONE` and they are not listed.
- CLI exit codes: `0` ok, `3` = 404, `4` = 401/403.

---

## See also

- Full reference: <https://docs.getfrontline.ai/docs> (concepts) and <https://docs.getfrontline.ai/cli> (command reference).
- App UI walkthroughs: <https://help.getfrontline.ai>.
