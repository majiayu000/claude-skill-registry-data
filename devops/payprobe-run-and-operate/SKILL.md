---
name: payprobe-run-and-operate
description: >
  Running, deploying and operating PayProbe: docker compose bring-up, service/port map,
  readiness checks, starting/watching/stopping functional runs and load runs, simulators +
  chaos dial, participant flows/network flows, schedules, where every artifact lands
  (runs.db, runtime.json, simulators.json, scenario-service JSON registries), the
  migration/deploy runbook, and the reconcile operation for stranded load runs (POST /load-runs/reconcile). Load this skill when the
  task involves: "docker compose up", "which port is X on", "start a run", "run won't
  stop", "reconcile stranded load runs", "HTTP 424", "where is the data stored",
  "restart lost my simulators/schedules", "deploy the migration", "reconcile",
  "WebSocket stream", "JUnit export", or "topology won't start / port collision".
---

# PayProbe — Run and Operate

Runbook for bringing the platform up, driving runs through their lifecycle, and knowing
what lands where on disk. All commands are relative to the repo root unless noted.
Facts verified against the repo on 2026-07-03.

**When NOT to use this skill:**

| You are trying to… | Use instead |
|---|---|
| Recreate the dev environment / install deps / build the portal | `payprobe-build-and-env` |
| Interpret `/diagnostics`, `/status`, or a failing run's diagnosis | `payprobe-diagnostics-and-tooling` |
| Understand what a flag/env var means or add a new one | `payprobe-config-and-flags` |
| Decide whether a change is safe to ship | `payprobe-change-control` |

Jargon used below: a **functional run** executes test scenarios once and reports
pass/fail; a **load run** drives one transaction repeatedly at a target TPS
(transactions per second); a **simulator** is an in-process responder that stands in for
a payment host (e.g. a card scheme switch); a **participant flow** is a listening
stand-in whose replies are computed by walking a flow graph; a **topology** is a set of
participant flows started/stopped as one unit.

## 1. Bring-up

One command runs the entire platform, in MOCK mode by default (in-memory adapters, no
payment hardware or secrets needed):

```bash
docker compose -f infra/docker/docker-compose.yml up --build
# then open http://localhost:8080
```

`infra/docker/docker-compose.mock.yml` is superseded — it defines no services and exists
only so old references don't break. Compose project name is `payprobe`.

### Service and port map (compose defaults; every port overridable via the env var shown)

| Service | Container port | Host port (env var) | Notes |
|---|---|---|---|
| portal (nginx) | 80 | 8080 (`PORTAL_PORT`) | Angular UI + reverse proxy (see below) |
| scenario-service | 8000 | 8000 (`SCENARIO_PORT`) | scenarios + config registries |
| orchestrator | 8100 | 8100 (`ORCH_PORT`) | runs, load runs, simulators, network flows |
| mcp-server | 8200 | 8200 (`MCP_PORT`) | MCP Streamable HTTP at `/mcp`, health at `/healthz` |
| auth-service | 8300 | 8300 (`AUTH_PORT`) | JWT issuance: `POST /token` |
| assistant | (inside agent-hub) | `/api/assistant/` → `agent-hub:8600/assistant` | config agent + LLM gateway; no container of its own since 2026-09-23 (ADR-0010 D2) |
| insight-service | 8500 | 8500 (`INSIGHT_PORT`) | advisory ML insights (ADR-0005): failure categorization/explanation, outcome prediction; read-only, never gates |
| postgres | 5432 | **not published** | schema in `infra/postgres/init.sql`; see gotcha #3 |
| redis | 6379 | **not published** | event backbone + load bus; see gotcha #4 |
| prometheus | 9090 (`PROMETHEUS_PORT`) | 9090 | `--profile observability` only |
| grafana | 3000 (`GRAFANA_PORT`) | 3000 | `--profile observability` only |

