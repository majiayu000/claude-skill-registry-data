---
name: debug
description: Debug and fix failing tests or errors
argument-hint: "<test-name|error-description|stack-trace>"
---

# Debug and Fix

Systematically debug and fix failing tests, build errors, or runtime issues using aggressive parallelization at every phase.

**DO NOT STOP UNTIL THE ISSUE IS FIXED AND TESTS PASS.**

## Arguments

- `$ARGUMENTS` - Test name, error message, or description of the issue

## Phase 1: Reproduce and Gather Context

### 1.1 Detect the Stack

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

Commands in this skill name a column of this table, for example "the stack's Test one command". Give every agent the detected stack's commands.

### 1.2 Gather Context in Parallel

Launch **three parallel agents** simultaneously to maximize information gathering speed.

**Agent 1 - Reproduce the failure:**

- Test failure: run the failing test (`$ARGUMENTS`) with the stack's Verbose single test command from Debug Techniques, or the Test all command to find every failure.
- Build error: run the stack's Build command and capture the complete error output, with stack traces enabled.
- Runtime error: get the full stack trace and identify the failing component.

Capture all error details: full error message, stack trace, test name and class, file and line number, input that caused the failure.

**Agent 2 - Check recent changes:**

```bash
git diff HEAD~5 --name-only
git diff HEAD~5 -- <relevant paths>
```

Identify what files changed recently that could be related to the failure. Summarize which changes are most likely to have introduced the bug.

**Agent 3 - Check git history:**

```bash
git log --oneline -15
git log --oneline -5 -- <files related to $ARGUMENTS>
```

Determine if this is a regression by finding when the relevant code last changed and who changed it.

**Wait for all three agents to complete.** Synthesize their findings to determine:
- Is this a single test failure or multiple?
- Is it flaky (intermittent)?
- Is it a regression (worked before)?
- What is the scope of the problem?

## Phase 2: Root Cause Analysis

Using the error details from Phase 1, launch **three parallel agents** to analyze all relevant code simultaneously.

**Agent 1 - Analyze the failing test** (use `Explore` or read directly):

Read and understand the failing test file completely. Document:
- What the test expects
- What setup and mocks it uses
- What assertions are failing and why
- Whether the test itself is correct or buggy

**Agent 2 - Analyze the code under test** (use `Explore` or read directly):

Read the production code that the test exercises. Document:
- The relevant function or method signatures
- The control flow path that leads to the failure
- Any recent changes to this code (cross-reference with Phase 1 Agent 2 results)
- Potential bugs: null references, wrong logic, missing error handling, race conditions

**Agent 3 - Analyze related dependencies** (use `Explore` or read directly):

Read related files: interfaces, shared utilities, configuration, DI modules, database schemas, or mocks that the code under test depends on. Document:
- Whether any dependencies changed recently
- Whether mocks match current interfaces
- Whether configuration or DI wiring is correct
- Whether database state assumptions still hold

**Wait for all three agents to complete.** Synthesize their findings into a root cause hypothesis:
- What is wrong
- Why it causes this specific error
- What the minimal fix should be

## Phase 3: Fix and Verify

### 3.1 Implement Fix

Use **architect** to implement the fix:
- Fix the root cause, not symptoms
- Make the minimal targeted change
- Preserve existing behavior for passing cases
- Do not change unrelated code

### 3.2 Parallel Verification

After implementing the fix, launch **two parallel agents** to verify simultaneously.

**Agent 1 - Run the specific failing test:**

Run the stack's Test one command for the failing test. Confirm the original failure is resolved. If it still fails, report the new error details.

**Agent 2 - Run related tests:**

Run the stack's Class, file or module command from Debug Techniques for the code the fix touched. Confirm no closely related tests have broken as a side effect of the fix.

**Wait for both agents to complete.** If either agent reports a failure, return to Phase 2 with the new information and repeat. Do not proceed until both pass.

## Phase 4: Full Validation

Launch **two parallel agents** for final validation.

**Agent 1 - Code review** (use **reviewer**):

Review the fix for:
- Correctness: is this the right fix for the root cause?
- Edge cases: does it handle all boundary conditions?
- Side effects: could it cause other issues?
- Quality: does it follow project conventions and naming standards?

If the review finds issues, fix them before proceeding.

**Agent 2 - Full test suite:**

Run the stack's Test all and Build commands to catch any regressions anywhere in the codebase.

**Wait for both agents to complete.** If the full suite has failures, fix every one of them (there are no "pre-existing" failures). If the code review raised issues, address them and re-run verification.

### 4.1 Add Test Coverage

If the bug was not caught by existing tests:
- Add a test for this specific case
- Add tests for related edge cases
- Ensure this bug cannot recur

Run the new tests with the stack's Test one command to confirm they pass.

### 4.2 Commit Fix

Delegate to the `skills:commit` command:

```
Skill(skill="skills:commit", args="fix(<scope>): [description of what was fixed]")
```

## Debug Techniques

Each stack's form for one test with its full output, for a whole class, file or module, and for rerunning a flaky test without a cached result:

| Stack | Verbose single test | Class, file or module | Flaky rerun |
|---|---|---|---|
| Gradle | `./gradlew test --tests "*Name*" --info` | `./gradlew :module:test --tests "com.example.NameTest"` | `./gradlew cleanTest test --tests "*Name*"` |
| Maven | `mvn test -Dtest=Name -DtrimStackTrace=false` | `mvn test -pl module -Dtest=NameTest` | `mvn test -Dtest=Name` |
| PHP | `composer test -- --filter Name` | `composer test -- tests/Path/NameTest.php` | `composer test -- --filter Name` |
| Node | `<pm> test -- -t "Name"` | `<pm> test -- path/to/name.test.ts` | `<pm> test -- -t "Name"` |
| Rust | `RUST_BACKTRACE=1 cargo test name -- --nocapture` | `cargo test -p crate module::` | `cargo test name` |
| Go | `go test -run Name -v ./...` | `go test -v ./path/to/package` | `go test -run Name -count=1 ./...` |
| Python | `pytest -k name -vv -l` | `pytest tests/test_name.py::TestName` | `pytest -k name` |

### For Test Failures

Run the failing test alone with the stack's Verbose single test command, then widen to its class, file or module.

### For Null Pointer / Missing Data
- Check test setup and mocks
- Verify DI is configured correctly
- Check database state for integration tests

### For Async / Timing Issues
- Check the lifetimes and cancellation of coroutines, tasks and promises
- Look for race conditions
- Verify test uses proper async testing utilities

### For Flaky Tests

Run the stack's Flaky rerun command ten times and stop at the first failure:

```bash
for run in $(seq 1 10); do <flaky rerun command> || { echo "Failed on run $run"; break; }; done
```

## Test Failure Policy

**IMPORTANT:** There is no such thing as a "pre-existing" test failure. If any test fails, whether it appears related to your changes or not, you must fix it. The task always completes with completely passing tests.

## Completion Criteria

- [ ] Root cause identified
- [ ] Fix implemented
- [ ] Original failing test passes
- [ ] ALL tests pass (no exceptions for "pre-existing" failures)
- [ ] No regressions introduced
- [ ] Fix reviewed via reviewer
- [ ] Committed with clear message
