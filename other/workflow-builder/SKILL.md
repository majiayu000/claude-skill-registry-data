---
name: workflow-builder
description: Build valid Frontline automation workflows AND agent flows from the CLI. Covers trigger types, incoming webhooks, DYNAMIC_TABLES with object schema lookup, variable interpolation, and end-to-end automation patterns. Use when creating or editing any workflow or flow graph.
allowed-tools: Bash(frontline:*)
---

# Workflow & Flow Builder

Covers two types of graphs:

- **Automation workflows** — standalone automations triggered by events or schedules (`frontline workflows ...`)
- **Agent flows** — conversation flows inside an AI agent (`frontline agents flows ...`)

Both share the same node/edge model and the same `nodeId` format rules.

## Valid Node Types Per Workflow Type

**Automation workflows** accept only these node types:
`TRIGGER`, `SCHEDULED_TRIGGER`, `WEBHOOK`, `TOOLS_AI`, `API`, `CONDITIONAL_ROUTING`, `AI_CAPTURE`, `DATA_TRANSFORMER`, `DYNAMIC_TABLES`, `CREATE_RECORD_ACTIVITY`, `ITERATION`, `BREAK`, `AUTOMATION_STATUS`, `SEND_MESSAGE`, `SEND_WHATSAPP_MESSAGE`, `TRANSCRIPTION`, `FILE_ANALYSIS`

**Agent flows** accept only these node types:
`START`, `TRIGGER_INTENT`, `SAY_AI`, `RESPONSE_AI`, `TOOLS_AI`, `API`, `CONDITIONAL_ROUTING`, `CREATE_RECORD_ACTIVITY`

> `DYNAMIC_TABLES` ("Data Action") is **automation-only** — it is **not** a flow node. Inside a flow, read/write records via a `TOOLS_AI` node whose agent has table tools.
> `CREATE_RECORD_ACTIVITY` is available in **both** automations and flows.

**Cross-type nodes are rejected by the backend with a 400 error.** For example, adding `SAY_AI` or `RESPONSE_AI` to an automation will fail, and adding `TRIGGER`, `SEND_MESSAGE`, or `DYNAMIC_TABLES` to a flow will also fail.

> For the authoritative, always-current catalog (which types are valid in flows vs automations and which allow multiple outgoing edges), run `frontline guidance nodes`. See the `guidance` skill.

---

## Node identity (`nodeId` and `alias`)

Do **not** send `nodeId` or `alias` in `nodes create` payloads. The server assigns both and returns them in the **201** JSON response (`nodeId` matches `node_<uuid>`). Read the id before edges or downstream `{node_<uuid>}` references:

```bash
frontline workflows nodes create --data '{"type":"API","position":{"positionX":0,"positionY":0},"data":{"type":"API","url":"https://example.com","method":"GET","headers":[]}}'
# NODE_ID=$(... | jq -r '.data.nodeId')   # CLI stdout is wrapped as { ok: true, data: <node> }
# API nodes only expose "success"/"fail" outgoing handles — never "default" (see the API node section below).
frontline workflows edges add --source "$NODE_ID" --source-handle success --target <other-node-id> --target-handle default
```

To set a **custom alias** after create, use `nodes update <nodeId> --data '{"alias":"My label"}'`.

---

## Auth Check

```bash
frontline auth whoami
```

---

## Automation Workflows

### Setup

```bash
frontline workflows create --name "My Automation"
# Saved as active workflow automatically

frontline workflows use <workflowId>   # switch active workflow
frontline workflows graph --table      # inspect before each change
```

### Trigger Node

Every automation needs exactly one trigger (type `TRIGGER` or `SCHEDULED_TRIGGER`).

Cron is not a `triggerType`: schedules are the separate `SCHEDULED_TRIGGER` node type (see below). No trigger of any kind delivers events until the workflow is `ACTIVE`.

**Supported `triggerType` values for `TRIGGER` nodes:**

| triggerType                                       | Required extra fields                                             |
| ------------------------------------------------- | ----------------------------------------------------------------- |
| `CONTACT_CREATED`                                 | —                                                                 |
| `CONTACT_UPDATED`                                 | —                                                                 |
| `CONVERSATION_ENDED`                              | `triggeredByAgentIds` — see below                                 |
| `CONVERSATION_IDLE`                               | `triggeredByAgentIds` — see below                                 |
| `FEEDBACK_CAPTURED`                               | `triggeredByAgentIds` — see below                                 |
| `INCOMING_WEBHOOK`                                | `triggerByWebhookIds` — see below                                 |
| `TABLE_ROW_CREATED` / `TABLE_ROW_UPDATED`         | `triggeredByTableId`                                              |
| `OBJECT_RECORD_CREATED` / `OBJECT_RECORD_UPDATED` | `triggeredByTableId`, `triggeredByRecordTypeId`                   |
| `COMPOSIO_TRIGGER`                                | `connectedAccountId`, `triggerToolkit`, `triggerSlug` — see below |

Example — contact created trigger:

```bash
frontline workflows nodes create --data '{"type":"TRIGGER","position":{"positionX":0,"positionY":0},"data":{"type":"TRIGGER","triggerType":"CONTACT_CREATED"}}'
```

### Conversation Trigger (ended / idle / feedback)

`CONVERSATION_ENDED`, `CONVERSATION_IDLE`, and `FEEDBACK_CAPTURED` fire **per agent**. They only run for the agents listed in `triggeredByAgentIds`, so a trigger without that array saves successfully and then never fires — this is the most common reason a conversation workflow looks correct but does nothing.

**Step 1** — get the agent UUIDs (the `id` column):

```bash
frontline agents list --table
```

**Step 2** — create the trigger with the agents bound to it:

```bash
frontline workflows nodes create --data '{"type":"TRIGGER","position":{"positionX":0,"positionY":0},"data":{"type":"TRIGGER","triggerType":"CONVERSATION_IDLE","triggeredByAgentIds":["550e8400-e29b-41d4-a716-446655440000"]}}'
```

Rules that are easy to get wrong:

- The field is `triggeredByAgentIds` (array of agent UUID strings). `assistantId` and `agentId` are **not** valid keys and are rejected with a 400.
- Pass one entry per agent that should fire the workflow. There is no "all agents" wildcard — adding a new agent later means updating the trigger node.
- Do **not** set `triggeredBy` to `USER` here. Conversation events always arrive from the agent, so `USER` silently blocks every run. Omit `triggeredBy`, or use `AGENT` / `BOTH`.

**`CONVERSATION_IDLE` has a second prerequisite:** the idle event only exists if idle is enabled on the agent's channel. Read the current settings, then send the same payload back with the idle fields set (the update is a full replace, not a patch):

```bash
frontline agents settings get whatsapp
frontline agents settings update whatsapp --data '{...existing fields...,"enableIdle":true,"idleSettings":{"after":5,"timeUnit":"MINUTES","resetsLimit":1}}'
```

`timeUnit` is `MINUTES` or `HOURS`; `after` is how long the conversation stays quiet before the trigger fires; `resetsLimit` caps how many times it can re-fire in one conversation.

### Incoming Webhook Trigger

**Step 1** — Create the incoming webhook resource:

```bash
frontline incoming-webhooks create --name "CRM events" --description "Receives contacts from external CRM"
```

Save the returned `id` and `url`. The `accessToken` is the bearer token callers must send.

**Step 2** — Create the trigger node referencing the webhook ID:

