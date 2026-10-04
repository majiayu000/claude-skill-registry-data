---
name: opcode
description: >
  Agent-first workflow orchestration engine exposed via MCP (SSE daemon).
  Define, execute, monitor, and signal workflows with 6 MCP tools.
  Supports DAG-based execution, 6 step types (action, condition, loop,
  parallel, wait, reasoning), 24+ built-in actions, ${{}} interpolation,
  reasoning nodes for human-in-the-loop decisions, and secret vault.
  Use when defining workflows, running templates, checking status,
  sending signals, or querying workflow history.
license: MIT
metadata:
  version: "1.2.0"
  transport: sse
  openclaw:
    emoji: "⚙️"
    os: ["darwin", "linux"]
    user-invocable: true
    repository: "https://github.com/rendis/opcode"
    primaryEnv: "OPCODE_VAULT_KEY"
    requires:
      bins: ["go"]
      anyBins: ["gcc", "clang"]
      env: ["OPCODE_VAULT_KEY"]
    install:
      - type: go
        package: github.com/rendis/opcode/cmd/opcode
---

# OPCODE

Workflow orchestration engine for AI agents. Runs as a persistent SSE daemon — 1 server, N agents, 1 database. Workflows are JSON-defined DAGs executed level-by-level with automatic parallelism. Communication happens via 6 MCP tools over SSE (JSON-RPC). Includes a built-in web panel for multi-agent monitoring and management.

**Token economy**: define a template once, execute it unlimited times for free (no re-reasoning). Reasoning nodes store decisions as events and never replay them.

## Which Tool?

| I want to...                         | Tool           |
| ------------------------------------ | -------------- |
| Create/update a workflow template    | opcode.define  |
| Execute a workflow                   | opcode.run     |
| Check status or pending decisions    | opcode.status  |
| Resolve a decision / cancel / retry  | opcode.signal  |
| List workflows, events, or templates | opcode.query   |
| Visualize a workflow DAG             | opcode.diagram |

## Prerequisites

- **Go 1.25+** (required)
- **CGO enabled** (`CGO_ENABLED=1`) — required by embedded libSQL (go-libsql)
- **C compiler** — `gcc` or `clang` for CGO compilation

## Installation

```bash
go install github.com/rendis/opcode/cmd/opcode@latest
```

Installs the `opcode` binary to `$GOBIN` (default: `$GOPATH/bin`). Ensure it's in your `PATH`.

## Running

OPCODE runs as a **persistent SSE daemon**. 1 server, N agents, 1 database. Agents connect via HTTP.

### Configuration

Data directory: `~/.opcode/` (DB, settings, pidfile). Created automatically.

First-time setup (installs config and starts daemon):

```bash
opcode install --listen-addr :4100 --vault-key "my-passphrase"
```

`--vault-key` is memory-only (not persisted). For production, set `OPCODE_VAULT_KEY` env var.

