---
name: frontline-workflows
allowed-tools: Bash(frontline:*)
description: Create, edit, connect, inspect, and delete Frontline automation workflows using the Frontline CLI. Use when the user asks to build workflows, add nodes or edges, manage workflow context, inspect status, or view analytics.
---

## Prerequisites

- The `frontline` CLI must be installed (`npm i -g @getfrontline/cli`).
- The user must be authenticated (`frontline auth login`).

## Commands

### List all workflows

```bash
frontline workflows list [--status <status>] [--table] [--debug]
```

Output is **JSON by default** (`--json` is accepted as a documented no-op — it never changes behavior). Use `--table`/`--pretty` to get human-readable output instead.

| Flag                | Description                                        |
| ------------------- | -------------------------------------------------- |
| `--status <status>` | Filter by status: `active`, `inactive`, or `draft` |
| `--table`           | Render as a human-readable table instead of JSON   |
| `--api-key <key>`   | Override the stored API key for this request       |
| `--profile <name>`  | Use a specific CLI profile                         |
| `--debug`           | Show HTTP request/response diagnostics             |

**Example:**

```bash
# List all workflows as JSON (default)
frontline workflows list

# List only active workflows as a table
frontline workflows list --status active --table
```

**Output columns:** `id`, `name`, `status`, `triggerType`, `runsCount`, `lastRunDate`

### Create and select a workflow

```bash
frontline workflows create --name "Daily CRM Sync" [--description "..."]
frontline workflows use <workflowId>
frontline workflows describe [--include-nodes]
frontline workflows graph [--table]
```

`create` saves the created workflow ID as the active workflow for the current
profile. `use` changes the active workflow. All graph commands accept
`--workflow-id <id>` to override the active workflow, which is preferred for
scripts and CI.

### Update or delete a workflow

```bash
frontline workflows update --status ACTIVE          # name is optional; fetched automatically if omitted
frontline workflows update --name "Daily CRM Sync" --status ACTIVE
frontline workflows delete
```

Use a USER API key for mutations. GENERAL keys can still read account-level
workflow data where the API allows it.

### Manage variables

Workflow variable commands use the active workflow by default. Override with
`--workflow-id <id>` in scripts and CI.

```bash
frontline workflows variables list --table
frontline workflows variables all
frontline workflows variables create --name order_id --description "Order ID"
frontline workflows variables describe 123
frontline workflows variables update 123 --name order_id --pattern "^[0-9]+$"
frontline workflows variables delete 123
frontline workflows variables check-name order_id
```

Use variables inside text fields as `{VARIABLE_NAME}`. Automation workflows also
make each node output available by node ID — node IDs follow the `node_<uuid>`
format, so a node with `nodeId` `node_a1b2c3d4-e5f6-7890-abcd-ef1234567890` is
referenced downstream as `{node_a1b2c3d4-e5f6-7890-abcd-ef1234567890}`.

## Building Workflow Graphs

Always inspect the graph before changing it:

```bash
frontline workflows graph --table
frontline workflows nodes list --table
```

### Node identity

Do **not** send `nodeId` or `alias` in `nodes create`. The server assigns both and returns them in the **201** JSON. Use `frontline workflows graph --table` or the create response before `edges add` or `{node_<uuid>}` references. Custom aliases: `nodes update <nodeId> --data '{"alias":"..."}'`.

### Create nodes

The full trigger reference (all `triggerType` values — `CONTACT_CREATED`,
`CONTACT_UPDATED`, `CONVERSATION_ENDED`, `FEEDBACK_CAPTURED`, `CONVERSATION_IDLE`,
`INCOMING_WEBHOOK`, `OBJECT_RECORD_CREATED`, `COMPOSIO_TRIGGER` — plus
`SCHEDULED_TRIGGER`, with required fields and payload variables) lives in the
`workflow-builder` skill. Two common examples follow.

Trigger node (CONTACT_CREATED):

```bash
frontline workflows nodes create --data '{"type":"TRIGGER","position":{"positionX":0,"positionY":0},"data":{"type":"TRIGGER","triggerType":"CONTACT_CREATED"}}'
```