```bash
frontline workflows nodes create --data '{"type":"TRIGGER","position":{"positionX":0,"positionY":0},"data":{"type":"TRIGGER","triggerType":"INCOMING_WEBHOOK","triggerByWebhookIds":["<incoming-webhook-id>"]}}'
```

When the webhook fires, the full POST body is available in the workflow as **`{webhook_payload}`** — a built-in variable you can reference in any downstream node without creating it manually.

### Object Record Trigger

First get the object IDs:

```bash
frontline object get people
# response: id (tableId) and record_types[0].id (recordTypeId)
```

```bash
frontline workflows nodes create --data '{"type":"TRIGGER","position":{"positionX":0,"positionY":0},"data":{"type":"TRIGGER","triggerType":"OBJECT_RECORD_CREATED","triggeredByTableId":2,"triggeredByRecordTypeId":2}}'
```

### Integration Event Trigger (COMPOSIO_TRIGGER)

Fires when something happens in a connected integration (new Gmail message, new Google
Sheets row, HubSpot deal stage change, …).

**Step 1** — Resolve the integration's `connectedAccountId` and the trigger slug/config:

```bash
frontline integrations list --toolkit GMAIL --connected --table   # → id = connectedAccountId
max tasks triggers --pretty                                       # → valid slugs + their config fields
frontline integrations resources gmail labels --table             # → resolve config-field IDs (see `integrations` skill)
```

**Step 2** — Create the trigger node:

```bash
frontline workflows nodes create --data '{"type":"TRIGGER","position":{"positionX":0,"positionY":0},"data":{"type":"TRIGGER","triggerType":"COMPOSIO_TRIGGER","connectedAccountId":42,"triggerToolkit":"GMAIL","triggerSlug":"GMAIL_NEW_GMAIL_MESSAGE","triggerConfig":{"labelIds":"INBOX"}}}'
```

All three of `connectedAccountId`, `triggerToolkit`, and `triggerSlug` are required (400
otherwise); `triggerSlug` must be a supported event trigger and `triggerConfig` is validated
against that trigger's config schema. When it fires, the event payload is available downstream
as the built-in **`{trigger_payload}`** variable (same plain-string semantics as
`{webhook_payload}` — no dot-access; extract fields with `DATA_TRANSFORMER` or `AI_CAPTURE`).

### Scheduled Trigger

```bash
frontline integrations list --table --is-connected true
```

**Step 2** — find the event slug and its config fields. Never guess a slug; this command is the source of truth:

```bash
frontline integrations trigger-types --toolkit GOOGLEDRIVE --table
```

Columns: `slug` (→ `triggerSlug`), `toolkit` (→ `triggerToolkit`), `deliveryType`, `requiredConfig` (keys you must send in `triggerConfig`), `optionalConfig`, and `pickers` (`field=resourceType` for fields whose value must be resolved — see step 3). Without `--table` you get the full JSON, including a per-field `required` / `userConfigurable` / `resourceType`.

**Step 3** — resolve any ids listed in `pickers`. This is how you get a real `folder_id`, `spreadsheet_id`, `workspace_gid`, and so on:

```bash
frontline integrations trigger-resources --type googledrive_folders --connected-account-id 42 --table
```

Send the chosen `id` as the value of the config field it came from. `--parent` is required when browsing inside another resource (`googlesheets_sheets` → spreadsheetId, `asana_projects` → workspaceGid, `salesforce_sobject_fields` → sobjectName) and is an optional folder path for `onedrive_folders`.

**Step 4** — create the trigger node:

```bash
frontline workflows nodes create --data '{"type":"TRIGGER","position":{"positionX":0,"positionY":0},"data":{"type":"TRIGGER","triggerType":"COMPOSIO_TRIGGER","connectedAccountId":42,"triggerToolkit":"GOOGLEDRIVE","triggerSlug":"GOOGLEDRIVE_FILE_CREATED_TRIGGER","triggerConfig":{"folder_id":"1a2b3c","max_results":10}}}'
```

Saving the node subscribes to the event with the provider and writes `connectedAccountTriggerId` back into the node. **Never send `connectedAccountTriggerId` yourself** — it is output only. Updating the node re-subscribes and deleting it unsubscribes, so change the existing trigger instead of adding a second one.

The event body is available to every downstream node as the built-in **`{trigger_payload}`** variable (a JSON string).

**Supported `triggerSlug` values.** Snapshot for orientation only — `frontline integrations trigger-types` is authoritative and always current. An unlisted slug is rejected with `Unsupported trigger: <slug>`.

| triggerToolkit   | triggerSlug                                                                                                                                                                                                                                                   |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `GOOGLEDRIVE`    | `GOOGLEDRIVE_FILE_CREATED_TRIGGER`, `GOOGLEDRIVE_FILE_UPDATED_TRIGGER`, `GOOGLEDRIVE_FILE_DELETED_OR_TRASHED_TRIGGER`                                                                                                                                         |
| `GMAIL`          | `GMAIL_NEW_GMAIL_MESSAGE`                                                                                                                                                                                                                                     |
| `OUTLOOK`        | `OUTLOOK_MESSAGE_TRIGGER`, `OUTLOOK_EVENT_TRIGGER`, `OUTLOOK_EVENT_CHANGE_TRIGGER`, `OUTLOOK_CONTACT_TRIGGER`                                                                                                                                                 |
| `GOOGLECALENDAR` | `GOOGLECALENDAR_EVENT_STARTING_SOON_TRIGGER`, `GOOGLECALENDAR_ATTENDEE_RESPONSE_CHANGED_TRIGGER`                                                                                                                                                              |
| `GOOGLESHEETS`   | `GOOGLESHEETS_NEW_ROWS_TRIGGER`                                                                                                                                                                                                                               |
| `GOOGLEDOCS`     | `GOOGLEDOCS_DOCUMENT_UPDATED_TRIGGER`, `GOOGLEDOCS_DOCUMENT_DELETED_TRIGGER`                                                                                                                                                                                  |
| `ONE_DRIVE`      | `ONE_DRIVE_FILE_CREATED_TRIGGER`, `ONE_DRIVE_FILE_UPDATED`, `ONE_DRIVE_FOLDER_CREATED_TRIGGER`                                                                                                                                                                |
| `HUBSPOT`        | `HUBSPOT_CONTACT_CREATED_TRIGGER`, `HUBSPOT_DEAL_STAGE_UPDATED_TRIGGER`                                                                                                                                                                                       |
| `SALESFORCE`     | `SALESFORCE_NEW_LEAD_TRIGGER`, `SALESFORCE_NEW_CONTACT_TRIGGER`, `SALESFORCE_CONTACT_UPDATED_TRIGGER`, `SALESFORCE_ACCOUNT_CREATED_OR_UPDATED_TRIGGER`, `SALESFORCE_NEW_OR_UPDATED_OPPORTUNITY_TRIGGER`, `SALESFORCE_GENERIC_S_OBJECT_RECORD_UPDATED_TRIGGER` |
| `STRIPE`         | `STRIPE_CHECKOUT_SESSION_COMPLETED_TRIGGER`, `STRIPE_PAYMENT_FAILED_TRIGGER`                                                                                                                                                                                  |
| `ZENDESK`        | `ZENDESK_NEW_ZENDESK_TICKET_TRIGGER`                                                                                                                                                                                                                          |
| `ASANA`          | `ASANA_TASK_TRIGGER`                                                                                                                                                                                                                                          |
| `YOUTUBE`        | `YOUTUBE_NEW_ACTIVITY_TRIGGER`, `YOUTUBE_NEW_SUBSCRIPTION_TRIGGER`                                                                                                                                                                                            |

