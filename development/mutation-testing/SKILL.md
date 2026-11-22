---
name: mutation-testing
description: Check whether the tests actually catch bugs by mutating the code and seeing if the tests fail. Use after a slice passes its tests, before calling it done, and whenever a test suite looks green but unproven. JavaScript/TypeScript only. Only invoke via the orcinus router.
license: MIT
user-invocable: false
compatibility: Requires Node.js and Stryker (JavaScript/TypeScript only).
---

# MUTATION-TESTING — do the tests catch anything?

A green test suite proves nothing on its own. A test that passes no matter what the code does is not a test. Mutation testing proves the tests: change the code in small ways (mutants) and check whether the tests fail. A mutant the tests kill is proof the tests work. A mutant that survives is a gap in the tests — record it, do not hide it.

## Rules

- Baseline first. Run the four commands (build, lint, typecheck, test) before mutating. If they are not green, stop — mutation testing on a broken suite measures nothing.
- Never weaken a test to raise the score. A surviving mutant is fixed by adding or strengthening a test, never by deleting the mutant or the test.
- Never report a score without running. A score from memory, from another project, or from a failed run is not a score.
- A surviving mutant is a finding, not a failure to hide. List every one, with file and line.
- A check that did not run is never reported as passed.

## Steps, in order

### 1. Baseline

Run the four commands. Record their outputs. All must exit 0 and all tests must pass. If not, stop.

### 2. Run Stryker as-is

Use Stryker (stryker-mutator/stryker-js, Apache-2.0) as-is. Do not rewrite it, and do not hand-roll mutants when Stryker can generate them.

- Install: `@stryker-mutator/core` and `@stryker-mutator/typescript-checker` as dev dependencies.
- Configure (`stryker.config.mjs`): mutate `src/**/*.ts`; use the `command` test runner with the project's own test command (for example `npm test`) when the project uses `node:test`, which Stryker has no dedicated runner for; use the `typescript` checker so mutants that do not compile are reported as compile errors, not as killed.
- Add a `mutation` script to `package.json` (for example `"mutation": "stryker run"`).
- Run it. Record the full output.

### 3. Read the score

Record the exact numbers: total mutants, killed, survived, timed out, no coverage, compile errors, and the mutation score. There are two scores for the same run, and they are different numbers — never print a bare percentage. Label every score with its formula:

- killed-only: killed divided by (total minus no coverage minus compile errors).
- Stryker-printed: (killed plus timed out) divided by (killed plus timed out plus survived plus no coverage) — this is the score Stryker itself prints, and the score its break threshold gates on. Record it as printed, do not recompute it by hand.

A comparison across arms or runs is only valid when both sides use the same formula — comparing one side's killed-only against the other side's Stryker-printed score is a false comparison, not a result.

Rounding is outside the mutator set: Stryker generates no mutant for Math.round at all — in the demo, the line-16 mutants are only ArithmeticOperator swaps — so even a break threshold of 80 would not have caught a Math.round → Math.floor swap, and a 100.00 score does not cover that class. The boundary test (a non-divisible case) is the only closure for it; record it alongside the score.

### 4. Prove the check can fail

The report must name at least one mutant the tests killed, with file, line, and what changed. If no mutant was killed, the check proved nothing — say so, and do not call the suite tested.

### 5. List every surviving mutant

For each surviving mutant, record file, line, the change, and what test is missing. Each one is a test gap. Fix the gaps by adding tests (one slice at a time, test first), then re-run Stryker and record the new score. Do not delete code to make a mutant disappear, and do not mark a mutant as ignored without writing down why.

## Report

Return the report in this form:

- Baseline (four commands, with outputs).
- Stryker version and config (mutate pattern, test runner, checker).
- Mutation score with the exact numbers: both formulas, each labelled (killed-only and Stryker-printed).
- Killed mutants (at least one, with file and line).
- Surviving mutants (every one, with file, line, and the missing test).
- Verdict: PASS (both scores recorded and labelled, Stryker-printed score at or above the configured break threshold — the threshold gates on Stryker's printed score, not on killed-only — at least one mutant killed, all survivors listed; a passing score does not cover rounding — see Step 3) or FAIL (Stryker did not run, no mutant killed, survivors hidden, or Stryker-printed score below the break threshold).

## Scope

Python is covered by the companion skill `mutation-testing-python` (mutmut as-is, BSD-3-Clause). Other languages are still a gap — each needs its own verified CLI. The Trail of Bits mutation-testing skill (CC-BY-SA-4.0) is a separate licensed module, not copied here; it is referenced, not used, for non-JS/TS work.

## Sources

Method, in our own words, using Stryker (stryker-mutator/stryker-js, Apache-2.0, licence verified from the primary LICENSE file) as-is. No text was copied from Stryker. Trail of Bits mutation-testing is referenced, not copied (CC-BY-SA-4.0).
