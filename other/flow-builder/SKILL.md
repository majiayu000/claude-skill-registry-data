---
name: flow-builder
description: Build valid Frontline assistant flows from CLI commands. Use when creating flow graphs, choosing conversation node payloads, connecting nodes, or validating flow structure before execution.
allowed-tools: Bash(frontline:*)
---

# Flow Builder

## Default Workflow

1. Select the agent:

```bash
frontline agents use <agentId>
```

2. Create or select a flow:

```bash
frontline agents flows create --name "Flow name"
frontline agents flows use <flowId>
```

3. Inspect before each change:

```bash
frontline agents flows graph --table
```

## Valid Flow Rules

- Supported nodes: `START`, `TRIGGER_INTENT`, `SAY_AI`, `RESPONSE_AI`, `TOOLS_AI`, `API`, `CONDITIONAL_ROUTING`, `CREATE_RECORD_ACTIVITY`.
- **Automation-only nodes (`TRIGGER`, `SCHEDULED_TRIGGER`, `WEBHOOK`, `AI_CAPTURE`, `DATA_TRANSFORMER`, `SEND_MESSAGE`, `SEND_WHATSAPP_MESSAGE`, `ITERATION`, `BREAK`, `AUTOMATION_STATUS`, `TRANSCRIPTION`, `FILE_ANALYSIS`, `DYNAMIC_TABLES`) are rejected by the backend with a 400 error if added to a flow.** To read/write records inside a flow, use a `TOOLS_AI` node with table tools (`DYNAMIC_TABLES` / "Data Action" is automation-only).
- `CREATE_RECORD_ACTIVITY` logs a manual activity on an Object record mid-conversation. Available in both flows and automations.
- Use exactly one initial node: `START` or `TRIGGER_INTENT`.
- A `START` node may only exist in the agent's **default Start flow** — the API rejects a `START` node in any other flow (`400`).
- `data.type` must match the node `type`.
- Edges cannot point from a node to itself.
- Edges cannot create cycles.
- `CONDITIONAL_ROUTING` and `TOOLS_AI`, and `API` can use multiple outgoing handles.
- `TOOLS_AI.conditions` is a **required** field (array) — pass `[]` if you don't need extra branches; omitting the key entirely returns `400`.
- Other nodes should use one outgoing edge.
- Deleting a node removes all incoming and outgoing edges.

## The Start flow & how flows are triggered

- **Default Start flow.** Every agent ships with a default flow named **"Start"** (`DRAFT`) holding a single `START` node. It runs **automatically at the start of every conversation** — build first-contact logic (greeting, capturing data, creating a record) by adding nodes after that `START`. Find it with `frontline agents flows list` (the one with `isDefault: true`).
- **Other flows are triggered, not automatic.** A non-default flow begins with a `TRIGGER_INTENT` node and is entered when it matches the user, configured either by:
    - **Intents** — `intentIds` on the `TRIGGER_INTENT` node (create them with `frontline agents intents create`); the flow fires when the user's message matches one.
    - **Agentic routing** — `agenticRouting`, a natural-language instruction describing when to enter the flow; the agent routes based on it and the user's intention.
- **Default-message rule.** If a flow finishes a turn without a user-facing message (e.g. it only captured variables or ran a tool action), the agent sends a **default AI-generated message** so the user always gets a reply.

## Variables And Intents

Use variables in text fields as `{VARIABLE_NAME}`. The name must match the agent
variable exactly.

```bash
frontline agents variables create --name customer_name --description "Customer name"
frontline agents intents create --name cancellation --phrases '["cancel order","stop subscription"]'
```

Flow fields with variable replacement include API `url`, `headers[].value`,
`parameters[].value`, `body`; Say AI `message` and `prompt`; Response AI
`instructions`; Tools AI `instructions`; Conditional Routing AI
`conditions[].expression`; and Create Record Activity `rowId` and `content`.

### Capturing values into variables

Reading a variable (`{name}`) and **capturing** one are different. To populate a variable, the field depends on the node type — and using the wrong field is **silently ignored** (no error):

