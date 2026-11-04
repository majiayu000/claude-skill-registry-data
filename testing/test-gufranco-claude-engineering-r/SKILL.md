---
name: test
description: Run tests, load benchmarks, coverage analysis, linting, and security scanning. Includes HTTP load testing with k6/wrk/hey/ab. Use when user says "run tests", "check coverage", "lint", "benchmark", "load test", "perf test", or wants to execute the project's test suite with results. For QA analysis of test gaps, use /review qa; for security auditing, use /audit; for writing test scenarios during planning, use /plan.
argument-hint: "/test [run|coverage|lint|perf] [target]"
allowed-tools: "Read, Bash, Grep, Glob, Write"
---

## Overview

Unified testing skill covering test execution, load testing, coverage, linting, and scanning.

## When to Use

- The user says "run tests", "check coverage", "lint", "benchmark", "load test", or "perf test".
- A change needs fresh suite, lint, or coverage output as completion evidence.
- An endpoint needs throughput and latency numbers under load.
- A test fails intermittently and needs a flake rate.

For QA analysis of test gaps, use `/review qa`; for a full security audit, use `/audit`; for a single test-first cycle, use `/tdd`.

## Process

Pick the row that matches the invocation, then follow that subcommand's section below.

| Invocation | Action |
|-----------|--------|
| `/test` | Run the full test suite (default) |
| `/test <path>` | Run tests matching a file or pattern |
| `/test --coverage` | Run with coverage reporting |
| `/test --watch` | Run in watch mode |
| `/test lint` | Run linters |
| `/test scan` | Security vulnerability scanning |
| `/test ci` | Simulate CI locally with `act` |
| `/test perf <url>` | Load test an HTTP endpoint |
| `/test stubs <path>` | Generate test stubs for uncovered code |
| `/test flaky` | Detect flaky tests by running the suite multiple times |

---

## Test Execution (default)

### Package Manager Detection

`bun.lock`/`bun.lockb` = bun, `pnpm-lock.yaml` = pnpm, `yarn.lock` = yarn, `package-lock.json` = npm, which is converted to pnpm with `pnpm import` before running anything, `Cargo.toml` = cargo, `go.mod` = go, `pyproject.toml` with `uv.lock` = uv, `pyproject.toml` with `[tool.poetry]` = poetry, `pyproject.toml`/`requirements.txt` = pip. Also check `Makefile`/`Justfile` for test targets.

### Test Runner Detection

- Node.js: `vitest.config.*` or vitest in devDeps, `jest.config.*` or jest in devDeps, `mocha` in devDeps.
- Rust: `cargo test`. Go: `go test ./...`. Python: look for [`pytest.ini`](../../pytest.ini), `pyproject.toml` with `[tool.pytest]`.
- Shell: check for `shellcheck`.

### Steps

1. Detect package manager and test runner.
2. Build command: base command + path/pattern + `--coverage` or `--watch` flags.
3. Run and capture output.
4. Parse: passed, failed, skipped counts. Coverage summary if requested.
5. Present: pass count, failures with error messages and file locations, coverage if applicable.

---

## lint

Run linters based on project configuration.

- Node.js: `package.json` lint script.
- Go: `golangci-lint run`.
- Shell: `shellcheck` on `.sh`/`.zsh` files.
- Python: `ruff check .` or `flake8`.
- GitHub Actions: `actionlint` on workflow files.

---

## scan

Deep security scanning with available tools.

- `trivy fs .` for dependency + config vulnerabilities.
- `snyk test` + `snyk code test`.
- `gitleaks detect --source .` for leaked secrets.

Report results from whichever tools are installed. List missing tools if none available.

---

## ci

Simulate CI locally with `act`.

1. Verify `act` installed.
2. `act --list` to show workflows.
3. Run selected workflow with `act push --container-architecture linux/amd64`.

---

## perf

Load test HTTP endpoints. Auto-detects the best available tool.

### Arguments

- A URL is required: endpoint to test.
- `-n <requests>`: total requests (default: 1000).
- `-c <concurrency>`: concurrent connections (default: 10).
- `-d <duration>`: test duration (e.g. `30s`). Overrides `-n`.
- `--method <METHOD>`: HTTP method (default: GET).
- `--body <json>`: request body.
- `--header <key:value>`: custom header, repeatable.
- `--compare`: run twice with a pause for changes between runs.
- `--script <path>`: custom k6 script.

### Steps

1. Parse arguments. Validate target with a single request.
2. Detect tool, preference order: k6, wrk, hey, ab.
3. Build command:
   - **k6**: generate temp script with VUs, duration/iterations, headers, body. Run with `--summary-trend-stats`.
   - **wrk**: `wrk -t<threads> -c<concurrency> -d<duration> <url>`. Lua script for POST.
   - **hey**: `hey -n <n> -c <c> -m <method> <url>`.
   - **ab**: `ab -n <n> -c <c> <url>`. Temp file for POST body.
