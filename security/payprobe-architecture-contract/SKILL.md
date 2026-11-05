---
name: payprobe-architecture-contract
description: >
  Load this skill when you need to understand WHY PayProbe is built the way it
  is before changing it: adding/modifying a service, adapter, connection,
  environment, group, or run-control path; wondering "can I just add a field to
  Connection?", "why is there both a worker and an orchestrator?", "where do
  per-environment values live?", "why does my step resolve to a connection I
  never named?", "why did the orchestrator refuse my load run?", "can I add
  endpoints[] to a connection?" (NO — read this first); or reviewing a design
  for conflicts with standing decisions. Contains the load-bearing design
  decisions with rationale, the invariants that must hold (with what breaks if
  violated and the file that enforces each), ADR summaries, and the known weak
  points stated plainly.
---

# PayProbe Architecture Contract

The decisions that hold the platform together, WHY each one exists, and what
breaks if you violate it. Verified against the repo 2026-07-03. This is a
*contract*: if a change you're planning contradicts something here, either the
change is wrong or this document and an ADR must change first — never silently.

**Jargon, defined once:**
- **ISO 8583** — the wire format banks/card networks use for card transactions
  (bitmap header + numbered data elements).
- **HSM** — Hardware Security Module; a network appliance that does payment
  crypto (PIN blocks, CVVs, MACs). PayProbe simulates a Thales payShield 10K.
- **Adapter** — worker-side client class that speaks one protocol (TCP/ISO 8583,
  HTTP, gRPC, HSM host commands, DB probe) to a target system.
- **Connection** — a *named, saved* configuration record (host/port/protocol…)
  that becomes an adapter instance at run time.
- **Participant flow / group / topology** — simulated network members: a flow is
  one scripted responder, a group is N interchangeable members behind one name,
  a topology starts a whole set as a unit.
- **TPS** — transactions per second.

## When NOT to use this skill

| You want | Use instead |
|---|---|
| The story of how a decision was reached, dead ends, removed features | `payprobe-failure-archaeology` |
| Concrete env var / flag values, defaults, add-a-flag checklist | `payprobe-config-and-flags` |
| Symptom-driven debugging | `payprobe-debugging-playbook` |
| The ADR-0001 implementation campaign | `payprobe-distributed-topology-campaign` |

---

## 1. Service topology — what runs where and why it's separate

All code lives under `packages/`. Run the suite from repo root: `make test`.

| Package | Boundary (what it owns) | Why it is separate |
|---|---|---|
| `packages/worker` | The async **execution engine**: adapters, three-phase engine (`worker/engine/engine.py`), load engine (`worker/engine/load/`), simulators/responders (`worker/adapters/`), code-node runner. No HTTP API of its own; it is a library plus `python -m worker.load_worker` processes. | Execution must scale horizontally and crash independently of control. Anything that opens sockets to targets lives here so the orchestrator can stay a control plane. |
| `packages/orchestrator` | **Control plane** (FastAPI): run lifecycle, phase gating, WebSocket event streaming, load coordination (`api/load_coordinator.py`), topology/simulator lifecycle, chaos, diagnostics, reports endpoints. | One place that owns "what is running"; it must survive worker churn and be replaceable per-replica (see run_control invariant). |
| `packages/scenario-service` | **Configuration of record** (FastAPI): scenarios, connections, environments, formats, starter flows, participant groups, test data, secrets inventory, agent tools. | Config outlives any run and is edited by humans/AI independently of execution. Separating it lets the orchestrator treat config as read-mostly input (`_attach_connections` fetches over HTTP). |
| `packages/auth-service` | **Identity**: issues short-lived HS256 JWTs; user/role management. Orchestrator + scenario-service only *verify* (shared `AUTH_JWT_SECRET`). | Single source of identity; verification stays local and cheap in every other service (see `packages/auth-service/README.md`). |
| `packages/report_service` | A **pure library**, not a service: JUnit/HTML/certification/diff generators over a run-detail dict (`packages/report_service/__init__.py` states this contract). Imported by the orchestrator. (`packages/report-service/` with a hyphen is a README-only stub.) | Format logic is dependency-free and testable in isolation; it can be lifted into a real service later without touching format code. Do not add I/O or FastAPI imports to it. |
| `packages/mcp-server` | **AI surface**: FastMCP proxy exposing scenario-service + orchestrator tools over Model Context Protocol. Authenticates outward via `_auth_header()` in `packages/mcp-server/mcp_server/tools.py` (static bearer or self-minted JWT). | AI clients get a curated, typed tool surface instead of raw HTTP; keeps agent capabilities auditable in one file. |
| `packages/payprobe-assistant` | **Unified LLM gateway** + the multi-turn tool-calling configuration assistant (standalone service). | LLM credentials/routing in exactly one process; other services call it, never providers directly. |
| `packages/portal` | Angular UI. Talks only to the HTTP APIs. | UI cadence and toolchain are decoupled from backend releases. |
| `packages/payprobe_common` | Shared small utilities (e.g. `SecretBox` in `payprobe_common/crypto.py`). | Avoids cross-service imports of service internals. |
| `packages/helpers` | Misc dev helpers. | Not part of the runtime contract. |

