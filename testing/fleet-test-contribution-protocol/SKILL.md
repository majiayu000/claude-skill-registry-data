---
name: fleet-test-contribution-protocol
description: The structured protocol for producing qa_test_definition contributions — TC-XXX format, phase-appropriate criteria depth, delivery via fleet_contribute that feeds the entire predefinition-validation cycle.
---

# Test Contribution Protocol — QA's Structured Output

Your qa_test_definition is the FOUNDATION of the test cycle. Engineers implement against your criteria. Fleet-ops validates against them. Accountability checks they were followed. If your output is vague, the entire downstream chain degrades.

## The TC-XXX Format

Every criterion gets a unique ID:

```
TC-001: {what must be true} | {type} | {priority}
```

| Field | Values | Purpose |
|-------|--------|---------|
| ID | TC-001, TC-002, ... | Unique reference for validation |
| Description | Specific, verifiable statement | What the engineer must satisfy |
| Type | unit / integration / e2e | How to test it |
| Priority | required / recommended | Must-have vs nice-to-have |

## The Full Contribution Flow

### Step 1: Read Context

Call `qa_test_predefinition(task_id)` to get:
- Verbatim requirement
- Acceptance criteria (may be vague — that's why you're here)
- Architect's design_input (shapes what to test)
- Delivery phase (determines rigor)

### Step 2: Identify Test Scenarios

For each acceptance criterion, ask:
- **Happy path:** What happens when everything is correct?
- **Sad path:** What happens when input is wrong?
- **Boundary:** What happens at the edges (empty, max, zero, null)?
- **Error:** What happens when dependencies fail?
- **State:** What happens in different states (loading, partial, complete)?

Use `/fleet-boundary-value-analysis` for systematic edge case identification.

### Step 3: Write Criteria (Phase-Appropriate)

**POC (minimal):**
```
TC-001: Feature works for valid input | unit | required
```

**MVP (main flows + edges):**
```
TC-001: Returns 200 for valid input with all required fields | unit | required
TC-002: Returns 400 for missing required field 'title' | unit | required
TC-003: Returns 400 for missing required field 'agent_name' | unit | required
TC-004: Handles concurrent requests without data corruption | integration | recommended
TC-005: Returns 401 for unauthenticated request | unit | required
```

**Staging/Production (comprehensive):**
```
TC-001: Returns 200 for valid input | unit | required
TC-002: Returns 400 for each missing required field (title, agent_name, task_type) | unit | required
TC-003: Returns 400 for invalid field values (SP > 13, unknown task_type) | unit | required
TC-004: Returns 401 for expired token | unit | required
TC-005: Returns 403 for unauthorized agent | unit | required
TC-006: Handles 100 concurrent requests without data loss | integration | required
TC-007: Response time < 200ms at p95 for single requests | integration | recommended
TC-008: Gracefully handles MC backend timeout (3s) | integration | required
TC-009: Event chain fires correctly (board memory + IRC) | integration | required
TC-010: Plane sync occurs after creation (when connected) | e2e | recommended
```

### Step 4: Deliver

```
fleet_contribute(
    task_id=TARGET_TASK_ID,
    contribution_type="qa_test_definition",
    content="""
    ## QA Test Definition for: {task_title}
    
    Phase: {delivery_phase}
    Based on: verbatim requirement + architect design_input
    
    TC-001: Returns 200 for valid input with all required fields | unit | required
    TC-002: Returns 400 for missing required field 'title' | unit | required
    TC-003: Returns 400 for missing required field 'agent_name' | unit | required
    TC-004: Handles concurrent requests without data corruption | integration | recommended
    TC-005: Returns 401 for unauthenticated request | unit | required
    
    Total: 5 criteria (4 required, 1 recommended)
    """
)
```

## What Makes a Good TC-XXX

| Quality | Good | Bad |
|---------|------|-----|
| Specific | "Returns 400 for missing 'title' field" | "Handles bad input" |
| Verifiable | "Response time < 200ms at p95" | "Fast enough" |
| Independent | Each TC can be tested alone | TC-003 depends on TC-001 passing |
| Traceable | Maps to a specific acceptance criterion | General quality aspiration |
| Type-appropriate | Unit for logic, integration for flow, e2e for full path | Everything as e2e |

## The Downstream Impact

Your TC-XXX criteria flow through 4 systems:

1. **Engineer context:** TC-XXX appears in their task context during work stage. Each is a REQUIREMENT.
2. **Fleet-ops review:** Reviewer checks TC-XXX coverage. Missing criteria = rejection risk.
3. **QA validation:** You validate each TC-XXX during review: MET or NOT MET with evidence.
4. **Accountability compliance:** Pattern detection checks if predefinition happened before work.

If you skip predefinition or produce vague criteria, all 4 downstream systems degrade. Your contribution is the foundation.

## The Hook Check

The PreToolUse hook on `fleet_contribute` warns if `qa_test_definition` doesn't contain "TC-" format. This is structural enforcement — the fleet expects structured criteria, not prose.
