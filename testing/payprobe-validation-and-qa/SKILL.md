---
name: payprobe-validation-and-qa
description: >
  The tests and thresholds that gate merges: what counts as evidence in PayProbe, and how to make the regression-vs-environment call. Load this
  when you are: adding or running tests; deciding whether a failing test is a
  real regression or an environment problem (missing pycryptodome/aiohttp/httpx);
  asked "is the suite green", "how many tests", "how do I test this"; adding an
  example scenario; working with certification packs, compliance %, sign-off
  gates (GO/NO-GO, GatePolicy), baselines, run-vs-run compare, or resilience
  pass/fail thresholds; quarantining a flaky test; or testing the Angular portal
  (Playwright e2e, E2E_FULL). Keywords: pytest, make test, evidence, gates,
  thresholds, golden, certification, signoff, flaky, coverage, no silent skip.
---

# PayProbe validation and QA — what counts as evidence

PayProbe is a payment-systems test platform (ISO 8583 = the binary card-message
standard; HSM = hardware security module for PIN/key crypto). This skill defines
the project's evidence standard, maps every test suite, lists the acceptance
thresholds that exist in code, and shows how to add tests correctly.

**When NOT to use this skill:**

| You actually need | Use instead |
|---|---|
| Recreating the dev env, dependency install traps, Python version issues | `payprobe-build-and-env` |
| Measuring a live/running system (diagnostics endpoints, traces, load metrics) | `payprobe-diagnostics-and-tooling` |
| How changes are classified/gated/reviewed; the non-negotiables and their history | `payprobe-change-control` |

## 1. The evidence standard (non-negotiable)

1. **Suite green before AND after.** `make test` (repo root) must pass before
   you start and after you finish. Known failures may not accumulate. If the
   suite is red before you begin, that is your first problem — do not build on
   a red baseline.
2. **A fix requires a reproducing test first.** No fix ships without a measured
   root cause. Write the test that fails for the exact reason the bug exists,
   watch it fail, then fix. `docs/history/PROGRESS.md` documents this discipline in action
   ("Root cause (measured, not assumed)") — e.g. the crypto-node failures were
   traced to `run_crypto()` returning `{"error": "pycryptodome is not
   installed…"}` before any fix was made.
3. **No silent skips.** A green run that quietly skipped work is NOT evidence.
   This is enforced in three places (see §3 and §4): the example-scenario guard,
   the `no_silent_skips` sign-off gate, and the flaky-test quarantine rule.

### Environment failure vs regression — the discrimination procedure

Some tests need optional native/third-party deps. A failure caused by a missing
dep is an **environment problem, not a regression**. Discriminate like this:

1. **Read the failure text.**
   - `ModuleNotFoundError: No module named 'httpx'` / `'aiohttp'` at
     *collection* time → environment. Known offenders:
     `worker/tests/test_cybersource_sim.py` (httpx),
     `worker/tests/test_http_flow_responder.py` (aiohttp).
   - Test *skipped* via `pytest.importorskip` → environment. Function-level
     skips are visible in the run output; MODULE-level importorskips (e.g.
     `test_registry.py`) silently shrink the collected COUNT instead — compare
     counts, not just failures. Known importorskips:
     `worker/tests/test_dukpt_pvv.py` (`Crypto`, i.e. pycryptodome),
     `orchestrator/tests/test_signoff.py` (`cryptography`),
     `mcp-server/tests/test_registry.py` (`mcp` SDK),
     `worker/tests/test_grpc_adapter.py` (skipif when grpcio-tools absent).
   - Crypto/EMV engine tests failing with an assertion whose payload contains
     `"pycryptodome is not installed in this runtime"` → environment
     (the crypto tool degrades to an error result; see `docs/history/PROGRESS.md` baseline
     notes). EMV = the chip-card standard; these tests need real DES/3DES.
2. **Fix the environment, re-run the same test.** `make install` covers the
   worker basics; per-package: `pip install -e "packages/<pkg>[dev]"`.
   Python **3.11+ is required** (packages declare `requires-python >= 3.11`).
3. **Still failing with deps present?** Now treat it as a candidate regression:
   re-run on the last known-green commit (`git stash` your change, re-run,
   restore). If it fails only with your change, it is your regression.
4. Never "fix" an env failure by deleting or skipping the test.

### The no-silent-skip guard (executable doctrine)

`packages/worker/tests/test_example_scenarios.py` parametrizes over **every**
`examples/scenarios/*.json` file, runs each through the real `WorkerEngine` in
mock mode, and asserts:

