---
name: frontline-agents
allowed-tools: Bash(frontline:*)
description: List, filter, inspect, run/test, and manage Frontline AI agents and their flows using the Frontline CLI. Use when the user asks about agents, running or testing an agent, flow CRUD, flow graph nodes/edges, status, conversations, or analytics.
---

## Prerequisites

- The `frontline` CLI must be installed (`npm i -g @getfrontline/cli`).
- The user must be authenticated (`frontline auth login`).

## Commands

## Agent Builder

Create an agent and store it as the active agent:

```bash
frontline agents create --name "Support Agent"
frontline agents describe
frontline agents update --name "Support Agent v2"
frontline agents deploy --offline false
```

Use `--no-use` on `create` if you do not want to change the active agent. Use
`--agent-id <id>` on scoped commands to override the active agent in scripts.

Delete uses the public API soft-delete flow:

```bash
frontline agents delete
frontline agents delete --agent-id <agentId>
```

Manage core agent settings with JSON payloads validated by the API:

```bash
frontline ai-models list --type TEXT --table
frontline agents agent-setting get
frontline agents agent-setting get --agent-id <agentId>
```

**`agent-setting update` merges with current settings in the CLI.** Send only the
fields you want to change. To clear tools or integrations, pass empty arrays
explicitly.

```bash
frontline agents agent-setting update \
  --agent-id <agentId> \
  --data '{"instructions":"New prompt only"}'

# Assign custom tools without dropping connected accounts
frontline agents agent-setting update \
  --agent-id <agentId> \
  --data '{"customToolIds":[123,456]}'
```

Create custom tools first with `frontline custom-tools create`; then assign them by
ID through `customToolIds`.
Use TEXT AI model IDs from `frontline ai-models list --type TEXT` as
`aiModelId`. The CLI validates referenced IDs in the same
`agents agent-setting update` command when the Public API exposes the referenced
resource, including `aiModelId`, `customToolIds`, and `selectedRecordTypes[].recordTypeId`
(from `frontline object record-type list <object>`, or the `record_types` array on a
`frontline table get <table>` response — tables have no record-type command because they only
ever carry one). The backend is still the source of truth for every existence and ownership
check.

Resolve `connectedAccountId` values with `frontline integrations list --table`
(USER API key). Communication channels use `frontline channels list`.

Manage theme fields. Image upload is not part of this public CLI surface; pass
existing image URLs or `null`.

```bash
frontline agents theme get
frontline agents theme update --data '{"title":"Support","initialMessage":"Hi! How can I help?","placeholder":"Type your message...","avatar":null,"bubbleImage":null,"bubbleColor":"#111827","userMessageColor":"#2563eb","agentMessageColor":"#f3f4f6","bubbleAlignment":"RIGHT","progressIndicator":"DYNAMIC","verticalPositionInPixels":24}'
```

Manage channel settings:

```bash
frontline agents settings get
frontline agents settings get livechat
frontline agents settings update whatsapp --data '{"splitMessages":true,"splitCharacterLimit":500,"conversationClose":"NEVER","closeAfter":null,"timeUnit":null,"sendCloseMessage":false,"closeMessageType":"STATIC","closeMessage":null,"closeInstruction":null}'
frontline agents settings list-channels --table
```

Mutating commands require a USER API key.

## Variables And Intents

Agent-scoped variables and intents use the active agent by default. Override with
`--agent-id <id>` in scripts.

```bash
frontline agents variables list --table
frontline agents variables all
frontline agents variables create --name customer_name --description "Customer name"
frontline agents variables describe 123
frontline agents variables update 123 --name customer_name --pattern "^[A-Za-z ]+$"
frontline agents variables delete 123
frontline agents variables check-name customer_name

frontline agents intents list --table
frontline agents intents all
frontline agents intents create --name cancellation --phrases '["cancel order","stop subscription"]'
frontline agents intents describe 10
frontline agents intents update 10 --name cancellation --phrases '[{"id":1,"phrase":"cancel order"},{"phrase":"stop order"}]'
frontline agents intents delete 10
frontline agents intents generate-phrases --name cancellation --samples '["cancel order"]' --amount 5
```

Use variables inside flow text fields as `{VARIABLE_NAME}`. The name must match
the saved variable name exactly. Flow fields with variable replacement include
API `url`, `headers[].value`, `parameters[].value`, `body`; Say AI `message` and
`prompt`; Response AI `instructions`; Tools AI `instructions`; and Conditional
Routing AI `conditions[].expression`.