**Design convention (strong, but not a confirmed hard rule): no parallel
stacks.** New capabilities reuse existing seams — adapters, the LoadBus, the
event backbone — rather than introducing sibling mechanisms. ADR-0001 and
ADR-0002 both follow this pattern.

---

## 2. Execution model: three phases as blast-radius gating

**Where:** `packages/worker/engine/engine.py` (module docstring is the spec).

- **Phase 1 — Components:** `health_check()` on every adapter in the environment.
- **Phase 2 — Integration:** scenarios with `test_class` in `{"component", "integration"}` (`PHASE_2_CLASSES`).
- **Phase 3 — End-to-End:** scenarios with `test_class` `"e2e"` (`PHASE_3_CLASSES`).

**WHY:** blast-radius containment. A scenario is marked **BLOCKED** (not
FAILED) when it depends on a target that failed an earlier gate: phase-1
failures block any scenario touching the unhealthy target; a phase-2 failure
blocks e2e scenarios touching that target. This keeps a single dead host from
producing hundreds of misleading FAILED results and makes reports readable.

**What breaks if violated:** if you run e2e scenarios against targets that
failed health checks, every downstream failure is noise and the report's
per-phase table (`packages/report_service/generators.py`, "Phase results")
loses meaning. Diagnosis regresses to log archaeology.

**Also load-bearing here:** two semaphores cap total outbound connections and
concurrent steps (`connection_semaphore`, `ops_limiter`), sized from the
environment's `connection_budget`. Phase 1 retries unhealthy components once
after `phase1_retry_delay_sec` (default 1.0s) — long enough for a relay's
stale-upstream reconnect.

---

## 3. Invariants

Each entry: the rule, WHY, what breaks if violated, and the enforcing file.

### 3.1 Adapter registry: instance name ≠ implementation

**Rule:** environments declare *named instances* under `adapters`; each picks
its implementation via the `adapter` (alias `type`) key. Real adapter classes
are imported lazily and registered in `ADAPTER_MAP` only if their optional
dependencies are installed.

**Enforced by:** `packages/worker/adapters/registry.py` (`ADAPTER_MAP`,
`AdapterRegistry`, `_register_real_adapters`). Config composition:
per-instance `extends` + env-level `adapter_defaults`, deep-merged, instance
wins (`_config_for`).

**WHY:** one deployment can talk to several switches, a primary and a backup
HSM, etc., without one class per target; and a missing optional dep (grpcio,
crypto libs) must not break import of the whole worker. Import failures are
logged at debug so a *broken* adapter module is distinguishable from
"dep not installed" — this distinction was learned the hard way (silently
vanishing adapters resurfacing as "Unknown adapter").

**What breaks:** hard-importing an adapter at module top level makes the worker
unimportable wherever that dep is absent (CI, slim images). Keying behaviour on
the instance *name* breaks multi-instance environments.

### 3.2 Derived adapters are named `{target}@{env}`