Slack has tools but no automation trigger — there is no way to start a workflow from a Slack message.

**`triggerConfig`** is validated per slug on save. Read the exact fields from `trigger-types` rather than memorising them; the rules are:

- A key the slug does not declare is **rejected**: `Unknown trigger config field for <slug>: folderId. Supported: query, folder_id, max_results`. Watch for snake_case vs camelCase — most fields are snake_case (`folder_id`, `spreadsheet_id`, `workspace_gid`) but Outlook and Gmail use camelCase (`folderId`, `calendarId`, `labelIds`).
- A bad value returns `Invalid trigger config: <field> - <message>`.
- Fields reported as `userConfigurable: false` (typically `interval`) are platform-managed: sending them is accepted and ignored.
- Fields reported as `required: true` must be present. At the time of writing: `GOOGLESHEETS_NEW_ROWS_TRIGGER` → `spreadsheet_id`; `ASANA_TASK_TRIGGER` → `workspace_gid` + `project_gid`; `YOUTUBE_NEW_ACTIVITY_TRIGGER` → `channel_id`; `HUBSPOT_*` → `app_id` + `developer_api_key`.
- Gmail accepts `query` **or** `labelIds`, not both.

Values are not verified against the provider: a well-formed but wrong `spreadsheet_id` saves fine and then the workflow never fires. Use `trigger-resources` to get real ids instead of typing them by hand.

**Resource types for `trigger-resources`:** `gmail_labels`, `googlesheets_spreadsheets`, `googlesheets_sheets`, `googledocs_documents`, `googledrive_folders`, `googledrive_shared_drives`, `onedrive_folders`, `asana_workspaces`, `asana_projects`, `salesforce_sobjects`, `salesforce_sobject_fields`, `outlook_folders`, `outlook_calendars`. The connected account must match the resource's toolkit, otherwise the call returns a 400 naming both toolkits.

### Scheduled Trigger (cron)

`SCHEDULED_TRIGGER` is its own node type, so `data.type` is `SCHEDULED_TRIGGER` and there is no `triggerType` key.

```bash
frontline workflows nodes create --data '{"type":"SCHEDULED_TRIGGER","position":{"positionX":0,"positionY":0},"data":{"type":"SCHEDULED_TRIGGER","cronExpression":"0 9 * * 1-5","timezone":"America/New_York","startTime":null,"endTime":null,"frequency":"DAILY"}}'
```

- `cronExpression` is validated with cron-validate; `timezone` must be an IANA name (`America/New_York`, `America/Argentina/Buenos_Aires`).
- `startTime` and `endTime` are **nullable but not optional** — send them as `null` when the schedule has no daily window, or the payload is rejected.
- Optional: `startDate`, `endDate`, and `frequency` (`INTERVALS` | `DAILY` | `WEEKLY` | `MONTHLY`). `frequency` is only a UI label; the cron expression is what schedules the run.
- The cron job is registered only while the automation is `ACTIVE`. Creating the node then activating, or activating then creating the node, both work. Setting the workflow back to `DRAFT` disables the job.

---

## Variables — How They Work

**Variables are plain text substitutions.** `{my_var}` is replaced at runtime with the exact string stored in that variable. There is no dot-access, no object traversal, no computed expressions — just a string replacement.

- `{webhook_payload}` → replaced with the full raw POST body as a string (the entire JSON blob).
- `{first_name}` → replaced with whatever text was stored in that variable by a prior node.

You **cannot** do `{webhook_payload.firstName}` — that is not valid syntax and will not extract a sub-property. The same rule applies everywhere: `{Loop.item.id}`, `{node_<uuid>.item.phone}`, and `{people_row_id}` when `people_row_id` is not a real variable name will **not** work.

### Loop variables

Inside a Loop (`ITERATION`) node, three runtime variables are exposed. **Always reference them by the loop node's `nodeId`** (look it up with `frontline workflows graph --table`):

- `{<loopNodeId>.item}` — current item (the whole value)
- `{<loopNodeId>.index}` — zero-based index
- `{<loopNodeId>.length}` — total item count

Example: if the loop node id is `node_d9de393b-4f82-45cd-9ea6-f084a664c48b`, use `{node_d9de393b-4f82-45cd-9ea6-f084a664c48b.item}` — not `{Loop.item}` unless you also set `alias` to exactly `Loop` and prefer alias-based names (node id is more reliable).

**`{<loopNodeId>.item}` is the entire current item.** If the item is an object, it is interpolated as a JSON string. There is **no** `{<loopNodeId>.item.field}` dot-access.

**To use a single field per iteration** (e.g. a People `id` or phone number):

1. **Preferred:** iterate an array that already contains scalars (e.g. `["id1","id2"]`) and use `{<loopNodeId>.item}` directly in `peopleRowId`, `phoneNumber`, etc.
2. **If items are objects:** add an `AI_CAPTURE` or `DATA_TRANSFORMER` node inside the loop body that reads `{<loopNodeId>.item}` and writes one field into a workflow variable; reference that variable downstream as `{my_extracted_id}`.

**`variablePath` on the Loop node** only navigates to a nested array inside the source variable (e.g. `data.items` on an API response). It does **not** map `[{id: "a"}, {id: "b"}]` to `["a","b"]` — setting `variablePath: "id"` on a list of objects yields `undefined`, not a list of ids.

---

## DYNAMIC_TABLES Node

Reads & writes records in any object/table. Actions: **CREATE, UPDATE, DELETE, SEARCH, SEARCH_BY_ID, CHANGE_RECORD_TYPE**.

### Step 1 — Get the object schema

```bash
frontline object get <object-name>
# e.g.: frontline object get people
```

From the response extract:

- `id` → `tableId`
- `record_types[0].id` → `recordTypeId` (the record type the node operates on)
- another record type's `id` → `targetRecordTypeId` (only for `CHANGE_RECORD_TYPE`)
- `fields[].name` → the field name string used as the **key** in `rowData` (e.g. `"First Name"`, `"Email"`)

### Step 2 — Build the node payload

`rowData` maps each **field name** (e.g. `"First Name"`) to a value — either a static string or a `{VARIABLE_NAME}` reference.

`inputModeByField` declares how each field value is interpreted:

- `"INPUT"` — static value, used as-is
- `"VARIABLE"` — interpolated at runtime; the value must contain a `{VARIABLE_NAME}` reference

**Important:** every variable referenced in `rowData` must already exist and must be populated by a prior node before this node executes. Create missing variables with `frontline workflows variables create`.

Example — create a People record with values from workflow variables:

```bash
frontline workflows nodes create --data '{
  "type": "DYNAMIC_TABLES",
  "position": {"positionX": 640, "positionY": 0},
  "data": {
    "type": "DYNAMIC_TABLES",
    "tableId": 2,
    "recordTypeId": 2,
    "actionType": "CREATE",
    "rowData": {
      "First Name":    "{first_name}",
      "Last Name":     "{last_name}",
      "Email":         "{email}",
      "Phone Number":  "{phone}",
      "Role":          "{role}"
    },
    "inputModeByField": {
      "First Name":    "VARIABLE",
      "Last Name":     "VARIABLE",
      "Email":         "VARIABLE",
      "Phone Number":  "VARIABLE",
      "Role":          "VARIABLE"
    }
  }
}'
```

### Actions & required fields

Every DYNAMIC_TABLES node needs `actionType` plus `recordTypeId` (or `tableId`). Each action requires specific extra fields — **the Public API rejects the node with `400` at create/update time if they're missing** (it no longer waits until the node runs):