Compose profiles: default = the working end-to-end mock stack (postgres, redis, auth,
scenario-service, orchestrator, mcp-server, assistant, portal). `--profile full` adds
placeholder stubs (report-service, helper-*) that return 501. `--profile observability`
adds Prometheus + Grafana (pre-provisioned "Load & Service Health" dashboard).
`--profile tools` = one-shot worker CLI (`docker compose run --rm worker`).
`--profile load` = the external load-worker container (section 4).

The portal's nginx (`infra/nginx/nginx.dev.conf`) proxies: `/api/auth/*` → auth-service,
`/api/scenarios/*` → scenario-service, `/api/assistant/*` → assistant, `/api/orch/*` →
orchestrator (with WebSocket upgrade + 3600s read timeout for long run streams). So the
browser only ever talks to :8080; `curl` examples below talk to the services directly.

### Readiness checks

```bash
curl -fsS localhost:8000/ready      # scenario-service: data store answers
curl -fsS localhost:8100/health     # orchestrator liveness (+ backbone type)
curl -fsS localhost:8100/ready      # orchestrator readiness: run_store + redis (503 when not)
curl -s   localhost:8100/status | jq .status   # aggregated: all services + redis + mcp + assistant + insight
curl -s   localhost:8100/system | jq           # runtime posture: auth gate, sandbox, durability
```

### Model insights (insight-service :8500 — advisory only)

```bash
curl -s localhost:8500/status | jq                    # corpus size, model versions, Brier self-score
curl -sX POST localhost:8500/train | jq               # incremental ingest + refit (idempotent)
curl -s localhost:8500/insights/failures/<run_id> | jq '.failures[] | {category,novel,explanation}'
curl -s localhost:8500/insights/predictions | jq '.predictions[:5]'   # riskiest scenarios first
```

Self-training runs on `INSIGHT_TRAIN_INTERVAL_SEC` (compose: nightly). The learned
categorizer only activates with the `[ml]` extra (scikit-learn) + a ≥50-failure corpus;
otherwise everything is the deterministic heuristic/frequency baseline — by design, not
a fault. Output is a model OPINION: it never gates runs or sign-off. Also exposed as MCP
tools (`get_run_insights`, `list_insight_predictions`, `train_insights`) and assistant
tools of the same names.

Predict step in scenarios: a `call` node on target `insight` (adapter `insight`,
connection base_url defaults to $INSIGHT_API_URL). Actions: `categorize` {text[,
model_id]} · `explain` {text[, model_id]} (adds why/fix/explanation) ·
`predict_outcome` {scenario_id[, environment]} · `model_status` (pre-flight:
custom_model_active etc.) · `train` (pipeline retrain). Inference hits POST
/infer, is side-effect-free (not logged into prediction self-scoring), and
exposes ${step.response.category|p_fail_next|...} for if/switch branching;
gates never see it. model_id pins one registered model over the active chain.

Corrections (human-in-the-loop): `POST /insights/corrections`
`{run_id, scenario_id, step_id, label}` — the label becomes ground truth
(never overwritten by retrains) and feeds the reserved "Operator corrections"
dataset; also available as "teach the model" in the run report's why-panel.

Custom training (Model Studio, portal `/model-studio`): upload labeled datasets
(`POST /datasets` — JSON rows or CSV `text,label`), train a supervised categorizer
(`POST /models/train` — reports holdout accuracy), activate it
(`POST /models/{id}/activate`; `none` deactivates). Active custom model outranks
auto-clusters outranks heuristics; artifacts persist in `INSIGHT_DATA_DIR` and
reload at boot.

`/status` reports `disabled` (not `down`) for intentionally-unconfigured deps (e.g. no
`REDIS_URL` single-node), and that does not degrade overall status.

### Auth posture

With `PAYPROBE_ENV=dev` (the compose default) the API gate is open — plain `curl` works.
In hardened deployments (`PAYPROBE_ENV != dev`) every call needs a bearer token:

```bash
TOKEN=$(curl -s -X POST localhost:8300/token -d username=admin -d password=admin | jq -r .access_token)
curl -H "Authorization: Bearer $TOKEN" localhost:8100/runs
```

