---
name: payprobe-distributed-topology-campaign
description: >
  Executable, decision-gated campaign for implementing ADR-0001 — moving
  participant-flow topologies off the orchestrator process onto the
  Redis-coordinated worker fleet. Load this skill when the task mentions:
  distributed topology, ADR-0001, worker fleet hosting, flow_host,
  topology_coordinator, endpoint registry, scaling participant flows,
  topology HA, "orchestrator restart drops listeners", 20K TPS / 100K
  connection targets for topologies, or fleet-hosted FlowResponders. Also
  load it when asked "what is the hardest open problem in PayProbe" or to
  plan/execute/review any work that touches start_topology,
  _launch_participant, LoadBus topology messages, or worker-side listener
  hosting. Each phase has exact commands, expected observations, and
  measurable gates — execute it phase by phase, never skipping a gate.
---

# Distributed Topology Campaign (ADR-0001)

The hardest live problem in PayProbe, as an executable campaign. Everything in
"Current state" below was verified against the repo on **2026-07-03**; everything
in Phases 2+ is **NOT BUILT** — this is a plan over verified ground truth, not a
description of existing code.

**Jargon (defined once):**

| Term | Meaning here |
|---|---|
| Participant flow | A graph (trigger → logic → reply nodes) that stands in for one party in a payment network (an issuer, a switch, an HSM). Runs as a *listener*. |
| Topology | A named set of participant flows × N instances, started/stopped as one unit (scenario-service `models/topology.py`). |
| FlowResponder | The worker class that hosts one flow instance as a TCP listener (`worker/adapters/tcp/flow_responder.py`, `class FlowResponder(FlowTraceMixin, TcpResponder)`). HTTP flows use `HttpFlowResponder`. |
| LoadBus | The coordinator↔worker transport for load runs (`worker/engine/load/bus.py`): `InMemoryLoadBus` (one process, dev/CI) and `RedisLoadBus` (real fleet). |
| Worker fleet | Separate `python -m worker.load_worker` processes coordinating through Redis; tracked by TTL heartbeats (`loadworker:{id}` keys, `WORKER_TTL_S = 15`). |
| Endpoint registry | NOT BUILT. ADR-0001's name for the map instance → live `host:port` that callers must consult once instances live on many hosts. |
| ISO 8583 | The binary message standard for card transactions; most PayProbe listeners speak it over TCP. |

## When NOT to use this skill

- General architecture questions, invariants, "why is it built this way" →
  **payprobe-architecture-contract**.
- Running/operating load tests, compose anatomy, scaling an existing fleet →
  **payprobe-run-and-operate**.
