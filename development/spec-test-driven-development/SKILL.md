---
name: spec-test-driven-development
description: Use when user requests new features or functionality. Defines complete workflow from specification through testing to implementation.
---

# Spec-TDD Development Workflow

When developing ANY new feature or functionality, follow this strict workflow:

## Workflow Steps

### 1. Write Specification FIRST (spec.md)
**Use the `specification` skill to write specifications following project conventions.**

The specification skill provides detailed guidelines for:
- Feature user story format (As a... I want... So that...)
- Requirements organization and naming (REQ-XXX-NNN)
- Requirement writing guidelines (atomic, testable, present tense)
- Scenario writing (Given/When/Then format)
- Proper spec structure and sections

After writing spec:
- Get user approval on spec before proceeding to tests

### 2. Write Tests SECOND (before implementation)
- Write tests based on the spec requirements
- One test per assertion (performance costs permitting)
- Test naming: `test_should_{expected_behavior}`
- Test files: `tests/test_{feature}/test_{module}.rs`

**When to write unit tests vs acceptance tests:**
- **Unit tests**: For isolated logic that doesn't require mocking
- **Acceptance tests**: For integration logic that requires mocking repositories, external services, or complex dependencies
- **Rule**: If a test requires mocking dependencies it should be an acceptance test instead
- Acceptance tests validate end-to-end behavior through actual API endpoints

### 3. Implement Code LAST
- Write minimal code to make tests pass
- Follow patterns from spec
- Reuse existing infrastructure where possible
- Update todo list as you work
- **CRITICAL: Update spec requirement markers as you complete each requirement**
  - After writing test: Mark test column with `U` (unit test) or `A` (acceptance test)
  - After implementing code: Mark code column with `X` (implemented)
  - Example: `[O][O]` → `[U][O]` (test written) → `[U][X]` (code implemented)

### 4. Run Tests to Verify Implementation
- **CRITICAL: After completing implementation, ALWAYS run the tests**
- All tests must pass before marking work as complete
- If tests fail, fix the implementation and re-run until all tests pass
- **DO NOT claim work is complete without running and passing tests**

**Use the `test-driven-development` skill for language-specific test running instructions:**
- The TDD skill contains detailed patterns for running tests
- For other languages: See corresponding files in `test-driven-development/{language}.md`

### 5. Run Pre-commit Hooks Before Completion
- **CRITICAL: After tests pass, ALWAYS run pre-commit hooks**
- Pre-commit hooks run linters, formatters, and static analysis tools
- Fix any issues raised by pre-commit hooks before marking work as complete
- **DO NOT claim work is complete without running and passing pre-commit hooks**

**Run pre-commit hooks:**
```bash
pre-commit run --all-files
```

## Commit Workflow

**Use the `write-commit-message` skill for git commit guidelines.**

## Do NOT Proceed Without

1. ❌ Do NOT write implementation code before spec
2. ❌ Do NOT write implementation code before tests
3. ❌ Do NOT skip writing tests
4. ❌ Do NOT write multiple assertions per test (unless justified)
5. ❌ Do NOT skip running tests after implementation
6. ❌ Do NOT skip running pre-commit hooks before completion
7. ✅ DO write spec → tests → implementation → run tests → run pre-commit in that order
8. ✅ DO get user approval on spec before proceeding
9. ✅ DO use TodoWrite to track progress
10. ✅ DO run tests and verify all pass
11. ✅ DO run pre-commit hooks and fix all issues