- the directory is non-empty (an emptied examples dir fails the suite),
- every scenario reaches a clear status in `{PASSED, FAILED, BLOCKED}` — never
  `error`,
- every step has a clear status — no step may error out or swallow an exception.

This guards the core promise: no shipped scenario silently degrades.

## 2. The suite map

Test counts measured 2026-07-03 via `pytest --collect-only -q` per package
(re-measure; they grow):

| Package | Test dir | Tests | In `make test`? | Covers |
|---|---|---:|---|---|
| worker | `packages/worker/tests` | 308 | yes | engine, adapters (ISO 8583/TCP/HTTP/gRPC/HSM), simulators (VISA, CyberSource, payShield), crypto (DUKPT/PVV/EMV), load engine, example-scenario guard |
| orchestrator | `packages/orchestrator/tests` | 274 | yes | run lifecycle, auth gate, certification/sign-off, load coordination + compare, schedules/trends, diagnostics, topology, chaos/resilience |
| scenario-service | `packages/scenario-service/tests` | 267 | yes | scenario/project stores, connections, environments, formats, packs, test-data manager, agent tools, assist |
| mcp-server | `packages/mcp-server/tests` | 79 without the `mcp` SDK / 89 with it | yes | MCP tool registry + proxying (MCP = Model Context Protocol, the AI-tool interface). `test_registry.py` does a module-level `importorskip("mcp")` — without the SDK, 10 tests drop out of collection SILENTLY (no skip line in the collect-only count) |
| payprobe-assistant | `packages/payprobe-assistant/tests` | 18 | yes | NL→scenario assistant against an in-memory fake REST surface |
| report_service | `packages/report_service/tests` | 37 | **no** (CI: yes) | pure report/gates/certify/diagnose library |
| auth-service | `packages/auth-service/tests` | 13 | **no** (CI: **no**) | login/JWT/user management |

`make test` total on 2026-07-03: **946 collected** (308+274+267+79+18) in an env without the `mcp` SDK; **956** (mcp-server 89) with full deps. The delta is the silent importorskip above, not a stale checkout.

> Coverage gaps worth knowing: `report_service` tests run in CI
> (`test-services` job) but not in `make test`; `auth-service` tests run in
> **neither** `make test` nor CI — run them manually when touching auth.
> CI also does not run mcp-server/payprobe-assistant suites (only `make test`
> does). `packages/payprobe_common` and `packages/helpers` have no test dirs.

### Config and markers

- `packages/pytest.ini` — repo-wide: `asyncio_mode = auto` (async tests need no
  decorator) and registers the one custom marker:
  `flaky: known-flaky test, quarantined with a written reason (see README)`.
- Per-package `[tool.pytest.ini_options]` in `pyproject.toml` mirrors this for
  isolated runs (e.g. `packages/worker/pyproject.toml`).
- **Flaky quarantine convention** (root `README.md`, "Flaky tests" section):
  mark with `@pytest.mark.flaky` + a one-line reason in the docstring.
  Quarantine, never silently skip: either fix the root cause or
  `pytest.mark.skip(reason=…)` with a tracking note so it shows in run output.
  As of 2026-07-03 **zero tests carry the marker** — the mechanism exists, the
  quarantine is empty. Keep it that way.

### Running tests

```bash
# everything (the gate)
make test
# one package
make test-worker            # or test-orchestrator / test-scenario
cd packages && python -m pytest mcp-server/tests -q
# one file / one test
cd packages && python -m pytest worker/tests/test_example_scenarios.py -v
cd packages && python -m pytest worker/tests/test_engine.py -k chip -q
# with coverage
make test-cov
```

Always run from `packages/` (or via make) — `packages/pytest.ini` supplies the
async mode and markers there.

## 3. The golden inventory (executable documentation)

- **Example scenarios** — `examples/scenarios/*.json` (7 on 2026-07-03:
  `code_step_surcharge`, `payshield_hsm_smoke`, `testpay_heartbeat_echo`,
  `testpay_iso8583_purchase_reversal`, `testpay_payment_auth`,
  `testpay_refund`, `testpay_reversal`). Every file auto-runs in the suite via
  the guard test (§1). These are the living spec of the scenario schema.
- **Certification packs** — curated regression suites, built in code at
  `packages/scenario-service/models/pack.py` (`BUILTIN_PACKS`; exactly **1 pack** on
  2026-07-03: `switch_settlement`, 2 cases). `POST /packs/{id}/install` imports a pack's scenarios into a
  fresh project; after a run, `report_service.generators.certify()` scores it:
  `compliance_pct = passed/total`, `certified` only when **100%** of cases pass
  (any `not_run` case blocks certification). HTML badge via the orchestrator's
  certification endpoints (`packages/orchestrator/api/main.py`, around the
  `certify` imports from report_service).
