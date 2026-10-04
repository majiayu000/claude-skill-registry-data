---
name: run-tests
description: Run the pytest suite, report pass/fail counts and coverage, and identify untested code. Use when the user asks to run tests, check test coverage, or verify that changes didn't break anything.
allowed-tools: Bash, Read, Glob, Grep
---

# Run Tests

Run the project's test suite and report results honestly, including failures.

## Steps

1. Determine scope from the request:
   - A specific file was mentioned → run just that file
   - "the tests" or no scope → the whole suite
   - "coverage" mentioned → include the coverage flags in step 3

2. Verify pytest is available:

   ```bash
   python -m pytest --version
   ```

   If missing, tell the user to run `pip install pytest pytest-cov` and stop.

3. Run:

   ```bash
   python -m pytest <scope> -v --tb=short
   ```

   With coverage:

   ```bash
   python -m pytest <scope> --cov=src --cov-report=term-missing --cov-report=json
   ```

   For a threshold summary, run `coverage_summary.py` from this skill directory against the generated `coverage.json`.

4. Report:
   - Pass / fail / skip counts, separately
   - For each failure: the test name, the assertion that failed, the file and line
   - Coverage percentage and which files fall below 80%, if coverage was run

5. If tests failed, do not fix them unless asked. Report first — the user may want to see the failure before it disappears.

## Interpreting failures

Read the actual assertion before theorising. Common patterns, in rough order of frequency:

- **Import errors** — a dependency is missing, or the package isn't installed in editable mode. Check that before assuming the test is wrong.
- **Fixture errors** — the fixture is out of scope or missing from `conftest.py`.
- **Assertion failures** — a genuine behavioural difference. Report expected and actual verbatim; do not summarize them.
- **Collection errors** — a syntax error in the test file. Not a test failure at all.

## Constraints

- Never modify a test to make it pass. If a test looks wrong, say so and explain why, then let the user decide.
- Never report success when tests were skipped. Skipped is not passed. Report the skip count separately and say why they skipped.
- Run the full suite before calling a change safe. A passing subset proves nothing about the rest.
