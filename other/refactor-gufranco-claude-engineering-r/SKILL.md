---
name: refactor
description: Guided refactoring with behavior preservation verification. Identifies candidates (long functions, deep nesting, duplicated logic, god classes), proposes a refactoring plan, executes incrementally with tests between steps, and verifies no behavior change. Use when user says "refactor", "clean up this code", "simplify", "extract", "restructure", "reduce complexity", "split this file", or wants to improve code structure without changing behavior. For new features, use /plan; for bug fixes, use /investigate; for code review, use /review.
argument-hint: "/refactor | /refactor src/services/order.service.ts | /refactor src --plan-only"
allowed-tools: "Read, Grep, Glob, Edit, Write, Bash"
---

## Overview

Incremental refactoring workflow that enforces behavior preservation at every step. Each refactoring is a separate commit with test verification before and after.

The refactoring principles follow [`../../rules/code-style.md`](../../rules/code-style.md). This skill provides the execution workflow.

## When to Use

- Tests pass, and a function, file, or class crosses one of the Phase 2 thresholds.
- A feature is next, and the code it lands in has to be made easy to change first.
- `/module-audit` produced a consolidation the user picked.
- For new behavior, use `/plan`; for a bug, use `/investigate`; for feedback on a diff, use `/review`.

## Arguments

- No arguments: analyze the current branch diff for refactoring candidates.
- `<path>`: refactor the specified file or directory.
- `--plan-only`: identify and rank candidates without executing any changes.

## Process

### Phase 1: Establish Baseline

1. **Run the full test suite.** Record the result. If tests fail, stop. Do not refactor code with a failing test suite. The user must fix tests first.

2. **Record coverage.** If a coverage tool is configured, record the current coverage numbers for affected files. Coverage must not decrease after refactoring.

3. **Gate on coverage of the target.** Every line and branch the refactoring will move needs a test that observes its behavior; the suite passing proves nothing about code no test reaches. When coverage of the target is insufficient, or no coverage tool exists to show it, take one of two paths:
   - Write characterization tests first: tests that pin the current observable behavior, including behavior that looks wrong, through the public interface. Commit them alone as `test(<scope>): characterize <unit>` before any structural change.
   - Stop and report which units lack coverage. Never refactor uncovered code.

### Phase 2: Identify Candidates

Scan the target files for refactoring candidates. Check each category:

| Category | Threshold | Refactoring |
|----------|-----------|-------------|
| Long functions | >30 lines | Extract function |
| Deep nesting | >3 levels | Guard clauses, early returns |
| Duplicated blocks | >5 lines appearing 2+ times | Extract shared function |
| Large files | >500 lines, per [`rules/code-style.md`](../../rules/code-style.md) | Split by responsibility |
| God classes | >7 public methods | Split into focused classes |
| Long parameter lists | >4 parameters | Extract options object |
| Circular imports | Any cycle | Restructure module boundaries |
| Dead code | Unreachable branches, unused exports | Remove |
| Primitive obsession | Repeated string/number with domain meaning | Extract type or enum |
| Feature envy | Function using more of another module's data than its own | Move to the correct module |

### Phase 3: Rank and Present

Rank candidates by impact score: lines affected multiplied by complexity reduction. Present as a table:

| Priority | File | Line | Issue | Proposed refactoring | Impact |
|----------|------|------|-------|---------------------|--------|
| 1 | ... | ... | ... | ... | High |
| 2 | ... | ... | ... | ... | Medium |

If `--plan-only` was passed, stop here.

### Phase 4: Execute Incrementally

For each approved candidate, in priority order:

1. **Describe the change.** State what will change and what will stay the same.
2. **Predict the test outcome.** All existing tests must continue to pass with no modifications.
3. **Apply the refactoring.** One structural change at a time.
4. **Run tests.** If tests fail:
   - Revert the change.
   - Analyze why the refactoring broke tests. If the tests were testing implementation details rather than behavior, note this as a separate finding.
   - Try an alternative approach.
   - If the alternative also fails, skip this candidate and move to the next.
5. **Run formatter, linter, type checker, and build.** Fix any new warnings introduced by the refactoring before the commit.
6. **Commit.** One commit per refactoring step:
   - `refactor(scope): extract validateInput from processOrder`
   - `refactor(scope): flatten nested conditionals in AuthService`
   - `refactor(scope): remove duplicate price calculation`

### Phase 5: Final Verification

1. Run the formatter check. No changes.
2. Run the full test suite. All tests pass.
3. Run the linter. Zero warnings.
4. Run the type checker. Zero errors.
5. Run the build. Clean build.
6. Compare coverage. Coverage is equal to or higher than the baseline.
7. Review the full diff. Confirm no behavior changes leaked in.

## Rules

- Never change behavior. A refactoring that alters what the code does is a bug, not a refactoring.
- Never combine refactoring with feature work in the same commit. Structure changes and behavior changes are separate commits.
- Never modify test assertions during refactoring. If a test breaks, the refactoring changed behavior.
- One refactoring per commit. If a commit does two things, split it.
- Revert immediately when tests fail. Do not debug a failed refactoring for more than 5 minutes. Try a different approach or skip the candidate.
- Do not refactor code you do not understand. Read the function, its callers, and its tests before touching it.

## Common Rationalizations

- "The test only broke because it asserts an implementation detail, so updating the assertion is fine": assertions stay untouched. Revert, and report the brittle test as its own finding.
- "The off-by-one is right here, fixing it during the extraction is quicker": a behavior change goes in its own commit, apart from the structural one.
- "Two tiny refactorings fit in one commit": one refactoring per commit, so each step reverts alone.
- "The suite was already red before I started": the baseline stays green. Stop until the user fixes the failing tests.
- "The suite is green, so the refactoring is safe": green says nothing about lines no test reaches. Characterize them first, or stop.
- "Five more minutes of debugging will save this candidate": revert, try one alternative, and skip the candidate when that also fails.

## Red Flags

- Stop before any change when the Phase 1 test run fails.
- Stop and write characterization tests, or report the gap, when a candidate touches lines no test reaches.
- Stop and revert when a test fails after a step.
- Stop and read the function, its callers, and its tests when the next edit targets code you have not read.
- Stop and split the commit when its diff mixes a structural change with a behavior change.
- Stop at the Phase 3 table when `--plan-only` was passed.

## Verification

- The full test suite passes, and the diff touches no test assertion.
- The linter reports zero warnings, the type checker zero errors, and the build is clean.
- Coverage of the affected files is at or above the Phase 1 baseline.
- `git log` shows one `refactor(<scope>)` commit per applied candidate.
- Every skipped candidate is listed with the test failure that ruled it out.

## Related skills

- `/review` -- Review the refactoring diff before shipping.
- `/test` -- Run the test suite during verification.
- `/ship commit` -- Commit each refactoring step.
- `/investigate` -- Debug if a refactoring unexpectedly changes behavior.