Conversation trigger (`CONVERSATION_ENDED`, `CONVERSATION_IDLE`, `FEEDBACK_CAPTURED`) — these fire per agent, so `triggeredByAgentIds` is required. Without it the node saves but the workflow never runs:

```bash
frontline agents list --table   # copy the agent uuid from the id column
frontline workflows nodes create --data '{"type":"TRIGGER","position":{"positionX":0,"positionY":0},"data":{"type":"TRIGGER","triggerType":"CONVERSATION_IDLE","triggeredByAgentIds":["550e8400-e29b-41d4-a716-446655440000"]}}'
```

Do not set `triggeredBy` to `USER` on these — conversation events always come from the agent. `CONVERSATION_IDLE` additionally requires `enableIdle` and `idleSettings` on the agent's channel (`frontline agents settings get/update <channel>`). See the `workflow-builder` skill for the full walkthrough.

Incoming webhook trigger — first create the webhook resource:

```bash
frontline incoming-webhooks create --name "My Webhook"
# Save the returned id
frontline workflows nodes create --data '{"type":"TRIGGER","position":{"positionX":0,"positionY":0},"data":{"type":"TRIGGER","triggerType":"INCOMING_WEBHOOK","triggerByWebhookIds":["<incoming-webhook-id>"]}}'
```

When this fires, the POST body is available as `{webhook_payload}` in all downstream nodes.

Integration trigger (`COMPOSIO_TRIGGER`) — fires on a third-party event such as a new Google Drive file or Gmail message. Requires `connectedAccountId` + `triggerToolkit` (both from `frontline integrations list --table`) and a `triggerSlug`:

```bash
frontline workflows nodes create --data '{"type":"TRIGGER","position":{"positionX":0,"positionY":0},"data":{"type":"TRIGGER","triggerType":"COMPOSIO_TRIGGER","connectedAccountId":42,"triggerToolkit":"GOOGLEDRIVE","triggerSlug":"GOOGLEDRIVE_FILE_CREATED_TRIGGER"}}'
```

Saving the node subscribes with the provider and fills in `connectedAccountTriggerId` — never send that field yourself. The event body arrives as `{trigger_payload}`.

Discover slugs and config fields instead of guessing (an unlisted slug fails with `Unsupported trigger: <slug>`, and a misnamed config key fails with `Unknown trigger config field`):

```bash
frontline integrations trigger-types --toolkit GOOGLEDRIVE --table
frontline integrations trigger-resources --type googledrive_folders --connected-account-id 42 --table
```

`trigger-types` lists each event's required and optional `triggerConfig` fields and which of them have a picker; `trigger-resources` returns the actual ids to put in those fields. See the `workflow-builder` skill for the full walkthrough.

Scheduled trigger (cron) is a **different node type**, not a `triggerType`. `startTime` and `endTime` are nullable but must be present:

```bash
frontline workflows nodes create --data '{"type":"SCHEDULED_TRIGGER","position":{"positionX":0,"positionY":0},"data":{"type":"SCHEDULED_TRIGGER","cronExpression":"0 9 * * 1-5","timezone":"America/New_York","startTime":null,"endTime":null,"frequency":"DAILY"}}'
```

The cron job only runs while the workflow is `ACTIVE`; setting it back to `DRAFT` disables the schedule.

API action node (**two fixed outgoing handles: `success`/`fail`** — the canvas never renders a `default` handle for this node type; connecting `default` is rejected):

```bash
frontline workflows nodes create --data '{"type":"API","position":{"positionX":320,"positionY":0},"data":{"type":"API","url":"https://example.com","method":"GET","headers":[]}}'
frontline workflows edges add --source <api-node-id> --source-handle success --target <next-node-id> --target-handle default
frontline workflows edges add --source <api-node-id> --source-handle fail --target <error-node-id> --target-handle default
```

Supported automation node types:

`TRIGGER`, `SCHEDULED_TRIGGER`, `WEBHOOK`, `TOOLS_AI`, `API`,
`CONDITIONAL_ROUTING`, `AI_CAPTURE`, `DATA_TRANSFORMER`, `DYNAMIC_TABLES`,
`CREATE_RECORD_ACTIVITY`, `ITERATION`, `BREAK`, `AUTOMATION_STATUS`,
`SEND_MESSAGE`, `SEND_WHATSAPP_MESSAGE`, `TRANSCRIPTION`, `FILE_ANALYSIS`.

### Integrations (read-only — for Send WhatsApp Message nodes)

```bash
frontline channels list --table
frontline channels whatsapp-templates --table
```

Use `channels list` to pick a `phoneNumberId` where `canSendMessages` is true.
Use `channels whatsapp-templates` to pick an approved template name.

For OAuth connected accounts (Google Sheets, Gmail, etc.), use `frontline integrations list --table` and pass the returned `id` as `connectedAccountId`.

### Loop (ITERATION) node

Wire type is `ITERATION`. Iterates an array variable with three handles: `body`, `completed`, `empty`.

```bash
frontline workflows nodes create --data '{"type":"ITERATION","position":{"positionX":320,"positionY":0},"data":{"type":"ITERATION","variableName":"items","variablePath":"data.items","continueOnError":false}}'
# Use the nodeId returned above (<loop-node-id>) for all three edges:
frontline workflows edges add --source <loop-node-id> --source-handle body --target <body-node> --target-handle default
frontline workflows edges add --source <loop-node-id> --source-handle completed --target <after-loop> --target-handle default
frontline workflows edges add --source <loop-node-id> --source-handle empty --target <empty-handler> --target-handle default
```

Inside the loop, use the loop node's **`nodeId`** (from `frontline workflows graph --table`):

- `{<loopNodeId>.item}` — current item (full value; JSON string if the item is an object)
- `{<loopNodeId>.index}` — zero-based index
- `{<loopNodeId>.length}` — total count

**No sub-properties:** `{<loopNodeId>.item.id}` / `{<loopNodeId>.item.phone}` do not work. To use one field per iteration, loop over scalars and use `{<loopNodeId>.item}` directly, or extract a field inside the loop with `AI_CAPTURE` / `DATA_TRANSFORMER`.

**Limits:** At most **50 items** per loop invocation. More than 50 items fails the automation run before the loop body starts (no partial processing). Max **500** automation execution steps total.

For DYNAMIC*TABLES **SEARCH** output, the result is a top-level array of rows — set `variablePath` empty when looping over `{node*<search-node-id>}`.

### Send WhatsApp Message node

```bash
frontline workflows nodes create --data '{"type":"SEND_WHATSAPP_MESSAGE","position":{"positionX":640,"positionY":0},"data":{"type":"SEND_WHATSAPP_MESSAGE","recipientMode":"PHONE_NUMBER","personName":"{first_name} {last_name}","phoneNumber":"{phone_number}","phoneNumberId":"<meta-phone-number-id>","template":"hello_world","templateVariables":{"body":{"1":"{first_name}"}}}}'
```

### DYNAMIC_TABLES node

Used to create, update, delete, search, or change the record type of records in an object. Always get the object schema first:

```bash
frontline object get <object-name>
# id → tableId, record_types[0].id → recordTypeId, fields[].name → rowData keys
```

`rowData` maps **field names** (e.g. `"First Name"`, `"Email"`) — not UUIDs — to static values or `{VARIABLE_NAME}` references. `inputModeByField` sets `"INPUT"` (static) or `"VARIABLE"` (interpolated) per field name. All variables used must exist and be populated by a prior node.

**Variables are plain text substitutions** — `{my_var}` is replaced with the exact string stored in that variable. There is no dot-access: `{webhook_payload.firstName}` is not valid.

```bash
frontline workflows nodes create --data '{"type":"DYNAMIC_TABLES","position":{"positionX":640,"positionY":0},"data":{"type":"DYNAMIC_TABLES","tableId":2,"recordTypeId":2,"actionType":"CREATE","rowData":{"First Name":"{first_name}","Email":"{email}"},"inputModeByField":{"First Name":"VARIABLE","Email":"VARIABLE"}}}'
```