- **AI nodes** (`TOOLS_AI`, `RESPONSE_AI`): `captureVariables` — references an **existing agent variable**. Create it first (`frontline agents variables create`), then reference it by `{ "name": "<var>" }` (or `{ "id": <id> }`); the API resolves it and stores the canonical `{ id, name, description }`. An unknown name returns `400` (`not_found`). The AI fills it based on the prompt/instructions.
- **API node**: `variables: [{ key, value, fullResponse }]` — `key` is the name of an **existing** variable (else `400`); `value` is a **property path** into the JSON response (e.g. `data.items[0].id`); set `fullResponse: true` to capture the whole body.
    - Path syntax is simple property access (not JSONPath): dot notation for nested objects and `[n]` for array indices. `[0]` is treated the same as `.0`, and a leading dot is optional.
    - Only works when the response is JSON. If a path step is missing/`null`, the variable is left unset (no error). Objects/arrays are stored as a JSON string.

> Do **not** put `captureVariables` on an API node (it's dropped silently) or `variables` on an AI node. Both nodes resolve the captured value by **name**, so the same `{name}` can be written by either.

> **Capturing contact info creates a Person automatically.** Capturing into the built-in contact variables `first_name`, `last_name`, `email`, or `phone_number` writes to (and **creates/identifies**) the conversation's **People** record — no record-create node needed. It deduplicates by email (a matching `email` links to the existing Person when the current contact has no email yet). **Do not create a custom variable named `email`** (or other default names): use `frontline agents variables check-name` — defaults are reserved. Use names like `email_api` for API-only values. If a Person already has an email, a newly captured different email is **not** applied to that record (other captured fields still merge).

## Node identity

Do **not** send `nodeId` or `alias` in `nodes create`. The server returns both in the **201** response. Use that `nodeId` for edges; set a custom alias with `nodes update` after create.

Persisted ids follow `node_<uuid>`. Names like `start_1` are invalid for stored nodes.

## Node Payloads

Start:

```bash
frontline agents flows nodes create --data '{"type":"START","position":{"positionX":0,"positionY":0}}'
```

Intent trigger:

```bash
frontline agents flows nodes create --data '{"type":"TRIGGER_INTENT","position":{"positionX":0,"positionY":0},"data":{"type":"TRIGGER_INTENT","intentIds":[123],"agenticRouting":null}}'
```

Say AI:

```bash
frontline agents flows nodes create --data '{"type":"SAY_AI","position":{"positionX":320,"positionY":0},"data":{"type":"SAY_AI","sayWithAi":false,"message":"Hello!"}}'
```

RESPONSE_AI (an assistant reply generated by a specific agent's model config — capture values into variables via `captureVariables`; see **Variables And Intents** below):

```bash
frontline agents flows nodes create --data '{"type":"RESPONSE_AI","position":{"positionX":320,"positionY":0},"data":{"type":"RESPONSE_AI","assistantId":"<agent-id>","model":"<external_id_from_ai_models_list>","aiVendor":"<vendor_from_same_row>","temperature":0.2,"instructions":"Answer the customer's question politely.","captureVariables":[],"exitNodeWhen":"ALL_VARIABLES"}}'
```

- `assistantId` — the agent id (same as `<agentId>` used elsewhere, e.g. `frontline agents use`), even though this node lives inside that agent's own flow.
- `model` / `aiVendor` — resolve them first with `frontline ai-models list --type TEXT --table`; hardcoded names like `gpt-4o-mini` may not exist in every account/environment. You can pass `aiModelId` instead of `model`+`aiVendor` if you prefer.
- `exitNodeWhen` (**required**) — one of `ALL_VARIABLES`, `FLOW_TRIGGERED`, `ANY_VARIABLES`; controls when the node considers its turn done relative to `captureVariables`.
- `captureVariables` (**required**, can be `[]`) — same shape as `TOOLS_AI` (see **Capturing values into variables** below).

API (**two fixed outgoing handles: `success` and `fail`** — the canvas never renders a `default` handle for this node type; connecting `default` is rejected):

```bash
frontline agents flows nodes create --data '{"type":"API","position":{"positionX":640,"positionY":0},"data":{"type":"API","url":"https://example.com","method":"GET","headers":[]}}'

# Connect both outgoing paths — never "default":
frontline agents flows edges add --source <api-node-id> --source-handle success --target <next-node-id> --target-handle default
frontline agents flows edges add --source <api-node-id> --source-handle fail --target <error-node-id> --target-handle default
```

Conditional routing (**AI evaluator** — write conditions in natural language; each `{var}` is injected as `"var": value` in the prompt; no dot-access like `{item.id}`; connect a **`no-match`** handle when none apply):

```bash
frontline agents flows nodes create --data '{"type":"CONDITIONAL_ROUTING","position":{"positionX":960,"positionY":0},"data":{"type":"CONDITIONAL_ROUTING","routingType":"CONDITIONAL_AI","conditions":[{"handleId":"yes","expression":"{confirmed} is true"},{"handleId":"no","expression":"{confirmed} is false"}]}}'
```

Create record activity (log a manual activity on an Object record mid-conversation):

```bash
frontline agents flows nodes create --data '{
  "type": "CREATE_RECORD_ACTIVITY",
  "position": { "positionX": 1280, "positionY": 0 },
  "data": {
    "type": "CREATE_RECORD_ACTIVITY",
    "recordTypeId": 5,
    "rowId": "{contact_row_id}",
    "activityType": "NOTE",
    "content": "El usuario preguntó: {user_question}"
  }
}'
```

- `recordTypeId` — get via `frontline object get <name>` → `data.record_types[0].id`. Must be an OBJECT (validated at save time).
- `activityType` — one of: `NOTE`, `EMAIL`, `PHONE_CALL`, `MEETING`, `WHATSAPP` (validated at save time).
- `rowId` and `content` support `{varName}` — variable must exist (create first with `frontline agents variables create`).

## Edges

Connect nodes:

```bash
frontline agents flows edges add --source node_11111111-1111-1111-1111-111111111111 --source-handle default --target node_22222222-2222-2222-2222-222222222222 --target-handle default
```

Connect routing handles:

```bash
frontline agents flows edges add --source node_44444444-4444-4444-4444-444444444444 --source-handle yes --target node_33333333-3333-3333-3333-333333333333 --target-handle default
frontline agents flows edges add --source node_44444444-4444-4444-4444-444444444444 --source-handle no  --target node_22222222-2222-2222-2222-222222222222 --target-handle default
```

Remove an edge:

```bash
frontline agents flows edges remove --source node_11111111-1111-1111-1111-111111111111 --source-handle default --target node_22222222-2222-2222-2222-222222222222 --target-handle default
```

## Updates

```bash
frontline agents flows nodes update node_22222222-2222-2222-2222-222222222222 --data '{"alias":"Greeting"}'
frontline agents flows nodes delete node_22222222-2222-2222-2222-222222222222
frontline agents flows update --name "Flow name" --status ACTIVE
```

---

## Reference validation (avoid 400s)

Every `customToolIds`, `intentIds`, `assistantId`, `aiModelId`, `knowledgeBaseIds`, `playbookIds`, `selectedRecordTypes[].recordTypeId`, `connectedAccountConfigs[].connectedAccountId` you put in a node's `data` is **validated against the database before the node is persisted**. A non-existent id returns `400 bad_request` with `details.issues[].code === "not_found"` and the node is dropped.

For `TOOLS_AI` table access, use `selectedRecordTypes` with `recordTypeId` and at least one permission set to `true`:

```json
"selectedRecordTypes": [
  { "recordTypeId": 5, "read": true, "create": true, "update": true, "delete": false }
]
```

Before composing a node, look up the referenced resources to make sure they exist:

- `frontline ai-models list` for `aiModelId`.
- `frontline custom-tools list` for `customToolIds`.
- `frontline agents intents list` (with `--agent-id <id>`) for `intentIds`.
- `frontline object schema <name>` to find a table id when configuring table tools on a `TOOLS_AI` node.

If you hand a non-existent id to the API, you'll see a clear `not_found` issue with the offending `path` — fix and retry, the API never half-creates the node.

---

## See also

- Full reference: <https://docs.getfrontline.ai/docs> (concepts) and <https://docs.getfrontline.ai/cli> (command reference).
- App UI walkthroughs (channels, billing, settings): <https://help.getfrontline.ai>.