| `actionType`         | Also required                   | Purpose                                  |
| -------------------- | ------------------------------- | ---------------------------------------- |
| `CREATE`             | `rowData`                       | Create a record                          |
| `UPDATE`             | `rowId` + `rowData`             | Update a record                          |
| `DELETE`             | `rowId`                         | Delete a record                          |
| `SEARCH`             | — (`query` / `search` optional) | Find records                             |
| `SEARCH_BY_ID`       | `rowId`                         | Fetch one record                         |
| `CHANGE_RECORD_TYPE` | `rowId` + `targetRecordTypeId`  | Move a record to a different record type |

**SEARCH output shape:** the node stores its result as a **top-level array of row objects** (field names as keys, e.g. `"First Name"`, `id`). It is **not** wrapped in `{ data: [...] }`. To loop over SEARCH results, point the Loop at the variable that holds the SEARCH output (often `{node_<search-node-id>}`) and leave `variablePath` **empty**.

Example — move a record to another record type:

```bash
frontline workflows nodes create --data '{
  "type": "DYNAMIC_TABLES",
  "position": {"positionX": 900, "positionY": 0},
  "data": {
    "type": "DYNAMIC_TABLES",
    "tableId": 2,
    "recordTypeId": 2,
    "actionType": "CHANGE_RECORD_TYPE",
    "rowId": "{record_id}",
    "targetRecordTypeId": 8
  }
}'
```

---

## Processing Webhook Payload into a Record

When the trigger is `INCOMING_WEBHOOK`, the full POST body is stored as-is in `{webhook_payload}` — a single string containing the raw JSON. Individual fields cannot be accessed directly from it.

### Pattern A — DATA_TRANSFORMER + DYNAMIC_TABLES (explicit)

1. Create one workflow variable per field you need:

```bash
frontline workflows variables create --name first_name --description "First name from webhook"
frontline workflows variables create --name last_name  --description "Last name from webhook"
frontline workflows variables create --name email      --description "Email from webhook"
frontline workflows variables create --name phone      --description "Phone from webhook"
frontline workflows variables create --name role       --description "Role from webhook"
```

2. Add a `DATA_TRANSFORMER` node that receives `{webhook_payload}` and extracts each field into its variable. Position it between the trigger and the DYNAMIC_TABLES node:

```bash
frontline workflows nodes create --data '{
  "type": "DATA_TRANSFORMER",
  "position": {"positionX": 320, "positionY": 0},
  "data": {
    "type": "DATA_TRANSFORMER",
    "prompt": "Given this JSON payload: {webhook_payload}\n\nExtract and return a JSON object with keys: first_name, last_name, email, phone, role. Use empty string if a field is missing.",
    "temperature": 0.2,
    "model": "gpt-4o-mini",
    "aiVendor": "OPENAI",
    "outputMode": "JSON"
  }
}'
```

Note: `model`, `aiVendor`, and `outputMode` must always be included; omitting them causes a validation error.

> **Models are account-specific — do not hardcode names.** `"gpt-4o-mini"` and other model names shown in this skill's examples are illustrative only and may not exist as an active `AiModel` in every account/environment (the create call fails with `400 not_found` if the `model`+`aiVendor` pair isn't found). Always resolve a real one first: `frontline ai-models list --type TEXT --table` (or `frontline ai-models default --type TEXT` for the account's default). From the row, either pass `aiModelId` (simplest — just the numeric `id`), or pass `model` (the row's `externalId`) together with `aiVendor` (`"OPENAI"`, `"ANTHROPIC"`, or `"GOOGLE"`). The same applies to `TRANSCRIPTION` and `FILE_ANALYSIS` models — filter by `--type TRANSCRIPTION` / `--type FILE_ANALYSIS` respectively.

3. Connect: `TRIGGER → DATA_TRANSFORMER → DYNAMIC_TABLES`.

4. The `DYNAMIC_TABLES` node uses `{first_name}`, `{email}` etc. — which are now populated by the transformer.

### Pattern B — TOOLS_AI agent (simpler, less setup)

Add a `TOOLS_AI` node with table access granted via `selectedRecordTypes` (there is **no** `agentId`/`assistantId` field on this node — automations aren't scoped to a chat agent). Pass the full payload as the prompt; the AI extracts fields and calls the table tool itself.

```bash
frontline workflows nodes create --data '{
  "type": "TOOLS_AI",
  "position": {"positionX": 320, "positionY": 0},
  "data": {
    "type": "TOOLS_AI",
    "conditions": [],
    "instructions": "You receive a webhook payload. Extract the contact fields (firstName, lastName, email, phone, role) and create a People record using your tools.",
    "prompt": "{webhook_payload}",
    "selectedRecordTypes": [
      { "recordTypeId": 2, "read": false, "create": true, "update": false, "delete": false }
    ]
  }
}'
```

- `conditions` is **required** on every `TOOLS_AI` node — pass `[]` if you don't need extra outgoing branches (it's how this node type supports multiple outgoing handles; see the Conditional Routing node for the condition shape).
- `selectedRecordTypes[].recordTypeId` comes from `frontline object get <name>` → `record_types[0].id`; set at least one permission (`read`/`create`/`update`/`delete`) to `true`.

Connect: `TRIGGER → TOOLS_AI`. No variables or extra nodes needed.

---

## Other Automation Action Nodes

### API node

The `API` node has **two outgoing handles**: `success` (HTTP 2xx) and `fail` (any error or non-2xx). Always connect both handles — never use `default`.

```bash
frontline workflows nodes create --data '{"type":"API","position":{"positionX":320,"positionY":0},"data":{"type":"API","url":"https://example.com/endpoint","method":"POST","headers":[{"key":"Content-Type","value":"application/json"}],"body":"{webhook_payload}"}}'

# Connect success path:
frontline workflows edges add --source <node-uuid> --source-handle success --target <next-node-uuid> --target-handle default

# Connect fail path:
frontline workflows edges add --source <node-uuid> --source-handle fail --target <error-node-uuid> --target-handle default
```

The full response body is available downstream as `{<nodeId>}`.

**Capturing specific values from the response — use the `variables` field** (objects/automations and flows both work this way):

```bash
frontline workflows nodes create --data '{"type":"API","position":{"positionX":320,"positionY":0},"data":{"type":"API","url":"https://api.example.com/value","method":"GET","headers":[],"variables":[{"key":"price","value":"data.price","fullResponse":false}]}}'
```

- `key` — the variable **name** to write into (referenced downstream as `{price}`).
- `value` — a **property path** into the JSON response (see below).
- `fullResponse` — set `true` to store the whole response body instead of a path.

**How `value` works (path syntax).** It's a simple property path into the parsed JSON response — **not** JSONPath (no `$`, wildcards, or filters):

- Dot notation for nested objects: `data.user.email`.
- Array index with brackets: `data.items[0].id` (brackets and dots are equivalent — `[0]` is treated as `.0`).
- A leading dot is optional (`.data.id` == `data.id`).
- Empty `value` (or `fullResponse: true`) captures the **whole** response body.

Given the response `{"data":{"items":[{"id":42,"price":9.99}],"total":1}}`:

| `value`               | captured |
| --------------------- | -------- |
| `data.total`          | `1`      |
| `data.items[0].id`    | `42`     |
| `data.items[0].price` | `9.99`   |

Notes:

- Path extraction only works when the response body is **JSON** (object/array). If the response is a plain string, use `fullResponse: true` to capture it.
- If the path doesn't resolve (a step is missing or `null`), the variable is **not set** — no error is raised.
- A captured object/array is stored as a JSON **string**; primitives are stored as their string value.
- Bracket keys must be word characters (letters, digits, `_`). Keys containing spaces or dots can't be addressed by this path syntax.

