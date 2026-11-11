---
name: pair-capability-execute-manual-tests
description: "Executes a project's manual test suite against released artifacts, producing a structured report. Resolves test variables, iterates through critical paths, records PASS/FAIL per test case, and generates the report from the manual-test-report template. Invocable independently or composed by /pair-process-review (post-merge validation)."
version: 0.4.1
author: Foomakers
---

# /pair-capability-execute-manual-tests — Manual Test Suite Executor

Execute a manual test suite against released or deployed artifacts (website, CLI packages, registries). Produces a structured report following the [manual-test-report-template](../../../.pair/knowledge/guidelines/collaboration/templates/manual-test-report-template.md).

Reads test case files from the project's manual test suite directory. Each test case follows the format defined in [manual-test-case-template](../../../.pair/knowledge/guidelines/collaboration/templates/manual-test-case-template.md).

For the organizational context (who, when, which areas), see [manual-verification.md](../../../.pair/knowledge/guidelines/quality-assurance/manual-verification.md). For test case design principles, see [manual-testing.md](../../../.pair/knowledge/guidelines/quality-assurance/manual-testing.md).

## Arguments

| Argument | Required | Description |
| --- | --- | --- |
| `$suite` | No | Path to the test suite directory. Default: auto-detect `qa/` at project root. |
| `$version` | No | Version under test. If omitted, derived from the artifact (e.g. `pair-cli --version` or release tag). |
| `$base-url` | No | Production website URL. If omitted, derived from deployment config or adoption files. |
| `$scope` | No | Limit execution to specific critical paths: `CP1`, `CP2`, ..., `all` (default: `all`). Comma-separated for multiple. |
| `$priority` | No | Minimum priority to execute: `P0`, `P1`, `P2` (default: `P2` — run all). Set `P0` to run only blockers. |

## Algorithm

Execute in sequence. For every step, follow the **check → skip → act → verify** pattern.

### Step 1: Locate Test Suite

1. **Check**: Does `$suite` point to a directory containing test case files (`CP*.md`)?
2. **Skip**: If no suite found and no `$suite` argument → **HALT**: "No manual test suite found. Run `/pair-capability-design-manual-tests` to generate one from your project's artifacts, then re-invoke `/pair-capability-execute-manual-tests`."
3. **Check**: If `$suite` directory exists but contains zero `CP*.md` files → **HALT**: "Suite directory exists but contains no critical path files. Run `/pair-capability-design-manual-tests --output {$suite}` to populate it."
4. **Act**: Read the suite `README.md` for variable definitions and execution order. List all `CP*.md` files.
5. **Verify**: Suite loaded. Report: N critical paths found, N total test cases.

### Step 2: Resolve Variables

1. **Check**: Are all required variables resolvable (`$VERSION`, `$BASE_URL`, `$WORKDIR`, `$RELEASE_URL`, `$REGISTRY`)?
2. **Skip**: Variables already provided via arguments.
3. **Act**: For each unresolved variable:
   - `$VERSION`: extract from artifact (`--version` flag) or release tag.
   - `$BASE_URL`: read from deployment config, adoption files, or ask the user.
   - `$WORKDIR`: create isolated temp directory: `mktemp -d /tmp/manual-test.XXXXX`.
   - `$RELEASE_URL`: derive from `$VERSION` and repo URL.
   - `$REGISTRY`: read from adoption files or default.
   - **Additional variables**: resolve any extra variables declared in the suite `README.md` Variables table (e.g. auth tokens, config files). Follow the "How to resolve" column for each.
4. **Verify**: All variables resolved. Present to user for confirmation:

```text
VARIABLES RESOLVED:
├── VERSION:     [value]
├── BASE_URL:    [value]
├── WORKDIR:     [value]
├── RELEASE_URL: [value]
├── REGISTRY:    [value]
└── [additional]: [per suite README]
```

Ask: _"Proceed with these values?"_

### Step 3: Select Tool Strategy

1. **Check**: Which tools are available in the current environment?
2. **Act**: Build tool mapping based on availability:

| Action | Preferred Tool | Fallback |
| --- | --- | --- |
| Website page load + interaction | `agent-browser` skill | Playwright MCP (`browser_navigate`, `browser_snapshot`) |
| Bulk HTTP status checks | `WebFetch` or `curl -sI` via Bash | `agent-browser` (slower) |
| CLI command execution | Bash | — |
| File existence / content | Read tool or Bash `test -f` | — |
| Checksum verification | Bash `sha256sum` / `shasum -a 256` | — |
| Search UI interaction | `agent-browser` (fill form, click, screenshot) | Playwright MCP (`browser_press_key`, `browser_fill_form`) |
| Responsive viewport | `agent-browser` (resize, screenshot) | Playwright MCP (`browser_resize`, `browser_take_screenshot`) |
| Report generation | Write tool | — |

1. **Verify**: Tool strategy set. Tests requiring unavailable tools are pre-marked BLOCKED.

### Step 4: Execute Critical Paths

For each critical path file (in order: CP1, CP2, ..., CPN):