**Rule:** when a step pins `environment_override`, the orchestrator registers
that environment's adapter for the step's target under the derived name
`f"{target}@{override}"` and re-points only that step at it.

**Enforced by:** `_attach_step_environments` in
`packages/orchestrator/api/main.py` (tests:
`packages/orchestrator/tests/test_step_environments_wiring.py`).

**WHY:** one run can hit staging for one step and the default env for the rest
without mutating the shared adapter entry. The derived name is collision-free
and self-describing in traces/reports. Resolution is deliberately best-effort:
unknown env / unreachable scenario-service / missing adapter leaves the step on
its default target rather than failing the run.

**What breaks:** writing the override into the base adapter entry silently
changes *every* step using that target; failing hard on a missing override env
turns a cosmetic config gap into a dead run.

### 3.3 Connection = hub; the override matrix is the single per-env value source

**Rule:** a connection is the single source of truth for its values. Base
config holds the shape and defaults; `environment_overrides` (dict keyed by
environment name, each a partial worker-shaped config) holds per-environment
values, shallow-merged over base at attach time. Metadata keys
(`_NON_ADAPTER_KEYS = {"name", "environments", "environment_overrides",
"default"}`) are stripped before the worker sees the config.

**Enforced by:** `ConnectionDraft.environment_overrides` in
`packages/scenario-service/api/connection_store.py`; merge in
`_connection_effective` + `_attach_connections` in
`packages/orchestrator/api/main.py`. The flag `_CONNECTION_OVERRIDE_WINS`
(env `PAYPROBE_CONNECTION_OVERRIDE_WINS`, **default ON**) makes the
connection's resolved config win over a same-named inline env adapter; `=0`
restores legacy precedence.

**WHY:** the costliest churn in project history was per-environment values
living in two places (environment adapter blocks *and* connections). One value
source per env, editable from either the Connection or the Environment editor
but stored on the connection, ends the ambiguity.

**What breaks:** reintroducing a second value source re-creates split-brain
config — a run's effective host/port depends on merge order nobody remembers.

**REMOVED — do not reintroduce:** per-connection `endpoints[]` + `selection`
multiplicity. It overlapped confusingly with participant groups, which are the
supported way to fan across several targets. The removal note is in the model
itself (comment block above `listen_port` in `connection_store.py`); the model
is `extra="allow"` so legacy records still load, and their endpoint fields are
ignored. If you need N interchangeable targets behind one name: use a
participant group.

### 3.4 Single `port`, both directions (`listen_port` deprecated, self-heals)

**Rule:** one `port` field serves outbound (dial) and inbound (bind). `mode`
selects direction; `port: 0` on inbound means pick a free port at bind time.

**Enforced by:** `_unify_port` model validator in
`packages/scenario-service/api/connection_store.py` — it folds any legacy
`listen_port` into `port` **on every load** and nulls it, so old records
self-heal without a re-save; `listen_port` is never persisted going forward.

**WHY:** two port fields caused the classic failure of dialing one port while
listening on another. A single field cannot disagree with itself.

**What breaks:** re-adding a second port field (or writing `listen_port`)
resurrects the split, and any code reading `listen_port` sees `None` after
validation.

### 3.5 Participant groups are typed to one adapter family

**Rule:** every member of a group must resolve to the same adapter family; the
family is validated and **stamped** onto the group as `adapter_type`.

**Enforced by:** `_type_participant_group` in
`packages/scenario-service/api/main.py` (raises HTTP 400 on mixed members or a
mismatched pre-set `adapter_type`; test:
`packages/scenario-service/tests/test_participant_group_typing.py`).

**WHY:** a group is one name serving one kind of traffic — the same
action/payload cannot serve both an HSM and an ISO 8583 host. The stamp lets
the portal and orchestrator know the family without re-deriving it.

**What breaks:** a mixed group would route ISO 8583 frames at an HSM (garbage
in, connection resets out) and the group adapter could not pick a protocol.

### 3.6 Event core: append-only stream, sink-agnostic, resumable

**Rule:** run events go through the `StreamBackbone` protocol
(`append`/`stream(after_id)`), not pub/sub. Two implementations:
`InMemoryStreamBackbone` (tests/dev/mock e2e) and `RedisStreamBackbone`
(Redis Streams XADD/XRANGE/XREAD) — the WebSocket handler is identical over
both.

