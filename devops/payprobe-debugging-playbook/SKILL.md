---
name: payprobe-debugging-playbook
description: >
  Symptom-to-cause triage for PayProbe failures. Load this when something is
  broken and you need to find out WHY: load runs stuck as "running" forever,
  crypto nodes returning {"error": ...} dicts, tests failing locally but green
  in CI, KeyError 'target', 401/503 on every API call, WebSocket closing
  immediately, TCP steps hanging or timing out, port collisions on topology
  start, 424 "required topology is not running", simulators vanishing after a
  restart, empty run history, chaos faults that won't stop, or a load run that
  got slower than last time. Contains the first-five-minutes checklist, a
  symptom→cause→experiment→fix table, and the trap stories that cost real time.
---

# PayProbe Debugging Playbook

Triage runbook for PayProbe's known failure modes. Every endpoint, flag, and
symbol below was verified against the repo on 2026-07-03.

**Jargon, defined once:**
- **Orchestrator** — FastAPI service (`packages/orchestrator/api/main.py`) that owns run lifecycle, simulators, topologies, load runs.
- **Scenario-service** — FastAPI service (`packages/scenario-service`) holding scenarios, connections, formats, environments.
- **Worker engine** — `packages/worker/engine/runner.py`; executes scenario steps via protocol adapters.
- **Load run** — distributed load test coordinated by the orchestrator; its run rows carry a `load:` label prefix.
- **Topology** — a set of participant flows (simulated network nodes) started/stopped as one unit.
- **ISO 8583** — the binary message format card networks use; PayProbe frames it over TCP with a length prefix.

## When NOT to use this skill

- You want to **measure** something (latency, TPS, memory) or need interpretation guides for the diagnostic endpoints → `payprobe-diagnostics-and-tooling`.
- You suspect the problem was **fought before** and want the investigation history, dead ends, and rejected fixes → `payprobe-failure-archaeology`.
- The environment itself won't come up (deps, docker, portal build) → `payprobe-build-and-env`.
- You have the root cause and are ready to ship a fix → `payprobe-change-control` (measured root cause + reproducing test are mandatory before any fix lands).

## 1. First five minutes

Run these in order; stop at the first thing that looks wrong. `$ORCH` is the
orchestrator base URL (compose default `http://localhost:8100`, mapped via `ORCH_PORT` in `infra/docker/docker-compose.yml`; adjust to your
deployment). Add `-H "Authorization: Bearer $API_TOKEN"` to every call except
the public paths (`/status` and `/health` among them; full 8-path allow-list in `payprobe-diagnostics-and-tooling`).

```bash
# 1. Is the platform up at all? (public, no auth needed)
curl -s $ORCH/status

# 2. Full platform doctor: services → connections → listeners → recent-run errors,
#    each failure with a concrete fix hint.
curl -s -H "Authorization: Bearer $API_TOKEN" $ORCH/diagnostics

# 3. If ONE run failed: automated triage against the error taxonomy
#    (unreachable / timeout / auth / assertion / tls / binding / reference / url).
curl -s -H "Authorization: Bearer $API_TOKEN" $ORCH/runs/<run_id>/diagnose

# 4. Is the suite itself green? (ground truth — never debug on a red baseline)
cd <repo-root> && make test

# 5. If load-run history shows phantom "running" runs after a restart:
curl -s -X POST -H "Authorization: Bearer $API_TOKEN" $ORCH/load-runs/reconcile
```

Checklist mindset:
- [ ] `/status` reachable → services up, move to layer 2.
- [ ] `/diagnostics` clean → problem is scenario/config-level, not platform-level.
- [ ] `/runs/{id}/diagnose` names a category → jump to that row in the table below.
- [ ] `make test` green → your bug is not a pre-existing regression.
- [ ] Not sure what changed? `git log --oneline -10` before touching anything.

## 2. Symptom → cause → discriminating experiment → fix

