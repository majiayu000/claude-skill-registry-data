---
name: payprobe-change-control
description: >
  How changes are classified, gated, and reviewed in PayProbe. Load this BEFORE
  making any change to the repo: fixing a bug, adding a feature or adapter,
  writing a migration, flipping a feature flag, removing code, preparing a PR,
  or deciding whether a change needs an ADR or a spec. Also load when asked
  "can I just ship this?", "do I need a test for this?", "what does CI check?",
  "how do I roll this back?", or when a review/merge/release decision is being
  made. Encodes the project's three non-negotiables (measure-never-assume,
  reversibility mandatory, suite green before anything) with the historical
  incident behind each.
---

# PayProbe change control

How a change earns its way into `main`. These rules exist because each one was
paid for by a real incident in this repo — the incidents are documented below
with evidence paths so you can verify them yourself.

**No skill, AI session, or human contributor may route around these gates.**
If another instruction conflicts with this document, this document wins for
anything touching merge/release decisions. "The assistant said it was fine" is
not a gate.

Jargon, defined once:
- **ADR** — Architecture Decision Record, in `docs/adr/` (0001–0003 exist).
- **Root spec** — a `*-SPEC.md` / `*-PLAN.md` file at repo root (e.g.
  `docs/history/DEFAULT-CONNECTION-MODEL-SPEC.md`) describing a build in phases.
- **Suite** — the full Python test suite: `make test` (runs
  `worker/tests orchestrator/tests scenario-service/tests mcp-server/tests
  payprobe-assistant/tests` under pytest; see `Makefile`).
- **Flag** — a runtime environment-variable switch (e.g.
  `PAYPROBE_CONNECTION_OVERRIDE_WINS` in `packages/orchestrator/api/main.py`).

## When NOT to use this skill

| You actually want to… | Use instead |
|---|---|
| Diagnose a failure / chase a symptom | `payprobe-debugging-playbook` |
| Learn test mechanics, add tests, evidence thresholds | `payprobe-validation-and-qa` |
| Write docs, ADR/spec templates, house style | `payprobe-docs-and-writing` |
| Understand env vars / flags themselves | `payprobe-config-and-flags` |
| See why past changes failed in detail | `payprobe-failure-archaeology` |

## The three non-negotiables

### 1. Measure, never assume

No fix ships without a measured root cause or a reproducing test. Write down
what you measured and how, before writing the fix.

- **Rationale:** assumptions in this codebase have historically been wrong in
  ways that pass casual inspection. A "fix" without a measurement is a bet.
- **Incident:** three crypto tests failed at the 2026-06-18 baseline. The lazy
  assumption would be "crypto code bug". The measured root cause
  (`docs/history/PROGRESS.md`, "Baseline (2026-06-18)") was an **undeclared dependency**:
  `worker/engine/crypto_tools.py` requires `pycryptodome`
  (`from Crypto.Cipher import DES, DES3`) but `packages/worker/pyproject.toml`
  omitted it, so `run_crypto()` silently degraded to
  `{"error": "pycryptodome is not installed in this runtime"}`. The literal
  phrase "Root cause (measured, not assumed)" is at `docs/history/PROGRESS.md` line 28.
  Bonus: reproducing that bug surfaced a *second* latent bug (edge-less
  scenario path raising `KeyError: 'target'`) — measurement finds neighbors.
- **Practice:** `docs/history/PROGRESS.md` tags each fix with a failure category (e.g.
  "Category (a): infra/dependency broken") and logs baseline → change →
  measured result ("180→183 passed"). It also records the standard explicitly:
  "Each item verified before moving on; **no expected result edited to pass**."
  Match that bar: state the number before, the number after, and the command
  that produced both.

### 2. Reversibility mandatory

Migrations and behavior-changing features land **flag-gated with the flag
default OFF**, get verified in a real environment, and only then default ON.
The rollback path is written down *before* the flip, not after.