**Enforced by:** `packages/worker/engine/stream.py` (the module docstring is
the rationale of record).

**WHY:** pub/sub is fire-and-forget — a dropped WebSocket or late-joining
watcher permanently loses history. Every event stored with a monotonic id
means a client reconnecting says "give me everything after id X", replays what
it missed, then tails live. This is exactly why portal refresh/reconnect
resumes mid-run instead of showing a blank monitor.

**What breaks:** publishing any run event outside the backbone makes it
invisible to replay; consumers that don't pass `after_id` back re-download or
lose history.

### 3.7 Durable RUN_DB + cross-replica run control

**Rule:** run history persists to SQLite by default outside dev
(`_default_run_db` in `packages/orchestrator/api/main.py`: explicit `RUN_DB`
wins; dev/test/CI get `:memory:`; anything else gets `RUN_DB_PATH`, default
`/data/runs.db`). Liveness and cancel of *in-flight* runs go through
`packages/orchestrator/api/run_control.py`: `InMemoryRunControl` (single
process) or `RedisRunControl` — registry in Redis hash `payprobe:runs`, cancel
fan-out on pub/sub channel `payprobe:run-cancel`; the replica owning the
asyncio task acts, others ignore.

**WHY:** the asyncio task executing a run lives in exactly one process. Without
this split, "stop run" only worked on the replica that happened to receive the
HTTP request, and a restart erased history. RunStore = durable document any
replica can read; run_control = the missing piece, acting on a run you don't
own. (Companion: `run_store.reconcile_orphans` marks runs stranded as
"running" after a crash.)

**What breaks:** cancelling by touching the local task dict only works on one
replica — users behind a load balancer get non-deterministic stop buttons.
Setting `RUN_DB=:memory:` in prod silently loses all history on restart (the
fail-safe default exists precisely because this happened).

### 3.8 Auth fails closed everywhere

**Rule:** every request is rejected unless a credential verifies OR the
deployment is explicitly dev. `packages/orchestrator/api/auth.py` is the gate;
`packages/scenario-service/api/auth.py` mirrors it by design ("fail closed
identically" — its docstring records the incident: orchestrator locked down
while scenario-service sat wide open). Accepted credentials: static bearer
`API_TOKEN` or a JWT verified with `AUTH_JWT_SECRET` (HS256) /
`AUTH_JWT_PUBLIC_KEY` (RS256), issued by auth-service. **The one escape
hatch:** `PAYPROBE_ENV` in `{dev, development, test, local}` makes auth
optional. `PUBLIC_PATHS` (health/ready/metrics/status/reference/openapi/docs)
stay open for probes and scraping.

**WHY:** misconfiguration in prod must be a loud 503, never an open door. The
default posture (unset env, no credentials configured) is *reject*.

**What breaks:** adding a route that bypasses `require_auth`, or widening
`PUBLIC_PATHS`, silently reopens the pre-hardening posture. Test:
`packages/orchestrator/tests/test_auth_gate.py`.

### 3.9 Code-node sandbox: netns isolation, `auto`/`strict`/`off`

**Rule:** user-supplied code nodes run in a subprocess wrapped in `unshare`
(`--user --map-root-user --net`, falling back to `--net`) so the snippet has
**no network egress**. Mode via `PAYPROBE_CODE_SANDBOX`: `auto` (default —
isolate if the host can, else run best-effort), `strict` (no sandbox available
⇒ **refuse to run**, raising the dedicated error), `off`.

**Enforced by:** `packages/worker/engine/code_runner.py` (`_sandbox_mode`,
the unshare probe; tests: `packages/worker/tests/test_code_sandbox.py`).

**WHY:** code nodes are arbitrary Python from the scenario editor. Network
isolation is the boundary that keeps "test helper snippet" from becoming
"exfiltration primitive" on a shared deployment. `strict` exists because
`auto` on a host without unshare degrades silently.

**What breaks:** executing code nodes in-process, or ignoring `strict`, gives
editor users the worker's network identity and credentials.