- Classifying/gating a change, flag rules, review protocol →
  **payprobe-change-control** (this campaign's promotion phase routes through it).
- Debugging a broken topology today → **payprobe-debugging-playbook**.

## Ground rules

**Non-negotiables (binding for every phase):**

1. **Measure, never assume.** Every phase starts by reproducing its claim with a
   command and comparing against the stated expected observation.
2. **Reversibility mandatory.** All new behaviour lands behind a flag, default
   OFF (proposed name: `PAYPROBE_TOPOLOGY_FLEET`; it does not exist yet — creating
   it is part of Phase 4). The in-process path must remain the dev/CI default.
3. **Suite green before anything.** `make test` passes before you start and after
   every phase. Known failures may not accumulate.

**Design convention (not a non-negotiable — deviation requires an ADR, per
`payprobe-change-control`):** reuse existing seams (LoadBus, heartbeats,
run_control, SecretBox) — ADR-0001 and ADR-0002 both reuse machinery. Do not
fork a parallel transport or clustering stack without an ADR making the case.

---

## Phase 0 — Mission + current-state verification gate

**Objective:** prove the "flows are orchestrator-local" premise still holds
before planning anything on top of it. If any check below diverges, STOP and
re-read `docs/adr/0001-distributed-topology-on-worker-fleet.md` plus recent
`git log` — someone may have started this campaign already.

Run from repo root:

```bash
# 0.1 The ADR exists and is still Proposed (not Accepted/Superseded)
grep -n "Status" docs/adr/0001-distributed-topology-on-worker-fleet.md
# EXPECTED: **Status:** Proposed

# 0.2 The orchestrator process itself imports and hosts FlowResponder
grep -n "from worker.adapters.tcp.flow_responder import FlowResponder" packages/orchestrator/api/main.py
grep -n "^PARTICIPANTS: dict\[str, FlowResponder\]" packages/orchestrator/api/main.py
# EXPECTED: one hit each (import near top; module-level in-memory registry).
# This is the smoking gun: listeners live in the orchestrator's event loop.

# 0.3 Topology start launches instances in-process, not on any fleet
grep -n "_launch_participant\|def start_topology" packages/orchestrator/api/main.py | head
# EXPECTED: start_topology calls _launch_participant in a loop; no bus involved.

# 0.4 None of ADR-0001's new components exist yet
grep -rn "flow_host\|topology_coordinator\|topology\.place\|instance\.up" packages/ --include='*.py' | grep -v __pycache__
# EXPECTED: no output. If anything matches → the campaign has started; audit
# what exists against the phase list before writing code.

# 0.5 The LoadBus has no topology vocabulary
grep -n "topology" packages/worker/engine/load/bus.py
# EXPECTED: no output. Bus primitives today: push_shards / claim_shard /
# pending_shards / report_sample / samples / signal_stop / is_stopped /
# mark_done / signal_retune / get_retune / worker_heartbeat / list_workers /
# drop_worker / signal_worker_stop / is_worker_stopped.

# 0.6 Suite is green (env caveat: crypto/aiohttp failures in a sandbox are
# missing-deps, not regressions — see payprobe-build-and-env)
make test
# EXPECTED: exit 0. Collected sizes on 2026-07-03: orchestrator/tests = 274
# tests, worker/tests = 308 tests. Counts may only have GROWN since.
```

**Which process hosts the listeners (live proof, if a deployment is running):**

```bash
# Start any topology, then look at who owns the sockets. The orchestrator
# API is ${ORCH_PORT:-8100} in infra/docker/docker-compose.yml:
curl -s localhost:8100/topology-runs | python3 -m json.tool
# EXPECTED: endpoints all on the orchestrator host (127.0.0.1 / orchestrator
# container). In compose: `docker compose exec orchestrator ss -ltnp` shows the
# planned ports bound INSIDE the orchestrator container, none in any worker.
curl -s localhost:8100/load-workers
# EXPECTED: [] unless a load run is active — proving today's fleet only exists
# for load generation, never for hosting listeners.
#
# NOTE: the orchestrator auth gate FAILS CLOSED outside dev (packages/
# orchestrator/api/auth.py). Unless PAYPROBE_ENV=dev, add
#   -H "Authorization: Bearer $API_TOKEN"
# to every curl in this campaign.
```

**Gate G0 (all must hold):** 0.1–0.5 match expectations exactly; `make test`
exit 0. *If 0.4 or 0.5 shows matches instead* → inventory what exists, map it to
the phase list below, and resume at the first phase whose gate fails.

---

## Phase 1 — Baseline characterization (measure current behaviour)

**Objective:** a written, numeric baseline of the single-host implementation so
every later phase can prove "no regression" instead of eyeballing it.

The current implementation, by symbol (all in `packages/orchestrator/api/main.py`
unless noted; re-locate with `grep -n <symbol>` — line numbers drift):

| Concern | Symbol(s) | Verified behaviour (2026-07-03) |
|---|---|---|
| Instance launch | `_launch_participant`, `_build_flow_responder` | Builds FlowResponder/HttpFlowResponder (gRPC inbound rejected 400) in-process; registers in `PARTICIPANTS` dict. |
| Per-instance port plan | `start_topology` planning loop, `_flow_listen_target` | N instances of one flow get `base, base+1, …` from the inbound connection's single `port` (`listen_port` is legacy, folded on read); no base → ephemeral (port 0). Cross-flow (host,port) duplicate → HTTP 409 *before any listener starts*. |
| Readiness gate | `_run_health`, `_topology_is_up`, `create_run` | ready = `total > 0 and live == total` (live = registered AND bound port). A run with `requires_topology` set gets **HTTP 424** until ready. |
| Rollback on partial start | `start_topology` except-branch | Any launch failure stops every already-started instance; nothing lingers. |
| Persistence | `_persist_runtime`, `_autostart_runtime`, `RUNTIME_STATE_FILE` (`ORCH_RUNTIME_FILE`, default `:memory:`; compose sets `/data/runtime.json`) | Desired state = standalone flow ids + topology ids; restored on boot unless `DISABLE_PARTICIPANT_AUTOSTART=1`. |
| Bound initiator | `start_topology` initiator block, `stop_topology` | Topology's driver scenario auto-runs on start (failure surfaces as `initiator_error`, never blocks start) and is cancelled on stop. |
| Ownership guard | `_flow_in_running_topology`, `start_participant` | Starting a flow standalone while a topology owns it → 409. |
| Observability | `/peers`, `/participants/traces`, `/participants/trace/{cid}`, `/participants/capture` | All iterate the in-process `PARTICIPANTS` dict directly. |
| Chaos | `_chaos_capable`, `/simulators/{sid}/chaos*` | Chaos dial targets the `SIMULATORS` dict ONLY. Participants have **no** chaos endpoint today (FlowResponder inherits `set_chaos` from TcpResponder, but nothing exposes it). Do not "restore" participant chaos that never existed. |

**Commands:**

```bash
# 1.1 The topology + participant suites pass and cover the behaviours above
cd packages && python -m pytest orchestrator/tests/test_topology.py orchestrator/tests/test_participants.py -q
# EXPECTED (2026-07-03): 10 + 6 = 16 tests, all pass.
#   test_topology.py proves: distinct ports 8400/8401/8402 for 3 instances;
#   409 collision pre-bind; 424 gate incl. half-dead topology; persistence
#   snapshot/restore; initiator run + cancel; cross-listener trace stitching.

# 1.2 The machinery to REUSE is healthy
cd packages && python -m pytest worker/tests/test_load.py orchestrator/tests/test_load_workers.py orchestrator/tests/test_run_control.py orchestrator/tests/test_worker_provisioner.py -q
# EXPECTED (2026-07-03): 30 + 4 + 5 + 18 = 57 tests, all pass.

# 1.3 Record the live baseline (running deployment only): start your reference
# topology, capture /topology-runs health JSON, /participants ports, and — if
# an initiator drives traffic — steady-state by_mti counts after 60s. Save the
# JSON; Phases 4-7 diff against it.
```

**Gate G1:** 1.1 and 1.2 fully green; baseline JSON captured (or explicitly
recorded as "no live deployment — tests only"). Write the numbers down in your
working notes; they are the regression reference for every later gate.

---

## Phase 2 — Bus protocol design (topology messages on the LoadBus)

**Objective:** extend the LoadBus vocabulary with placement messages (ADR-0001
action item 2) — design reviewed and written down BEFORE code.

**What exists today vs what is needed:**

| Message | Today | Needed (NOT BUILT) |
|---|---|---|
| `push_shards` / `claim_shard` | Redis list + `BLPOP` — exactly one consumer per shard, fire-and-forget | `topology.place {placement_id, flow_id, instance_idx, config, flow_doc, downstream}` — same claim-queue pattern works: each placement claimed by exactly one host |
| — | — | `instance.up {placement_id, instance_id, host, port}` — advertisement; feeds the endpoint registry |
| `signal_stop(run_id)` | stop flag key, polled | `topology.stop {instance_id | topology_run_id}` — per-instance and per-run stop |
| `worker_heartbeat` / `list_workers` | TTL key `loadworker:{id}` (ex=`WORKER_TTL_S`=15) + index set; refresh every `WORKER_HEARTBEAT_S`=5 | Reuse as-is for flow hosts; heartbeat `info` gains `role: "flow_host"` + hosted instance ids |

**Theory obligations — write the answers into the design note before coding:**

1. **Delivery semantics.** `BLPOP` claim = *at-most-once*: a host that crashes
   after claiming but before binding loses the placement silently. For load
   shards that is acceptable; for listeners it is not. You must state the
   recovery authority: the coordinator treats "placement claimed but no
   `instance.up` within T_bind" as failed and re-queues it. Derive T_bind
   (bind is milliseconds; config fetch is one Redis read since the flow doc is
   embedded in the placement — mirror the load shard pattern where "a worker
   needs nothing but the bus to start"; 10s is generous, justify your number).
2. **Advertisement transport.** `instance.up` as a Redis Stream (`XADD`, like
   metric samples) gives replayable history but requires the registry to
   compact; a TTL key per instance (`topoinst:{id}`, like `loadworker:{id}`)
   makes liveness and registration THE SAME mechanism — recommended, because
   the readiness gate then needs no second liveness source. State your choice
   and why.
3. **Heartbeat/failover math.** Worst-case dead-listener detection with TTL
   keys = `WORKER_TTL_S` = 15s. Failover budget = detection (≤15s) + re-place
   (one queue round-trip) + re-bind + re-advertise. If the topology readiness
   gate must not flap during a single missed beat, require age > TTL (not
   age > heartbeat interval) before declaring an instance dead. Write the
   numbers down; Phase 6's chaos test asserts them.
4. **In-memory parity.** Every new bus method gets an `InMemoryLoadBus`
   implementation with identical semantics — that is what keeps dev/CI
   Redis-free (ADR-0001 action item 7). The Protocol class in
   `worker/engine/load/bus.py` is the single source of the contract.

**Gate G2 (measurable):** a design note exists in the repo (`docs/` or the ADR's
own file, per **payprobe-docs-and-writing**) answering obligations 1–4 with
numbers; new Protocol methods stubbed on BOTH buses; `make test` still green
(stubs may not break the 57-test reuse baseline from G1).

---

## Phase 3 — Worker-side hosting: the `flow_host` role

**Objective:** a `python -m worker.flow_host` process that claims placements,
runs FlowResponders, advertises endpoints, heartbeats (ADR-0001 action item 1).

**Rules:**
- Model it on `packages/worker/load_worker.py` (362 lines — read it first): env
  `REDIS_URL` required, heartbeat task refreshing inside the TTL, clean
  `drop_worker` on exit. Key difference: `load_worker` claims ONE shard and
  exits when done; `flow_host` is long-lived and hosts MANY instances.
- The placement payload must embed everything (flow doc, resolved listen config,
  resolved downstream adapter map) so the host never calls scenario-service.
  The resolution logic already exists orchestrator-side
  (`_participant_listen_config`, `_participant_downstream`,
  `_build_flow_responder`) — move/share it, do not duplicate it. Watch the
  relay special case: `_relay_node` terminal → TcpProxy, not FlowResponder.
- Secrets in downstream configs travel like load shards do today; anything
  encrypted at rest uses SecretBox (`packages/payprobe_common/crypto.py`; background in `docs/history/project-review.md`).

**Commands / expected:**

```bash
# 3.1 New unit tests, in-memory bus only (no Redis in CI):
cd packages && python -m pytest worker/tests/test_flow_host.py -q
# EXPECTED: covers at minimum — claim→bind→advertise happy path (instance.up
# carries the REAL bound port, incl. ephemeral port-0 case); topology.stop for
# one instance stops only that instance; host crash simulation = heartbeat key
# expiry; two hosts + N placements = each placement claimed exactly once.

# 3.2 Manual smoke with real Redis (optional but recommended):
# terminal A: REDIS_URL=redis://localhost:6379 python -m worker.flow_host
# terminal B: push a placement via a scratch script; then:
redis-cli keys 'topoinst:*'   # or XLEN of your advertisement stream
# EXPECTED: one advertisement with a live host:port; `nc <host> <port>` connects.
```

**Gate G3:** new flow_host tests green; full `make test` green; worker test
count strictly greater than the 308 baseline; ZERO changes yet to
orchestrator start_topology behaviour (G1's 16 topology/participant tests
still pass byte-identical).

---

## Phase 4 — Orchestrator delegation: `topology_coordinator` + fallback retention

**Objective:** a `topology_coordinator` (parallel to `load_coordinator`) that
places instances over the bus, collects advertisements into the endpoint
registry, rolls back partial placement, and tracks fleet health in
`TOPOLOGY_RUNS` (ADR-0001 action item 3) — behind the new flag, default OFF.

**Rules:**
- Flag: `PAYPROBE_TOPOLOGY_FLEET` (unset/0 = today's in-process path,
  bit-for-bit). Register the flag per **payprobe-config-and-flags**' add-a-flag
  checklist. The in-process path is not "legacy" — it is the permanent dev/CI
  fallback (ADR-0001 explicitly recommends keeping it the default there).
- Mirror `LoadCoordinator`'s structure: constructor takes bus + run_store-like
  deps; `start()` pushes placements; background tasks aggregate advertisements
  and watch liveness. Reuse `run_control` for cross-replica stop registration
  (`payprobe:runs` hash + `payprobe:run-cancel` pub/sub) — do not invent a
  second cancel path.
- Partial placement rollback now spans hosts: on any placement failing its
  T_bind deadline, issue `topology.stop` for every already-up instance of that
  run, then surface the same HTTPException the in-process path raises today.
- Follow the in-proc cap pattern: `LoadCoordinator` refuses in-process work
  above `inproc_max_tps=2000` / `inproc_max_connections=5000` and emits an
  actionable notice instead of silently degrading. The topology analog: with
  the flag ON but zero live flow hosts, FAIL the start with a notice containing
  the copy-paste worker command (see `worker_provisioner.manual_command` for
  the pattern) — never silently fall back to in-process hosting when the
  operator asked for fleet hosting, and never host unbounded listeners in the
  orchestrator loop.

**Commands / expected:**

```bash
# 4.1 Flag OFF (default): the entire existing suite is untouched
cd packages && python -m pytest orchestrator/tests -q
# EXPECTED: ≥274 tests, green, no test edited to accommodate the new code path.

# 4.2 Flag ON, in-memory bus, in-proc flow-host task (the CI stand-in for a
# fleet — same trick LoadCoordinator uses with in_proc_worker):
cd packages && python -m pytest orchestrator/tests/test_topology_coordinator.py -q
# EXPECTED: place → advertise → run ready; partial failure → cross-host
# rollback → 4xx; registry lists every instance's host:port.

# 4.3 Flag ON with no hosts:
# EXPECTED: topology start fails fast with the actionable notice; nothing binds
# in the orchestrator process.
```

**Gate G4:** 4.1–4.3 as stated; `git grep PAYPROBE_TOPOLOGY_FLEET` shows the
flag read in exactly one place (coordinator selection), documented default OFF.

---

## Phase 5 — Port plan and readiness on a multi-host fleet

**Objective:** adapt the per-instance port planner and the `requires_topology`
gate to registry reality (ADR-0001 action items 4 and 5).

**Theory obligation — port collision across hosts.** Today's planner allocates
`base+i` and rejects duplicate `(host, port)` pairs — sound on ONE host. Across
hosts, `(host, port)` uniqueness is only known AFTER placement (two hosts can
both bind 8400 legitimately; one host given two instances of base 8400 cannot).
Two policies (ADR-0001 "Revisit" leaves this open):

| Policy | Mechanics | Verdict |
|---|---|---|
| **Ephemeral + advertise (recommended)** | Fleet placements always bind port 0; the OS picks; `instance.up` advertises the real port; callers only ever read the registry | Eliminates the collision class entirely; the fixed-port UX survives on the in-process path where it is actually meaningful |
| Assigned ranges per worker | Each host owns a port range; coordinator allocates within it | Preserves predictable ports but adds range bookkeeping, exhaustion handling, and a new config axis — only justify if some caller genuinely cannot do discovery |

Whichever you pick, derive: max instances per host, behaviour when a host
restarts and re-binds different ports (registry must be updated, callers must
re-resolve — this is why group resolution moves to dispatch time).

**Discovery:** groups/connections resolve to registry endpoints at dispatch /
run-build time — extend `_attach_groups` / `_attach_connections` (they already
rewrite step targets; verified in `orchestrator/tests/test_groups.py` and
`test_connections_wiring.py`). Readiness becomes: every placement registered
AND advertisement fresh (age < TTL) — `_run_health` / `_topology_is_up` consult
the registry when the flag is ON.

**Gate G5 (measurable):**
```bash
cd packages && python -m pytest orchestrator/tests/test_topology.py orchestrator/tests/test_groups.py -q
# EXPECTED: original port-plan tests (8400/8401/8402, 409 pre-bind) still pass
# UNCHANGED with flag OFF; new flag-ON tests prove: registry-resolved group
# dispatch reaches a fleet instance; 424 until ALL advertisements fresh; a
# stale advertisement (simulated expiry) flips ready → false.
```

---

## Phase 6 — Lifecycle: cross-replica stop, worker death, crash/reconcile

**Objective:** the failure modes ADR-0001 flags as "Harder" (action item 6),
proven by tests, not argued.

**Sub-tasks:**

1. **Cross-replica stop.** Register topology runs with `run_control` so a stop
   arriving at replica B reaches the coordinator on replica A (exact pattern:
   load runs already do this — `orchestrator/tests/test_run_control.py`, 5
   tests, is your template).
2. **Worker death → re-place.** Coordinator watches instance liveness (TTL
   expiry); on death, re-queues the instance's placement and updates the
   registry. Bound the flap: derive from Phase 2 math (detection ≤15s +
   re-place + re-bind) and assert the budget in the test.
3. **Crash/reconcile interplay.** Study `run_store.reconcile_orphans` +
   `_reconcile_stuck_load_runs` + `POST /load-runs/reconcile` (built for load
   runs stranded as "running" after an orchestrator crash). Topology runs today
   live only in the in-memory `TOPOLOGY_RUNS` dict + the desired-state file.
   Under fleet hosting, an orchestrator crash leaves REAL listeners running on
   workers with no owning run record. Decide and document: on boot, the
   coordinator re-adopts fleet instances whose advertisements match persisted
   desired state, and stops orphans that match nothing (the topology analog of
   reconcile_orphans; expose it on the existing reconcile surface, don't invent
   a second one).
4. **Persistence.** `_persist_runtime` / `_autostart_runtime` keep working under
   the flag: desired state (topology ids) is host-agnostic, so restore = ask the
   coordinator to ensure placements, adopting live instances instead of
   double-placing them. `DISABLE_PARTICIPANT_AUTOSTART=1` must still bypass.

**Gate G6 (measurable):**
```bash
cd packages && python -m pytest orchestrator/tests -q
# EXPECTED: green, and new tests exist proving each: (a) stop routed via
# run_control from a non-owning registry; (b) killed in-proc host task →
# instance re-placed, registry updated, ready flips false→true within the
# derived budget; (c) coordinator restart with live instances → re-adopt, not
# double-place (instance count unchanged); (d) orphan instance with no desired
# state → stopped by reconcile.
```

---

## Phase 7 — Feature-parity checklist (flag ON must lose nothing)

Every row below is a behaviour verified to exist on the in-process path on
2026-07-03. Parity means: with `PAYPROBE_TOPOLOGY_FLEET=1`, the same API call
gives the same shape of answer, now sourced from the fleet.

| # | Feature | Today's source | Parity proof (flag ON) |
|---|---|---|---|
| P1 | `/peers` participant rows | Iterates in-proc `PARTICIPANTS`, calls `r.peers()` | Peers of fleet-hosted listeners appear (needs a worker→orchestrator peers report; the heartbeat `info` dict is the cheap channel — same trick load workers use to ship tps/rss) |
| P2 | `/participants/traces` + `/participants/trace/{cid}` | Iterates `r.traces()` in-proc | Cross-hop trace stitches hops recorded on DIFFERENT hosts for one correlation id (this is the ADR's "aggregated across the fleet" item 8) |
| P3 | `/participants/capture` pause/resume + `DELETE /participants/traces` | Flips `_capture` on live objects | Capture toggle propagates to fleet hosts (bus control message), returns accurate buffered counts |
| P4 | Chaos dial | `/simulators/{sid}/chaos*` — SIMULATORS only; participants have no chaos endpoint | **No regression required**: simulator chaos is orchestrator-local and unaffected. Do NOT invent participant chaos in this campaign; if product wants it, that is a separate change through change control. Record this explicitly so a reviewer doesn't flag "missing" parity. |
| P5 | `requires_topology` → 424 | `_topology_is_up` over in-proc dict | Same 424 until fleet-ready (G5 test) |
| P6 | Persistence + boot restore | `_persist_runtime`/`_autostart_runtime` | G6(c,d) tests |
| P7 | Reconcile | load-run reconcile only | G6(d) topology reconcile |
| P8 | Bound initiator run/cancel | `start_topology`/`stop_topology` | Initiator fires only after fleet-ready; cancelled on stop |
| P9 | Standalone-vs-topology 409 guard | `_flow_in_running_topology` | Guard consults registry too |
| P10 | Network graph / topology map pages, MCP `list_topologies`/`list_topology_runs` | `/network-graph`, MCP proxy | Same JSON shapes; portal renders fleet endpoints without code changes (or the portal change ships in the same gated slice) |

**Gate G7:** a written checklist run — each row marked with the test name or
curl transcript proving it. Any row without evidence blocks promotion.

---

## Solution menu (ranked)

1. **Option B of ADR-0001 (chosen there; this campaign):** LoadBus + topology
   coordinator + endpoint registry, in-memory fallback preserved.
   *Obligations:* Phase 2 items 1–4 (delivery semantics, advertisement
   transport, heartbeat math), Phase 5 port policy derivation.
2. **Option B, minimal slice first:** ship only `flow_host` + placement +
   registry for SINGLE-instance flows, keep groups/multi-instance in-process;
   widen later. Lower risk, two flag states to test. Acceptable if a deadline
   forces it — the gates still apply per slice.
3. **Option C (k8s deployments per flow):** rejected by the ADR — platform
   coupling, slow start/stop vs the ephemeral test-network workflow, and you
   STILL must build the endpoint registry. Only revisit if PayProbe becomes
   k8s-only operationally; that is an ADR supersession, not a campaign detour.
4. **Option A (status quo):** legitimate "do nothing" — the ADR itself notes
   the single-host path is solid post port-fix. Choosing it = closing ADR-0001
   as Rejected with the scaling targets re-scoped. That is a product decision;
   route it through change control, don't let the campaign silently stall.

## Wrong paths — fenced, with archaeology

- **Do NOT reintroduce per-connection `endpoints[]` / `routing.py`.** Built,
  then REMOVED in commit `fe59454` ("remove deprecated endpoint selection
  model") because it confusingly overlapped participant groups. The endpoint
  registry is RUNTIME state keyed by placement, not a config-model field on
  connections. If you find yourself editing the connection model, stop.
- **Do NOT run flows in the orchestrator loop beyond the capped in-proc
  pattern.** The whole ADR exists because listeners contend with the API event
  loop. Follow `LoadCoordinator`'s cap-and-notice discipline (Phase 4); a
  silent in-process fallback under the fleet flag recreates the problem while
  claiming to fix it — silent degradation is a documented costliest-failure
  class in this repo.
- **Do NOT fork a parallel event/coordination transport.** One bus
  (`LoadBus`, Redis + in-memory twin), one heartbeat scheme, one run_control.
  A second Redis schema or a new pub/sub layer doubles the operational model
  the ADR explicitly chose Option B to avoid.
- **Do NOT break the single-port model or typed groups.** Connections carry ONE
  `port` for both directions (`listen_port` is legacy, folded on read —
  self-heals); groups are typed to one adapter family and validated. The
  registry maps logical instance → advertised address; it must not resurrect
  per-direction ports or untyped member lists.
- **Do NOT edit existing green tests to make new code pass.** The 16
  topology/participant tests and the 57 reuse-machinery tests are the contract;
  flag-OFF behaviour changes are regressions by definition.

## Validation and promotion protocol

Route through **payprobe-change-control**. Order is mandatory:

1. Flag `PAYPROBE_TOPOLOGY_FLEET` exists, default OFF, documented
   (payprobe-config-and-flags checklist).
2. `make test` green with flag OFF (whole suite) AND the flag-ON test set green
   on the in-memory bus (Gates G3–G6).
3. Feature-parity checklist G7 completed with evidence per row
   (P1–P3, P5–P10; P4 recorded as intentionally out of scope).
4. Real-Redis staging soak: compose deployment with ≥2 `flow_host` processes,
   reference topology up ≥1h, one deliberate host kill mid-soak; assert
   recovery within the Phase 2 budget and zero orphan sockets after stop
   (`ss -ltn` on every worker container).
5. Flip the flag ON in `infra/docker/docker-compose.yml` (orchestrator env
   block — same block that already sets `REDIS_URL`, `ORCH_RUNTIME_FILE:
   /data/runtime.json`, `SIMULATORS_FILE`, `PAYPROBE_WORKER_PROVISIONER`).
   Dev/CI stays flag-OFF (ADR recommendation).
6. Update `docs/adr/0001-distributed-topology-on-worker-fleet.md`: Status
   Proposed → Accepted (implemented), tick the action items, record the
   port-policy and delivery-semantics decisions in Notes. Update docs/history/PROGRESS.md
   per house style (payprobe-docs-and-writing).

## Rollback plan

- **Instant (config):** unset `PAYPROBE_TOPOLOGY_FLEET` in compose, restart the
  orchestrator. Boot restore (`_autostart_runtime`) re-launches persisted
  topologies in-process — the desired-state file is host-agnostic by design, so
  no data migration exists in either direction.
- **Cleanup after rollback:** stray fleet listeners are stopped by the Phase 6
  reconcile (orphans matching no desired state) or, bluntly,
  `docker compose stop <flow-host services>`; verify with `curl /peers` and
  `ss -ltn` on worker hosts showing zero topology ports.
- **Code rollback:** the flag isolates every new call site; reverting the
  enabling commit(s) must leave the flag-OFF suite green — which is exactly
  what Gate G4.1 proved continuously.
- **Trigger examples (decide thresholds before the flip, per change control):**
  readiness flapping without host deaths, initiator error rate above the G1
  baseline, or any parity row regressing in production use.

## Provenance and maintenance

All "current state" claims verified 2026-07-03 against the working tree
(orchestrator suite = 274 collected, worker = 308 collected; ADR-0001 Status:
Proposed; no `flow_host`/`topology_coordinator`/`topology.place` symbols).
Re-verify before executing:

```bash
grep -n "Status" docs/adr/0001-distributed-topology-on-worker-fleet.md
grep -rn "flow_host\|topology_coordinator\|topology\.place\|instance\.up" packages/ --include='*.py' | grep -v __pycache__
grep -n "topology" packages/worker/engine/load/bus.py
cd packages && python -m pytest orchestrator/tests worker/tests --collect-only -q | tail -1
git log --oneline -5 -- packages/orchestrator/api/main.py packages/worker/engine/load/ docs/adr/
```

If any check diverges from Phase 0's expectations, this campaign has moved:
re-run Phase 0, map findings onto the phase gates, and resume at the first
failing gate. Line numbers cited nowhere, symbol names everywhere — use
`grep -n <symbol>` to relocate. Maintainer of record for the phase structure:
whoever last edits this file (update the date above when you do).
