---
name: managed-agents
description: "Stand up, budget, and operate Claude Managed Agents - Anthropic-hosted agents with a per-session sandbox, versioned agent configs, vault-held credentials, cron deployments, and hard dollar budgets. Use when a task should run WITHOUT a human at the keyboard (scheduled briefings, recurring research, unattended ops), when you need Anthropic to run the agent loop and host the container, or when a user says 'managed agent', 'run this every night', 'spin up an agent that...', or 'enable Managed Agents'. Ships a preflight readiness check, an offline manifest validator that catches API 400s before they cost a round-trip, an idempotent apply loop, a budget-mandatory session runner with lossless reconnect and the correct idle gate, cron deployments that refuse to fire uncapped or on an agent that would wait for a human, and an allowlisted bridge that exposes chosen skills from this repository to a mounted session."
version: "1.1.0"
tags: ["managed-agents", "anthropic-api", "agents", "automation", "scheduling", "sandbox", "budgets", "zero-human"]
---

# Managed Agents

**Purpose:** Turn "I want an agent that does X on its own" into a running, budgeted, auditable Managed Agents session - and make it impossible to do the things that quietly cost money, leak secrets, or park an unattended session forever.

Managed Agents is the Anthropic API surface where **Anthropic runs the agent loop and hosts the container** the agent's tools execute in. You define a persistent, versioned **Agent**; every run is a **Session** that points at it. Sessions can be started by you or by a **scheduled deployment** (cron), and each carries a **hard dollar budget** the platform enforces.

This skill is the operator's console for that surface. It is runnable: `python -m engine <command>` from `skills/managed-agents/`.

---

## When to use this skill

Load this skill when any of these apply:

- The task should run **without a human present** - nightly, weekly, "every morning at 7", "watch this and report"
- The user wants **Anthropic to host the execution sandbox** (bash, files, code) rather than run tools on their own machine
- The user says **"managed agent"**, **"enable Managed Agents"**, **"spin up an agent that..."**, **"agent team"**, **"zero-human"**
- Work needs a **persistent, versioned agent definition** that many runs share, with rollback
- Work needs **credentials the agent can use but never see** (vaults - substituted at egress, never inside the sandbox)
- Work needs a **spend ceiling** that the platform enforces, not one the model is politely asked to respect
- Work fans out across sources or files and one loop would drown in reading (multiagent roster)

Do NOT load this skill for:
- A single classification / summarisation / extraction call - use the plain Messages API
- A coding agent on the user's own machine with the user watching - that is Claude Code / the Agent SDK, a different product
- Tools that must execute on the user's hardware with the user's own runtime - use the Messages API tool runner and host it yourself
- Anything where the user has said they will not spend API credit - Managed Agents bills the API workspace, not a Claude Pro/Max seat

---

## The five rules

| # | Rule | Why it exists |
|---|------|---------------|
| 1 | **Agent first, session second. Agent ONCE.** `model` / `system` / `tools` / `mcp_servers` / `skills` live on `POST /v1/agents`, never on the session. Create it once, store the ID, reference it forever. | Sessions pin to an agent *version*. Re-creating agents orphans running sessions, defeats rollback, and pays create latency every run. |
| 2 | **Every session and every deployment carries a budget.** `budget: {type: limit, max_list_cost: {amount: "<cents>", currency: USD}}`. The engine refuses to create an uncapped session and refuses to create an uncapped deployment. | The platform enforces this before every model request. A session that hits it *pauses* (`stop_reason: budget_reached`) - history and sandbox preserved. It is the only ceiling that does not rely on the model's good behaviour. A cron deployment fires unattended, forever, so an uncapped one is the most expensive mistake available. |
| 3 | **Secrets go in a vault, never in a manifest, prompt, or message.** MCP auth: `mcp_oauth` / `static_bearer` keyed by server URL. Anything else: `environment_variable`, substituted at egress. A repo-mount token is written as `${GITHUB_TOKEN}` and read from the environment at apply time. | Prompts and messages are persisted in the session's event history for the life of the session. A vault credential never enters the sandbox at all. The validator rejects credential-shaped strings and literal tokens because these manifests are committed. |
| 4 | **`session.status_idle` is not "done", and history is not "read-only".** Break only on `session.status_terminated`, or on idle with `stop_reason.type != requires_action`. On every (re)connect, `events.list()` history goes through the *same dispatch* as the live stream, and a `requires_action` idle's `stop_reason.event_ids` is answered in full. | Sessions idle transiently while waiting on *you*. SSE has no replay: a pending ask emitted while your stream was down exists only in history. Read it without answering it and the session deadlocks. |
| 5 | **A deployment must fire an agent that can finish alone.** No `always_ask` tool and no `custom` tool may be in effect on a scheduled run; `agent_overrides.tools` disables them for the deployment only. The validator cross-checks this, and `deploy` refuses if it cannot find the agent's manifest to check. | A deployment has no client attached. The first gated tool call - or the first custom tool call, which likewise idles the session for a client - parks the run in `requires_action`: every firing, silently, with the sandbox alive. |

