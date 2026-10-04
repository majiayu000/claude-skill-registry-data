---
name: variables
description: Manage Frontline agent variables, workflow variables, and flow intents from the CLI, and explain variable interpolation in nodes and actions.
allowed-tools: Bash(frontline:*)
---

# Variables And Intents

## Agent Variables

```bash
frontline agents use <agentId>
frontline agents variables list --table
frontline agents variables all
frontline agents variables create --name customer_name --description "Customer name"
frontline agents variables describe 123
frontline agents variables update 123 --name customer_name --pattern "^[A-Za-z ]+$"
frontline agents variables delete 123
frontline agents variables check-name customer_name
```

Use `--agent-id <id>` to avoid relying on saved context.

## Agent Intents

```bash
frontline agents intents list --table
frontline agents intents all
frontline agents intents create --name cancellation --phrases '["cancel order","stop subscription"]'
frontline agents intents update 10 --name cancellation --phrases '[{"id":1,"phrase":"cancel order"},{"phrase":"stop order"}]'
frontline agents intents delete 10
frontline agents intents generate-phrases --name cancellation --samples '["cancel order"]' --amount 5
```

For create, `--phrases` is a JSON array of strings. For update, `--phrases` is a
JSON array of objects; existing phrases include `id`, and new phrases omit it.

## Workflow Variables

```bash
frontline workflows use <workflowId>
frontline workflows variables list --table
frontline workflows variables all
frontline workflows variables create --name order_id --description "Order ID"
frontline workflows variables describe 123
frontline workflows variables update 123 --name order_id --pattern "^[0-9]+$"
frontline workflows variables delete 123
frontline workflows variables check-name order_id
```

Use `--workflow-id <id>` to avoid relying on saved context.

## Name availability (custom variables)

Custom variable names must be unique **case-insensitively** within the agent or workflow, and must not collide with **platform default variables** stored in the database (`isDefault: true`, global rows with `assistantId` / `automationId` null).

```bash
frontline agents variables check-name customer_name
frontline workflows variables check-name order_id
```

Returns `{ "exists": true }` when the name is taken by another custom variable on the same agent/workflow **or** matches a default variable (for example `email`, `first_name`, `webhook_payload`). Create and update reject the same collisions with `409`.

Use a distinct name (for example `email_api`) when capturing API data that must **not** update the built-in People `email` field.

## Interpolation Syntax

Variables are referenced inside text fields as `{VARIABLE_NAME}`. The name must
match `variable.name` exactly. Automation workflows also expose each node output
as a runtime variable named after the node ID. Because node IDs follow the
`node_<uuid>` format, a node with `nodeId`
`node_a1b2c3d4-e5f6-7890-abcd-ef1234567890` is referenced downstream as
`{node_a1b2c3d4-e5f6-7890-abcd-ef1234567890}`.

Agent flow fields with variable replacement:

- API: `url`, `headers[].value`, `parameters[].value`, `body`.
- Say AI: `message`, `prompt`.
- Response AI: `instructions`.
- Tools AI: `instructions`.
- Conditional Routing AI: `conditions[].expression`.
- Create Record Activity: `rowId`, `content`.

(Dynamic Tables is automation-only — it is not a flow node.)

Automation workflow fields with variable replacement:

- API: `url`, `headers[].value`, `parameters[].value`, `body`.
- Send Message / Say AI: `message`, `prompt`.
- Response AI: `instructions`.
- Tools AI: `instructions`, `prompt`.
- AI Capture: `prompt`, `instructions`.
- Data Transformer: `prompt`.
- Conditional Routing AI: `conditions[].expression`.
- Dynamic Tables: `rowId`, `search`, `rowData` values.
- Transcription: `audioUrl`.
- WhatsApp Template: `templateVariables.header`, `templateVariables.body`, `templateVariables.buttons`.

---

## See also

- Full reference: <https://docs.getfrontline.ai/docs> (concepts) and <https://docs.getfrontline.ai/cli> (command reference).
- App UI walkthroughs (channels, billing, settings): <https://help.getfrontline.ai>.
