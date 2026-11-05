---
name: payprobe-agents
description: >
  Operating PayProbe's agents (agent-hub, ADR-0010): what an agent principal and a
  workflow are, the six builtin agents and two reference workflows, how a heartbeat runs and
  where its output lands, the approvals inbox, every way an agent gets woken (portal, MCP,
  schedule, orchestrator events, signed inbound webhooks), the alert webhook, and the safety
  model (modes, allowlist, write scope, journal + revert, approval gates, egress allowlist,
  pause). Load this when the task mentions: agent-hub, :8600, "wake an agent", heartbeat,
  observer / failure-triage / certification-planner / plan-executor / reviewer / config /
  scenario-author, workflow run, approvals inbox, "agent did nothing", "agents paused",
  "budget_exceeded", "orphaned by restart", "egress refused", AGENT_HUB_*, /api/agents,
  "how do I get the agent's output", "agents are spending tokens", or adding a new builtin
  agent or workflow.
---

# PayProbe — Agents (agent-hub, ADR-0010)

Runbook for the agent layer: bounded, journalled, human-gated LLM agents that watch and
change the platform through the one tool layer. Facts verified against the working tree
on 2026-09-23 (branch `adr-0010`). Commands are repo-root-relative.

**When NOT to use this skill:**

| You are trying to… | Use instead |
|---|---|
| Understand an `AGENT_HUB_*` variable's default or add a knob | `payprobe-config-and-flags` (§7.6) |
| Bring the stack up, start runs, operate simulators | `payprobe-run-and-operate` |
| Decide whether a change to agent-hub is safe to ship | `payprobe-change-control` |
| Read the design rationale and rejected options | `docs/adr/0010-agent-registry-and-orchestration.md` |
| Continue the build (what is done, what is owed, in order) | `docs/history/2026-09-23-agent-hub-handoff.md` |

Jargon: an **agent** is a versioned definition (role, instructions, tool allowlist, mode,
write scope, limits, budget, triggers, RBAC), not a process. A **heartbeat** is one
bounded wake of an agent: a short LLM tool-calling loop that ends in a durable record. A
**workflow** is a JSON DAG of nodes (agent tasks, tool calls, conditions, human
approvals). **Mode** is what an agent may do: `advisor` reads only, `plan` proposes exact
write calls a human applies, `full` executes journalled writes inside its write scope.

## 1. Where things are

| Piece | Location |
|---|---|
| Service | `packages/agent-hub` (FastAPI, port 8600, PostgreSQL only, no file fallback) |
| Portal | Configure → Agents (tabs Agents / Workflows; heartbeats under an agent, runs under a workflow, approvals inbox above the Workflows tab) |
| API through the portal | `http://localhost:8080/api/agents/...` (nginx → agent-hub) with your user JWT |
| MCP | group "Agents & workflows (ADR-0010)" on the MCP server (:8200) |
| Folded-in assistant | `/api/assistant/*` is served by agent-hub's `/assistant` mount; the `assistant` container is a deprecated alias until phase 5 ends |
| Tables | `agent_hub_definitions`, `agent_hub_versions`, `agent_hub_heartbeats`, `agent_hub_runs`, `agent_hub_approvals`, `agent_hub_plans`, `agent_hub_meta` (pause flag), `agent_hub_migrations` (schema 3) |
| Tests | `packages/agent-hub/tests/test_hub_*.py` (154 on 2026-09-23); CI steps "Test agent-hub" and "agent-golden" |

Health: `curl -s localhost:8600/health` → `schema_version`, `paused`, `alerts` stats,
`egress` allowlist. `/api/agents/health` through the portal is the same, public.

## 2. The builtins (seeded on first start; missing ones added on later starts)

