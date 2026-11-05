---
name: payprobe-diagnostics-and-tooling
description: >
  Measure, don't eyeball: every PayProbe diagnostic tool with an interpretation
  guide plus ready-to-run scripts. Load this when you need to answer "is the
  platform healthy?", "why can't X reach Y?", "why did this run fail?", "is this
  test flaky or broken?", "did performance regress?", "did the client survive
  chaos?", "what exactly went over the wire?", or "where did this transaction
  go?" — i.e. whenever you are about to guess at a cause instead of measuring
  it. Covers GET /diagnostics (platform doctor), /runs/{id}/diagnose (failure
  taxonomy), /runs/flakiness, /runs/trend, run compare, /load-runs/{id}/compare,
  resilience certification scoring, Prometheus /metrics + Grafana, execution
  trace (wire bytes + engine log + waterfall), network trace, /peers, the ISO
  8583 inspector, and the MCP diagnostic tools. NOT for fixing what you found
  (payprobe-debugging-playbook) or for pass/fail evidence standards
  (payprobe-validation-and-qa).
---

# PayProbe diagnostics and tooling

The house rule is **measure, never assume** — no fix ships without a measured
root cause. This skill is the toolbox that makes measuring cheaper than
guessing: every diagnostic surface in the platform, what its output means, and
executable helpers in `scripts/`.

All commands are repo-root-relative. All facts below were verified against the
code on 2026-07-03; the "Provenance and maintenance" section at the end has
one-line re-verification commands.

## Setup: URLs and auth

Default ports (from `infra/docker/docker-compose.yml`):

| Service | Base URL | Notes |
|---|---|---|
| orchestrator | `http://localhost:8100` | runs, load runs, simulators, diagnostics |
| scenario-service | `http://localhost:8000` | scenarios, connections, ISO 8583 inspector |
| auth-service | `http://localhost:8300` | mints JWTs (`POST /token`) |
| mcp-server | `http://localhost:8200` | MCP Streamable HTTP at `/mcp`, liveness at `/healthz` |
| assistant | `http://localhost:8600/assistant` | config assistant, mounted inside agent-hub (ADR-0010 D2; no :8400 container) |
| portal | `http://localhost:8080` | UI (Diagnostics, Trends, run reports, Network Trace, Peers pages) |

Auth (orchestrator `api/auth.py`, scenario-service `api/auth.py` — same model):

- **Always public, never need a token:** `/health`, `/ready`, `/metrics`,
  `/status`, `/reference`, `/openapi.json`, `/docs`, `/redoc`.
- Everything else (including `/diagnostics` and all `/runs/*`) goes through a
  **fail-closed** gate: open only when `PAYPROBE_ENV` is `dev`/`development`/
  `test`/`local` *and* no credential is configured; otherwise you need
  `Authorization: Bearer <token>` (static `API_TOKEN` or a JWT).
- Get a JWT: `curl -s -X POST http://localhost:8300/token -d username=admin -d password=<pw> | jq -r .access_token`

Every script in `scripts/` honors `ORCH_URL` (default `http://localhost:8100`)
and `TOKEN` (optional bearer; omit in open dev mode).

## Tool map — pick by question

| Question | Tool | Where |
|---|---|---|
| Is the platform up at all? | `GET /status` (public) | orchestrator |
| Can this replica serve traffic? | `GET /ready` (503 = no) | orchestrator |
| Why can't X reach Y? | `GET /diagnostics` platform doctor | orchestrator |
| Why did this run fail? | `GET /runs/{id}/diagnose` | orchestrator |
| Is this scenario flaky or broken? | `GET /runs/flakiness` | orchestrator |
| Getting better or worse over days? | `GET /runs/trend` | orchestrator |
| What changed vs the last run? | `GET /runs/{id}/compare` | orchestrator |
| Did load performance regress? | `GET /load-runs/{id}/compare` | orchestrator |
| Does the client survive chaos? | `POST /resilience/runs` + scorer | orchestrator |
| What went over the wire, step by step? | run detail trace (`GET /runs/{id}`) | orchestrator / portal Trace tab |
| Where did this transaction travel? | `GET /participants/traces` | orchestrator |
| Who is connected right now? | `GET /peers` | orchestrator |
| Is this ISO 8583 message well-formed? | `POST /iso8583/analyze` | scenario-service |
| Continuous metrics / alerting | `/metrics` + observability compose profile | all services + `infra/` |