4. Run and extract metrics:

| Metric | Description |
|--------|-------------|
| Total requests | Completed |
| Failed requests | Non-2xx or connection errors |
| Requests/sec | Throughput |
| Latency avg | Mean response time |
| Latency p50 | Median |
| Latency p95 | 95th percentile |
| Latency p99 | 99th percentile |
| Transfer rate | Data throughput |

1. Flag: p99 > 1s, error rate > 1%.
2. **Compare mode**: run once, wait for user signal, run again. Side-by-side comparison with percentage changes.
3. Clean up temp files.

---

## flaky

Detect flaky tests by running the full suite multiple times and tracking which tests have inconsistent results.

### Steps

1. Detect the test runner and build the test command with no watch mode.
2. Run the suite 5 times in sequence, capturing pass/fail status for each test.
3. Track per-test consistency: a test is flaky if it fails in at least 1 run and passes in at least 1 run.
4. Rank by flake rate. Every flaky test is fixed or deleted in this change, per [`rules/testing.md`](../../rules/testing.md); the rate only orders the work, highest first. A skip, a quarantine, or a later pass is never the outcome.
5. Report results:

```
## Flaky Test Report: <date>

### Summary
- Suite runs: 5
- Total tests: <N>
- Consistently passing: <N>
- Flaky (inconsistent): <N>
- Consistently failing: <N>

### Flaky Tests

| Test | Fail Rate | Category | Root Cause Hint |
|------|----------|---------|-----------------|
| <test name> | 2/5 = 40% | fix | timing dependency suspected |

### Fix or Delete

Each flaky test with its proposed action: a fix for the named root cause, or deletion when the test asserts nothing a user would notice. Never `.skip` or `xit`.
```

1. For each flaky test, suggest likely root causes: shared mutable state, hardcoded ports, timing, unseeded random, missing database cleanup.

### Rules

- Never run this against production endpoints.
- If the test suite takes more than 60 seconds per run, reduce to 3 runs and note the limitation.
- Do not apply a fix or a deletion automatically. Present the list and wait for approval.

---

## stubs

Generate test file stubs for code that lacks tests.

### Steps

1. Read the target file(s).
2. Identify all exported functions, classes, and methods.
3. Check for existing test files. Skip already-tested exports.
4. Generate a test stub per untested export following project conventions:
   - Read existing test files in the same module for patterns.
   - Follow [`rules/testing.md`](../../rules/testing.md): three blocks opened by the bare `Arrange`, `Act`, `Assert` markers and no other comment, faker for data, real database.
   - Include one happy-path test and one error-path test. Edge cases are listed in the approval message, never as a marker comment in the file.
5. Present stubs for approval before writing.
6. After writing, run the test suite. Every stub carries a real assertion whose expected value comes from the spec or a worked example, never a `TODO` placeholder. A stub whose expected value is unknown is not written; it goes in the approval message as a question.

---

## Rules

- Always detect package manager and test runner from project config.
- Never install test dependencies without asking.
- Never modify test files during test execution, only `stubs` generates files.
- Never run perf tests against production URLs without explicit confirmation.
- Always validate perf target is reachable before load testing.
- Always clean up temporary files.
- Default perf to safe values, 1000 requests, 10 concurrency.
- Show exact commands so user can reproduce manually.
- If no test config exists, say so and stop.

## Common Rationalizations

- "The last run passed, so report it": evidence comes from a run in this session. Rerun and read the exit code.
- "Reading the last lines of output is enough": a summary line can hide one failure above it. Gate on the exit code, then grep for `passed|failed`.
- "One flaky failure is noise, rerun until green": a test that fails once in five runs is flaky by the definition in `flaky`. Report it with its rate.
- "The URL looks like staging": a hostname proves nothing. Treat a URL you cannot classify as production and ask before the perf run.

## Red Flags

- Stop and say no test configuration exists when detection finds no runner.
- Stop and ask before installing a missing test dependency or tool.
- Stop and confirm the target when a perf URL resolves to a production host.
- Stop and present the fix-or-delete list for approval before any flaky test changes, and never add `.skip` or `xit`.

## Verification

- The exact command that ran is shown, so the user can rerun it.
- The reported pass, fail, and skip counts match the runner's own summary, and the exit code is stated.
- Warnings and deprecations in the output are listed, or the report says there were none.
- Perf runs report every metric in the table, and temp scripts and payload files are deleted.

## Related skills

- `/ship` -- Commit after tests pass.
- `/review qa` -- QA analysis for coverage gaps.
- `/audit scan` -- Security vulnerability scanning.
