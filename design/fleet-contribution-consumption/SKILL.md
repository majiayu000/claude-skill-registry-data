---
name: fleet-contribution-consumption
description: How engineers consume contributions from architect, QA, DevSecOps, and UX — treating colleague inputs as requirements, not suggestions.
---

# Contribution Consumption — Engineer's Primary Workflow

You don't work alone. Before you write a single line of code, other agents have provided structured inputs that shape your implementation. These are NOT suggestions. They are REQUIREMENTS.

## What You Receive and From Whom

The synergy matrix (config/synergy-matrix.yaml) defines what you receive:

| From | Type | Priority | What It Contains |
|------|------|----------|-----------------|
| Architect | design_input | REQUIRED (stories/epics) | Patterns, target files, approach, constraints, rationale |
| QA | qa_test_definition | REQUIRED (stories/epics) | TC-XXX criteria: what to test, how, expected results |
| DevSecOps | security_requirement | CONDITIONAL | Specific controls: auth method, input validation, secrets handling |
| UX | ux_spec | CONDITIONAL | States, interactions, accessibility, component patterns |

## The Consumption Workflow

### Step 1: Call eng_contribution_check FIRST

Before ANY work, call your role-specific group call:

```
eng_contribution_check()  # or eng_contribution_check(task_id="...")
```

This reads your task's comments for typed contributions, checks the synergy matrix for what's required, and tells you:
- What's been received (with summaries)
- What's missing (with `fleet_request_input` commands)
- Whether you're ready for work

If contributions are missing and your task is a story or epic, DO NOT START WORK. Call `fleet_request_input` to request the missing inputs.

### Step 2: Read Each Contribution as a Requirement

Contributions appear as typed comments on your task:
```
**Contribution (design_input)** from architect:
Use adapter pattern for external API calls. Target files:
fleet/infra/api_client.py (new), fleet/core/models.py (extend).
Rationale: isolates external dependency, allows mocking in tests.
```

This is NOT optional advice. The architect has designed the approach. You implement it. If you disagree, raise it via `fleet_chat(mention="architect")` — do not silently deviate.

### Step 3: Map QA Criteria to Implementation Steps

QA's test definition provides specific criteria:
```
TC-001: API client returns parsed response for valid input | unit | required
TC-002: API client raises specific exception for 4xx errors | unit | required
TC-003: Adapter handles timeout gracefully (3s default) | integration | required
```

Each TC-XXX becomes a checkpoint in your implementation:
- Write the code that satisfies TC-001
- Write the test that verifies TC-001
- Move to TC-002

Do NOT add criteria beyond what QA defined. If you discover additional test scenarios during implementation, call `fleet_task_create(agent_name="qa-engineer")` to let QA define them properly.

### Step 4: Follow Security Requirements Absolutely

DevSecOps provides specific, actionable controls:
```
**Contribution (security_requirement)** from devsecops-expert:
- Use JWT with RS256 (not HS256) for token verification
- Pin all GitHub Actions to SHA (not @latest)
- Input validation: reject requests > 1MB, validate content-type
- No credentials in environment variables — use secrets manager
```

These are non-negotiable. If a security requirement conflicts with the design input, escalate to both architect and devsecops via `fleet_escalate`.

### Step 5: Apply UX Spec to All User-Facing Surfaces

UX spec covers more than UI:
```
**Contribution (ux_spec)** from ux-designer:
CLI output: structured with clear sections, no raw JSON
Error messages: include what went wrong, what to do, error code
Config: validate on load, report all errors (not just first)
```

## What Happens If You Ignore Contributions

1. `fleet_task_complete` fires → creates approval for fleet-ops
2. Fleet-ops runs `ops_real_review` → checks contributions were consumed
3. Review finds: "design_input says adapter pattern, implementation uses direct calls"
4. Fleet-ops rejects → readiness regresses to 80% → stage regresses to reasoning
5. You get a fix task with specific feedback about what was missed
6. Doctor may flag this as a pattern if it repeats

The contribution system is not bureaucracy. It's how 10 agents coordinate without meetings.

## When Contributions Are NOT Required

Some task types skip contributions entirely (subtask, blocker, concern, spike). For these, `eng_contribution_check` will show `all_received: true` immediately.

For tasks and simple stories where no contributions arrived but the task is in work stage, the PM has already determined this task doesn't need them. Proceed with work.
