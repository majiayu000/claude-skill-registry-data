---
name: code-quality-instruments
description: Measure whether a test suite is any good, not only that it passes — branch coverage, mutation score, complexity-times-coverage risk, duplication. Use when adding or reviewing tests on a change that matters, a suite passes but a bug still shipped, coverage is high and confidence is not, or before promising a module is well tested.
---

The `testing` stance says whether tests are required. This is how you find out whether the ones
you wrote are worth anything.

A suite can reach full line coverage with no assertions at all. Every line executes, nothing is
checked, and the gate is green. Coverage measures what ran; it does not measure what was
verified. Everything below exists to close that gap.

## What to measure, in order of what it tells you

1. **Branch coverage, not line coverage.** Line coverage counts a two-way branch as covered when
   one side ran. Branch coverage is the cheapest upgrade available and usually the one that
   reveals the untested error path.
2. **Mutation score.** Change an operator, flip a boundary, delete a statement, then rerun the
   suite. A mutant that survives is a change to your code no test objects to. This is the only
   instrument here that measures assertions rather than execution, so it is the one that catches
   an assertion-free suite.
3. **Complexity against coverage.** A function that is both branchy and thinly covered is where
   defects concentrate. Either number alone is weak; the pair ranks the work. Robert Martin's CRAP
   formula is one published way to combine them, and any complexity report joined to a coverage
   report gets you the same ranking.
4. **Duplication.** A refactor signal, never a gate. Duplicated logic means a fix lands in one
   copy. Do not fail a build on it, and do not let a tool talk you into a bad abstraction.

## Per-language instruments

Verify each one against the `licensing` stance with the `licensing-review` skill before adopting
it. These run in CI rather than shipping inside the product, and the permissive-commercial stance
still makes no exception for tooling.

| Language | Branch coverage | Mutation | Duplication |
| --- | --- | --- | --- |
| Python | `coverage.py` with `branch = true`, usually via `pytest-cov` | `mutmut`, or `cosmic-ray` for a larger tree | `pylint --enable=duplicate-code`, or `jscpd` |
| TypeScript | `vitest --coverage` or `jest --coverage`, `branches` threshold set | Stryker Mutator | `jscpd` |
| Rust | `cargo-llvm-cov` | `cargo-mutants` | no standard tool worth adopting |
| Go | `go test -covermode=atomic -coverprofile` | `go-mutesting` | `dupl` |

Read the tool's own documentation for flags before the first run. A stale flag in a skill is
worse than no flag, and these move.

## How to run them

- **Differentially, against what changed.** Mutating a whole tree on every change buys a number
  nobody reads and a loop nobody waits for. Mutate the diff. Reserve a full run for a release or
  a scheduled job.
- **One at a time.** Coverage, mutation and duplication runs all spawn test processes. Run them
  concurrently and they contend for the same CPU, the same ports and the same fixtures, and the
  numbers get noisy in a way that looks like flakiness.
- **Bounded workers.** Pass an explicit worker limit rather than letting a tool take every core,
  or an unrelated command in the same session will time out.
- **Report progress on long runs.** A mutation run over a large module is indistinguishable from a
  hang without periodic output, and a killed run teaches nothing.

## What to do with the numbers

- **A surviving mutant is a missing assertion**, so write the assertion. It is not a reason to
  delete the mutant or add it to an ignore list.
- **Separate the testable from the environment-bound.** Code that opens a window, talks to a
  device, or needs a network is not a fair subject for these instruments. Push logic out of it
  until the untestable boundary is thin, then measure only the part that can be measured, and say
  which part that is.
- **Do not set a coverage threshold as the goal.** A threshold is a floor that stops regression.
  Chasing a number produces tests that execute code and assert nothing, which is the exact failure
  mutation testing exists to find.
- **Record the baseline** in the repo's agent instructions the first time you run an instrument,
  the way the verification gates record their clean-tree output, so a later movement is
  attributable.
