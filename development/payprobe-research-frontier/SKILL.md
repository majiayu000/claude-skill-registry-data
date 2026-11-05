---
name: payprobe-research-frontier
description: >
  The four state-of-the-art ambitions for PayProbe and how to advance them:
  full-fidelity scheme simulation (binary/BCD/EBCDIC ISO 8583 on the wire),
  time-travel observability (Chronoscope replay as a regression artifact),
  AI-operated test platform (assistant + MCP + guardrails as the safety case),
  and chaos-certified payment resilience (a rigorous, repeatable certificate).
  Load this when asked "what should PayProbe do next", "what's novel here",
  "how do we beat the state of the art", "research direction", "publishable",
  "binary ISO 8583", "spec-exact VISA", "replay diff", "AI operates the
  platform", or "make the resilience certificate rigorous". Each ambition has
  verified assets, three concrete first steps in this repo, and a falsifiable
  milestone.
---

# PayProbe Research Frontier

Four ambitions where PayProbe can plausibly advance the state of the art in
payment-system testing. For each: why current ecosystem tools fall short,
which asset PayProbe already has (verified in this repo, 2026-07-03), the
first three concrete steps, and a **falsifiable** "you have a result when…"
milestone — measurable, never judged by eye.

**When NOT to use this skill:**

| You want… | Use instead |
|---|---|
| Current-state architecture, invariants, what is load-bearing today | `payprobe-architecture-contract` |
| The evidence bar, hypothesis→numbers discipline, idea lifecycle | `payprobe-research-methodology` |
| What may be claimed publicly and what must be proven first | `payprobe-external-positioning` |
| The ADR-0001 distributed-topology campaign specifically | `payprobe-distributed-topology-campaign` |

**Ground rules for everything below**

- Labels: **[BUILT]** = verified in this repo at the stated path. **[CANDIDATE]**
  = proposed, not built; treat as an idea entering the lifecycle defined in
  `payprobe-research-methodology`. **[general knowledge]** = claim about the
  outside ecosystem from training knowledge, not verified against vendors.
- Every milestone must pre-register its numbers *before* the runs (see
  `payprobe-research-methodology`); numbers given here are starting proposals,
  not policy.
- Nothing here licenses a public claim. A milestone met = evidence you may
  *start* the claims process in `payprobe-external-positioning`. PayProbe is
  PolyForm Noncommercial (source-available, not OSS); never position otherwise.
- Non-negotiables apply to frontier work too: measured not assumed,
  reversibility (flag-gated with rollback), `make test` green before and after.

---

## Ambition 1 — Full-fidelity scheme simulation

**Goal:** spec-faithful, scriptable simulators for card schemes, HSMs, and
gateways — including *binary* ISO 8583 on a live socket — runnable in CI by
anyone, no scheme sandbox access required.

### (a) Why current SOTA fails

[general knowledge] The ecosystem splits into two unsatisfying halves:

- **Commercial certification simulators** (Paragon FASTest, ACI ASSET-class
  tools, scheme-provided test systems such as Visa's own certification
  environments) are spec-faithful but closed, expensive, scheme-gated, and not
  scriptable inside an ordinary CI pipeline.
- **Open libraries** (jPOS, py8583-style ISO 8583 parsers) give you message
  *codecs* and a framework to build a simulator, but no stateful scheme
  behaviour (STIP decisions, reversals against original auths, network
  management), no HSM, no gateway, and no certification scoring out of the box.

The gap: an integrated, open-runnable stack where scheme + HSM + gateway
simulators, message-format registry, dialect validation, and certification
scoring live in one test platform.

### (b) PayProbe's specific assets (verified)