| Symptom | Likely cause | Discriminating experiment | Fix pointer |
|---|---|---|---|
| Load run shows `running` forever; portal Load history never settles | Orchestrator crashed/restarted while the run was live; the in-memory coordinator that would have finalized the SQLite row is gone, so the row is stranded | `curl $ORCH/load-runs` shows `running` but the run does not appear in any live coordinator (a fresh process has none). Stranded = row status running, no live owner | `POST /load-runs/reconcile` (marks them `interrupted`), or the portal Load page "Fix stuck runs" button. A startup hook (`@app.on_event("startup")` → `_reconcile_stuck_load_runs`, `main.py` ~line 1872) also runs this on boot; `POST /load-runs/{id}/stop` reconciles a single stranded run |
| Crypto step "fails" with response `{"error": "pycryptodome is not installed in this runtime"}` | `worker/engine/crypto_tools.py` needs `Crypto.Cipher` (pycryptodome) and degrades to an error dict instead of raising | `python -c "from Crypto.Cipher import DES, DES3"` in the runtime that executes the worker. ImportError = dependency; success = different problem | `pip install pycryptodome` (declared as `pycryptodome>=3.19` in `packages/worker/pyproject.toml` since 2026-06). Then re-run the failing scenario |
| `worker/tests/test_engine.py` crypto/EMV tests fail locally but pass in CI | Environment, not regression: sandboxes may lack pycryptodome or the crypto key material these tests need (`docs/history/project-review.md` records exactly this: "missing key material in this sandbox; they pass in CI") | Run one failing test with `-x` and read the actual error. An `{"error": ...}` dict about pycryptodome or key material = environment. An assertion mismatch on computed values = real regression | Fix the environment (install deps per `payprobe-build-and-env`), never edit the test expectation. If CI is also red, treat as regression |
| Starting an HTTP-trigger participant flow returns an error naming `aiohttp` | The slim orchestrator image doesn't ship `aiohttp`; HTTP participant listeners import it lazily (`main.py` ~line 2683 catches `ModuleNotFoundError`) | Error text literally says HTTP listeners need `aiohttp`. `python -c "import aiohttp"` inside the orchestrator container | Rebuild the image with aiohttp installed (the current Dockerfile does), or use a TCP trigger connection |
| Step errors with `KeyError: 'target'` on a crypto/code/http node | Scenario has NO `edges` array, and something is routing edge-less (linear) execution through the action-step path that reads `step["target"]`. This exact bug was fixed (see trap story 2) — a recurrence means a new code path bypasses `_execute_node` kind dispatch in `worker/engine/runner.py` | Reproduce with the regression test: `cd packages && python -m pytest worker/tests/test_engine.py::test_edgeless_non_action_nodes_run_without_target_keyerror -q` | If that test fails, the linear-path dispatch regressed; diff `runner.py` around the edge-less loop (~line 1129, 1194) |
| EVERY API call rejected — but is it 401 or 503? | Fail-closed auth gate (`packages/orchestrator/api/auth.py`, mirrored in `packages/scenario-service/api/auth.py`) | **503** "auth is not configured; refusing to serve" = no credential configured AND not a dev env. **401** = auth configured but your token is missing/wrong. This status-code split IS the discriminating experiment | Local dev: `export PAYPROBE_ENV=dev` (accepted values: `dev`, `development`, `test`, `local`). Real deployments: set `API_TOKEN` (static bearer) or `AUTH_JWT_SECRET`/`AUTH_JWT_PUBLIC_KEY` (JWT), then send `Authorization: Bearer <token>` |
| WebSocket run stream connects then instantly closes (code 1008) | WS routes skip the app-level auth dependency and are guarded by `authorize_websocket`, which closes unauthenticated sockets. Browsers can't set WS headers | Same WS URL with `?token=<API_TOKEN or JWT>` appended works | Pass the credential as `?token=` on `GET /runs/{run_id}/stream` |
| Refreshed the browser mid-run — did I lose events? | No. The stream replays from a cursor | Reconnect with `?last_event_id=<id>`; server replays everything after it, then tails live | Working as designed. Backbone is in-process by default; set `REDIS_URL` for Redis Streams (needed for multi-replica) |
| `POST /topologies/{tid}/start` → 409 "port collision in topology" | A flow with N instances shares one inbound connection; the orchestrator plans ports base, base+1, … per instance BEFORE starting anything, and two flows' plans overlap | The 409 body names both flow ids and the exact host:port contested | Adjust the connection's port or instance counts so plans don't overlap. Partial starts are rolled back automatically, so nothing lingers |
| Scenario run → 424 "required topology '…' is not running" | The scenario declares `requires_topology` and the readiness gate (`_topology_is_up`) found no run where EVERY participant is still registered and bound — a half-dead topology counts as down | `curl $ORCH/topology-runs` and read `health` (`{total, live, ready}`) for the topology's run | Start it: `POST /topologies/{tid}/start`. If `live < total`, find which participant died (`/diagnostics?layers=listeners`) |
| TCP step hangs then times out; the peer definitely answered | Framing mismatch: adapter and responder must agree on `framing.length_prefix_bytes` (default 2, big-endian). With mismatched framing the reader waits for bytes that never complete a frame | Read the step's wire log: run detail → step `raw_log` / Trace tab. You'll see the request go out and either garbage or silence come back. Compare `framing` blocks on both connection configs | Align `framing` config (see `packages/worker/adapters/tcp/README.md`). Note the chaos dial's `bad_length` fault deliberately fakes this — check no chaos block is active: `GET /simulators/{sid}/chaos` |
| TCP steps fail once after a simulator restart, then recover | Expected: the TCP adapter auto-reconnects with exponential backoff + re-sign-on (`adapter.py` `_reconnect`, `backoff_initial_sec` 0.5 → `backoff_max_sec` 30, `max_attempts` 0 = unlimited); in-flight exchanges wait for the reconnect, bounded by the response timeout | Failures only in the window right after a restart, then clean = reconnect working. Persistent failures = the listener never came back (check `/peers` and `/diagnostics?layers=listeners`) | Nothing to fix if it recovers. Tune `reconnect.*` keys on the connection if the window is too long |
| Simulators / participant listeners gone after orchestrator restart | Runtime desired-state persistence is off: `ORCH_RUNTIME_FILE` and `SIMULATORS_FILE` default to `:memory:` | `echo $ORCH_RUNTIME_FILE $SIMULATORS_FILE` in the orchestrator env — empty or `:memory:` means nothing survives restarts | Point both env vars at files on a volume; the orchestrator re-launches persisted listeners on boot |
| Run history empty after restart | `RUN_DB` unset in a dev-ish environment → in-memory SQLite (explicit `RUN_DB` always wins; non-dev defaults to `RUN_DB_PATH` or `/data/runs.db`) | Check `RUN_DB` in the orchestrator env | Set `RUN_DB` to a file on a volume |
| Simulator keeps failing after a chaos storm "ended" | A manual chaos block is still applied, or the storm never restored baseline (it restores on normal end/cancel; a manual `PUT /simulators/{sid}/chaos` cancels the storm and takes over) | `GET /simulators/{sid}/chaos` — shows the live chaos block, fault count, storm status | `PUT /simulators/{sid}/chaos` with `{}` turns chaos off |
| Load run slower / more errors than last time — regression or noise? | Could be either; never eyeball it | `GET /load-runs/{run_id}/compare` — diffs vs the previous like-for-like run (error categories, TPS series, stability). Functional runs: `GET /runs/{run_id}/compare` reports `regressed`/`fixed` per step | If regressed, bisect with the run history; escalate measurement methodology to `payprobe-diagnostics-and-tooling` |
| A scenario passes sometimes, fails sometimes | Flakiness, not a hard bug | `GET /runs/flakiness` — per-scenario flip score across history | Quarantine per the `flaky` marker convention; root-cause before un-quarantining |

