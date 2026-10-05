---
name: criterion-verification-map
description: "Transform acceptance criteria into plan-time runnable verification commands (behavioral, API, UI, error, performance, config, data, contract types) with expected evidence shapes and risk areas, then execute at verify time and assemble the evidence bundle with its mandatory completeness subsections, including test inputs/expected values taken from test source and risk-map coverage. Use when planning implementation against issue acceptance criteria or verifying completeness. This skill MUST be consulted because deferring verification to later causes incomplete PRs, and suppressing evidence gaps prevents the verdict judge from reasoning about gaps."
allowed-tools: Bash, Read, Grep, Glob, TaskCreate, TaskList, TaskUpdate, TaskGet
context: fork
agent: general-purpose
---

# Criterion Verification Map

## Contract

Iron law: **every acceptance criterion is an eval source: at plan time it must produce a runnable verification command, or planning is blocked.** Invoked by `/flow:start` at the Spec Validation Gate and PLAN (Phases 1-2) to classify each criterion and emit the task's verification fields, and at VERIFY (Phase 4) to run them and assemble the evidence bundle shaped by [`references/evidence-bundle-format.md`](../../references/evidence-bundle-format.md). Returns task fields at plan time, the bundle at verify time. Permitted skips: none; an unmappable criterion is escalated through the Spec Validation Gate.

## Classification

| Type | Signal words | Method |
|---|---|---|
| behavioral | "when X then Y", "should return" | unit/integration test |
| api | "status code", "endpoint", "header" | curl/fetch |
| ui | "displays", "renders", "layout" | screenshot + analysis |
| error | "error message", "invalid", "fails gracefully" | invalid-input test |
| performance | "within N ms", "timeout" | benchmark/timing |
| config | "config", "setting" | build/load test |
| data | "transforms", "output matches" | run with test data |
| contract | "schema", "type", "signature" | validator / type-check |

## Plan-time task fields

Tasks are atomic (`commands/start.md` Phase 2). Emit per criterion:

```
Criterion: {full criterion text}
Verification type: {type from the table}
Verification command: {exact runnable command}
Expected evidence: {what successful output looks like}
Does NOT promise: {non-goals scoped to this criterion}
Risk areas: {risk-map rows whose area this criterion's logic touches, verbatim | none | (disabled by specFirst.riskMap)}
```

`Does NOT promise` comes from the journal's `### Non-goals`, `Risk areas` from `### Risk map` ([`references/specification-journal-format.md`](../../references/specification-journal-format.md)). `implementation-planner` adds one discriminating test per risk row (input, expected, source). Any unfillable field: escalate through the Spec Validation Gate.

## Evidence collection protocol (verify time)

For each atomic task:

1. `TaskUpdate(taskId, status: "in_progress")`
2. Run the verification command
3. Capture output verbatim
4. `TaskUpdate(taskId, status: "completed", result: "EVIDENCE_COLLECTED")`

Then assemble one `## Criterion {N}` section each. `### Type` and `### Does NOT promise` are the plan-time fields; `### What was NOT tested`, `### Known limitations of this evidence`, `### Negative/adversarial cases covered` are authored honestly now (`none — {reason}` is positive; blank is an auto-FAIL). `### Visual analysis` copies every `Viewport:` and `Step:` block from the `visual-verification` result, or its `Flows: none — {reason}` line when no flow ran, never re-derived; non-`ui` types write `none — criterion type {type} has no visual surface`.

Two subsections come from test source, never memory:

- **`### Test inputs and expected values`**: open every test file the command or its output cites. For each test that ran, record one `| Test | Input | Expected | Source of expected |` row from its source: literal input, literal asserted value, its origin (spec/criterion text, reference implementation, hand computation, existing fixture, external standard). Implementation-captured values are written `implementation output`; the judge FAILs them. `none — {reason}` only for `ui`/`config` types.
- **`### Risk map coverage`**: for each `Risk areas` row, find the test whose input is its discriminating check and write `<area> → <test file:line>`. A row with no such test is a gap: add it or escalate. `none — {reason}` only when no row maps here; `none — risk map disabled (specFirst.riskMap=false)` only when the journal subsection is the disabled marker.

Validate the bundle against the reference (every mandatory subsection present, `none` only where permitted) before `Agent(verdict-judge)`.

## Judge isolation

The verdict-judge has no file tools and receives ONLY acceptance criteria, evidence bundle, and holdout-validation output — never diff, journal, planning notes, self-review findings, test source, or screenshots.