`actionType` values: `CREATE`, `UPDATE`, `DELETE`, `SEARCH`, `SEARCH_BY_ID`, `CHANGE_RECORD_TYPE`.

Required fields per action (the Public API returns `400` at create/update if missing): `CREATE` → `rowData`; `UPDATE` → `rowId` + `rowData`; `DELETE` / `SEARCH_BY_ID` → `rowId`; `CHANGE_RECORD_TYPE` → `rowId` + `targetRecordTypeId` (the destination record type id).

### FILE_ANALYSIS node

Runs OCR + AI analysis on a file from a URL (PDF, image, scanned doc). Produces two outputs: the extracted **OCR text** and an **XML analysis** guided by `prompt`.

```bash
frontline workflows nodes create --data '{"type":"FILE_ANALYSIS","position":{"positionX":640,"positionY":0},"data":{"type":"FILE_ANALYSIS","fileUrl":"{document_url}","prompt":"Extract the invoice total and vendor name.","model":"<external_id_from_ai_models_list>","aiVendor":"<vendor_from_same_row>","captureVariables":[{"id":<analysis_var_id>,"name":"<analysis_var_name>","description":"XML analysis output"}],"captureOcrVariable":{"id":<ocr_var_id>,"name":"<ocr_var_name>","description":"Extracted OCR text"}}}'
```

- `fileUrl` (required, interpolable) usually references a `{var}` holding a file URL. `prompt` (optional, interpolable) guides the XML analysis; OCR always runs.
- `model` / `aiVendor` reference a model of type `FILE_ANALYSIS` — list them with `frontline ai-models list --type FILE_ANALYSIS`.
- `captureVariables` (at most one) stores the XML analysis and `captureOcrVariable` stores the OCR text. Both must already exist and both take the full `{ id, name, description }` — a name-only ref is rejected. Get the `id` from `frontline workflows variables create` / `describe`.

### Connect nodes

```bash
frontline workflows edges add \
  --source node_11111111-1111-1111-1111-111111111111 \
  --source-handle default \
  --target node_22222222-2222-2222-2222-222222222222 \
  --target-handle default
```

The API enforces one outgoing edge per node (except `CONDITIONAL_ROUTING`,
`TOOLS_AI`, and `API`, which support multiple outgoing handles), no self-edges,
source/target existence, and no cycles.

### Edit and delete nodes

```bash
frontline workflows nodes update node_22222222-2222-2222-2222-222222222222 --data '{"alias":"Fetch external data"}'
frontline workflows nodes delete node_22222222-2222-2222-2222-222222222222
```

Deleting a node also removes incoming and outgoing edges.

### Remove an edge

```bash
frontline workflows edges remove \
  --source node_11111111-1111-1111-1111-111111111111 \
  --source-handle default \
  --target node_22222222-2222-2222-2222-222222222222 \
  --target-handle default
```

## Validation Checklist

- Use exactly one initial trigger node (`TRIGGER` or `SCHEDULED_TRIGGER`).
- Conversation triggers must carry `triggeredByAgentIds`.
- All node IDs must follow `node_<uuid>` format.
- Use only supported automation node types.
- Ensure `data.type` matches the node `type`.
- Connect only existing source and target nodes.
- Keep a single outgoing edge per node (multi-handle exceptions: `CONDITIONAL_ROUTING`, `TOOLS_AI`, `API`).
- Avoid self-edges and cycles.
- Inspect `frontline workflows graph` after each structural change.

## Variable Interpolation

Interpolable workflow fields include API `url`, `headers[].value`,
`parameters[].value`, `body`; Send Message / Say AI `message` and `prompt`;
Response AI `instructions`; Tools AI `instructions` and `prompt`; AI Capture
`prompt` and `instructions`; Data Transformer `prompt`; Conditional Routing AI
`conditions[].expression`; Dynamic Tables `rowId`, `search`, `rowData` values;
Transcription `audioUrl`; and WhatsApp template variables in
`templateVariables.header`, `templateVariables.body`, and
`templateVariables.buttons`.

