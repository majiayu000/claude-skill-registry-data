---
name: verify-test-quality
description: Apply five concrete heuristics to detect tautological tests, mock-rubber-stamps, and tests written after production code. Use after writing a test, before running it, and any time a test passes too easily.
---

# Verify test quality

Apply these five heuristics to the test you just wrote (or are reviewing). Any that triggers warrants a closer look.

## Heuristics

1. **Test imports SUT but only asserts on mock return values.**
   If the test mocks the SUT's collaborators and then asserts that the SUT returns what the mocks returned, the test isn't testing the SUT — it's testing the mock framework. Restructure so assertions land on values the SUT *transforms*, not values it passes through.

2. **Test body has no `expect` calls on SUT-returned data.**
   Tests that only assert on mocks (`expect(mockFn).toHaveBeenCalledWith(...)`) without ever inspecting what the SUT *returned* are testing the call shape, not the behavior. Add an assertion on the SUT's return value.

3. **Test name matches `/should call/` or `/should return what mock returns/`.**
   These are red flags. Rename to describe the observable outcome. (See: derive-test-name-from-behavior.)

4. **Test was created AFTER the production code it claims to test.**
   Use `file_edits` ordering to check. If the test file was edited *after* the production file in the same TDD cycle, the test was written to match the implementation — the test cannot fail in a way that catches the implementation being wrong. The killer signal.

5. **Coverage delta of new test is zero.**
   A test that doesn't increase coverage either duplicates an existing test or asserts something the type system already enforces. Re-evaluate.

## Reusable outside TDD

Code review and coverage-gap workflows use this. The PostToolUse `post-tool-use/test-quality.sh` hook (orchestrator-scoped) is a narrow automated check today: it scans test-file edits for escape-hatch tokens (`it.skip`/`it.todo`/`it.fails`/`it.concurrent`, the `test.*` and `describe.*` equivalents, and `.skipIf`/`.todoIf`) and records `tdd_artifacts(kind='test_weakened')` when any of them appear. Heuristics #1, #2, and #4 — mock-rubber-stamping, no-SUT-assertion, and test-after-code — are NOT detected by the hook; they remain agent/reviewer responsibilities and are why this skill is consulted manually after writing a test. Heuristic #3 (suspicious test names) is a manual review item too. Heuristic #5 (zero-coverage-delta) requires a coverage run to evaluate.
