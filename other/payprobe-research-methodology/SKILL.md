---
name: payprobe-research-methodology
description: >
  WHEN a claim counts as proven in PayProbe — the evidence bar and idea lifecycle that turn a hunch into an accepted result. Load this
  when you are about to claim a root cause, propose a fix or new mechanism, design an
  experiment, decide whether a hypothesis is proven, plan a migration/feature rollout,
  or decide whether to promote or retire an idea. Triggers: "I think the cause is…",
  "root cause", "hypothesis", "let's verify", "is this proven?", "should we flip the
  flag?", "should we remove this?", "the fix worked" (did it?), designing a benchmark
  or comparison, writing up an investigation, or reviewing someone else's claimed
  result. Encodes: the evidence bar (one mechanism explains ALL observations +
  survives assigned adversarial refutation), hypothesis-predicts-numbers-first, the
  idea lifecycle (hunch → spec → flag-gated build → verify → flip ON or documented
  retirement), where good ideas historically came from, and observed anti-patterns.
---

# PayProbe Research Methodology — from hunch to accepted result

Everything below is grounded in this repo's verified history (commits, specs,
docs/history/PROGRESS.md). This is not aspiration; it is how results have actually been
accepted here — plus the codified refutation step that makes the pattern explicit.

**Terms used once, defined once**
- **Root cause** — the mechanism that produces the symptom, not the place the symptom appears.
- **Flag-gated** — new behavior sits behind an environment variable/flag, default OFF, so one line reverts it.
- **No-op** — a change proven to alter nothing in the live system's observable behavior.
- **TPS** — transactions per second (load-test throughput unit).
- **ADR** — Architecture Decision Record, in `docs/adr/`.

## When NOT to use this skill

| You actually want | Go to |
|---|---|
| Concrete analysis recipes (queueing math, latency budgets, worked examples) | `payprobe-proof-and-analysis-toolkit` |
| The change gates themselves (what may merge, review rules, non-negotiables) | `payprobe-change-control` |
| What to research next / the four state-of-the-art ambitions | `payprobe-research-frontier` |
| Symptom → triage for a live bug (you're firefighting, not researching) | `payprobe-debugging-playbook` |
| Past investigations' outcomes (what was tried and rejected) | `payprobe-failure-archaeology` |
| Which doc to record a result in, and its template | `payprobe-docs-and-writing` |
| What counts as a passing test / acceptance threshold | `payprobe-validation-and-qa` |

---

## 1. The evidence bar

A root cause is **accepted** only when BOTH hold:

1. **One mechanism explains ALL observations — including the negatives.**
   It must explain what failed, *and why everything else passed*. A mechanism
   that only covers the failing case is a correlation, not a cause.
2. **It survived assigned adversarial refutation.** Before acceptance, a
   specific session/person is ASSIGNED the job of breaking the claim — propose a
   rival mechanism, find an observation the claim can't explain, or construct an
   experiment whose outcome would differ under the rival. Acceptance without a
   named refuter is provisional.

**House precedent (verified in `docs/history/PROGRESS.md`, baseline 2026-06-18).** Suite at
180 passed / 3 failed. The accepted root cause — `worker/pyproject.toml`
declared `python-pkcs11` and `iso8583` but **omitted `pycryptodome`**, so
`run_crypto()` in `worker/engine/crypto_tools.py` returned
`{"error": "pycryptodome is not installed in this runtime"}` — is recorded
under the header **"Root cause (measured, not assumed)"** and passes the bar:

- Explains all three failures: exactly the three `test_engine.py` tests with
  kind=`crypto` nodes, no others.
- Explains the negatives: the other 180 tests never enter the crypto path, so
  they pass. The degradation was *silent* (error dict, not exception) — which
  also explains why nothing crashed.
- Verified by prediction: declaring the dependency should flip exactly those 3
  → suite went 180→183 passed, 0 failed. It did.

Note what the bar bought: while *reproducing* (not guessing), the investigation
surfaced a second latent bug — the edge-less scenario path raising
`KeyError: 'target'` for non-action nodes — fixed as its own Iteration 2 with
its own new test. Reproduction pays twice.

**Refutation assignment in practice.** The repo's precedent for hostile review
of one's own results is `docs/history/project-review.md` (ranked weak spots *with
evidence*, 2026-06-20) and docs/history/PROGRESS.md's closing "Self-review — weakest part
now" item. This skill codifies the stronger form: name the refuter *before*
accepting. Give them the claim, the raw observations, and one question: *"what
observation would this mechanism NOT explain?"* If they produce one, you are
back to hypothesis.