| Asset | Status | Path |
|---|---|---|
| VISA Base I simulator (auth/reversal/network-mgmt/clearing, opt-in CVV2/PVV/ARQC) | [BUILT] functional; spec-exact explicitly deferred | `packages/worker/adapters/scheme/visa.py` (`class VisaSimulator(TcpResponder)`, line ~120); `docs/simulators/visa-scheme.md` states spec-exact is "a follow-on phase" |
| payShield 10K HSM simulator, hybrid real crypto | [BUILT] | `packages/worker/adapters/hsm/payshield.py` (`class PayShieldSimulator(TcpResponder)`); command handlers `NC A0 BU CW CY CA EC M6 M8` as `@command(...)` in `packages/worker/adapters/hsm/commands.py` |
| CyberSource REST gateway sim on generic HTTP base | [BUILT] | `packages/worker/adapters/scheme/cybersource.py` (`class CyberSourceSimulator(HttpResponder)`); base `packages/worker/adapters/http/responder.py` |
| MessageFormat registry (1987 / 1993 / VISA / pacs.008 builtins) | [BUILT] | `packages/scenario-service/models/message_format.py` (`BUILTIN_FORMATS`) |
| Dialect validation on the live responder (warn/reject, violations on trace) | [BUILT] | `packages/worker/adapters/tcp/responder.py` (`validate` block, `validate_mode`, `invalid` counter) |
| Certification packs + scoring | [BUILT] | scenario-service `GET/POST /packs*` in `packages/scenario-service/api/main.py`; certification generators in `packages/report_service/generators.py`; MCP `run_certification` tool |
| **Binary/BCD/EBCDIC codec on the live wire** | [BUILT 2026-09-24, ADR-0011 Accepted, phases 0–5 on branch `feature/adr-0011-iso8583-codec`; format-encoding injection `PAYPROBE_ISO8583_FORMAT_ENCODING` default ON after a real-environment run, `0` is the escape hatch] | `packages/payprobe_common/iso8583/` (one codec, one field dictionary, per-field overrides); worker `adapters/tcp/iso8583.py` is a re-export; loopback proof `packages/worker/tests/test_iso8583_binary_wire.py`; golden contract `packages/worker/tests/test_iso8583_golden.py` |

**Status 2026-09-24: the blocker below is closed by ADR-0011** (`docs/adr/0011-one-iso8583-codec-binary-wire.md`): the codec moved to `payprobe_common/iso8583`, the worker wire path packs and unpacks bytes under a profile, `VisaSimulator` passes its flow set over a live socket under `binary`, and the wire bytes decode byte-identically with the shared codec (milestone (d) met by test). Phase 5 done the same day: a real-environment run against the live registry, then the flag flipped on and the docs flipped; the ADR is Accepted. The paragraph is kept as the record of what the gap was.

**The blocker as it stood (standards-gap #1).** The *analyzer* had
already gained binary profiles: `packages/scenario-service/models/iso8583_analyzer.py`
implements `resolve_encoding()` with an ASCII profile, a `"binary"` profile
(binary bitmap + packed-BCD numerics + raw binary fields + BCD length
prefixes), EBCDIC text via code page cp037, and a dict form for fine control
per axis (`bitmap: hex|binary`, `numeric: ascii|bcd`, `text: ascii|ebcdic`,
`binary: hex|raw`, `length: ascii|bcd`). This powers the Inspector's
analyze/build (`iso8583_analyze` / `iso8583_build`) — **offline messages
only**. The *live socket path* is still ASCII-only: the worker's wire codec
`packages/worker/adapters/tcp/iso8583.py` is by its own docstring a
"Self-contained ASCII ISO 8583 codec" (`iso_pack`/`iso_unpack`), used by
`TcpResponder._decode/_encode` and the tcp adapter. Note the docstring's
constraint: *the worker must not import from the scenario-service package* —
so closing the gap means porting or sharing the codec (e.g. via
`packages/payprobe_common`), a placement decision to make in step 1.
`docs/standards-gap-analysis.md` rates ISO 8583 "partial (functional but
ASCII-only)" and lists the binary codec path as recommendation #1.

### (c) First three steps in this repo

