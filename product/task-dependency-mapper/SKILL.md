---
name: task-dependency-mapper
description: Builds an evidence-based dependency graph for project tasks and detects blocked work, circular dependencies, unnecessary coupling, critical-path constraints, and tasks that are safe to run in parallel. Use when the user asks to map task prerequisites, diagnose why a plan is stuck, validate execution order, untangle coupled work, identify parallel workstreams, or review a backlog, roadmap, milestone, issue set, or implementation plan for dependency risks.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access unless stated otherwise.
metadata:
  category: project-planning
  task_type: planner
  audience: project-leads-software-teams-and-coding-agents
  tags:
    - task-dependencies
    - dependency-graph
    - blockers
    - critical-path
    - parallel-work
    - project-planning
  status: draft
  side_effects: none
---

# Task Dependency Mapper

## Purpose

Turn a task list or plan into a directed dependency graph, then use that graph to expose blockers, cycles, redundant constraints, and safe concurrency. Produce an execution view that distinguishes genuine prerequisites from coordination preferences and inferred relationships.

This is a planning-only skill. Do not modify tasks, issue trackers, plans, or repositories unless the user separately asks for implementation.

## When to use this skill

Use this skill when:

- The user wants to know which tasks block other tasks or why a plan is stuck.
- A backlog, roadmap, milestone, issue set, or implementation plan needs a dependency review.
- The user wants to find circular dependencies or an executable task order.
- Multiple people or agents need safe parallel workstreams.
- A plan appears over-sequenced because tasks share a component, owner, or milestone.
- The user wants to reduce coordination overhead without violating real prerequisites.

Do not use this skill when:

- The user only needs tasks decomposed from requirements; use `implementation-plan-writer`.
- The task is to choose among competing features based on value; use `feature-priority-planner`.
- The user wants a phased product roadmap rather than task-level dependency analysis; use `project-roadmap-builder`.
- No task set, plan, or reliable basis for deriving one is available. Request or derive a provisional task set and label it as assumed.

## Inputs to inspect

Start with the smallest useful evidence set:

- Task IDs, titles, descriptions, statuses, owners, and acceptance criteria.
- Explicit `depends on`, `blocked by`, `blocks`, parent-child, milestone, and linked-issue fields.
- Implementation plans, roadmaps, architecture decisions, API contracts, schemas, and migration notes.
- Repository files or tests that reveal actual build, data, interface, or integration order.
- External approvals, credentials, environments, vendors, teams, release windows, and other non-task prerequisites.
- Shared files, services, environments, fixtures, datasets, or decision surfaces that may create execution conflicts.

Do not infer a dependency merely because two tasks mention the same feature, owner, component, or milestone.

## Dependency model

Represent each task as a node. Use the edge direction `prerequisite -> dependent`: `A -> B` means B cannot complete until A satisfies the named condition.

Classify every edge:

| Type | Meaning | Scheduling effect |
|---|---|---|
| Hard | B cannot start or produce a valid result before A completes. | Order A before B. |
| Start-to-start | B may start only after A reaches a named checkpoint. | Allow partial overlap after the checkpoint. |
| Validation | B may be built earlier but cannot be accepted until A supplies evidence. | Separate build readiness from completion readiness. |
| Resource conflict | A and B compete for an exclusive resource or overlapping mutation surface. | Serialize or coordinate; do not call it a prerequisite. |
| Soft | Ordering is convenient, conventional, or risk-reducing but not required. | Treat as a recommendation, not a blocker. |
| Inferred | Evidence suggests a relationship but does not prove it. | Mark confidence and state how to verify it. |

Keep external prerequisites as explicit gate nodes when they affect scheduling. Examples include `approval granted`, `test environment available`, or `API contract decided`.

## Workflow

1. Define the graph boundary. State the task set, planning horizon, completion meaning, and whether the analysis concerns task start, task completion, or both.
2. Normalize tasks. Assign a stable ID, concise outcome, current status, and completion criterion to each task. Split a task only when it combines independently schedulable outcomes.
3. Extract explicit edges. Record the source evidence and the condition the prerequisite must satisfy.
4. Infer candidate edges from contracts, artifacts, data flow, decisions, integrations, and acceptance criteria. Label each inference and its confidence; do not silently promote it to a hard dependency.
5. Classify every edge with the dependency model. Replace vague edges such as “related to” with a precise gating condition or remove them.
6. Add external gate nodes and resource-conflict relationships. Keep resource conflicts visually and semantically separate from directed prerequisite edges.
7. Detect direct blockers. A task is blocked when an unmet hard prerequisite or external gate prevents its next valid action. Name the immediate blocker and, when useful, its upstream root blocker.
8. Detect cycles among hard and checkpoint dependencies. Report the complete cycle path. Do not produce a topological order until every hard cycle is resolved or explicitly represented as an invalid planning state.
9. Challenge each cycle edge. Look for mistaken direction, oversized tasks, hidden shared decisions, mutual acceptance criteria, or a contract that can be defined independently. Recommend the smallest truthful decoupling action.
10. Find unnecessary coupling. Flag duplicate or transitive edges, soft preferences recorded as hard blockers, shared ownership mistaken for dependency, artificial phase gates, and tasks coupled only because their boundaries are unclear.
11. Determine readiness. Mark each task as `ready`, `conditionally ready`, `blocked`, `in progress`, `complete`, or `unknown`, based on current evidence rather than list position.
12. Build execution layers by repeatedly selecting ready nodes after satisfied hard prerequisites are removed. These layers are candidates for concurrency, not automatic permission to run concurrently.
13. Check parallel safety within each layer. Confirm tasks do not depend on the same unresolved decision, mutate overlapping files or state, require one exclusive environment, invalidate each other's assumptions, or rely on an unstable shared contract.
14. Identify the critical chain when duration or effort evidence exists. If estimates are missing, report high-leverage blocker chains without claiming a mathematical critical path.
15. Produce a corrected graph and execution view. Preserve unresolved uncertainty and explain which new evidence could change the result.

