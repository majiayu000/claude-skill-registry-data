---
name: safe-refactor
description: |
  Guide safe refactoring of complex, untested code using a multi-phase hybrid approach: characterization tests → agent-assisted refactoring → manual review → integration testing → staged rollout. Use this skill whenever the user mentions refactoring, code cleanup, or code modernization — especially when there are no existing tests, when delegating to an agent, or when regressions would be costly. Also trigger for: "improve code quality without breaking things", "migrate to a new pattern safely", "modernize legacy code", "rewrite this module", "clean up this file", "my code has no tests but I need to refactor it", or any scenario involving high-risk code changes where behavior preservation matters. When in doubt, use this skill — a structured approach is almost always better than ad-hoc refactoring.
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# Safe Refactoring with Hybrid Approach

## When to Use This Skill

✅ **Use when:**

- Refactoring complex, high-risk code with **zero or minimal test coverage**
- Delegating refactoring work to an **agent or external developer**
- Need to **guarantee behavior preservation** across changes
- Dealing with **mission-critical functions** where regressions are expensive

❌ **Skip when:**

- Code already has 80%+ test coverage (just keep tests green)
- Change is trivially small and isolated (rename a variable, extract a constant)

---

## The Hybrid Approach: 5 Safety Layers

| Layer                     | Who   | Goal                                      |
| ------------------------- | ----- | ----------------------------------------- |
| 1. Characterization tests | You   | Lock current behavior before any changes  |
| 2. Agent refactoring      | Agent | Refactor while keeping all tests green    |
| 3. Manual code review     | You   | Catch logic errors tests can't find       |
| 4. Integration testing    | You   | Verify end-to-end flows still work        |
| 5. Staged rollout         | You   | Monitor in staging before full production |

---

## Phase 1: Generate Characterization Tests

**Goal**: Capture current behavior as a golden master — before touching a line of code.

> ⚠️ Run these tests against the _original_ code first to confirm they pass. A characterization test that never passed is worthless.

### 1a: Identify What to Test

Focus on:

- Public API surface (functions called by other modules)
- Business-critical logic (money, auth, data transforms)
- Functions with side effects (DB writes, file I/O, external calls)
- Complex conditional trees

### 1b: Design Test Cases Per Function

For each function, capture **3–5 cases**:

| Scenario                  | What to verify                                   |
| ------------------------- | ------------------------------------------------ |
| Happy path                | Correct output, expected side effects            |
| Boundary / edge           | Empty input, max values, zero, null              |
| Error / invalid input     | Exception type, error message, no partial writes |
| Concurrency (if relevant) | No race conditions, correct locking              |

**Template per test case:**

```
Function:  processPayment(amount, card, expiry)
Input:     {amount: 100.00, card: "4532123456789010", expiry: "12/25"}
Output:    {status: "SUCCESS", transaction_id: <non-null>, fee: 2.50}
Side fx:   DB INSERT into payments table (verify row exists)
Timing:    < 500ms
```

### 1c: When Characterization Tests Reveal Bugs

Sometimes you'll discover the current code is _wrong_. Don't blindly preserve bugs.

- **Obvious bug** (off-by-one, null dereference): Fix it separately before refactoring. Keep the fix in its own commit.
- **Ambiguous behavior** (undocumented edge case): Flag it as a known issue; preserve the behavior for now and file a follow-up.
- **Intentional quirk** (backward-compat hack): Document it clearly in the test with a comment explaining why.

---

## Phase 2: Brief the Agent

Paste this template directly into your agent prompt — fill in the bracketed fields:

```
REFACTORING TASK
================

OBJECTIVE:
Refactor [FILE OR FUNCTION] to [SPECIFIC IMPROVEMENT — e.g., "reduce cyclomatic
complexity", "migrate from callbacks to async/await", "split into smaller functions"].
Do NOT add new features or change behavior.

HARD CONSTRAINT — ALL TESTS MUST PASS:
A characterization test suite is at [TEST PATH]. Run it with:
  [TEST COMMAND — e.g., pytest tests/characterization/, npm run test:char]

Before submitting:
1. Make your changes
2. Run the full test suite
3. If any test fails:
   a. Determine if it's a test bug or a regression you introduced
   b. If it's a test bug, explain why in your submission notes
   c. If it's your regression, fix it and retest
4. Do NOT submit until all tests are green

QUALITY GATES:
- No new lint warnings (run: [LINT COMMAND])
- No new type errors (if applicable)
- All functions still exported with same signatures
- Comments updated to reflect new logic

SUBMIT FORMAT:
Reply with:
1. Summary of changes made
2. Test results (paste output)
3. Any flagged test bugs with justification
4. Any concerns or questions about the codebase

WHAT NOT TO DO:
- Do not refactor things outside the specified scope
- Do not change function signatures
- Do not add dependencies
- Do not "improve" behavior — only improve structure
```

### Handling Agent Escalations

The agent may come back with one of these situations:

| Agent says                                                    | Your response                                                      |
| ------------------------------------------------------------- | ------------------------------------------------------------------ |
| "Test X seems wrong — the code clearly should return Y"       | Review the test. If the agent is right, fix the test and re-run.   |
| "I couldn't keep test X green without changing the signature" | This signals a deeper problem. Pause and discuss scope.            |
| "I added a dependency to make this cleaner"                   | Reject unless you approved it. Ask for a version without it.       |
| "Some tests are flaky"                                        | Investigate before proceeding — flaky tests mask real regressions. |

