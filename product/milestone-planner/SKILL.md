---
name: milestone-planner
description: Groups a defined body of work into meaningful outcome-based milestones with entry criteria, completion criteria, dependencies, risks, and expected outcomes. Use when the user asks to organize a backlog or plan into milestones, define milestone gates, sequence delivery increments, or clarify what must be true before a milestone starts or finishes.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: planner
  audience: project-leads-and-implementers
  tags:
    - milestones
    - delivery-planning
    - sequencing
    - dependencies
    - risks
    - completion-criteria
  status: draft
  side_effects: none
---

# Milestone Planner

## Purpose

Turn a defined project, roadmap, backlog, or body of work into outcome-based milestones with explicit gates. Each milestone should represent a meaningful change in project capability or confidence, not merely a date range or arbitrary batch of tasks.

## When to use this skill

Use this skill when:

- The user asks to group work into milestones or delivery increments.
- A backlog or implementation plan needs clearer sequencing and gates.
- The team needs entry criteria, completion criteria, risks, and expected outcomes for each milestone.
- A project needs review points where work can continue, pause, or change direction.

Do not use this skill when:

- The project goal and scope are still too vague to identify the work.
- The user needs detailed implementation tasks rather than milestone-level grouping.
- The user needs to compare an existing plan with actual repository progress.
- The main decision is what belongs in an MVP; use `mvp-scope-planner` first.

## Inputs to inspect

- Project brief, requirements, PRD, roadmap, or feature description.
- Existing backlog, issues, TODOs, implementation plan, or milestone document.
- Dependencies, constraints, deadlines, staffing assumptions, and known risks.
- Success measures, validation requirements, release gates, and non-goals.
- Repository evidence when it materially affects sequencing.

## Workflow

1. Establish the target outcome, planning horizon, fixed constraints, and available work inventory. State assumptions where inputs are incomplete.
2. Normalize the work into deliverables and decisions. Separate required work, optional work, validation work, and unresolved questions.
3. Identify dependency order and critical gates. Do not place work in a milestone whose prerequisites are unmet.
4. Choose milestones around verifiable outcomes such as risk retired, capability enabled, integration proven, or release readiness achieved. Avoid milestones named only after activities or calendar periods.
5. For each milestone, define:
   - Objective and expected outcome.
   - Included deliverables and explicit exclusions.
   - Entry criteria that must be true before work begins.
   - Completion criteria expressed as observable evidence.
   - Dependencies and decisions.
   - Principal risks and mitigations.
6. Add review gates between milestones. Identify the evidence needed to proceed, revise scope, repeat work, or stop.
7. Check milestone size and coherence. Split milestones with unrelated outcomes; merge milestones that cannot deliver or validate anything independently.
8. Surface cross-milestone risks, critical-path items, parallel work, and confidence levels. Do not disguise uncertain estimates as commitments.
9. Validate that every required work item has a home, every milestone advances the target outcome, and completion criteria prove outcomes rather than task activity.

## Output format

Return:

```md
## Planning basis

- Target outcome:
- Constraints:
- Assumptions:

## Milestone overview

| Milestone | Outcome | Depends on | Review gate |
|---|---|---|---|

## Milestone 1: Name

- Objective:
- Expected outcome:
- Included work:
- Excluded work:
- Entry criteria:
  - [ ] ...
- Completion criteria:
  - [ ] ...
- Dependencies and decisions:
- Risks and mitigations:
- Evidence for the review gate:

## Cross-milestone considerations

- Critical path:
- Parallel work:
- Scope or schedule risks:
- Open decisions:
```

## Quality bar

The task is complete only when:

- Milestones are organized around meaningful, independently reviewable outcomes.
- Entry and completion criteria are specific, observable, and distinct.
- Dependencies and review gates make the sequence defensible.
- Required work is covered and exclusions prevent likely scope creep.
- Risks include a concrete response, owner or decision point when known.
- Unknowns and assumptions are visible rather than presented as facts.

## Edge cases

- If no work inventory exists, produce a provisional milestone skeleton and list the missing planning inputs.
- If a fixed deadline cannot accommodate all work, preserve the outcome hierarchy and show scope tradeoffs instead of compressing every milestone.
- If milestones must overlap, identify the interface, ownership boundary, and synchronization gate.
- If one milestone contains most of the project, split it by risk retirement, usable capability, integration, or validation outcome.
- If external approvals control progress, treat them as dependencies and define fallback paths where possible.

## Related skills

- `project-brief-builder`
- `mvp-scope-planner`
- `project-roadmap-builder`
- `implementation-plan-writer`
- `project-plan-reconciler`
