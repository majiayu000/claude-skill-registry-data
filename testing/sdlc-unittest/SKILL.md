---
name: sdlc-unittest
description: Invoked explicitly by /unittest. Implements automated unit and mocked-integration tests from the test case catalog, using the test framework and file conventions of the active stack profile, tagging each test with @trace.verifies, and running the suite until coverage clears the profile minimum.
argument-hint: "<UC-ID | FEAT-ID | BUG-ID>"
disable-model-invocation: true
---

# /unittest — automated unit tests

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

**Phase inputs** — phase `unit`, gate `G5a`, input
`{{paths.testcase_dir}}/{FEAT-ID}/TC-*.md`, outputs under `{{layout.unit_tests}}` and
`{{layout.integration_tests}}`.

---

## Step 1 — Input check

Gate Step 2.7 has already run `.agent/steps/input-check.md` against
`input_contracts.unit`. Act on its verdict:

- `NO_SOURCE` — no test case catalog. Report and **stop**.
- `NOT_READY` — usually rows whose Expected result is not checkable ("works correctly",
  "returns the right thing"). Report those rows by TC-ID and **stop**: whoever automates
  an uncheckable row has to invent the expectation, and the test then encodes that
  invention rather than the requirement. **QA** owns those cells.
- `PARTIAL` / `READY` — proceed. A missing implementation is non-blocking — writing the
  test first is legitimate, and the failure is the point.

A hand-written catalog is a valid input.

## Step 2 — Select the rows

Take **only** catalog rows with `Level` in `{unit, integration-mocked}`. Rows marked
`acceptance`, `integration-live` or `eval` belong to `/run-test` and `/eval`; implementing
them here means running live systems in the fast suite, and the fast suite stops being
run.

## Step 3 — Read what exists

Read the existing test files for the modules in scope, and the shared fixtures. **Reuse
the fixtures.** A second fixture that does what an existing one does is how a suite
becomes impossible to reason about.

Read the implementation only to learn the seams — constructor signatures, injection
points, exception types. Do not read it to learn what to assert; assert the catalog's
Expected result. Reading the implementation for expectations is how tests come to
describe the bug rather than the requirement.

## Step 4 — Write the tests

One test per TC row. Follow the profile's `test_conventions`: `file_pattern` for file
names, `name_pattern` for test names (typically
`test_uc{n}_sc{m}_{expected_behavior}`), and `framework` for the idiom.

Tag every test with `@trace.verifies={UC-ID}-SC{n}` and `@trace.test_type={level}`, in
the syntax `traceability.tag_syntax` names.

Assert the **Expected result** and the **Oracle** the catalog specifies:

- `exact` — compare literally
- `schema` — assert shape, required fields, types and constraints, not exact content

**Isolation is not optional at this level.** No network, no real database, no real
broker, no real model. Inject through the protocol and substitute a double. A unit test
that reaches out is an integration test with the wrong label, and it will be the one that
fails in CI for reasons nobody can reproduce.

## Step 5 — Fill in the catalog

Write `path::test_name` into each row's `Automated by` cell and set `Status`. A test that
cannot be traced back to a case is a test nobody will know to update when the requirement
changes.

## Step 6 — Run and iterate

Run `quality_commands.test`, then `quality_commands.coverage`.

**When a test fails, the default diagnosis is that the code is wrong.** Do not adjust the
assertion to match observed behaviour. Classify against `framework.yaml → loop_routes`:

| Observation | Diagnosis | Action |
|---|---|---|
| Spec is clear, code does something else | `impl_defect` | finding routed to `code`; stop here |
| The assertion encodes the wrong expectation | `test_defect` | fix the test, and record the finding |
| The scenario is ambiguous | `spec_gap` | finding routed to `srs`; do not guess |

Changing a test requires a recorded finding. Silently relaxing an assertion is the single
fastest way to make a suite worthless, and it is invisible in review.

Coverage below `coverage_min` means missing cases, not a threshold to lower. Find which
branches are untested and check whether the catalog has a row for them; if it does not,
that is a gap in the catalog.

## Step 7 — Evaluate G5a and record

Run `.agent/gates/G5a-unit.yaml`: suite green, coverage at or above minimum, **no test
file that collects zero tests**, every unit-level row has `Automated by`, every test
tagged, no live provider reachable from a unit test.

The empty-file check is deliberate. An empty test file is worse than a missing one: it
reads as covered while covering nothing. Any placeholder file that a previous author left
behind under the profile's test globs must be filled or deleted before this gate passes —
report each one by path rather than quietly collecting zero tests from it.

Update state: `phase: unit`, the gate verdict and `input_hash`, and the coverage number
into `quality.json`.

---

## Boundaries

- **Do not modify implementation code.** If a test proves the code wrong, that is a
  finding routed to `code`. Even a one-line obvious fix — the separation is what keeps
  the diagnosis honest.
- Do not skip, xfail or mark a test optional to reach green. A skipped test carries a
  reason and a finding.
- Do not lower `coverage_min` or any threshold.
- Do not write acceptance or eval tests here.
- Do not delete an existing failing test to make the suite pass.
