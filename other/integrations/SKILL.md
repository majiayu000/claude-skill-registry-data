---
name: integrations
description: Manage account integrations (Studio connected accounts/toolkits — Gmail, Slack, Salesforce, etc.) and resolve trigger resource IDs using the `frontline integrations` CLI. Use this to list connected integrations and read the numeric `id` that becomes the `connectedAccountId` in workflow/flow triggers and tool nodes, to discover connectable toolkits and their tool slugs, to configure which tools an integration exposes (`integrations tools set`), and to turn human labels like "my Q3 budget sheet" into the IDs an event-trigger config needs. Requires a USER API key.
allowed-tools: Bash(frontline:*)
---

# Account integrations (Studio connected accounts)

Account integrations are the account-scoped (Studio) connected accounts — Gmail, Slack,
Salesforce, Google Sheets, etc. Each one has a numeric **`id`** that is the **`connectedAccountId`**
you wire into workflow/flow triggers, tool nodes, and the resource pickers below. Setting up an
automation almost always starts here: find the integration, confirm it's connected, and read its
`id`.

All `frontline integrations` commands are **USER-scoped** — a GENERAL/account key returns 401.
Auth uses the same per-user API key as the rest of the CLI (`frontline auth login <key>`).

## Managing integrations

| Command                                   | What it does                                                        |
| ----------------------------------------- | ------------------------------------------------------------------- |
| `integrations list`                       | List connected integrations. Each `id` is the `connectedAccountId`. |
| `integrations toolkits`                   | Catalog of connectable toolkits + their supported tool slugs.       |
| `integrations get <integrationId>`        | Full details of one integration.                                    |
| `integrations update <integrationId>`     | Change `--alias` and/or `--visibility` (`SHARED`/`PRIVATE`).        |
| `integrations tools list <integrationId>` | Tools split into enabled vs available (with required-scope status). |
| `integrations tools set <integrationId>`  | Replace the enabled tool slugs (`--slugs a,b,c`).                   |

`integrations list` filters: `--toolkit <TOOLKIT>`, `--filter-text <text>`, `--connected`,
`--disconnected`. Toolkit values are **UPPERCASE enum names** (`GMAIL`, `SLACK`, `SALESFORCE`,
`GOOGLESHEETS`, `HUBSPOT`, …) — `integrations toolkits` is the authoritative list; an unknown
value returns 400. Add `--table` to any read command for a compact view.

```bash
# Find the Gmail integration and grab its id (the connectedAccountId for triggers).
frontline integrations list --toolkit GMAIL --connected --table
#   → id: 42   toolkit: GMAIL   alias: Support inbox   isConnected: true

# See what a toolkit can do, then enable a specific set of tools.
frontline integrations toolkits --table
frontline integrations tools list 42 --table
frontline integrations tools set 42 --slugs GMAIL_SEND_EMAIL,GMAIL_FETCH_EMAILS
```

### Output shapes (default JSON)

- `integrations list` → `{ "results": [ … ] }` (no pagination). Key fields per integration:
  `id` (the `connectedAccountId`), `toolkit`, `alias`, `visibility`, `isConnected`, `isExpired`,
  `connectedEmail`, `allowedToolSlugs` (currently enabled), `enabledToolsCount`,
  `availableToolsCount`, `createdByUser`.
- `integrations toolkits` → `{ "results": [ { toolkit, name, description, authScheme, toolCount, tools[] } ] }`.
  `tools[]` are the valid slugs for `tools set`.
- `integrations tools list <id>` → `{ "enabledTools": [...], "availableTools": [...] }`, each entry
  `{ slug, name, description, enabled, hasRequiredScopes }`. `hasRequiredScopes: false` means the
  connected account's OAuth grant is missing the scopes that tool needs — it will fail at runtime
  until the user reconnects the integration in the Studio UI with broader permissions. Don't
  enable such tools without flagging this.

### Using the `id` in workflows and flows

This is what the `id` is for (see the `workflow-builder` skill for full node payloads):

- **Event trigger node**: a workflow `TRIGGER` node with `triggerType: "COMPOSIO_TRIGGER"` —
  its `data` requires `connectedAccountId`, `triggerToolkit` (e.g. `GMAIL`), and `triggerSlug`,
  plus the trigger's `triggerConfig` (whose IDs you resolve with the resource pickers below).
  Discover valid slugs + their config fields with `max tasks triggers`.

```bash
frontline workflows nodes create --data '{"nodeId":"node_11111111-1111-1111-1111-111111111111","type":"TRIGGER","position":{"positionX":0,"positionY":0},"data":{"type":"TRIGGER","triggerType":"COMPOSIO_TRIGGER","connectedAccountId":42,"triggerToolkit":"GMAIL","triggerSlug":"GMAIL_NEW_GMAIL_MESSAGE","triggerConfig":{"labelIds":"INBOX"}}}'
```

When the trigger fires, the event payload is available in downstream nodes as the
built-in **`{trigger_payload}`** variable (plain string, no dot-access — extract
fields with `DATA_TRANSFORMER` or `AI_CAPTURE`, same as `{webhook_payload}`).

- **AI tool nodes** (`TOOLS_AI`): node `data.connectedAccountConfigs` is an array of
  `{ connectedAccountId, useAllTools, selectedToolSlugs }` — so a node can use all of the
  integration's enabled tools (`"useAllTools": true`) or a narrower subset
  (`"useAllTools": false, "selectedToolSlugs": ["GMAIL_SEND_EMAIL"]`).
