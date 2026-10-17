---
name: implementation-plan-writer
description: Turns requirements, product specs, architecture decisions, technical designs, or feature briefs into an ordered implementation plan without writing code. Use when the user asks to sequence build work, break requirements into implementation tasks, translate design decisions into execution steps, identify dependencies, define validation gates, or prepare a coding agent or engineering team to implement safely.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: planner
  audience: developers-technical-leads-product-engineers-and-agent-orchestrators
  tags:
    - implementation-plan
    - requirements
    - architecture
    - task-breakdown
    - sequencing
    - validation
  status: draft
  side_effects: none
---

# Implementation Plan Writer

## Purpose

Turn requirements and architecture decisions into an ordered implementation plan that can guide a developer, engineering team, or coding agent before code is written.

This skill converts product goals, functional requirements, constraints, architecture notes, API contracts, data models, design decisions, and known risks into sequenced work packages. It emphasizes dependencies, safe increments, validation checkpoints, and handoff clarity.

The output is a planning artifact only. Do not write, patch, generate, or refactor implementation code while using this skill unless the user separately asks for implementation after the plan is complete.

## When to use this skill

Use this skill when:

- The user provides requirements, a PRD, technical design, architecture decision record, feature brief, or planning notes and wants an implementation plan.
- Work needs to be sequenced for a coding agent, sprint, issue breakdown, or engineering handoff.
- Architecture decisions need to become concrete implementation tasks.
- Requirements need dependencies, prerequisites, validation gates, and risk controls.
- The user wants a plan before coding begins.
- The user asks for task ordering, implementation phases, milestones, or a safe execution path for a feature.
- The project needs explicit non-code steps such as migrations, configuration, documentation, tests, rollout checks, or observability.

Common trigger phrases include:

- “Write an implementation plan.”
- “Turn these requirements into tasks.”
- “Create a coding plan, but do not write code.”
- “Sequence the implementation.”
- “Break this architecture into steps.”
- “Plan how to build this.”
- “Prepare a plan for another agent to implement.”
- “What order should we implement this in?”
- “Convert this technical design into an execution plan.”

Do not use this skill when:

- The user wants actual code changes immediately.
- The user needs a high-level roadmap rather than implementation-level steps.
- The task is primarily reconciling an existing plan against repository progress.
- The request is a repository health review, release readiness check, or code-quality audit.
- The requirements are too vague to produce a useful plan and the user has not allowed assumptions.
- Current external facts, prices, laws, standards, or service limits are needed before planning.

## Inputs to inspect

Start with user-provided material, including:

- Requirements, user stories, acceptance criteria, and non-goals
- Architecture decisions, ADRs, diagrams, schemas, APIs, and data contracts
- Product specs, PRDs, design docs, issue descriptions, and stakeholder notes
- Constraints around timeline, compatibility, migration, rollout, security, privacy, performance, and accessibility
- Existing open questions, risks, assumptions, and dependencies

If working in a repository, inspect only files needed to understand the plan, such as:

- `README.md`
- `PRD.md`
- `REQUIREMENTS.md`
- `ARCHITECTURE.md`
- `ADR.md` or `docs/adr/`
- `DESIGN.md`
- `PLAN.md`
- `ROADMAP.md`
- `TODO.md`
- API, schema, migration, configuration, or integration documentation
- Existing tests or examples that define expected behavior

Do not scan the whole repository by default. Prefer planning and architecture artifacts first, then inspect implementation files only when they clarify dependencies or constraints.

## Workflow

1. Establish the planning scope: feature or system boundary, intended audience, target outcome, non-goals, and whether the plan is for one agent, one developer, or a team.
2. Extract source requirements: functional behavior, acceptance criteria, constraints, architectural decisions, integrations, data changes, operational needs, and user-visible outcomes.
3. Identify gaps and assumptions: distinguish confirmed decisions from inferred ones. Ask concise questions only when missing information blocks sequencing; otherwise mark assumptions explicitly.
4. Define the implementation strategy: choose the smallest safe increments that move from prerequisites to working behavior, validation, rollout, and cleanup.
5. Sequence tasks by dependency:
   - Discovery or confirmation before irreversible work
   - Data model and contract changes before dependent features
   - Infrastructure or configuration before runtime usage
   - Core logic before UI or integration polish
   - Tests and validation alongside each meaningful increment
   - Documentation, migration, observability, and rollout checks before completion
6. For each task, specify:
   - Objective
   - Required inputs or dependencies
   - Concrete work to perform without writing code in the plan itself
   - Expected deliverables
   - Acceptance criteria or verification method
   - Risks, edge cases, or rollback considerations when relevant
7. Include validation checkpoints: unit, integration, end-to-end, manual QA, accessibility, performance, migration dry runs, security review, or stakeholder review as appropriate.
8. Identify parallelizable work only when dependencies allow it. Keep critical-path work ordered and avoid implying parallelism where shared files or decisions conflict.
9. Separate required implementation tasks from optional enhancements, polish, or future work.
10. End with the exact first actions needed to begin implementation and any unresolved questions that should be answered before coding.

## Output format

Return the implementation plan using this structure:

```md
## Summary

Briefly state the implementation objective, recommended strategy, and highest-risk dependency.

## Source inputs and assumptions

- Confirmed inputs:
  - ...
- Assumptions:
  - ...
- Open questions:
  - ...

## Ordered implementation plan

| Step | Goal | Work to do | Dependencies | Validation / acceptance criteria |
|---|---|---|---|---|
| 1 | ... | ... | ... | ... |

## Critical path

1. ...
2. ...
3. ...

## Parallelizable work

- ...

## Risks and mitigations

| Risk | Why it matters | Mitigation | Validation point |
|---|---|---|---|

## Testing and verification plan

- ...

## Documentation, rollout, and handoff notes

- ...

## Immediate next actions

1. ...
2. ...
3. ...
```

If the user requests another format, adapt while preserving task order, dependencies, assumptions, validation, risks, and immediate next actions.

## Quality bar

The task is complete only when:

- The plan is ordered by real dependencies rather than presented as an unordered checklist.
- Each step has a clear goal, concrete work, dependencies, and validation criteria.
- Requirements and architecture decisions are traceable to implementation tasks.
- The plan avoids writing code, patches, or implementation snippets unless the user explicitly requested examples.
- Assumptions and open questions are visible.
- Risks, migrations, rollout concerns, and non-functional requirements are not hidden.
- Testing and verification are integrated into the sequence, not left as a generic final step.
- Immediate next actions are specific enough for an implementer or coding agent to start safely.

## Edge cases

- If requirements conflict, identify the conflict and propose the smallest decision needed before implementation.
- If the architecture is undecided, split the plan into decision tasks followed by conditional implementation paths.
- If the user says “without writing code,” do not include code blocks, diffs, or file contents; describe intended edits at the task level.
- If the plan spans risky migrations, include backup, rollback, dry-run, and verification steps.
- If multiple agents may implement the plan, define ownership boundaries and avoid overlapping write scopes.
- If the repository state appears stale or uncertain, recommend a plan reconciliation pass before finalizing task order.
- If the user asks for estimates, provide effort bands only when there is enough context and clearly mark assumptions.

## Related skills

- `project-brief-builder`
- `project-roadmap-builder`
- `project-plan-reconciler`