## 2. Hypothesis predicts numbers — before running

Write down the expected **counts, latencies, status codes, pass/fail deltas**
BEFORE the experiment. A hypothesis compatible with any outcome is worthless —
if you can't state what number would falsify it, you don't have a hypothesis
yet, you have a mood.

House pattern, verified:

- **docs/history/PROGRESS.md iterations record expected vs got.** Iteration 1: expected the
  3 crypto tests to flip → "Result: full suite 180→183 passed, 0 failed."
  Iteration 2: new test added, 184 passed, "No regressions." The hardening pass
  closes with the load-bearing sentence: **"Each item verified before moving
  on; no expected result edited to pass."** That sentence is the rule: when
  reality disagrees with the prediction, the *hypothesis* changes, never the
  recorded expectation.
- **The platform ships machinery precisely to make numeric predictions
  checkable.** `GET /load-runs/{run_id}/compare` (in
  `packages/orchestrator/api/main.py`) diffs a load run against a baseline;
  runs persist `tps_series` + `tps_stability` and `error_categories` in their
  summary (`packages/orchestrator/api/load_coordinator.py`). So a performance
  hypothesis is stated as "compare vs run X will show ≤N% TPS drop and no new
  error category" — and the endpoint settles it.

Minimum form before any experiment (put it in the PR/PROGRESS entry):

```
Hypothesis: <one mechanism, one sentence>
Predicts:   <numbers: which tests flip, expected count, expected p99, expected status codes>
Falsified if: <the concrete observation that would kill it>
```

## 3. The idea lifecycle

Every idea that changes behavior walks this path. Both terminal states —
**adopted** and **retired** — are normal; only *stuck in the middle* is failure.

```
hunch → root spec (phased) → build flag-gated, default OFF
      → verify (tests + live no-op / safe-state check)
      → flip default ON            → …or documented retirement
```

Each stage, with its verified house exemplar:

| Stage | Rule | Verified exemplar |
|---|---|---|
| **Hunch → spec** | Behavior-changing ideas get a root-level spec with explicit backward-compatible phases before code | `docs/history/DEFAULT-CONNECTION-MODEL-SPEC.md` Phases **A–F**, each phase marked BUILT individually, "each backward-compatible; the fallback is removed last" |
| **Build flag-gated, default OFF** | The risky phase lands behind a flag | `docs/history/CONNECTION-ENV-MIGRATION-PLAN.md` Phase 4: "flag-gated, default OFF"; rollback for the flip is "a one-line revert" |
| **Verify: tests** | Per-phase test matrix in the spec, not ad hoc | Both specs carry a "Test matrix" section naming "the important one" (Phase C / Phase 4) |
| **Verify: live no-op check** | Before flipping, prove against *live state* what the flip will actually change | `GET /admin/migrate/collisions` returns `safe_to_flip` (`packages/scenario-service/api/env_migration.py`); the live registry check proved the migration was a **no-op** — "finalizing the default carried no data risk" (plan header, COMPLETE 2026-06-26) |
| **Flip default ON** | Only after the above; keep the escape hatch | Two flags now default ON in `packages/orchestrator/api/main.py`: `PAYPROBE_CONNECTION_OVERRIDE_WINS` (default `"1"`) and `PAYPROBE_DEFAULT_CONNECTION_RESOLUTION` (default `"1"`), each documented in-code as an escape hatch |
| **…or documented retirement** | If a better model wins, delete cleanly and record why | See below |

**Retirement is a result, not a failure.** Two verified cases:

