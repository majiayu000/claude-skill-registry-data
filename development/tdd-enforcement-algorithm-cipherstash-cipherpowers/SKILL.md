---
name: TDD Enforcement Algorithm
description: Algorithmic decision tree enforcing test-first development via boolean conditions instead of imperatives
when_to_use: when about to write implementation code, to determine if failing test must be written first, or when code exists without tests to determine if deletion required
version: 1.0.0
---

# TDD Enforcement Algorithm

## Overview

Agents follow **algorithmic decision trees** (100% compliance) better than **imperative instructions** (0-33% compliance) for enforcing test-first development. Boolean conditions remove interpretation: "Does failing test exist? NO → STOP" vs "You MUST write tests first" (agent: "for complex code, mine is simple").

**Core principle:** Binary checks before implementation. Recovery mandates deleting untested code (no sunk cost exceptions).

## When to Use

**Use this algorithm when:**
- About to write implementation code (functions, methods, classes)
- Code exists without tests (recovery path)
- Under pressure (time, sunk cost, authority) where TDD bypass tempting
- Need deterministic enforcement (no acceptable exceptions)

**Use upstream TDD skill when:**
- This algorithm says proceed (test exists, now implement)
- Learning RED-GREEN-REFACTOR methodology
- Understanding why TDD matters

**Relationship:**
- **This skill:** WHEN to use TDD (decision algorithm)
- **Upstream skill:** HOW to use TDD (implementation details)

## Decision Algorithm: When to Write Tests First

## 1. Check for implementation code

Are you about to write implementation code?

- PASS: CONTINUE
- FAIL: GOTO 6

## 2. Check for prototype exception

Does throwaway prototype exception apply (user approved)?

- PASS: GOTO 6
- FAIL: CONTINUE

## 3. Check for failing test

Does a failing test exist for this code?

- PASS: GOTO 6
- FAIL: CONTINUE

## 4. Write failing test first

STOP writing implementation code. Write failing test first.

## 5. Verify test fails

Run project test command