Rule of thumb for connectivity questions, from broad to narrow:
`/status` (service pulse) → `/diagnostics` (whole stack, cross-correlated) →
`/connections/test` (one link) → `/runs/{id}/diagnose` (one finished run).

---

## 1. GET /diagnostics — the platform doctor

One layered pass over every hop that can break, with a concrete fix hint per
failure. Engine: `packages/orchestrator/api/diagnostics.py`; endpoint wiring in
`packages/orchestrator/api/main.py`.

```bash
curl -s -H "Authorization: Bearer $TOKEN" "$ORCH_URL/diagnostics" | jq .
# scope it:
curl -s -H "Authorization: Bearer $TOKEN" "$ORCH_URL/diagnostics?layers=connections,listeners"
curl -s -H "Authorization: Bearer $TOKEN" "$ORCH_URL/diagnostics?connection=visa&environment=mock"
```

Or: `scripts/payprobe-doctor.sh` (pretty-prints only the problems + hints).
Portal: **Diagnostics** page. MCP: `diagnose_platform`.

Four layers, each check `{id, layer, name, target, status, latency_ms, detail,
error, hint}` with `status ∈ ok|warn|fail|skip|disabled`:

| Layer | What it checks | Typical failure it catches |
|---|---|---|
| `services` | scenario-service, auth-service, Redis PING, optional MCP/assistant, run store | dead container, wrong `SCENARIO_API_URL`, Redis down |
| `connections` | every saved connection, staged: config sanity → DNS → live adapter probe (env overrides applied first — it tests what a run would actually dial); participant-group member sanity | missing host/port, hostname typo / Docker-vs-localhost mixup, dead target, wrong credentials, group members missing/disabled |
| `listeners` | every running simulator/participant listener really accepts on its port | listener registered but crashed / failed to bind |
| `runs` | last 20 runs' connectivity-class step errors, bucketed by taxonomy and cross-linked to live connection state | "recent runs failed 'unreachable' against visa AND visa's probe fails right now" — two mysteries become one answer |

**Interpretation:**

- Top-level `status`: `ok` (no warn/fail), `degraded` (warns only), `failing`
  (any fail). `summary` gives counts per status.
- Read `fail` checks first, in layer order — a `services` fail (e.g. Redis
  down) explains cascading fails below it. Connection stages short-circuit:
  a config fail means DNS/probe were never attempted, so the *first* failing
  stage is the real problem, not the deepest.
- `hint` is the next action, not a restatement. Two hints worth trusting:
  the localhost cross-check ("dials localhost:5010 but nothing listens there"
  → start the listener or fix the port), and "TCP connect worked but the
  sign-on/health exchange failed" → wrong adapter family or dialect mismatch,
  NOT a network problem.
- `skip`/`disabled` are intentional posture (no connections saved, Redis
  single-node mode) — they never degrade the verdict.
- Checks in the `runs` layer carry a `runs` array of affected run ids —
  follow up with `/runs/{id}/diagnose` on one of them.

**Good output:** `status: "ok"`, every check `ok`/`skip`/`disabled`, service
latencies single-digit-to-low-hundreds ms. **Bad:** any `fail`; a `warn` on a
participant group ("unusable members") means the fleet is silently smaller
than configured — fix before trusting load numbers.

## 2. GET /runs/{id}/diagnose — run failure taxonomy

Turns a finished (or live load) run into ranked findings `{code, severity,
title, cause, suggestion, evidence}`. Pure logic in
`packages/report_service/diagnose.py` (`classify_error`, `diagnose_run`,
`diagnose_load`). MCP: `diagnose_run`.

```bash
curl -s -H "Authorization: Bearer $TOKEN" "$ORCH_URL/runs/$RUN_ID/diagnose" | jq '{headline, ok, findings: [.findings[] | {code, severity, title, suggestion}]}'
```

The taxonomy — what each verdict means and the next step:

