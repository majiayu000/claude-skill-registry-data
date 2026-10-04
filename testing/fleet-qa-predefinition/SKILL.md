---
name: fleet-qa-predefinition
description: How QA thinks about test predefinition — structured TC-XXX criteria BEFORE implementation, phase-appropriate rigor, boundary value analysis
user-invocable: false
---

# QA Test Predefinition

## The Fundamental Shift

QA contributes BEFORE implementation, not just after. Test criteria become
REQUIREMENTS that the implementing agent must satisfy. When the task reaches
review, QA validates against what they specified, not what they discover.

## When This Applies

The brain creates a `qa_test_definition` contribution task when a story/epic
enters REASONING stage. You produce test criteria and deliver them via
`fleet_contribute` so the engineer sees them in context during WORK stage.

## Step 1: Read the Target Task

Call `qa_test_predefinition(task_id)` — your group call that gathers:
- Verbatim requirement
- Acceptance criteria
- Architect's design input (if available)
- Delivery phase (determines rigor)

## Step 2: Think Like a Pessimist

For EACH piece of functionality in the requirement:

### Happy Path
What SHOULD happen with valid input?
- Input X → Output Y
- User does A → System responds with B

### Sad Paths (where things go wrong)
- What if required input is missing?
- What if input is malformed?
- What if input is the wrong type?
- What if the dependency is unavailable?
- What if the operation times out?

### Boundary Values
- Empty string, null, zero, negative
- Maximum length, maximum value
- Just inside the boundary, just outside
- Unicode, special characters, injection patterns

### State-Based
- What if called twice?
- What if called before prerequisite?
- What if called after cleanup?
- What if concurrent calls?

### Integration Points
- What happens at each system boundary?
- What if the external service returns an error?
- What if the response format changes?

## Step 3: Phase-Appropriate Rigor

**DO NOT over-test POC. DO NOT under-test production.**

| Phase | What to Test | What to Skip |
|-------|-------------|-------------|
| poc | Happy path only. "Does the core concept work?" | Edge cases, error handling, performance |
| mvp | Main flows + critical edges. "Can a real user use this?" | Load testing, resilience, exhaustive edges |
| staging | Comprehensive: unit + integration + load. "Is this reliable?" | Chaos engineering, pen-testing |
| production | Everything. "Can this survive real-world use?" | Nothing — full coverage required |

## Step 4: Write Structured TC-XXX Criteria

Each criterion must be:
- **Specific** — not "it works correctly"
- **Checkable** — you can write a test for it
- **Measurable** — pass/fail, not "good enough"

### Format

```
TC-001: [description]
  Type: unit | integration | e2e
  Priority: required | recommended
  Input: [what triggers this test]
  Expected: [what should happen]
  Verification: [how to check — specific file, function, command]

TC-002: ...
```

### Examples

**Bad:**
- "The API should work" (not specific)
- "Handle errors gracefully" (not checkable)
- "Good performance" (not measurable)

**Good:**
- TC-001: POST /api/tasks returns 201 with valid payload
  Type: integration | Priority: required
  Input: `{"title": "Test", "type": "task"}`
  Expected: 201 status, response body has `id` field
  Verification: pytest fleet/tests/api/test_tasks.py::test_create_valid

- TC-002: POST /api/tasks returns 400 when title is missing
  Type: integration | Priority: required
  Input: `{"type": "task"}` (no title)
  Expected: 400 status, error message mentions "title"
  Verification: pytest fleet/tests/api/test_tasks.py::test_create_missing_title

- TC-003: POST /api/tasks returns 401 without auth token
  Type: integration | Priority: required
  Input: Valid payload, no Authorization header
  Expected: 401 status
  Verification: pytest fleet/tests/api/test_tasks.py::test_create_no_auth

## Step 5: Deliver

```
fleet_contribute(
  task_id=TARGET_TASK_ID,
  contribution_type="qa_test_definition",
  content=YOUR_TC_XXX_CRITERIA
)
```

## Step 6: During Review — Validate

When the task enters review, call `qa_test_validation(task_id)`.
For EACH TC-XXX you defined:
- **MET**: point to specific code/test that addresses it
- **NOT MET**: describe what's missing, flag to fleet-ops

The validation is against YOUR criteria, not your post-hoc impression.