> **Footgun — the API node captures with `variables`, NOT `captureVariables`.** That is different from the AI nodes (see below). If you put `captureVariables` on an API node it is **silently dropped** (no error) and nothing is captured. Use `variables` for API nodes; use `captureVariables` only for AI nodes.

---

### Data transformer (AI extraction/normalization)

```bash
frontline workflows nodes create --data '{"type":"DATA_TRANSFORMER","position":{"positionX":320,"positionY":0},"data":{"type":"DATA_TRANSFORMER","prompt":"Extract firstName, lastName and email from: {webhook_payload}","temperature":0.2,"model":"gpt-4o-mini","aiVendor":"OPENAI","outputMode":"JSON"}}'
```

### CREATE_RECORD_ACTIVITY node

Logs a manual activity on an Object record at automation run time. Available in **both** automations and flows.

```bash
frontline workflows nodes create --data '{
  "type": "CREATE_RECORD_ACTIVITY",
  "position": { "positionX": 640, "positionY": 0 },
  "data": {
    "type": "CREATE_RECORD_ACTIVITY",
    "recordTypeId": 5,
    "rowId": "{contact_row_id}",
    "activityType": "PHONE_CALL",
    "content": "Llamada de seguimiento: {call_summary}"
  }
}'
```

| Field          | Notes                                                                                                                                                            |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `recordTypeId` | Numeric id of the Object's record type. Get it via `frontline object get <name>` → `record_types[].id`. Must be an OBJECT (not a Table). Validated at save time. |
| `rowId`        | MongoDB ObjectId of the record. Supports `{varName}` interpolation.                                                                                              |
| `activityType` | `NOTE` \| `EMAIL` \| `PHONE_CALL` \| `MEETING` \| `WHATSAPP`. Validated at save time.                                                                            |
| `content`      | Activity body text. Supports `{varName}` interpolation.                                                                                                          |

**Validation at save time (not at run time):**

- `recordTypeId` must point to an existing OBJECT record type in your account.
- `activityType` must be a valid enum value.
- Any `{varName}` in `rowId` or `content` must reference an existing variable (create it first). Unknown variable names return `400`.

**How to get the recordTypeId:**

```bash
frontline object get people    # → data.record_types[0].id
frontline object get deals     # → data.record_types[0].id
```

### WEBHOOK node (outgoing)

Sends data to an external URL. Useful for notifying third-party systems when an automation runs. Configure which context to include in the payload:

```bash
frontline workflows nodes create --data '{"type":"WEBHOOK","position":{"positionX":320,"positionY":0},"data":{"type":"WEBHOOK","url":"https://example.com/hook","includeConversationTranscript":false,"includeContactInfo":true,"includeFeedbackCaptured":false,"includeCapturedVariables":true,"includeWebhookPayload":false}}'
```

Fields: `includeConversationTranscript`, `includeContactInfo`, `includeFeedbackCaptured`, `includeCapturedVariables`, `includeWebhookPayload` — set to `true` to include that data in the POST body.

> Note: `WEBHOOK` (outgoing) is different from the `INCOMING_WEBHOOK` trigger type. The trigger receives data; this node sends it.

### AI_CAPTURE node

Uses an AI model to process a prompt and extract values into workflow variables. Useful when you need to parse or transform unstructured text and capture named fields.

```bash
frontline workflows nodes create --data '{"type":"AI_CAPTURE","position":{"positionX":320,"positionY":0},"data":{"type":"AI_CAPTURE","prompt":"Extract the customer name from: {webhook_payload}","instructions":"You are a data extraction assistant.","model":"gpt-4o-mini","aiVendor":"OPENAI","temperature":0.2,"captureVariables":[{"name":"customer_name","description":"Customer full name"}]}}'
```

Variables listed in `captureVariables` must already exist (`frontline workflows variables create`). The node populates them at runtime.

### TRANSCRIPTION node

Transcribes an audio file from a URL into text. The result is stored in workflow variables.

```bash
frontline workflows nodes create --data '{"type":"TRANSCRIPTION","position":{"positionX":320,"positionY":0},"data":{"type":"TRANSCRIPTION","audioUrl":"{audio_url}","language":"es","model":"gpt-4o-transcribe","aiVendor":"OPENAI","enableDiarization":false,"captureVariables":[{"name":"transcript","description":"Transcribed text"}]}}'
```

`audioUrl` supports variable interpolation. `language` is a BCP-47 language code (e.g. `"es"`, `"en"`). Set `enableDiarization: true` to separate speakers.

### FILE_ANALYSIS node

Runs OCR + AI analysis on a file fetched from a URL (PDFs, images, scanned documents). It produces **two** outputs: the raw extracted **OCR text** and an **XML analysis** guided by your prompt. Automation-only — rejected in flows.

```bash
frontline workflows nodes create --data '{"type":"FILE_ANALYSIS","position":{"positionX":320,"positionY":0},"data":{"type":"FILE_ANALYSIS","fileUrl":"{document_url}","prompt":"Extract the invoice total and vendor name.","model":"<external_id_from_ai_models_list>","aiVendor":"<vendor_from_same_row>","captureVariables":[{"id":<analysis_var_id>,"name":"<analysis_var_name>","description":"XML analysis output"}],"captureOcrVariable":{"id":<ocr_var_id>,"name":"<ocr_var_name>","description":"Extracted OCR text"}}}'
```

- `fileUrl` (required) supports variable interpolation — most commonly a `{var}` holding a file URL captured by an earlier node.
- `prompt` (optional, interpolable) guides the **XML analysis** output. OCR text extraction always runs regardless of the prompt.
- `model` / `aiVendor` reference a **FILE_ANALYSIS** model — list them with `frontline ai-models list --type FILE_ANALYSIS`. If omitted, the account default is used.
- `captureVariables` — at most **one** variable; receives the XML analysis. Unlike other capture nodes, FILE_ANALYSIS does **not** accept a name-only ref here — pass the full `{ id, name, description }` (the variable must already exist).
- `captureOcrVariable` — a single variable that receives the extracted OCR text. Also pass the full `{ id, name, description }`. Get the `id` from `frontline workflows variables create` (returned on creation) or `frontline workflows variables describe <name>`.

### SEND_MESSAGE node

Sends a message to a contact via WhatsApp, Instagram, or Messenger. Requires an active conversation context — most commonly used in workflows triggered by `CONVERSATION_IDLE`.

```bash
frontline workflows nodes create --data '{"type":"SEND_MESSAGE","position":{"positionX":320,"positionY":0},"data":{"type":"SEND_MESSAGE","whatsapp":{"messageType":"TEXT","message":"Hello {first_name}!"}}}'
```

Channel configs: `whatsapp`, `instagram`, `messenger`. Each has `messageType` (`TEXT` or `AI`). For `AI` type include `prompt`, `model`, `aiVendor`, `temperature`.

> **Not the same as `SEND_WHATSAPP_MESSAGE`.** `SEND_MESSAGE` pushes to an active conversation (typically `CONVERSATION_IDLE` trigger). `SEND_WHATSAPP_MESSAGE` sends a WhatsApp Business **template** to a phone number or People record without requiring an active conversation.

### Conditional Routing node

Branches the workflow using an **AI evaluator** — conditions are **natural-language / textual**, not a strict JavaScript expression engine. Write each condition however reads best to you or the model (e.g. "the phone number is not empty", `{confirmed} is true`, or `{score} >= 80`).

