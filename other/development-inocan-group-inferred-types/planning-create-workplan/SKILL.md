---
name: planning/create-workplan
description: Creates a WorkPlan (Schedule of Intent) and logs U.Work.
version: 0.1.0
status: experimental
family: planning
role: Planning Coordinator
allowed-tools:
  - write_to_file
policies:
  - A.15.2 WorkPlan (Schedule of Intent)
  - A.15.1 U.Work Logging
outputs:
  - WorkPlan
---

# Planning: Create WorkPlan (A.15.2)

## 1. Context

This skill implements **Pattern A.15.2 (WorkPlan / Schedule of Intent)**. It captures a planning artifact that scopes intent, deliverables, and context in a durable, reviewable form.

## 2. Metadata

- **ID**: `planning/create-workplan`
- **Role**: `U.RoleAssignment(PlanningCoordinator)`
- **Standard**: A.15.2, A.15.1

## 3. Instructions

### 3.1 Input Requirements

1. **Context**: Bounded context to place the WorkPlan (safe path segment).
2. **Plan ID**: Kebab-case identifier used for the WorkPlan filename.
3. **Title**: Short title for the plan.
4. **Intent**: One or two sentences describing the objective.
5. **Deliverables**: Optional semicolon-separated list (e.g., "Checklist; Timeline").

### 3.2 Output Artifact

Create a WorkPlan markdown file at:

`runtime/contexts/<context>/planning/workplans/<id>.md`

The WorkPlan MUST include:
- Title and intent.
- Deliverables list (or a TBD placeholder).
- Creation metadata.

### 3.3 Execution Steps

1. Validate inputs and sanitize `context`/`id`.
2. Resolve the target directory and create it if missing.
3. Render the WorkPlan markdown with sections for intent and deliverables.
4. Write the file to the target directory without overwriting existing plans.
5. Emit `U.Work` via `telemetry/log-work` for the creation action.