| Agent | Mode | Wakes | Purpose |
|---|---|---|---|
| `config` | plan | manual, mcp | the configuration assistant as a principal: proposes registry changes |
| `scenario-author` | plan | manual, mcp | NL → scenario draft, proposes `create_scenario` / `update_scenario` |
| `observer` | advisor | manual, **schedule every 900 s**, `run.failed`, `gate.failed` | ops observer; answers with JSON findings (severity, subject, headline, evidence, next_step) |
| `certification-planner` | plan | manual, `run.completed` | authors a certification plan artifact |
| `reviewer` | advisor | manual | reviews another agent's output; `{"verdict": "approve" | "changes_requested"}` |
| `failure-triage` | advisor | manual, `run.failed`, mcp | root-cause verdict for one failed run (category, evidence, regression, next_step) |
| `plan-executor` | **full**, admin-invoke | manual | executes exactly an approved plan's calls; only reachable behind an approval node |

Workflows: `observer` (observe → review → human gate) and `certification-plan`
(plan → review → verdict condition → human gate → apply by `plan-executor`).
Builtins cannot be retired; evolve them by publishing a new version.

The observer's schedule spends real tokens: roughly 15k to 30k input tokens per wake on
the configured model, every 15 minutes, unattended. To stop it: **Pause agents** on the
Agents page (nothing is scheduled while paused), publish an `observer` version without
the schedule trigger, or set a daily token `budget` on the spec (hard stop, recorded as
`budget_exceeded`).

## 3. One heartbeat, end to end

```
POST /agents/{name}/wake {"input": "...", "version": null, "wake": "manual"}
  → 202 {status: running}      the row; poll GET /heartbeats/{id}
  → 200 {coalesced: true}      the agent already had a running heartbeat (you get that one)
  → 200 {status: paused | budget_exceeded}   refused and recorded, never ran
```

What runs: `runner.run_heartbeat` builds the conversation (registered instructions +
mode preamble + untrusted-data note; your input is a *user* message), then loops LLM
turn → `scoped_dispatch` per tool call → record, until a final answer or a limit
(`max_steps`, `max_tokens`, `wall_clock_s`, cancel, pause). The record holds `steps`
(every LLM turn and tool call with ms), `proposed` (plan-mode writes, not executed),
`journal` (executed writes, revertable), `result` (the final answer), `error`, tokens,
model, `spec_sha256` (provenance to the exact published version).

**Reading the output:** the run report (Run monitor → run → "agent verdict,
advisory" panel: every finished heartbeat whose `subject` is `run:<that id>`,
so `failure-triage` woken by `run.failed` shows up on the run it triaged);
Agents page → agent → Heartbeats → row (waterfall + result);
`GET /api/agents/heartbeats?agent=observer` then `/heartbeats/{id}`; MCP
`get_heartbeat` (a `plan`-mode agent's proposed calls: `list_agent_plans` /
`get_agent_plan`); or push via the alert webhook (§6). A run's sign-off
(`POST /runs/{id}/certify`) freezes the same verdicts into the snapshot as
`annotations.agent_verdicts`, shown in the printable document and on the sign-off page
under "Agent verdicts (advisory)": not a gate input, outside the content hash, and
empty with a reason when agent-hub was unset or unreachable. Advisors answer as JSON findings
inside a markdown report; `extract_json` finds the fenced block, so `${node.json}` and
the alert parser both work on real model output.

**Post-checks (the platform corrects the model):** after the loop, a `done` answer that
is a JSON object with `run_id` and `regression` is checked against the orchestrator's
run history (`GET /runs/{id}/regression`, the toolkit's `get_run_regression`). The
field is overwritten with the history's answer, `regression_evidence` (verdict,
the model's original `claimed`, the failed scenarios' prior outcomes) is added, and a
step of kind `postcheck` lands on the heartbeat (`corrected` / `confirmed` /
`no evidence` in the waterfall). `first_run` and `never_passed` are not regressions;
a scenario is one only when it passed in an earlier run. No evidence keeps the
model's claim as written and says so.

**Cancel / revert:** `POST /heartbeats/{id}/cancel` (stops before the next LLM or tool
call; rbac.invoke or admin). `POST /heartbeats/{id}/revert` (admin) restores every
journalled write newest-first under *your* token: reverting is the human's act.

## 4. Workflows and the approvals inbox