| Category | Matched error text (essence) | Meaning | Next step |
|---|---|---|---|
| `unreachable` | refused / reset / no route / cannot connect / name not known | Nothing accepted the connection — target down or wrong host/port | Start the target (Simulators page) or fix the Connection; confirm with `/diagnostics?connection=<name>` |
| `timeout` | timed out / deadline exceeded | Connected but no answer in time — firewall drop, hung target, or overload | Raise timeout only after checking target health; under load this usually means the target is the bottleneck |
| `auth` | 401 / 403 / unauthorized / invalid token | Target rejected credentials | Fix the Connection's key/secret (check the environment override too) |
| `assertion` | assertion / expected…got / response_code / did not match | The link works; the *response content* mismatched | Functional issue, not connectivity — verify expected values or fix upstream data (evidence bar: see payprobe-validation-and-qa) |
| `tls` | tls / ssl / certificate / handshake | Handshake failed | Check http vs https, cert validity, client-cert requirement |
| `binding` | no connection / not bound / unknown target / not configured | Scenario target isn't bound to a real endpoint in this environment | Attach a Connection or pick an environment that defines it (mock for a dry run) |
| `reference` | unresolved reference / unknown variable | A `${step.response.field}` points at data that doesn't exist at run time | Open the Trace tab, find the *referenced* step: did it run, succeed, and return that field? Authoring problem, not network |
| `url` | no usable base_url / missing http(s):// | Malformed/empty URL — adapter had nothing valid to dial | Set the connection's `base_url` (or fill the `*_base_url` variable it interpolates) |
| `error` / `unknown` | anything else / no message | Unclassified | Read the raw error and the run trace |

Load-run findings (from `diagnose_load`), with their exact triggers:

| Code | Trigger (in code) | Meaning |
|---|---|---|
| `no_workers` | workers expected > 0 but `workers_reporting == 0` | No load was generated at all — start the worker fleet (`LOAD_RUN_ID=<id> python -m worker.load_worker`) |
| `all_failing_<cat>` | `sent > 0`, `received == 0`, `errors > 0` | Every transaction failed; `<cat>` is the taxonomy class of `last_error` |
| `partial_failures_<cat>` | error rate ≥ **20%** | Elevated failures, same taxonomy drill-down |
| `below_target` | achieved TPS < **0.6 ×** target with `pending > 0` | The target or network is the bottleneck, not the generator |
| `healthy` | none of the above | No action needed |

**Doctor ride-along:** when a finding is connectivity-class, the endpoint also
runs a scoped doctor pass (`connections` + `listeners`) and attaches its
problems under `doctor` — "this failed because visa was unreachable, and visa
is STILL down". If `doctor.problems` is empty, the outage was transient.

## 3. GET /runs/flakiness — intermittent scenarios

`packages/orchestrator/api/run_store.py::flakiness()`. Portal: Trends page
"Flaky scenarios" card. MCP: `run_flakiness`.

```bash
curl -s -H "Authorization: Bearer $TOKEN" "$ORCH_URL/runs/flakiness?days=30&min_runs=3" | jq .
# or: scripts/flakiness-report.sh 30
```

Definition (exact, from code): for each scenario seen ≥ `min_runs` times
(default 3) in the window, take its time-ordered pass/fail sequence. A
scenario is flaky **only if it both passed and failed** — always-pass is
stable, always-fail is a *regression* (shows up in trend/compare instead).
`flips` = count of consecutive-run result changes;
**`score` = flips / (runs − 1)**, in 0..1.

**Interpretation:**

- `score = 1.0` — alternates every single run: almost certainly ordering,
  shared-state, or timing dependent, not a real product bug.
- A single blip in many runs scores low (e.g. 1 flip in 10 runs = 0.11) — check
  `last_status`: if `failed`, it may be a fresh regression that just started,
  not flakiness.
- High `score` + roughly even `passed`/`failed` split is the classic
  race/timeout signature. (Bands like "≥0.5 = severe" are guidance, not code.)
- Empty result ≠ all good — it means nothing *flipped*. Pair with `/runs/trend`
  to catch stable-but-failing scenarios.
- Known failures may not accumulate (house rule): a flaky scenario is work to
  schedule, not noise to ignore.

## 4. GET /runs/trend — daily regression health

