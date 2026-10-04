---
name: custom-tools
allowed-tools: Bash(frontline:*)
description: Create, list, inspect, update, delete, execute (test), and assign Frontline custom tools (API call tools created by the account) from the CLI. Use when the user asks about custom tools, API tools, headers, arguments, query params, testing/running a custom tool, or assigning custom tools to agents.
---

## What is a custom tool?

A **custom tool** is an HTTP/API-call tool that the **account creates** and assigns to agents, flows, and workflows. These are user-created tools — distinct from Frontline's built-in **system tools** and from **connected-integration (MCP) tools** that come from a connected account. This skill (and the `frontline custom-tools` command) only manages custom tools.

The CLI command is `frontline custom-tools`. The older alias `frontline tools` still works for back-compat, but prefer `custom-tools`.

## Prerequisites

- Authenticate with `frontline auth login <api-key>`.
- Creating, updating, deleting, and executing custom tools requires a USER API key.
- This public surface supports `API_CALL` custom tools only. WhatsApp template tools are not exposed yet.

## List And Inspect

```bash
frontline custom-tools list
frontline custom-tools list --status ACTIVE --filter-text contact
frontline custom-tools list --table
frontline custom-tools describe <toolId>
```

List output includes `id`, `name`, `status`, `method`, `url`, and timestamps.

## Create A Custom Tool

```bash
# GET with a path argument
frontline custom-tools create \
  --name "Fetch contact" \
  --description "Fetches a CRM contact" \
  --method GET \
  --url "https://api.example.com/contacts/{contactId}" \
  --arguments '[{"name":"contactId","description":"CRM contact ID","dataType":"STRING"}]' \
  --headers '[{"key":"Authorization","value":"Bearer {apiKey}"}]' \
  --query-params '[{"key":"include","value":"deals"}]'

# POST with a JSON body
frontline custom-tools create \
  --name "Create lead" \
  --description "Creates a lead in the CRM" \
  --method POST \
  --url "https://api.example.com/leads" \
  --arguments '[{"name":"nombre_cliente","description":"Client name","dataType":"STRING"},{"name":"tipo_cliente","description":"Client type","dataType":"STRING"}]' \
  --headers '[{"key":"Content-Type","value":"application/json"}]' \
  --body '{"nombre_cliente":"{nombre_cliente}","tipo_cliente":"{tipo_cliente}"}'
```

Options:

- `--arguments`: `[{ "name": "...", "description": "...", "dataType": "STRING", "required": true, "defaultValue": "..." }]` — the inputs the AI fills in before the tool runs.
- `--headers`: `[{ "key": "...", "value": "..." }]`
- `--query-params`: `[{ "key": "...", "value": "..." }]`
- `--body`: a raw request body **string** (typically a JSON string). Use it for `POST`/`PUT`/`PATCH` tools. Interpolate argument values into it (see below).

Argument `dataType` must be one of `STRING`, `NUMBER`, or `BOOLEAN`. Use `NUMBER` for any numeric value, including decimals.

Argument `required` and `defaultValue` (both optional):

- `required` defaults to `true`. A required argument with no value **and** no `defaultValue` is rejected before the request runs, so the agent retries with the missing value.
- `defaultValue` is always a **string**, even for `NUMBER`/`BOOLEAN` (`"42"`, `"true"`). It is coerced to `dataType` and used when the caller omits the argument. A `defaultValue` that doesn't parse for its `dataType` is rejected at create time.

> **Do not use `DECIMAL`.** The API technically accepts it, but the app UI's **Format** dropdown only knows `STRING` / `NUMBER` / `BOOLEAN` — a `DECIMAL` argument shows up with a **blank** Format in the UI. Always pick `NUMBER` for decimals.

Supported methods are `GET`, `POST`, `PUT`, `PATCH`, and `DELETE`.

## Variable Interpolation (single braces `{name}`)

Every `arguments[].name` you declare can be referenced inside the `url`, `headers` values, `query-params` values, and the `body` using **single curly braces**: `{argumentName}`. At call time the AI fills each argument and the value is substituted in.

```text
argument name:  contactId   →   reference as  {contactId}
```

> **Use single braces, not double.** The interpolation engine matches `{name}` exactly. `{{contactId}}` is **wrong** — it does not interpolate and leaves a broken `{value}` in the request. This applies everywhere, including the `--body`.

## Update And Delete

```bash
frontline custom-tools update <toolId> --status PAUSED
frontline custom-tools update <toolId> --url "https://api.example.com/v2/contacts/{contactId}"
frontline custom-tools update <toolId> --headers '[{"key":"Authorization","value":"Bearer {apiKey}"}]'
frontline custom-tools update <toolId> --body '{"nombre_cliente":"{nombre_cliente}","tipo_cliente":"{tipo_cliente}"}'
frontline custom-tools delete <toolId>
```

Update replaces `arguments`, `headers`, `queryParams`, or `body` when those options
are provided. Delete is a soft delete.

## Test A Custom Tool

Run a saved custom tool against its live endpoint and inspect the raw HTTP response — useful
to verify a tool works before assigning it to an agent.

```bash
# No arguments
frontline custom-tools test <toolId>

# With argument values (interpolated into the tool's {placeholders})
frontline custom-tools test <toolId> --values '{"contactId":"abc123"}'
```

- `--values` is a JSON **object** mapping `argumentName → value` (not the array form used by `create`). Each value is substituted into the stored `url`, `headers`, `query-params`, and `body` via the same single-brace `{name}` interpolation.
- Returns the downstream response: `status`, `duration` (ms), `contentLength`, `headers`, and the parsed `data`.
- Only `API_CALL` tools can be executed; a non-API tool returns a 400.

## Assign To An Agent

Use `customToolIds` in the agent setting payload. The CLI command
`agents agent-setting update` **merges** your `--data` patch with the current
settings before sending the PUT, so you can change only `instructions` or
`customToolIds` without dropping connected accounts.

```bash
frontline agents agent-setting update \
  --agent-id <agentId> \
  --data '{"instructions":"New prompt only"}'
```

To clear tools or integrations intentionally, pass empty arrays:

```bash
frontline agents agent-setting update \
  --agent-id <agentId> \
  --data '{"customToolIds":[],"connectedAccountConfigs":[]}'
```

When building payloads programmatically outside the CLI, merge manually:

```bash
# 1. Fetch current settings
frontline agents agent-setting get --agent-id <agentId>

# 2. Update with the full merged payload (instructions is REQUIRED)
frontline agents agent-setting update \
  --agent-id <agentId> \
  --data '{
    "customToolIds": [123],
    "aiModelId": <currentAiModelId>,
    "temperature": <currentTemperature>,
    "instructions": "<full current instructions text>"
  }'
```

When building the payload programmatically, use `jq` to keep multi-line
instructions safe:

```bash
INSTRUCTIONS="$(frontline agents agent-setting get --agent-id <agentId> | jq -r '.instructions')"
frontline agents agent-setting update \
  --agent-id <agentId> \
  --data "$(jq -n --argjson ids '[123]' --arg inst "$INSTRUCTIONS" \
    '{customToolIds: $ids, aiModelId: -1, temperature: 0.2, instructions: $inst}')"
```

The API validates that assigned custom tool IDs belong to the same account.

---

## See also

- Full reference: <https://docs.getfrontline.ai/docs> (concepts) and <https://docs.getfrontline.ai/cli> (command reference).
- App UI walkthroughs (channels, billing, settings): <https://help.getfrontline.ai>.
