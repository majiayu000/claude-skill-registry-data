---
name: implementing-stories
description: Implement using TDD Red-Green cycle. Focus on Red-Green only; refactoring is separate step.
---

# Implementing Stories (Red-Green)

Implement using TDD Red-Green cycle. Refactoring happens separately with fresh context.

## Context

Find story log, understand codebase, identify what to implement.

## Principles

- Small steps: one behavior at a time
- Test-driven: write test first
- Red-Green focus: get tests passing, skip cleanup

## TDD Cycle

### Red: Write Failing Test

- [ ] Write test defining behavior
- [ ] Scaffold symbols (avoid "not found")
- [ ] Confirm fails for right reason

**Key**: Fails because feature missing, not syntax error.

### Green: Make It Pass

- [ ] Implement minimum to pass
- [ ] No extras or cleanup
- [ ] Confirm passes

Don't worry about quality/duplication. Refactoring is next phase.

## Map Criteria

For each criterion:
1. Identify behavior
2. Write test (Given-When-Then)
3. Implement minimum
4. Next criterion (skip refactoring)

## Update Story Log (REQUIRED)

**CRITICAL**: Must update before finishing.

```markdown
### Implementation (Red-Green)

**Status: Complete - Ready for Refactor**

**Implemented:**
- [Criterion]: [Approach]

**Decisions:**
- [Decision]: [Why]

**Tests:**
- [Test file]: [What tests]
- Status: All passing (X)

**Technical debt:**
- [Item]: Duplication needing refactor
- [Item]: Naming improvements

**Next:** Refactor
```

Steps:
1. Find story log (docs/stories/**/*.story.md)
2. Update "Completed Work Summary"
3. Save and verify

## When to Stop

- All criteria have passing tests
- All tests pass
- No syntax/type errors
- **Story log updated**

**Only after story log updated**, pass to Refactor.

## Pitfalls

- Skipping tests
- Big steps
- Premature cleanup (resist refactoring)
- Ignoring error handling
- Over-implementation