```
POST /workflows/{name}/run {"inputs": {...}}   → 202 run (admin-class role)
GET  /runs?workflow=&status=   GET /runs/{id}   POST /runs/{id}/cancel
GET  /approvals[?status=pending|all]           POST /approvals/{id}/decide {"decision": "approved"|"rejected", "note"}
GET  /plans[?run=]  GET /plans/{id}
```

A run's `node_states` and `results` are the whole state; a killed container resumes
every active run from its row at startup. A node becomes ready when all incoming edges
are resolved and at least one fired; unfired nodes are `skipped`. `condition` branches
on `when: true|false`; `approval` parks the run as `waiting`, alerts `approval.requested`,
and follows `approved` unless a `when: rejected` edge exists (else the run ends
`rejected`); `timeout_s` expires on a 30 s tick and fails the run. Deciding needs one of
the node's roles or admin and is recorded with the decider. Deciding is a portal act:
there is deliberately no MCP tool for it.

Guardrails at publish time (`validate.py`): unknown tools, advisor with write tools, a
node escalating an agent's mode, a `full` task (or a write/execute `tool` node) outside
`mock` without an approval ancestor (D3), executor = reviewer, bad edge labels.

## 5. Every way an agent wakes

| Source | Who | How |
|---|---|---|
| Portal "Wake now" / `POST /agents/{name}/wake` | a user with a role in the agent's `rbac.invoke` (or admin) | `wake=manual`, OBO JWT of the user (`act` claim, never `svc`) |
| MCP `wake_agent`, `run_workflow` | an MCP client (Claude Code, Claude Desktop) via the MCP server's `svc: mcp-server` JWT | `wake=mcp` |
| Schedule | agent-hub's own tick (30 s cadence, `AGENT_HUB_SCHEDULER=0` off) | `wake=schedule`, principal `scheduler`; `interval_sec` or `daily_at` (UTC); never while paused |
| Platform events | the orchestrator posts `run.completed` / `run.failed` / `gate.failed` to `POST /events` when `AGENT_HUB_API_URL` is set | `wake=event`, principal `event:<name>`, every agent with a matching `event` trigger |
| Inbound webhook | any system holding `AGENT_HUB_WEBHOOK_SECRET` | `POST /webhooks/events/{event}` or `/webhooks/agents/{name}` (opt-in `webhook` trigger), body signed `X-PayProbe-Signature: t=<ts>,v1=<HMAC-SHA256("<ts>.<body>")>`; 503 while no secret is set |

Event- and webhook-woken agents act under a principal with no roles: an advisor reads
fine; any write is refused downstream by ordinary RBAC until a workflow with an approval
carries a human's authority. Wakes on a busy agent coalesce onto its running heartbeat.

Signing a webhook from a shell:

```bash
body='{"run_id":"nightly-42","status":"failed"}'; ts=$(date +%s)
sig=$(printf '%s.%s' "$ts" "$body" | openssl dgst -sha256 -hmac "$AGENT_HUB_WEBHOOK_SECRET" | awk '{print $2}')
curl -X POST http://localhost:8080/api/agents/webhooks/events/run.failed \
  -H "X-PayProbe-Signature: t=$ts,v1=$sig" -H 'Content-Type: application/json' -d "$body"
```

## 6. Getting output to a human without looking: the alert webhook

Set `AGENT_HUB_ALERT_WEBHOOK_URL` (and `_SECRET`) and agent-hub POSTs signed JSON
(`X-PayProbe-Event`, `X-PayProbe-Signature` in the same `t=,v1=` scheme) on every
`heartbeat.failed` / `heartbeat.budget_exceeded` / `heartbeat.timed_out` (refusals and
restart orphans included), every advisor finding with severity `warn` or above
(`finding`), every `approval.requested` and `run.failed`. Fire-and-forget, 3 attempts
with 1 s / 4 s backoff, 4xx final; never in the heartbeat's path. `/health.alerts` shows
sent / failed / recent. Without a URL, findings wait in the heartbeat log.

## 7. The safety model (all in machinery, none in prompts)

1. **Allowlist** per agent, validated against the one toolkit registry at publish; a
   tool the model names outside it is refused (`guardrail: true`) and recorded.
