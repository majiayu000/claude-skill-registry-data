---
name: audit-test-suite
description: Find where an existing test suite is weak and decide what to test next, ranked by risk. Use this when asked to add missing tests, find gaps, raise coverage, assess test quality or see which areas are thin, even if the request only mentions a coverage percentage.
---

# Audit a test suite

A coverage number shows which lines ran, not which behaviour was checked. The
most valuable finds are often tests that never run, tests that cannot fail, and
risky behaviour nobody tested.

## When to use

The task is about finding what to test, not writing one known test. Once you have
the list, use `write-tests` for each item.

## Steps

1. **Run what exists.** Follow `orient-in-codebase`, run the suite, and record
   how many tests ran and how many passed.

2. **Check that every test runs.** List all test files, then check that each one
   is reached by a CI job, directly or through a script it calls. Files that
   nothing runs are the cheapest gap to close. Wire each one in only if it passes.

3. **Check what the coverage number means.** Find which tests and source files are
   in scope, and what is excluded. Do not trust the percentage until you know that.

4. **Look for tests that cannot fail.** Sample tests in the riskiest areas:

   - Mocks of the code under test
   - Assertions that only check that something exists
   - Tests that read a copy of the code, or only match source text
   - Tests with no assertions, or skipped tests
   - Empty loops, such as a table that no longer has any rows

5. **Map risk.** List the areas by the damage a bug would cause:

   1. Money, credits, quota, entitlements
   2. Login, permissions, data belonging to other users
   3. Data loss and irreversible actions
   4. Secrets and personal data
   5. Schedules, retries, state changes
   6. Everything else

6. **Compare risk with tests.** For each of the top areas, use the list in step 2
   of `write-tests`. Mark each item as tested, weakly tested or missing. Read the
   test before you mark it. A matching file name is not evidence.

7. **Use coverage to find unexplored code.** Look at uncovered branches in the top
   areas. Skip generated code and trivial getters.

8. **Rank the gaps.** Order by risk first, then by effort. Make each item a
   specific case, not an area.

## Stop and ask when

- The suite cannot run locally.
- Fixing a gap needs a production change that you were not asked to make.

## Common mistakes

| Tempting move | Why it fails | Do this instead |
| --- | --- | --- |
| Start with the lowest coverage file | It may be harmless | Start from risk |
| Write tests to hit lines | Adds tests that check nothing | Target a behaviour |
| Report "add tests for billing" | Nobody can act on that | Name the exact case |
| Exclude files to raise the number | Hides the gap | Keep the scope unchanged |
| Lower a coverage floor to pass | Removes the protection | Add real tests |
| Assume a test checks what its name says | Names can be wrong | Read the assertions |

## Example

Weak finding: "Payment module has 62% coverage."

Strong finding:

```markdown
1. High: a repeated refund webhook can credit twice.
   Evidence: `refund()` has no idempotency check; `refund.test` sends one event.
   Add: deliver the same event twice and concurrently, and assert one credit.
```

## Report

```markdown
Suite: <tests run, passed, failed, skipped>
Not running: <files no job reaches>
Cannot fail: <tests that check nothing, and why>
Coverage scope: <what the number includes and excludes>

Gaps, highest risk first:
1. <severity>: <defect that could ship>
   Evidence: <file and what you read>
   Add: <exact test case>
```
