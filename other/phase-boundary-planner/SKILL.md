---
name: phase-boundary-planner
description: Determines where one project phase should end and the next should begin by defining phase objectives, exit criteria, entry criteria, handoff artifacts, dependencies, risks, and go/no-go decision gates. Use when the user asks to split a roadmap into phases, clarify phase boundaries, decide what belongs before or after a milestone, prevent premature phase transitions, or define readiness gates between planning, implementation, validation, launch, and follow-up work.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: planner
  audience: project-leads-product-managers-technical-leads-and-implementation-agents
  tags:
    - phase-planning
    - roadmap
    - milestones
    - decision-gates
    - dependencies
    - handoffs
    - risk-management
  status: draft
  side_effects: none
---

# Phase Boundary Planner

## Purpose

Determine defensible boundaries between project phases so each phase ends only after the right outcome, evidence, decision, or handoff exists. The skill turns an ambiguous roadmap, milestone plan, implementation sequence, or project brief into phase transitions with clear exit criteria, entry criteria, dependencies, and go/no-go gates.

## When to use this skill

Use this skill when:

- The user asks where one project phase should end and the next should begin.
- A roadmap has phases, milestones, or stages but the transition points are vague.
- The team needs exit criteria, entry criteria, handoffs, or review gates between phases.
- Work is being sequenced across discovery, design, implementation, validation, launch, migration, stabilization, or follow-up phases.
- The user wants to prevent premature movement into a dependent phase before risks, decisions, or prerequisites are resolved.
- A plan needs clearer ownership and artifacts at the boundary between teams, agents, or workstreams.

Do not use this skill when:

- The user needs a full roadmap from scratch; use `project-roadmap-builder` first.
- The user needs detailed implementation tasks rather than phase transition criteria.
- The main need is grouping work into outcome-based milestones; use `milestone-planner` when milestone definition is the central task.
- The user only asks whether a new request is in or out of scope; use `scope-creep-guard` instead.
- There is not enough project context to identify at least a target outcome, rough work sequence, or known dependency.

## Inputs to inspect

- User-provided project brief, roadmap, milestone list, implementation plan, or backlog.
- Existing phase names, stage descriptions, release plan, sprint plan, or workstream handoff notes.
- Requirements, acceptance criteria, constraints, deadlines, non-goals, and success measures.
- Known dependencies, blockers, unresolved decisions, risks, approvals, and validation needs.
- Repository planning artifacts such as `README.md`, `ROADMAP.md`, `PLAN.md`, `TODO.md`, `MILESTONES.md`, `STATUS.md`, `docs/`, or exported issue lists when available.

Do not inspect the whole repository by default. Start with planning artifacts and inspect implementation files only when they clarify current capability, dependency status, or completion evidence.

## Workflow

1. Identify the planning context: target outcome, current phase structure, audience, time horizon, fixed constraints, and whether the plan is product, technical, research, migration, content, or operations oriented.
2. Inventory candidate work, decisions, evidence, and artifacts. Separate work that creates capability from work that validates readiness, reduces risk, or prepares a handoff.
3. Map dependencies and irreversibility. Mark tasks or decisions that must happen before downstream work can safely start, and flag expensive-to-reverse choices.
4. Define the purpose of each phase in outcome terms. A phase should end when a meaningful state is achieved, not merely when a list of activities has been attempted.
5. Place phase boundaries at the strongest natural transition points, such as:
   - A decision gate has enough evidence.
   - A foundation or interface is stable enough for dependent work.
   - A user-facing capability is complete enough to validate.
   - A risk has been retired or explicitly accepted.
   - A handoff artifact is ready for another team, agent, or workstream.
   - A release, migration, or rollout can proceed with rollback and support plans.
6. For each boundary, define:
   - Exit criteria for the ending phase.
   - Entry criteria for the next phase.
   - Required evidence or artifacts.
   - Go/no-go decision owner or review forum when known.
   - Dependencies that must be satisfied before crossing.
   - Risks of crossing too early or too late.
7. Check for boundary quality. Split phases that contain multiple unrelated outcomes; merge phases separated only by arbitrary dates, team preference, or vague progress markers.
8. Identify overlap rules where phases may run in parallel. Specify what can safely start early and what must wait for the boundary gate.
9. Produce a transition plan that shows phase order, boundary rationale, readiness gates, open questions, and immediate actions needed to validate uncertain boundaries.

## Output format

Return:

```md
## Planning basis

- Target outcome:
- Existing phases or candidate sequence:
- Constraints:
- Assumptions:

## Recommended phase boundaries

| Boundary | End phase when... | Start next phase when... | Required evidence | Rationale |
|---|---|---|---|---|
| Phase 1 → Phase 2 | ... | ... | ... | ... |

## Phase transition details

### Boundary: Phase 1 → Phase 2

- Ending phase objective:
- Next phase objective:
- Exit criteria:
  - [ ] ...
- Entry criteria:
  - [ ] ...
- Required artifacts or evidence:
- Decision gate:
- Dependencies:
- Safe overlap:
- Do not cross if:
- Risks of crossing too early:
- Risks of waiting too long:

## Boundary risks and open questions

- ...

## Immediate next actions

1. ...
2. ...
3. ...
```

If the user requests a shorter answer, preserve the boundary table, exit criteria, entry criteria, and immediate next actions.

## Quality bar

The task is complete only when:

- Each boundary is tied to an observable outcome, artifact, decision, or evidence threshold.
- Exit criteria and entry criteria are specific, testable, and not duplicates of each other.
- Boundary rationale explains why the next phase should not start earlier or later.
- Dependencies, risks, and unresolved decisions are visible.
- Safe overlap is distinguished from unsafe premature execution.
- The plan avoids arbitrary date-based or activity-only phase transitions unless a fixed external date is a real constraint.
- The output gives immediate actions for validating uncertain boundaries.

## Edge cases

- If the project has fixed calendar phases, keep the dates but add readiness gates and scope tradeoffs for each date.
- If phases must overlap, define the permitted overlap, synchronization point, and blocking conditions.
- If a dependency is controlled by an external party, treat the approval or input as boundary evidence and define a fallback path where possible.
- If the current phase names are misleading, preserve user terminology when useful but recommend clearer outcome-based labels.
- If the input is too vague, provide provisional boundaries and list the missing context needed to make them reliable.
- If the project is already underway, distinguish completed evidence from assumed completion before recommending a boundary crossing.

## Related skills

- `project-roadmap-builder`
- `milestone-planner`
- `implementation-order-planner`
- `implementation-checkpoint-planner`
- `task-dependency-mapper`
- `scope-creep-guard`
