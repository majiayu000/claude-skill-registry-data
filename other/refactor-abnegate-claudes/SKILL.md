---
name: refactor
description: Safe refactoring with comprehensive test coverage
argument-hint: "<what-to-refactor>"
---

# Safe Refactoring

Refactor code safely with tests as a safety net.

**RULE: All tests must pass before AND after. No behavior changes.**

## Arguments

- `$ARGUMENTS` - What to refactor (file, module, pattern, etc.)

## Phase 0: Preparation

### 0.1 Detect the Stack

Detect the stack from the first manifest in this table's row order that exists at the repository root. `<pm>` is the package manager chosen by lockfile, as in the `skills:build` skill. Prefer the project's own scripts or Makefile targets when they exist. When tests run in Docker Compose (Appwrite), run the same command inside the service, for example `docker compose exec <service> vendor/bin/phpunit --filter Name`.

| Manifest | Stack | Test all | Test one | Build | Lint | Format | Static analysis | Coverage |
|---|---|---|---|---|---|---|---|---|
| build.gradle.kts / build.gradle | Gradle | `./gradlew test` | `./gradlew test --tests "*Name*"` | `./gradlew build` | `./gradlew spotlessCheck` (or `ktlintCheck`) | `./gradlew spotlessApply` (or `ktlintFormat`) | `./gradlew detekt` | `./gradlew koverReport` |
| pom.xml | Maven | `mvn test` | `mvn test -Dtest=Name` | `mvn package` | configured plugin | `mvn spotless:apply` if configured | — | `mvn jacoco:report` if configured |
| composer.json | PHP | `composer test` | `composer test -- --filter Name` | `composer install` | `composer lint` | `composer format` | `composer check` (PHPStan) | `vendor/bin/phpunit --coverage-text` (PCOV/Xdebug) |
| package.json | Node | `<pm> test` | `<pm> test -- -t "Name"` | `<pm> run build` | `<pm> run lint` | `<pm> run format` / `npx prettier --write .` | `<pm> exec tsc --noEmit` | `<pm> test -- --coverage` |
| Cargo.toml | Rust | `cargo test` | `cargo test name` | `cargo build` | `cargo clippy -- -D warnings` | `cargo fmt` | `cargo clippy -- -D warnings` | `cargo llvm-cov` if installed |
| go.mod | Go | `go test ./...` | `go test -run Name ./...` | `go build ./...` | `go vet ./...` | `gofmt -w .` | `golangci-lint run` if configured | `go test -cover ./...` |
| pyproject.toml / setup.py | Python | `pytest` | `pytest -k name` | `pip install -e .` | `ruff check .` | `ruff format .` | `mypy .` if configured | `pytest --cov` |

Commands in this skill name a column of this table. In the agent prompts below, replace a placeholder such as `<Test all command>` with the detected stack's command from that column.

### 0.2 Parallel Discovery

Launch **three agents in parallel** to gather all baseline information simultaneously:

**Agent A: Coverage Report**
```
Task: Generate the test coverage report for the affected area.
Run `<Coverage command>` and read the coverage output.
Report the coverage percentage for every file in the refactoring scope.
Flag any file below 80% coverage.
If the project has no coverage tool set up, report that instead of a percentage.
```

**Agent B: Baseline Tests**
```
Task: Run the full test suite and report results.
Run `<Test all command>`.
Report pass/fail counts and list any failures with their full stack traces.
```

**Agent C: Scope Analysis**
```
Task: Analyze the refactoring scope for `$ARGUMENTS`.
Determine what is being refactored: single file, multiple related files, entire module, or cross-cutting pattern.
Identify and list:
- Every public API surface (public functions, classes, interfaces, data types)
- Expected inputs and outputs for each public entry point
- Edge cases and error paths
- Integration points with other modules
- All direct dependents (files that import or reference the target)
Return the findings in your report.
```

**Wait for all three agents to complete before continuing.**

### 0.3 Evaluate Results

Review the outputs from all three agents:
- If Agent B reported test failures: **STOP. Fix failures before proceeding.**
- If Agent A reported coverage below 80% for any file in scope, or no coverage tool: proceed to Phase 1.
- If coverage is adequate (>=80%): skip Phase 1, proceed to Phase 2.

## Phase 1: Add Missing Tests

### 1.1 Parallel Gap Analysis

Launch **parallel agents per dimension** to identify every untested path. Create one agent per category:

