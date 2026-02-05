---
name: fix-test-case
description: Fix a specific failing test case in this repo by identifying the root cause, adding a minimal repro under tests/, explaining the cause, applying a targeted fix, re-running the test, and reporting any new failures uncovered.
---

# Fix a failing test case

## Scope

- Work on one concrete failing test at a time.
- Keep the repro small and isolated under tests/.
- Do not try to fix failures that are due to changing the source layout; add them to `EXPECTED_FAILURE.md` instead.
- If a failure is due to shifting line numbers or changed source content (literal tracebacks, linecache, etc.), add it to `EXPECTED_FAILURE.md`.

## Workflow

1. Reproduce the failure
   - Re-run the failing test directly (use the narrowest command possible, e.g. `uvx pytest tests/test_file.py -k "test_name"`).
   - Capture the exact error, traceback, and any assertion mismatch.

2. Identify the root cause
   - Inspect the failing code path and surrounding logic.
   - Map the failure back to the minimal incorrect behavior (state mismatch, wrong transform, missing edge case).
   - If needed, use the `python-debug` skill for pdb stepping or the `python-monitoring-trace` skill for a sys.monitoring trace.

3. *Always* add a minimal repro under tests/
   - Create a new test file or extend the most relevant existing test file.
   - Keep the input as small as possible while still reproducing the failure.
   - Prefer integration-style tests consistent with existing tests/ conventions.

4. Explain the cause
   - Summarize the bug in one or two sentences.
   - Point to the relevant code path and why it misbehaves.

5. Implement the fix
   - Apply the smallest change that makes the repro pass.
   - Avoid unrelated refactors or behavior changes.
   - Never change the cpython source to fix a test.
   - The goal is to transform python to a minimal form, so do not selectively disable that to fix the tests.

6. Re-run the test
   - Re-run the specific failing test and the new repro.
   - If it uncovers additional failures, summarize them and continue iterating.

7. Final verification
   - Run the full required test commands (`cargo test` and `uvx pytest tests/`).

## Output expectations

- Provide a short cause explanation and the fix rationale.
- List the exact tests re-run and the results.
- If more failures appear, list them with a brief classification (ERROR/FAIL/TIMEOUT/CRASHED).