> **Capturing contact info creates a Person automatically.** When a flow captures
> into the built-in contact variables `first_name`, `last_name`, `email`, or
> `phone_number`, the value is written to — and **creates/identifies** — the
> conversation's **People** record (deduplicated by email when the contact has no
> email yet). Use the platform `email` variable, not a custom duplicate name
> (`check-name` rejects names that match defaults). API-only values belong in
> variables such as `email_api`. If the Person already has an email, a different
> captured email is not overwritten on that record.

### List all agents

```bash
frontline agents list [--status <status>] [--table] [--debug]
```

Output is **JSON by default** (`--json` is accepted as a no-op). Use `--table`/`--pretty` for human-readable output.

| Flag                | Description                                        |
| ------------------- | -------------------------------------------------- |
| `--status <status>` | Filter by status: `active`, `inactive`, or `draft` |
| `--table`           | Render as a human-readable table instead of JSON   |
| `--api-key <key>`   | Override the stored API key for this request       |
| `--profile <name>`  | Use a specific CLI profile                         |
| `--debug`           | Show HTTP request/response diagnostics             |

**Example:**

```bash
# List all active agents as a table
frontline agents list --status active --table

# Get agent list as JSON for programmatic use (default)
frontline agents list
```

**Output columns:** `id`, `name`, `status`, `createdAt`, `updatedAt`

### Get flows for a specific agent

```bash
# Shorthand: list flows for an agent (positional agent id only)
frontline agents flows <agent-id>

# Explicit subcommand (use for --agent-id, --status, or scripting)
frontline agents flows list --agent-id <agent-id> [--status <status>]
frontline agents flows create --agent-id <agent-id> --name "Order Routing"
```

> **Commander note:** For `agents flows` subcommands (`list`, `create`, …), pass
> `--agent-id` on the **subcommand**, not only on the parent `flows` command.
> The parent accepts a positional `[agentId]` for the list shorthand only.

| Flag                   | Description                                                      |
| ---------------------- | ---------------------------------------------------------------- |
| `<agentId>`            | Optional agent ID                                                |
| `--agent-id <id>`      | Override the active agent                                        |
| `--status <status>`    | Filter by flow status: `ACTIVE`, `SUSPENDED`, `DELETED`, `DRAFT` |
| `--table` / `--pretty` | Human-readable table (JSON is the default output)                |
| `--api-key <key>`      | Override API key                                                 |
| `--profile <name>`     | Use a specific CLI profile                                       |
| `--debug`              | Show HTTP request/response diagnostics                           |

**Example:**

```bash
# List all flows for agent abc-123 (positional shorthand)
frontline agents flows abc-123

# Filter active flows only, as a table (positional shorthand)
frontline agents flows abc-123 --status ACTIVE --table

# Filter by status (use the list subcommand)
frontline agents flows list --agent-id abc-123 --status DRAFT
```

**Output columns:** `id`, `name`, `status`, `runCount`, `createdAt`

## Flow CRUD And Context

Select an agent once:

```bash
frontline agents use <agentId>
```

Then manage its flows:

```bash
frontline agents flows list
frontline agents flows create --name "Order Routing" --description "Routes order questions"
frontline agents flows use <flowId>
frontline agents flows describe --include-nodes
frontline agents flows update --name "Order Routing v2" --status ACTIVE
frontline agents flows delete
```

`create` selects the new flow by default. Use `--agent-id` and `--flow-id` to
override saved context in scripts.

## Flow Graphs

Inspect before changing:

```bash
frontline agents flows graph --table
frontline agents flows nodes list
```

Create a minimal flow (do **not** send `nodeId` or `alias` on create — the server always assigns and returns both in the JSON response, even if you pass them):

```bash
frontline agents flows nodes create --data '{"type":"START","position":{"positionX":0,"positionY":0}}'
frontline agents flows nodes create --data '{"type":"SAY_AI","position":{"positionX":320,"positionY":0},"data":{"type":"SAY_AI","sayWithAi":false,"message":"Hello!"}}'
frontline agents flows edges add --source <start-node-id> --source-handle default --target <say-node-id> --target-handle default
```

Update and delete:

```bash
frontline agents flows nodes update <node-id> --data '{"alias":"Greeting"}'
frontline agents flows nodes delete <node-id>
frontline agents flows edges remove --source <start-node-id> --source-handle default --target <say-node-id> --target-handle default
```