---

## Phase 3: Manual Code Review

**Goal**: Catch logic errors that tests can't detect — wrong algorithm, subtle off-by-one, silent data corruption.

Focus your review time on **top 3–5 highest-risk functions** only.

### Review Checklist

For each critical function, compare before/after:

- [ ] **Algorithm unchanged**: Same logical steps, same order of operations?
- [ ] **Conditionals preserved**: Every `if/else` branch still present and correct?
- [ ] **Loop termination**: Conditions and exit logic unchanged?
- [ ] **Side effects intact**: All DB writes, API calls, file ops still happen?
- [ ] **Error handling**: Exceptions still caught and re-raised correctly?
- [ ] **Type handling**: No implicit coercions introduced?
- [ ] **Variable mutation**: Are assignments in the same order? (order matters for side effects)

### Red Flags That Demand Deeper Investigation

- A `for` loop became a `map/filter` — check edge cases on empty input
- An `if/else` chain was restructured — verify all branches with a truth table
- Multiple functions were merged or split — confirm all logic is still reachable
- Error handling was "cleaned up" — verify error paths aren't silently swallowed

### Review Pattern

```
FUNCTION: validateUser
RISK: HIGH (auth logic)

BEFORE: checks role first, then expiry, then IP allowlist
AFTER:  checks expiry first, then role, then IP allowlist

VERDICT: ⚠️ Order changed. Ask agent: does order matter here?
         (If role check short-circuits on invalid role, expiry check was
          never reached for invalid roles. New order changes that behavior.)
```

---

## Phase 4: Integration Testing

**Goal**: Verify end-to-end flows that span multiple functions.

### Integration Test Template

```
FLOW: [Name — e.g., "User checkout with payment"]

SETUP:
  1. [Seed test data]
  2. [Reset mocks / external stubs]

STEPS:
  1. [User action 1]
  2. [User action 2]
  ...

VERIFY:
  ✓ [Expected DB state]
  ✓ [Expected API response]
  ✓ [Expected file/email/queue output]
  ✓ No orphaned records
  ✓ No unhandled errors in logs

PERFORMANCE:
  Baseline: [X ms, measured on original code]
  Threshold: < [X * 1.10] ms (allow 10% variance)
```

**How to establish your baseline** if you don't have one:

1. Run the integration flow 5 times on the _original_ code
2. Take the median execution time
3. Set alert threshold at +10%

---

## Phase 5: Staged Rollout

### Deployment Gates

```
GATE 1 — STAGING
  Deploy → Run full suite → Monitor 1–2 hours
  Watch: error rate, latency, unexpected exceptions
  → Green? Proceed. Red? Rollback.

GATE 2 — PRODUCTION CANARY (10–20% traffic)
  Monitor 30 minutes
  Watch: error rate ≤ baseline + 5%, latency ≤ baseline + 10%
  → Green? Proceed. Red? Rollback.

GATE 3 — PRODUCTION FULL
  Monitor 2–4 hours
  Keep rollback ready
```

### What to Monitor

| Metric          | How to set baseline                   | Alert threshold                    |
| --------------- | ------------------------------------- | ---------------------------------- |
| Error rate      | Avg over last 7 days in production    | Baseline + 5 percentage points     |
| P95 latency     | Measure on staging with original code | Baseline × 1.10                    |
| DB query count  | Log slow queries on staging           | + 50% vs baseline                  |
| Business metric | Revenue / conversions / key actions   | Any statistically significant drop |

---

## Rollback Plan

**Trigger rollback if:**

- Any critical test failure in staging
- Error rate increases by more than 5 percentage points
- Latency degrades more than 10%
- User reports data loss or corruption

**Procedure (target: < 15 minutes):**

```
1. Alert on-call team
2. Pause new ingestion if safe to do so
3. Revert:
     git revert <commit>         # code rollback
     kubectl rollout undo ...    # if Kubernetes
4. Wait for deploy (~2–3 min)
5. Verify error rate returns to baseline
6. Check DB for consistency (orphaned records, partial writes)
7. Document: what failed, what the tests missed, how to prevent recurrence
```

---

## Workflow Summary

### Delegating to an Agent

```
1. Write characterization tests locally (1–2 hrs)
   → Confirm they pass against original code

2. Give agent: code + tests + Phase 2 brief
   → Agent refactors, returns code + test output

3. Manual review: top 3–5 functions (30–45 min)
   → Focus on algorithm correctness, not style

4. Run integration tests (15–30 min)
   → Verify end-to-end flows

5. Deploy to staging → monitor → canary → full
   → Keep rollback ready throughout
```

### Doing It Yourself

Same sequence — skip the agent brief and do the refactoring yourself between steps 1 and 3.

---

## Common Pitfalls

| Pitfall                                | Why it bites you                | Prevention                               |
| -------------------------------------- | ------------------------------- | ---------------------------------------- |
| Skip characterization tests            | No way to know what broke       | Non-negotiable: write them first         |
| Add features during refactor           | Mixes concerns, harder to debug | Separate commits: refactor, then feature |
| Use different test data for validation | Can't compare apples to apples  | Same inputs, always                      |
| Ignore performance metrics             | Silent 3× slowdown ships        | Measure baseline before touching code    |
| Deploy directly to production          | First real test is on users     | Always stage first                       |
| No rollback plan                       | Scrambling during an incident   | Write it before you deploy               |
| Trust flaky tests                      | They hide real regressions      | Fix or skip flaky tests explicitly       |