Writes `~/.opcode/settings.json`, downloads [`mermaid-ascii`](https://github.com/AlexanderGrooff/mermaid-ascii) to `~/.opcode/bin/` for enhanced ASCII diagrams, and starts the daemon. All settings overridable via env vars (`OPCODE_LISTEN_ADDR`, `OPCODE_DB_PATH`, etc.).

| Setting       | Default                 | Env override         | Description                                 |
| ------------- | ----------------------- | -------------------- | ------------------------------------------- |
| `listen_addr` | `:4100`                 | `OPCODE_LISTEN_ADDR` | TCP listen address                          |
| `base_url`    | `http://localhost:4100` | `OPCODE_BASE_URL`    | Public base URL for SSE                     |
| `db_path`     | `~/.opcode/opcode.db`   | `OPCODE_DB_PATH`     | Path to embedded libSQL database            |
| `log_level`   | `info`                  | `OPCODE_LOG_LEVEL`   | `debug`, `info`, `warn`, `error`            |
| `pool_size`   | `10`                    | `OPCODE_POOL_SIZE`   | Worker pool size                            |
| `panel`       | `false`                 | `OPCODE_PANEL`       | Enable web panel (`true`/`1`)               |
| _(env only)_  | _(empty)_               | `OPCODE_VAULT_KEY`   | Passphrase for secret vault (never in JSON) |

> **Security**: Never put `OPCODE_VAULT_KEY` in `settings.json`. Use env vars or your platform's secrets manager. The passphrase derives the AES-256 encryption key via PBKDF2.

If the process stops, restart with:

```bash
OPCODE_VAULT_KEY="my-passphrase" opcode
```

`install` is only needed once. Subsequent restarts use `opcode` directly with the env var.

### Subcommands

| Command           | Description                                            |
| ----------------- | ------------------------------------------------------ |
| `opcode`          | Start SSE daemon (same as `opcode serve`)              |
| `opcode serve`    | Start SSE daemon explicitly                            |
| `opcode install`  | Write settings.json, SIGHUP running server or start    |
| `opcode update`   | Self-update (GitHub releases → `go install` fallback)  |
| `opcode version`  | Print embedded version (default `dev`)                 |

### Hot-Reload via SIGHUP

Running `opcode install` with a server already running sends SIGHUP to reload configuration without restarting. You can also send it manually: `kill -HUP $(cat ~/.opcode/opcode.pid)`.

| Setting      | Hot-Reload | Notes                  |
| ------------ | ---------- | ---------------------- |
| `panel`      | YES        | Mux swapped atomically |
| `log_level`  | YES        | LevelVar.Set()         |
| `listen_addr`| NO         | Needs listener rebind  |
| `base_url`   | NO         | SSEServer constructed  |
| `db_path`    | NO         | Store opened at startup|
| `pool_size`  | NO         | Pool sized at startup  |

### Building with Version

```bash
make build          # embeds git tag/commit as version
./opcode version    # prints e.g. "v1.0.0" or "abc1234-dirty"
```

Without `make`, `go build` works normally (version = `dev`).

### MCP Client Configuration

Connect to the running daemon via SSE URL:

```json
{
  "mcpServers": {
    "opcode": {
      "url": "http://localhost:4100/sse"
    }
  }
}
```

### Agent Identity

Each agent self-identifies via the `agent_id` parameter in tool calls. Opcode auto-registers unknown agents on first use. Choose a stable, unique ID per agent (e.g., `"content-writer"`, `"deploy-bot"`). Use `opcode.query` with `filter.agent_id` to see only your workflows.

### Startup Sequence

1. Writes pidfile to `~/.opcode/opcode.pid`
2. Loads config from `~/.opcode/settings.json` (env vars override)
3. Creates data directory, opens/creates libSQL database, runs migrations
4. Suspends orphaned `active` workflows (emits `workflow_interrupted`)
5. Initializes secret vault (if `OPCODE_VAULT_KEY` set)
6. Registers 24 built-in actions
7. Starts cron scheduler (recovers missed jobs)
8. Registers SIGHUP handler for config hot-reload
9. Begins listening for MCP JSON-RPC over SSE (+ web panel if `panel` enabled) on same port
10. Shuts down gracefully on SIGTERM/SIGINT (10s timeout), removes pidfile

### Recovery

Workflows survive process restarts. On startup, opcode transitions orphaned `active` workflows to `suspended` and recovers missed cron jobs.

Find interrupted workflows:

```plaintext
opcode.query({ "resource": "workflows", "filter": { "status": "suspended" } })
```

Inspect via `opcode.status`, then resume or cancel with `opcode.signal`.

### Security Model

Built-in actions respect `ResourceLimits` configured at startup:

| Control        | Description                                                                                                |
| -------------- | ---------------------------------------------------------------------------------------------------------- |
| **Filesystem** | `DenyPaths` / `ReadOnlyPaths` / `WritablePaths` restrict file access. Symlink resolution prevents escapes. |
| **Shell**      | Linux: cgroups v2 (memory, CPU, PID namespace). macOS: timeout-only fallback.                              |
| **HTTP**       | `MaxResponseBody` (10 MB) and `DefaultTimeout` (30 s).                                                     |

**Defaults are permissive** (no path deny-lists, no network restrictions). For production:

- Set `DenyPaths` for sensitive directories (`/etc/shadow`, `~/.ssh`)
- Set `WritablePaths` to constrain write scope
- Run the opcode process under a restricted OS user
- Use a network proxy/firewall for HTTP egress control
- Treat `OPCODE_VAULT_KEY` as root-equivalent for stored secrets

Crypto, assert, and workflow actions perform no I/O beyond the opcode database.

## MCP Tools

### opcode.define

Register a reusable workflow template. Version auto-increments (v1, v2, v3...).

| Param           | Type   | Required | Description                       |
| --------------- | ------ | -------- | --------------------------------- |
| `name`          | string | yes      | Template name                     |
| `definition`    | object | yes      | Workflow definition (see below)   |
| `agent_id`      | string | yes      | Defining agent ID                 |
| `description`   | string | no       | Template description              |
| `input_schema`  | object | no       | JSON Schema for input validation  |
| `output_schema` | object | no       | JSON Schema for output validation |
| `triggers`      | object | no       | Trigger configuration             |

**Returns**: `{ "name": "...", "version": "v1" }`

### opcode.run

Execute a workflow from a registered template.

| Param           | Type   | Required | Description               |
| --------------- | ------ | -------- | ------------------------- |
| `template_name` | string | yes      | Template to execute       |
| `agent_id`      | string | yes      | Initiating agent ID       |
| `version`       | string | no       | Version (default: latest) |
| `params`        | object | no       | Input parameters          |

**Returns**:

```json
{
  "workflow_id": "uuid",
  "status": "completed | suspended | failed",
  "output": { ... },
  "started_at": "RFC3339",
  "completed_at": "RFC3339",
  "steps": {
    "step-id": { "step_id": "...", "status": "completed", "output": {...}, "duration_ms": 42 }
  }
}
```

If `status` is `"suspended"`, call `opcode.status` to see `pending_decisions`.

### opcode.status

Get workflow execution status.

| Param         | Type   | Required | Description       |
| ------------- | ------ | -------- | ----------------- |
| `workflow_id` | string | yes      | Workflow to query |

**Returns**:

```json
{
  "workflow_id": "uuid",
  "status": "suspended",
  "steps": { "step-id": { "status": "...", "output": {...} } },
  "pending_decisions": [
    {
      "id": "uuid",
      "step_id": "reason-step",
      "context": { "prompt": "...", "data": {...} },
      "options": [ { "id": "approve", "description": "Proceed" } ],
      "timeout_at": "RFC3339",
      "fallback": "reject",
      "status": "pending"
    }
  ],
  "events": [ ... ]
}
```

Workflow statuses: `pending`, `active`, `suspended`, `completed`, `failed`, `cancelled`.

### opcode.signal

Send a signal to a suspended workflow.

| Param         | Type   | Required | Description                                       |
| ------------- | ------ | -------- | ------------------------------------------------- |
| `workflow_id` | string | yes      | Target workflow                                   |
| `signal_type` | enum   | yes      | `decision` / `data` / `cancel` / `retry` / `skip` |
| `payload`     | object | yes      | Signal payload (see below)                        |
| `step_id`     | string | no       | Target step                                       |
| `agent_id`    | string | no       | Signaling agent                                   |
| `reasoning`   | string | no       | Agent's reasoning                                 |

**Payload by signal type**:

| Signal     | step_id  | Payload                       | Behavior                        |
| ---------- | -------- | ----------------------------- | ------------------------------- |
| `decision` | required | `{ "choice": "<option_id>" }` | Resolves decision, auto-resumes |
| `data`     | optional | `{ "key": "value", ... }`     | Injects data into workflow      |
| `cancel`   | no       | `{}`                          | Cancels workflow                |
| `retry`    | required | `{}`                          | Retries failed step             |
| `skip`     | required | `{}`                          | Skips failed step               |

**Returns** (decision): `{ "ok": true, "resumed": true, "status": "completed", ... }`
**Returns** (other): `{ "ok": true, "workflow_id": "...", "signal_type": "..." }`

### opcode.query

Query workflows, events, or templates.

| Param      | Type   | Required | Description                          |
| ---------- | ------ | -------- | ------------------------------------ |
| `resource` | enum   | yes      | `workflows` / `events` / `templates` |
| `filter`   | object | no       | Filter criteria                      |

**Filter fields by resource**:

| Resource    | Fields                                                   |
| ----------- | -------------------------------------------------------- |
| `workflows` | `status`, `agent_id`, `since` (RFC3339), `limit`         |
| `events`    | `workflow_id`, `step_id`, `event_type`, `since`, `limit` |
| `templates` | `name`, `agent_id`, `limit`                              |

Note: event queries require either `event_type` or `workflow_id` in filter.

**Returns**: `{ "<resource>": [...] }` — results wrapped in object keyed by resource type.

### opcode.diagram

Generate a visual DAG diagram from a template or running workflow.

| Param            | Type   | Required | Description                                                |
| ---------------- | ------ | -------- | ---------------------------------------------------------- |
| `template_name`  | string | no\*     | Template to visualize (structure preview)                  |
| `version`        | string | no       | Template version (default: latest)                         |
| `workflow_id`    | string | no\*     | Workflow to visualize (with runtime status)                |
| `format`         | enum   | yes      | `ascii` / `mermaid` / `image`                              |
| `include_status` | bool   | no       | Show runtime status overlay (default: true if workflow_id) |

\* One of `template_name` or `workflow_id` required.

**Use cases**:

- `template_name` — preview DAG structure before execution
- `workflow_id` — visualize with live step status (completed, running, suspended, pending)
- `format: "ascii"` — CLI-friendly text output with box-drawing characters
- `format: "mermaid"` — markdown-embeddable flowchart syntax
- `format: "image"` — base64-encoded PNG for visual channels (Telegram, WhatsApp, Slack)

**Returns**: `{ "format": "ascii", "diagram": "..." }` — diagram content as text (ascii/mermaid) or base64 PNG (image).

## Web Panel

The daemon can serve a web management panel at the same port as MCP SSE (default `http://localhost:4100`). Enable with `--panel` flag or `OPCODE_PANEL=true` env var. Can be toggled at runtime via SIGHUP.

| Page            | Features                                                  |
| --------------- | --------------------------------------------------------- |
| Dashboard       | System counters, per-agent table, pending decisions, feed |
| Workflows       | Filter by status/agent, pagination, cancel, re-run        |
| Workflow Detail | Live DAG diagram, step states, events timeline            |
| Templates       | List, create via JSON paste (auto-versions), definition   |
| Template Detail | Version selector, Mermaid diagram preview                 |
| Decisions       | Pending queue, resolve/reject forms with context          |
| Scheduler       | Cron job CRUD, enable/disable, run history                |
| Events          | Event log filtered by workflow and/or type                |
| Agents          | Registered agents with type and last-seen                 |

Live updates via SSE — dashboard and workflow detail pages auto-refresh on new events.

## Workflow Definition

Durations use Go format: `500ms`, `30s`, `5m`, `1h30m`.

```json
{
  "steps": [ ... ],
  "inputs": { "key": "value or ${{secrets.KEY}}" },
  "context": { "intent": "...", "notes": "..." },
  "timeout": "5m",
  "on_timeout": "fail | suspend | cancel",
  "on_complete": { /* step definition */ },
  "on_error": { /* step definition */ },
  "metadata": {}
}
```

| Field         | Type             | Required | Description                                       |
| ------------- | ---------------- | -------- | ------------------------------------------------- |
| `steps`       | StepDefinition[] | yes      | Workflow steps                                    |
| `inputs`      | object           | no       | Input parameters (supports `${{}}`)               |
| `context`     | object           | no       | Workflow context, accessible via `${{context.*}}` |
| `timeout`     | string           | no       | Workflow deadline (e.g.,`"5m"`, `"1h"`)           |
| `on_timeout`  | string           | no       | `fail` (default), `suspend`, `cancel`             |
| `on_complete` | StepDefinition   | no       | Hook step after completion                        |
| `on_error`    | StepDefinition   | no       | Hook step on workflow failure                     |
| `metadata`    | object           | no       | Arbitrary metadata                                |

### Step Definition

```json
{
  "id": "step-id",
  "type": "action | condition | loop | parallel | wait | reasoning",
  "action": "http.get",
  "params": { ... },
  "depends_on": ["other-step"],
  "condition": "CEL guard expression",
  "timeout": "30s",
  "retry": { "max": 3, "backoff": "exponential", "delay": "1s", "max_delay": "30s" },
  "on_error": { "strategy": "ignore | fail_workflow | fallback_step | retry", "fallback_step": "id" },
  "config": { /* type-specific */ }
}
```

`type` defaults to `action`. The `config` field varies by type. See [workflow-schema.md](references/workflow-schema.md) for all config blocks.

## Step Types

### action (default)

Executes a registered action. Set `action` to the action name, `params` for input.

### condition

Evaluates a CEL expression and branches.

```json
{
  "id": "route",
  "type": "condition",
  "config": {
    "expression": "inputs.env",
    "branches": { "prod": [...], "staging": [...] },
    "default": [...]
  }
}
```

### loop

Iterates over a collection or condition. Loop variables: `${{loop.item}}`, `${{loop.index}}`.

```json
{
  "id": "process-items",
  "type": "loop",
  "config": {
    "mode": "for_each",
    "over": "[\"a\",\"b\",\"c\"]",
    "body": [
      {
        "id": "hash",
        "action": "crypto.hash",
        "params": { "data": "${{loop.item}}" }
      }
    ],
    "max_iter": 100
  }
}
```

Modes: `for_each` (iterate `over`), `while` (loop while `condition` true), `until` (loop until `condition` true).

### parallel

Executes branches concurrently.

```json
{
  "id": "fan-out",
  "type": "parallel",
  "config": {
    "mode": "all",
    "branches": [ [{ "id": "a", "action": "http.get", "params": {...} }], [{ "id": "b", "action": "http.get", "params": {...} }] ]
  }
}
```

Modes: `all` (wait for all branches), `race` (first branch wins).

### wait

Delays execution or waits for a named signal.

```json
{ "id": "pause", "type": "wait", "config": { "duration": "5s" } }
```

### reasoning

Suspends workflow for agent decision. Empty `options` = free-form (any choice accepted).

```json
{
  "id": "review",
  "type": "reasoning",
  "config": {
    "prompt_context": "Review data and decide",
    "options": [
      { "id": "approve", "description": "Proceed" },
      { "id": "reject", "description": "Stop" }
    ],
    "data_inject": { "analysis": "steps.analyze.output" },
    "timeout": "1h",
    "fallback": "reject",
    "target_agent": ""
  }
}
```

## Variable Interpolation

Syntax: `${{namespace.path}}`

| Namespace  | Example                             | Available fields                                                  |
| ---------- | ----------------------------------- | ----------------------------------------------------------------- |
| `steps`    | `${{steps.fetch.output.body}}`      | `<id>.output.*`, `<id>.status`                                    |
| `inputs`   | `${{inputs.api_key}}`               | Keys from `params` in `opcode.run`                                |
| `workflow` | `${{workflow.run_id}}`              | `run_id`, `name`, `template_name`, `template_version`, `agent_id` |
| `context`  | `${{context.intent}}`               | Keys from `context` in workflow definition                        |
| `secrets`  | `${{secrets.DB_PASS}}`              | Keys stored in vault                                              |
| `loop`     | `${{loop.item}}`, `${{loop.index}}` | `item` (current element), `index` (0-based)                       |

Two-pass resolution: non-secrets first, then secrets via AES-256-GCM vault.

**CEL gotcha**: `loop` is a reserved word in CEL. Use `iter.item` / `iter.index` in CEL expressions. The `${{loop.item}}` interpolation syntax is unaffected.

See [expressions.md](references/expressions.md) for CEL, GoJQ, Expr engine details.

## Built-in Actions

| Category       | Actions                                                                                                 |
| -------------- | ------------------------------------------------------------------------------------------------------- |
| **HTTP**       | `http.request`, `http.get`, `http.post`                                                                 |
| **Filesystem** | `fs.read`, `fs.write`, `fs.append`, `fs.delete`, `fs.list`, `fs.stat`, `fs.copy`, `fs.move`             |
| **Shell**      | `shell.exec`                                                                                            |
| **Crypto**     | `crypto.hash`, `crypto.hmac`, `crypto.uuid`                                                             |
| **Assert**     | `assert.equals`, `assert.contains`, `assert.matches`, `assert.schema`                                   |
| **Workflow**   | `workflow.run`, `workflow.emit`, `workflow.context`, `workflow.fail`, `workflow.log`, `workflow.notify` |

**Quick reference** (most-used actions):

- **`http.get`**: `url` (req), `headers`, `timeout`, `fail_on_error_status` -- output: `{ status_code, headers, body, duration_ms }`
- **`shell.exec`**: `command` (req), `args`, `stdin`, `timeout`, `env`, `workdir` -- output: `{ stdout, stderr, exit_code, killed }`
- **`fs.read`**: `path` (req), `encoding` -- output: `{ path, content, encoding, size }`
- **`workflow.notify`**: `message` (req), `data` -- output: `{ notified: true/false }` -- pushes real-time notification to agent via MCP SSE (best-effort)

See [actions.md](references/actions.md) for full parameter specs of all 25 actions.

## Scripting with shell.exec

`shell.exec` supports any language (Bash, Python, Node, Go, etc.). Scripts receive input via **stdin** and produce output via **stdout**. JSON stdout is **auto-parsed** — access fields directly with `${{steps.cmd.output.stdout.field}}`.

| Language | Command   | Args                  | Boilerplate                                                 |
| -------- | --------- | --------------------- | ----------------------------------------------------------- |
| Bash     | `bash`    | `["script.sh"]`       | `set -euo pipefail; input=$(cat -)`                         |
| Python   | `python3` | `["script.py"]`       | `json.load(sys.stdin)` -> `json.dump(result, sys.stdout)`   |
| Node     | `node`    | `["script.js"]`       | Read stdin stream ->`JSON.parse` -> `JSON.stringify`        |
| Go       | `go`      | `["run","script.go"]` | `json.NewDecoder(os.Stdin)` -> `json.NewEncoder(os.Stdout)` |

**Convention**: stdin=JSON, stdout=JSON, stderr=errors, non-zero exit=failure. Use `stdout_raw` for unprocessed text.

See [patterns.md](references/patterns.md#10-scripting-with-shellexec) for full templates.

## Reasoning Node Lifecycle

1. Workflow reaches a reasoning step
2. Executor creates PendingDecision, emits `decision_requested` event
3. Workflow status becomes `suspended`
4. Agent calls `opcode.status` to see pending decision with context and options
5. Agent resolves via `opcode.signal`:

   ```json
   {
     "workflow_id": "...",
     "signal_type": "decision",
     "step_id": "reason-step",
     "payload": { "choice": "approve" }
   }
   ```

6. Workflow auto-resumes after signal
7. If timeout expires: `fallback` option auto-selected, or step fails if no fallback

## Common Patterns

See [patterns.md](references/patterns.md) for full JSON examples: linear pipeline, conditional branching, for-each loop, parallel fan-out, human-in-the-loop, error recovery, sub-workflows, and MCP lifecycle.

## Error Handling

| Strategy        | Behavior                         |
| --------------- | -------------------------------- |
| `ignore`        | Step skipped, workflow continues |
| `fail_workflow` | Entire workflow fails            |
| `fallback_step` | Execute fallback step            |
| `retry`         | Defer to retry policy            |

Backoff: `none`, `linear`, `exponential`, `constant`. Non-retryable errors (validation, permission, assertion) are never retried.

See [error-handling.md](references/error-handling.md) for circuit breakers, timeout interactions, error codes.
