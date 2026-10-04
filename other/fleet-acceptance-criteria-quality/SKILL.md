---
name: fleet-acceptance-criteria-quality
description: How QA evaluates whether task acceptance criteria are testable — catching vague, unmeasurable, or untestable criteria before they become bad predefinitions. Maps to qa_acceptance_criteria_review group call.
---

# Acceptance Criteria Quality — QA's Upstream Filter

Bad acceptance criteria become bad test predefinitions become bad implementations become rejections. You catch them EARLY — before anyone wastes cycles on untestable requirements.

## When to Check

- **Heartbeat:** Review inbox tasks for criteria quality (CLAUDE.md step: "review inbox tasks")
- **Before predefinition:** Before producing TC-XXX criteria, verify the source is testable
- **When PM asks:** PM flags vague criteria for your assessment

Use `qa_acceptance_criteria_review(task_id)` to get the task's description and a testability checklist.

## The 3 Testability Tests

Every acceptance criterion must pass ALL three:

### 1. SPECIFIC — Does it say exactly what?

| Untestable | Testable |
|-----------|---------|
| "It works correctly" | "Returns 200 for valid input with all required fields" |
| "Good performance" | "Response time < 200ms at p95 for 100 concurrent users" |
| "Secure authentication" | "JWT tokens expire after 1h, refresh tokens after 7d" |
| "User-friendly" | "Error messages include: what failed, error code, suggested action" |

**The test:** Can you write a function that returns true/false for this criterion? If not, it's not specific.

### 2. CHECKABLE — Can you verify it with evidence?

| Uncheckable | Checkable |
|------------|----------|
| "Follows best practices" | "Uses conventional commit format: type(scope): description [task:XXXXXXXX]" |
| "Clean code" | "All functions < 50 lines, all modules < 500 lines, no circular imports" |
| "Well documented" | "README has: purpose, quickstart, configuration, usage, troubleshooting sections" |

**The test:** Can you point to a test file, a metric, or a specific artifact that proves this criterion is met? If not, it's not checkable.

### 3. MEASURABLE — Is there a threshold?

| Unmeasurable | Measurable |
|-------------|-----------|
| "Fast enough" | "< 200ms p95" |
| "High availability" | "99.9% uptime over 30 days" |
| "Good test coverage" | "> 80% line coverage for fleet/core/" |
| "Few bugs" | "Zero critical bugs, < 3 medium bugs per sprint" |

**The test:** Is there a number or boolean that tells you pass/fail? If not, it's not measurable.

## What to Do with Bad Criteria

### Option 1: Suggest Improvements

Post a comment on the task with specific rewrites:

```
fleet_chat(
    "Task X acceptance criteria need revision for testability:\n"
    "- 'It works correctly' → 'Returns 200 for valid input, 400 for missing fields, 401 for unauthenticated'\n"  
    "- 'Good performance' → 'Response time < 500ms at p95 for 50 concurrent requests'\n"
    "- 'Secure' → 'All endpoints require JWT, tokens expire after 1h'",
    mention="project-manager"
)
```

### Option 2: Flag to PM

If criteria are too vague to even suggest improvements:

```
fleet_chat(
    "Task X has no testable acceptance criteria. "
    "Cannot produce meaningful test predefinition without them. "
    "Please add specific, checkable, measurable criteria.",
    mention="project-manager"
)
```

### Option 3: Define Criteria Yourself

If the task is clear but criteria are just missing (PM didn't write them), and you understand the requirement well enough:

1. Read the verbatim requirement
2. Read the architect's design_input (if available)
3. Derive testable criteria from the requirement
4. Post as a suggestion for PM to confirm before you predefine tests

## The Connection to Test Predefinition

Good criteria → good TC-XXX predefinitions → good implementation → good validation:

```
Criterion: "Returns 400 for missing required fields"
  ↓
TC-001: POST /api/tasks with empty body returns 400 | unit | required
TC-002: POST /api/tasks without title returns 400 with error.field="title" | unit | required
TC-003: POST /api/tasks without agent_name returns 400 with error.field="agent_name" | unit | required
  ↓
Engineer implements validation for each field
  ↓
QA validates: TC-001 ✓ (test_api.py:42), TC-002 ✓ (test_api.py:55), TC-003 ✓ (test_api.py:68)
```

The quality of the FIRST step (criteria) determines the quality of every subsequent step.

## Phase-Appropriate Criteria Depth

| Phase | Criteria Expectation |
|-------|---------------------|
| poc | "Feature exists and works for the happy path" — minimal is OK |
| mvp | Specific criteria for main flows + critical edge cases |
| staging | Comprehensive criteria covering all flows, errors, performance |
| production | Everything above + resilience, security controls, operational concerns |

Don't demand production-grade criteria for a POC. But also don't accept "it works" for production.
