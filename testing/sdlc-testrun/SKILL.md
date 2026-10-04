---
name: sdlc-testrun
description: Invoked explicitly by /run-test. Implements and executes the acceptance and live-integration tests from the test case catalog, records every result and the run detail into state, and triages each failure into a spec defect, code defect, test defect or flake with a route back into the chain.
argument-hint: "<FEAT-ID | UC-ID>"
disable-model-invocation: true
---

# /run-test — acceptance execution

## Protocol (shared — do not restate here)
Framework assets — `.agent/framework.yaml`, `.agent/steps/`, `.agent/rules/`,
`.agent/gates/`, `.agent/templates/`, `.agent/modules/` — resolve **project-first**: use
the repository's copy when it exists, otherwise `${CLAUDE_PLUGIN_ROOT}/.agent/…`. That is
how one repo can override a single template or rule without forking the framework.
`.agent/project-context.yaml` and `.agent/state/` are **always project-local** — never
read or write them under the plugin root.
1. If `.agent/state/context-cache.md` exists and its `framework_version` matches
   `.agent/framework.yaml`, Read ONLY that file. Otherwise Read
   `.agent/steps/context-loader.md` and execute it, then write the digest back to the cache.
2. Read `.agent/steps/gate.md` and execute it with the phase inputs below.
3. On completion, format output per `.agent/steps/report-footer.md`.
Never copy the contents of those files into this skill.

**Phase inputs** — phase `acceptance`, gate `G5b`, inputs the catalog + the in-scope
`.feature` files, outputs under `{{layout.acceptance_tests}}`, plus
`.agent/state/runs/{ISO8601}.json` and a run report under `{{paths.review_dir}}`.

---

## Step 1 — Select the rows

Only catalog rows with `Level` in `{acceptance, integration-live}`. `eval` rows are
`/eval`'s; unit rows were `/unittest`'s.

Gate Step 2.7 has already run `.agent/steps/input-check.md` against
`input_contracts.acceptance`. `NO_SOURCE` or `NOT_READY` → report and stop.

If `G5a_unit` has not passed, say so and recommend running `/unittest` first: the slow,
expensive suite should not be spent rediscovering what the fast one already knows. But
**this is advice, not a refusal** — QA may legitimately need to execute acceptance cases
against a build whose unit suite is red, to find out whether the failure is broader than
one module. Record `G5a: {verdict}` in the report so the result is read in context.

## Step 2 — Implement the acceptance tests

One test per row, under `{{layout.acceptance_tests}}`, named
`test_{UC-ID}` per the profile's conventions. Where the stack has a BDD runner, bind
directly to the `.feature` scenarios so the specification is executed rather than
transcribed — a transcription drifts from its source the first time either is edited.

Tag with `@trace.verifies` and `@trace.test_type=acceptance`, and mark them so the
default fast suite excludes them.

Acceptance tests exercise the system **through its real entry points**, with real
adapters where the row says `integration-live`. Reaching inside to set up state is
acceptable for arrangement; asserting on internals is not — that is a unit test in
disguise.

## Step 3 — Execute

Run `quality_commands.acceptance`. Capture per row: `pass`, `fail`, or `blocked`
(could not run — environment missing, dependency unavailable, precondition
unreachable).

Write the raw detail to `.agent/state/runs/{ISO8601}.json`: command, exit code, duration,
per-test outcome, and the failure output. This file is append-only history; keep it out
of the small state files that get read on every command.

## Step 4 — Triage every failure

**No failure may be recorded without a diagnosis.** An unclassified failure cannot be
routed, so it stalls the loop. Classify against `framework.yaml → loop_routes`:

| Observation | Diagnosis | route_to |
|---|---|---|
| Spec clear, system behaves differently | `impl_defect` | `code` |
| The test encodes the wrong expectation | `test_defect` | `tests` |
| Scenario ambiguous or untestable as written | `spec_gap` | `srs` |
| Requirement conflicts with the PRD or is new | `product_gap` | `prd` |
| An NFR cannot be met by this design | `design_gap` | `techdoc` |
| Passes and fails across identical runs | flaky | `tests` |

**Bias: when a test fails, the code is wrong.** Routing to `tests` or `srs` requires
stating why the test or scenario is the thing that is wrong, and leaves a change-log
entry in the SRS.

A `blocked` row is never silently acceptable — it needs a finding too, or the gate reads
an unrun test as an absence of problems.

Flakes get a finding of their own. A test that passes on retry has told you something
about the system or the test; suppressing it with a retry loop discards that.

## Step 5 — Write findings and the run report

Append one row per failure to `{{paths.findings}}`, with `id = RF-{FEAT-ID}-{nnn}`,
severity, category, `found_in: acceptance`, and the `route_to` from triage.

Write the run report to `{{paths.review_dir}}/{FEAT-ID}/TR-{nnn}-acceptance.md`:
command, environment, totals, the per-row table, and the triage summary.

## Step 6 — Evaluate G5b and record

Run `.agent/gates/G5b-acceptance.yaml`. For AI features it also requires a recorded eval
run for every touched prompt version, pass rate at or above the spec threshold, no
regression beyond tolerance versus baseline, and cost and latency within budget. Those
figures come from `/eval` — **if it has not run, this gate is `block`, not `pass`.**
Gates read the recorded eval state rather than triggering a run, so checking a gate never
costs money.

Update state: `phase: acceptance`, the verdict and `input_hash`, the acceptance counts in
`quality.json`, and the findings counts on the feature.

---

## Boundaries

- **Do not modify implementation code.** Diagnose and route; `/gen-code` fixes.
- Do not retry a failing test until it passes and call it green.
- Do not mark a row `blocked` to avoid a failure — blocked means genuinely could not run.
- Do not run the eval suite here. `/eval` owns it, so that a run's cost is always a
  deliberate command rather than a side effect.
- Do not weaken a threshold to pass a gate.
