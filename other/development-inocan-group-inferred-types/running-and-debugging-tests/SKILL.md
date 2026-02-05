---
name: Running and Debugging Tests
description: Executes language-agnostic test suites to validate behavioral correctness, enforce regression safety, and automatically debug or repair test failures. Includes fallback loops, coverage validation, and failure classification to maximize suite reliability. Use to validate code changes proactively, or when the user mentions running tests, test failures, or test debugging.
---

# Running and Debugging Tests

Execute and automatically debug test suites to validate behavioral correctness.

## What you should do

**CRITICAL TEST INTEGRITY**: This workflow NEVER bypasses test failures to achieve user goals. Tests exist to improve code quality and prevent regressions—they are not obstacles to be removed when inconvenient. Only fix tests when intended behavior changes, never to accommodate bugs.

1. **Gather test configuration** – Determine the test command (e.g., `npm test`, `pytest`, `go test`, `dotnet test`) and locate the test directories or files. Optionally identify tooling for coverage (e.g., NYC, `pytest --cov`, `go test -cover`).

2. **Execute test suite** – Run the full test suite in quiet or minimal output mode. Capture the results for parsing.

   ```bash
   [test-runner-command] [optional flags]
   ```

   *Example:* `npm test --silent`, `pytest -q`, `go test ./... -v`, `dotnet test --nologo`

3. **Evaluate test results** –

   * ✅ If **all tests pass**, proceed to Step 4.
   * ❌ If **any tests fail**, proceed directly to Step 5.

4. **Verify test quality and behavior coverage** – Focus on whether tests validate meaningful behavior rather than achieving coverage percentages.

   ```bash
   [coverage-command]  # Optional for information only
   ```

    *Example:* `npx nyc --reporter=text npm test`, `pytest --cov=src --cov-report=term-missing`, `go test -coverprofile=coverage.out`

   * **Quality indicators to check:**
     - Tests use behavioral names (`test_should_X_when_Y`, `test_rejects_X_when_Y`)
     - Tests verify outcomes, not implementation details
     - Error paths and edge cases are tested
     - Mocking is minimal and strategic (external dependencies only)
   * If behavior coverage is insufficient, create new tests that validate actual user-facing functionality.

5. **Diagnose test failures** – Parse the output logs to identify failing test cases. Extract:

   * Test name or function
   * Source file and line
   * Error message and exception type
   * Stack trace or diff output

5a. **Parallel resolution option** – For multiple test failures (3+ failures), consider spawning parallel resolution agents:

   * Assign each agent a specific test failure to resolve in isolation
   * Maximum parallelization: one agent per failing test (up to system limits)
   * Agents work independently on different files/functions to avoid conflicts
   * Monitor completion and merge fixes before proceeding to step 11
   * **Fallback**: If parallel execution is not available, proceed sequentially with steps 6-10

6. **Retry on failure** – If the test suite fails, rerun with `-v` for verbose output. Log the result to `logs/test-failure.log`.

7. **Re-run failing test in isolation** – Execute each failing test individually to isolate behavior.

   ```bash
   [test-runner] path/to/file [test-selector]
   ```

   *Example:* `npm test -- test/file.test.js -t "should render correctly"`, `pytest path/to/test_file.py::test_name -q`, `go test -run TestFunctionName`, `dotnet test --filter "TestName"`

8. **Classify failure cause** –

   * ✅ If failure is due to **stale test logic** (e.g., broken mocks, outdated assertions), proceed to Step 8a.
   * ❌ If caused by **source implementation bug**, proceed to Step 8b.

9. **Apply fix based on classification**

   * **8a. Update invalid test** – Modify test code: adjust mocks, inputs, or expected outputs to match intended behavior. Ensure proper tagging and descriptive assertions.
   * **8b. Patch code defect** – Identify root cause and apply a minimal fix to the implementation. Maintain logic intent and regression safety.

10. **Verify individual fix** – Re-run the isolated test.

   ```bash
   [test-runner] path/to/file [test-selector]
   ```

* If the test fails again, loop back to Step 6.
* If it passes, proceed to Step 11.

11. **Re-run full test suite** – Ensure all tests pass and no regressions were introduced.

    ```bash
    [test-runner-command]
    ```

    * If new failures occur, repeat Steps 5–10 for each.

12. **Finalize and commit changes** – Once the suite passes and coverage is adequate:

    * Commit with message: `"Fix test failures and verify coverage compliance"`
    * Optionally run or validate the CI/CD pipeline.
    * Recommend tagging a patch release if this resolves a bug cycle.

## Language-Specific Guidance

- Python (PyTest):
  - Full suite: `pytest -q`
  - Coverage: `pytest --cov=src --cov-report=term-missing`
  - Markers by domain: `pytest -m unit`, `pytest -m feature`
  - Isolate a test: `pytest path/to/test_file.py::test_name -q`
  - Verbose retry: `pytest -v`

## Test quality standards

**Behavioral focus**: Write tests with descriptive names like `test_should_X_when_Y` that verify observable behavior, not implementation details.

**Strategic mocking**: Mock external dependencies only (databases, APIs, file systems) with maximum 5 mocks per test and 3:1 mock-to-assertion ratio.

**Quality over coverage**: Focus on meaningful tests that would fail if functionality broke, avoid vanity tests written solely for coverage metrics.

**Failure resolution**: Address root causes systematically. For multiple failures, resolve in parallel when possible to maximize development velocity.