1. **Draft the codec-parity spec.** One document (repo `docs/`, Diátaxis
   explanation style — see `payprobe-docs-and-writing`) that (i) enumerates the
   five encoding axes exactly as `resolve_encoding()` defines them, (ii)
   decides codec placement given the no-import constraint (port into
   `packages/worker/adapters/tcp/iso8583.py` vs. extract to
   `packages/payprobe_common` consumed by both) — [CANDIDATE] either way, and
   (iii) defines where `encoding` is configured: as a field on the
   MessageFormat model (`packages/scenario-service/models/message_format.py`),
   defaulting to `"ascii"` so behaviour is preserved (reversibility rule).
2. **Write cross-codec golden tests first.** New
   `packages/worker/tests/test_iso8583_binary_wire.py`: for a fixed set of
   logical messages, assert the worker-side codec output is byte-identical to
   the analyzer's `iso8583_build` output for the same encoding profile. Seed
   cases from `packages/scenario-service/tests/test_iso8583_analyzer.py`.
   These tests fail until step 3 lands — that is the point (measure, never
   assume).
3. **Thread `encoding` through the live path.** Extend the worker codec, then
   `TcpResponder._decode/_encode` (`packages/worker/adapters/tcp/responder.py`)
   and the tcp adapter (`packages/worker/adapters/tcp/adapter.py`), resolving
   the profile from the bound message format at simulator start (the
   resolution hook already exists — the orchestrator resolves
   `message_format_id` when starting simulators). Finish with a loopback test:
   scenario step → live socket → `VisaSimulator` under the `"binary"` profile.

### (d) You have a result when…

A scenario run over a **live TCP socket** against `VisaSimulator` bound to a
binary-profile message format (binary bitmap + BCD numerics + BCD length
prefixes) passes the same flow set that `packages/worker/tests/test_visa_simulator.py`
covers in ASCII, **and** a capture of the wire bytes decodes via
`iso8583_analyze` with `encoding="binary"` to field values byte-identical to
what the sender intended, **and** `make test` is green with the ASCII default
untouched. Pass/fail is byte comparison and test exit codes — nothing is
judged by eye. (Spec-exact VISA field semantics remain a separate, later
milestone; do not conflate the two — see the "no oversell" rule.)

---

## Ambition 2 — Time-travel observability

**Goal:** make "scrub backwards through the whole simulated network, then hand
the replay file to a colleague or a CI job" a normal debugging and regression
workflow — correlated across topology, execution, and wire layers.

### (a) Why current SOTA fails

[general knowledge] Metrics/tracing stacks (Prometheus+Grafana, OpenTelemetry
+Jaeger/Tempo) answer "what were the numbers/spans" but cannot *replay* system
state; record-replay debuggers (rr, UDB) are single-process, not
distributed-topology; browser session-replay tools replay UI DOM, not backend
networks. Crucially, no mainstream tool treats a **replay file as a
first-class regression artifact** — something you export from a failing run,
attach to a bug, diff against a baseline, and re-inspect offline. Distributed
payment topologies (many simulators + flows + wire protocols) have no
equivalent of "attach the core dump".

### (b) PayProbe's specific assets (verified)

| Asset | Status | Path |
|---|---|---|
| Chronoscope: rolling buffer + time scrubber + replay transport | [BUILT] | `packages/portal/src/app/topologies/chronoscope/` (7 files: model, recorder service, orbital layout, scrubber/chronicle/inspector components, page component). `MAX_FRAMES = 240` at 2 s polls ≈ 8 min (`chronoscope.model.ts`) |
| Replay export **and** import (offline review mode) | [BUILT] | `chronoscope-recorder.service.ts`: `exportReplay()` and `importReplay(file)`; `ReplayFile` interface in `chronoscope.model.ts` (frames of `NetworkGraph` snapshots + chronicle events) |
| Live graph source | [BUILT] | `GET /network-graph` in `packages/orchestrator/api/main.py` — nodes with status, cumulative counts, peers |
| Execution trace: wire-level `raw_log` + timing on every step | [BUILT] | `StepOutcome.raw_log` + `duration_ms` in `packages/worker/engine/runner.py`; adapters populate it (e.g. `packages/worker/adapters/tcp/adapter.py` `_wire_log`); portal Trace tab with timing waterfall in `packages/portal/src/app/run-monitor/run-report.component.ts` |
| Network trace across participant flows | [BUILT] | `GET /participants/traces` in `packages/orchestrator/api/main.py` |
| Connected-peers view | [BUILT] | `GET /peers` in `packages/orchestrator/api/main.py` |

