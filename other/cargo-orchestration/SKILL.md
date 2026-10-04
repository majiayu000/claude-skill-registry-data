---
name: cargo-orchestration
description: "Make Cargo actually run something, or show what it would run — execute one connector action, run a multi-step workflow, trigger a batch across a whole segment or model, message an AI agent, build or edit a node graph, draw a workflow, tool or play as a diagram, and query the runtime tables (runs, batches, spans, records) with SQL. Triggers: \"run this on all my contacts\", \"execute the action\", \"kick off a batch\", \"build a workflow\", \"schedule a play\", \"make it run every morning\", \"ask the agent\", \"show me the workflow\", \"what does this tool do\", \"visualize this play\", \"draw the graph\", \"explain this workflow\", \"how many runs failed today\", \"what is the output schema for this action\", \"add a step that\". Skip when: explaining why a run misbehaved — use cargo-diagnostics; downloading result files — use cargo-analytics; committing the workflow as code — use cargo-project."
version: "1.13.0"
compatibility: Requires @cargo-ai/cli (npm). Sign in or create an account with `cargo-ai login --email` (emailed code, no browser), `--oauth`, or an API token
homepage: https://github.com/getcargohq/cargo-skills
metadata:
  author: getcargo
  openclaw:
    requires:
      bins:
        - cargo-ai
    install:
      - kind: node
        package: "@cargo-ai/cli@latest"
        bins:
          - cargo-ai
    homepage: https://github.com/getcargohq/cargo-skills
---

# Cargo CLI — Orchestration

Runtime operations for the Cargo platform.

**What do you want to run?**

```
Need to run something?
├── Don't know the action yet    → action list <keywords>
├── One action, one record       → action execute
├── One action, many records     → action execute-batch
├── Multiple actions chained
│   ├── One-off / ad-hoc         → run create --nodes (one record)
│   │                              batch create --nodes (many records)
│   └── Reusable workflow        → build a tool, then run create --workflow-uuid
│                                  or batch create --workflow-uuid
├── Conversational AI agent      → message create
└── Testing ONE node of a
    workflow you're building     → node execute (debug only — see below)
```

