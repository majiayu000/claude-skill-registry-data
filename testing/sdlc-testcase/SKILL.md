---
name: sdlc-testcase
description: Invoked explicitly by /gen-testcase. Derives a human-readable test case catalog from the SRS scenarios and the tech design's test strategy — happy path, edge, negative and non-functional — before any test code exists. For AI features it also authors the evaluation cases. Produces specifications only, never test code.
argument-hint: "<UC-ID | FEAT-ID>"
disable-model-invocation: true
---

# /gen-testcase — the test case catalog

This phase writes **specifications a person can read and execute by hand**. No test code
is produced here. The catalog is the hand-off document that `/unittest` and `/run-test`
then partition between themselves by the `Level` column.

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

**Phase inputs** — phase `testcases`, gate: none (validated downstream by G5a/G5b),
inputs: the in-scope `.feature` files + techdoc §9, template
`{{paths.templates_dir}}/testcase-spec.md`, output
`{{paths.testcase_dir}}/{FEAT-ID}/TC-{UC-ID}.md`.

---

## Step 1 — Input check

Gate Step 2.7 has already run `.agent/steps/input-check.md` against
`input_contracts.testcases`. Act on its verdict:

- `NO_SOURCE` — no scenarios. The catalog is derived from them; report and **stop**.
- `NOT_READY` — usually scenarios exist but techdoc §9 does not assign a Level and an
  Oracle to every SC-ID. Report which SC-IDs are unassigned and **stop**. Choosing levels
  yourself would silently move the decision from design time to test-authoring time, and
  that is how a suite drifts into one slow integration run.
- `PARTIAL` / `READY` — proceed.

Hand-written scenarios and a hand-written techdoc are valid inputs.

## Step 2 — Read the sources

The `.feature` scenarios (behaviour and tags) and techdoc §9 (the assigned Level and
Oracle per SC-ID). §9 is authoritative — it was decided at design time precisely so this
phase would not have to improvise.

## Step 3 — Write the catalog

One table per scenario. Columns:

`TC-ID | Level | Preconditions | Steps | Test data | Expected result | Oracle | Automated by | Status`

- `TC-ID` = `TC-{SC-ID}`, suffixed `-A`, `-B` … when one scenario needs several cases.
- `Automated by` is left **empty** — `/unittest` and `/run-test` fill it with
  `path::test_name`. An empty cell after those phases is a gate failure; an empty cell
  now is correct.
- `Status` starts as `not-run`.

**Expected result must be checkable.** "Works correctly" is not a result. Write the
observable outcome: the status code, the field values, the exception type, the rejection
reason. If you cannot state what correct looks like, the scenario is ambiguous — report a
`spec-gap` finding routed to `srs` rather than writing a vague row that will be
interpreted differently by whoever automates it.

## Step 4 — Cover more than the happy path

Every scenario gets its happy case. Then add, in `## Negative & edge cases`:

- boundary values on every constrained input — empty, one, maximum, maximum plus one
- malformed and wrong-type input
- the failure of each dependency the sequence touches
- authorisation and ownership violations where relevant
- idempotency and repeat submission, where the operation is not naturally idempotent
- the numbers from each NFR that applies to this use case

In `## Data variants`, list the input sets that exercise genuinely different paths.
Three variants that all take the same branch are one test case with extra runtime.

## Step 5 — AI evaluation cases (when `ai_class != none`)

For scenarios with `Level: eval`, author
`{{paths.eval_data_dir}}/{name}/{version}/cases.jsonl` following `eval_case_schema` in
`.agent/modules/ai-llm/stack-profile.yaml`. One JSON object per line:

- `id` — `EV-{name}-{nnn}`
- `origin` — `golden` (the core set), `adversarial` (built to break it), `regression`
  (added because something failed once), `prod-sample`
- `trace` — the SC-ID or BUG-ID this case exists to protect
- `input` — the prompt's declared variables
- `expect` — `json_schema`, `must_contain`, `must_not_contain`, `max_output_tokens`,
  optional `reference` for similarity, optional `judge` rubric minimums
- `tags` — buckets used to slice results later

Build the golden set from the scenarios; build the adversarial set from the PRD's
tolerated-failure-modes list. Cases carried over from a previous version keep their ids —
renumbering them breaks comparison against the recorded baseline, which is the only thing
a judge oracle can gate on.

Every case needs at least one **structural** expectation. A case that only carries a
judge rubric cannot fail deterministically, so it cannot protect anything.

## Step 6 — Say what will not be automated

`## Not automated` — each row with a reason. Manual-only is a legitimate answer for
physical devices, third-party sandboxes and visual judgement. An unstated exclusion is
not: it reads as coverage that does not exist.

Anything listed here needs a matching row in `.agent/state/trace-waivers.tsv` with an
owner and an expiry, or `/trace` will report it as a missing test (T3).

## Step 7 — Record

Update state: `phase: testcases`, the testcase artifact paths, the eval data paths. No
gate runs here — the catalog is validated by G5a and G5b, once the rows have been
automated and executed.

---

## Boundaries

- **Do not write test code.** Not even a snippet. The moment this document contains
  code, it stops being reviewable by the people whose judgement it exists to capture.
- Do not change a scenario's Level or Oracle from what §9 assigned. Disagreement is a
  finding routed to `techdoc`.
- Do not invent expected behaviour absent from the scenario. Report the gap.
- Do not write a case you know the implementation currently fails and mark it optional.
  Write it, and let it fail — that is a finding, and hiding it here is how a suite comes
  to describe the code instead of the requirements.