**The gap, stated precisely:** the layers are uncorrelated. `ReplayFile`
frames carry `seq`/`at`/`tps` + graph — **no run ids, no trace ids** (verified
against `chronoscope.model.ts`). You cannot yet click a chronoscope frame and
land on the execution-trace step or network-trace hop that was in flight.

### (c) First three steps in this repo

1. **Draft the correlation-key spec.** [CANDIDATE] Audit the three timelines —
   `ReplayFile.frames[].at` (client clock), `StepOutcome` timing (worker
   clock), `/participants/traces` entries (orchestrator clock) — and specify a
   shared key: run/trace id plus a single authoritative time base. Deliverable
   is a short spec in `docs/` naming exactly which fields are added where;
   clock-skew handling is the hard part, write it down before coding.
2. **Enrich frames at the source.** Extend `GET /network-graph`
   (`packages/orchestrator/api/main.py`) to include currently-active run ids /
   trace ids per node (the orchestrator already holds `SIMULATORS` runtime and
   run state in-process), then store them in the frame in
   `chronoscope-recorder.service.ts`. Flag the payload addition as additive
   (new optional fields only) so old replay files still import — reversibility.
3. **Build a replay-diff tool.** [CANDIDATE] A small standalone checker that
   takes two exported `ReplayFile` JSONs and reports structural differences:
   node status timelines, event sequences, per-node message-count deltas,
   frame gaps. Home it beside the other operational probes in
   `packages/helpers/` (existing pattern: `db-probe`, `hsm-probe`,
   `log-harvester`, `restpay-probe`) with its own tests. This is what turns a
   replay into a regression artifact: baseline replay + candidate replay →
   machine-readable diff, exit code non-zero on divergence.

### (d) You have a result when…

For a scripted incident (chaos storm on one simulator during a load run — both
primitives exist, see Ambition 4), you can: export the replay, re-import it in
a fresh session, and from the frame at storm onset navigate by shared id to
(1) the execution-trace step and (2) the network-trace hop that failed —
where "navigate" means the ids match programmatically, verified by a test that
walks replay JSON → `/runs/{id}` trace → `/participants/traces` and asserts id
equality; **and** the replay-diff tool run on baseline-vs-incident replays
exits non-zero and names the degraded node, while run on two baseline replays
of the same scenario it exits zero. All checks are id-equality and exit codes.

---

## Ambition 3 — AI-operated test platform

**Goal:** an AI agent safely operates PayProbe end-to-end — author scenario,
run, read evidence, fix, re-run, and *revert on demand* — with the safety case
resting on server-side guardrails and a journaled undo, not on prompt
discipline.

### (a) Why current SOTA fails

[general knowledge] AI testing tools today mostly *generate* tests (copilot
autocomplete, unit-test generators) or *self-heal* UI selectors; agent
frameworks can call APIs but platforms rarely offer a mutation surface that is
safe for an unattended agent: no transactional journal, no server-enforced
guardrails, no one-click revert of everything an agent session did. The
missing piece is not model capability — it is the platform-side **safety
case**: every write journaled, every guardrail enforced below the model, and
restoration provable. Payment test platforms in particular have no
"AI-operable" story at all.

### (b) PayProbe's specific assets (verified)