Supported flow node types:

`START`, `TRIGGER_INTENT`, `SAY_AI`, `RESPONSE_AI`, `TOOLS_AI`, `API`,
`CONDITIONAL_ROUTING`, `CREATE_RECORD_ACTIVITY`.

> `DYNAMIC_TABLES` ("Data Action") is **automation-only** and is rejected with
> a `400` if added to a flow. To read/write records inside a flow, use a
> `TOOLS_AI` node with table tools instead. See the `flow-builder` skill for
> full node payloads and required fields (e.g. `RESPONSE_AI`).

Validation rules:

- Use exactly one initial node: `START` or `TRIGGER_INTENT`.
- `data.type` must match `type` when `data` is present.
- Edges must reference existing source and target nodes.
- No self-edges and no cycles.
- `CONDITIONAL_ROUTING` and `TOOLS_AI`, and `API` can use multiple outgoing handles; other nodes use one outgoing edge.
- `TOOLS_AI.conditions` is a **required** field — pass `[]` if you don't need extra branches; omitting the key returns `400`.

### Get analytics for a specific agent

```bash
frontline agents analytics <agentId> [--start-date <YYYY-MM-DD>] [--end-date <YYYY-MM-DD>] [--table] [--debug]
```

Output is **JSON by default** (`--json` is accepted as a no-op).

| Flag                  | Description                            |
| --------------------- | -------------------------------------- |
| `<agentId>`           | **(required)** The agent ID            |
| `--start-date <date>` | Start date in `YYYY-MM-DD` format      |
| `--end-date <date>`   | End date in `YYYY-MM-DD` format        |
| `--table`             | Human-readable summary + table         |
| `--api-key <key>`     | Override API key                       |
| `--profile <name>`    | Use a specific CLI profile             |
| `--debug`             | Show HTTP request/response diagnostics |

**Example:**

```bash
# Get analytics for agent abc-123 for a date range (JSON, default)
frontline agents analytics abc-123 --start-date 2025-01-01 --end-date 2025-01-31

# Get analytics as a human-readable table
frontline agents analytics abc-123 --table
```

**Output:** Summary (totalCredits, totalConversations), Credits by Date table, Conversations by Channel table.

### Run / test an agent

Send a message to an agent and get its reply — the same way the in-app
Overview/Playground tests an agent and its flow. Runs over the `OVERVIEW` channel
against the agent's **active OR draft** flow, so it's the way to test end-to-end.

```bash
frontline agents run [--agent-id <id>] [--message <text>] [--conversation-id <id>] [--contact-id <id>]
frontline agents run close <conversationId> [--agent-id <id>]
```

`frontline agents chat` is an alias of `frontline agents run`.

| Flag                     | Description                                                   |
| ------------------------ | ------------------------------------------------------------- |
| `--agent-id <id>`        | Override the active agent                                     |
| `--message <text>`       | Message to send. Omit on a new conversation to just run Start |
| `--conversation-id <id>` | Continue an existing conversation (requires `--message`)      |
| `--contact-id <id>`      | Link the conversation to a People record                      |

**Examples:**

```bash
# Open a new conversation and run the Start flow (no message)
frontline agents run

# Open + send a first message
frontline agents run --message "Hi, I need help with my order"

# Continue an existing conversation
frontline agents run --message "yes please" --conversation-id 123

# Close the test conversation when done
frontline agents run close 123
```

**Output:** `{ conversation_id, messages: [{ id, role, type, text, created_at }] }`.
The `messages` array holds the agent's reply (and the opening Start-flow message on a
new conversation). Use the returned `conversation_id` to continue.

**Run vs. read:** `agents run` _drives_ the agent (test channel, mutates a conversation).
To inspect what already happened in production conversations, use
`agents conversations` (list/get/trace) below — that's read-only.

### Read conversations & transcripts

List the conversations an agent has handled, search them, and read each one's transcript.
Each conversation includes its latest rolling `summary` and the linked CRM `contact`.

```bash
frontline agents conversations [--agent-id <id>] [--is-closed <bool>] [--search <text>] [--channels <list>] [--feedback <rating>] [--start-date <YYYY-MM-DD>] [--end-date <YYYY-MM-DD>] [--page <n>] [--page-size <n>] [--table]
frontline agents conversations get <conversationId> [--agent-id <id>] [--include-events] [--pretty]
frontline agents conversations trace <conversationId> <messageId> [--agent-id <id>] [--pretty]
```

