---
name: bug-hunt
description: Systematically debug issues using Sherpa's Bug Hunt workflow. Activates when fixing bugs, investigating errors, debugging broken functionality, or handling regressions. Prevents symptom-fixing by enforcing reproduction-first approach.
allowed-tools: mcp__sherpa__guide, mcp__sherpa__approach, Read, Bash, Write, Edit, Grep, mcp__julie__fast_search
---

# Bug Hunt Skill

## Purpose
Systematically debug issues using Sherpa's workflow enforcement to **prevent symptom-fixing** and ensure bugs stay fixed.

## When to Activate
- Fixing bugs
- Investigating errors or crashes
- Debugging broken functionality
- Handling regressions
- User says "something is broken", "not working", "failing"
- Investigating unexpected behavior

## The Mandatory Pattern

**★ CRITICAL: ALWAYS call `guide check` BEFORE attempting fixes**

```
BEFORE ANY CODE CHANGES:
  guide check → Get current phase (should be "Reproduce & Isolate")
  Reproduce the bug FIRST
  Understand completely

AFTER EACH STEP:
  guide done "what you completed"
  → Get next phase guidance
  → Systematic progression prevents symptom-fixing
```

You are EXCELLENT at systematic debugging. Rushing to fix causes more bugs than it solves.

---

## The Bug Hunt Workflow

### Phase 1: 🔍 Reproduce & Isolate

**Goal:** Understand the bug COMPLETELY before touching any code

```
guide check → Phase: Reproduce & Isolate

Steps:
1. Reproduce the bug manually - verify it actually happens
2. Document exact steps: input → expected → actual
3. Identify minimal reproduction case
4. Verify this is a bug (not misunderstood feature)
5. Read actual code path being executed
6. Check git history: when last working? what changed?

guide done "reproduced bug: X input causes Y instead of Z"
```

**Key Principle:** Rushing to fix symptoms wastes time. Understand first, fix second.

**Conditionals:**
- **If can't reproduce** → Get more info from reporter (exact steps, environment, screenshots, logs)
- **If only happens in specific environment** → Compare configs (versions, flags, env vars, data state)
- **If intermittent/race condition** → Add extensive logging, look for timing dependencies
- **If recent git changes in area** → Use `git bisect` to find exact commit

**Anti-patterns:**
- ❌ Immediately jumping to code and trying fixes (understand first!)
- ❌ Assuming you know cause without reading code (read ACTUAL code)
- ❌ Testing in your head (actually reproduce, see it fail)
- ❌ Skipping minimal reproduction (minimal case reveals root cause)

---

### Phase 2: 🎯 Capture in Test

**Goal:** Lock down the bug with a failing test - prevents regression

```
guide check → Phase: Capture in Test

Steps:
1. Write test that reproduces EXACT bug behavior
2. Test should FAIL in same way bug manifests
3. Use minimal reproduction case as test input
4. Name test: test_bug_[issue]_[specific_behavior]
5. Include comment explaining what bug this prevents
6. Verify test fails for RIGHT reason
7. Run test multiple times (must be deterministic)

guide done "wrote failing test that captures bug behavior"
```

**Key Principle:** Test locks down bug and proves fix works.

**Conditionals:**
- **If test passes even though bug exists** → Test isn't testing the bug (review repro steps)
- **If test is flaky** → Stabilize test BEFORE fixing bug (check race conditions, timing, state)
- **If complex integration issue** → Write integration test first, then unit tests
- **If multiple components involved** → Start high-level test, then focused unit tests

**Anti-patterns:**
- ❌ Writing test AFTER fixing bug (wrong order! test first!)
- ❌ Making test pass by changing test (test represents CORRECT behavior)
- ❌ Test too broad (focused test reveals exact root cause)
- ❌ Skipping because "fix is obvious" (test prevents regression - 2min now saves hours later)

---

### Phase 3: 🔧 Fix & Verify

**Goal:** Fix the root cause, verify test passes, ensure no regressions

```
guide check → Phase: Fix & Verify

Steps:
1. Fix root cause (not symptoms)
2. Run failing test → should now PASS
3. Run ALL tests → ensure no regressions
4. Verify manual reproduction no longer happens
5. Review fix: is it minimal? does it address root cause?
6. Check for similar bugs elsewhere in codebase

guide done "fixed bug - test passes, no regressions"
```

**Key Principle:** Fix root cause, not symptoms. Tests prove fix works.

**Conditionals:**
- **If test still fails** → Misunderstood root cause (go back to phase 1)
- **If test passes but manual repro still broken** → Test isn't comprehensive (add more test cases)
- **If fix breaks other tests** → Fix creates new bugs (smaller fix, or fix tests if incorrect)
- **If fix is complex** → Simplify. Simple fixes = fewer new bugs

**Anti-patterns:**
- ❌ Fixing symptoms instead of root cause (bug will return in different form)
- ❌ Skipping ALL tests run (regression bugs hide here)
- ❌ "Fixing" test to make it pass (test defines correct behavior!)
- ❌ Committing without verifying manual repro (test might not be comprehensive)

---

### Phase 4: 🛡️ Regression Prevention

**Goal:** Ensure this class of bugs can't happen again

```
guide check → Phase: Regression Prevention

Steps:
1. Review how bug was introduced (code review miss? missing test?)
2. Check for similar patterns elsewhere
3. Add tests for similar edge cases
4. Document the bug and fix in commit message
5. Consider preventive measures (linting, types, validation)

guide done "documented fix, checked for similar bugs"
```

