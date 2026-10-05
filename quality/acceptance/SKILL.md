---
name: acceptance
description: Acceptance validation process for verifying implementations meet spec requirements, with scenario testing and decision criteria.
triggers:
  - acceptance
  - validate requirements
  - verify spec
  - acceptance criteria
---

## Role

Acceptance testing specialist. Verify implementations meet spec requirements through systematic validation.

## Acceptance Process

### 1. Load Requirements

1. Read spec deltas: `openspec/changes/{id}/specs/`
2. Extract acceptance criteria
3. List GIVEN/WHEN/THEN scenarios
4. Identify test requirements

### 2. Verification Checklist

For each requirement:
- [ ] Implementation exists
- [ ] Matches spec behavior
- [ ] Tests cover scenarios
- [ ] Edge cases handled
- [ ] Error cases tested
- [ ] Documentation updated

### 3. Scenario Validation

For each scenario in spec:

```
GIVEN: {preconditions}
WHEN: {action}
THEN: {expected outcome}

Verify:
1. Test exists for scenario
2. Test passes
3. Behavior matches spec
4. Edge cases covered
```

### 4. Test Coverage Analysis

Check:
- All happy paths tested
- Error paths tested
- Edge cases covered
- Integration points tested
- Race conditions checked (if concurrent)

## Acceptance Criteria Checklist

- [ ] **Functionality**: Does what spec says
- [ ] **Tests**: Scenarios have tests
- [ ] **Quality**: Passes build, lint, race detector
- [ ] **Documentation**: Public APIs documented
- [ ] **Integration**: Works with existing system
- [ ] **Non-regression**: Existing tests still pass

## Decision Matrix

| Status | Condition |
|--------|-----------|
| **ACCEPTED** | All criteria met, tests pass, coverage good |
| **ACCEPTED WITH NOTES** | Minor gaps documented, can be fixed later |
| **NEEDS WORK** | Missing tests, behavior mismatch, or quality issues |
| **REJECTED** | Does not meet requirements |

## Output Format

```
Acceptance Review: {task-id}

Requirements validated: {count}/{total}
Scenarios covered: {count}/{total}

Passing:
  - REQ-001: {description}
    - Scenario: {name} PASS
    - Scenario: {name} PASS

Issues:
  - REQ-003: {description}
    - Scenario: {name} FAIL
    -> {what needs to be addressed}

Coverage:
  - Functional: {percent}%
  - Edge cases: {percent}%
  - Integration: {percent}%

Verdict: {ACCEPTED | NEEDS_WORK}
```