| Flag                   | Description                                                     |
| ---------------------- | --------------------------------------------------------------- |
| `--agent-id <id>`      | Override the active agent                                       |
| `--is-closed <bool>`   | Filter by closed state (`true`/`false`)                         |
| `--search <text>`      | Full-text search over message content and conversation name     |
| `--channels <list>`    | Comma-separated channels (see valid values below)               |
| `--feedback <rating>`  | Filter to conversations with a rated message (see valid values) |
| `--start-date <date>`  | Start date in `YYYY-MM-DD` format                               |
| `--end-date <date>`    | End date in `YYYY-MM-DD` format                                 |
| `--include-events`     | (get) Debug view: add non-message events to the transcript      |
| `--table` / `--pretty` | Human-readable output (JSON is the default)                     |

**Valid `--channels` values** (comma-separated): `LIVE_CHAT`, `SHARED`, `OVERVIEW`,
`API`, `WHATSAPP`, `INSTAGRAM`, `MESSENGER`, `SLACK`, `MAX_EXTENSION`.

**Valid `--feedback` values:** `POSITIVE`, `NEGATIVE`.

**Examples:**

```bash
# List conversations for the active agent
frontline agents conversations --table

# Search conversations mentioning "refund" on WhatsApp
frontline agents conversations --search "refund" --channels WHATSAPP --table

# Only conversations with negative feedback
frontline agents conversations --feedback NEGATIVE --table

# Read a clean transcript (user-facing messages only)
frontline agents conversations get 42 --pretty

# Debug view: transcript + events (flow enter/exit, intents, tool calls, errors)
frontline agents conversations get 42 --include-events --pretty

# Drill into one message's full LLM/tool execution trace
frontline agents conversations trace 42 1001 --pretty
```

**Output:** list = conversations (`id`, `name`, `channel`, `is_closed`, `contact_id`,
`summary`, `created_at`) plus the full `contact` record (People) in JSON output; detail adds
a `Transcript` table (`id`, `role`, `type`, `text`, `created_at`, `audit_log_id`) and a
`Contact` block.

**Clean vs. debug transcript:** by default `get` returns a clean transcript — only the
user-facing message types `MESSAGE`, `WHATSAPP_TEMPLATE_MESSAGE`, `PROCESSED_MEDIA_WITH_AI`.
Pass `--include-events` for a debug view that also includes every intermediate event row.
Each row's `type` tells you what it is. Full list of event `type` values added in debug mode:
`TRIGGER_INTENT`, `RESPONSE_AI`, `SAY_AI`, `API`, `ENTER_FLOW`, `EXIT_FLOW`, `ERROR_MESSAGE`,
`SET_VARIABLES`, `OFF_TOPIC`, `CONVERSATION_ENDED`, `CONVERSATION_IDLE`, `CONDITIONAL_ROUTING`,
`AGENT_TOOL`, `START_CONVERSATION`, `WHATSAPP_FLOW_COMPLETED`, `MESSAGE_REACTION`,
`CHANNEL_CONTEXT`, `ABORTED_MESSAGE`.

**Tracing:** each transcript/event row carries an `audit_log_id` when it has a trace.
`conversations trace <conversationId> <messageId>` returns that row's full audit log
(model, prompt, reasoning, tool calls, captured variables). Trace is fetched per message,
not for the whole conversation — use `--include-events` to discover the event rows worth tracing.

### Test chat (Playground)

To **run** an agent's flow interactively (not just read transcripts), use the
`agents-chat` skill or:

```bash
frontline agents chat --message "Hello"
frontline agents chat --message "Continue" --conversation-id <id>
frontline agents chat close <id>
```

See the `agents-chat` skill for full details and flags.

## Troubleshooting

- **"No API key found"**: run `frontline auth login` to authenticate.
- Use `--debug` to see the full HTTP request URL, headers, and response status for diagnosing issues.
- JSON is the default output — pipe it to `jq` or other tools. Add `--table`/`--pretty` for human-readable views (there is no `--json` flag).
- Use `--profile <name>` if you have multiple Frontline accounts configured.

---

## See also

- `agents-chat` skill — test an agent end-to-end from the terminal (Playground)
- Full reference: <https://docs.getfrontline.ai/docs> (concepts) and <https://docs.getfrontline.ai/cli> (command reference).
- App UI walkthroughs (channels, billing, settings): <https://help.getfrontline.ai>.