- **Run-vs-run diffing** — `GET /runs/{run_id}/compare?to=<base>` (functional
  runs) and `GET /load-runs/{run_id}/compare?to=<base>` (load runs; defaults to
  previous comparable run) on the orchestrator.
- **Sign-off baseline** — `SignoffStore` (`packages/orchestrator/api/
  signoff_store.py`) keeps a baseline pointer per `(project, pack, environment)`
  = the last run that got a GO. The regression gate always diffs against what
  actually shipped, not an arbitrary run.
- **Sign-off / certify (ADR-0003**, `docs/adr/0003-report-gates-provenance-two-modes.md`**)** —
  `POST /runs/{run_id}/certify` evaluates gates, stamps provenance (pack
  version, resolved endpoints, principal, baseline run id), computes a
  tamper-evident `content_hash`, and freezes an **immutable** snapshot. Evidence
  is never mutated afterwards; only the approval trail appends
  (`POST /signoffs/{sid}/approve`). Printable artifact:
  `GET /signoffs/{sid}/html` (Print → PDF).

## 4. Acceptance thresholds in code (exact values)

### Sign-off gates — `packages/report_service/gates.py` (`GatePolicy`)

Defaults (all overridable via the `policy` dict on certify):

| Gate | Default | Meaning |
|---|---|---|
| `tiers` | `{"all": 100.0}` | minimum pass-% per priority tier; `"all"` matches every case. Typical pack policy: `{"P0": 100, "P1": 95}` |
| `require_coverage` | `True` | every pack case must have actually run (pack mode only) |
| `forbid_not_run` | `True` | **no_silent_skips**: any `not_run` / `blocked` / `pending` outcome (the `SKIP_STATUSES` frozenset) blocks GO — "absence of evidence" |
| `max_regressions` | `0` | steps that passed in the baseline (last GO) must still pass |
| `allowed_environments` | `None` (off) | when set, the run must have hit an approved env — a sim-only run is not a prod-readiness signal |

Verdict is `GO` only when **every** applicable gate passes; `blocking` lists
the failed gate ids.

### Resilience certification — `packages/orchestrator/api/resilience.py`

`ResilienceThresholds` defaults (overridable per run):

| Threshold | Default | Meaning |
|---|---|---|
| `min_availability_ratio` | `0.90` | storm-stage success rate ≥ 90% of baseline success rate |
| `min_recovery_ratio` | `0.98` | post-storm success rate ≥ 98% of baseline |
| `max_latency_multiple` | `4.0` | storm p95 latency ≤ baseline p95 × 4 |
| `pass_score` | `70.0` | overall 0–100 score bar |

Component weights (`WEIGHTS`): availability 0.35, absorption 0.30,
recovery 0.25, latency 0.10. Grade ladder (`_grade`): A+ ≥95, A ≥90, B ≥80,
C ≥70, D ≥55, else F. Verdict is `PASS` only when `score >= pass_score` **and**
no hard gate failed (availability, no_wedge, recovery, latency).

### Certification packs — `packages/report_service/generators.py`

`certified` requires `passed == total` (100% compliance); per-tier breakdown in
`by_priority`; `failed_cases` and `not_run_cases` are named explicitly.

## 5. How to ADD a test

General: plain pytest, `asyncio_mode=auto` (write `async def test_…` directly),
module docstring stating what is guarded and how to run it. Match the file
you sit next to.

### worker (`packages/worker/tests/`)

Idiom (see `test_engine.py`, `test_example_scenarios.py`): build a mock env
dict (`{"mode": "mock", "adapters": {...}}`), instantiate
`WorkerEngine(MOCK_ENV, InMemorySink())`, `await engine.run_scenario_batch([...])`,
assert on statuses (`PASSED`/`FAILED`/`BLOCKED` constants from `worker.engine`).
No conftest tricks needed.

### orchestrator (`packages/orchestrator/tests/`)

`conftest.py` pre-sets `PAYPROBE_ENV=test` (keeps the fail-closed auth gate
open) and `PAYPROBE_ALLOW_UNAUTH_CODE=1` (code nodes without sandbox). Idioms
(see `test_certification.py`): set `os.environ["DISABLE_SCHEDULER"] = "1"`
**before** importing `orchestrator.api.main`; swap stores to in-memory in a
fixture (`m.run_store = RunStore(":memory:")`, same for signoff/simulator
stores). Auth behaviour itself is tested separately in `test_auth_gate.py`.

