---
name: test
description: Run tests with automatic failure fixing and regression prevention
disable-model-invocation: true
user-invocable: true
argument-hint: "[test target or pattern]"
---

# Test Runner with Auto-Fix

Run tests and fix any failures for: $ARGUMENTS

## Process

1. **Run Tests** — Execute the test suite for the target
2. **Analyze Failures** — For each failure:
   - Read the failing test to understand intent
   - Read the source code being tested
   - Identify root cause (not symptoms)
3. **Fix Issues** — One by one:
   - Fix the code (not the test, unless the test is wrong)
   - Re-run the specific test after each fix
   - Verify no regressions by running the full suite
4. **Report** — Final test results and summary of fixes applied

## Rules

- Never delete or skip failing tests to make builds pass
- Fix root causes, not symptoms
- Re-run tests after each fix to catch regressions
- If a test is genuinely wrong (testing outdated behavior), fix the test with explanation