**Agent: Branch Coverage**
```
Task: Analyze the coverage report (if Phase 0 produced one) and source code for `$ARGUMENTS`.
List every uncovered branch (if/else, switch/match, try/catch) with file path and line numbers.
For each uncovered branch, write a one-line description of what condition triggers it.
```

**Agent: Edge Cases**
```
Task: Analyze the source code for `$ARGUMENTS`.
List every edge case that lacks a test: null inputs, empty collections, boundary values,
overflow conditions, concurrent access, and type coercion scenarios.
For each, specify the function and the exact edge condition.
```

**Agent: Error Paths**
```
Task: Analyze the source code for `$ARGUMENTS`.
List every error/exception path that lacks a test: thrown exceptions, error returns,
fallback branches, retry logic, timeout handling, and resource cleanup paths.
For each, specify the function, the error condition, and expected behavior.
```

**Wait for all agents to complete.** Merge their findings into a single prioritized list.

### 1.2 Write Characterization Tests

Tests that capture CURRENT behavior (even if it seems wrong):
- Test what the code DOES, not what it SHOULD do
- These tests lock in behavior during refactoring
- Work through the merged list from 1.1, highest-priority gaps first

Run the stack's Test all command to verify the new tests pass.

**STOP IF TESTS FAIL.** Fix tests until green.

## Phase 2: Plan Refactoring

Launch a **planner** agent (`subagent_type: "planner"`) with the scope analysis from Phase 0 and the refactoring request. The planner will:
- Rank refactoring goals by impact (readability, performance, maintainability, duplication, abstractions)
- Identify which standard refactoring patterns apply with exact file/line locations
- Break the refactoring into small, safe steps — each independently committable and test-green
- Identify which steps are independent (can run in parallel worktrees) vs sequential
- Order renames and moves before structural changes

Then launch a **verifier** agent (`subagent_type: "verifier"`) to validate the plan. Iterate until APPROVED.

## Phase 3: Execute Refactoring

Commit any characterization tests from Phase 1 first (`skills:commit` with `test(<scope>): …`), because uncommitted work is not part of BASE. Then record BASE: the SHA `git rev-parse HEAD` prints in this checkout. Give each independent step's `architect` agent the checkout's absolute path as the repo, BASE, its own branch and an absolute worktree path (explicit worktree mode: the architect follows its Worktree BASE protocol). Prompt the consolidator with this checkout as the integration worktree, BASE, and merge as the integration mode.

**Independent steps** (touching different files with no dependency): launch ALL simultaneously as **architect** agents, each in its own worktree, then merge via the **consolidator**.

**Sequential steps** (each depends on the previous): execute one at a time:

For each step:

### 3.1 Make One Change

Single, focused change:
- Rename
- Extract method/class
- Move code
- Simplify logic
- Remove duplication

### 3.2 Run Tests

Run the stack's Test all command.

**STOP IF TESTS FAIL.** Fix or revert before continuing.

### 3.3 Commit

Delegate to the `skills:commit` command:

```
Skill(skill="skills:commit", args="refactor(<scope>): [specific change made]")
```

### 3.4 Repeat

Continue with next step until refactoring complete.

## Phase 4: Review

Launch a **reviewer** agent (`subagent_type: "reviewer"`) to review the full diff (`git diff <BASE>...HEAD`, with the BASE SHA recorded at the start of Phase 3). Focus: behavior preservation, no accidental API changes, code quality improvement. Fix any critical/major issues found.

## Phase 5: Final Verification

Launch a **verifier** agent (`subagent_type: "verifier"`) in post-verification mode with the stack's Test all, Lint and Build commands. It confirms: tests pass (count not decreased from baseline), lint clean, build succeeds, no behavior changes, all public APIs preserved.

## Common Refactoring Patterns

### Extract Method
```kotlin
// Before
fun process() {
    // 20 lines of validation
    // 20 lines of processing
}

// After
fun process() {
    validate()
    doProcessing()
}
```

### Extract Class
When a class has too many responsibilities.

### Rename for Clarity
When names don't reflect purpose.

### Remove Duplication
Extract shared logic into the domain that owns it — no helper/utility files.

### Simplify Conditionals
Replace complex if/else with switch/match expressions, early returns, or polymorphism.

### Replace Magic Values
Extract constants with meaningful names.

## Completion Criteria

- [ ] Adequate test coverage before starting
- [ ] All tests pass after each step
- [ ] Refactoring improves code quality
- [ ] No behavior changes
- [ ] Code reviewed
- [ ] Final tests pass
- [ ] Committed with clear messages
