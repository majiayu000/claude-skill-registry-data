---
name: flaky-test-fixer
description: Use when a test passes and fails without code changes, fails only in CI or only when run with other tests, times out intermittently, or the team is retrying, skipping or quarantining unreliable tests — unit, integration or end-to-end.
---

# Flaky Test Fixer

## Overview

A flaky test has a cause that can be found: timing, shared state, order, environment or randomness. Reproduce the flake reliably, identify which of those it is, and fix the cause. Retries and longer timeouts hide the problem; they do not fix it.

## Method

1. **Reproduce the flake.** Run the test many times, alone and with the full suite:
   - Jest/Vitest: run in a loop, or `--runInBand` vs parallel.
   - pytest: `pytest -x --count=50` (pytest-repeat) and random order with pytest-randomly.
   - Playwright: `npx playwright test <file> --repeat-each=20 --workers=4`.
   - JUnit: `@RepeatedTest(50)` on the test, or run the suite in a shell loop.
   Record the failure rate and the exact error.
2. **Classify** using the table below. Compare passing and failing runs: logs, timing, order, environment.
3. **Confirm the cause** with a deliberate change that makes it fail every time (shuffle order, add a delay, slow the network, change the time zone).
4. **Fix the cause**, then rerun the loop until there are zero failures across many runs.
5. **Remove** any retries, sleeps or skips added as workarounds.

## Causes and fixes

| Cause | Signs | Fix |
|---|---|---|
| Timing / async | Passes when slow, fails when fast; `waitForTimeout`, missing `await` | Await the real condition (event, response, visible element); add missing awaits |
| Shared state | Fails only with other tests; order matters | Fresh data per test, reset singletons, mocks and module state in `beforeEach`, isolate database (transaction rollback or unique data) |
| Test order | Fails with random ordering | Remove dependence on data created by earlier tests |
| Time and dates | Fails near midnight, month end, DST, other time zones | Freeze or inject the clock; use UTC; avoid `new Date()` in assertions |
| Randomness | Different inputs per run | Seed the generator or use fixed fixtures |
| Concurrency | Parallel workers clash on ports, files, accounts | Unique ports, temp directories, accounts per worker |
| External services | Network calls to real third parties | Mock third parties; use local containers for owned dependencies |
| Environment | Only in CI | Compare versions, CPU speed, locale, time zone, screen size, env vars |
| Resource leaks | Fails late in long runs | Close servers, connections, timers, listeners in `afterEach` |

## Output

```
Test: <name and file>
Failure rate: <before> → <after> over <N> runs
Cause: <category and the specific line or condition>
Fix: <change made>
```

## Common mistakes

- Adding retries or increasing timeouts and calling it fixed.
- Running the test once after the fix.
- Fixing the test when the flake is a real race condition in product code.
- Quarantining tests with no owner or follow-up date.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
