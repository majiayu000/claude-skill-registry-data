---
name: implementing-stories
description: Guides the implementation inner loop with TDD practices. Use when coding a feature, writing tests, following red-green-refactor cycle, or working through acceptance criteria incrementally.
---

# Implementing Stories

## Inner Loop Principles

- **Small steps**: One workflow, model, or behavior at a time
- **Reviewable**: Each change should be easy to understand and revert
- **Test-driven**: Write test first, then implementation

## TDD Cycle (Red-Green-Refactor)

### 1. Red: Write Failing Test

```
Task Progress:
- [ ] Write test that defines desired behavior
- [ ] Scaffold target symbols (empty bodies) to avoid "not found" errors
- [ ] Confirm test fails for the right reason
```

### 2. Green: Make It Pass

```
Task Progress:
- [ ] Implement minimum code to pass
- [ ] No extra features or cleanup yet
- [ ] Confirm test passes
```

### 3. Refactor: Clean Up

```
Task Progress:
- [ ] Improve code quality
- [ ] Keep tests green
- [ ] Remove duplication
```

## Mapping Acceptance Criteria to Implementation

For each acceptance criterion:

1. Identify the behavior to implement
2. Write a test that captures the Given-When-Then
3. Implement the minimum to pass
4. Refactor
5. Move to the next criterion

## Updating Story Log

As you work, update "Completed Work Summary":
- What was implemented
- Key design decisions made
- Test coverage added

## Common Pitfalls

- **Skipping tests**: Always write the test first
- **Big steps**: Break down if a change touches many files
- **Premature optimization**: Make it work, then make it right
- **Ignoring error cases**: Implement error handling from acceptance criteria
