---
name: cargo-observability
description: "Watch a Cargo workspace and get told when something breaks — scheduled threshold alerts over workflow telemetry (spans, runs, records), a storage model freshness or row count, or any SQL query, firing a connector, tool, or agent when a metric breaches. Triggers: \"alert me when\", \"notify me if\", \"let me know when the error rate\", \"monitor this workflow\", \"tell me if the sync stops\", \"warn me before I run out of credits\", \"dead man’s switch\", \"is this still running\", \"set up monitoring\", plus listing, previewing, editing, and reviewing an alert firing history. Skip when: diagnosing something that already went wrong — use cargo-diagnostics."
version: "1.0.3"
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

# Cargo CLI — Observability

**Alerts.** An alert is a scheduled threshold check. On every cron tick it measures a **scope** (what to watch), compares the measured value against a **threshold** (the breach condition), and on breach fires **actions** — each as its own run — and records an **event**. This is the proactive counterpart to `cargo-diagnostics`: diagnostics explains a failure *after* you notice it; an alert *tells you* the moment a metric crosses a line.

Everything lives under one CLI domain:

```bash
cargo-ai observability alert   …   # the alert CRUD + preview surface
cargo-ai observability event   …   # an alert's firing history
```

## Bootstrap

Already signed in (`cargo-ai whoami` returns a workspace)? Skip to the next section.

```bash
npm install -g @cargo-ai/cli            # no global install? prefix every command with `npx @cargo-ai/cli`
cargo-ai login --email you@company.com  # emailed code, no browser; creates the account on first use
                                        # alternatives: --oauth (browser) · --token <api-token> (CI)
cargo-ai whoami                         # confirm the active workspace before any write
```

Every command prints JSON to stdout; failures exit non-zero with `{"errorMessage": "..."}`. Anything that creates a run or a batch is async — pass `--wait-until-finished` or poll the matching `get`. Alerts are guarded by `observability:read` / `observability:write` permissions. If a create/update/remove returns a permission error, the token lacks `observability:write` — use an admin token or have one granted ([`../cargo-workspace-management/SKILL.md`](../cargo-workspace-management/SKILL.md)). When the full skill bundle is installed, [`../cargo/references/prerequisites.md`](../cargo/references/prerequisites.md) adds the CLI version pin, token scopes, and the admin-only surface.

## The three moving parts of every alert

| Part | Flag | What it is |
| --- | --- | --- |
| **Scope** | `--scope <json>` | *What* to measure — one of six sources: `spans`, `runs`, `records`, `orchestrationQuery`, `storageQuery`, `model`. |
| **Threshold** | `--threshold <json>` | *When it breaches* — a `metric` + `operator` (`gte`/`lte`) + `value`. The metric menu depends on the scope. |
| **Actions** | `--actions <json>` | *What happens on breach* — an `Action[]` (connector / tool / agent / native nodes), each fired as its own run. Optional; omit for a silent alert whose breaches you read from its events. |

The scope and threshold are a **matched pair** — a metric can only be computed over the scopes that produce it (e.g. `errorRate` needs telemetry, `freshness` needs a model). The full compatibility matrix, every metric's meaning and units, and every scope filter field are in **[`references/scopes-and-thresholds.md`](references/scopes-and-thresholds.md)** — read it before writing a `--scope`/`--threshold` pair you haven't used before.

## The golden rule: `preview` before you `create`

`alert preview` evaluates a scope + threshold **right now, without firing actions or writing an event**. It returns the value the alert would measure and whether that value breaches — so you calibrate the threshold against reality instead of guessing, and you confirm the scope/threshold pairing is even valid before committing it to a schedule.

```bash
cargo-ai observability alert preview \
  --scope '{"kind":"runs","workflowUuid":"<uuid>","statuses":["error"]}' \
  --threshold '{"metric":"errorRate","operator":"gte","value":10}' \
  --window-minutes 1440          # last 24h; default 60
```

- `outcome: "computed"` → `{ value, total, failed, isBreached }`. Set your threshold from `value`.
- `outcome: "empty"` → the window had nothing to measure (see the empty-vs-zero rule in `references/alert-lifecycle.md`).
- `outcome: "notComputed"` → `{ errorMessage }`. A bad SQL query, a deleted model, or an **invalid scope/threshold pairing** all land here — fix it before creating.

`--window-minutes` only shapes the window for telemetry scopes (`spans`/`runs`/`records`). A `model` is measured as it stands right now; a query scope windows itself in its SQL.

**Always preview first.** It is free, it is the only way to size a threshold correctly, and it catches an invalid pairing before it becomes a schedule that writes an `error` event every tick.

## Commands

All commands output JSON. Reads need a token with `observability:read`; create/update/remove need `observability:write` (an admin token has both; a plain member token may not — see Bootstrap above).

### Create an alert

```bash
cargo-ai observability alert create \
  --name "CRM sync error rate" \
  --description "Page when the HubSpot sync starts failing" \
  --cron "*/30 * * * *" \
  --scope '{"kind":"runs","workflowUuid":"<workflow-uuid>","statuses":["error"]}' \
  --threshold '{"metric":"errorRate","operator":"gte","value":10}' \
  --actions '[{"kind":"agent","agentUuid":"<agent-uuid>","config":{"message":"{{alert.name}} breached: {{event.value}}% errors. {{alert.url}}"}}]'
```

