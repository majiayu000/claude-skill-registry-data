---
name: project-roadmap-builder
description: Produces a phased project roadmap with goals, deliverables, dependencies, acceptance criteria, milestones, risks, sequencing rationale, and checkpoint reviews. Use when the user asks to create a roadmap, phase a project, turn a brief into milestones, plan delivery increments, define implementation stages, identify dependencies, or prepare a project for coordinated execution.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: planner
  audience: product-managers-technical-leads-developers-founders-and-project-maintainers
  tags:
    - roadmap
    - milestones
    - project-planning
    - dependencies
    - deliverables
    - acceptance-criteria
    - checkpoints
  status: draft
  side_effects: none
---

# Project Roadmap Builder

## Purpose

Turn a project brief, product idea, feature request, repository plan, or stakeholder goal into a phased roadmap that is practical to execute and easy to review.

This skill organizes work into phases with explicit goals, deliverables, dependencies, acceptance criteria, checkpoint reviews, risks, and decision points. It keeps sequencing grounded in constraints and known dependencies instead of presenting a flat task list.

The result should be useful as a handoff artifact for implementation planning, issue creation, stakeholder alignment, sprint planning, or staged agent execution.

## When to use this skill

Use this skill when:

- The user asks for a project roadmap, phased plan, delivery roadmap, milestone plan, or execution sequence.
- A project brief or rough idea needs to be broken into realistic phases.
- Work needs clear goals, deliverables, dependencies, acceptance criteria, and checkpoints.
- A team needs to understand what should happen first, next, and later.
- A feature or product needs incremental delivery stages rather than one large implementation pass.
- A repository, README, PRD, issue list, TODO file, or planning document contains enough context to derive a roadmap.
- The user wants a roadmap that can later become tickets, milestones, or agent tasks.
- The project has meaningful dependencies, risks, or validation gates that affect sequencing.

Common trigger phrases include:

- “Create a project roadmap.”
- “Turn this brief into phases.”
- “Build a phased roadmap.”
- “Plan milestones and checkpoints.”
- “What should we deliver in each phase?”
- “Define dependencies and acceptance criteria.”
- “Make an implementation roadmap.”
- “Sequence this project.”
- “Break this into milestones.”
- “Create a delivery plan.”

Do not use this skill when:

- The user only needs a high-level project brief before roadmap planning.
- The user asks to reconcile an existing roadmap against actual repository progress.
- The primary task is code review, release readiness, or bug fixing.
- The user wants detailed ticket specs for every task rather than roadmap-level phases.
- The request requires current market, legal, pricing, or regulatory data that must be researched first.
- Another more specific roadmap, release, or domain planning skill applies.

## Inputs to inspect

Start with the user-provided brief, notes, goals, constraints, and conversation context.

If working inside a repository or document set, inspect relevant sources such as:

- `README.md`
- `BRIEF.md`
- `PRD.md`
- `ROADMAP.md`
- `PLAN.md`
- `TODO.md`
- `BACKLOG.md`
- `MILESTONES.md`
- `STATUS.md`
- `docs/`
- `issues/` or exported issue lists
- Architecture, API, schema, design, or deployment notes that constrain sequencing

Do not read the entire repository by default. Start with planning artifacts and only inspect implementation files when they clarify current capabilities, dependencies, or feasibility.

## Workflow

1. Identify the roadmap objective: target outcome, audience, planning horizon, desired level of detail, and whether the roadmap is for product, implementation, operations, content, or research.
2. Extract known context: goals, users, scope, non-goals, constraints, assumptions, deadlines, existing assets, open questions, and success measures.
3. Define the roadmap spine: choose phases that represent meaningful delivery increments, not arbitrary time buckets.
4. Sequence phases by dependency: put prerequisite decisions, architecture, research, setup, validation, or foundational work before dependent feature delivery.
5. For each phase, specify:
   - Goal
   - Key deliverables
   - Required inputs or dependencies
   - Acceptance criteria
   - Checkpoint or review gate
   - Risks and mitigations
6. Separate must-have work from optional enhancements so the roadmap can survive scope pressure.
7. Add cross-phase checkpoints for stakeholder review, technical validation, user feedback, launch readiness, or go/no-go decisions.
8. Capture unresolved questions and assumptions without inventing certainty. Mark assumptions that should be validated before a later phase begins.
9. If dates are requested, use explicit dates or relative durations only when the user provided enough scheduling context. Otherwise use phase order and estimated effort bands.
10. Finish with the immediate next actions needed to start Phase 1.

## Output format

Return the roadmap using this structure:

```md
## Summary

Brief statement of the roadmap objective and recommended sequencing.

## Roadmap

| Phase | Goal | Deliverables | Dependencies | Acceptance criteria | Checkpoint |
|---|---|---|---|---|---|
| Phase 1: Name | ... | ... | ... | ... | ... |

## Cross-phase dependencies

- ...

## Risks and mitigations

| Risk | Impact | Mitigation | Review point |
|---|---|---|---|

## Assumptions and open questions

- ...

## Immediate next actions

1. ...
2. ...
3. ...
```

If the user requests a different format, adapt while preserving goals, deliverables, dependencies, acceptance criteria, and checkpoints.

## Quality bar

The task is complete only when:

- Each phase has a clear goal and concrete deliverables.
- Dependencies explain why the sequence is ordered the way it is.
- Acceptance criteria describe observable completion conditions.
- Checkpoints identify when to review, validate, decide, or adjust scope.
- Risks, assumptions, and open questions are explicit instead of hidden.
- The roadmap distinguishes required work from optional or later enhancements.
- The immediate next actions are specific enough to begin execution.

## Edge cases

- If the input is too vague, create a provisional roadmap and list the questions that would most improve it.
- If the user provides a fixed deadline, design the roadmap around scope tradeoffs and critical path constraints.
- If dependencies are unclear, state the likely dependency and how to validate it.
- If the project is already underway, ask whether to reconcile current progress first or clearly mark the roadmap as based only on provided context.
- If the roadmap would require external facts, identify which claims need current research before finalizing commitments.
- If the user asks for implementation, produce the roadmap first unless they explicitly requested file changes or ticket creation.

## Related skills

- `project-brief-builder`
- `project-plan-reconciler`
- `repo-next-steps-review`