**How variables appear in conditions:** each `{variableName}` token is replaced before the AI sees the condition as `"variableName": <value>` (JSON). Example: `{confirmed} == true` becomes something like `"confirmed": true == true` in the prompt sent to the model.

```bash
frontline workflows nodes create --data '{"type":"CONDITIONAL_ROUTING","position":{"positionX":320,"positionY":0},"data":{"type":"CONDITIONAL_ROUTING","routingType":"CONDITIONAL_AI","conditions":[{"handleId":"yes","expression":"{confirmed} is true"},{"handleId":"no","expression":"{confirmed} is false"}],"model":"gpt-4o","aiVendor":"OPENAI","temperature":0.1}}'
```

- Use **exact variable names** only — no dot-access (`{<loopNodeId>.item}` is valid; `{<loopNodeId>.item.id}` is not).
- Connect one edge per `handleId` in `conditions`, plus a **`no-match`** edge for when none of the conditions apply.
- Inside a loop, reference the current item as `{<loopNodeId>.item}` (full item JSON), not `{Loop.item}` unless the alias is explicitly `Loop`.

### Loop (ITERATION) node

Iterates over an array stored in a workflow variable. The wire type is **`ITERATION`** (not `LOOP`).

```bash
frontline workflows nodes create --data '{"type":"ITERATION","position":{"positionX":320,"positionY":0},"data":{"type":"ITERATION","variableName":"items","variablePath":"data.items","continueOnError":false}}'
```

| Field             | Notes                                                                                                                                                                                                                                                                                                      |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `variableName`    | Name or alias of an existing workflow variable. Must resolve to an array (or JSON string parseable to an array) at runtime.                                                                                                                                                                                |
| `variablePath`    | Optional dot path to a **nested array** inside the variable (e.g. `data.items` on an API response). Leave empty when the variable is already an array (e.g. DYNAMIC*TABLES SEARCH output, or `{node*<uuid>}` from a prior node). Does **not** extract a field from each object (`id`on`[{id:"a"}]` fails). |
| `continueOnError` | When `true`, a node failure inside the loop body skips that item and continues. When `false` (default), any failure stops the whole automation.                                                                                                                                                            |

**Three outgoing handles** (never use `default`):

```bash
frontline workflows edges add --source <loop-node> --source-handle body --target <body-first-node> --target-handle default
frontline workflows edges add --source <loop-node> --source-handle completed --target <after-loop-node> --target-handle default
frontline workflows edges add --source <loop-node> --source-handle empty --target <empty-handler-node> --target-handle default
```

- `body` — entered when the list has items (for-each iteration).
- `completed` — entered after all items are processed (or after a `BREAK` node exits the loop).
- `empty` — entered when the list is null or empty. **Does not** fall through to `completed`.