`run_store.trend()`: per-day buckets `{date, runs, passed, failed,
scenarios_total, scenarios_passed, pass_rate}` (last `days` buckets *with
data*; `pass_rate` = scenario-level, rounded to 4 places, `null` on days with
no scenario counts). MCP: `run_trend`.

```bash
curl -s -H "Authorization: Bearer $TOKEN" "$ORCH_URL/runs/trend?days=30&label=nightly" | jq .
```

**Interpretation:** watch `pass_rate` direction, not single days. A step-change
down that persists = a regression landed that day (bisect with
`/runs/{id}/compare`). Sawtooth pass_rate with flat run counts = flakiness —
cross-check section 3. Use `label=` to keep like-for-like (e.g. only the
nightly schedule).

## 5. GET /runs/{id}/compare — run-vs-run functional diff

Diffs per-step statuses against a base run (default: previous run with the
same `label`, falling back to the previous run of any label). MCP:
`compare_runs`.

```bash
curl -s -H "Authorization: Bearer $TOKEN" "$ORCH_URL/runs/$RUN_ID/compare" | jq '{base_run_id, base_found, summary}'
```

Change kinds: `regressed` (was passing → now failing) — the only one that
blocks; `fixed` (failing → passing); `changed` (e.g. failed → error);
`added` / `removed` (scenario set drifted — if unexpected, your comparison is
not like-for-like and the counts are noise). Always check `base_found: true`
and that `base_run_id` is the run you think it is before trusting the verdict.

## 6. GET /load-runs/{id}/compare — performance regression verdict

Diffs a load run against a base (default: previous finished load run with the
same label; load labels carry a `load:` prefix so it never falls back to a
functional run). Implementation: `_compare_load_summaries` in
`packages/orchestrator/api/main.py`. MCP: `compare_load_runs`. Portal: "vs
previous run" panel on the Load page.

```bash
curl -s -H "Authorization: Bearer $TOKEN" "$ORCH_URL/load-runs/$RUN_ID/compare" | jq '{base_run_id, summary, deltas}'
```

Six deltas, each `{current, base, delta, pct, direction, regressed, improved}`:

| Metric | Worse when | Notes |
|---|---|---|
| `latency_p50` / `latency_p95` / `latency_p99` | up | p99 moves first under saturation |
| `error_rate` | up | errors / (errors + received) |
| `tps` | **down** | achieved throughput |
| `tps_cv` | up | throughput stability (see below) |

**Dead-band:** changes under **2% relative** (`eps = 0.02`) read as `flat` —
never `regressed`/`improved` — so sub-2% jitter can't cry wolf.
`summary.regressions` / `summary.improvements` count metrics outside the band.

**How to read a regression verdict:**

- `regressions ≥ 1` with `error_rate` up → look at `error_categories` (list of
  `{category, current, base, delta}`, taxonomy names from section 2): a new or
  growing category names the failure mode (e.g. `timeout` grew = target
  saturating; `unreachable` appeared = something died mid-run).
- `tps` down + latencies up + `error_rate` flat → the target got slower, the
  client is fine.
- `tps_cv` up alone → same average throughput but unstable delivery.
  `tps_stability` (persisted on the run summary) = `{mean, stdev, cv, min,
  max, samples}` over the per-second `tps_series`, leading warm-up zeros
  trimmed. `cv` = stdev/mean, unit-free; 0.0 is perfectly flat, and an
  interior dropout shows as `min` far below `mean` even when `mean` looks
  fine. (Exact bands are guidance: single-digit-% cv is steady.)
- `base_found: false` → no verdict, only `current` values. Pick a base
  explicitly with `?to=<run_id>`.

## 7. Resilience certification — /resilience/runs

Scores whether a *client* survives injected chaos. Scorer:
`packages/orchestrator/api/resilience.py` (pure, unit-tested); endpoints
`GET/POST /resilience/runs`, `GET /resilience/runs/{rid}`. Portal:
**/resilience** page. Prereqs: a **running load run** (`load_run_id`) and a
**running chaos-capable simulator** (`target_sim_id`) — the chaos dial lives
at `GET/PUT /simulators/{sid}/chaos` and storms at
`POST /simulators/{sid}/chaos/storm`. On a shared deployment, chaos on a
simulator that other runs/schedules depend on is behavior-changing — coordinate
per `payprobe-change-control`.