> **Fanning out across many records (`action execute-batch`, `batch create`)? Sample first.** Run 10–20 records, report the observed cost and hit-rate, then ask the user to approve the full enrollment — quoting the **record count** and the **credit estimate**. See [Create a batch → the sample gate](#the-sample-gate).

> **Every node execution costs 0.01 credits — 1 credit per 100 — whatever the node is.**
> `branch`, `filter`, `switch`, `variables` and the rest carry no provider price, but
> they are not free: the charge is per *execution*, so a graph's cost has two terms,
> `(provider cost × records) + (nodes × records ÷ 100)`. On step-heavy, action-light
> graphs the second term dominates. It shows up in **no** per-node field — not
> `executions[].creditsUsedCount`, not `spans.execution_credits_used_count` — only in
> `billing usage get-metrics --unit orchestration.executions`. Quote both terms in the
> approval message ([`../cargo-gtm/references/cost-discipline.md`](../cargo-gtm/references/cost-discipline.md) §1).

> **Find the action before you hand-write the JSON.** `cargo-ai orchestration
> action list <keywords>` searches the integration catalog, Cargo native actions,
> workspace tools, and agents in one call — free, runs nothing — and each result
> carries a ready-to-paste `action` object (with `connectorUuid` already filled
> in), the action's **credit costs**, and its autocomplete slugs. Narrow with
> `--kind connector|native|tool|agent`, `--integration-slug <slug>`, `--limit`
> (default 20, max 50). `unknown command` means the CLI predates it — refresh.

> **`action execute`, not `node execute`, is the default for running something.**
> `node execute` is a **debug** surface for a node that already lives in a workflow:
> it requires `--workflow-uuid`, `--release-uuid`, `--node`, `--computed-config`
> **and** `--context` (all five, enforced client-side), and it bills like any live
> call. If you just want an operation's output — enrich a domain, call a connector
> action, invoke a tool or agent — use `action execute` / `action execute-batch`
> with a small `--action` + `--data` payload. Only reach for `node execute` when
> verifying one node's behavior before running the full graph.

> **Terminology:** An orchestration **tool** is a saved on-demand workflow (listed via `tool list`). An **action** is a single operation you execute without building a workflow — it can embed a saved orchestration tool (`kind: "tool"`), call a third-party connector (`kind: "connector"`), invoke an AI agent (`kind: "agent"`), or run a built-in platform operation (`kind: "native"`).

> **Composing a node graph? Build it from dedicated actions + expressions, in this order:**
> 1. **A dedicated action.** Search first with `action list <keywords>` (free): connector
>    actions, native actions (`agent`, `modelUpsert`, `branch`, `group`…), tools.
> 2. **An expression** for the glue. It's inline JavaScript in the field that needs the
>    value: reshaping, payloads, conditions, arrays.
> 3. **HTTP**, only if step 1 found no action for that API.
> 4. **A `script` node**, only if the logic can't fit in an expression.
>
> See **`references/node-selection.md`**.

> **Show the graph, don't describe it.** Before deploying a draft, and whenever
> the user asks what a workflow or play does, draw it:
> `cargo-ai orchestration node diagram --workflow-uuid <uuid> --format ascii --raw`
> (free, runs nothing; `--format` needs CLI ≥ 1.0.56, the command itself ≥ 1.0.54).
> Routing, fallback edges, and which steps bill are what the user is actually
> approving, and prose flattens all three. **Pick the format by where the output
> goes:** `ascii` renders a picture a person can read in a terminal or a chat
> reply; `mermaid` (the default) is source code, correct only when you are
> pasting into a PR, a doc, or a page that renders it. Sources, the ASCII legend,
> cost marking, and the duplicate-slug footgun: **`references/node-diagram.md`**.

**References:**

> `references/examples/actions.md` — action execute and execute-batch examples
> `references/examples/tools.md` — tool (on-demand workflow) examples
> `references/examples/plays.md` — play (segment-driven automation) examples
> `references/examples/agents.md` — AI agent chat examples
> `references/examples/templates.md` — pre-built workflow templates
> `references/examples/queries.md` — `orchestration query execute` (ClickHouse: runs/batches/spans/records) SQL examples. For `storage query` (workspace storage), see the `cargo-storage` skill.
> `references/examples/segments.md` — segment fetch and filter examples
> `references/nodes.md` — full node creation guide (kinds, native actions, expressions, validation, routing)
> `references/node-diagram.md` — **draw a node graph as a Mermaid flowchart** (`node diagram`): every source (workflow / draft / release / run / raw nodes), marking paid nodes, highlighting a failing node, and why diagrams key on `uuid` rather than `slug`
> `references/node-selection.md` — **build from dedicated actions + expressions** (action → expression → HTTP → `script`, in that order): expressions are inline JavaScript, where the logic goes (inline in one field, a shared `variables` node, or a `script`), native actions to prefer over code/HTTP, and expression traps (silent empty paths, ISO strings arriving as `Date`, testing with `expression eval`)
> `references/filter-syntax.md` — complete filter condition reference
> `references/polling.md` — async polling patterns, error handling, retry strategies
> `references/response-shapes.md` — full JSON response structures
> `references/troubleshooting.md` — common errors, plus a "Debugging a workflow run" section for runs that succeed but produce wrong output (wrong-branch routing, empty downstream values)

> **Diagnosing after the fact?** For the ordered forensic runbooks built on these surfaces — trace one run, sweep a batch for errors grouped by root cause, profile a play's credit spend — load the [`cargo-diagnostics`](../cargo-diagnostics/SKILL.md) skill.

## Bootstrap

Already signed in (`cargo-ai whoami` returns a workspace)? Skip to the next section.

```bash
npm install -g @cargo-ai/cli            # no global install? prefix every command with `npx @cargo-ai/cli`
cargo-ai login --email you@company.com  # emailed code, no browser; creates the account on first use
                                        # alternatives: --oauth (browser) · --token <api-token> (CI)
cargo-ai whoami                         # confirm the active workspace before any write
```

Every command prints JSON to stdout; failures exit non-zero with `{"errorMessage": "..."}`. Anything that creates a run or a batch is async — pass `--wait-until-finished` or poll the matching `get`. When the full skill bundle is installed, [`../cargo/references/prerequisites.md`](../cargo/references/prerequisites.md) adds the CLI version pin, token scopes, and the admin-only surface.

## Discover resources first

Most commands require UUIDs. Always discover them before acting.

```bash
cargo-ai orchestration action list <query>  # actions across connectors, native, tools, agents (+ credits)
cargo-ai orchestration play list            # all plays (name, workflowUuid, modelUuid, segmentUuid)
cargo-ai orchestration tool list            # all tools (name, workflowUuid, description)
cargo-ai orchestration workflow list        # all workflows (uuid only — no name)
cargo-ai orchestration template list       # all workflow templates (slug, name, kind)
cargo-ai ai agent list                     # all agents (uuid, name)
cargo-ai ai template list                  # all AI agent templates (slug, name, languageModelSlug)
cargo-ai storage model list                # all models (uuid, name, slug, columns)
cargo-ai storage dataset list              # all datasets
cargo-ai segmentation segment list         # all segments (uuid, name, modelUuid)
cargo-ai connection connector list         # all connectors
```

**Plays vs tools:** Both are backed by a workflow. A **play** is a segment-driven automation — it reacts to data changes in a segment (records added, updated, removed). A **tool** is an on-demand workflow — triggered manually, via API, or on a cron schedule. Workflows don't have a `name` field; use `play list` or `tool list` to find names and extract the `workflowUuid`.

**Retrieve in the UI:** plays live at `app.getcargo.io/workspaces/<WORKSPACE_UUID>/plays/<PLAY_UUID>` and tools at `app.getcargo.io/workspaces/<WORKSPACE_UUID>/tools/<TOOL_UUID>`. Get `<WORKSPACE_UUID>` from `cargo-ai whoami` under `workspace.uuid`.

**Designing a new tool or play?** Check templates first — they are pre-built node graphs for common automation patterns (enrichment pipelines, CRM syncs, lead scoring) and are an excellent starting point. List templates with `cargo-ai orchestration template list` and inspect a specific one with `cargo-ai orchestration template get <slug>`. Templates are tagged by `kind` so you can find ones suited for tools (`"kind":"tool"`) or plays (`"kind":"play"`) right away. See `references/examples/templates.md` for the full guide.

**Compatibility rules:**

- **`run create`** — only works with **tool** workflows (or no `workflowUuid`). Play workflows return `playNotCompatible`.
- **`batch create`** — allowed data kinds depend on the workflow type:
  - **Play** workflows: `filter`, `recordIds`, `segment`, `change`. Trigger a play with `filter`; `segment` takes a standalone segment only, never the `segmentUuid` from `play list`.
  - **Tool** workflows (or no `workflowUuid`): `file`, `records`

## Quick reference

```bash
# Find an action (free — no run, no credits)
cargo-ai orchestration action list enrich company
cargo-ai orchestration action list send --kind connector --integration-slug slack

# Single actions
cargo-ai orchestration action execute --action '{"kind":"tool","toolUuid":"<uuid>"}' --data '{"domain":"acme.com"}'
cargo-ai orchestration action execute-batch --action '{"kind":"connector","integrationSlug":"clearbit","actionSlug":"enrichCompany"}' --records '[{...},{...}]'
cargo-ai orchestration action get-output-schema --action '{"kind":"connector","integrationSlug":"clearbit","actionSlug":"enrichCompany"}' # → {"schema": <JSON Schema>} without executing

# Workflows (chain multiple actions)
cargo-ai orchestration run create --workflow-uuid <uuid> --data '{"company":"Acme","domain":"acme.com"}'
cargo-ai orchestration run create --data '{"domain":"acme.com"}' --nodes '[...]'
cargo-ai orchestration batch create --workflow-uuid <uuid> --data '{"kind":"filter","modelUuid":"...","filter":{"conjonction":"and","groups":[]}}'

# AI agents
cargo-ai ai message create --chat-uuid <uuid> --parts '[{"type":"text","text":"..."}]'

# Data
cargo-ai orchestration query execute "SELECT count() FROM runs WHERE status='error'" # ClickHouse: spans, runs, batches, records
cargo-ai segmentation segment fetch --model-uuid <uuid> --filter '{"conjonction":"and","groups":[]}' --fetching-limit 100
# For SQL against workspace storage (Companies, Contacts, …), see the cargo-storage skill: `storage query execute`
```

## Polling async operations

All operations are asynchronous. Either poll until terminal state, or pass `--wait-until-finished` to block.

`action execute` returns a run. `action execute-batch` returns a batch. They poll the same way:

| Result type     | Poll command         | Interval | Done when                                      |
| --------------- | -------------------- | -------- | ---------------------------------------------- |
| Run             | `run get <uuid>`     | 2s       | `status` is `success`, `error`, or `cancelled` |
| Batch           | `batch get <uuid>`   | 5s       | `status` is `success`, `error`, or `cancelled` |
| Agent message   | `message get <uuid>` | 2s       | `status` is `success` or `error`               |

For long-running batches (1000+ records), increase the interval to 10-15s after the first minute.

## Execute actions

Run a single action — no workflow or node graph needed.

### Find it first — `action list`

```bash
cargo-ai orchestration action list enrich company          # all kinds
cargo-ai orchestration action list --kind tool             # this workspace's tools
cargo-ai orchestration action list send --kind connector --integration-slug slack
```

Free, executes nothing. All query terms must match (AND); a hit on the action
slug or name ranks above the integration, which ranks above the description.
Returns `{query, totalMatches, results[]}` where each result carries `name`,
`description`, `score`, an `action` object to paste straight into `execute` /
`execute-batch` / `get-output-schema`, the workspace `connectors` for that
integration, `credits` (the cost table, when the action bills), and
`autocompletes` (config fields that need a picked id — a HubSpot object type, a
Slack channel). Defaults to 20 results, max 50.

```bash
# One action, one record → returns a run
cargo-ai orchestration action execute \
  --action '{"kind":"connector","integrationSlug":"clearbit","actionSlug":"enrichCompany"}' \
  --data '{"domain":"acme.com"}' \
  --wait-until-finished

# One action, many records → returns a batch
cargo-ai orchestration action execute-batch \
  --action '{"kind":"tool","toolUuid":"<tool-uuid>"}' \
  --records '[{"domain":"acme.com"},{"domain":"globex.com"}]' \
  --wait-until-finished
```

Action kinds: `tool`, `connector`, `agent`, `native`. See `references/examples/actions.md` for all action kinds, parameters, retry config, response shapes, and end-to-end examples.

> **A top-level action has no `config` — omit it.** Inputs belong in `--data` /
> `--records`; `execute` and `execute-batch` take the action with no `config` key
> at all, which is exactly what `action list` hands back, so its result pastes
> straight in. (`"config": {}` is still accepted there, harmlessly.)
>
> **`get-output-schema` takes the same pair.** The action object from
> `action list`, plus `--data` when the action's output depends on its inputs —
> a HubSpot object type or a target sheet decides which fields come back
> (`--data` needs **CLI ≥ 1.0.67**; the config-less `--action` works from 1.0.66).
> Workflow **nodes**, an alert's `--actions`, a play's `healthAlertActions`, and
> an agent's or MCP server's `--actions` are where `config` still lives; that is
> a node's configuration, not an action's input.
>
> **Inputs put in `config` are now dropped, not rejected.** The guard that used to
> answer `A top-level action does not use action.config…` is gone, so the action
> runs with *no input* — you get a provider-side missing-field error or an empty
> result that never mentions `config`. Check this first when a call comes back
> empty for no visible reason.

> **`execute-batch` bills per record.** Pass a 10–20 record slice of `--records` first, report the observed per-record cost and hit-rate, and get approval (with the full record count and credit estimate) before sending the rest — same gate as [Create a batch](#the-sample-gate).

### Resolve an action's output schema (without executing)

**Never guess what an action outputs.** Two free sources — no run, no credits:

1. **Connector actions:** the integration catalog carries the output schema inline — `integration get <slug>` (and `integration list`) return `actions.<actionSlug>.output.schema` next to the input `config.jsonSchema`. Not every action declares one.
2. **Any action kind** (`tool` / `connector` / `agent` / `native`) — resolve it with the same `--action` object as `action execute`:

```bash
cargo-ai orchestration action get-output-schema \
  --action '{"kind":"connector","integrationSlug":"clearbit","actionSlug":"enrichCompany"}'
# → {"schema": {"type": "object", "properties": {...}}}  — the JSON Schema is under the top-level "schema" key

# When the output depends on the inputs, pass them exactly as `execute` takes
# them (--data needs CLI >= 1.0.67):
cargo-ai orchestration action get-output-schema \
  --action '{"kind":"connector","integrationSlug":"hubspot","actionSlug":"findRecords"}' \
  --data '{"objectType":"contacts"}' 
```

Actions that declare no output schema fail with `"Action has no output schema."` (non-zero exit, status 404) — that's the signal to fall back to inspecting `runContext` from a real run. Use these to:

- Know which fields a downstream node can read (`{{nodes.<slug>.<field>}}`) **before** wiring the graph.
- See an `agent` action's real output envelope — a default free-text agent resolves to `{"schema":{"type":"object","properties":{"answer":{"type":"string"}}}}`, which is why downstream references need `{{nodes.<slug>.answer...}}`.
- Map an action's output onto storage columns without a throwaway run.

See `references/examples/actions.md` ("Resolve an action's output schema") for verified per-kind examples and the response/error shapes.

## Create a run

A run processes a single record through a workflow. Use `run create` when you need to **chain multiple actions** together via a node graph, or when running an existing tool workflow.

**Runs only work with tool workflows.** Play workflows return `playNotCompatible` — use `batch create` instead.

```bash
cargo-ai orchestration run create \
  --workflow-uuid <tool.workflowUuid> \
  --data '{"company":"Acme","domain":"acme.com"}'
# → Poll with: cargo-ai orchestration run get <run-uuid>

# Or wait synchronously — blocks until the run reaches a terminal state and returns the final result
cargo-ai orchestration run create \
  --workflow-uuid <tool.workflowUuid> \
  --data '{"company":"Acme","domain":"acme.com"}' \
  --wait-until-finished
```

Also supports `--release-uuid` to pin a specific release.

**Cancelling runs:**

```bash
cargo-ai orchestration run cancel --workflow-uuid <uuid> --uuids run-uuid-1,run-uuid-2
```

See `references/examples/tools.md` for file uploads, monitoring, and cancellation. See `references/nodes.md` for custom node graphs.

## Create a batch

> **Sample first, then ask before enrolling everything — blocking.** A batch fans one workflow across every record in its data source, so a mistake and a full bill land together. Never enroll a full segment/file/model on the first attempt: run a **10–20 record sample**, report what it cost and returned, then ask the user to approve the full enrollment with the **record count and credit estimate** in the question. Mechanics below; the spend rules behind it are [`../cargo-gtm/references/cost-discipline.md`](../cargo-gtm/references/cost-discipline.md).

### The sample gate

**1. Count the pool first (free).** Never quote an estimate from a guess:

```bash
cargo-ai segmentation segment get <segment-uuid>          # → recordsCount (also on `segment list`)
cargo-ai storage query execute "SELECT count() FROM <dataset>.<model>"   # for a filter/model source
# For a file source: wc -l on the CSV, minus the header row.
```

**2. Run 10–20 records through the exact workflow and config.** Sample by data kind:

```bash
# Play workflow, segment source → reuse the segment's own filter, capped by `limit`
cargo-ai segmentation segment get <segment-uuid>          # → copy .filter and .modelUuid
cargo-ai orchestration batch create \
  --workflow-uuid <play.workflowUuid> \
  --data '{"kind":"filter","modelUuid":"<modelUuid>","filter":<segment.filter>,"limit":15}' \
  --wait-until-finished

# Play workflow, explicit records → pick 10–20 ids
cargo-ai orchestration batch create \
  --workflow-uuid <play.workflowUuid> \
  --data '{"kind":"recordIds","modelUuid":"<modelUuid>","ids":["id-1","…","id-15"]}'

# Tool workflow, inline records → slice the array
cargo-ai orchestration batch create \
  --workflow-uuid <tool.workflowUuid> \
  --data '{"kind":"records","records":[ /* first 15 only */ ]}'

# Tool workflow, file → upload a truncated CSV (header + 15 rows), not the full file
head -n 16 leads.csv > leads-sample.csv
cargo-ai workspaceManagement file upload --file ./leads-sample.csv
```

`limit` is the sampling lever for `kind: "filter"`. `kind: "segment"` and `kind: "change"` have **no limit** — they always enroll the whole set, so sample via `filter` or `recordIds` and switch to `segment` only for the approved full run.

**3. Report the sample, then ask.** The confirmation must carry both numbers the user needs to decide:

```
Sample: 15 of 1,240 records · 6.2 credits (0.41/record) · 13/15 enriched (87%)
Full enrollment: 1,225 remaining records ≈ 502 credits (balance: 780)

Enroll all 1,225? Or:
  1. Enroll all 1,225 (≈502 cr, leaves ~278)
  2. Trim scope — e.g. the 610 records with a domain set (≈250 cr)
  3. Stop here and review the sample output first
```

Wait for an explicit answer. **Do not enroll the full set on an unanswered question**, and don't treat approval of the sample as approval of the full run. Skip the gate only when the batch is free (no paid nodes) *and* small, or when the user has already named the scope and approved the cost this session.

Batches process multiple records at once. Allowed data kinds depend on the workflow type:

- **Play** workflows: `filter`, `recordIds`, `segment`, `change`
- **Tool** workflows (or no `workflowUuid`): `file`, `records`

Use `filter` to trigger a play — it queries the model directly. `segment` only
accepts a **standalone** segment from `segmentation segment list`; passing the
`segmentUuid` that `play list` returns is rejected (`segmentLinkedToPlay`, or
`noRecords` on older backends) because a play's generated segment never has a
populated record count.

```bash
# Play workflow — run over the play's model (empty filter = all rows)
cargo-ai orchestration batch create \
  --workflow-uuid <play.workflowUuid> \
  --data '{"kind":"filter","modelUuid":"...","filter":{"conjonction":"and","groups":[]}}'

# Tool workflow — run on a file
cargo-ai orchestration batch create \
  --workflow-uuid <tool.workflowUuid> \
  --data '{"kind":"file","s3Filename":"..."}'
# → Poll with: cargo-ai orchestration batch get <batch-uuid>

# Or wait synchronously — blocks until the batch reaches a terminal state and returns the final result
cargo-ai orchestration batch create \
  --workflow-uuid <play.workflowUuid> \
  --data '{"kind":"filter","modelUuid":"...","filter":{"conjonction":"and","groups":[]}}' \
  --wait-until-finished
```

**Downloading results:** get the `releaseUuid` from batch get, then `cargo-ai orchestration release get <release-uuid>` to find `nodes[].slug`, then `cargo-ai orchestration batch download --uuid <batch-uuid> --output-node-slug <slug>`.

**Cancelling a batch:**

```bash
cargo-ai orchestration batch cancel <batch-uuid>
```

See `references/examples/plays.md` and `references/examples/tools.md` for filtering, record IDs, file uploads, monitoring, and cancellation.

## Send a message to an AI agent

```bash
cargo-ai ai agent list                                    # 1. Find the agent
cargo-ai ai chat create \                                 # 2. Create a chat
  --trigger '{"type":"draft"}' \
  --agent-uuid <agent-uuid> --name "Research session"
cargo-ai ai message create \                              # 3. Send a message
  --chat-uuid <chat-uuid> \
  --parts '[{"type":"text","text":"Find the VP of Sales at Acme Corp"}]'
# → Extract assistantMessage.uuid, poll with: cargo-ai ai message get <uuid>
#   Done when .message.status is "success" (read .parts) or "error" (read .errorMessage)
```

Also supports `--actions`, `--resources`, `--language-model-slug`, `--temperature`, `--max-steps`, and `--wait-until-finished` (blocks until the assistant message reaches a terminal status). See `references/examples/agents.md` for multi-turn conversations, action/resource injection, and model selection.

## Inspect records

Records are individual items processed by a workflow. Use these commands to list, count, download, or cancel records within a workflow.

`record download-outputs` is the **record**-grained sibling of `run download-outputs`: one row per record rather than per run. It pages with `--limit` / `--offset` (CLI ≥ 1.0.90), which is how you export a set too large for one file — walk it in fixed slices rather than asking for everything and timing out.

```bash
# List records for a workflow
cargo-ai orchestration record list --workflow-uuid <uuid> --limit 50

# Filter by batch or status
cargo-ai orchestration record list --workflow-uuid <uuid> --batch-uuid <uuid> --statuses error

# Count records
cargo-ai orchestration record count --workflow-uuid <uuid>

# Download records as a file
cargo-ai orchestration record download --workflow-uuid <uuid>

# Download one output node's data, per record, paging through a large set
cargo-ai orchestration record download-outputs \
  --workflow-uuid <uuid> \
  --output-node-slug <slug> \
  --limit 1000 --offset 2000

# Get per-node execution metrics
cargo-ai orchestration record get-metrics --workflow-uuid <uuid>

# Cancel records
cargo-ai orchestration record cancel --workflow-uuid <uuid> --ids record-id-1,record-id-2
```

## Query orchestration history (orchestration query)

Run SQL against orchestration runtime tables — `spans`, `runs`, `batches`, `records` — with `orchestration query execute`. Use this for ad-hoc analytics on workflow execution (error rates, throughput, slowest nodes) without the workflow-scoped filters of `run get-metrics` / `run count`.

```bash
cargo-ai orchestration query execute "SELECT count() FROM runs WHERE status = 'error'"
cargo-ai orchestration query execute "SELECT status, count() FROM batches GROUP BY status"
cargo-ai orchestration query execute "SELECT * FROM spans ORDER BY execution_started_at DESC LIMIT 10"
```

Tables are referenced without a schema prefix — just `spans`, `runs`, `batches`, or `records`. Workspace scoping is applied automatically. The query is read-only; DDL, table functions, dictionary accessors, and introspection are denied. See `references/examples/queries.md` for the schemas, example queries, and limits.

## Fetch segment data

Retrieve live records from a segment. **IMPORTANT:** requires `--model-uuid` (not `--segment-uuid`). Get the `modelUuid` from `segment list`. Filter JSON uses `conjonction` (not `conjunction`) — this is intentional.

```bash
cargo-ai segmentation segment fetch \
  --model-uuid <uuid> \
  --filter '{"conjonction":"and","groups":[]}' \
  --fetching-limit 100 --fetching-offset 0
```

Supports `--sort`, `--enrich`, and `--sync`. See `references/filter-syntax.md` for the full filter syntax and `references/examples/segments.md` for filtering, pagination, sorting, enrollment filters, and enrichment.

**Managing segments:**

```bash
# Update a segment's name or filter
cargo-ai segmentation segment update --uuid <segment-uuid> --name "Updated Name"
cargo-ai segmentation segment update --uuid <segment-uuid> --filter '{"conjonction":"and","groups":[...]}'

# Remove a segment (fails if linked to a workflow)
cargo-ai segmentation segment remove <segment-uuid>
```

## Use a workflow template

Templates are pre-built node graphs for common automation patterns (enrichment pipelines, CRM syncs, lead scoring). Browse with `template list`, inspect with `template get <slug>`, fill in placeholders, validate, and run.

```bash
cargo-ai orchestration template list              # list available templates
cargo-ai orchestration template get <slug>        # get template nodes + config
```

See `references/examples/templates.md` for the full guide including placeholder conventions and end-to-end examples.

## Validate and test nodes

Always validate custom node graphs before running them.

```bash
cargo-ai orchestration node validate --nodes '[...]'
# → { "outcome": "valid" } or { "outcome": "notValid", "invalidNodes": [...] }
```

Then **show it before deploying it** — `validate` proves the graph is well-formed,
not that it does what the user asked for:

```bash
cargo-ai orchestration node diagram --nodes '[...]' --format ascii --raw   # free, runs nothing
```

Same command draws a deployed workflow (`--workflow-uuid`), a draft (`--draft`), a
release (`--release-uuid`), or the graph a run executed (`--run-uuid`). See
`references/node-diagram.md`.

For debugging, use `node compute` (dry-run expressions) or `node execute` (live test of one node **of an existing workflow** — needs `--workflow-uuid` + `--release-uuid` + `--computed-config`, and costs credits; for anything that isn't node-level debugging, use `action execute` instead). For runs that complete with `status: success` but produce wrong output (wrong branch taken, empty downstream values), use `run.executions[].title` from `run get` only as a quick summary — it may be truncated — and read `runContext.<nodeSlug>` (returned at the top level of the same `run get <run-uuid>` response) to verify field-level data. See `references/troubleshooting.md` → "Debugging a workflow run" and `references/nodes.md` for the full node creation guide, validation error codes, and examples.

## Help

Every command supports `--help`:

```bash
cargo-ai orchestration run create --help
cargo-ai orchestration template list --help
cargo-ai orchestration node validate --help
cargo-ai ai message create --help
cargo-ai orchestration query execute --help
```