**Variables exposed inside the loop** (use the loop node's **`nodeId`**, not a guessed alias):

- `{<loopNodeId>.item}` — current item (full value; JSON string if object)
- `{<loopNodeId>.index}` — zero-based index
- `{<loopNodeId>.length}` — total item count

No sub-properties: `{<loopNodeId>.item.id}` does not work. To pass a single field (id, phone) to a downstream node, iterate scalars or extract inside the loop body (see **Variables — How They Work**).

Limits: max **50 items** per loop invocation (if the resolved array has more than 50 items, the automation run fails before the loop body starts; no items are processed). Max **500** total automation execution steps (each node run counts one step).

### Break node

Exits the current loop early and continues on the loop's `completed` path. **Automation-only.**

```bash
frontline workflows nodes create --data '{"type":"BREAK","position":{"positionX":640,"positionY":0},"data":{"type":"BREAK"}}'
```

> Place `BREAK` only inside a Loop `body` branch. If it runs outside an active loop, the automation **fails** at runtime.

### Automation Status node

Changes another automation's operational status (live/draft/toggle). Does **not** publish draft graph changes. **Automation-only.**

```bash
frontline workflows list --table   # resolve automationId
frontline workflows nodes create --data '{"type":"AUTOMATION_STATUS","position":{"positionX":320,"positionY":0},"data":{"type":"AUTOMATION_STATUS","automationId":1,"automationName":"My workflow","action":"SET_ACTIVE"}}'
```

| Field            | Notes                                                                                      |
| ---------------- | ------------------------------------------------------------------------------------------ |
| `automationId`   | Target automation id. Validated at save time — must exist in your account.                 |
| `automationName` | Display label only (optional).                                                             |
| `action`         | `SET_ACTIVE` (live) · `SET_DRAFT` · `TOGGLE` (flip current status). Default: `SET_ACTIVE`. |

### Send WhatsApp Message node

Sends a WhatsApp Business **template** message. **Automation-only.** Distinct from `SEND_MESSAGE` (conversation push).

**Step 1 — resolve integration resources (read-only):**

```bash
frontline channels list --table
frontline channels whatsapp-templates --table
```

Only WhatsApp numbers with `canSendMessages: true` (an `assistantId` assigned) can be used as `phoneNumberId`.

**Step 2 — create the node:**

```bash
# PHONE_NUMBER mode (default): provide personName + phoneNumber
frontline workflows nodes create --data '{"type":"SEND_WHATSAPP_MESSAGE","position":{"positionX":320,"positionY":0},"data":{"type":"SEND_WHATSAPP_MESSAGE","recipientMode":"PHONE_NUMBER","personName":"{first_name} {last_name}","phoneNumber":"{phone_number}","phoneNumberId":"<meta-phone-number-id>","template":"hello_world","templateVariables":{"body":{"1":"{first_name}"}}}}'

# PEOPLE_RECORD mode: peopleRowId must be a single variable token (scalar id), not a sub-property
frontline workflows nodes create --data '{"type":"SEND_WHATSAPP_MESSAGE","position":{"positionX":320,"positionY":0},"data":{"type":"SEND_WHATSAPP_MESSAGE","recipientMode":"PEOPLE_RECORD","peopleRowId":"{<loopNodeId>.item}","phoneNumberId":"<meta-phone-number-id>","template":"hello_world","templateVariables":{}}}'
```

| Field               | Notes                                                                                                                                                             |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `recipientMode`     | `PHONE_NUMBER` (default) or `PEOPLE_RECORD`.                                                                                                                      |
| `personName`        | Required in `PHONE_NUMBER` mode. Supports `{var}` interpolation — one full variable name per token (e.g. `{first_name}`, not `{item.name}`).                      |
| `phoneNumber`       | Required in `PHONE_NUMBER` mode. Full international format (e.g. `+54911...`). Use `{<loopNodeId>.item}` when iterating scalars, not `{<loopNodeId>.item.phone}`. |
| `peopleRowId`       | Required in `PEOPLE_RECORD` mode. MongoDB ObjectId string. Use `{var}` or `{<loopNodeId>.item}` when the loop iterates ids — never `{<loopNodeId>.item.id}`.      |
| `phoneNumberId`     | Meta WhatsApp Business phone number id. Validated at save time — must exist and have `assistantId`.                                                               |
| `template`          | Approved template name from `frontline channels whatsapp-templates`.                                                                                              |
| `templateVariables` | Maps template parameter ids to values: `{ body: { "1": "{first_name}" }, header: {}, buttons: [] }`.                                                              |

> If no approved templates are returned, you can still save the node with `"template": ""` and ask the user to verify their WhatsApp templates in Meta. The node will fail at runtime until a valid template is set.

### Activate

```bash
frontline workflows update --status ACTIVE
```

---

## Agent Flows

Agent flows live inside an AI agent and control conversation logic.

### How flows run & how they are triggered

- **Default Start flow.** Every agent ships with a default flow named **"Start"** (in `DRAFT`) that contains a single **`START`** node. This flow runs **automatically at the beginning of every conversation** — build your first-contact logic here (greeting, capturing data, creating a record). To inspect it: `frontline agents flows list` → the flow with `isDefault: true`; add nodes after its existing `START` node.
- **The `START` node is unique.** Only the default Start flow may contain a `START` node. The API **rejects** creating a `START` node in any other flow (`400`).
- **Other flows are triggered**, they don't auto-run. A non-default flow starts with a **`TRIGGER_INTENT`** node and is entered when it matches the user. Two ways to configure when it fires:
    - **Intents** — assign `intentIds` to the `TRIGGER_INTENT` node. When the user's message matches one of those intents, the flow is entered. Create intents with `frontline agents intents create`.
    - **Agentic routing** — set `agenticRouting` to a natural-language instruction describing _when_ to enter the flow (e.g. "when the user wants to cancel an order"). The agent decides based on that instruction and the user's intention.
- **Default-message rule (all flows).** If a flow finishes a turn without producing a message for the user (e.g. it only captured variables or ran a tool action), the agent automatically sends a **default AI-generated message** so the user always gets a reply.
- **Capturing contact info creates a Person.** Capturing into the built-in contact variables `first_name`, `last_name`, `email`, or `phone_number` writes to — and **creates/identifies** — the conversation's **People** record (deduplicated by email). To register a contact from a flow, just capture into those variable names; no record-create step is needed (a separate create would make a duplicate).

### Setup

```bash
frontline agents use <agentId>
frontline agents flows create --name "My Flow"
frontline agents flows use <flowId>
frontline agents flows graph --table   # inspect before each change
```

### Supported node types

`START`, `TRIGGER_INTENT`, `SAY_AI`, `RESPONSE_AI`, `TOOLS_AI`, `API`, `CONDITIONAL_ROUTING`.

Use exactly one initial node: `START` or `TRIGGER_INTENT`. `DYNAMIC_TABLES` ("Data Action") is **not** available in flows (automation-only) — do record operations through a `TOOLS_AI` node with table tools.

### Node payloads

Start:

```bash
frontline agents flows nodes create --data '{"type":"START","position":{"positionX":0,"positionY":0}}'
```

Intent trigger:

```bash
frontline agents flows nodes create --data '{"type":"TRIGGER_INTENT","position":{"positionX":0,"positionY":0},"data":{"type":"TRIGGER_INTENT","intentIds":[123],"agenticRouting":null}}'
```

Say AI (static or AI-generated message):

```bash
frontline agents flows nodes create --data '{"type":"SAY_AI","position":{"positionX":320,"positionY":0},"data":{"type":"SAY_AI","sayWithAi":false,"message":"Hello, how can I help?"}}'
```

AI agent node — `TOOLS_AI` (agent that can run tools) or `RESPONSE_AI`. To make it **capture values into variables**, list them in `captureVariables`:

```bash
frontline agents flows nodes create --data '{"type":"TOOLS_AI","position":{"positionX":320,"positionY":0},"data":{"type":"TOOLS_AI","conditions":[],"instructions":"Ask for and capture the customer name.","prompt":"Capture the value into {customer_name}","temperature":0.2,"model":"gpt-4o-mini","aiVendor":"OPENAI","captureVariables":[{"id":2080,"name":"customer_name","description":"Customer name"}]}}'
```

- `captureVariables` items are `{ id, name, description }` and reference an **existing agent variable**. Create it first with `frontline agents variables create --name customer_name --description "..."` and use the returned `id`. The AI extracts the value (guided by your `prompt`/`instructions`) and stores it under that name; reference it downstream as `{customer_name}`.
- The variable is matched at runtime by **name**, so the same name can be captured by an AI node and an API node (`variables` field) and they resolve to the same `{name}`.

> **Footgun:** AI nodes capture with **`captureVariables`**; the API node captures with **`variables`** (different field/shape — see the API node section). Mixing them up is silently ignored, not an error.

`RESPONSE_AI` is a plain assistant reply (no tool calls) generated with a specific model config. Unlike `TOOLS_AI`, it requires `assistantId` and `exitNodeWhen`:

```bash
frontline agents flows nodes create --data '{"type":"RESPONSE_AI","position":{"positionX":320,"positionY":0},"data":{"type":"RESPONSE_AI","assistantId":"<agent-id>","model":"<external_id_from_ai_models_list>","aiVendor":"<vendor_from_same_row>","temperature":0.2,"instructions":"Answer the customer politely and concisely.","captureVariables":[],"exitNodeWhen":"ALL_VARIABLES"}}'
```

Required fields beyond the common node envelope: `assistantId` (the owning agent's id), `model` + `aiVendor` (or `aiModelId` — resolve with `frontline ai-models list --type TEXT --table`, do not assume `gpt-4o-mini` or any other name exists in this account), `temperature`, `captureVariables` (`[]` if none), and `exitNodeWhen` — one of `ALL_VARIABLES`, `FLOW_TRIGGERED`, `ANY_VARIABLES` (controls when the node considers the turn finished relative to `captureVariables`).

`API` node — same **fixed `success`/`fail` handles** as in automations (see the API node section above); the canvas never renders a `default` handle for this node type, so connecting `default` is rejected:

```bash
frontline agents flows nodes create --data '{"type":"API","position":{"positionX":320,"positionY":0},"data":{"type":"API","url":"https://example.com","method":"GET","headers":[]}}'
frontline agents flows edges add --source <api-node-id> --source-handle success --target <next-node-id> --target-handle default
frontline agents flows edges add --source <api-node-id> --source-handle fail --target <error-node-id> --target-handle default
```

Conditional routing (AI evaluator — conditions are textual; `{var}` becomes `"var": value` in the prompt; connect a `no-match` handle; no dot-access on variables):

```bash
frontline agents flows nodes create --data '{"type":"CONDITIONAL_ROUTING","position":{"positionX":320,"positionY":0},"data":{"type":"CONDITIONAL_ROUTING","routingType":"CONDITIONAL_AI","conditions":[{"handleId":"yes","expression":"{confirmed} is true"},{"handleId":"no","expression":"{confirmed} is false"}]}}'
```

> To read or write records **inside a flow**, use a `TOOLS_AI` node whose agent has table tools configured — the `DYNAMIC_TABLES` ("Data Action") node is automation-only and is rejected in flows.

### Flow edges

```bash
frontline agents flows edges add --source node_11111111-1111-1111-1111-111111111111 --source-handle default --target node_22222222-2222-2222-2222-222222222222 --target-handle default

# Conditional routing handles:
frontline agents flows edges add --source node_22222222-2222-2222-2222-222222222222 --source-handle yes --target node_33333333-3333-3333-3333-333333333333 --target-handle default
frontline agents flows edges add --source node_22222222-2222-2222-2222-222222222222 --source-handle no  --target node_44444444-4444-4444-4444-444444444444 --target-handle default
```

Activate:

```bash
frontline agents flows update --name "My Flow" --status ACTIVE
```

---

## Edges (both automations and flows)

Connect nodes:

```bash
frontline workflows edges add \
  --source node_11111111-1111-1111-1111-111111111111 \
  --source-handle default \
  --target node_22222222-2222-2222-2222-222222222222 \
  --target-handle default
```

Remove an edge:

```bash
frontline workflows edges remove \
  --source node_11111111-1111-1111-1111-111111111111 \
  --source-handle default \
  --target node_22222222-2222-2222-2222-222222222222 \
  --target-handle default
```

Rules:

- One outgoing edge per node (except `CONDITIONAL_ROUTING`, `TOOLS_AI`, `API`, and `ITERATION` which support multiple handles).
- `TOOLS_AI.conditions` is a **required** field in both automations and flows — pass `[]` if you don't need extra branches; omitting the key returns `400`.
- No self-edges, no cycles.
- Source and target nodes must exist.
- Deleting a node removes all its edges.

---

## Variables

Create before referencing:

```bash
frontline workflows variables create --name my_var --description "..."
```

Reference in any interpolable field as `{my_var}`.

> For **agent flows**, create variables with `frontline agents variables create` (agent-scoped). Variables are matched by **name** at runtime.

### Which field captures a value into a variable

Different node types use different fields to populate variables — do not mix them up:

| Node                                                     | Capture field                                                  | Item shape                                                                            |
| -------------------------------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `TOOLS_AI`, `RESPONSE_AI`, `AI_CAPTURE`, `TRANSCRIPTION` | `captureVariables`                                             | reference an existing variable (by `{name}` or `{id}`)                                |
| `FILE_ANALYSIS`                                          | `captureVariables` (analysis), `captureOcrVariable` (OCR text) | each a full `{ id, name, description }` ref — **not** name-resolved, so pass the `id` |
| `API`                                                    | `variables`                                                    | `{ key, value, fullResponse }` — `key` is an existing variable name                   |

> **Capture variables must reference a variable that already exists.** Create it first (`frontline workflows variables create` for automations, `frontline agents variables create` for flows). In `captureVariables` you may pass just `{ "name": "<var>" }` (or `{ "id": <id> }`) — the API resolves it and stores the canonical `{ id, name, description }` so the app links and renders it. An unknown name/id returns `400` (`not_found` at `data.captureVariables[i]`). Same for the API node: `variables[].key` must be an existing variable name, else `400`. **Exception:** the `FILE_ANALYSIS` node validates `captureVariables` / `captureOcrVariable` strictly and does **not** accept a name-only ref — pass the full `{ id, name }` there.

Putting the wrong **field** on a node (e.g. `captureVariables` on an API node) is silently ignored — the value just never gets captured.

Automation workflows also expose each node's output as a runtime variable named after its `nodeId`. A node with `nodeId` `node_11111111-1111-1111-1111-111111111111` is accessible downstream as `{node_11111111-1111-1111-1111-111111111111}`.

**Critical — never invent node IDs.** When writing a prompt or expression that references another node's output, you must first retrieve the actual `nodeId` from the workflow:

```bash
frontline workflows graph --table   # shows all nodes with their nodeIds
```

Do NOT guess or hard-code a `nodeId`. Always look it up first and use the exact value.

Interpolable fields: API `url`, `headers[].value`, `parameters[].value`, `body`; Send Message `message`; Say AI `message`, `prompt`; Response AI `instructions`; Tools AI `instructions`, `prompt`; AI Capture `prompt`, `instructions`; Data Transformer `prompt`; Conditional Routing `conditions[].expression`; Dynamic Tables `rowId`, `search`, `rowData` values; Transcription `audioUrl`; File Analysis `fileUrl`, `prompt`.

---

## Validation Checklist

- [ ] After `nodes create`, use the returned `nodeId` (format `node_<uuid>`) for edges and `{node_<uuid>}` references.
- [ ] Set a custom alias with `nodes update` after create when the exact label matters.
- [ ] Exactly one trigger node per workflow/flow.
- [ ] `data.type` matches the node `type`.
- [ ] All variables referenced in `rowData` exist and are populated by a prior node.
- [ ] `tableId` and `recordTypeId` obtained from `frontline object get <name>` (not guessed).
- [ ] `rowData` keys are field **names** from the object schema (e.g. `"First Name"`, `"Email"`) — not UUIDs.
- [ ] Node output references (`{node_<uuid>}`) use the **actual** `nodeId` retrieved via `frontline workflows graph --table` — never invented.
- [ ] Conversation triggers (`CONVERSATION_ENDED`, `CONVERSATION_IDLE`, `FEEDBACK_CAPTURED`) set `triggeredByAgentIds` with real agent UUIDs, and `triggeredBy` is not `USER`.
- [ ] `CONVERSATION_IDLE` also has `enableIdle` + `idleSettings` on the agent's channel.
- [ ] The workflow is live (`frontline workflows update --status ACTIVE`) — a `DRAFT` workflow never fires.
- [ ] `SEND_MESSAGE` is only used when the trigger type is `CONVERSATION_IDLE`.
- [ ] `ITERATION` has all three handles connected (`body`, `completed`, `empty`).
- [ ] `BREAK` is placed only inside a Loop `body` branch.
- [ ] `SEND_WHATSAPP_MESSAGE.phoneNumberId` comes from `frontline channels list` with `canSendMessages: true`.
- [ ] One outgoing edge per node (unless multi-handle node type).
- [ ] Run `frontline workflows graph --table` after each structural change.

---

## Reference validation (avoid 400s)

Every `aiModelId`, `customToolIds`, `tableId`, `recordTypeId`, `triggeredByAgentIds[]`, `triggerByWebhookIds[]`, `connectedAccountId`, `knowledgeBaseIds`, `playbookIds`, `selectedRecordTypes[].recordTypeId` you put in a node's `data` is **validated against the database before the node is persisted**. A non-existent id returns `400 bad_request` with `details.issues[].code === "not_found"` and the node is dropped.

For `TOOLS_AI` table access, use `selectedRecordTypes` with `recordTypeId` and at least one permission set to `true`:

```json
"selectedRecordTypes": [
  { "recordTypeId": 5, "read": true, "create": true, "update": true, "delete": false }
]
```

Additionally:

- `SCHEDULED_TRIGGER.cronExpression` is validated by `cron-validate`. `SCHEDULED_TRIGGER.timezone` must be an IANA zone accepted by the server (`Intl.supportedValuesOf("timeZone")`). Some environments run Node with a reduced ICU dataset and reject zones like `America/Argentina/Buenos_Aires` or `UTC` with "Unknown IANA timezone" — use a widely supported zone (e.g. `America/New_York`) or try another if validation fails.
- `WEBHOOK.url` and `API.url` must be valid URLs.

Before composing a node, look up the referenced resources:

- `frontline ai-models list` for `aiModelId`.
- `frontline custom-tools list` for `customToolIds`.
- `frontline agents list` for `triggeredByAgentIds[]`.
- `frontline incoming-webhooks create` (you can't list them in the Public API yet) or coordinate with whoever already created the webhook.
- `frontline object schema <name>` / `frontline table schema <name>` for `tableId`.
- `frontline object record-type list <name>` for `recordTypeId`.
- `frontline workflows list` for `AUTOMATION_STATUS.automationId`.
- `frontline channels list` for `SEND_WHATSAPP_MESSAGE.phoneNumberId` (must have `canSendMessages: true`).
- `frontline channels whatsapp-templates` for `SEND_WHATSAPP_MESSAGE.template` name.
- `frontline integrations list` for `connectedAccountId` values in agent settings and TOOLS_AI nodes.

A `not_found` response lists every offending `path` in a single payload — fix all of them in one update rather than discovering them one at a time.

---

## See also

- Full reference: <https://docs.getfrontline.ai/docs> (concepts) and <https://docs.getfrontline.ai/cli> (command reference).
- App UI walkthroughs (channels, billing, settings): <https://help.getfrontline.ai>.
