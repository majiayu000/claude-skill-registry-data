---
name: incremental-tdd
description: Use when implementing features or refactoring with TDD - enforces writing ONE test at a time, implementing minimal code to pass, then repeating, preventing batch test writing that defeats incremental design discovery
---

# Incremental TDD

## Overview

**Write ONE test. Make it pass. Repeat.**

TDD is not "write all tests, then implement." It's an incremental cycle where each test teaches you what to build next.

**Core principle:** Writing tests in batch defeats the design discovery benefit of TDD.

## The Iron Law

```
ONE FAILING TEST AT A TIME
```

Write a single failing test → Implement minimal code to pass → Refactor if needed → Write NEXT failing test.

**No exceptions:**
- Not "write a few failing tests"
- Not "cover main scenarios first"
- Not "write comprehensive test suite then implement"
- ONE failing test, make it pass, then next failing test

**Clarification:** Having multiple GREEN (passing) tests is fine. The rule is about FAILING tests. Only write ONE failing test at a time.

## The Cycle

```
1. Write ONE simple test (simplest case)
2. Run ALL tests - watch it fail (RED)
3. Write minimal code to pass (GREEN)
4. Run ALL tests - verify all pass (still GREEN)
5. Refactor if needed (REFACTOR)
   5a. Check code quality (duplication, complexity)
   5b. Review ADR compliance (dispatch reviewer subagent with adr-review skill)
   5c. Fix issues found
6. Run ALL tests - verify still passing
7. Commit
8. GOTO 1 for next test
```

**IMPORTANT: Always run ALL tests, not just the one you're working on.**

This catches regressions immediately. If you only run the current test, you won't notice if your changes broke existing functionality.

**REFACTOR phase includes ADR review:** After tests pass, dispatch a reviewer subagent with the adr-review skill to check compliance with all project ADRs. This catches issues that tests don't verify (naming, structure, documentation standards).

## Two Stages of RED

**Compile error? Add empty stub. Run again. Then implement.**

| Step | Action | Don't Do This |
|------|--------|---------------|
| 1 | Write test | |
| 2 | Run → "Export not found" | Don't implement yet |
| 3 | Add: `export function foo() { return null; }` | Not the full implementation |
| 4 | Run → "Expected X, got null" | This is still RED |
| 5 | NOW implement real behavior | |
| 6 | Run → GREEN | |

**Compile error ≠ implement.** Stub first, run again, see behavior failure, THEN implement.

## Why One Test at a Time Matters

**The REFACTOR step is where design emerges.**

When you write ONE test at a time:
1. RED: Write one failing test
2. GREEN: Minimal code to pass
3. **REFACTOR: Evaluate the emerging design, improve it**
4. Now you understand the design → inform next test

**Critical insight:** After each test passes, you can evaluate the design and discover what's next. Writing 3-5 tests at once commits you to a design before seeing what you need.

❌ **Batch**: Write 5 tests → implement everything
✓ **Incremental**: Write ONE test → implement → evaluate → next test

## ADR Review in REFACTOR Phase

After tests pass (GREEN), check ADR compliance BEFORE committing.

**Use a reviewer subagent with adr-review skill:**

```markdown
**Dispatch reviewer subagent:**

You are reviewing code for ADR compliance in the REFACTOR phase.

**Your task:** Use the adr-review skill to review [file/function]

**Instructions:**
1. Use Skill tool to load: adr-review
2. Follow the skill to review code against all ADRs
3. Report violations with specific line numbers and fixes
4. STOP and report back

Be strict - flag all violations per the skill.
```

**After review:**
- Fix violations found
- Re-run ALL tests (ensure still GREEN)
- Only then commit

**Why separate subagent?**
- Separates concerns: behavior (tests) vs structure (ADRs)
- Reviewer can't rationalize "close enough"
- Clear authority: reviewer reports, you decide

**When to skip ADR review:**
- No ADRs exist in project yet
- Trivial change (typo fix, comment update)
- Emergency hotfix (review after deployment)

## Quick Reference

| Situation | Action |
|-----------|--------|
| Starting TDD task | Write ONE simplest test, run ALL tests (RED) |
| Test passes | Run ALL tests, refactor if needed, write NEXT test |
| After GREEN | Dispatch reviewer subagent for ADR compliance |
| After ADR review | Fix violations, re-run tests, commit |
| Refactoring existing code | ONE test for simplest case first |

## Common Rationalizations (All Wrong)

| Excuse | Reality |
|--------|---------|
| "Need comprehensive coverage upfront" | Build incrementally, one test at a time. |
| "Senior engineer/best practices say all tests first" | Incremental TDD IS best practice. |
| "Let me plan all test cases first" | Planning ≠ writing. Write ONE, discover next. |
| "It's urgent, batch for speed" | Incremental is FASTER. Prevents over-engineering. |
| "This is simple, I know what I need" | You think you know. Write ONE, you'll learn. |
| "I'll write 3-4 main scenarios" | That's batch testing. Write ONE. |
| "Run single test for speed, full suite later" | Regressions happen NOW. Always run all tests. |
| "Production urgent, skip full test run" | Breaking more under pressure makes it worse. Run all tests. |

**Seeing yourself in this table? Write ONE test. Stop rationalizing.**

## Red Flags - You're Doing Batch TDD

**STOP if you:**
- Write more than one FAILING `test()` / `it()` block before implementing
- Think "let me cover the main scenarios" and write them all
- Plan out all test cases AND write them all at once
- Write multiple failing tests numbered test1, test2, test3
- **Jump straight from compile error to full implementation** (skipping stage 2 RED)
- Think "I'll just implement it all at once since I know what it needs"

**All of these mean: Keep only ONE failing test. Comment out or delete the rest. Make it pass. Then uncomment/write the next one.**

**For two-stage RED:** Add stub first, see behavior failure, THEN implement.

## Integration with RED-GREEN-REFACTOR

This skill enforces the incremental nature of RED-GREEN-REFACTOR:

1. **RED**: Write ONE failing test
2. **GREEN**: Minimal code to pass THAT test
3. **REFACTOR**: Clean up if needed
4. **Repeat**: Write NEXT test

You cannot skip step 2 (implementing) by writing multiple tests in step 1.

## The Bottom Line

**TDD means ONE test at a time.**

Not "tests first, then code." Not "batch of tests, then batch of code."

One test → Implementation → Next test.

That's the cycle. Follow it.