| Asset | Status | Path |
|---|---|---|
| MCP server exposing the platform | [BUILT] | `packages/mcp-server/`: **144 tools + 8 resources** registered from `mcp_server/registry.py` (`TOOL_SPECS` / `RESOURCE_SPECS`, counted by importing the module 2026-07-06; was 127 on 2026-07-03 — commit `0c1ceaa` added 17. The count drifts; recount, don't trust), each with `readOnlyHint`/`destructiveHint`/`openWorldHint` annotations; `tests/test_registry.py` keeps table↔module in sync |
| Conversational agent loop | [BUILT] | `packages/payprobe-assistant/assistant_service/loop.py` — bounded tool-calling loop (`max_iterations`), emits journal + iterations in its final event; REST facade in `rest.py`/`main.py` |
| Guardrails + change journal + revert (server-side) | [BUILT] | `packages/scenario-service/api/agent_tools.py`: `GuardrailError`, `ChangeJournal` (JSON-serialisable, restore derived from `before`), `restore_journal()`, `ChangeJournal.revert()`; module docstring: "Guardrails live here, not in the prompt." Endpoints `/agent/chat`, `/agent/chat/stream`, `/agent/revert` in `packages/scenario-service/api/main.py`; tests `test_agent_tools.py`, `test_agent_loop.py`, `test_agent_session.py` |
| NL→flow scenario assistant | [BUILT] | `POST /scenarios/assist` + `/assist/config` in `packages/scenario-service/api/main.py`; tests `test_assist.py` |
| **This skill library** | [BUILT, ongoing] | `.claude/skills/` — runbooks written so AI sessions can operate PayProbe are themselves part of this ambition: the agent's operating manual is a deliverable, not documentation overhead |

### (c) First three steps in this repo

1. **Inventory the unguarded mutation surface.** The journal/guardrail layer
   covers scenario-service writes routed through `agent_tools.py`. Many of the
   ~144 MCP tools mutate the *orchestrator* (start/stop simulators, load runs,
   chaos) with no journal. Produce the gap table mechanically: parse
   `mcp_server/registry.py` hints, list every non-`readOnlyHint` tool, and mark
   which have a journaled path. This is a read-only analysis — do it first;
   it defines the scope of "safe".
2. **Build a benchmark harness.** [CANDIDATE] A fixed task list (create
   scenario → validate → run → read report → deliberately misconfigure → fix →
   revert) executed through the MCP tool layer against a local stack, recording
   per-task success, tool-call counts, and journal coverage. Reuse the test
   scaffolding pattern in `packages/mcp-server/tests/` (it has a conftest and a
   fake-backend pattern; `packages/payprobe-assistant/tests/` likewise). The
   harness is the measuring instrument — without it every claim about "AI can
   operate PayProbe" is anecdote.
3. **Close one loop end-to-end under journal.** Extend the agent-loop tests
   (`packages/scenario-service/tests/test_agent_loop.py`) with a full
   author→run→diagnose→fix→re-run cycle where every write lands in the
   `ChangeJournal`, then `POST /agent/revert` and assert the backing stores
   are content-identical to the pre-session snapshot (hash the store files —
   scenario-service stores are file-backed).

### (d) You have a result when…

On the benchmark harness (task list and pass criteria frozen *before* the
runs, per `payprobe-research-methodology`): an unattended agent session
completes ≥ the pre-registered fraction of tasks with **zero writes outside
the journal** (verified by diffing store state against journal contents), and
after `POST /agent/revert` every touched store is byte/hash-identical to its
pre-session snapshot. The safety claim is the measurable one — "N tasks, 0
unjournaled writes, revert restores state hash-exactly" — not "the AI seemed
to do a good job". Failure of any hash comparison falsifies the milestone.

---

## Ambition 4 — Chaos-certified payment resilience

**Goal:** turn the existing chaos + scoring pipeline into a *rigorous*
certificate: statistically repeatable, sensitive to storm parameters in the
right direction, and honest about its own error bars — something you could
defend in a publication or an audit.

### (a) Why current SOTA fails

[general knowledge] Chaos tooling (Chaos Monkey lineage, LitmusChaos, Gremlin)
injects infrastructure faults — killed pods, network partitions — but has no
payments-domain scoring: nothing knows what an ISO 8583 timeout-with-late-
reversal *means*. Resilience "certifications" in industry are bespoke
consultancy reports, not reproducible artifacts. And chaos results are
notoriously unrepeatable: the same experiment rerun gives different numbers,
and few frameworks quantify that variance at all. A certificate nobody can
reproduce is marketing, not measurement.

### (b) PayProbe's specific assets (verified)

| Asset | Status | Path |
|---|---|---|
| Fault-injection engine on live simulators | [BUILT] | `packages/worker/adapters/tcp/chaos.py` — `ChaosEngine`/`ChaosOutcome`; faults: `drop_pct`, `latency_ms` (flat or `{min,max,pct}`), malformed frames, partial writes; documented precedence (drop ≻ latency ≻ malform ≻ partial); tests `packages/worker/tests/test_chaos.py` |
| Chaos dial + timed storms API | [BUILT] | `packages/orchestrator/api/main.py`: `GET/PUT /simulators/{sid}/chaos`, `POST/DELETE /simulators/{sid}/chaos/storm` (storm phases drive `set_chaos()`, restore baseline after) |
| Resilience scorer with gates and grade | [BUILT] | `packages/orchestrator/api/resilience.py`: `score_resilience(samples, thresholds)` — components availability/absorption/recovery/latency, `WEIGHTS = {0.35, 0.30, 0.25, 0.10}`, gates incl. `min_availability_ratio = 0.90`, `min_recovery_ratio = 0.98`; stages baseline/storm/recovery; API `GET/POST /resilience/runs`, `GET/DELETE /resilience/runs/{rid}`; tests `packages/orchestrator/tests/test_resilience.py` |
| Load subsystem to generate the observed traffic | [BUILT] | `packages/worker/engine/load/` (`profile.py`, `driver.py`, `bus.py`), `packages/worker/load_worker.py`, `packages/orchestrator/api/load_coordinator.py`; steady/ramp/spike/soak profiles |
| Run-vs-run comparison | [BUILT] | `GET /load-runs/{run_id}/compare` in `packages/orchestrator/api/main.py`; `compare_load_runs` MCP tool |

**The gap, stated precisely:** the certificate is a *single-run* artifact. One
storm, one score, one grade. Nothing measures score variance across identical
runs, nothing checks that the score responds monotonically to fault intensity,
and the persisted result carries no sample sizes or confidence information.

### (c) First three steps in this repo

1. **Property-test the scorer as a pure function.** `score_resilience()` takes
   a list of sample dicts — no I/O — which makes it ideal for synthetic-input
   testing *before* any live experiment. New
   `packages/orchestrator/tests/test_resilience_properties.py`: (i) monotonicity
   — for synthetic sample sets where storm-stage success strictly decreases,
   the availability component and composite score must not increase; (ii)
   boundary behaviour at each gate threshold; (iii) weight-sum and clamping
   invariants. Any violation found here is a scorer bug caught for free.
2. **Repeatability experiment.** [CANDIDATE] Script N identical certificate
   runs (same simulator, same load profile, same storm parameters) via
   `POST /resilience/runs`, collect composite scores and per-component values,
   compute stddev / spread. Home the driver script with the other probes in
   `packages/helpers/`. Pre-register the acceptable variance bound before
   running (see methodology skill). This experiment defines whether the
   certificate is even a stable measurement.
3. **Extend the certificate schema with methodology fields.** [CANDIDATE]
   Draft-first (spec in `docs/`, then code): persist per-stage sample counts,
   exact storm parameters, scorer version, and — once step 2 gives you a
   variance estimate — a repeatability figure on the stored result in
   `packages/orchestrator/api/resilience.py` / the `/resilience/runs` payload.
   Additive fields only; old stored runs must still load (reversibility).

### (d) You have a result when…

(i) The property suite passes: across the pre-registered synthetic families,
`score_resilience` is monotone non-increasing in injected fault intensity and
exact at gate boundaries — violations are concrete counterexamples, so this is
falsifiable by construction. (ii) Over N ≥ 10 identical live certificate runs,
the composite score's spread is within the bound you registered before the
experiment (and if it is not, *that is a publishable finding about the
certificate, not a failure to hide* — report it per the methodology skill).
(iii) A storm-intensity sweep (e.g. `drop_pct` ascending, all else fixed)
never produces a strictly better grade at strictly higher intensity, checked
by script exit code. Only after (i)–(iii) may "chaos-certified" language go
near external material — route through `payprobe-external-positioning`.

---

## How the four ambitions interlock

- Ambition 1's binary wire path makes Ambition 4's certificates meaningful
  against realistic hosts (an ASCII-only certificate certifies less).
- Ambition 2's replay-as-artifact is the evidence format for Ambition 4's
  incident analysis and for Ambition 3's agent to *read* what happened.
- Ambition 3's harness is how the other three get exercised cheaply at scale.
- All four are gated by the same evidence bar: `payprobe-research-methodology`
  for how to measure, `payprobe-validation-and-qa` for what counts as a test,
  `payprobe-change-control` for how anything lands.

---

## Provenance and maintenance

Authored 2026-07-03 against the repo state on that date. All [BUILT] claims
were verified by reading the cited files; ecosystem claims are labeled
[general knowledge] and were NOT verified against current vendor offerings.
Re-verify volatile facts before relying on them:

```bash
# From the repo root.

# Ambition 1 — one codec on the wire (expect: worker module is a re-export of
# payprobe_common.iso8583; the binary loopback test exists and passes)
head -5 packages/worker/adapters/tcp/iso8583.py
ls packages/payprobe_common/iso8583/
cd packages && PYTHONPATH=. python3 -m pytest worker/tests/test_iso8583_binary_wire.py worker/tests/test_iso8583_golden.py -q && cd ..
grep -n "PAYPROBE_ISO8583_FORMAT_ENCODING" packages/orchestrator/api/main.py   # default "1" since phase 5 (2026-09-24)

# Simulators still where cited
grep -n "class VisaSimulator\|class PayShieldSimulator\|class CyberSourceSimulator" \
  packages/worker/adapters/scheme/*.py packages/worker/adapters/hsm/payshield.py

# Ambition 2 — chronoscope buffer + import/export + correlation gap
grep -n "MAX_FRAMES" packages/portal/src/app/topologies/chronoscope/chronoscope.model.ts
grep -n "exportReplay\|importReplay" \
  packages/portal/src/app/topologies/chronoscope/chronoscope-recorder.service.ts
grep -n -A5 "interface ReplayFile" \
  packages/portal/src/app/topologies/chronoscope/chronoscope.model.ts   # still no run ids?

# Ambition 3 — tool count (144 on 2026-07-06; recount, do not trust this file)
cd packages/mcp-server && python3 -c \
  "from mcp_server import registry; print(len(registry.TOOL_SPECS), len(registry.RESOURCE_SPECS))" && cd ../..
grep -n "class ChangeJournal\|def restore_journal\|class GuardrailError" \
  packages/scenario-service/api/agent_tools.py

# Ambition 4 — scorer weights/gates unchanged?
grep -n -A6 "WEIGHTS = {" packages/orchestrator/api/resilience.py
grep -n "min_availability_ratio\|min_recovery_ratio" packages/orchestrator/api/resilience.py
grep -n "chaos/storm" packages/orchestrator/api/main.py
```

If any check disagrees with this skill, the repo wins — update this file.