- These references are **validated server-side**: a wrong `connectedAccountId` returns
  `400 bad_request` with `details.issues[].code === "not_found"` and the node is dropped.

### Semantics, permissions, and errors

- **`tools set` is a full replace**, not a merge — pass every slug you want enabled. Slugs must
  belong to the integration's toolkit (invalid slugs → `400` "Invalid tool slugs: …"). The change
  is **account-wide**: every workflow/agent node using this integration with `useAllTools: true`
  immediately gains/loses those tools.
- **Visibility**: `SHARED` = usable by the whole account; `PRIVATE` = only the creator.
  `integrations list` only returns integrations visible to the calling user, so a missing
  integration may simply be someone else's PRIVATE one.
- **Only the creator, an admin, or an owner** may `update` an integration or change its tools —
  otherwise `403`. Renaming to an alias that already exists in the account returns `409`.
- **Connecting a new integration (OAuth)** is not available from the CLI — it needs an interactive
  browser redirect. Connect it in the Studio UI, then manage it here. Disconnecting/deleting is
  also UI-only.
- An integration that is `isConnected: true` but `isExpired: true` needs to be reconnected in the
  UI before its tools/triggers will run.
- A GENERAL/account API key returns `401` on every command in this skill; a wrong
  `integrationId` returns `404`.

## Integration resources (trigger ID resolver)

Event triggers don't take human names — they take **IDs**. A "new rows in a Google Sheet"
trigger needs a `spreadsheet_id`, not "my budget sheet". These commands list the resources in a
user's connected integration so you can pick the right ID and drop it into a trigger config.

This is the missing middle step of the event-trigger flow:

1. **Discover the trigger** — `max tasks triggers` (or the workflow trigger catalog): gives you the
   `slug` and its **config field names** (e.g. `spreadsheet_id`, `sheet_name`).
2. **Resolve the IDs** — _these commands_: turn names into IDs for those config fields.
3. **Create** — pass the resolved IDs in the trigger config
   (`max tasks create --trigger-slug … --trigger-config '{…}'`, or the workflow trigger node).

If a picker returns nothing or 401s unexpectedly, check `integrations list` first — the toolkit
may not be connected, may be expired, or may be someone else's PRIVATE integration.

## Which command resolves which config field

| Command                                                      | Resolves       | Common trigger config field |
| ------------------------------------------------------------ | -------------- | --------------------------- |
| `integrations resources gmail labels`                        | Gmail label id | label id                    |
| `integrations resources googlesheets spreadsheets`           | spreadsheet id | `spreadsheet_id`            |
| `integrations resources googlesheets sheets <spreadsheetId>` | sheet/tab name | `sheet_name`                |
| `integrations resources googledocs documents`                | document id    | `document_id`               |
| `integrations resources googledrive folders`                 | folder id      | `folder_id`                 |
| `integrations resources googledrive shared-drives`           | drive id       | `drive_id`                  |
| `integrations resources asana workspaces`                    | workspace gid  | `workspace_gid`             |
| `integrations resources asana projects <workspaceGid>`       | project gid    | `project_gid`               |
| `integrations resources salesforce sobjects`                 | sobject name   | `sobject_name`              |
| `integrations resources salesforce fields <sobjectName>`     | field name     | field selectors             |
| `integrations resources outlook folders`                     | mail folder id | `folderId`                  |
| `integrations resources outlook calendars`                   | calendar id    | `calendarId`                |

The searchable pickers (sheets, docs, drive folders/drives) accept `--query <text>` and
`--limit <n>` (1–100, default 50). Add `--table` for a readable list.

## Typical flow

```bash
# 1. See what the trigger needs.
max tasks triggers --pretty
#   → GOOGLESHEETS_NEW_ROWS_TRIGGER needs { spreadsheet_id, sheet_name, start_row }

# 2. Resolve the spreadsheet, then its tabs.
frontline integrations resources googlesheets spreadsheets --query "Q3 budget" --table
#   → id: 1AbC...   name: Q3 Budget
frontline integrations resources googlesheets sheets 1AbC... --table
#   → title: Sheet1

# 3. Create the task with the resolved IDs.
max tasks create \
  --name "New budget rows" \
  --instructions "Summarize each new budget row and flag anything over $10k." \
  --trigger-slug GOOGLESHEETS_NEW_ROWS_TRIGGER \
  --trigger-config '{"spreadsheet_id":"1AbC...","sheet_name":"Sheet1","start_row":2}'
```

## Multiple accounts of the same toolkit

If the user has more than one connected account for a toolkit (e.g. two Gmail accounts), pass
`--connected-account-id <id>` to target a specific one — the `<id>` is the integration `id` from
`integrations list`. With a single account per toolkit you can omit it.

## Examples

```bash
frontline integrations resources gmail labels --table
frontline integrations resources googledocs documents --query proposal
frontline integrations resources googledrive folders --query Invoices --table
frontline integrations resources asana workspaces
frontline integrations resources asana projects 1200000000000001
frontline integrations resources salesforce sobjects --table
frontline integrations resources salesforce fields Opportunity
frontline integrations resources outlook calendars
```

---

## See also

- Building workflows/flows (exact `TRIGGER` and `TOOLS_AI` node payloads where
  `connectedAccountId` goes): the `workflow-builder` skill.
- Max automated tasks (where the resolved resource IDs get used): the `max-tasks` skill.
- Full reference: <https://docs.getfrontline.ai/cli>.