## 2. Functional run lifecycle

### Start

`POST /runs` (orchestrator). Body = `CreateRunRequest`; pick the scenario source with
exactly one of the selectors:

```bash
curl -s -X POST localhost:8100/runs -H 'Content-Type: application/json' -d '{
  "scenario_ids": ["<id-from-scenario-service>"],
  "environment_name": "mock",
  "label": "smoke"
}'
# -> {"run_id": "<uuid>", "status": "pending"}
```

Selector fields: `scenarios` (inline docs) | `scenario_ids` | `project_id` (every case in
a project) | `set_id`. Environment: `environment` (inline dict) or `environment_name`
(bundled/registry env; defaults to the bundled mock env when omitted). Optional:
`debug: true` + `breakpoints: [...]` (step-through; drive with
`POST /runs/{id}/debug/step|continue|pause|breakpoints`), `data_table`/`dataset`
(data-driven), `requires_topology: "<topology_id>"` — a gate that returns **424 Failed
Dependency** unless a run of that topology is live AND every participant is still bound
to its port.

`POST /flows/debug-run` is the sibling for test-firing one participant flow (inline
`flow` or `flow_id`, sample `request`, `debug` defaults to true); it lands in the same
run registry and uses the same debug controls.

### Watch — WebSocket with durable resume

```
ws://localhost:8100/runs/{run_id}/stream            (via portal: /api/orch/runs/{id}/stream)
```

Events are published to the backbone; with `REDIS_URL` set that is Redis Streams, so the
stream is durable and resumable: reconnect with `?last_event_id=<id>` (each frame carries
its `id`) and you receive everything after that entry — no gap after a disconnect.
Without Redis the backbone is in-memory (single process only).

### Fetch results

| What | Endpoint |
|---|---|
| Run history (newest first) | `GET /runs` |
| Full detail, per-step results | `GET /runs/{id}` |
| JUnit XML (CI import) | `GET /runs/{id}/junit` |
| Self-contained HTML report | `GET /runs/{id}/html` |
| Failure triage (taxonomy + fixes; adds a live doctor pass for connectivity-class failures) | `GET /runs/{id}/diagnose` |
| Diff vs previous like-for-like run (regressed/fixed steps) | `GET /runs/{id}/compare[?to=<base_id>]` |
| Trend / flaky scenarios | `GET /runs/trend`, `GET /runs/flakiness` |
| Certification / sign-off | `GET /runs/{id}/certification[/html]`, `POST /runs/{id}/certify`, `GET /signoffs` |

### Stop / cancel — cross-replica semantics

`POST /runs/{id}/cancel` tries, in order: (1) this replica owns the asyncio task →
cancel directly; (2) another replica owns it → route via the run-control channel
(Redis-backed when `REDIS_URL` set; every replica registers its in-flight runs and
listens for cancel requests); (3) already finished → returns its terminal status, not
a 404. So cancel is safe to send to any replica.

## 3. Load runs

### Start

`POST /load-runs`. Transaction selectors are the same as `/runs` (the first resolved
scenario is driven), plus profile fields:

```bash
curl -s -X POST localhost:8100/load-runs -H 'Content-Type: application/json' -d '{
  "scenario_ids": ["load-payment"],
  "environment_name": "mock",
  "type": "steady", "target_tps": 50, "duration_s": 60, "workers": 1
}'
```

Profile `type`: `steady` (target_tps) | `ramp` (start_tps→end_tps over ramp_s) |
`spike` (base_tps + spike_tps every spike_every_s for spike_duration_s) |
`soak` (connections + open_rate_per_s + heartbeat_interval_s). Extras: `mix` (weighted
transaction blend — supersedes scenario selectors; first entry is primary),
`provision_scenario_id`/`provision_scenario` (a scenario run ONCE before the load; if it
does not pass, the API returns **HTTP 424** `provisioning pre-run failed` and the load
never starts), `max_in_flight_per_worker` (backpressure cap, default 2000).

### Worker fleet vs in-process fallback