## Analysis rules

- Distinguish “cannot start,” “cannot finish,” and “should not merge or release.” They imply different edges.
- A path `A -> B -> C` already makes C transitively dependent on A. Flag an explicit `A -> C` edge as redundant unless it documents a distinct condition.
- Sibling tasks are not automatically dependent. A shared parent usually expresses grouping, not order.
- Shared ownership limits capacity but does not create a logical dependency.
- Shared files or services may create a merge or mutation conflict without creating a prerequisite. Report this as a resource conflict.
- A task with incomplete prerequisites may still have preparatory work available. Use `conditionally ready` only when that work will remain valid if the blocker resolves differently.
- Never claim tasks are safe in parallel solely because no explicit edge connects them. Check hidden contracts, resources, decisions, and mutation surfaces.
- Do not invent durations. Critical-path claims require duration or effort evidence; otherwise use dependency depth and downstream reach as qualitative signals.

## Output format

Return the result using this structure:

```md
## Summary

- Graph status: acyclic | cyclic | incomplete
- Tasks: [count]
- Ready now: [IDs]
- Blocked: [IDs]
- Safe parallel groups: [count]
- Highest-leverage blocker: [task or gate and reason]

## Dependency graph

[Mermaid flowchart when supported, otherwise an adjacency list. Use prerequisite -> dependent.]

## Task status

| Task | Status | Immediate prerequisite or conflict | Root blocker | Evidence / confidence |
|---|---|---|---|---|
| ... | ready / conditionally ready / blocked / in progress / complete / unknown | ... | ... | ... |

## Dependency findings

### Cycles

- `A -> B -> C -> A` — cause; smallest proposed break.

### Unnecessary coupling

- Edge or relationship — why it is not a hard dependency; proposed correction.

### Uncertain dependencies

- Relationship — assumption; evidence needed.

## Execution layers

1. **Layer 0:** [tasks ready now]
2. **Layer 1:** [tasks unlocked by Layer 0]

## Parallel work

| Group | Tasks | Why parallel-safe | Coordination boundary | Synchronization point |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

## Recommended graph changes

- Add / remove / reclassify / reverse / split: ...

## Assumptions and open questions

- ...
```

Omit empty sections. For a small graph, combine the status and dependency findings into one compact table. For a large graph, summarize the main execution view and place the complete edge list in a collapsible section or separate artifact when the environment supports it.

## Quality bar

The task is complete only when:

- Every hard edge has a named gating condition and evidence or an explicit inference label.
- Edge direction is defined and used consistently.
- Blocked tasks name an unmet immediate prerequisite or external gate.
- Every reported cycle includes its full path and a concrete decoupling option.
- Unnecessary coupling is distinguished from valid hard dependencies and resource conflicts.
- Ready and parallel-safe are treated as different conclusions.
- Parallel groups account for shared decisions, contracts, resources, and mutation surfaces.
- A topological execution order is produced only for an acyclic hard-dependency graph.
- Critical-path language is used only when adequate duration or effort data exists.
- Missing evidence, assumptions, and confidence are visible.

## Edge cases

- If task descriptions are too vague to identify outcomes or gates, mark affected edges `unknown` and list the minimum clarification needed.
- If a cycle represents genuine simultaneous coordination, replace the cyclic tasks with a shared contract or coordination task, then make both tasks depend on that node.
- If completed work conflicts with declared dependencies, report the inconsistency; do not rewrite history to make the graph appear valid.
- If a task is blocked by an external event with no owner, recommend assigning an owner and observable exit condition to the gate.
- If the graph is very large, analyze strongly connected components and root blockers first, then summarize downstream impact.
- If one task contains several independently unblockable outcomes, recommend splitting it before scheduling parallel work.
- If estimates are inconsistent or incomparable, avoid a critical-path calculation and report the dependency chain with the greatest downstream reach instead.

## Related skills

- `implementation-order-planner`
- `implementation-plan-writer`
- `milestone-planner`
- `project-plan-reconciler`
- `project-roadmap-builder`
