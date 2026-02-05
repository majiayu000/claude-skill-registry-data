---
name: TDD Methodology
description: This skill should be used when the user asks to "write tests first", "use TDD", "test-driven development", "red green refactor", "test first", "add unit tests before code", "write regression test first", "safe refactor with tests", or when TDD mode is active and the user makes any coding request that affects behavior (features, bugs, refactors).
version: 0.1.0
---

# TDD Methodology

Transform coding behavior into strict Test-Driven Development practice. Enforce the Red→Green→Refactor cycle where no behavior-changing code is written without a failing test first.

## Core Philosophy

TDD is not about testing—it is about **design through tests**. Tests drive the implementation, not the other way around.

### The Iron Rules

1. **No production code without a failing test** - Write a test that fails for the right reason before writing any implementation
2. **Minimal code to pass** - Write only enough code to make the failing test pass, nothing more
3. **Refactor only when green** - Clean up code only after all tests pass
4. **Small increments** - Each cycle should be minutes, not hours

### The Red→Green→Refactor Loop

```
┌─────────────────────────────────────────────────┐
│                                                 │
│   RED: Write a failing test                     │
│   ↓                                             │
│   GREEN: Write minimal code to pass             │
│   ↓                                             │
│   REFACTOR: Clean up while staying green        │
│   ↓                                             │
│   (repeat)                                      │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Strictness Modes

### Strict Mode (Default)

Block any behavior-changing implementation without a failing test:
- Refuse to write/edit source files until a failing test exists
- Enforce test-first for every behavior change
- No exceptions without explicit user override

### Standard Mode

Warn and prompt for confirmation:
- Alert when attempting to write code without a failing test
- Ask: "No failing test exists. Proceed anyway? (yes/no)"
- Log violations for awareness

### Relaxed Mode

Coach and suggest without blocking:
- Recommend writing tests first
- Provide guidance on TDD approach
- Allow user to proceed without tests

## TDD Workflow Execution

### Phase 1: RED - Write Failing Test

1. **Understand the requirement** - Clarify what behavior is needed
2. **Identify test location** - Find or create appropriate test file
3. **Write the test first**:
   - Describe expected behavior clearly in test name
   - Use Arrange-Act-Assert pattern
   - Test should fail because the feature doesn't exist yet
4. **Run tests** - Confirm test fails for the right reason (not syntax error)
5. **Verify failure message** - Ensure it clearly indicates missing behavior

### Phase 2: GREEN - Minimal Implementation

1. **Write the simplest code that passes** - Resist over-engineering
2. **Focus on making the test green** - Nothing more
3. **Run tests** - Confirm the new test passes
4. **Check for regressions** - All existing tests must still pass

### Phase 3: REFACTOR - Clean Up

Only proceed to refactor when all tests are green.

1. **Identify code smells** - Duplication, unclear names, long methods
2. **Make incremental changes** - One refactoring at a time
3. **Run tests after each change** - Stay green throughout
4. **Stop when code is clean** - Don't gold-plate

## Test Output Interpretation

Present test results with progressive detail:

### Summary View (Default)

```
Tests: 12 passed, 3 failed (score: 0.80)
Failing:
  - test_user_can_login
  - test_validates_email_format
  - test_handles_empty_input
```

### Full Output (On Request)

Provide complete test runner output when user asks "show full output" or when debugging complex failures.

## Iteration Management

### Cycle Limits

Default: 5 Red→Green iterations per request.

After 5 cycles without success:
1. Summarize what was attempted
2. Show current test failures
3. Ask: "Continue with 5 more iterations? (Yes/No)"

### When to Stop Iterating

- All tests pass (success)
- User requests stop
- Iteration limit reached and user declines continuation
- Fundamental blocker identified (missing dependency, unclear requirement)

## Framework-Specific Patterns

### Jest/Vitest (JavaScript/TypeScript)

Test file naming: `*.test.ts`, `*.spec.ts`, `__tests__/*.ts`

```typescript
// RED: Write failing test first
describe('Calculator', () => {
  it('should add two numbers', () => {
    const calc = new Calculator();
    expect(calc.add(2, 3)).toBe(5);
  });
});
```

Run command detection: Check `package.json` for `test` script.

### Pytest (Python)

Test file naming: `test_*.py`, `*_test.py`, `tests/`

```python
# RED: Write failing test first
def test_user_can_register():
    user = User.register("test@example.com", "password123")
    assert user.email == "test@example.com"
    assert user.is_active is True
```

Run command detection: Check for `pytest.ini`, `pyproject.toml`, or `setup.cfg`.

### Generic Fallback

For other frameworks (Go, JUnit, etc.):
1. Detect test command from project files
2. Use standard naming conventions
3. Apply same Red→Green→Refactor loop

## Source vs Test File Detection

### Source Patterns (Hook Enforcement Applies)

Default patterns for files where hook blocks/warns:
- `src/**/*.ts`, `src/**/*.tsx`, `src/**/*.js`
- `app/**/*.py`, `lib/**/*.py`
- `*.go` (excluding `*_test.go`)

### Test Patterns (Excluded from Hook)

Files where writing is always allowed:
- `**/*.test.*`, `**/*.spec.*`
- `**/__tests__/**`
- `tests/**`, `test/**`
- `*_test.go`, `*_test.py`

## Settings Reference

Read settings from `.claude/tdd-dev.local.md`:

```yaml
testCommand: npm test
strictness: strict
maxIterations: 5
sourcePatterns:
  - src/**/*.ts
testPatterns:
  - **/*.test.*
```

Merge order: Global (`~/.claude/tdd-dev.local.md`) → Project → Command flags

## Additional Resources

### Reference Files

For detailed patterns and advanced workflows:
- **`references/patterns.md`** - Common TDD patterns and anti-patterns
- **`references/frameworks.md`** - Framework-specific test templates and commands

### Example Files

Working examples in `examples/`:
- **`examples/jest-tdd-cycle.md`** - Complete Jest TDD cycle walkthrough
- **`examples/pytest-tdd-cycle.md`** - Complete Pytest TDD cycle walkthrough

## Quick Reference

| Phase | Action | Validation |
|-------|--------|------------|
| RED | Write failing test | Test fails for correct reason |
| GREEN | Minimal implementation | New test passes, no regressions |
| REFACTOR | Clean up code | All tests still pass |

| Mode | On Violation |
|------|--------------|
| Strict | Block write |
| Standard | Prompt confirmation |
| Relaxed | Show warning |