- In-memory bus (no `REDIS_URL`): workers run in-process immediately.
- Redis bus: shards are pushed to the bus for external `python -m worker.load_worker`
  processes. A provisioner (`PAYPROBE_WORKER_PROVISIONER`: `auto`|`local`|`docker`|
  `compose`|`none`; compose default `docker` with the socket mounted and image
  `payprobe-load-worker`) brings the fleet up automatically. If after a grace window
  nothing has claimed shards, the coordinator falls back to in-process workers — **unless**
  the demand exceeds the safe cap (`PAYPROBE_INPROC_MAX_TPS`, default 2000 peak TPS;
  `PAYPROBE_INPROC_MAX_CONNECTIONS`, default 5000 for soak), in which case it refuses,
  posts a `notice` on the run (visible on the Load page) and gives the manual command:

```bash
REDIS_URL=redis://<host>:6379 LOAD_RUN_ID=<run_id> python -m worker.load_worker
# or by container: LOAD_RUN_ID=<id> docker compose -f infra/docker/docker-compose.yml \
#   --profile load up -d --scale load-worker=4 load-worker
```

  Set `PAYPROBE_LOAD_EXTERNAL_WORKERS=1` to disable the in-process fallback entirely
  (real distributed fleets).

### Control and inspect

| Action | Endpoint |
|---|---|
| Live snapshot / final summary | `GET /load-runs/{id}` |
| History (label `load:` prefix, headline metrics) | `GET /load-runs` |
| Stop (this replica → other replica via run control → stranded record reconciled to `interrupted`) | `POST /load-runs/{id}/stop` |
| Hot re-tune rate without restart (`target_tps`/`base_tps`/`spike_tps`/`end_tps`) | `POST /load-runs/{id}/retune` |
| Scale the fleet to N workers (dynamic path) | `POST /load-runs/{id}/scale` `{"desired": N}` |
| vs-previous regression diff (p95, error rate, TPS stability…) | `GET /load-runs/{id}/compare` |
| Fleet presence / drain one / drain all | `GET /load-workers`, `POST /load-workers/{wid}/stop`, `POST /load-workers/stop-all` |
| Provisioner capabilities + manual command template | `GET /load-workers/provisioner` |

## 4. Simulators, chaos, participant flows, network flows

### Simulators (in-process responders on the orchestrator)

- Ad-hoc: `POST /simulators` `{"label": "...", "config": {<TcpResponder config>}}` → id.
  List/detail/metrics: `GET /simulators`, `GET /simulators/{sid}`, `GET /simulators/{sid}/metrics`
  (stats + throughput timeline + last 50 decoded requests). `POST /simulators/{sid}/clear`
  resets counters. `DELETE /simulators/{sid}` stops it (a saved config of the same id survives).
- Saved: CRUD under `/simulator-configs`; `POST /simulator-configs/{cid}/start|stop`,
  `POST /simulator-configs/{cid}/enabled` — **enabled saved simulators auto-start on boot**
  (skip with `DISABLE_SIMULATOR_AUTOSTART=1`). Promote a running ad-hoc one with
  `POST /simulators/{sid}/save?enabled=true` (the live responder is re-keyed to the saved id).

### Chaos dial (live, no restart)

```bash
curl -s localhost:8100/simulators/<sid>/chaos                      # current dial + storm status
curl -s -X PUT localhost:8100/simulators/<sid>/chaos \
  -H 'Content-Type: application/json' -d '{"drop_pct": 20, "latency_ms": 300}'   # {} = off
curl -s -X POST localhost:8100/simulators/<sid>/chaos/storm -H 'Content-Type: application/json' \
  -d '{"phases":[{"duration_s":30,"chaos":{"drop_pct":100},"label":"outage"},
                 {"duration_s":30,"chaos":{},"label":"calm"}], "repeat":3}'
curl -s -X DELETE localhost:8100/simulators/<sid>/chaos/storm      # cancel + restore baseline
```