- `--cron` — 5-field cron **or** `@every <interval>` (e.g. `@every 30m`), always **UTC**, at most once a minute. The UI presets bottom out at 30 minutes; go tighter only with reason (every tick scans ClickHouse and can fire paid runs).
- `--disabled` — create it paused (evaluate nothing until you `update --enabled true`).
- `--folder <uuid>` — file it under a folder (from `cargo-workspace-management`).
- `--actions` — optional. Omit for a silent alert. Each entry is a **configured** action: unlike `orchestration action execute`, which carries no `config` at all, an alert action **requires** one — that is where the templated message lives. The config is templated against the firing context (`{{alert.*}}`, `{{event.*}}`) — see [`references/alert-lifecycle.md`](references/alert-lifecycle.md) for the full variable list. Each action's target (`agentUuid`/`toolUuid`/`connectorUuid`) is validated to exist in the workspace at create time.

### List, get, update, remove

```bash
cargo-ai observability alert list                      # all alerts, each with its lastEvent
cargo-ai observability alert get <uuid>                # one alert + its lastEvent

cargo-ai observability alert update --uuid <uuid> \
  --enabled false                                      # pause it (true/false — must be literal)
cargo-ai observability alert update --uuid <uuid> \
  --threshold '{"metric":"errorRate","operator":"gte","value":20}'   # raise the bar
cargo-ai observability alert update --uuid <uuid> \
  --description none                                    # "none" clears; --folder none unfiles

cargo-ai observability alert remove <uuid>
```

`--enabled` is strict: only the literal `true` or `false` are accepted — `--enabled yes` is rejected rather than silently disabling the alert. On `update`, any flag you omit is left unchanged; `--description none` / `--folder none` are the explicit "clear it" spellings.

### Inspect firing history

```bash
cargo-ai observability event list <alertUuid>          # latest evaluation events, newest first
```

Each event carries `status` (`healthy` / `unhealthy` / `error`), the measured `value`, a **snapshot** of the `scope`/`threshold`/`actions` as they were when it fired (the alert can change afterwards), `runUuids` (the runs the actions spawned — feed these to `cargo-diagnostics` or `orchestration run get`), the evaluation window, and `errorMessage` for `error` events. `unhealthy` = breached and fired; `error` = the metric could not be computed.

## How evaluation actually works

The lifecycle — cron windows and the ClickHouse indexing lag, the **at-most-once** firing guarantee (an alert never re-fires on the same rows; a *sustained* breach is re-detected on the next tick), the empty-window-vs-real-zero rule that makes `lte` a dead-man's switch, and the full `{{alert.*}}`/`{{event.*}}` templating context — is documented in **[`references/alert-lifecycle.md`](references/alert-lifecycle.md)**. Read it before you rely on an alert for anything time-sensitive.

## Worked recipes

**[`references/examples/recipes.md`](references/examples/recipes.md)** — copy-paste starting points: error-rate pager, credit-budget guard, p95-latency watch, a **dead-man's switch** (`count lte 0` — alert when a workflow *stops* running), model freshness / empty-model alerts, and a custom SQL-query alert.

## Declarative alternative: `defineAlert` (CDK)

This skill is the **imperative** surface — one-off `cargo-ai observability alert …` calls. To manage an alert **as code** (in git, reproducible, deployed alongside the workflow it watches), use CDK's `defineAlert` builder instead — see [`../cargo-project/SKILL.md`](../cargo-project/SKILL.md) and "Declarative vs imperative" in the router. Same scope/threshold/action model; different authoring mode.

## Cost discipline

An alert's **actions fire as real runs** — if an action calls a paid connector action or an agent, every breach re-bills. A poorly-sized threshold on a tight cron can breach (and bill) every tick. Two safeguards:

- **Preview to size the threshold** so it fires on genuine anomalies, not normal variance.
- If an action node calls a **credits-based provider action**, treat it like any scheduled paid workflow: read that provider's playbook (esp. its *Recurring use* section) in `../cargo-gtm/provider-playbooks/`, and apply the spend rules in [`../cargo-gtm/references/cost-discipline.md`](../cargo-gtm/references/cost-discipline.md). Prefer cheap notification actions (an agent that posts to Slack, a connector notification) over anything that fans out.

## When the CLI surprises you

If a documented flag, scope field, or response shape doesn't match what you observe (a fix may have shipped, or the docs may have drifted), re-refresh the CLI and skills; if it still doesn't add up, file a report — it's read by the team:

```bash
cargo-ai workspaceManagement report create \
  --title "<one-line summary>" \
  --description "<exact command(s), errorMessage verbatim, expected vs actual, UUIDs>"
```

## Presenting results

Follow [`../cargo/references/interaction.md`](../cargo/references/interaction.md): lead with the outcome ("alert created, will page the on-call agent when the CRM sync's error rate hits 10% over 30 min"), summarize an alert or its events as a compact table, never dump raw `alert get` / `event list` JSON into the conversation.