### scenario-service (`packages/scenario-service/tests/`)

`conftest.py` sets `PAYPROBE_ENV=test` — the **auth-open pattern**: most tests
drive endpoints token-free; auth is exercised only where a test sets
`API_TOKEN` explicitly. Stores accept `":memory:"`
(see `test_connections.py`: `ConnectionStore(":memory:")` + draft-model
round-trips). Imports are package-relative to the service dir
(`from api.connection_store import …`).

### mcp-server / payprobe-assistant

Their `conftest.py` files `sys.path.insert` the package dir so tests run from
`packages/`. The assistant's conftest also defines the in-memory fake of the
PayProbe REST surface — extend that fake rather than mocking HTTP ad hoc.

### Adding an example scenario (auto-running, zero test code)

Drop a scenario JSON into `examples/scenarios/` — `make test` picks it up
automatically via the guard test. Shape (see `testpay_payment_auth.json`):
`name`, `steps[]` with `id`/`target`/`action`/`payload`/`assertions[]`
(`field`/`operator`/`expected`), optional `edges` (omit = top-to-bottom).
Rules: it must produce a clear pass/fail **in mock mode** (the guard runs it
with `{"mode": "mock", "adapters": {}}`); per the README, **don't add a
scenario you can't actually run**.

## 6. Portal testing reality

- **Zero unit specs**: `find packages/portal/src -name "*.spec.ts"` → 0
  (verified 2026-07-03). Do not look for Karma/Jest; there is none. CI's
  `test-portal` job only checks Prettier formatting + production build.
- **Playwright e2e** in `packages/portal/e2e/`:
  - `golden-paths.spec.ts` — backend-free UI smoke; seeds a fake session in
    `localStorage` (`pp.auth.token` / `pp.auth.user`) to pass the auth guard.
    Runs in CI (`portal-e2e` job).
  - `full-flows.spec.ts` — full-stack flows (author→run→report, load test);
    **skipped unless `E2E_FULL=1`** and a backend stack is up.
- Commands (from `packages/portal/`):

```bash
npm run e2e:install                       # one-time; Playwright is deliberately NOT in package.json
npm run e2e                               # build+serve+run golden paths
E2E_BASE_URL=http://localhost:4200 npm run e2e    # against an already-running portal
E2E_FULL=1 npm run e2e                    # full flows; bring the compose stack up first
```

## 7. CI map (`.github/workflows/ci.yml`, verified 2026-07-03)

| Job | Runs |
|---|---|
| `test-worker` | ruff + black check, then worker pytest with coverage (py3.11) |
| `test-services` | report_service, orchestrator, scenario-service pytest (postgres+redis service containers) |
| `test-portal` | Prettier check + `npm run build` |
| `portal-e2e` | Playwright golden paths (backend-free; full-flows stay skipped) |
| `mock-integration` | docker compose mock-mode stack + JWT-authenticated smoke run |

Plus `security-scan.yml` (Syft SBOM, Trivy). Note again: mcp-server,
payprobe-assistant and auth-service suites are not in CI — `make test` is the
broader gate for the first two; run auth-service manually.

## Provenance and maintenance

Authored 2026-07-03 against the live repo. Everything above was verified by
reading the cited files and running collection. Re-verify volatile facts:

```bash
# test counts (per package) — update the §2 table
cd packages && for p in worker orchestrator scenario-service mcp-server payprobe-assistant auth-service report_service; do \
  echo "== $p =="; python -m pytest $p/tests --collect-only -q 2>&1 | tail -1; done
# make test package list
grep '^PKGS' Makefile
# flaky quarantine population (expect empty; investigate any hit)
grep -rn "mark.flaky" packages --include="*.py"
# example scenario inventory
ls examples/scenarios/
# gate defaults
grep -n -A6 "class GatePolicy" packages/report_service/gates.py
# resilience thresholds + weights + grade ladder
grep -n "min_availability_ratio\|min_recovery_ratio\|max_latency_multiple\|pass_score\|WEIGHTS\|def _grade" -A2 packages/orchestrator/api/resilience.py | head -40
# builtin pack count (list entries, not the class def)
grep -c "^    Pack($" packages/scenario-service/models/pack.py
# portal unit-spec count (expect 0)
find packages/portal/src -name "*.spec.ts" | wc -l
# CI job list
grep -E "^  [a-z-]+:" .github/workflows/ci.yml
```

Drift risks: test counts (grow constantly), pack count, example-scenario list,
threshold defaults (if someone tunes `GatePolicy`/`ResilienceThresholds`), and
the auth-service/CI coverage gap (fix may land; re-check before repeating it).