Accepted chaos keys: `seed, drop_pct, drop, latency_ms, malformed_pct, malformed,
malformed_mode, partial_pct, partial, partial_bytes`. A manual PUT cancels any running
storm; a storm restores the pre-storm baseline when it ends. Resilience certification
(chaos + load-run observation → graded certificate) lives at `GET|POST /resilience/runs`.

### Participant flows and network flows

- One flow: `POST /participants/start` `{"flow_id": "...", "port": <optional>}` — 409 if
  that flow is already running inside a live topology (would clash ports).
  `GET /participants`, `DELETE /participants/{pid}`. Per-transaction network traces:
  `GET /participants/traces`, `GET /participants/trace/{cid}`; capture pause/resume via
  `GET|POST /participants/capture`.
- Whole network (ADR-0004; the legacy `POST /topologies/{tid}/start` was removed —
  topologies migrated into network flows with the same ids):
  `POST /network-flows/{nid}/start`. Saved simulators referenced by `simulator` nodes
  come up first (and stop with the run only if the run started them). **Port planning
  happens before anything starts**: each flow's inbound connection port is the base (a
  participant node's `port` overrides it); N instances get base, base+1, … (no fixed
  port = ephemeral). A planned (host, port) wanted by two flows is a **409 port
  collision** and nothing is started; a mid-start failure rolls back the already-started
  participants + simulators. Start order = topological sort of the wiring edges (callees
  first; node list order when unwired). Every autostart `scenario` node (initiator) runs
  once the listeners are up (failure surfaced as `initiator_error`, not a teardown) and
  is cancelled on stop. `GET /topology-runs` shows health
  (`live/total/ready` — the same readiness the `requires_topology` run gate checks);
  `DELETE /topology-runs/{run_id}` stops the set.
- `GET /peers` — every established inbound socket on hosted listeners (simulators +
  participants) plus proxy upstream legs; per-run worker adapter sockets are NOT listed.

## 5. Schedules

`POST /schedules` with `{label, kind: "run"|"load", request: <CreateRunRequest or
LoadRunRequest body>, interval_sec | daily_at ("HH:MM" UTC), enabled}`. A 30s poll loop
triggers due schedules (disable loop: `DISABLE_SCHEDULER=1`). `kind: "load"` on an
interval with a soak profile = a **cyclic soak** (unattended leak-hunting).
`POST /schedules/{sid}/run` fires now; `POST /schedules/{sid}/enabled`, `DELETE /schedules/{sid}`.

Where scheduled runs land: the same registries as manual ones — `kind: "run"` in
`GET /runs`, `kind: "load"` in `GET /load-runs` (label = the schedule label; load runs
get the `load:` prefix). There is no separate schedule-run store.

## 6. Artifact and data conventions

Code defaults vs what the compose file actually sets — the difference is the #1 source
of "my X vanished after restart" reports:

| Store | Service | Code default | Compose setting | Volume |
|---|---|---|---|---|
| Run registry (runs + summaries, functional AND load) | orchestrator | `RUN_DB`; unset → `:memory:` when `PAYPROBE_ENV` ∈ {dev,development,test,local}, else `RUN_DB_PATH` (`/data/runs.db`) | `RUN_DB=/data/runs.db` (SQLite, WAL) | `orchestrator_data` |
| Saved simulators | orchestrator | `SIMULATORS_FILE` → `:memory:` | `/data/simulators.json` | `orchestrator_data` |
| Participant/topology desired state (re-launched on boot) | orchestrator | `ORCH_RUNTIME_FILE` → `:memory:` | `/data/runtime.json` | `orchestrator_data` |
| Schedules | orchestrator | `SCHEDULES_FILE` → `:memory:` | **not set → in-memory** (gotcha #1) | — |
| Sign-offs (immutable Go/No-Go snapshots) | orchestrator | `SIGNOFFS_FILE` → `:memory:` | **not set → in-memory** (gotcha #1) | — |
| Scenarios/projects/sets | scenario-service | `DATABASE_URL` → `scenarios.db` (SQLite) | `/data/scenarios.db` | `scenario_data` |
| Config registries: catalog, formats, variables, tables, connections, flows, participant_flows, participant_groups, topologies (legacy migration input), network_flows, assist, test_data, environments | scenario-service | one JSON file each, sibling of the SQLite db (e.g. `/data/connections.json`); `:memory:` when db is `:memory:` | siblings in `/data` | `scenario_data` |
| Users/roles | auth-service | `AUTH_DB` | `/data/auth.db` (SQLite) | `auth_data` |
| Run event streams + load bus + run control | redis | in-memory backbone when `REDIS_URL` unset | `redis://redis:6379`, AOF-less RDB on volume | `redis_data` |
| Postgres schema (`users`, `environments`, `scenarios`…) | postgres | — | provisioned by `infra/postgres/init.sql` but **unused by default** (gotcha #3) | `postgres_data` |

Live simulator/participant *state* is always in-memory; the files above hold desired
state that is re-created on boot (enabled simulators auto-start; runtime.json re-launches
participants/network flows — skip with `DISABLE_PARTICIPANT_AUTOSTART=1`).

`GET /system` (orchestrator) reports `run_store_durable` and the rest of the posture, so
you can verify durability without shelling into the container.

## 7. Deploy / migrate (distilled from docs/history/MIGRATION-DEPLOY-RUNBOOK.md)

The pattern generalizes: pre-flight suites → rebuild only changed services → smoke-check
→ dry-run data steps → apply → verify → per-step rollback.

```bash
# 0. pre-flight (local)
make test-scenario && make test-orchestrator && make portal-build
# 1. rebuild + restart only the changed services
cd infra/docker
docker compose build scenario-service orchestrator portal
docker compose up -d  scenario-service orchestrator portal
# 2. smoke
curl -fsS localhost:8000/ready && curl -fsS localhost:8100/health
# 3. data migration — ALWAYS dry-run first (endpoints default to dry-run; ?apply=true applies)
curl -s localhost:8000/admin/migrate/collisions | jq .safe_to_flip   # GET, expect true. (Upstream bug: docs/history/MIGRATION-DEPLOY-RUNBOOK.md shows -XPOST here — the route is GET; POST returns 405.)
curl -s -XPOST localhost:8000/admin/migrate/seed-default-connections | jq '.create' # review
curl -s -XPOST 'localhost:8000/admin/migrate/seed-default-connections?apply=true' | jq '{created,failed}'
curl -s -XPOST localhost:8000/admin/migrate/slim-environments | jq '{remove,blocked}'  # optional; leave anything "blocked"
```

Applying (`?apply=true`) and any flag-default flip is a migration-class change — gate it
per `payprobe-change-control` (dry-run evidence + rollback path first).

Rollback is per-step and flag-based: `PAYPROBE_DEFAULT_CONNECTION_RESOLUTION=0` (undo
resolution), `PAYPROBE_CONNECTION_OVERRIDE_WINS=0` (legacy env-wins precedence), re-add
the slimmed env block, or delete the seeded default connection. In hardened deployments
add the bearer token to the `/admin/migrate/*` calls. Note (2026-07-03): the live
registry was verified a no-op for the connection/env part (`safe_to_flip: true`).

### Stuck-run reconcile (orchestrator crash/restart leaves runs "running")

A fresh orchestrator process owns no live load runs, so any DB row still `running` is an
orphan. Three ways it gets fixed — all end in status `interrupted` with a
`{"reconciled": true, "reason": ...}` summary:

1. Automatic on boot (startup hook).
2. `curl -s -XPOST localhost:8100/load-runs/reconcile` → `{"reconciled": [ids], "count": N}` —
   safe anytime; runs a live coordinator owns are skipped. Portal: Load page →
   "Fix stuck runs" button.
3. `POST /load-runs/{id}/stop` on a stranded run reconciles that one run.

## 8. Ops gotchas (each verified in code/compose)

1. **Schedules and sign-offs are in-memory in the stock compose file.** `SCHEDULES_FILE`
   and `SIGNOFFS_FILE` are not set in `infra/docker/docker-compose.yml`, so both default
   to `:memory:` and vanish on container restart — even though runs, simulators and
   runtime state persist. Set them to files on the `/data` volume for durability.
2. **`PAYPROBE_ENV=dev` flips two behaviors at once**: it opens the auth gate AND makes
   an unset `RUN_DB` mean `:memory:`. Compose pins `RUN_DB=/data/runs.db` explicitly, so
   dev-mode compose still persists runs; a bare `uvicorn` dev process does not.
3. **Postgres runs but nothing uses it by default.** scenario-service is SQLite
   (`DATABASE_URL=/data/scenarios.db`); the compose comment says the Postgres store
   needs schema reconciliation with `infra/postgres/init.sql` before it can be used.
   Don't debug data issues in Postgres; look in the SQLite/JSON files on `scenario_data`.
4. **Redis is not published to the host** (no `ports:` mapping). A manual
   `python -m worker.load_worker` on the host cannot reach `redis://localhost:6379`
   unless you publish 6379 or run the worker inside the compose network
   (`--profile load` container path does this for you). A standalone load worker
   **exits immediately without `REDIS_URL`**.
5. **Load run refuses silently-looking?** If no external workers join and demand exceeds
   the in-proc cap, the run stays alive at 0 TPS with a `notice` explaining the fix —
   read `GET /load-runs/{id}` `.notice` before assuming a hang.
6. **Cancel/stop return values matter**: a stop on an already-finished run returns its
   terminal status (200), not 404. 404 means the id is genuinely unknown.
7. **`requires_topology` checks health, not existence**: every participant of a live run
   of that topology must still be bound to a port, otherwise the run start gets 424.
8. **The orchestrator needs the docker socket** for the default `docker` worker
   provisioner (`/var/run/docker.sock` mount + `PAYPROBE_WORKER_IMAGE`); remove the mount
   and dynamic fleet scaling degrades to the manual path (the API then returns the
   manual command instead of scaling).
9. **Event streams need Redis for resume.** Without `REDIS_URL` the backbone is
   in-memory: a portal reconnect after an orchestrator restart cannot replay missed
   events, and multi-replica setups won't see each other's streams at all.

## 9. Playground — ad-hoc execution by reference (ADR-0007)

One surface to fire a single interaction at anything addressable, without
authoring a scenario. Secrets resolve server-side (connection ⊕ override
matrix); echoes come back masked with the capture redaction rules. Backend
verified in code; the portal `/playground` page still owes a host build +
click-through.

```bash
# what can I call right now? (connections × envs, running sims, participants
# incl. NATS subjects, groups, crypto functions — each with sample chips)
curl -s localhost:8100/playground/targets | jq 'keys'

# fire one ISO 8583 message at a registered connection, resolved for an env
curl -s -X POST localhost:8100/playground/execute -H 'Content-Type: application/json' -d '{
  "target": {"kind": "connection", "id": "cn_to_auth", "environment": "mock"},
  "action": "send_message",
  "payload": {"mti": "0200", "amount": 1500},
  "message_format_id": null
}'
# target.kind: connection | group | simulator | participant | raw | function
# kind=raw takes host/port/adapter/protocol/config (parity with /hsm/command)

# history (per-user, in-memory ring, masked), re-fire, promote
curl -s localhost:8100/playground/history | jq '.rows[0]'
curl -s -X POST localhost:8100/playground/history/3/refire
curl -s -X POST localhost:8100/playground/save-as-scenario \
  -H 'Content-Type: application/json' -d '{"name": "explored-auth-flow"}'
curl -s -X DELETE localhost:8100/playground/history      # clear
```

Notes (verified in `orchestrator/api/main.py` + `api/playground.py`):

- Execution is fully delegated (`WorkerEngine._execute_step` / `run_crypto`)
  — no second engine. An unreachable target is a normal `{ok:false,error}`
  result, not a 5xx.
- Playground fires against a **running simulator** are tagged: `playground_hits`
  on the sim detail, and certification-time stats subtract in-window
  playground traffic — ad-hoc pokes don't contaminate a cert run.
- Assistant/MCP: `playground_targets` + `playground_execute` (toolkit tier
  **execute** — never journalled; refused in plan mode, hidden from advisor).
- `save-as-scenario` accepts `{"seqs": [...]}` to promote selected entries and
  `project_id` to file the result; default promotes the whole history.

## Database probes and run fixtures (ADR-0012, 2026-09-25)

- A `db_probe_core` / `db_probe_switch` connection is a real worker adapter now
  (PostgreSQL via asyncpg, SQLite via stdlib). Reads run in a read-only database
  session; the SQL for `query_transaction` / `query_balance` lives on the
  connection as `queries` (per-environment overrides for schema differences).
  How-to: `docs/adapters/db-probe.md`; example: `examples/scenarios/db_probe_settlement.json`
  against the bundled `example_sqlite_probe` connection.
- `GET /diagnostics?layers=databases` answers "why does my probe not work": per
  probe connection reachable / read-only enforced / writes enabled / named
  queries that do not parse. A dead probe BLOCKs (never fails) every scenario
  that touches it in phase 1.
- Writes: `writes: true` on the connection (per environment), every `execute`
  step declares a `cleanup` the runner executes at scenario end (any outcome,
  `cleanup` step outcomes in the run, `cleanup_failed:<step>` note never changes
  the verdict). `writes: "permanent"` allows `cleanup: null`.
- Load runs refuse a probe target with 400 unless the connection has
  `load_ok: true` (mocked probes exempt).
- Run fixtures (on by default; `PAYPROBE_RUN_FIXTURES=0` disables): `POST /runs {"fixtures": {"before": [...], "after": [...]}}`
  runs saved scenarios once around the run; results under `summary.fixtures`,
  in the sign-off report's Fixtures section and the provenance stamp. With the
  flag set to 0 the request is refused (400), never silently run without fixtures.

## Provenance and maintenance

Verified 2026-07-03 against the working tree (compose file, nginx conf,
`packages/orchestrator/api/{main,load_coordinator,run_store,worker_provisioner}.py`,
`packages/scenario-service/api/main.py`, `packages/auth-service/api/main.py`,
`docs/history/MIGRATION-DEPLOY-RUNBOOK.md`, `docs/operations/load-test-runbook.md`,
`infra/postgres/init.sql`, portal Load page). Re-verify before trusting:

```bash
# service list, ports, profiles, volumes, env defaults
sed -n '1,60p' infra/docker/docker-compose.yml && grep -n 'ports:\|profiles:\|_FILE\|RUN_DB' infra/docker/docker-compose.yml
# orchestrator endpoint inventory (the tables above)
grep -n '@app\.\(get\|post\|put\|delete\|websocket\)' packages/orchestrator/api/main.py
# storage defaults (":memory:" fallbacks)
grep -n 'RUN_DB\|SCHEDULES_FILE\|SIMULATORS_FILE\|SIGNOFFS_FILE\|ORCH_RUNTIME_FILE' packages/orchestrator/api/main.py
grep -n '_sibling_file\|DATABASE_URL' packages/scenario-service/api/main.py
# in-proc caps + fallback + manual worker command
grep -n 'inproc_max\|manual_command\|LOAD_EXTERNAL' packages/orchestrator/api/{main,load_coordinator,worker_provisioner}.py
# migration steps
sed -n '1,100p' docs/history/MIGRATION-DEPLOY-RUNBOOK.md
# nginx proxy routes
grep -n 'location\|proxy_pass' infra/nginx/nginx.dev.conf
```

Volatile facts most likely to drift: compose env defaults (worker provisioner backend,
port vars), the in-proc caps (2000 TPS / 5000 conns), whether `SCHEDULES_FILE`/
`SIGNOFFS_FILE` get added to compose, and Postgres-store readiness in scenario-service.
