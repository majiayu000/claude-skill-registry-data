---
name: tdd
description: Fire when creating or modifying test files. Enforces write-test-first discipline and correct framework selection per project layer.
user-invocable: false
paths:
  - "**/*.test.*"
  - "**/*.spec.*"
  - "**/*Test.*"
  - "**/*Spec.*"
  - "**/__tests__/**/*.{js,ts,jsx,tsx}"
---

# Explore-Plan-Act TDD Workflow

When implementing any feature or bugfix, follow the Explore → Plan → Act discipline.

## Process

### 1. EXPLORE — Investigate Before Coding
- **Read the codebase first** — use Grep, Read, and LS to understand the current state
- Trace the code path related to the change: entry points → dependencies → side effects
- Check `CLAUDE.md` and relevant `claude/*.md` docs for domain-specific patterns
- Identify existing tests in the area — understand what's already covered
- Look for similar implementations elsewhere in the codebase to follow conventions
- **Output:** Clear understanding of what exists, what patterns to follow, what constraints apply

### 2. PLAN — Design the Solution + Write Failing Tests
- Design the solution approach based on what you explored
- Document any assumptions or open questions
- Write failing tests that describe the expected behavior BEFORE implementation
- Each test should be specific and focused on one behavior
- Run the tests and confirm they fail for the right reason
- Consider edge cases: null/undefined, empty arrays, concurrent calls, boundary values
- **Output:** Failing tests that serve as a specification for the implementation

### 3. ACT — Implement with TDD Cycle
- Write the simplest code that makes the tests pass
- Do not add code that isn't required by a failing test
- Run the tests and confirm they pass
- **Refactor** while keeping tests green — clean up, extract patterns, improve naming
- Run all tests to ensure nothing breaks
- Repeat for each component or behavior
- **Output:** Working implementation with green tests

## Testing Conventions

### Framework per Layer
<!-- Populated by /bootstrap -->
- **Unit**: none (syntax-check)
- **Integration**: none (syntax-check)

### What to Test
- Every new branch/case in switch statements
- Every guard condition
- Every new field (cross-layer: DTO → backend → frontend)
- Edge cases: null/undefined, empty arrays, concurrent calls

### Code Style
- Follow project formatter rules
- Use descriptive test names: `it('should <behavior> when <condition>')`
- Follow existing test patterns in the service being modified

## ⚠️ Gotchas (Common Failure Points)

1. **Don't mix test frameworks** — check which framework the service uses before writing tests
2. **Stub keys must match actual exported function names** — a typo'd key silently does nothing
3. **Missing fixture properties cause silent failures** — always include ALL accessed properties
4. **Stubs without assertions are dead code** — every stub must have a corresponding assertion
5. **Redirect large test output** — `command > claude/tasks/out.txt 2>&1; echo "EXIT=$?"`

