---
name: agent-workstream-planner
description: Divides a project into coordinated workstreams for agents, developers, or teams, such as architecture, UI, data, accessibility, testing, and documentation. Use when the user asks to split work across multiple contributors, define ownership boundaries, identify dependencies and handoffs, prevent overlapping edits, plan parallel execution, or establish integration checkpoints.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: planner
  audience: technical-leads-project-maintainers-developers-and-agent-orchestrators
  tags:
    - workstreams
    - multi-agent
    - delegation
    - ownership
    - dependencies
    - parallel-execution
    - coordination
  status: draft
  side_effects: none
---

# Agent Workstream Planner

## Purpose

Divide a project into coordinated workstreams that can be assigned to agents, developers, or teams without losing shared context or creating avoidable conflicts.

This skill defines outcomes, ownership boundaries, inputs, deliverables, dependencies, handoffs, shared decisions, and integration checkpoints for workstreams such as architecture, UI, data, accessibility, testing, and documentation. It produces a coordination plan only; it does not start agents, assign real people, edit files, or implement the work.

## When to use this skill

Use this skill when:

- The user asks to split a project among multiple agents, developers, specialists, or teams.
- A project has several disciplines that can progress partly in parallel.
- Contributors need clear ownership boundaries, file scopes, contracts, or handoff expectations.
- The user wants an agent orchestration plan, delegation map, parallel work plan, or workstream breakdown.
- Shared decisions and cross-workstream dependencies need to be identified before execution.
- Concurrent work could cause overlapping edits, duplicated effort, integration failures, or inconsistent assumptions.

Common trigger phrases include:

- “Split this project into workstreams.”
- “Plan tasks for multiple agents.”
- “What can run in parallel?”
- “Divide this among architecture, UI, data, accessibility, testing, and docs.”
- “Define ownership and handoffs.”
- “Create a coordinated delegation plan.”
- “Prevent agents from editing the same files.”

Do not use this skill when:

- One contributor can complete the work more clearly than multiple workstreams.
- The user needs a high-level roadmap without ownership or coordination details.
- The user needs an ordered implementation plan for a single implementer.
- The user asks to launch agents or execute the work rather than plan it.
- The project lacks enough scope to identify meaningful workstream boundaries; clarify or create a project brief first.

## Inputs to inspect

Start with the smallest set of sources that establishes scope and coordination needs:

- Project brief, requirements, user stories, acceptance criteria, and non-goals
- Architecture notes, API contracts, schemas, design files, and interface specifications
- Repository structure and likely file ownership boundaries
- Existing roadmap, implementation plan, issues, milestones, or task list
- Constraints involving accessibility, security, privacy, performance, compatibility, release, and documentation
- Available contributors or agents, their specialties, and any concurrency limits
- Known deadlines, sequencing constraints, shared resources, and integration risks

If repository access is available, inspect planning documents and top-level structure before implementation details. Do not scan every file unless file ownership or coupling cannot otherwise be determined.

## Workflow

1. Establish the project outcome, in-scope deliverables, non-goals, planning horizon, and intended executors.
2. Identify the coordination constraints: available contributors, concurrency limits, required specialties, shared files, fixed interfaces, deadlines, and review requirements.
3. Map the project into capability areas. Consider architecture, UI, data, accessibility, testing, documentation, security, infrastructure, release, or research only when each area has a distinct outcome.
4. Choose workstream boundaries around cohesive deliverables rather than job titles alone. Merge streams that are too small or tightly coupled, and split streams whose ownership or outputs are ambiguous.
5. Define each workstream with:
   - Objective and user or project outcome
   - In-scope and out-of-scope work
   - Inputs and prerequisite decisions
   - Deliverables and acceptance criteria
   - Owned files, modules, artifacts, or decision areas when known
   - Dependencies, consumers, and handoff contract
   - Validation responsibilities
6. Identify shared concerns that must not become orphaned work. Assign explicit ownership for accessibility, security, privacy, performance, observability, migration, testing, and documentation as relevant.
7. Build the dependency map. Distinguish:
   - Blocking prerequisites
   - Stable contracts that enable parallel work
   - Outputs consumed by another stream
   - Shared decisions requiring joint review
   - Final integration dependencies
8. Mark execution lanes:
   - Start now: independent or prerequisite work
   - Start after contract: work that can proceed once an interface is agreed
   - Start after dependency: work blocked on another deliverable
   - Integration only: work reserved for coordinated merge and validation
9. Prevent collisions by assigning one owner per shared artifact, defining read-only consumers, naming likely overlapping files, and selecting a tie-breaker for cross-stream decisions.
10. Define coordination checkpoints for contract approval, intermediate integration, cross-discipline review, end-to-end validation, and final handoff. Specify what evidence each checkpoint requires.
11. Check workload balance and critical-path coverage. Reassign or resize streams that create idle contributors, overloaded owners, or a coordination cost greater than the benefit of parallelism.
12. Finish with the recommended launch order, first handoffs, unresolved decisions, and conditions that require replanning.

## Output format

Return the workstream plan using this structure:

```md
## Summary

State the project outcome, recommended workstream model, and critical coordination risk.

## Assumptions and constraints

- ...

## Workstream map

| Workstream | Objective | Owner profile | Scope | Deliverables | Dependencies | Acceptance criteria |
|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... |

## Ownership and interface boundaries

| Artifact or decision | Primary owner | Consumers | Handoff contract | Collision risk |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

## Dependency and execution plan

- Start now: ...
- Start after contract: ...
- Start after dependency: ...
- Integration only: ...

## Coordination checkpoints

| Checkpoint | Participants | Required evidence | Decision or output |
|---|---|---|---|
| ... | ... | ... | ... |

## Risks and conflict controls

- ...

## Launch order and first handoffs

1. ...

## Open decisions

- ...
```

Adapt the format when the user requests another artifact, but preserve ownership, boundaries, dependencies, handoffs, validation, and checkpoints.

## Quality bar

The task is complete only when:

- Every workstream owns a cohesive outcome rather than a vague discipline label.
- Each deliverable has one primary owner and observable acceptance criteria.
- Dependencies distinguish blockers from contracts that allow parallel execution.
- Cross-cutting concerns have explicit owners and validation duties.
- Shared files, artifacts, and decisions include collision controls or handoff rules.
- Integration and review checkpoints name participants, evidence, and expected decisions.
- The critical path and safe parallel work are both visible.
- The plan does not imply that agents or contributors have been started or assigned when they have not.

## Edge cases

- If only one or two cohesive outcomes exist, recommend fewer workstreams instead of manufacturing parallelism.
- If contributor capabilities are unknown, define owner profiles rather than inventing names or assignments.
- If architecture or contracts are unresolved, create a short prerequisite stream and make dependent streams conditional.
- If several streams must edit the same files, appoint one integration owner or restructure ownership around modules or artifacts.
- If accessibility, testing, or documentation must be continuous, embed responsibilities in every stream while retaining one coordinating owner.
- If work is already underway, mark current owners and partial outputs before proposing reassignment.
- If estimates are requested, use effort bands and state assumptions; do not infer calendar dates without capacity information.
- If the user asks for actual multi-agent execution, produce the coordination plan first, then use available orchestration capabilities only with the required authorization and controls.

## Related skills

- `implementation-plan-writer`
- `implementation-order-planner`
- `milestone-planner`
- `project-roadmap-builder`
- `constraint-mapper`
