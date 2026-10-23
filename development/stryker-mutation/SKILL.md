---
name: stryker-mutation
description: "Configures StrykerJS for mutation testing of JavaScript / TypeScript / React / Vue / Svelte / Node - picks the test-runner plugin (`@stryker-mutator/jest-runner`, `mocha-runner`, `vitest-runner`, `karma-runner`), authors `stryker.conf.json` with mutate globs + thresholds, runs incremental mode for PRs (only mutate changed files), and reports the mutation score. Use when a JS/TS test suite has ≥80% line coverage and the team wants to verify the tests actually catch bugs (not just touch lines)."
---

# stryker-mutation

## Overview

Per [stryker-intro][si]:

[si]: https://stryker-mutator.io/docs/stryker-js/introduction/

> "Stryker started as a pure JavaScript mutation testing
> framework" and now "supports most JavaScript projects, including
> TypeScript, React, Angular, VueJS, Svelte, and NodeJS."

Mutation testing introduces small bugs (mutants) into the production
code; if tests still pass, the test suite is too weak. **A green
suite with high mutation-survival rate** is the bug coverage hides.

## When to use

- A JS/TS suite has ≥80% line/branch coverage and the team wants
  to verify assertions actually catch bugs.
- Code review keeps surfacing weak assertions in tests
  (`.toBeTruthy()` etc); mutation testing makes the cost visible.
- A critical module needs a higher quality bar than coverage alone
  proves.

## Step 1 - Install

```bash
npm install --save-dev \
  @stryker-mutator/core \
  @stryker-mutator/jest-runner   # or mocha-runner / vitest-runner / etc.
```

Per [stryker-intro][si], supported runners include Jest, Mocha,
Karma, Vitest, Jasmine, Cucumber, Tap.

## Step 2 - Initialize

```bash
npx stryker init
```

Generates `stryker.conf.json`:

```json
{
  "$schema": "./node_modules/@stryker-mutator/core/schema/stryker-schema.json",
  "packageManager": "npm",
  "reporters": ["progress", "clear-text", "html"],
  "testRunner": "jest",
  "coverageAnalysis": "perTest",
  "mutate": ["src/**/*.ts", "!src/**/*.test.ts"],
  "thresholds": { "high": 80, "low": 60, "break": 50 }
}
```

Key fields:

| Field                | Use                                                                         |
|----------------------|-----------------------------------------------------------------------------|
| `mutate`             | Glob patterns: which files to mutate; exclude tests + types.               |
| `testRunner`         | `jest` / `mocha` / `vitest` / `karma` / etc.                                 |
| `coverageAnalysis`   | `perTest` (fastest - only re-run tests that touched the mutated line).      |
| `thresholds.break`   | Mutation score below this → `npx stryker run` exits non-zero (CI gate).    |
| `incremental`        | `true` to only mutate files changed since last run.                         |
| `concurrency`        | Worker count (default = CPU count).                                         |

## Step 3 - Run

```bash
npx stryker run
```

Per-mutant output:

```
[Survived] Conditional Boundary
src/cart.ts:42:5
- if (item.qty < 0) throw new Error(...);
+ if (item.qty <= 0) throw new Error(...);
Tests run: 12 (all passed - mutant survived).
```

**Survived mutant = tests passed despite the introduced bug** =
the tests don't actually catch this regression. Add a test for
qty = 0.

## Step 4 - Report + threshold

```
Ran 142 tests.
Mutants killed:    198
Mutants survived:   24
Mutants timed out:   3
Mutants no coverage: 12

Mutation score: 84.7%
```

Per [stryker-intro][si]: thresholds via the `thresholds` object
gate the build:

- `>= high` (80) → green.
- `>= low` (60) → yellow.
- `< break` (50) → red, exit code != 0.

The HTML report shows per-file mutation breakdown - drill in to
see which mutants survived and where to add tests.

## Step 5 - Incremental mode for PR runs

Full mutation runs are slow (5-30 min on medium codebases). For
PRs, incremental mode only mutates changed files:

```bash
npx stryker run --incremental
```

This stores state in `.stryker-tmp/` (commit to git so subsequent
runs benefit). Per-PR runs typically complete in <2 min.

## Step 6 - CI integration

```yaml
- name: Mutation testing (changed files only)
  if: github.event_name == 'pull_request'
  run: npx stryker run --incremental

- name: Full mutation run
  if: github.ref == 'refs/heads/main' && github.event.schedule == '0 2 * * 0'
  run: npx stryker run

- uses: actions/upload-artifact@v4
  if: always()
  with:
    name: stryker-report
    path: reports/mutation/
```

Pattern: incremental on PRs (fast feedback) + full weekly run on
main (catches drift in unchanged code).

## Anti-patterns

| Anti-pattern                                                          | Why it fails                                                              | Fix |
|-----------------------------------------------------------------------|---------------------------------------------------------------------------|-----|
| Setting `break: 100`                                                   | Impossible bar; team disables.                                            | Start at 50-60; ratchet up over time. |
| Running on every PR without `--incremental`                            | 30-min PR feedback loop; team disables.                                   | `--incremental` for PRs (Step 5). |
| Mutating test files                                                    | Mutants in test code don't reflect production quality.                   | Exclude in `mutate` glob (Step 2). |
| Ignoring "no coverage" mutants                                         | Files in `mutate` glob without any test coverage; mutation testing wastes effort. | Either add tests OR exclude those files from `mutate`. |
| Using `coverageAnalysis: off`                                           | Re-runs entire suite per mutant; very slow.                              | `perTest` (the default; Step 2). |
| Hard-coding break threshold without team agreement                      | Fails surprise PRs; team disables.                                       | Land threshold via PR with team review. |

## Limitations

- **Slow for large codebases.** Even with incremental + perTest,
  mutation testing scales worse than test execution.
- **Surviving mutants don't always indicate weak tests** - some
  are equivalent mutants (semantically identical to the original);
  flag and exclude these.
- **TypeScript checking adds time.** Disable type-check (`tsconfig.tsbuildinfo`)
  for mutation runs if not needed.
- **Per-runner integration quality varies.** Jest is the most
  mature; Vitest / Karma have known edges.

## References

- [si][si] - StrykerJS overview, supported test runners, supported
  frameworks (TS / React / Angular / Vue / Svelte / Node).
- `stryker-net-mutation` - 
  .NET sibling.
- `pitest-mutation` - Java sibling.
- `mutmut-mutation` - Python sibling.
- `mull-mutation` - C/C++ sibling.