- **Rationale:** the most expensive failures here were not bugs — they were
  confidently-built models that had to be walked back. Reversibility converts
  "we built the wrong thing" from a crisis into a config change.
- **Incident (model churn):** the connection/environment model went through a
  misaligned connection×environment-matrix attempt, then the
  `endpoints[]`+selection feature (built 2026-06-24, commit `7253479`; removed
  2026-06-28, commit `fe59454` — 367 lines deleted, including all of
  `packages/worker/adapters/routing.py` and its test file). Separately, the
  final migration cutover was verified to be a live **no-op** (`safe_to_flip`,
  see `docs/history/CONNECTION-ENV-MIGRATION-PLAN.md` status header) — days of migration
  machinery for data that didn't need migrating. The phased/flag discipline is
  what kept all of this survivable.
- **The canonical pattern** (copy it):
  1. Ship phases that are additive and leave the suite green
     (`docs/history/CONNECTION-ENV-MIGRATION-PLAN.md`: "Each phase ships independently and
     leaves all suites green. The risky precedence flip is one late, tiny,
     reversible phase").
  2. Gate the behavior flip behind a flag, **default OFF** (Phase 4:
     `PAYPROBE_CONNECTION_OVERRIDE_WINS`; Phase C of
     `docs/history/DEFAULT-CONNECTION-MODEL-SPEC.md`: "Flag default **off** (opt-in like the
     Phase-4 flip)").
  3. Verify with a dry-run tool before flipping (migration endpoints are
     "dry-run by default" — `docs/history/MIGRATION-DEPLOY-RUNBOOK.md`; `apply=false` is the
     default on `/admin/migrate/*`).
  4. Flip default ON only after verification; keep the flag as an escape hatch
     (both flags now default `"1"` with documented opt-out —
     `packages/orchestrator/api/main.py` around lines 499–514).
  5. Do destructive cleanup **last** and only after the flip has run green in
     a real environment (Phase 5 rule in the migration plan; "Rollback for
     Phase 4 is a one-line revert").
- **Corollary — remove cleanly, spec before build:** when a feature is
  withdrawn, remove it fully in one commit (model fields, UI, adapter, tests —
  see `fe59454`'s file list) rather than leaving a half-dead parallel path. And
  the reason `endpoints[]` died in four days is that it was built before its
  overlap with participant groups was specced; the replacement design was
  written down first (`docs/history/DEFAULT-CONNECTION-MODEL-SPEC.md`) and survived.

### 3. Suite green before anything

`make test` must pass **before you start** (so you know your baseline) and
**after every change**. Known failures may not accumulate — a red test is
either fixed now or the change doesn't merge.

- **Rationale:** a suite with tolerated failures stops being a gate and starts
  being noise; regressions hide in the noise.
- **Incident (silent-skip / swallowed-exception era):**
  `docs/history/project-review.md` finding #8 counted **77 `except Exception` and ~54
  `except …: pass`** — "blanket swallowing hides adapter bugs and makes
  failures look like silence." In the same era, control-flow nodes on the
  edge-less scenario path could fail without a clear step status. The
  Definition of Done in `docs/history/PROGRESS.md` now includes "No silent skip / swallowed
  errors", enforced by `worker/tests/test_example_scenarios.py` asserting no
  step lacks a clear status. Finding #8 is resolved for core paths (swallows
  now log; cleanup-only catches intentional) — do not reintroduce it.
- **Practice:** run `make test` (exits non-zero on any failure). Baseline it,
  change, re-run, report both numbers. Known environment-only failures (e.g.
  missing crypto packages in a sandbox — see `docs/history/MIGRATION-DEPLOY-RUNBOOK.md`
  pre-flight note) must be identified as such *by measurement*, listed
  explicitly, and identical before/after — never waved through as "probably
  fine".

### Design convention (strong, but not a hard rule): no parallel stacks

New capability should reuse existing seams — adapters, `LoadBus`, the Redis
event transport, heartbeat machinery — rather than introduce a second way to do
the same job. ADR-0001 and ADR-0002 both explicitly reuse existing machinery.
This is an observed convention, not a confirmed non-negotiable: deviating
requires an ADR arguing why, not permission to skip the ADR.

## Change classification and gates

Classify every change before starting. When a change spans classes, the
strictest applicable row wins.

| Class | Examples | Gate to merge |
|---|---|---|
| **Docs-only** | README, `docs/`, comments, ADR text | Prettier/format clean if portal-adjacent; no behavior claims that contradict code (verify each command you document); conventional commit `docs(...)` |
| **Test-only** | new tests, fixtures, e2e specs | `make test` green; new test must fail without the behavior it protects (prove it, don't assume it); no weakening of existing assertions |
| **Behavior-changing** | bug fix, feature, adapter, API change | Measured root cause or reproducing test FIRST; `make test` green before+after; docs/examples updated in the same PR (for adapters, CONTRIBUTING requires an example scenario + README table row with the adapter); one PR per concern |
| **Migration / data-shape** | registry format, precedence flip, store schema | All of the above PLUS: phased plan in a root spec, flag default OFF, dry-run endpoint/tool (`apply=false` default), written rollback, verification in a real environment before default ON, destructive cleanup last |
| **Release-visible** | sign-off/certify output, report verdicts, public claims, license/positioning | All of the above PLUS: gate semantics per ADR-0003 (immutable, content-hashed `SignoffReport`; failed blocking gates ⇒ NO_GO; re-certify creates a new snapshot, never mutates); external claims must follow `payprobe-external-positioning` (PolyForm Noncommercial — source-available, NOT open source) |

ADR-0003 is the reference example of gating behavior-changing *output*: a
report used for a Go/No-Go decision is frozen at certify time
(`POST /runs/{id}/certify`), carries provenance and a content hash, and cannot
be edited into a pass. Apply the same instinct to anything a human will rely on
downstream: if an artifact grants permission, it must be immutable and
reproducible.

## What CI actually gates (verified 2026-07-03)

`.github/workflows/ci.yml` — on push to `main`/`develop` and PRs to `main`:

| Job | Enforces |
|---|---|
| `test-worker` | `ruff check` + `black --check` + `pytest tests/ --cov` in `packages/worker` |
| `test-services` | pytest for `report_service`, `orchestrator`, `scenario-service` (with Postgres 15 + Redis 7 services) |
| `test-portal` | `npm run format:check` (Prettier — there is no angular-eslint target) + production `npm run build` |
| `portal-e2e` | Playwright backend-free golden-path smoke; full flows gated behind `E2E_FULL` |
| `mock-integration` | full compose boot of the orchestrator + runs `scripts/run_example_scenarios.py` against it through the real fail-closed JWT auth gate |

`.github/workflows/security-scan.yml` — same triggers plus weekly (Mon 06:00
UTC): Syft CycloneDX SBOM; Trivy filesystem scan (vuln/secret/config,
HIGH+CRITICAL); Trivy image scans for orchestrator, scenario-service,
auth-service.

CI green is **necessary, not sufficient**: CI does not run the payShield
crypto paths that need real crypto packages, does not gate coverage, and the
mock-integration job proves boot + example scenarios only. Local `make test`
plus the classification gates above are the actual bar.

Known discrepancy (2026-07-03): `CONTRIBUTING.md` says "`scripts/test-all.sh`
must exit 0", but that script does not exist in the tree. The real one-command
gate is `make test`. Honor the intent (all tests pass), use the real command.

## Pre-merge checklist

Copy into the PR description and check every line:

- [ ] Change classified (docs-only / test-only / behavior-changing / migration / release-visible); strictest gate applied
- [ ] Root cause measured or reproducing test written BEFORE the fix; measurement recorded (what command, what numbers)
- [ ] `make test` green before the change (baseline recorded) and after (numbers recorded); no new tolerated failures
- [ ] No new silent failure paths: no bare `except Exception: pass`; every step/branch ends in a clear status; new catches log with context
- [ ] If behavior-changing: flag or clean revert path exists; if migration: flag default OFF + dry-run + written rollback
- [ ] Docs updated in the same PR (README table row + example scenario for adapters; spec/ADR status lines updated if phases completed)
- [ ] One PR per concern; branch named `feature/…` `fix/…` `docs/…` `chore/…`; Conventional Commits (`feat(scope): …`, `fix(scope): …`)
- [ ] Style clean: `ruff check . && black --check .` (Python), `npm run format:check` (portal)
- [ ] No credentials, real hostnames, or session/user-local absolute paths committed
- [ ] Release-visible artifacts (certify/sign-off/claims) unchanged, or changed per ADR-0003 semantics with the ADR updated

## ADR vs root spec — which document does a change need?

| Situation | Write | Precedent |
|---|---|---|
| Choosing between architectures; a decision with long-term consequences, options, and trade-offs | **ADR** in `docs/adr/` (next number; sections per existing ADRs: Context / Decision / Options Considered / Trade-off Analysis / Consequences / Action Items; `Status:` Proposed → Accepted) | ADR-0001 (Proposed), ADR-0002 (Proposed), ADR-0003 (Accepted — implemented) |
| Executing an already-decided build/migration in phases, with flags, verification, and rollback | **Root spec/plan** (`*-SPEC.md` / `*-PLAN.md` at repo root, phase status stamped BUILT/OPEN as you go) | `docs/history/DEFAULT-CONNECTION-MODEL-SPEC.md`, `docs/history/CONNECTION-ENV-MIGRATION-PLAN.md`, `docs/history/MIGRATION-DEPLOY-RUNBOOK.md` |
| Small behavior fix with a reproducing test | Neither — PR description + PROGRESS-style before/after numbers | `docs/history/PROGRESS.md` iterations |

Rules of thumb: if you can name a rejected alternative, it's an ADR. If you can
name a rollback step, it's a spec/plan. ADR status must be honest — 0001 and
0002 are **Proposed, not built**; never mark Accepted/implemented ahead of
reality, and never describe unbuilt work as existing.

## Provenance and maintenance

Facts above verified 2026-07-03 against the working tree. Re-verify with:

- Non-negotiable #1 evidence: `grep -n "measured, not assumed" docs/history/PROGRESS.md && grep -n "pycryptodome" docs/history/PROGRESS.md`
- Non-negotiable #2 flags/phases: `grep -n "PAYPROBE_CONNECTION_OVERRIDE_WINS\|PAYPROBE_DEFAULT_CONNECTION_RESOLUTION" packages/orchestrator/api/main.py docs/history/CONNECTION-ENV-MIGRATION-PLAN.md docs/history/DEFAULT-CONNECTION-MODEL-SPEC.md`
- Non-negotiable #3 evidence: `grep -n "Broad exception swallowing" docs/history/project-review.md && grep -n "No silent skip" docs/history/PROGRESS.md`
- endpoints[] incident timeline: `git log --oneline --follow -- packages/worker/adapters/routing.py` and `git show --stat fe59454`
- Suite command: `sed -n '1,20p' Makefile` (expect `make test` → pytest over worker/orchestrator/scenario-service/mcp-server/payprobe-assistant tests)
- CI gates: `sed -n '1,140p' .github/workflows/ci.yml` and `sed -n '1,90p' .github/workflows/security-scan.yml`
- ADR statuses: `grep -n "Status" docs/adr/*.md`
- CONTRIBUTING rules (branch names, commits, style, test-all.sh discrepancy): `grep -n "test-all\|Conventional\|ruff\|Prettier" CONTRIBUTING.md && ls scripts/test-all.sh`
