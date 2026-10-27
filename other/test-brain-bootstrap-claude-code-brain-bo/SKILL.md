---
name: test
description: Run the test suite and report results. Use after making changes to verify nothing is broken. Reads the test command from claude/build.md.
---

# Test Skill

Run tests and report results with actionable failure analysis.

## Protocol

### 1. Read the test command
Read `claude/build.md` for the test command and any special flags.

### 2. Run tests
```bash
# Use the command from claude/build.md
# Example: npm test 2>&1 | tail -50
```

For targeted tests (faster feedback):
```bash
# Example: npm test -- --testPathPattern=<filename> 2>&1 | tail -30
```

### 3. Analyze results
- All pass: report summary and exit
- Failures: analyze each failure

### 4. For each failing test

**A. Read the exact assertion failure:**
```
Expected: <value>
Received: <value>
```

**B. Find the source of the failure:**
- What code is the test exercising?
- What did the recent change touch?
- Is this a pre-existing failure or newly introduced?

**C. Fix or flag:**
- If newly introduced by current change: fix it
- If pre-existing: document it, do NOT fix unrelated failures
- If test itself is wrong: flag for user review (never silently delete a failing test)

### 5. Re-run after fixes
Keep running until all tests pass (or all failures are documented as pre-existing).

### 6. Report
```
Tests: PASS — 142 passed, 0 failed, 0 skipped
```
or
```
Tests: FAIL — 140 passed, 2 failed, 0 skipped
Newly introduced failures:
  - test/auth.test.ts:45 — [failure reason + fix applied]
Pre-existing failures (not caused by current change):
  - test/legacy.test.ts:12 — [noted, not fixed]
```

## Rules
- NEVER delete a failing test to make the suite pass
- NEVER mock the thing being tested
- NEVER mark a task complete with failing tests
- Pre-existing failures must be distinguished from introduced failures