---

## Commands

Run from `skills/managed-agents/`:

| Command | What it does | Spends money? |
|---------|--------------|---------------|
| `python -m engine preflight [--live]` | Readiness: Python, SDK version + namespaces, credential *source* (never the value), billing note, manifests. `--live` adds one `GET /v1/agents` - the definitive "is the beta enabled for this workspace" answer. | **No.** `--live` is a control-plane read. |
| `python -m engine validate` | Lint every manifest against the documented API constraints offline, including cross-manifest checks (a deployment's effective tools). | **No.** No network at all. |
| `python -m engine bridge [--check] [--all] [--no-prune] [--mode copy\|symlink]` | Build root `.claude/skills/` from `bridge.allowlist` so a session that mounts this repo discovers those skills. `--check` verifies (missing / extra / broken / stale). | **No.** |
| `python -m engine apply [--dry-run]` | Create-or-update every agent and environment manifest, idempotent by name, **declarative** (a block deleted from the file is cleared on the live agent). Writes IDs + versions to `agents/state.json`. | **No.** |
| `python -m engine status` | Show applied IDs and versions. | **No.** |
| `python -m engine run <Agent> "<task>" --budget 5` | Create a budgeted session pinned to the applied version, stream it, answer tool asks, print the Console trace link. Confirms before spending unless `--yes`. | **YES.** Capped at `--budget` (default $5.00). |
| `python -m engine deploy <manifest> [--budget 5]` | Create-or-update a cron deployment. Budget precedence: `--budget` flag, else the manifest's `budget:`, else **refused**. | **On every firing**, capped. |
| `python -m engine runs <deployment> [--failures]` | Audit trail of deployment firings (every page). | **No.** |

Every command accepts `--json` after the subcommand.

---

## Enabling it - the sequence

```
1. python -m engine preflight          # what is missing on this machine?
2. pip install --upgrade anthropic     # if preflight said so
3. ant auth login   OR   export ANTHROPIC_API_KEY=...   (never paste a key into chat)
4. python -m engine preflight --live   # is the workspace enrolled?  ($0)
5. python -m engine validate           # manifests clean, cross-checks pass?
6. python -m engine apply              # create the agents + environment ($0)
7. python -m engine run Atlas "..." --budget 2   # first real session, tiny cap
8. python -m engine deploy agents/morning-briefing.deployment.yaml --dry-run
```

Step 4 is the one that answers "is Managed Agents enabled?" - a 403/404 on `GET /v1/agents` means the workspace is not enrolled in the beta; fix that in the Console before anything else.

**Billing reality check:** Managed Agents bills the Anthropic **API workspace** (console credit / invoicing). A Claude Pro or Max subscription does not cover it. Confirm the workspace has credit before step 7.

---

## What ships in `agents/`

| File | Kind | Notes |
|------|------|-------|
| `environment.yaml` | environment `henry-cloud` | `limited` egress, package managers on. `web_search` / `web_fetch` are unaffected by this - they run on Anthropic's side. |
| `atlas.yaml` | agent | Strategy. Full toolset, `bash` asks (interactive). Houston-localised search. |
| `ledger.yaml` | agent | Finance. `xlsx` + `pdf` skills, `bash` asks - **interactive by design**, not for cron. |
| `shield.yaml` | agent | Legal research. **No bash.** Web tools allow-listed to primary-source domains. `read` handles PDFs natively; no script-driven skills. |
| `closer.yaml` | agent | Sales. No bash, Markdown drafts only, never sends. |
| `axis.yaml` | agent | Operations. Bash asks. Meant to mount this repository. |
| `morning-briefing.deployment.yaml` | deployment | Atlas at 07:10 weekdays `America/Chicago`, with `agent_overrides.tools` disabling `bash` for the unattended run and a manifest `budget:` of $5.00. |

Forge (engineering) is deliberately absent: it runs on a different model stack and is not a Claude Managed Agent.

These files live in a **public** repository. They carry personas and rules, not numbers: pricing bands, acquisition multiples, pipeline identifiers, and matter facts are supplied per session (prompt or mounted file), never committed. The validator enforces the credential half of that; the business-fact half is on you.

The manifest **is** the API body plus a `kind:` discriminator and an optional `x-notes:` block. Anything the API accepts, the manifest accepts.

---

## Manifest shapes

**Agent**

```yaml
kind: agent
name: Atlas                      # 1-256 chars; apply is idempotent on this
model: {id: claude-opus-5, effort: high}   # effort lives HERE - inside an override it is silently ignored
system: |                        # <= 100K chars. NO secrets. NO business facts if the file is committed.
  ...
tools:
  - type: agent_toolset_20260401
    default_config: {enabled: true, permission_policy: {type: always_allow}}
    configs:
      - name: bash
        permission_policy: {type: always_ask}     # session idles; you send user.tool_confirmation
      - name: web_search
        allowed_domains: [texas.gov, courtlistener.com]   # plain hostnames, covers subdomains, max 64
        user_location: {type: approximate, city: Houston, country: US, timezone: America/Chicago}
      - name: web_fetch
        max_content_tokens: 50000
  # - {type: mcp_toolset, mcp_server_name: github}   # must match an mcp_servers entry
  # - {type: custom, name: run_tests, description: ..., input_schema: {...}}
mcp_servers: []                  # {type: url, name, url} ONLY - auth is a vault credential
skills:
  - {type: anthropic, skill_id: xlsx}   # requires the `read` tool; script-driven ones also need bash
metadata: {owner: henry-ai}      # <= 16 keys, string values only
```

**Deployment**

```yaml
kind: deployment
name: henry-morning-briefing
agent_name: Atlas                # resolved from agents/state.json at deploy time
environment_name: henry-cloud
agent_overrides:                 # optional -> API `agent_with_overrides`; replaces fields IN FULL
  tools: [...]                   #   restate the whole toolset with the gated tools disabled
budget: {type: limit, max_list_cost: {amount: "500", currency: USD}}   # "500" = $5.00 per firing
schedule: {type: cron, expression: "10 7 * * 1-5", timezone: America/Chicago}
initial_events:
  - {type: user.message, content: [{type: text, text: "..."}]}
resources:                       # optional; tokens are ${ENV} references, never literals
  - {type: github_repository, url: https://github.com/o/r, authorization_token: "${GITHUB_TOKEN}"}
```

Things the validator will stop you from sending - each is a documented 400 or a documented deadlock:
`environment_id` / `resources` / `vault_ids` / `budget` on an agent - a wildcard, scheme, port, IP, underscore, `localhost`, or registry suffix (`co.uk`) in a domain list - `allowed_domains` and `blocked_domains` on the same tool - a path on a `web_fetch` domain - a decimal or zero-padded budget amount (`"25.00"`, `"0500"`; it must be `"2500"`) - an `mcp_toolset` naming an undeclared server - skills with `read` disabled - non-string metadata values - `packages` outside `config` on an environment - a 4-field cron or a missing timezone - a deployment with no starting event - a literal `authorization_token` or any `ghp_` / `sk-ant-` / `AKIA`-shaped string anywhere - a deployment whose effective tools still carry `always_ask`.

---

## Exposing this repository to a session

The platform scans a mounted repository's **root `.claude/skills/<name>/SKILL.md`** at session start - one level deep, nothing nested, nothing outside `.claude`. This repository keeps skills in `skills/`, some nested two levels.

`python -m engine bridge` builds that flat index **from `bridge.allowlist`**, as **copies** by default:

- **Allowlist, not everything.** Repository skills are agent instructions loaded with no review step, in a sandbox with `bash` and `web_fetch`. This library also carries ~25 offensive-security skills; they are not in the default list. Every bridged skill's name and description is also announced to the agent each session - a per-turn context cost charged against the budget. `--all` overrides.
- **Copy, not symlink.** Nothing in the platform docs says the scanner follows symlinks, and confirming it costs money. Copies are guaranteed to work; `--check` reports a copy whose source has since changed as `stale`. `--mode symlink` exists for when symlink-following has been confirmed.
- **Never deletes.** A stray symlink is unlinked (the bridge's own artefact). Every real directory that is unwanted, or that differs from its source (a local edit, or drift), is moved to `.claude/skills-quarantine/<date>/` before anything is written; an up-to-date copy is left untouched. `--no-prune` leaves strays alone. `--dry-run` names exactly what would be created, left, unlinked, or quarantined. A skill containing a symlink that resolves outside the repository is refused rather than copied.
- **Not itself, not the document skills.** `managed-agents` is not bridged (a mounted session reads `skills/managed-agents/` directly; a copy would drift), and the four `*-official` document skills are not either - they are 73% of the library's bytes and the agents that need them attach Anthropic's *hosted* `xlsx`/`pdf`/... via `skills:`.

Then mount:

```yaml
resources:
  - type: github_repository
    url: https://github.com/whd4/expert-ai-skills
    authorization_token: "${GITHUB_TOKEN}"   # fine-grained PAT, Contents: Read; injected by Anthropic's git proxy
    checkout: {type: branch, name: main}
```

Skills are scanned once, from the checkout at session start - push a change, start a new session. Only mount what you trust.

---

## Driving a session correctly (what `engine/session.py` does)

```
open stream
  -> read events.list() history (every page) and DISPATCH each event exactly like a live one
  -> send user.message (once)
  -> for each event, history or live:
       agent.custom_tool_use                          -> run host-side, send user.custom_tool_result   (once per event id)
       agent.tool_use | agent.mcp_tool_use, permission=ask
                                                      -> send user.tool_confirmation {allow|deny, deny_message}
                                                         (session_thread_id echoed for multiagent)
       session.status_terminated                      -> stop
       session.status_idle, requires_action           -> answer every stop_reason.event_ids not yet answered; keep reading
       session.status_idle, anything else             -> stop (end_turn | retries_exhausted | budget_reached)
  -> stream drops: reconnect (<= 3x), re-read history, dedupe by id, continue
  -> settle(): poll retrieve() until status != running before archive/delete
```

`tool_use_id` on a confirmation is the **event id** (`sevt_…`), not a `toolu_…` id. `session.usage` events carry the running `list_cost`. `budget_reached` is a pause, not a failure - raise or remove the budget to resume. `--approve allow-all` auto-approves every gated call, including a shell command the agent composed from a page it just fetched; the CLI requires `--yes` alongside it and logs each auto-approval.

---

## Credentials - how they actually flow

| Need | Mechanism | The agent sees |
|------|-----------|----------------|
| MCP server auth | vault credential `mcp_oauth` / `static_bearer`, keyed by server URL; attach `vault_ids` at session create (create-only) | nothing - injected by Anthropic's MCP proxy |
| API key for a CLI / SDK / `curl` in `bash` | vault credential `environment_variable` with `networking.allowed_hosts` | an opaque placeholder; real value substituted at egress, headers/body only, never URL path |
| Git push to a mounted repo | `authorization_token: "${GITHUB_TOKEN}"` on the `github_repository` resource, expanded from the environment at apply time | nothing - git proxy injects it |
| Secret that must never leave your infra | declare a `custom` tool; your orchestrator executes the call with its own key and returns `user.custom_tool_result` | only the result |

Never put a key in `system`, in a `user.message`, or in a committed manifest. The validator rejects `auth`/`token`/`headers` keys on `mcp_servers` entries, literal resource tokens, and credential-shaped strings anywhere.

---

## Scheduled deployments - the three traps

1. **Jitter.** Firing is delayed up to 15% of the interval (floor 5 s, cap 9 min). Never hang a downstream deadline off `upcoming_runs_at`.
2. **DST.** Cron matches literal wall-clock in the IANA timezone. 01:00-03:59 local is *skipped* on spring-forward and *fires twice* on fall-back. The validator warns; the shipped deployment fires at 07:10.
3. **Nobody is there.** An `always_ask` tool on the fired agent parks every run in `requires_action`. Put the gated tools behind `agent_overrides.tools` (restating the whole toolset) or give the deployment its own agent. The validator refuses a deployment whose effective tools still ask.

Pause is reversible; archive is terminal. Test with a manual run (`POST /v1/deployments/{id}/run` - works while paused) before trusting the schedule. Every firing writes a `drun_` record whether it succeeded or not - `python -m engine runs <name> --failures` is the audit. `apply` for deployments never falls through from a failed update to a create: a transient 500 must not leave two cron jobs firing.

---

## Other agents calling this skill

See `engine/agent_contract.md` - every command has a `--json` form, and `engine.config.validate(manifest)` / `engine.config.validate_all(paths)` / `engine.preflight.run(...)` are importable without the SDK installed.

## Tests

```bash
cd skills/managed-agents && python3 -m engine.tests.test_managed_agents
```

Offline. No SDK, no credentials, no spend. Every rejection test is a negative control; the session runner is driven end-to-end by a fake client (history-only pending asks, stream drops, duplicate delivery, `event_ids` recovery, MCP confirmations, budget pauses).