Three sampled stages: `baseline` (calm) → `storm` (chaos on) → `recovery`
(chaos lifted). Per-second cumulative samples feed four component scores:

| Component | Weight | Measures |
|---|---|---|
| `availability` | 0.35 | storm success rate as a fraction of baseline success rate |
| `absorption` | 0.30 | injected faults the client recovered from (retry/reconnect): `1 − error_rate/fault_rate` during the storm |
| `recovery` | 0.25 | post-storm success rate vs baseline |
| `latency` | 0.10 | storm p95 between baseline p95 (full marks) and the ceiling (zero) |

Hard gates (any failure ⇒ FAIL regardless of score; defaults, tunable via the
request's `thresholds`):

| Gate | Passes when | What a failure means |
|---|---|---|
| `availability` | storm success ≥ baseline × **0.90** | client lost >10% of its success rate under chaos |
| `no_wedge` | NOT (sim answered some requests cleanly AND client got nothing through) | the client wedged — hung connections, no failover |
| `recovery` | recovery success ≥ baseline × **0.98** | client did not heal after the storm passed — the worst verdict (leaked sockets, poisoned pools) |
| `latency` | storm p95 ≤ baseline p95 × **4.0** | latency blew through the ceiling |

**Verdict:** `PASS` iff overall score ≥ **70** (`pass_score`) AND no gate
failed. Score = weighted component sum, 0–100. Grades: A+ ≥95, A ≥90, B ≥80,
C ≥70, D ≥55, else F.

**Interpretation:** read `blocking` (failed gate ids) before the grade — a B
with a failed `recovery` gate is a FAIL and worse than a plain C. Check
`notes`: "no faults were injected during the storm stage" or "no client
traffic recorded" means the certificate measured nothing — fix the storm
config / load run and re-run rather than quoting the number. Component
`absorption` mirrors `availability` when no faults landed (neutral, not
earned).

## 8. Prometheus /metrics + Grafana

Every service exposes `/metrics` (Prometheus text format, public). Orchestrator
series are defined in `packages/orchestrator/api/observability.py`; the full
operator guide is `infra/OBSERVABILITY.md`.

```bash
# spot-check without Prometheus:
curl -s "$ORCH_URL/metrics" | grep '^payprobe_' | head -30
# bring up Prometheus (:9090) + Grafana (:3000, admin/admin):
docker compose -f infra/docker/docker-compose.yml --profile observability up
```

Key metric names (grep-able):

| Metric | Labels | Reading it |
|---|---|---|
| `payprobe_http_requests_total` | method, route, code | request rate + error codes per route |
| `payprobe_http_request_duration_seconds` | route | service latency |
| `payprobe_http_inflight_requests` | — | concurrency right now |
| `payprobe_runs_inflight` / `payprobe_runs_total` | — / status | scenario-run load and outcomes |
| `payprobe_load_runs_inflight` | — | active load runs on this replica |
| `payprobe_load_run_tps` | run_id | achieved throughput, live |
| `payprobe_load_run_errors` | run_id | cumulative errors, live |
| `payprobe_load_run_workers_reporting` | run_id | fleet liveness — fewer than expected ⇒ fleet not fully up |
| `payprobe_load_worker_rss_bytes` | run_id, worker_id | per-worker resident memory — the soak leak signal |
| `payprobe_simulator_up` / `_messages_received` / `_rps` / `_faults` | sim_id, label | simulator liveness, traffic, chaos faults injected |

**Interpretation shortcuts** (from `infra/OBSERVABILITY.md`):
`workers_reporting < expected` ⇒ fleet not fully up; errors rising with tps
flat ⇒ the target is rejecting. Soak/leak: a clean cyclic soak's RSS
saw-tooths and its 10-minute growth rate averages ~0; a monotonic climb trips
the `WorkerMemoryLeak` alert (`infra/prometheus/rules/payprobe-soak.rules.yml`).
Grafana auto-provisions "PayProbe — Load & Service Health" plus a simulators
dashboard (`infra/grafana/provisioning/dashboards/`). Scrape targets:
`infra/prometheus/prometheus.yml` (orchestrator:8100, scenario-service:8000,
auth-service:8300; workers not scraped yet — roadmap).

Optional tracing: `init_tracing()` is a no-op unless the OTel SDK is installed
AND `OTEL_EXPORTER_OTLP_ENDPOINT` is set.

## 9. Execution trace — wire bytes + engine log + waterfall

Every step outcome carries (defined in `packages/worker/engine/runner.py::StepOutcome`):

- `started_at_ms` (epoch ms) + `duration_ms` — lay steps on a shared timeline;
  the portal Trace tab renders this as the timing waterfall.
- `raw_log` — adapter-provided wire detail (e.g. exact ISO 8583 bytes
  sent/received), secret-redacted before it leaves the worker.
- `trace` — structured engine-log lines `{level, msg}` with levels `info`
  (dispatch/response), `debug` (request/response payloads), `wire` (raw_log
  folded in), `pass`/`fail` (per assertion, with expected → actual), `error`.

Where to get it: `GET /runs/{id}` (the full run detail JSON contains all of
it, under `summary.scenarios[].steps[]`), or portal run report → **Trace**
tab → **⤓ Trace JSON** export. `scripts/collect-run-bundle.sh` extracts a
standalone `trace.json` for you.

**How to read it:** find the first `fail`/`error` line — everything after is
usually consequence. For an `assertion` verdict, the `pass|fail` lines show
`assert <field> <op> <expected> → <actual>` — the actual value came off the
wire, so compare it with the `wire` lines to decide whether the *target*
returned the wrong thing or the *scenario* expected the wrong thing. For a
`reference` verdict, walk back to the referenced step's `debug` response
payload line and check the field really exists. Gaps in the waterfall (step
start ≫ previous step end) are orchestration/queueing time, not target time.

## 10. Network trace — /participants/traces

Cross-hop, per-transaction trace across the participant-flow network (a
correlation id ties hops together; for ISO 8583 that's derived from the
message, e.g. searchable by STAN). Portal: **Network Trace** page.

```bash
curl -s -H "Authorization: Bearer $TOKEN" "$ORCH_URL/participants/traces?limit=50&q=000123" | jq .
curl -s -H "Authorization: Bearer $TOKEN" "$ORCH_URL/participants/trace/$CID" | jq .
```

Index rows: `{correlation_id, ts, mti, kind, flows[], hops, ok}` — `ok:false`
means at least one hop failed. Detail: every hop tagged with that correlation
id across all live listeners, time-ordered, each hop including its downstream
`calls`.

**Interpretation:** `ok:false` → open the detail and find the first failing
hop — failed *downstream* hops are preserved in the flow trace, so a missing
reply from the issuer shows as a failed call on the switch hop, not as
silence. Fewer `hops` than your topology has participants = the message never
reached the later legs (cross-check `/diagnostics` listeners layer). Traces
live in memory on the listeners: `DELETE /participants/traces` clears them for
a clean experiment window.

## 11. GET /peers — who is connected right now

Live Sessions view: every inbound client socket connected to a listener we
host (simulators + participant flows), plus the outbound upstream legs of
transparent proxies. Per-run engine adapter sockets in the worker are NOT
reported (known limitation, in code docstring). Portal: **/peers** page.
Per-simulator counters: `GET /simulators/{sid}/metrics`.

```bash
curl -s -H "Authorization: Bearer $TOKEN" "$ORCH_URL/peers" | jq '{counts, inbound: [.inbound[] | {peer, label, local_port, protocol}]}'
```

**Interpretation:** an expected client absent from `inbound` = the client side
never connected — go to `/diagnostics` (its dial is failing) rather than
staring at the listener. Persistent-connection protocols (ISO 8583 over TCP)
should show long-lived peers; a churn of short-lived entries for the same
source is a reconnect loop (guidance: check the client's timeout vs the
simulator's chaos/latency settings).

## 12. ISO 8583 inspector — analyze / build / diff

Scenario-service endpoints (`packages/scenario-service/api/main.py`), also on
MCP as `iso8583_analyze` / `iso8583_build` / `iso8583_diff` /
`iso8583_tlv_build`. Portal: Inspector page. Default field table is the 1987
dialect; pass `fields` (a `{de: {name,len_type,length,type}}` table) or a
saved Message Format's fields for other dialects; `encoding` accepts
`"ascii"`, `"binary"`, or a fine-grained dict — binary messages travel as hex
strings.

```bash
# decode + validate a wire message:
curl -s -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -X POST "$SCENARIO_URL/iso8583/analyze" -d '{"message": "<wire or hex>"}' | jq .
# build (validates values first):
curl -s -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -X POST "$SCENARIO_URL/iso8583/build" \
  -d '{"mti":"0200","values":{"2":"4111111111111111","4":"000000010000","49":"840"}}' | jq .
# field-level diff of two messages:
curl -s -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -X POST "$SCENARIO_URL/iso8583/diff" -d '{"a":"<msg1>","b":"<msg2>"}' | jq .
```

**Interpretation of `analyze` output:** `mti_info` decodes the four MTI digits
(version / class / function / origin — e.g. 0210 = 1987 Financial
request-response from acquirer). `bitmap.present` lists the DEs actually on
the wire; `bitmap.secondary` non-null means DEs > 64 are present. Each
`fields[]` row carries `de`, `value`, a human `interpretation` (DE39 `00` =
"Approved", `51` = "Insufficient funds"; DE49 `840` = USD; PANs come back
masked), and — the important one — an `error` key when the value violates the
field spec (wrong length/type). Any `error` = the message is malformed per the
table you gave it; if the *counterparty* accepts it anyway, your field table
(dialect) is wrong, not the message. `build` returns `{message, errors[]}` and
refuses to pack invalid values — use it to produce known-good probes. `diff`
returns added/removed/changed DEs — ideal for "what changed between the
request that works and the one that doesn't".

## 13. MCP diagnostic tools

The MCP server (`packages/mcp-server`, Streamable HTTP `:8200/mcp` or stdio)
proxies the same APIs for AI sessions. Diagnostics-relevant tool names
(verified in `packages/mcp-server/mcp_server/tools.py`):

`diagnose_platform`, `diagnose_run`, `test_connection`, `run_flakiness`,
`run_trend`, `compare_runs`, `compare_load_runs`, `run_junit`, `list_runs`,
`get_run`, `list_load_runs`, `get_load_run`, `list_load_workers`,
`iso8583_analyze`, `iso8583_build`, `iso8583_diff`, `iso8583_tlv_build`,
`list_simulators`, `get_simulator`, `list_participants`, `list_topology_runs`,
`run_certification`.

The registry is far larger (144 registered tools + 8 resources as of 2026-07-06 — CRUD for every store; the count drifts, recount before quoting). List them all:

```bash
# authoritative count (imports the registry; def-grep undercounts helpers)
cd packages/mcp-server && python3 -c "import sys; sys.path.insert(0,'.'); \
from mcp_server import registry; \
print(len(registry.TOOL_SPECS), 'tools,', len(registry.RESOURCE_SPECS), 'resources')"
```

MCP liveness is `GET :8200/healthz` (the `/mcp` route only answers POST; a
bare GET is a 405, and a 421 means the DNS-rebinding guard rejected your Host
header — set `MCP_ALLOWED_HOSTS`).

---

## Scripts

Executable helpers in `scripts/` (bash + curl + jq only; each has a usage
header; all honor `ORCH_URL` and `TOKEN`):

### scripts/payprobe-doctor.sh — full platform verdict

```bash
cd <repo-root>/.claude/skills/payprobe-diagnostics-and-tooling
./scripts/payprobe-doctor.sh                          # liveness + /ready + /status + /diagnostics
TOKEN=$(curl -s -X POST localhost:8300/token -d username=admin -d password=admin | jq -r .access_token) \
  ./scripts/payprobe-doctor.sh
LAYERS=connections,listeners CONNECTION=visa ./scripts/payprobe-doctor.sh   # scoped doctor pass
```

Exit code: 0 healthy, 1 degraded/failing, 2 something unreachable. Prints only
warn/fail checks, each with its fix hint.

### scripts/collect-run-bundle.sh — one directory with all evidence for a run

```bash
./scripts/collect-run-bundle.sh <run_id>              # → ./run-bundle-<run_id>/
./scripts/collect-run-bundle.sh <run_id> /tmp/evidence
```

Fetches `run.json` (full detail), extracts `trace.json` (per-step timing +
wire log + engine log — the waterfall data), `junit.xml`, `report.html`,
`diagnose.json`, `compare.json`, and — when the id is a load run —
`load-run.json` + `load-compare.json`. Missing artifacts are skipped with a
warning, never fatal. Attach the directory to a bug report or hand it to a
review; it is the "measured, not assumed" evidence pack.

### scripts/flakiness-report.sh — flakiness + trend in one view

```bash
./scripts/flakiness-report.sh                 # last 30 days, min 3 runs
./scripts/flakiness-report.sh 14 nightly      # 14 days, label=nightly only
MIN_RUNS=5 ./scripts/flakiness-report.sh 30
```

Prints the flaky-scenario table (score, flips, runs, last status) and the
daily pass-rate trend, followed by the interpretation cheat-sheet.

Script assumptions (documented, verified): endpoints as in this skill; `jq`
and `curl` on PATH; orchestrator on `ORCH_URL` (default `http://localhost:8100`);
`TOKEN` optional only when the dev auth gate is open. Syntax-checked with
`bash -n`.

## When NOT to use this skill

- **You measured it and now need to fix it** → `payprobe-debugging-playbook`
  (symptom→triage, time-costing traps).
- **You need to decide whether evidence is good enough to claim pass/ship**
  (acceptance thresholds, golden inventory, certification/sign-off standards)
  → `payprobe-validation-and-qa`.
- **The stack won't come up at all / compose anatomy** →
  `payprobe-run-and-operate`; dev-env setup traps → `payprobe-build-and-env`.
- **What a config knob does** → `payprobe-config-and-flags`.
- **History of a past investigation** → `payprobe-failure-archaeology`.

## Provenance and maintenance

Authored 2026-07-03 against the live repo; every endpoint, field, threshold
and metric name above was read from source (not from docs or memory). Volatile
facts and how to re-verify each:

| Claim | Re-verify with |
|---|---|
| Orchestrator routes (diagnostics, diagnose, flakiness, trend, compare, resilience, peers, traces, metrics) | `grep -n '@app\.\(get\|post\)' packages/orchestrator/api/main.py` |
| Doctor layers, statuses, hints | `sed -n '1,60p' packages/orchestrator/api/diagnostics.py` |
| Taxonomy categories + load findings (20% / 0.6× triggers) | `sed -n '32,190p' packages/report_service/diagnose.py` |
| Flakiness score = flips/(runs−1), min_runs=3 | `grep -n -A15 'def flakiness' packages/orchestrator/api/run_store.py` |
| Load-compare metrics + 2% dead-band | `grep -n -B2 -A20 'def _delta' packages/orchestrator/api/main.py` |
| Resilience weights 35/30/25/10, gates 0.90/0.98/4.0, pass 70, grade bands | `grep -n -A8 'WEIGHTS\|class ResilienceThresholds\|def _grade' packages/orchestrator/api/resilience.py` |
| Metric names | `grep -n 'payprobe_' packages/orchestrator/api/observability.py` and `infra/OBSERVABILITY.md` |
| StepOutcome trace fields | `grep -n -A20 'class StepOutcome' packages/worker/engine/runner.py` |
| ISO 8583 endpoints + shapes | `grep -n 'iso8583' packages/scenario-service/api/main.py`; examples in `packages/scenario-service/tests/test_iso8583_analyzer.py` |
| MCP tool names | `grep -E '^def [a-z_]+\(' packages/mcp-server/mcp_server/tools.py` |
| Ports / compose profiles / token mint command | `infra/docker/docker-compose.yml` |
| Public (unauthenticated) paths | `grep -n -A4 'PUBLIC_PATHS' packages/orchestrator/api/auth.py packages/scenario-service/api/auth.py` |
| Scripts still parse | `bash -n .claude/skills/payprobe-diagnostics-and-tooling/scripts/*.sh` |

If any re-verification disagrees with this file, the code wins — update this
skill in the same change.
