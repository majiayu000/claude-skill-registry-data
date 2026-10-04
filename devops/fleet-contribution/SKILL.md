---
name: fleet-contribution
description: How to produce and consume contributions via the synergy system — required inputs before work, structured output format
user-invocable: false
---

# Fleet Contribution Skill

## The Synergy System

Before a task enters WORK stage, contributors provide input. These are
REQUIREMENTS, not suggestions. The brain blocks dispatch without them.

Source of truth: `config/synergy-matrix.yaml`

## Who Contributes What to Whom

### To Software Engineer (story/epic)
| From | Type | Priority | What |
|------|------|----------|------|
| Architect | design_input | required | Architecture constraints, patterns, integration points |
| QA | qa_test_definition | required | Structured TC-XXX test criteria, edge cases |
| DevSecOps | security_requirement | conditional | Threat model, required controls (if security-relevant) |
| UX | ux_spec | conditional | Interaction states, accessibility (if user-facing) |

### To Architect (story/epic)
| From | Type | Priority | What |
|------|------|----------|------|
| Engineer | feasibility_assessment | recommended | Can we build this? Implementation constraints |
| DevSecOps | security_review | conditional | Architecture security assessment |

### To DevOps
| From | Type | Priority | What |
|------|------|----------|------|
| Architect | infrastructure_design | required | Deployment architecture, scaling strategy |
| DevSecOps | security_requirement | conditional | Infrastructure security requirements |
| Engineer | application_requirements | recommended | What the application needs from infrastructure |

## Phase-Dependent Requirements

| Delivery Phase | Required Contributions |
|----------------|----------------------|
| idea/conceptual | Architect only |
| poc | Architect only |
| mvp | Architect + QA + DevSecOps (if applicable) |
| staging | + Technical Writer |
| production | ALL applicable contributions required |

## Producing a Contribution

### Step 1: Call your role's contribution group call
- Architect: `arch_design_contribution(task_id)` — prepares context
- QA: `qa_test_predefinition(task_id)` — prepares TC-XXX context
- DevSecOps: `sec_contribution(task_id)` — prepares security context
- UX: `ux_spec_contribution(task_id)` — prepares UX context
- DevOps: `devops_deployment_contribution(task_id)` — prepares infra context
- Writer: `writer_doc_contribution(task_id)` — prepares doc context

### Step 2: Produce SPECIFIC content
**Bad:** "Be secure" / "Write good tests" / "Consider UX"
**Good:**
- "Use JWT with RS256 signing, not HS256. Pin GitHub Actions to SHA."
- "TC-001: Valid input returns 200 with expected shape. TC-002: Missing required field returns 400."
- "Loading state → skeleton, error state → retry button with message, empty state → CTA."

### Step 3: Deliver via fleet_contribute
```
fleet_contribute(
  task_id=TARGET_TASK_ID,
  contribution_type="design_input",  # or qa_test_definition, security_requirement, etc.
  content=YOUR_SPECIFIC_CONTENT
)
```

This posts a typed comment on the target task, embeds in the target agent's
context, checks completeness (all required received?), and notifies PM when complete.

## Consuming Contributions

### Step 1: Check what you have
Call `eng_contribution_check(task_id)` (engineer) or `pm_contribution_check(task_id)` (PM).

### Step 2: Read contributions in your context
Contributions appear as typed comments: `**Contribution (design_input)** from architect:`
They are also embedded in your task-context.md at dispatch time.

### Step 3: Treat them as REQUIREMENTS
- Architect's design_input → your implementation MUST follow these patterns
- QA's test_definition → your implementation MUST pass these TC-XXX criteria
- DevSecOps' security_requirement → your implementation MUST satisfy these controls

### Step 4: If required contributions are missing
```
fleet_request_input(task_id, from_role="architect", question="Need design input for auth middleware")
```
Do NOT proceed to work stage without required contributions.

## Trail

Every contribution action is recorded:
- `fleet_contribute` → trail event with contributor, type, target
- Completeness check → trail event with received/missing
- PM notification when all received → trail event
