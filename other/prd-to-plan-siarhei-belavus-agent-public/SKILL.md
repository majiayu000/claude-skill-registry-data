---
name: prd-to-plan
description: Turn a PRD into a multi-phase implementation plan using tracer-bullet vertical slices, saved as a local plan artifact alongside the PRD.
---

Your job is to convert a PRD into a practical implementation plan that another agent can execute safely.

The plan should be sequenced, reviewable, and biased toward visible progress. Prefer vertical slices that validate assumptions early over large horizontal phases.

## Process

1. Read and understand the PRD

Extract the key information:
- user problem and desired outcomes
- critical workflows
- constraints and non-goals
- major risks and open questions

If the PRD path is not given explicitly, infer the PRD slug from the provided PRD artifact and use that slug consistently.

2. Derive an implementation strategy

Create a strategy that:
- validates risky assumptions early
- delivers value incrementally
- keeps the system working after each phase
- limits branching complexity and migration risk
- makes validation straightforward at each step

Avoid plans that defer all user-visible value until the end.

3. Create the plan file

Write the plan to:
- `.prd/<prd-slug>/plans/implementation-plan.md`

Create the `plans/` directory if it does not exist.

4. Write the plan

Use this structure:

```md
# Implementation Plan: <initiative name>

## Parent PRD
.prd/<prd-slug>/prd.md

## Planning Principles
- Principle 1
- Principle 2

## Phase 1: <name>
### Goal
What this phase proves or delivers.

### Scope
- Step 1
- Step 2

### Validation
- Test or check 1
- Test or check 2

### Risks / Notes
- Important warning or dependency

## Phase 2: <name>
...

## Dependencies and Order
- Cross-phase dependency 1
- Cross-phase dependency 2

## Open Questions
- Question 1
- Question 2
```
```

Each phase should be small enough to review and validate, but large enough to produce meaningful progress.

5. Make the plan executable

The plan should be detailed enough that another agent can pick it up in a fresh context window without extra explanation.

That means:
- explicit phase goals
- clear sequencing
- concrete validation steps
- important constraints called out near the relevant work
- no reliance on unstated tribal knowledge

6. Final response

In your final response:
- summarize the implementation strategy
- provide the final plan path
- mention any major unresolved risks or questions

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.