## 3. Trap stories (why these rows exist)

**1. The silently degrading crypto node (2026-06-18).** The suite baseline was
180 passed / 3 failed, all crypto scenarios. Nothing crashed: `run_crypto()`
in `worker/engine/crypto_tools.py` returns `{"error": "pycryptodome is not
installed in this runtime"}` as a *result*, so steps "completed" with error
payloads. The worker's `pyproject.toml` declared `python-pkcs11` and `iso8583`
but omitted `pycryptodome`. The trap: an error-shaped response is easy to
mistake for a scenario-logic bug or a simulator fault. The fix was one
dependency line (docs/history/PROGRESS.md, Iteration 1). Lesson: when a crypto/code node
"fails", read the response body first — a dependency confession beats an hour
of scenario archaeology.

**2. KeyError: 'target' on edge-less scenarios (2026-06, docs/history/PROGRESS.md
Iteration 2).** Found *while reproducing* trap 1. The graph execution path
dispatched steps by `kind`; the linear (no-`edges`) path called `_run_step()`
for everything, which reads `step["target"]` unconditionally — so any
crypto/code/http node in an edge-less scenario crashed with `KeyError:
'target'`. Fixed by routing the linear loop through kind-aware
`_execute_node()`; guarded by
`test_edgeless_non_action_nodes_run_without_target_keyerror`. Lesson: PayProbe
has TWO execution paths (graph and linear); a bug that "only happens in simple
scenarios" is often the linear path missing something the graph path has.

**3. Stuck "running" load runs (fixed 2026-07-03).** Load-run state lived in
two places: a durable SQLite row and an in-memory coordinator. Kill the
orchestrator mid-run and the row stays `running` forever — history lies, and
"is anything running?" checks return phantoms. The fix is reconciliation, not
deletion: rows with no live owner become `interrupted` with a
`{"reconciled": true, "reason": ...}` summary (`run_store.reconcile_orphans`).
It runs at startup, on `POST /load-runs/reconcile`, and inside
`POST /load-runs/{id}/stop`. Lesson: any "durable record + in-memory owner"
split needs an orphan-reconcile story; when state looks impossible, ask who
was supposed to write the final status and whether that process survived.