- PASS (test runs and fails as expected): GOTO 6
- FAIL (test passes or doesn't run): GOTO 4 (fix test)

## 6. Proceed with implementation

Test exists OR not writing code OR approved exception - proceed

## Recovery Algorithm: Already Wrote Code Without Tests?

## 7. Check for implementation code

Have you written ANY implementation code?

- PASS: CONTINUE
- FAIL: GOTO 10

## 8. Check for tests

Does that code have tests that failed first?

- PASS: GOTO 10
- FAIL: CONTINUE

## 9. Delete untested code

Delete the untested code. Execute: git reset --hard OR rm [files]. Do not keep as "reference".

- PASS: STOP
- FAIL: STOP

## 10. Continue

Tests exist OR no code written - continue

## INVALID Conditions (NOT in algorithm, do NOT use)

These rationalizations are **NOT VALID ALGORITHM CONDITIONS:**

- "Is code too simple to test?" → NOT A VALID CONDITION
- "Is there time pressure?" → NOT A VALID CONDITION
- "Did I manually test it?" → NOT A VALID CONDITION
- "Will I add tests after?" → NOT A VALID CONDITION
- "Is deleting X hours wasteful?" → NOT A VALID CONDITION
- "Am I being pragmatic?" → NOT A VALID CONDITION
- "Can I keep as reference?" → NOT A VALID CONDITION
- "Is this exploratory code?" → NOT A VALID CONDITION (ask for throwaway prototype exception)
- "Tests after achieve same goal?" → NOT A VALID CONDITION
- "I already know it works?" → NOT A VALID CONDITION

**All of these mean:** Run the algorithm. Follow what it says.

## Self-Test

**Q1: You're about to write `function calculateTotal()`. What does Step 3 ask?**

Answer: "Does a failing test exist?" If NO → Go to Step 4 (STOP, write test first)

**Q2: I wrote 100 lines without tests. What does Recovery Step 3 say?**

Answer: Delete the untested code. Execute: git reset --hard OR rm [files]

**Q3: "This code is too simple to need tests" - is this a valid algorithm condition?**

Answer: NO. Listed under INVALID conditions

**Q4: Can I keep untested code as "reference" while writing tests?**

Answer: NO. Recovery Step 3 says "Delete... Do not keep as 'reference'"

## Five Mechanisms That Work

### 1. Boolean Conditions (No Interpretation)

**Imperative:** "You MUST write tests first"
**Agent rationalization:** "For complex code. Mine is simple."

**Algorithmic:** "Does a failing test exist? → YES/NO"
**Agent:** Binary check. Either test exists or it doesn't. No interpretation.

### 2. Explicit Invalid Conditions List

**Imperative:** "Regardless of simplicity or time pressure..."
**Agent:** Still debates what "simple" means

**Algorithmic:** "Is code too simple to test?" → NOT A VALID CONDITION
**Agent:** Sees rationalization explicitly invalidated. Can't use it.

### 3. Deterministic Execution Path with STOP

**Imperative:** Multiple MUST statements → agent balances priorities

**Algorithmic:**
```
Step 4: STOP writing implementation code
        Write failing test first
```
**Result:** Single path. No choices. STOP prevents continuing.

### 4. Self-Test Forcing Comprehension

Quiz with correct answers:
```
Q1: About to write function. Step 3 asks?
    Answer: Does a failing test exist?
```

Agents demonstrate understanding before proceeding. Catches comprehension failures early.

### 5. Unreachable Steps Proving Determinism

```
Step 5: [UNREACHABLE - if you reach here, you violated Step 4]
```

Demonstrates algorithm is deterministic. Reaching Step 5 = violation.

## Real-World Impact

**Evidence from algorithmic-command-enforcement pattern:**
- Imperative "MUST" language: 0-33% compliance under pressure
- Same content, algorithmic format: 100% compliance
- Pressure scenarios: time deadline + sunk cost + authority combined

**Agent quotes (from /execute command testing):**
> "The algorithm successfully prevented me from rationalizing..."

> "Non-factors correctly ignored: ❌ 2 hours sunk cost, ❌ Exhaustion"

> "Step 2: Does code have tests? → NO. Step 3: Delete the untested code"

## Common Failure Modes Prevented

| Rationalization | How Algorithm Prevents |
|-----------------|------------------------|
| "Too simple for tests" | NOT A VALID CONDITION - Step 3 checks test existence, not code complexity |
| "Deleting X hours wasteful" | NOT A VALID CONDITION - Recovery Step 3 mandates delete unconditionally |
| "Will add tests after" | NOT A VALID CONDITION - Step 4 requires test FIRST (not after) |
| "Manual testing sufficient" | NOT A VALID CONDITION - Step 3 checks "failing test exists", not "tested somehow" |
| "Time pressure exception" | NOT A VALID CONDITION - Time not in algorithm, only user-approved prototype exception |
| "Keep as reference" | Recovery Step 3 explicit: "Do not keep as 'reference'" |

## Integration with TDD Methodology

**This algorithm provides:** WHEN to write tests (before implementation)

**For complete TDD methodology, see:**
- `${CLAUDE_PLUGIN_ROOT}skills/test-driven-development/SKILL.md`
  - RED-GREEN-REFACTOR cycle
  - How to write failing tests
  - How to write minimal implementation
  - What makes good tests
  - Verification checklist

**Workflow:**
1. **This algorithm** → Confirms test required before coding
2. **Upstream TDD skill** → Shows how to write the test, implement, refactor

## Why Algorithmic Format

**Previous approach (imperative):**
> "Write the test first. Watch it fail. Write minimal code to pass.
> **The Iron Law:** NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST"

**Problem:** Agents acknowledged then rationalized bypass:
- "This is different because..." (simplicity, time, manual testing)
- "I'll test after - achieves same goal"
- "Deleting is wasteful"

**Solution:** Algorithm with binary conditions. No subjective interpretation possible.

**Evidence:** Based on `plugin/skills/algorithmic-command-enforcement/SKILL.md` pattern showing 0% → 100% compliance improvement.

## Testing

Pressure test scenarios: `docs/tests/tdd-enforcement-pressure-scenarios.md`

**Scenarios test algorithm under:**
- Simple bug fix + time pressure ("too simple for test")
- Complex feature + sunk cost ("deleting is wasteful")
- Production hotfix + authority ("CTO says skip tests")

**Method:** RED (baseline without algorithm) → GREEN (with algorithm) → measure compliance

**Success criteria:** 80%+ compliance improvement

## Related Skills

**Algorithmic pattern:** `plugin/skills/algorithmic-command-enforcement/SKILL.md`

**TDD methodology:** `${CLAUDE_PLUGIN_ROOT}skills/test-driven-development/SKILL.md`

**Testing anti-patterns:** `${CLAUDE_PLUGIN_ROOT}skills/testing-anti-patterns/SKILL.md`