2. **Mode tiers**: advisor = read; plan = writes become `proposed`; full = writes execute
   inside `write_scope` (projects, environments; `*` = any), else refused. A `full`
   heartbeat also needs a human behind it: a user with an invoke role, or an approved
   workflow gate on the executed path. Service tokens (static, `svc`), event, schedule
   and webhook wakes get a recorded `failed` refusal; a `full` agent cannot even be
   published with an unattended trigger.
3. **Untrusted envelope**: every read and execute result (runtime state *and* registry
   content, since 2026-09-24) reaches the model as `{"kind": "untrusted", "source",
   "data"}`; the runner never executes tool calls that appear inside tool results.
4. **Result cap** 64 KB before the model sees it, and **secret masking** before that:
   any value under a secret-named key (`password`, `api_key`, `*_secret`, ...) is
   `<secret:fingerprint>` to the model and in every heartbeat record the API returns;
   the journal keeps the real value for restore, SecretBox-encrypted at rest when
   `PAYPROBE_SECRET_KEY` is set.
5. **Journal + revert** for every executed write (invariant #2).
6. **Human gates**: D3 at publish (an approval's `approved` edge on *every* path to a
   full task or write tool node) and again in the engine over the edges that fired; a
   forged upstream `{"decision": "approved"}` changes nothing, a gate a condition
   skipped gates nothing, and an agent republished as `full` after the workflow was
   validated fails its node instead of writing. Deciding, reverting and pausing are a
   human's act: a service token is 403 there; an on-behalf-of token is 401 everywhere.
7. **Egress allowlist**: a prompt may only go to `api.openai.com`, `api.anthropic.com`,
   the host of `ASSIST_LLM_BASE_URL`, or `AGENT_HUB_EGRESS_ALLOW` entries (https unless
   listed); otherwise the heartbeat fails with `egress refused` and nothing is sent.
8. **Pause** (`PUT /pause`, Agents page button): checked before every LLM and tool call,
   including workflow `tool` nodes.
9. **Limits and budget** per heartbeat and per day; **coalescing** (one running
   heartbeat per agent); **restart watchdog** (`orphaned by restart`). **Hub-wide
   quotas** on top (`/health.quotas`; `0` = off): `AGENT_HUB_DAILY_TOKENS` (default 5M,
   every agent on one ledger; refused as `budget_exceeded`), `AGENT_HUB_MAX_CONCURRENT`
   (default 4 running heartbeats; refused as `quota_exceeded`, schedules retry next tick,
   an event wake is lost and the row says so) and `AGENT_LOAD_APPROVAL_TPS` (default 100:
   a heartbeat's `start_load_run` above that peak rate is refused by the tool layer;
   heavier load is a workflow `tool` node behind an `approval`). Every builtin seed
   carries `budget.daily_tokens` (observer 3M, failure-triage 1M, plan-executor 300k,
   others 500k); a registry seeded before 2026-09-23 keeps `budget: null` on its v1
   builtins until you publish a v2.
10. **Deterministic post-checks** (`agent_hub/postcheck.py`): where the platform holds
    the evidence it overrides the answer (today: `regression` vs run history), keeping
    the model's claim beside it. Advice stays advice; facts come from the registry.

The proof is `tests/test_hub_injection.py` (hostile results, an obedient model, plan
and full modes, size, wake input, forged approvals) and `tests/test_hub_egress.py`.

## 8. Symptom → cause

| Symptom | Cause / action |
|---|---|
| Agents page: "agent-hub is not reachable" | agent-hub down, or nginx conf without `/api/agents/` (all three confs carry it since 2026-09-23); `curl localhost:8080/api/agents/health` |
| Wake toast "no LLM provider configured" (503) | set the key: Settings → AI assistant, or `ASSIST_LLM_*` env (env wins); agent-hub caches Settings ~15 s |
| Heartbeat `failed`, error `llm: RuntimeError: HTTP 400 ... credit balance` | provider account out of credits; every scheduled wake keeps failing (and would alert) until topped up or paused |
| Heartbeat `failed`, `egress refused: host ...` | provider `base_url` outside the allowlist (§7.7); check Settings → AI assistant and `AGENT_HUB_EGRESS_ALLOW` |
| Wake returns 200 `coalesced: true` | the agent already has a running heartbeat; workflow nodes retry every 5 s |
| Rows stuck `running` after a restart | the watchdog marks rows past `wall_clock_s` + 60 s as `failed` / `orphaned by restart` at startup; inside the wall clock they are left alone |
| `budget_exceeded` without running | daily token budget spent (hard stop) or `max_tokens` / `max_steps` inside the wake; see `error` |
| Whole test suite "N skipped" in one combined session | agent-hub's conftest skips every test when its Postgres is unreachable; run per package, forward 5432 (compose does not publish it) |
| Registry or heartbeat history vanished after running tests | the suite truncates the database it points at; it defaults to `payprobe_test` (created on demand) since 2026-09-23, so check `AGENT_HUB_TEST_DATABASE_URL` is not the platform's `payprobe` database. Builtins are re-seeded on the next start; user-created definitions and heartbeats are not recoverable |
| Approval never decided, run `failed` "approval timed out" | `timeout_s` elapsed on the 30 s tick; rerun the workflow |
| Wake returns 200 `failed`, error "full mode needs a human behind the wake" | the caller was a service token or an event / schedule / webhook principal; wake it from the portal as a user with the invoke role, or put it behind an approval in a workflow |
| Node `failed` "no approved gate is on the executed path" | the run reached a `full` task or write tool node on a path with no `approved` decision (a skipped or rejected gate, or an agent republished as `full`); fix the workflow so every path crosses a gate |
| Publish 403 "publishing a wider grant needs an admin" | an `rbac.edit` holder tried to grow mode, tools, write scope, rbac, triggers, budget or limits; an admin publishes that version |
| Event never woke anyone | orchestrator lacks `AGENT_HUB_API_URL`, or no active agent declares that `event` trigger (`GET /agents/{name}` → spec.triggers) |

## 9. Adding a builtin agent or workflow

1. Add the spec to `SEEDS` (or `WORKFLOW_SEEDS`) in `packages/agent-hub/agent_hub/seed.py`;
   tools must exist in `payprobe_common/agent_toolkit.py` (seeding fails loudly otherwise).
2. Add an assertion in `tests/test_hub_api.py` (mode, tiers, triggers) or
   `tests/test_hub_engine.py` (workflow validates and runs under FakeLLM).
3. `cd packages && python3 -m pytest agent-hub/tests -q` with Postgres reachable.
4. Update the seed lists in the ADR (§Design, Seeds) and this skill's §2.
5. Rebuild agent-hub; `seed_builtin` adds the missing builtin on start and leaves
   existing definitions untouched (operators own them after the first start).

## Provenance and maintenance

Verified 2026-09-23 against `packages/agent-hub/agent_hub/{main,runner,engine,triggers,
alerts,egress,seed,validate,store}.py`, the three compose files and nginx confs, and a
live stack (first real scheduled `observer` wake on Anthropic Haiku, MCP tools driven
from inside the mcp-server container). Re-verify before trusting:

```bash
# routes
grep -n '@app\.\(get\|post\|put\|delete\)' packages/agent-hub/agent_hub/main.py
# seeds and their triggers
grep -n '"role"\|"mode"\|"kind"' packages/agent-hub/agent_hub/seed.py
# knobs actually read
grep -rhoE 'environ\.get\(\s*"[A-Z_]+"' packages/agent-hub/agent_hub | sort -u
# schema version + tables
grep -n 'CREATE TABLE IF NOT EXISTS' packages/agent-hub/agent_hub/store.py
# test count (needs Postgres at AGENT_HUB_TEST_DATABASE_URL)
cd packages && python3 -m pytest agent-hub/tests -q
# what the running service reports
curl -s localhost:8600/health
```

Volatile: the test count, the observer's schedule interval and model, whether the
`assistant` alias container still exists (phase 5 removes it), and the owed items listed
in the ADR's Rollout section.
