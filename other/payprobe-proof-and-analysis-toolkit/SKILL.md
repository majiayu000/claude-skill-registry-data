---
name: payprobe-proof-and-analysis-toolkit
description: >
  HOW to measure and prove things in PayProbe — analysis recipes with
  commands (prove it, don't just install it). Load when you need to establish
  a fact rather than fix a known symptom — reproducing and categorizing a failing suite before touching code,
  verifying crypto (DUKPT/ARQC/PVV/CVV) against known vectors instead of
  trusting it by inspection, proving what bytes actually crossed a TCP wire
  (ISO 8583 analyze/diff, raw_log, length-prefix framing), measuring load
  performance without fooling yourself (tps_series, error_categories,
  /load-runs/{id}/compare, the in-process TPS cap), designing chaos
  fault-injection experiments where a gate decides pass/fail (resilience
  scoring), and reasoning about crash-safety and delivery semantics
  (reconcile_orphans, Redis Streams last_event_id resume). Keywords: worked
  example, test vector, measured not assumed, root cause, wire trace, hex dump,
  regression detection, chaos storm, resilience certificate, crash recovery,
  stuck run, exactly-once, at-least-once.
---

# PayProbe Proof & Analysis Toolkit

Six recipes for turning "I think it works" into "here is the evidence".
Each recipe is a method that generalizes, anchored to a worked example that
actually happened in this repo. Every path, symbol, endpoint, and number below
was verified against the repo on 2026-07-03.

**Jargon, defined once:**

| Term | Meaning |
|---|---|
| ISO 8583 | The binary/text message standard used by card networks. Messages = MTI (4-digit message type) + bitmap + numbered Data Elements (DEs). DE 39 = response code. |
| DUKPT | Derived Unique Key Per Transaction (ANSI X9.24-1) — each transaction gets a fresh key derived from a Base Derivation Key (BDK) and a Key Serial Number (KSN). IPEK = initial PIN encryption key. |
| ARQC / ARPC | EMV chip cryptograms: card→issuer request cryptogram / issuer→card response cryptogram. |
| PVV / CVV | Visa PIN Verification Value / Card Verification Value — short check digits derived from keys. |
| HSM | Hardware Security Module. PayProbe simulates a Thales payShield 10K host-command interface (commands like A0, CW, CY, CA, EC, M6, M8, KQ). |
| Length-prefix framing | TCP is a byte stream; each ISO 8583 message is preceded by an N-byte length field so the receiver knows where a message ends. |
| TPS | Transactions per second. |
| Chaos dial | Runtime fault-injection config on a running simulator (drops, latency, malformed replies). |
| Orphaned run | A DB run row stuck in `running` because the process that owned it died before finalizing it. |

Run everything from the repo root. The full suite is `make test`.

---

## Recipe 1 — Reproduce, then categorize (the docs/history/PROGRESS.md discipline)

**When to use:** any failing test, broken suite, or reported bug — BEFORE
writing a fix. Also when inheriting an unknown baseline ("does the suite even
pass today?").

**The rule (a confirmed non-negotiable): measure, never assume.** No fix ships
without a measured root cause or a reproducing test. The unit of work is not
"the failure" but "the category of failure":

- **(a) infra/dependency broken** — the product code is fine; the runtime,
  a dependency declaration, or the harness is wrong.
- **(b) product regression** — the code genuinely does the wrong thing.
- **(c) test bug** — the expectation is wrong, not the behavior.

Fix the *category*, not the symptom. A category-(a) failure "fixed" by editing
the test (as if it were category (c)) hides a silently degraded product.

### Steps

1. **Establish the baseline number.** Run the whole suite and record the exact
   pass/fail count and the named failing tests:
   `make test` (equivalent: `cd packages && python -m pytest worker/tests orchestrator/tests scenario-service/tests mcp-server/tests payprobe-assistant/tests -q`).
2. **Reproduce one failure in isolation** (`python -m pytest <file>::<test> -q`
  from `packages/`) and read what the code *returns*, not what you expect it
   to return.
3. **Trace to the first wrong value.** Follow the data until you find the
   place where reality diverges — quote the actual returned value in your
   notes.
4. **Assign the category.** Write it down explicitly ("Category (a): …").
5. **Fix at the category level**, re-run the FULL suite, and record
   before→after counts. The delta must be exactly the failures you explained —
   no expected result may be edited to make a test pass.
6. **Log the loop** in `docs/history/PROGRESS.md` style: Baseline → Root cause (measured,
   not assumed) → Did → Result → Next. While reproducing, note latent bugs you
   trip over — they become the next iteration, not a drive-by edit.

### Worked example: the pycryptodome investigation (repo history, 2026-06-18)

From `docs/history/PROGRESS.md` (repo root) — the actual reasoning chain, quoted:

> **Baseline (2026-06-18)** — Full suite: **180 passed, 3 failed**.
> Failures (all `worker/tests/test_engine.py`, kind=`crypto` nodes):
> `test_crypto_node_pin_block_roundtrip`, `test_crypto_emv_arqc_chain_from_mdk`,
> `test_crypto_emv_arqc_to_arpc_verify_flow`.
>
> **Root cause (measured, not assumed):** `run_crypto()` in
> `worker/engine/crypto_tools.py` returns `{"error": "pycryptodome is not
> installed in this runtime"}`. The worker's `pyproject.toml` declares
> `python-pkcs11` and `iso8583` but **omits `pycryptodome`**, which
> `crypto_tools.py` requires (`from Crypto.Cipher import DES, DES3`). So the
> crypto code-path silently degrades to an error result and the 3 scenarios
> error out. Category (a): infra/dependency broken.
>
> **Iteration 1** — added `pycryptodome>=3.19` to
> `packages/worker/pyproject.toml`. Result: **180→183 passed, 0 failed**.

Note what did NOT happen: nobody patched the three tests, mocked the crypto,
or marked them flaky. The dependency declaration was the defect. And the
reproduce step paid twice — while reproducing, a *latent* bug surfaced (the
edge-less scenario path called `step["target"]` unconditionally, raising
`KeyError: 'target'` for crypto/code/http nodes). That became Iteration 2: a
kind-aware `_execute_node()` dispatch plus a new reproducing test
(`test_edgeless_non_action_nodes_run_without_target_keyerror`) → 184 passed.

Evidence: `docs/history/PROGRESS.md` (Baseline + Iterations 1–2);
`packages/worker/pyproject.toml` (the `pycryptodome>=3.19` line); commit
`6f5643c` contains the dependency addition (`git log -S pycryptodome --oneline
-- packages/worker/pyproject.toml`; note the repo history is squash-style, so
trust `git log -S` diffs over commit message titles).

### How you know you're done
- You can state the category in one sentence with the measured evidence.
- Full-suite counts recorded before AND after; the delta equals exactly the
  failures your root cause explains.
- A reproducing test exists for any product-level fix.
- The loop is written down (docs/history/PROGRESS.md style) including latent finds.

---

## Recipe 2 — Crypto correctness by construction

**When to use:** adding or touching ANY cryptographic operation (key
derivation, PIN blocks, cryptograms, MACs, check values). Never trust crypto
code by inspection — DES-era financial crypto fails silently: wrong parity,
wrong variant XOR, or wrong PAN slicing still produces plausible-looking hex.

**The rule:** an algorithm is correct when (1) it reproduces an *authoritative
published vector*, and (2) *two independent paths agree* — not when the code
"looks right".

### Steps (adding a new algorithm)

1. **Find the authoritative vector source** — the standard itself (ANSI X9.24
   appendix, EMV Book 2), a scheme manual, or a widely cross-checked reference
   implementation. If no published vector exists, generate one with an
   independent tool and record its provenance in the test docstring.
2. **Encode the vector as a failing test FIRST** — literal hex in, literal hex
   out. Guard the import (`pytest.importorskip("Crypto")`) so a missing
   dependency skips loudly rather than degrades silently (see Recipe 1's
   worked example for why).
3. **Implement until the vector passes.**
4. **Add a cross-path check:** derive via route A, verify via route B
   (BDK-path vs IPEK-path; generator vs verifier; library vs HSM simulator).
   Agreement of two independent code paths catches errors a single vector
   can't.
5. **Add a negative test** — a wrong input must be *rejected*, not merely
   produce different output.

### Worked example: how this repo's DUKPT/PVV/ARQC tests establish correctness

`packages/worker/tests/test_dukpt_pvv.py` uses all three techniques:

- **Published vector** — the canonical ANSI X9.24 test triple, verbatim in the
  module docstring and asserted literally:
  `BDK 0123456789ABCDEFFEDCBA9876543210` + `KSN FFFF9876543210E00000` →
  `IPEK 6AC292FAA1315B4D858AB3A3D7D5933A`
  (`test_ipek_matches_ansi_vector`), plus the canonical derived transaction
  key for KSN `…E00001` = `042666B49184CFA368DE9628D0397BC9`
  (`test_transaction_key_matches_ansi_vector`).
- **Two-path agreement** — `test_ipek_from_bdk_or_directly_agree`: deriving
  the working key from the BDK must equal deriving it from the IPEK.
- **Roundtrip across roles** — `test_pin_block_round_trips_terminal_to_host`:
  the *terminal side* encrypts a PIN under the DUKPT PIN key; the *host side*
  independently re-derives the same key from BDK+KSN and decrypts; the PIN
  must survive.

`packages/worker/tests/test_payshield_sim.py` then closes the strongest loop
available in-repo: **HSM-simulator vs `crypto_tools` parity** — two
implementations written against the spec independently must agree:

- `test_ec_verifies_pvv` — computes a PVV with `crypto_tools.pvv()` and a PIN
  block with `crypto_tools.pin_block_encode()`, then asks the payShield
  simulator's `EC` command to verify: it must answer error `00`.
- `test_ca_pin_translate_round_trips` — builds an ISO-0 PIN block under a
  clear TPK, has the simulator translate TPK→ZPK via `CA`, then decodes the
  output with `crypto_tools.pin_block_decode()` — same PIN out.
- `test_kq_arqc_verify_and_arpc` — generates an ARQC with
  `crypto_tools.arqc()` and has the simulator's `KQ` command verify it.
- **Negative tests everywhere** — `test_cw_then_cy_verifies_and_rejects`:
  `CY` with a forged CVV `999` must return error `01` (verification failed),
  not a different success.

The pure-engine EMV chain lives in `packages/worker/tests/test_engine.py`:
`test_crypto_emv_arqc_chain_from_mdk` (MDK → ICC master key → session key →
ARQC wired across scenario crypto nodes) and
`test_crypto_emv_arqc_to_arpc_verify_flow` (ARQC → ARPC method 1 → card-side
verify with `expected` binding) — the full issuer flow, generator and verifier
exercised against each other.

### How you know you're done
- At least one literal published vector asserted, with its source named.
- At least one two-path/parity assertion (library vs simulator, or role A vs
  role B).
- At least one rejection test.
- `make test` green; the new tests fail if you perturb the implementation by
  one bit (try it once — a test that can't fail proves nothing).

---

## Recipe 3 — Wire-protocol analysis: decode, don't guess

**When to use:** "the host rejected my message", "the TCP step hangs",
"the response parses wrong", any dispute about what actually crossed the
wire. The failure mode this recipe prevents: reasoning from what you *meant*
to send instead of the bytes that were sent.

**The rule:** get the actual bytes, decode them with a tool, and diff against
a known-good message. Never debug an ISO 8583 problem from the request dict.

### The instruments (all verified in-repo)

| Instrument | Where | What it proves |
|---|---|---|
| `POST /iso8583/analyze` | scenario-service (`packages/scenario-service/api/main.py`) — also MCP tool `iso8583_analyze`, portal Inspector page | Decodes a wire message (hex/ascii) into MTI + bitmap + validated DEs (+ EMV TLV for DE 55). If analyze can't parse it, neither can the endpoint you sent it to. |
| `POST /iso8583/diff` | same file — MCP `iso8583_diff` | Field-level diff of two messages: added / removed / changed DEs. Diff your failing message against the last passing one. |
| `POST /iso8583/build` | same file | Validates a `{DE: value}` map against the field table, then packs it — build the message you *think* you sent and byte-compare. |
| `StepResult.raw_log` | `packages/worker/adapters/base/base_adapter.py`; filled by `TcpAdapter._wire_log` in `packages/worker/adapters/tcp/adapter.py` | The framed TX bytes as hex (first 512 hex chars), sent MTI, received MTI, DE39, DE list — captured at the moment of exchange. |
| Trace tab | `_build_trace` in `packages/worker/engine/runner.py` folds `raw_log` lines into the run report as `level:"wire"` entries; visible on the run report's Trace tab and its JSON export | Per-step wire evidence attached to every run, no packet capture needed. |

### Worked example: length-prefix framing in TcpAdapter/TcpResponder

TCP has no message boundaries, so every PayProbe TCP exchange is
length-prefix framed. Both sides implement the *same* four-knob model —
`TcpAdapter._frame`/`._read_frame` (`packages/worker/adapters/tcp/adapter.py`)
and the mirrored `TcpResponder._frame`/`._read_frame`
(`packages/worker/adapters/tcp/responder.py`):

```
frame = length_prefix + [TPDU header] + body

length_prefix_bytes     width of the prefix (default 2; validated >= 1)
length_byte_order       "big" (default) or "little"
length_includes_prefix  does the declared length count the prefix itself? (default False)
length_includes_header  does it count the TPDU header? (default True)
tpdu_bytes / tpdu_outbound_hex   optional TPDU header handling
```

The read side is `await reader.readexactly(prefix_bytes)` → decode length →
`readexactly(remaining)`. **This is why a framing mismatch presents as a hang,
not an error:** `readexactly` waits for exactly the declared byte count. If
the sender's declared length is 2 bytes larger than the receiver expects
(e.g. one side counts the prefix, the other doesn't), the receiver waits for
bytes that never come → timeout — or reads 2 bytes into the *next* message →
permanent stream desync.

The repo encodes this reasoning as a deliberate fault: the chaos engine's
`bad_length` malformed mode (`packages/worker/adapters/tcp/chaos.py`) inflates
the length prefix precisely to reproduce "read stall / timeout or stream
desync" — the framing hypothesis is testable on demand.

**The decode-don't-guess procedure for a hanging/rejected TCP step:**
1. Pull the step's `raw_log` from the run report Trace tab (TX hex line).
2. By hand: take the first `length_prefix_bytes*2` hex chars, decode with the
   configured byte order, and compare against the actual remaining byte count.
   The arithmetic difference tells you which boolean knob is wrong (off by
   `prefix_bytes` → `length_includes_prefix` mismatch; off by TPDU length →
   header/tpdu mismatch).
3. Feed the body (after prefix/TPDU) to `POST /iso8583/analyze` to prove the
   payload itself decodes.
4. If a previously-good message exists, `POST /iso8583/diff` the two bodies —
   the changed DE list is your suspect set.

### How you know you're done
- You can show the offending bytes (hex), the decode of them, and the
  one-line arithmetic or DE-diff that explains the failure.
- The fix is expressed in framing/table config terms, and a re-run's
  `raw_log` shows the corrected frame.

---

## Recipe 4 — Load & performance measurement discipline

**When to use:** any claim of the form "it's faster/slower/handles more now",
capacity planning, or investigating a throughput/latency complaint.

**The rule:** hypothesis with predicted numbers → controlled run → compare
against a persisted previous run. A single-number TPS claim is not a
measurement (see also `payprobe-research-methodology` for the general
evidence bar).

### Why single-number TPS lies

The persisted summary keeps more than the mean for a reason
(`packages/orchestrator/api/load_coordinator.py` writes `tps_series` and
`tps_stability` into the run summary at finalize; error categorization landed
in commit `cb91924`):

- **Oscillation hides in the mean** — `tps_series` (per-sample achieved TPS)
  and `tps_stability` (coefficient of variation, `cv`) distinguish a steady
  2000 TPS from a 0/4000 sawtooth averaging 2000.
- **Fast failures inflate TPS** — a run that errors instantly can post
  *higher* TPS than a healthy one. Read `error_rate` and the per-category
  `error_categories` breakdown alongside throughput.
- **Tails hide in the mean** — p50/p95/p99 are persisted; a p99 regression
  with a flat p50 is a real regression.

### The instruments

- `GET /load-runs/{run_id}/compare?to=<base_id>` — defaults to the previous
  like-for-like load run (`run_store.previous_load`). Returns per-metric
  deltas for `latency_p50/p95/p99`, `error_rate`, `tps`, `tps_cv`, each with a
  `regressed`/`improved`/`flat` verdict decided against a **2% relative
  dead-band** (`eps=0.02` in `_delta`, `packages/orchestrator/api/main.py`) so
  jitter doesn't read as regression — plus a union table of error categories
  with per-category deltas and a headline `{regressions, improvements}` count.
  MCP tool: `compare_load_runs`. Tests: `packages/orchestrator/tests/test_load_compare.py`.
- `POST /load-runs/{run_id}/retune` — change target TPS mid-run (one variable,
  live) instead of launching a confounded new run.

### The in-process cap: a validity guard, not a limit

When no external `load_worker` fleet claims the shards, the coordinator can
fall back to running workers *inside the orchestrator's own event loop*
(`LoadCoordinator._external_or_fallback`,
`packages/orchestrator/api/load_coordinator.py`). Above a safe cap it
**refuses to run** rather than produce a number:

- `PAYPROBE_INPROC_MAX_TPS` (default **2000**) and
  `PAYPROBE_INPROC_MAX_CONNECTIONS` (default **5000**), wired in
  `packages/orchestrator/api/main.py`.
- Rationale (from the code): driving 20K TPS in-process would starve the
  API/WebSocket loop — the load generator and the system under observation
  would contend for the same event loop, so the measurement would be an
  artifact of the harness. **Any in-process measurement above the cap is
  invalid by construction**, which is why the coordinator sets a `notice`
  telling the operator to scale a real fleet instead of silently degrading.

Generalize this: before trusting any performance number, ask "was the
measuring instrument itself saturated?" If the generator shares a core, an
event loop, or a NIC with the target, cap the claim accordingly.

### Steps

1. Write the hypothesis WITH numbers first: "raising X will move p95 from
   ~180ms to <120ms at 1500 TPS with error_rate flat".
2. Ensure a comparable baseline run exists (same profile/env); if not, run one.
3. Change ONE variable. Run. (External fleet if demand exceeds the in-proc cap.)
4. `GET /load-runs/{id}/compare` — read the verdicts, not the means: any
   `regressed=true` on a metric you predicted flat falsifies the hypothesis.
5. Record predicted-vs-actual. A prediction that missed is a finding, not a
   failure.

### How you know you're done
- Prediction written before the run; compare output attached after.
- No metric verdict unexplained (including `tps_cv` and error categories).
- The run was within instrument validity (external workers, or demand ≤ cap).

---

## Recipe 5 — Failure-injection experiment design

**When to use:** proving a client/system *tolerates* faults — reconnect
logic, retry policies, brownout behavior — rather than merely works on the
happy path.

**The rule:** a chaos exercise is an experiment only if the acceptance
criterion is decided **before** the run and evaluated **by a gate, not a
human eyeball**. "We injected faults and it seemed fine" is theater.

### The instruments (all verified in-repo)

- **Chaos dial** — `TcpResponder.set_chaos()`
  (`packages/worker/adapters/tcp/responder.py`): swap the live fault config on
  a running simulator; takes effect on the very next reply; passing a `seed`
  restarts the RNG stream so a fault sequence is **reproducible** — always set
  one in an experiment. API: `GET` (read) / `PUT` (set) `/simulators/{sid}/chaos`; `POST` exists only on `/simulators/{sid}/chaos/storm`. On a shared deployment, injecting chaos into a simulator other runs/schedules depend on is behavior-changing — coordinate per `payprobe-change-control`. Accepted keys
  (`_CHAOS_KEYS`, `packages/orchestrator/api/main.py`): `seed`, `drop_pct`,
  `latency_ms`, `malformed_pct`/`malformed_mode`, `partial_pct`/`partial_bytes`,
  plus the aliases `drop`/`malformed`/`partial` (full list in
  `payprobe-run-and-operate`).
- **Malformed modes as distinct hypotheses**
  (`packages/worker/adapters/tcp/chaos.py`): `garbage` (valid frame,
  unparseable body → decode-error handling), `flip_bits` (subtle corruption),
  `bad_mti` (valid frame, wrong message type → dispatch handling),
  `bad_length` (inflated length prefix → read-stall/desync handling, see
  Recipe 3). Pick the mode that matches the failure you're hypothesizing
  about — they exercise different client code paths.
- **Timed storms** — `POST /simulators/{sid}/chaos/storm`: a sequence of
  phases (`duration_s` + chaos block; `{}` = calm phase) × `repeat`, modeling
  outage / brownout / flapping; baseline chaos is restored when the storm
  ends; `DELETE` cancels.
- **Resilience runs = codified acceptance** — `POST /resilience/runs` ties a
  storm to a live load run's client and samples per-second through three
  stages (baseline → storm → recovery). `score_resilience()`
  (`packages/orchestrator/api/resilience.py`) then computes four weighted
  components — **availability 0.35, absorption 0.30, recovery 0.25,
  latency 0.10** — and four **hard gates**:

  | Gate | Passes when (defaults) |
  |---|---|
  | `availability` | storm success rate ≥ baseline × `min_availability_ratio` (0.90) |
  | `no_wedge` | not (sim still answered some requests cleanly AND client got zero through) |
  | `recovery` | post-storm success ≥ baseline × `min_recovery_ratio` (0.98) |
  | `latency` | storm p95 ≤ baseline p95 × `max_latency_multiple` (4.0) |

  Verdict: `PASS` iff weighted score ≥ `pass_score` AND **no gate failed**;
  plus a letter grade (A+ ≥95 … F). Thresholds are overridable per run —
  which is exactly where you pre-register your acceptance bar.
  Tests demonstrating each gate firing: `packages/orchestrator/tests/test_resilience.py`
  (`test_fragile_client_fails_availability_gate`,
  `test_wedged_client_trips_no_wedge_gate`, `test_no_recovery_fails_recovery_gate`,
  `test_latency_ceiling_gate`, `test_threshold_override_relaxes_pass_bar`).

### Steps (designing the experiment)

1. **State the resilience hypothesis** as gate outcomes: "under a 30s
   brownout (drop_pct 30, latency_ms 250), availability and no_wedge pass;
   recovery passes within the recovery window; latency gate passes at the
   default ×4 ceiling."
2. **Pin the thresholds first.** If the defaults aren't your bar, set
   `thresholds` in the request BEFORE running — never after seeing results.
3. **Fix the seed** in every chaos block so a failing run replays.
4. **One fault variable per experiment.** A storm phase may combine faults
   only if the combination itself is the hypothesis.
5. Start the load run, then `POST /resilience/runs` pointing at it (the API
   enforces this ordering — it refuses without a running load run:
   `test_resilience_run_requires_running_load`).
6. **Read the verdict and `blocking` list — not the dashboard.** A FAIL with
   `blocking: ["recovery"]` is a precise, falsifiable finding.

### How you know you're done
- Predicted gate outcomes written before the run; actual verdict/gates
  attached after.
- The run is reproducible (seed + profile + thresholds recorded).
- Any FAIL has a follow-up hypothesis, or an accepted-risk note; any PASS
  states which client behavior (retry/reconnect/backoff) it certifies.

---

## Recipe 6 — Concurrency & distributed reasoning: prove crash-safety

**When to use:** any state that outlives a process (DB rows, Redis entries)
or crosses processes (events, shards, replicas). The question is never "does
it work?" but "**which invariant holds after a crash at the worst moment, and
who restores it?**"

**The method:**
1. State the invariant explicitly.
2. Enumerate the failure moments that break it (crash between write A and
   write B; restart; network partition).
3. For each, name the *restorer* — the code path that re-establishes the
   invariant — and prove each restorer is **idempotent** (safe to run when
   nothing is broken).
4. Cover all three restoration triggers: **boot** (automatic), **operator**
   (manual endpoint/button), **user intent** (the action a user takes when
   they notice, e.g. pressing Stop).

### Worked example A: `reconcile_orphans` — restoring the run-ownership invariant

**Invariant:** *a DB run row in a non-terminal state (`pending`/`running`)
implies a live in-memory coordinator owns it.* An orchestrator crash breaks
it: the coordinator that would have called `finish()` is gone, so the row is
stranded as `running` forever — history and pickers show phantom live runs.

**Restorer:** `RunStore.reconcile_orphans(live_ids, label_prefix=...)` in
`packages/orchestrator/api/run_store.py` — closes every unfinished row NOT in
`live_ids` as `interrupted` with a `{"reconciled": True, "reason": ...,
"previous_status": ...}` summary. Idempotent by construction: rows a live
coordinator still owns are skipped, and already-finalized rows aren't
candidates.

**All three triggers exist** (`packages/orchestrator/api/main.py`):

1. **Boot** — startup hook `_reconcile_stuck_runs_on_boot`: "a fresh process
   owns no live runs, so any DB row still marked `running` was stranded by a
   previous crash/restart" — reconcile is safe *because* the live set is
   provably empty. (Wrapped in try/except: housekeeping never blocks boot.)
2. **Operator** — `POST /load-runs/reconcile` (portal Load page renders it as
   the "Fix stuck runs" button, `packages/portal/src/app/load/load.component.ts`).
3. **User intent (stop-clears-stranded)** — `POST /load-runs/{run_id}/stop`
   is a three-rung ladder: (i) owned by this replica → stop directly;
   (ii) owned by another replica → route via `run_control.request_cancel`;
   (iii) a persisted row still `running` with NO live owner anywhere → it's
   stranded, finalize as `interrupted` right there. Rung (iii) closes the
   loop: the natural human reaction to a phantom run ("just stop it") now
   *repairs* the invariant instead of 404ing.

Tests: `packages/orchestrator/tests/test_simulators.py`
(`test_reconcile_stuck_load_runs`, `test_reconcile_skips_live_runs` — the
idempotence proof). Code landed in commit `1b377c8` (squash-style history;
verify with `git log -S reconcile_orphans --oneline`).

### Worked example B: delivery & resume semantics — Redis Streams over pub/sub

`packages/worker/engine/stream.py` (module docstring carries the full
argument): the original spec used Redis *pub/sub* for run events. Pub/sub is
fire-and-forget — a client not connected at publish time never sees the
event, so a dropped WebSocket loses history. The replacement invariant:
*every event is appended to a per-run log with a monotonic id, so any
consumer can resume from the last id it saw.*

- `RedisStreamBackbone`: XADD to `run:{run_id}:stream`; Redis-native entry
  ids (`<ms>-<seq>`) double as the resume cursor; resume = XRANGE from
  `(<last_id>` (exclusive) to replay the backlog, then blocking XREAD to tail
  live; the `RUN_COMPLETED` event terminates the stream.
- The WebSocket handler (`packages/orchestrator/api/main.py`) accepts
  `?last_event_id=<id>` and replays everything after it — reconnect-resume
  with no lost events.
- `InMemoryStreamBackbone` mirrors the exact semantics for tests/dev, so the
  handler is backend-agnostic.

The distilled reasoning, reusable anywhere: **don't chase exactly-once
delivery — make delivery at-least-once and resumable, and keep the cursor on
the consumer.** The id is opaque to consumers; they only hand back the last
one they saw. Consumers must therefore tolerate replays (idempotent handling)
— which is the same property that made `reconcile_orphans` safe.

### How you know you're done
- The invariant is written down in one sentence.
- Every failure moment has a named restorer; boot/operator/user-intent
  triggers all covered (or the gap is documented).
- Idempotence is tested (the "skips live" / "safe to call twice" test exists).
- For event flows: a consumer that disconnects and resumes with its last id
  observably misses nothing (`stream.py` semantics).

---

## When NOT to use this skill

- **Routine symptom→fix debugging** (known failure modes, triage tables,
  trap stories) → `payprobe-debugging-playbook`.
- **Running a multi-step research program** (evidence bar, idea lifecycle,
  adversarial refutation, hypothesis registers) → `payprobe-research-methodology`.
- **What counts as shippable evidence / acceptance thresholds** →
  `payprobe-validation-and-qa`.
- **Which diagnostic endpoint to call and how to read it** →
  `payprobe-diagnostics-and-tooling`.
- **The chronicle of past investigations and dead ends** →
  `payprobe-failure-archaeology`.

---

## Provenance and maintenance

Authored 2026-07-03 against the repo at that date. All quotes, symbols,
endpoints, defaults, and test names were read from source. Git history is
squash-style: verify code archaeology with `git log -S <symbol>`, not commit
titles. Re-verify before trusting drift-prone facts:

| Claim | Re-verify with (from repo root) |
|---|---|
| docs/history/PROGRESS.md baseline/iterations quoted in Recipe 1 | `sed -n '22,65p' docs/history/PROGRESS.md` |
| pycryptodome declared in worker deps | `grep pycryptodome packages/worker/pyproject.toml` |
| ANSI X9.24 vectors + two-path tests | `grep -n "6AC292FAA1315B4D858AB3A3D7D5933A\|via_bdk" packages/worker/tests/test_dukpt_pvv.py` |
| HSM↔crypto_tools parity tests | `grep -n "def test_" packages/worker/tests/test_payshield_sim.py` |
| ISO 8583 analyze/build/diff routes | `grep -n '"/iso8583/' packages/scenario-service/api/main.py` |
| raw_log capture + wire lines in trace | `grep -n raw_log packages/worker/adapters/tcp/adapter.py packages/worker/engine/runner.py` |
| Framing knobs & readexactly semantics | `grep -n "length_prefix_bytes\|readexactly" packages/worker/adapters/tcp/adapter.py packages/worker/adapters/tcp/responder.py` |
| Compare deltas, 2% dead-band, error categories | `grep -n "eps: float = 0.02\|error_categories" packages/orchestrator/api/main.py` |
| In-proc cap defaults (2000 TPS / 5000 conns) | `grep -n INPROC packages/orchestrator/api/main.py` |
| Resilience weights/gates/thresholds | `sed -n '30,60p' packages/orchestrator/api/resilience.py` |
| Chaos keys + malformed modes | `grep -n "_CHAOS_KEYS" packages/orchestrator/api/main.py; grep -n "bad_length\|garbage\|flip_bits\|bad_mti" packages/worker/adapters/tcp/chaos.py` |
| reconcile_orphans + boot hook + stop ladder | `grep -n "reconcile" packages/orchestrator/api/run_store.py packages/orchestrator/api/main.py` |
| Redis Streams resume semantics | `sed -n '1,25p' packages/worker/engine/stream.py` |
| Suite entry point | `grep -n "^test:" -A2 Makefile` |
