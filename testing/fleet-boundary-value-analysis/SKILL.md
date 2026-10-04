---
name: fleet-boundary-value-analysis
description: Deep QA skill for boundary value analysis — systematic identification of edge cases, off-by-one traps, state transitions, and the inputs that break assumptions
user-invocable: false
---

# Boundary Value Analysis

## The Principle

Bugs cluster at boundaries. The code that handles 5 items works fine.
The code that handles 0, 1, MAX, MAX+1, and -1 is where things break.

Every input has a range. Every range has edges. Every edge is a test.

## The Method

### Step 1: Identify Input Domains

For each function, endpoint, or component:
- What are the inputs? (parameters, config values, external data)
- What are the expected ranges? (0-100, non-empty string, valid task_id)
- What types are expected? (int, string, list, None)

### Step 2: Map Boundaries

For each input, identify:

| Boundary | Values to Test |
|----------|---------------|
| Minimum | min, min-1 |
| Just above minimum | min+1 |
| Nominal | typical value |
| Just below maximum | max-1 |
| Maximum | max, max+1 |
| Zero / Empty | 0, "", [], None |
| Type boundary | int vs float, str vs bytes |

### Step 3: Apply to Fleet Concepts

| Fleet Domain | Boundary Tests |
|-------------|---------------|
| task_readiness | 0, 1, 49, 50, 89, 90, 99, 100, 101, -1 |
| story_points | 0, 1, 2, 3, 5, 8, 13, 14, -1, None |
| heartbeat_interval | 0, 1, minimum, typical, very large |
| agent_name | valid, empty, None, unknown agent, special chars |
| task_stage | each valid stage, invalid stage, None |
| delivery_phase | each valid phase, invalid phase, None |
| contribution count | 0, 1, all required, extra, duplicate |
| blocker count | 0, 1, 2, 3 (above PM threshold) |
| sprint capacity | 0, under, exact, over |

### Step 4: State Transition Boundaries

Not just input values — state transitions have boundaries too:

| Transition | Test |
|-----------|------|
| inbox → accepted | valid plan, empty plan, plan without verbatim reference |
| in_progress → review | with tests, without tests, partial tests |
| review → approved | with trail, without trail, partial trail |
| review → rejected | specific feedback, vague feedback, repeated rejection |
| readiness 89 → 90 | gate request triggered? ntfy sent? |
| readiness 49 → 50 | checkpoint notification? |

### Step 5: Combination Boundaries

Single boundaries are necessary but insufficient. Combine:
- Empty list AND null parent → what happens?
- Max readiness AND missing contributions → can it advance?
- Budget exhausted AND task dispatched → should it continue?

## Test Naming Convention

Use TC-XXX format with descriptive names:

```
TC-001: readiness_at_zero_blocks_dispatch
TC-002: readiness_at_90_triggers_gate_request
TC-003: empty_plan_rejects_acceptance
TC-004: missing_contribution_prevents_work_stage
TC-005: third_blocker_escalates_to_po
```

## Mapping to Pytest

```python
@pytest.mark.parametrize("readiness,expected", [
    (0, "blocked"),
    (1, "conversation"),
    (49, "conversation"),
    (50, "checkpoint"),
    (89, "investigation"),
    (90, "gate_request"),
    (99, "ready_for_work"),
    (100, "ready_for_work"),
    (-1, "invalid"),
    (101, "invalid"),
    (None, "invalid"),
])
def test_readiness_boundaries(readiness, expected):
    ...
```

## Output: Test Definition Contribution

When producing TC-XXX for a story:

```
## Test Definition: {task_title}

### Domain Analysis
- Inputs: {list with types and ranges}
- State transitions: {list}
- External boundaries: {API limits, config bounds}

### Test Cases
TC-001: {name}
  Input: {specific values}
  Expected: {specific outcome}
  Boundary: {which boundary this tests}
  Priority: {must-have | should-have | nice-to-have}

TC-002: ...

### Coverage Matrix
| Input | Min | Min+1 | Nominal | Max-1 | Max | Over | None |
|-------|-----|-------|---------|-------|-----|------|------|
| {field} | TC-X | TC-X | TC-X | TC-X | TC-X | TC-X | TC-X |
```