- **`endpoints[]` + selection policies**: built in commit `7253479` ("implement
  participant groups with selection policies and routing capabilities"),
  removed in `fe59454` (2026-06-28) — `worker/adapters/routing.py` (114 lines)
  and `worker/tests/test_endpoint_selection.py` (85 lines) deleted outright,
  367 lines removed net; portal models/UI swept in the same commit. Reason: the
  per-connection endpoint model overlapped confusingly with participant groups.
  The *good part* survived: `selection.py` and groups were kept. Lessons live
  in `payprobe-failure-archaeology`.
- **Step environment override**: built end-to-end (backend
  `_attach_step_environments` in `packages/orchestrator/api/main.py` plus a
  step-editor dropdown), then the *UI was removed* when the per-env connection
  override matrix won as the single value source. Verify today: the backend
  resolver still exists; `environment_override` survives only in
  `portal/src/app/constructor/scenario.models.ts`, no editor component
  references it. Partial retirement — keep the mechanism, retire the surface —
  is also a legitimate outcome.

The gate rules for who approves a flip or a removal live in
`payprobe-change-control`; this skill defines what *evidence* the gate demands.

## 4. Where good ideas came from (verified history)

Prospect where the repo has actually struck ore:

1. **Periodic honest project reviews.** `docs/history/project-review.md` (2026-06-20)
   ranked weak spots with evidence and listed quick wins + new ideas. Traceable
   idea→shipped: the review proposed an in-app **"diagnose my run"** helper and
   a **reopenable load-run** view — both now marked ✅ in the same doc's status
   table (`report_service/diagnose.py` + `GET /runs/{id}/diagnose`;
   `GET /load-runs` + `/load/:id` replay). Reviews that name weaknesses
   honestly generate the roadmap for free.
2. **Standards-gap prioritization.** `docs/standards-gap-analysis.md` scores
   capability against ISO 8583 / scheme-conformance / test-process standards
   (✅/🟡/❌), tags "*(highest-impact gap)*" inline, and ends with "Recommended
   priorities". Gaps ranked against an external yardstick beat gaps ranked by
   annoyance.
3. **Dogfooding the platform on itself.** The review's product-polish idea is
   explicit that diagnose-my-run is "the manual version of what we just did for
   '0 TPS'" — a debugging session on PayProbe, by PayProbe's authors, became a
   PayProbe feature. When an investigation hurts, the pain is a feature spec.
4. **ADR "Forces" sections.** `docs/adr/0001-*` lists Forces (reuse the proven
   bus/heartbeat machinery; listeners are long-lived and addressable; keep the
   single-host dev path) before Options. Writing forces first exposes which
   options die on contact — cheaper than building them.

## 5. Checklist: hunch → accepted result (one page)

Work top to bottom; each unchecked box is where claims die later.

- [ ] **Define terms.** One sentence per ambiguous word in the claim ("slow", "flaky", "the env model"). If two readers could disagree on what passed, it's not defined.
- [ ] **State the mechanism.** One sentence, causal, specific to a code path.
- [ ] **Predict numbers.** Counts / latencies / status codes / which tests flip — written down BEFORE running. Include the falsifier.
- [ ] **Minimal experiment.** Smallest run that can distinguish your mechanism from its nearest rival. Prefer existing instruments: `make test`, `GET /load-runs/{id}/compare`, `GET /runs/{id}/diagnose`, `GET /diagnostics` (see `payprobe-diagnostics-and-tooling`).
- [ ] **All-observations test.** Does the mechanism explain every observation, including what did NOT fail? List the negatives explicitly.
- [ ] **Adversarial assignment.** Name the refuter (person or fresh session with only the raw observations). They get one job: break it. Record their attempt and outcome.
- [ ] **Spec if behavior changes.** Root-level phased spec (model: `docs/history/DEFAULT-CONNECTION-MODEL-SPEC.md`). No spec → no behavior change.
- [ ] **Flag if risk.** Default OFF, escape hatch documented in-code, rollback = one line. (Flag registry + add-a-flag checklist: `payprobe-config-and-flags`.)
- [ ] **Promote or retire.** Flip ON only after tests green + live safe-state check (model: `safe_to_flip`). If a better model won, delete cleanly in one commit and keep the salvageable parts explicitly.
- [ ] **Record in the right doc.** Iteration → `docs/history/PROGRESS.md` (expected vs got); decision → ADR; phased change → its spec's status lines; investigation post-mortem → failure archaeology. Which doc + template: `payprobe-docs-and-writing`.

## 6. Anti-patterns (each observed, each has a repo counter-example)

| Anti-pattern | Why it burns you | The house counter-example |
|---|---|---|
| **Fitting the mechanism to the first observation** | First observation of the pycryptodome case was "3 crypto tests fail" — a plausible-but-wrong fix was "fix the crypto math". Measuring found an undeclared dependency and a *silent* error-dict degradation | docs/history/PROGRESS.md insists "measured, not assumed" and categorizes before fixing ("Category (a): infra/dependency broken") |
| **Fixing the symptom, not the category** | Patching one failing test leaves the class of bug alive | Iteration 2 fixed the *dispatch path* (`_execute_node`, kind-aware) for ALL non-action node kinds in edge-less scenarios, not just the crypto node that surfaced it — and added a test for the category |
| **Editing the expectation to match the result** | Converts your test suite into a diary | "no expected result edited to pass" — docs/history/PROGRESS.md, hardening pass |
| **Keeping dead code "just in case"** | Dead paths accrete into a second, unowned model; the confusion cost recurs forever | This repo deletes cleanly: `fe59454` removed `routing.py` + its 85-line test file entirely (−367 lines) the moment the endpoint model lost — no commented-out husks, no deprecation limbo |
| **Un-falsifiable hypotheses** | "It's probably load-related" fits every outcome | The compare endpoint exists so you must say *which* number moves and by how much |
| **Flipping defaults on faith** | A migration you *believe* is safe is a production incident with a delay | `safe_to_flip` was computed against the live registry before the precedence flip; it proved the flip was a no-op, and only then did the default change |

---

## Provenance and maintenance

Authored 2026-07-03 against the live tree. Every citation above was verified by
the commands below; re-run them if this skill looks stale.

```bash
# Evidence bar + expected-vs-got + "no expected result edited to pass"
grep -n "measured, not assumed\|no expected result edited to pass\|180→183" docs/history/PROGRESS.md

# Numeric-prediction machinery
grep -n "load-runs/{run_id}/compare\|error_categories" packages/orchestrator/api/main.py
grep -n "tps_series\|tps_stability" packages/orchestrator/api/load_coordinator.py

# Lifecycle: phases, live no-op check, flags now defaulting ON
grep -n "^### Phase" docs/history/DEFAULT-CONNECTION-MODEL-SPEC.md
grep -n "safe_to_flip\|no-op" docs/history/CONNECTION-ENV-MIGRATION-PLAN.md
grep -n "PAYPROBE_CONNECTION_OVERRIDE_WINS\|PAYPROBE_DEFAULT_CONNECTION_RESOLUTION" packages/orchestrator/api/main.py

# Retirement: built then removed, cleanly
git log --oneline 7253479 -1 && git show --stat fe59454 | tail -15
ls packages/worker/adapters/ | grep -c routing   # expect 0
grep -rln "environment_override" packages/portal/src/app/constructor/   # expect only scenario.models.ts

# Idea sources
grep -n "Quick wins\|Diagnose-my-run\|Reopenable load runs" docs/history/project-review.md
grep -n "Recommended priorities\|highest-impact gap" docs/standards-gap-analysis.md
grep -n "### Forces" docs/adr/0001-distributed-topology-on-worker-fleet.md
```

Volatile facts to re-check on drift: the two flag defaults (they may gain a
successor model), the compare endpoint's summary keys, and whether the
`environment_override` model field has been fully removed from the portal.
The "assigned adversarial refutation" step is this skill's codification of the
house self-review precedent, not a pre-existing written rule — if
`payprobe-change-control` later formalizes it as a gate, defer to that wording.
