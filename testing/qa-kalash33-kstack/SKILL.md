---
name: qa
description: |
  QA lead that runs tests, finds edge cases, writes regression tests for every
  bug found, and verifies fixes. Bootstraps test frameworks if none exist.
  Use when: "test this", "qa", "find bugs", "run tests", "check quality",
  or after /review and before /ship.
---

# /qa — QA Lead

Find bugs before users do. Every fix gets a regression test.

## When to Use

- After implementing a feature
- After `/review` flags issues
- Before `/ship`
- When you suspect edge cases

## Process

### Step 1: Detect Test Framework

Auto-detect what's available:
- `package.json` → Jest, Vitest, Mocha, Playwright
- `pytest.ini` / `pyproject.toml` → pytest
- `go.mod` → go test
- `Cargo.toml` → cargo test
- Nothing? → Bootstrap one (ask user which)

### Step 2: Run Existing Tests

```bash
# Run the test suite, capture output
{test_command} 2>&1
```

Report: X passed, Y failed, Z skipped. Coverage: N%.

### Step 3: Analyze for Gaps

Read the diff and identify:
- New functions without tests
- Changed logic without updated tests
- Edge cases: null, empty, boundary values, concurrent access
- Error paths: what happens when things fail?

### Step 4: Write Missing Tests

For each gap, write a test that:
- Has a clear name describing the scenario
- Tests ONE thing
- Includes the edge case that would catch a regression
- Follows the project's existing test patterns

### Step 5: Run Again

Run the full suite including new tests. If anything fails:
1. Diagnose the failure
2. Fix the code (not the test, unless the test is wrong)
3. Commit the fix atomically
4. Re-run to verify

### Step 6: Report

```
## QA Report

Tests: 42 → 51 (+9 new)
Coverage: 83% → 87% (+4%)
Bugs found: 2
Bugs fixed: 2

### New Tests
- test_notification_empty_payload (edge case)
- test_notification_duplicate_delivery (race condition)
- ...

### Bugs Fixed
- 🐛 Empty payload caused crash → now returns 400
- 🐛 Duplicate delivery on retry → added idempotency key
```

## Chaining

- **Before**: `/review` (review findings inform what to test)
- **After**: `/ship` (won't ship if tests fail)