### 3.10 In-process load fallback is capped — the orchestrator refuses above it

**Rule:** when no external `python -m worker.load_worker` processes claim the
shards, the coordinator can run load workers *inside the orchestrator event
loop* — but only up to `PAYPROBE_INPROC_MAX_TPS` (default **2000**) /
`PAYPROBE_INPROC_MAX_CONNECTIONS` (default **5000**). Above the cap it refuses
the run, logs, and the portal shows "Action needed: start external workers".
`PAYPROBE_LOAD_EXTERNAL_WORKERS=1` disables the fallback entirely on a real
fleet.

**Enforced by:** `_inproc_demand` + the refusal branch in
`packages/orchestrator/api/load_coordinator.py`; cap values wired in
`packages/orchestrator/api/main.py`.

**WHY:** driving 20K TPS in the control plane's own event loop starves the
API/WebSocket loop — the platform would DoS itself and drop the very event
stream you're using to watch the run. Refusing loudly beats degrading
silently.

**What breaks:** raising the caps instead of starting workers turns every big
load run into an orchestrator brownout with garbage latency numbers (the load
generator competing with its own measurement plane).

### 3.11 Default-connection resolution (bare steps → type default, flag ON)

**Rule:** an action step that names NO connection resolves to the **default
connection for its adapter type** (at most one default per type, enforced by
`ConnectionStore` demoting the previous default). No default for the type ⇒
the step falls back to the environment's inline adapter — retained on purpose
so a not-yet-seeded type degrades gracefully. Flag
`PAYPROBE_DEFAULT_CONNECTION_RESOLUTION` **defaults ON**; `=0` restores legacy
(bare targets hit the env adapter).

**Enforced by:** `_DEFAULT_CONNECTION_RESOLUTION`, `_conn_type_key`,
`_target_type_key`, and the "Phase C" block of `_attach_connections` in
`packages/orchestrator/api/main.py`; `default: bool` on `ConnectionDraft` in
`packages/scenario-service/api/connection_store.py` (spec:
`docs/history/DEFAULT-CONNECTION-MODEL-SPEC.md` at repo root).

**WHY:** authors shouldn't need to bind every step; "the ISO 8583 step goes to
the ISO 8583 default" matches intent. Type keys are deliberately coarse — the
TCP adapter's two wire protocols are distinct types (`tcp/iso8583` vs
`tcp/header_echo`), everything else is one type per adapter.

**What breaks:** two connections marked default for one type makes resolution
order-dependent; changing `_target_type_key`'s mapping silently rebinds
existing scenarios' bare steps to different hosts.

---

## 4. ADRs (docs/adr/)

- **ADR-0001 — Run participant-flow topologies on the worker fleet.**
  **Status: Proposed** (not built). Today `start_topology` launches every flow
  instance inside the orchestrator process, so a topology is single-host, dies
  with the orchestrator, and cannot back the 20K TPS / 100K-connection
  targets. The accepted direction: move flow instances onto the existing
  Redis-coordinated worker fleet, reusing LoadBus, heartbeats, and the
  provisioner rather than building a parallel stack. This is the hardest live
  problem — the executable campaign lives in
  `payprobe-distributed-topology-campaign`.
- **ADR-0002 — Transparent TCP proxy / tap.** **Status: Proposed**, partially
  realized: stage-1 byte-exact tap relay exists (`TcpProxy`, connection
  `kind: "proxy"`), giving PayProbe a third posture — sitting in the middle of
  a live client↔upstream connection, relaying and observing. Intercept/stub/
  capture-to-scenario and TLS termination remain unbuilt; treat them as design
  intent, not capability.
- **ADR-0003 — Report gates, provenance, two-mode rendering.** **Status:
  Accepted — implemented.** Reports serve two unrelated jobs: *Improvement*
  (engineer mid-loop, high detail, throwaway) and *Go/No-Go* (approver at a
  gate, defensible verdict). Implemented as explicit gates + provenance +
  immutable certify + baseline in `packages/report_service/` and the
  orchestrator sign-off endpoints; do not blur the two modes back together.