**4. The lopsided auth gate (fixed per scenario-service `auth.py` docstring).**
The orchestrator verified JWTs and failed closed; the scenario-service only had
an optional static bearer, off by default. You could lock the orchestrator down
completely while the service holding every scenario, connection, and secret
stayed wide open. Now both services share one gate contract (same env vars,
same fail-closed 503). Lesson: when debugging 401/503s, remember there are
*multiple* gates that must agree — and that 503 means "gate unconfigured",
not "service down".

**5. The slim image without aiohttp.** HTTP participant listeners need
`aiohttp`; the slim orchestrator image historically didn't install it, and a
top-level import would have crashed orchestrator startup entirely. It's
imported lazily and converted to a clear HTTP error instead
(`main.py` ~2683). Lesson: "works with TCP flows, breaks only with HTTP
trigger connections" is an image-contents problem, not a code problem.

## 4. Wire-level debugging arsenal

When triage says "the message is wrong" rather than "the platform is broken":

| Tool | What it shows | Where |
|---|---|---|
| Execution trace | Per-step wire bytes (`raw_log`) + structured engine events (`trace`) with timing, built by `_build_trace` in `worker/engine/runner.py`; secrets redacted | Run report → Trace tab; fields on each step in `GET /runs/{id}` |
| Network trace | One transaction's hop-by-hop path across a participant-flow network, including failed downstream hops | `GET /participants/traces` (index), `GET /participants/trace/{cid}` (one transaction) |
| Connected peers | Who is actually connected to each listener right now (incl. a proxy's upstream leg) | `GET /peers` |
| Chronoscope | Time-travel replay of the live network map (8-min buffer), exportable as a replay JSON file and re-importable for offline review | Portal `/topology-map-3`; recorder in `packages/portal/src/app/topologies/chronoscope/` |
| ISO 8583 Inspector | Decode/build raw ISO 8583 messages against a format | Portal Inspector page |

## 5. Escalation

- **Need numbers, not vibes** (latency breakdowns, TPS math, interpreting `/diagnostics` output in depth, helper scripts): → `payprobe-diagnostics-and-tooling`.
- **"Has this been fought before?"** (a symptom smells familiar, a fix feels like it was tried and removed — e.g. anything touching connection/environment modeling): → `payprobe-failure-archaeology` BEFORE re-attempting a known dead end.
- **Ready to fix**: no fix ships without a measured root cause and a reproducing test (`payprobe-change-control`). `make test` green before and after.

## Provenance and maintenance

Authored 2026-07-03 against the repo at that date. Everything above was
verified by reading the cited files. Re-verify before trusting, from repo root:

```bash
# stuck-run machinery
grep -n "reconcile_orphans" packages/orchestrator/api/run_store.py packages/orchestrator/api/main.py
grep -n "load-runs/reconcile\|Fix stuck runs" packages/orchestrator/api/main.py packages/portal/src/app/load/load.component.ts
# crypto dependency story
grep -n "pycryptodome" packages/worker/pyproject.toml packages/worker/engine/crypto_tools.py docs/history/PROGRESS.md
# edge-less KeyError regression guard
cd packages && python -m pytest worker/tests/test_engine.py::test_edgeless_non_action_nodes_run_without_target_keyerror --collect-only -q; cd ..
# auth gate env vars (both services)
grep -n "PAYPROBE_ENV\|API_TOKEN\|AUTH_JWT" packages/orchestrator/api/auth.py packages/scenario-service/api/auth.py
# diagnose taxonomy + doctor
grep -n "def classify_error" -A 25 packages/report_service/diagnose.py
grep -n '@app.get("/diagnostics")\|/runs/{run_id}/diagnose\|/runs/{run_id}/compare\|/load-runs/{run_id}/compare\|/runs/flakiness' packages/orchestrator/api/main.py
# topology port plan + readiness gate + 424
grep -n "port collision\|requires_topology\|_topology_is_up" packages/orchestrator/api/main.py
# stream resume + persistence env vars
grep -n "last_event_id\|ORCH_RUNTIME_FILE\|SIMULATORS_FILE\|RUN_DB" packages/orchestrator/api/main.py
# TCP reconnect/framing
grep -n "_reconnect\|length_prefix_bytes" packages/worker/adapters/tcp/adapter.py
```

Volatile facts most likely to drift: orchestrator `main.py` line numbers
(cited approximately), the `ORCH_PORT` compose mapping, and the
`@app.on_event("startup")` style (FastAPI is migrating the ecosystem to
lifespan handlers).