Each node's output is also available as `{nodeId}` in downstream nodes.

### Get analytics for a specific workflow

```bash
frontline workflows analytics [workflowId] [--workflow-id <id>] [--start-date <YYYY-MM-DD>] [--end-date <YYYY-MM-DD>] [--table] [--debug]
```

Output is **JSON by default** (`--json` is accepted as a no-op). Use `--table`/`--pretty` for the summary + table view.

| Flag                  | Description                            |
| --------------------- | -------------------------------------- |
| `<workflowId>`        | Optional workflow ID                   |
| `--workflow-id <id>`  | Override the active workflow           |
| `--start-date <date>` | Start date in `YYYY-MM-DD` format      |
| `--end-date <date>`   | End date in `YYYY-MM-DD` format        |
| `--table`             | Human-readable summary + table         |
| `--api-key <key>`     | Override API key                       |
| `--profile <name>`    | Use a specific CLI profile             |
| `--debug`             | Show HTTP request/response diagnostics |

**Example:**

```bash
# Get workflow analytics for a date range as JSON (default)
frontline workflows analytics 42 --start-date 2025-01-01 --end-date 2025-01-31

# Get workflow analytics as a human-readable table
frontline workflows analytics 42 --table
```

**Output:** Summary section, Runs by Date table (date, totalRuns, successfulRuns, failedRuns, totalCredits).

### Read run logs

Every workflow run records an execution log. List them to audit results or debug
failures; get one log to see the per-node results.

```bash
frontline workflows logs [workflowId] [--workflow-id <id>] [--status <s>] [--start-date <YYYY-MM-DD>] [--end-date <YYYY-MM-DD>] [--page <n>] [--page-size <n>] [--table]
frontline workflows logs get <logId> [--workflow-id <id>] [--pretty]
frontline workflows logs trace <logId> <nodeResultId> [--workflow-id <id>] [--pretty]
```

Output is **JSON by default** (`--json` is accepted as a no-op).

| Flag                   | Description                                     |
| ---------------------- | ----------------------------------------------- |
| `--workflow-id <id>`   | Override the active workflow                    |
| `--status <s>`         | Filter by run status (e.g. `SUCCESS`, `FAILED`) |
| `--start-date <date>`  | Start date in `YYYY-MM-DD` format               |
| `--end-date <date>`    | End date in `YYYY-MM-DD` format                 |
| `--table` / `--pretty` | Human-readable output                           |

**Examples:**

```bash
# List recent runs as a table
frontline workflows logs --workflow-id 2 --table

# Only failed runs since a date
frontline workflows logs --workflow-id 2 --status FAILED --start-date 2025-01-01

# Inspect one run with its per-node results
frontline workflows logs get 9001 --workflow-id 2 --pretty

# Drill into one node's full execution trace within that run
frontline workflows logs trace 9001 7001 --workflow-id 2 --pretty
```

**Output:** list = runs (`id`, `successful`, `started_at`, `completed_at`, `duration`,
`ai_credits`, `error`); detail adds a `node_results` table (`id`, `node_id`, `alias`, `type`,
`success`, `ai_credits`, `error`, `audit_log_id`).

**Tracing:** a run is many node results; the UI shows the audit log per node. Each
`node_results` row has its own `id` and an `audit_log_id` when it has a trace.
`logs trace <logId> <nodeResultId>` returns that one node's full execution trace — fetched
per node, never the whole run at once.

## Troubleshooting

- **"No API key found"**: run `frontline auth login` to authenticate.
- Use `--debug` to see the full HTTP request URL, headers, and response status for diagnosing issues.
- Output is JSON by default (pipe to `jq` or other tools); use `--pretty`/`--table` for human-readable output instead. `--json` is also accepted as a no-op.
- Use `--profile <name>` if you have multiple Frontline accounts configured.

---

## See also

- Full reference: <https://docs.getfrontline.ai/docs> (concepts) and <https://docs.getfrontline.ai/cli> (command reference).
- App UI walkthroughs (channels, billing, settings): <https://help.getfrontline.ai>.
