---
name: forge-tdd
description: Enforces test-driven development workflow for Claude Code. Implements Red-Green-Refactor cycle with configurable gates. Use when writing code, implementing features, or fixing bugs.
---

# Test-Driven Development Workflow

## The Cycle

```
┌─────────────────────────────────────────────────┐
│  RED → GREEN → REFACTOR → DOCUMENT → COMMIT    │
└─────────────────────────────────────────────────┘
```

### Phase 1: RED (Write Failing Test)

1. Understand the requirement
2. Write a test that describes expected behavior
3. Run the test - it MUST fail
4. If test passes, the test is wrong or feature exists

### Phase 2: GREEN (Minimal Implementation)

1. Write the minimum code to pass the test
2. Run the test - it MUST pass
3. Do not optimize, do not refactor yet

### Phase 3: REFACTOR (Improve)

1. Clean up the implementation
2. Run tests after each change
3. Tests must stay green throughout

### Phase 4: DOCUMENT (If Tests Pass)

1. Update docstrings/comments
2. Update README if public API changed
3. Only document after tests pass

### Phase 5: COMMIT

1. Stage changes
2. Write descriptive commit message
3. Tests must pass before commit

## Gate Enforcement

**Mode: {{TDD_GATE}}**

### Soft Gate (default)

- Warn if tests fail
- Allow proceeding with user acknowledgment
- Log warning in output

### Hard Gate

- Block all progress until tests pass
- No exceptions
- Must fix tests before any other action

## Validation

Run before committing:

```bash
~/.claude/skills/tdd/scripts/check-tests.sh
```

Check current gate status:

```bash
~/.claude/skills/tdd/scripts/gate-status.sh
```

## Checklist

Copy and track progress:

```
TDD Progress:
- [ ] Requirement understood
- [ ] Failing test written
- [ ] Test fails for right reason
- [ ] Minimal implementation done
- [ ] Test passes
- [ ] Code refactored
- [ ] All tests still pass
- [ ] Documentation updated
- [ ] Ready to commit
```
