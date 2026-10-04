---
name: assistant-tdd
description: "Apply Red-Green-Refactor. Use when tests-first/TDD is requested or required by project conventions."
---

# Test-Driven Development

## Goal

Protect each behavior change with verified RED, minimal GREEN, and
behavior-neutral REFACTOR evidence before production code is trusted.

## Success Criteria

- Each behavior starts with a test that fails for the intended reason.
- Production code is limited to the smallest change that makes that test pass.
- Targeted and relevant regression tests pass before the next cycle.
- RED/GREEN/REFACTOR evidence is recorded in the task journal or output.
- When a workflow Architecture Decision Pack carries semantic type, primitive-boundary, public compatibility, or quality-scenario obligations, tests prove those obligations rather than merely compiling wrappers.

## Constraints

- Never treat syntax, import, environment, or flaky failures as valid RED.
- Do not write production code before RED evidence exists.
- Ask every material question when behavior or acceptable test scope changes the test; group questions by topic with why, risk if guessed, and a safe default where available rather than enforcing a numeric quota.

## Progressive Contract Loading

Canonical tier files are `contracts/input.yaml`, `contracts/output.yaml`,
`contracts/phase-gates.yaml`, and `contracts/handoffs.yaml`.

Read `contracts/index.yaml` first and load only the active enforcement boundary:

- `entry` for activation, behaviors, debugging evidence, framework, and exceptions;
- `current_phase` for RED, GREEN, or REFACTOR; and
- `completion` for the returned cycle artifact.

The handoffs contract remains canonical but empty because `assistant-workflow`
owns cross-role dispatch. Missing or invalid selectors fall back to the full
named canonical contract; do not load every contract at entry.

## Ownership

assistant-tdd owns RED-GREEN-REFACTOR correctness. Generic workflow coordinates
task packets and role dispatch, but specialist gates are authoritative.

When workflow delegates, ownership follows `execution_lane` without weakening
the phase boundary:

- In `bounded_executor`, one bounded executor owns RED, GREEN, focused verification, and refactor safety; production code still starts only after valid RED evidence is recorded.
- In `separated_workers`, Builder/Tester owns RED, Code Writer owns GREEN, and
  Builder/Tester owns verification/refactor-safety. Use this lane for explicit
  independent RED evidence, high-risk work, or broad/noisy/environment-heavy
  verification.

Required RED evidence before production implementation:

- Test file and test name
- Command run
- Failure summary
- Why the failure proves the intended missing behaviour

When a workflow Architecture Decision Pack applies, bring only its testable obligations into the cycle: semantic type validation, primitive-boundary conversion, public-contract compatibility, a stated quality scenario, or a design-pressure check such as early exit, ownership/disposal, bounded resources, extension registration, or representative-path behavior. Do not invent a Pack or benchmark for ordinary local behavior. A memory, performance, or extensibility claim remains an explicit unknown until a workload, budget/threshold, measurement method, and failure condition are testable.

If TDD is active and RED evidence is missing, the selected production owner
must return `NEEDS_CONTEXT` and make no production changes.

## Cycle

1. **RED** — write one behavior test, run it, and verify the right failure. If it
   passes unexpectedly, inspect whether behavior already exists or the test is wrong.
2. **GREEN** — write the simplest passing code, rerun the target, then relevant
   regressions. Repair regressions before continuing.
3. **REFACTOR** — remove duplication or improve names without new behavior; keep
   tests green after each change.
4. Repeat for the next behavior.

For unknown-cause bugs, use `assistant-debugging` first. Start TDD only after
reproduction/root-cause evidence can define a meaningful regression test.

Allowed exceptions require recorded approval/reason when TDD is active:
throwaway spikes, generated code, docs-only work, behavior-free config, and
layout-only styling. Do not claim TDD completion for an exception.

## Output

Return status, cycle log with commands/outcomes, test and production files,
targeted/regression verification, approved exceptions, and blockers.

## Stop Rules

- Stop before production edits when RED is absent or invalid.
- Stop and repair the test when RED passes or fails for the wrong reason.
- Stop and repair regressions before the next behavior.