1. **Check**: Is this CP in `$scope`? Are there test cases at or above `$priority`?
2. **Skip**: If CP not in scope or all tests below priority threshold → skip entire CP.
3. **Act**: For each test case `MT-{CPNN}` in the file:
   a. **Check preconditions**: if a required precondition test failed → mark BLOCKED.
   b. **Execute steps**: run each step using the selected tool. Capture output/evidence. Follow any setup instructions in the test case (e.g. config files to copy, auth to configure).
   c. **Evaluate expected result**: compare actual vs expected. Determine PASS or FAIL.
   d. **Record result**: store test ID, status, evidence (command output, HTTP status, screenshot path).
4. **Verify**: All tests in CP executed or marked SKIP/BLOCKED. Log progress:

```text
CP{N} COMPLETE: [X pass | Y fail | Z skip | W blocked] of N total
```

### Step 5: Generate Report

1. **Check**: Is the [manual-test-report-template](../../../.pair/knowledge/guidelines/collaboration/templates/manual-test-report-template.md) available?
2. **Skip**: If not found → generate a minimal plain-text report.
3. **Act**: Fill the report template with:
   - Test suite name, version, date, tester (AI agent ID), environment details
   - Summary table (per CP: total, pass, fail, skip, blocked)
   - Overall result: PASS (all P0 pass, no Critical/Major failures) or FAIL
   - Failure details with evidence
   - Skipped/Blocked tests with reasons
4. **Verify**: Report written. Output path.

### Step 6: Store Report

1. **Act**: Write report to `.tmp/manual-test-reports/{suite-name}-{VERSION}-{YYYY-MM-DD}.md`.
   - Create directory if it doesn't exist.
   - If file already exists, append timestamp to filename to avoid overwrite.
2. **Verify**: File written. Report path.

### Step 7: Cleanup

1. **Act**: Remove `$WORKDIR` temp directory.
2. **Verify**: Cleaned up. Present final summary to user.

## Output Format

```text
MANUAL TEST EXECUTION:
├── Suite:    [{suite path}]
├── Version:  [{VERSION}]
├── Scope:    [{scope}]
├── Priority: [≥{priority}]
├── Results:
│   ├── CP1: [X/Y pass]
│   ├── CP2: [X/Y pass]
│   └── ...
├── Total:    [N pass | N fail | N skip | N blocked] of N
├── Result:   [PASS | FAIL]
└── Report:   [{report path}]
```

## Composition Interface

When composed by `/pair-process-review` (Phase 6, post-merge):

- **Input**: /pair-process-review invokes `/pair-capability-execute-manual-tests` after merge as optional post-release validation.
- **Output**: Returns the overall result (PASS/FAIL) and report path.
  - FAIL does NOT revert the merge — it creates an issue for the findings.
  - Results are appended to the review report as an addendum.
- **Scope**: /pair-process-review passes `$scope = P0` (blockers only) for fast post-merge validation. Full suite runs standalone.

When composed by `/pair-capability-verify-done` (Step 5.5, optional):

- **Input**: /pair-capability-verify-done checks if a manual test report exists for the current version with PASS result.
- **Output**: Returns PASS (report exists and passing) or SKIPPED (no suite or no report).
- **Note**: /pair-capability-verify-done does NOT invoke /pair-capability-execute-manual-tests — it only checks for an existing report.

When invoked **independently**:

- Run all CPs (or scoped CPs) at full priority.
- Generate and store the report.
- Present summary to user.

## Determinism Strategies

To maximize reliability when executed by AI agents:

- **Never rely on timing**: use explicit waits (Playwright `waitUntil: networkidle`), not `sleep`.
- **Assert on stable selectors**: use text content, `data-testid`, semantic HTML — not CSS classes.
- **Checksum comparison**: always compute and compare — never hardcode expected hashes.
- **Version from artifact**: extract from the artifact itself, never from source code.
- **Isolated filesystem**: `$WORKDIR` must be outside the repo to avoid workspace interference.
- **Clean npm environment**: use `--no-workspaces`, ensure no `.npmrc` inheritance from parent dirs.
- **Idempotent re-run**: re-executing produces the same result without manual cleanup.

## Graceful Degradation

- **No test suite found**: HALT with guidance to run `/pair-capability-design-manual-tests` first.
- **`agent-browser` not available**: Fall back to Playwright MCP. If Playwright MCP also unavailable, fall back to WebFetch/curl for HTTP checks. Mark interactive tests (search, responsive) as BLOCKED.
- **No internet**: Skip tests requiring network (website, registry, auto-download). Mark as BLOCKED with reason.
- **Suite-specific variable not resolvable**: Mark dependent tests as BLOCKED with the resolution hint from the suite README.
- **$VERSION not resolvable**: Ask user to provide explicitly.
- **Report template not found**: Generate minimal plain-text report.
- **Partial failure**: Complete all CPs even if some fail. Never abort early on FAIL.

## Notes

- This skill **executes tests and writes reports** — it does not modify application code.
- Test execution order follows CP numbering. Within a CP, tests execute in document order.
- The `$WORKDIR` is created once and shared across all CPs, then cleaned up at the end.
- Evidence (command output, screenshots) is captured inline in the report, not as separate files.
- This capability is designed to evolve into a standalone skill that AI agents invoke autonomously after each release.
