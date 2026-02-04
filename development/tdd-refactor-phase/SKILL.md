---
name: tdd-refactor-phase
description: Guide experienced developers through REFACTOR phase of TDD cycle - improving code quality while maintaining green tests
license: Complete terms in LICENSE.txt
---

# TDD REFACTOR Phase
**Version:** 0.19.0
**Source:** Skills/tdd-refactor-phase/SKILL.md

Guide through REFACTOR phase: improving code quality while keeping tests green.

## When to Use
- GREEN phase complete with passing test
- Proceeding autonomously after GREEN phase
- Code works but could be improved

## Objectives
1. **Improve code quality** - Cleaner, more maintainable
2. **Keep tests green** - No behavior changes

**Refactoring IS:** Improving structure without changing behavior
**Refactoring IS NOT:** Adding features, fixing bugs, breaking tests

## Workflow

**Step 1: Analyze Opportunities**
ASSISTANT instructs: "Ask Claude Code: Analyze this code for refactoring opportunities"
Identify: Duplication, long functions, unclear names, complex logic

**Step 2: Evaluate Suggestions**
- **Refactor Now:** Clear improvement, low risk, high value
- **Skip:** Premature abstraction, high risk, over-engineering

**Step 3: Apply Refactoring (Single Code Block)**
```
TASK: [Description]
STEP 1: Open implementation file
STEP 2: Navigate to code
STEP 3: Apply refactored code
STEP 4: Explanation of improvements
STEP 5: Save file
STEP 6: Run full test suite
STEP 7: Verify ALL tests still PASS
STEP 8: Report: All tests green?
```

**Step 4: Verify Tests Remain Green**
- Run FULL test suite
- ALL tests must pass
- **If any fail → ROLLBACK immediately**

**Step 5: Complete**
- Refactoring applied + tests green → Continue with next behavior or Story-Complete
- Refactoring skipped → Continue with next behavior or Story-Complete

## Best Practices
1. Refactor in small steps (test after each)
2. One refactoring at a time
3. **Keep tests green** (rollback if broken)
4. Refactor for clarity, not cleverness

## Common Refactorings
- Extract Variable/Function
- Rename for Clarity
- Eliminate Duplication
- Simplify Conditional Logic

## When to Skip
- Only one use of code (Rule of Three)
- Code already clear
- High risk, low value
- Premature abstraction

## Anti-Patterns
- Refactoring without tests
- Accepting broken tests
- Big bang refactoring
- Mixing refactor + features

## Checklist
- [ ] Claude Code analyzed code
- [ ] ASSISTANT evaluated suggestions
- [ ] If applied: All tests PASS
- [ ] If skipped: Valid reason documented
- [ ] Ready to continue with next behavior or Story-Complete

---

**End of TDD REFACTOR Phase Skill**