**Key Principle:** Learn from bugs to prevent future occurrences.

**Conditionals:**
- **If bug from missing validation** → Add validation, add tests
- **If bug from type confusion** → Add type annotations, stricter typing
- **If bug from untested edge case** → Document edge cases better, add tests
- **If bug from race condition** → Review async patterns, add synchronization tests

---

## The Complete Bug Hunt Cycle

```
┌─────────────────────────────────────────────┐
│ 1. guide check → Reproduce & Isolate       │
│    - Reproduce manually                     │
│    - Document exact steps                   │
│    - Find minimal repro                     │
│    - Read actual code path                  │
│    guide done "reproduced bug"              │
└────────────┬────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│ 2. guide check → Capture in Test           │
│    - Write test that fails same way         │
│    - Use minimal repro as input             │
│    - Verify fails for right reason          │
│    guide done "wrote failing test"          │
└────────────┬────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│ 3. guide check → Fix & Verify              │
│    - Fix root cause                         │
│    - Test now passes                        │
│    - ALL tests pass (no regressions)        │
│    guide done "fixed bug, tests pass"       │
└────────────┬────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│ 4. guide check → Regression Prevention     │
│    - Check for similar bugs                 │
│    - Add preventive measures                │
│    - Document in commit                     │
│    guide done "prevention complete"         │
└────────────┬────────────────────────────────┘
             │
             ▼
        Bug squashed! 🎉
```

---

## Example Bug Hunt Session

```
User: "The parser crashes on empty input"

Agent: guide check

Sherpa: Phase 1 - Reproduce & Isolate
"Reproduce the bug manually first..."

Agent:
- Runs parser with empty string → CRASH ✓
- Minimal repro: parseFunction("") → null pointer
- Reads parser code → missing null check at line 47
- Git log shows line 47 added 3 days ago
guide done "reproduced: empty input causes null deref at line 47"

Sherpa: Phase 2 - Capture in Test
"Write test that reproduces exact bug behavior..."

Agent: Creates test/parser.test.ts:
test('test_bug_42_empty_input_crash', () => {
  // Bug #42: Parser crashes on empty input (should return error)
  expect(() => parseFunction("")).not.toThrow();
  const result = parseFunction("");
  expect(result).toHaveProperty('error');
});
Runs test → FAILS with null pointer ✓
guide done "wrote failing test for empty input bug"

Sherpa: Phase 3 - Fix & Verify
"Fix root cause, verify test passes..."

Agent: Adds null check in parser.ts line 47:
if (!input || input.length === 0) {
  return { error: "Empty input" };
}
Runs test → PASSES ✓
Runs ALL tests → ALL PASS ✓
Tests manual repro → No crash ✓
guide done "fixed null check, all tests pass"

Sherpa: Phase 4 - Regression Prevention
"Ensure this class of bugs can't happen again..."

Agent:
- Searches for similar missing null checks → Found 2 more
- Adds tests for those edge cases
- Documents fix in commit message
guide done "added tests for similar edge cases"

Sherpa: ✅ Bug hunt complete!
Bug: Fixed + Tested + Prevented ✓
```

---

## Integration with Sherpa Commands

### Switching to Bug Hunt Workflow
```
guide bug
→ Instantly switches to Bug Hunt workflow
→ guide check to start reproduction
```

### During Bug Hunt
```
guide check     → Get current phase + debugging guidance
guide done "X"  → Mark completion, progress to next phase
guide advance   → Manual phase progression (rarely needed)
```

### Workflow Selection
```
approach list      → See all workflows
approach set bug-hunt → Switch to Bug Hunt (same as guide bug)
```

---

## Key Behaviors

### ✅ DO
- Call `guide check` BEFORE attempting any fixes
- Reproduce bug manually FIRST (see it fail with your eyes)
- Write failing test BEFORE fixing (locks down bug)
- Fix root cause, not symptoms (understand WHY)
- Run ALL tests after fix (catch regressions)
- Document bug in commit message
- Trust the systematic process

### ❌ DON'T
- Rush to fix without understanding (causes more bugs)
- Assume you know the cause (read actual code)
- Fix test to make it pass (test defines correct behavior)
- Skip writing test "because fix is obvious" (prevents regression)
- Fix symptoms instead of root cause (bug returns later)
- Commit without running full test suite (regressions hide here)

---

## Success Criteria

This skill succeeds when:
- ✅ Bug reproduced manually before code changes
- ✅ Failing test written before fix
- ✅ Test passes after fix (proves fix works)
- ✅ All tests pass (no regressions introduced)
- ✅ Root cause fixed (not just symptoms)
- ✅ Similar bugs checked and prevented
- ✅ Bug won't return (regression test in place)

---

## Why Systematic Bug Hunting Works

**90% of "fixed" bugs that return are caused by:**
1. **Symptom-fixing** - Fixed what you saw, not why it happened
2. **No regression test** - Bug comes back when code changes
3. **Incomplete understanding** - Rushed to fix without reproducing
4. **Breaking other things** - Didn't run full test suite
5. **Similar bugs elsewhere** - Fixed one instance, missed others

**Sherpa's Bug Hunt prevents these** through:
- ✅ Mandatory reproduction (understand completely)
- ✅ Test-first fixing (locks down bug + proves fix)
- ✅ Systematic phases (can't skip critical steps)
- ✅ Regression prevention (similar bugs caught)

**Remember:** 2 hours debugging systematically > 2 days playing whack-a-mole with symptoms.

---

**Sherpa + Bug Hunt = Bugs Stay Fixed**