---

## 5. Known weak points — stated plainly

Verified against `docs/history/project-review.md` and
`docs/standards-gap-analysis.md` (2026-07-03). These are open; do not let new
work silently depend on them being better than they are.

1. ~~**ISO 8583 WIRE codec is ASCII-only.**~~ **Closed 2026-09-24 by ADR-0011**
   (`docs/adr/0011-one-iso8583-codec-binary-wire.md`): one codec in
   `packages/payprobe_common/iso8583/` speaks ASCII, binary bitmap, BCD, EBCDIC and
   raw binary on the live socket, with BCD/binary length indicators; the worker,
   the Inspector and the catalog share it. Still open on the same line: no
   published-edition field dictionary and no DE padding/justification rules
   (see payments-domain-reference §1.5 and the standards gap doc's ISO 8583 row).
2. **Portal unit-test coverage is near zero.** ~12k+ lines of Angular; a
   Playwright e2e harness exists (golden paths, backend-free in CI; full flows
   gated behind `E2E_FULL`) but component unit coverage is thin and the
   auth/login UI ships essentially untested.
3. **Tracing is not threaded end-to-end.** OpenTelemetry scaffolding
   (`init_tracing`) exists; spans do not flow through a run. "Why is
   throughput low" still degrades to log reading.
4. **Scenario `secret_vars` are plaintext in Postgres.** Connection-file
   secrets are encrypted at rest (`SecretBox`, Fernet, `PAYPROBE_SECRET_KEY` —
   `packages/scenario-service/api/crypto.py` /
   `packages/payprobe_common/crypto.py`); the scenario-store `secret_vars`
   are masked in the UI but stored unencrypted.
5. **The architecture overview doc is stale.** `docs/architecture/overview.md`
   predates the load subsystem and gRPC and draws stub services as if built.
   Trust this skill and the code over that diagram.
6. **CI gaps.** No coverage gate. (mock-integration DOES poll `/health` in a
   retry loop — an older review's "fixed sleep" complaint is fixed. A security
   scan workflow exists: `.github/workflows/security-scan.yml` — Syft SBOM +
   Trivy.)

---

## Provenance and maintenance

Authored 2026-07-03 from direct code inspection. Re-verify before trusting
volatile claims (all commands from repo root):

```bash
# Service layout
ls packages/
# Three-phase engine + gating
sed -n '1,20p' packages/worker/engine/engine.py
# Adapter registry
grep -n "ADAPTER_MAP" packages/worker/adapters/registry.py
# {target}@{env} derivation
grep -n '@{override}' packages/orchestrator/api/main.py
# Connection hub / override matrix / endpoints removal / port unify / default flag
grep -n "environment_overrides\|listen_port\|endpoints\[\]\|default: bool" packages/scenario-service/api/connection_store.py
# Flags and caps (defaults)
grep -n "PAYPROBE_CONNECTION_OVERRIDE_WINS\|PAYPROBE_DEFAULT_CONNECTION_RESOLUTION\|PAYPROBE_INPROC_MAX" packages/orchestrator/api/main.py
# Typed groups
grep -n "_type_participant_group" packages/scenario-service/api/main.py
# Event backbone
sed -n '1,25p' packages/worker/engine/stream.py
# Run control + durable RUN_DB
sed -n '1,25p' packages/orchestrator/api/run_control.py && grep -n "_default_run_db" packages/orchestrator/api/main.py
# Auth gates
sed -n '1,25p' packages/orchestrator/api/auth.py && sed -n '1,10p' packages/scenario-service/api/auth.py
# Code sandbox
grep -n "PAYPROBE_CODE_SANDBOX" packages/worker/engine/code_runner.py
# In-proc load cap refusal
grep -n "inproc_max\|refuse" packages/orchestrator/api/load_coordinator.py
# ADR statuses
grep -n "Status" docs/adr/000*.md
# Weak points
grep -n -i "ascii\|secret_vars\|tracing\|portal" docs/history/project-review.md docs/standards-gap-analysis.md | head
```

If any command's output contradicts this file, the code wins — update this
skill and note the drift.
