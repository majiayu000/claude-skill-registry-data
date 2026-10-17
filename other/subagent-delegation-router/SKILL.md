---
name: subagent-delegation-router
description: Decomposes complex work into bounded subagent tasks, decides whether delegation is worthwhile, routes each task to an appropriate available model and reasoning effort, runs independent work in parallel, and synthesizes the evidence. Use when the user asks to use subagents, delegate, parallelize, split work across agents, investigate independent concerns, explore a large repository, or add an independent validation pass and expects the agents to execute now. For a plan-only delegation map, use agent-workstream-planner instead.
license: MIT
compatibility: Portable Agent Skill. Requires an Agent Skills-compatible environment with subagent support for delegated execution; degrades to a sequential parent-agent workflow when subagents or per-agent routing controls are unavailable.
metadata:
  category: project-planning
  task_type: planner
  audience: developers-and-agent-users
  tags:
    - subagents
    - orchestration
    - delegation
    - parallelism
    - model-routing
    - reasoning-effort
  status: draft
  side_effects: none
---

# Subagent Delegation Router

## Purpose

Turn one complex request into a controlled multi-agent workflow by using the smallest useful team, respecting dependencies and write boundaries, and returning one synthesized result.

The parent agent remains responsible for the outcome. Delegation does not expand the user's authorization, relax repository instructions, or replace evidence-based judgment.

## When to use this skill

Use this skill when:

- The user explicitly asks for subagents, delegation, or parallel execution.
- Independent repository areas, documents, hypotheses, or review dimensions can be investigated concurrently.
- Read-heavy exploration, logs, tests, or research would otherwise crowd the parent context.
- A complex implementation benefits from separate exploration, ownership, and validation phases.
- Independent review would materially improve confidence in a consequential result.

Do not use this skill when:

- One agent can finish the task faster than it can define and coordinate a useful subtask.
- Every step depends directly on the previous step.
- The next action is small, obvious, and inexpensive to verify.
- Multiple agents would need to modify the same files concurrently.
- The user wants only a workstream or delegation plan without launching agents; use `agent-workstream-planner` instead.
- The runtime or applicable instructions prohibit subagent use; execute the same decomposition sequentially instead.

## Inputs to inspect

Inspect the minimum context needed to establish:

- The user's intended outcome, deliverables, constraints, and authorized side effects
- Applicable repository instructions and skills
- Relevant architecture, files, artifacts, and existing plans
- Independent concerns, unresolved hypotheses, and dependency boundaries
- Available subagent models, reasoning levels, concurrency slots, context-sharing controls, and tool permissions
- Mutable files or external systems that require a single owner

Do not perform a broad parent-agent scan when bounded explorers can gather that evidence more efficiently.

## Workflow

### 1. Define the final outcome

Restate the deliverable internally before creating agents. Describe the result, not the activity.

Examples:

- Bug investigation: root cause, smallest authorized fix, and validation
- Code review: evidence-backed findings ordered by severity
- Feature work: working implementation and proportionate verification

Exclude analysis that does not help produce that deliverable.

### 2. Apply the delegation gate

Delegate only when all applicable answers are favorable:

1. Can the work be divided into bounded responsibilities?
2. Can at least two tasks make useful progress independently or concurrently?
3. Will delegation reduce latency, context noise, or important uncertainty?
4. Can file ownership and permissions prevent avoidable collisions?
5. Is the expected benefit greater than the coordination cost?

If not, continue in the parent agent. Do not manufacture work to justify subagents.

### 3. Decompose by responsibility

Split by outcome or concern rather than arbitrary file counts. Give each proposed task one primary class:

```txt
lookup | extraction | scan | exploration | research | review
debugging | planning | implementation | validation | adjudication
```

Prefer responsibilities such as "trace authentication state" or "review concurrency correctness" over "inspect files 1–20." Use file-based splits only when the files are genuinely independent.

### 4. Map dependencies and write ownership

For every task, record:

- Inputs and prerequisite results
- Outputs and downstream consumers
- Read-only or write access
- Owned files, modules, or artifacts
- Completion condition

Parallelize independent read work aggressively. Parallelize writes only across clearly disjoint ownership boundaries. Assign one implementation owner for any shared area, and sequence dependent work honestly.

Use a default delegation depth of one. Allow nested delegation only when it has a clear, bounded advantage and the runtime permits it.

### 5. Route model and reasoning effort

Read [Model and effort routing](references/model-and-effort-routing.md) whenever the task requires choosing a subagent model or reasoning level.

Base routing on workload characteristics:

- Fast tier: narrow, deterministic, mechanical tasks
- Balanced tier: read-heavy exploration and evidence gathering
- Frontier reasoning tier: ambiguity, architecture, difficult debugging, implementation, security, synthesis, or adjudication

Inspect the runtime's available model identifiers and supported reasoning levels before spawning. Treat reference model names as examples, never as guaranteed availability. Choose model and reasoning effort separately, and use expensive reasoning only where it can materially improve the result.

### 6. Create the delegation plan

Define the plan before spawning:

| Agent | Role | Task | Model tier | Effort | Access | Depends on |
|---|---|---|---|---|---|---|
| A | explorer | Trace state flow | balanced | medium | read-only | — |
| B | explorer | Inspect API path | balanced | medium | read-only | — |
| C | reviewer | Resolve evidence | frontier | high | read-only | A, B |
| D | worker | Implement authorized fix | frontier | medium | write owner | C |
| E | validator | Inspect resulting change | frontier | high | read-only | D |

Use only the rows the task justifies. Prefer two to four concurrent subagents for ordinary complex work, subject to actual capacity. Do not create an agent merely because a slot is available.

### 7. Write bounded subagent prompts

Give every subagent:

```txt
Goal: The one question or outcome it owns.
Scope: Files, subsystem, artifact, or concern included.
Exclusions: Work it must avoid.
Context: Only the task-local facts and constraints it needs.
Deliverable: Exact result shape.
Evidence: Required paths, symbols, tests, observations, or sources.
Completion: The condition that ends the task.
```

Also state:

- Whether file modification is allowed
- Which files or artifacts it owns
- Whether it may delegate further
- Which claims require direct evidence

When model overrides require reduced context inheritance, pass the necessary context explicitly. Do not leak expected conclusions to independent reviewers or validators.

### 8. Execute in dependency-aware waves

Spawn all currently independent tasks together, up to the runtime's available capacity. While they run, continue useful parent-agent work that does not duplicate their assignments.

Collect completed results before launching dependent tasks. Retry failures only when the result is required and the failure appears transient; otherwise narrow the task, change routing, or continue without an optional contribution.

Stop spawning when all required workstreams are covered, new work would duplicate existing assignments, or the remaining work is inherently sequential.

### 9. Reconcile and synthesize

Evaluate subagent results against their evidence. Do not paste raw outputs into the final answer.

When agents disagree:

1. Check whether they inspected the same behavior and evidence.
2. Identify missing facts or incompatible assumptions.
3. Resolve the issue in the parent when straightforward.
4. Use an adjudication agent only for a material conflict that cannot be resolved cheaply.

Do not use majority vote as a substitute for evidence.

### 10. Validate proportionately

Add independent validation when the work affects security, accessibility, correctness guarantees, shared architecture, several systems, or a meaningful regression surface. Validation must inspect the artifact or behavior independently rather than confirm the implementation owner's explanation.

Skip a separate validator for trivial, deterministic results that the parent can verify directly.

## Permissions and safety

- Treat explorers, researchers, reviewers, and validators as read-only unless the original request authorizes changes.
- Grant write ownership only for the files or systems required by the delegated implementation.
- Never infer permission to publish, deploy, delete, send, or mutate remote systems from permission to delegate.
- Follow applicable repository and environment instructions when they conflict with this workflow.
- Remember that agents may share a workspace; one agent's edits can become immediately visible to others.

## Output format

Return one distilled result. When delegation materially contributed, use:

```md
## Result

<Final answer or implementation outcome>

## Delegated work

- <Role>: <Evidence or result established>

## Changes

- `path/to/file` — <change>

## Validation

- <Check and result>

## Remaining uncertainty

- <Only unresolved material issues>
```

Omit empty sections. Show the full routing table only when the user asks, model choices materially affect the result, or orchestration itself is under review. Summarize decisions without exposing private reasoning traces.

## Quality bar

The task is complete only when:

- Delegation provides a clear benefit over direct execution.
- Every subagent owns one bounded, non-duplicative responsibility.
- Dependencies and concurrency are represented honestly.
- Model tier and reasoning effort match the actual workload.
- Read and write boundaries prevent avoidable conflicts.
- Prompts define evidence and completion requirements.
- The parent resolves contradictions and synthesizes one answer.
- Validation is proportional to risk.
- Agent count and reasoning cost remain proportional to the problem.
- The final result answers the original request and respects its authorization.

## Edge cases

- If subagents are unavailable, use the same decomposition and execute it sequentially in the parent.
- If a preferred model or reasoning level is unavailable, choose the closest supported option by workload characteristics.
- If the user specifies a model, effort, or agent count, honor it when feasible without inventing filler tasks or violating runtime limits.
- For highly coupled implementation, delegate research and review, then use one implementation owner.
- For a huge repository, start with several narrow explorers rather than giving every agent the whole repository.
- If a subagent discovers greater complexity, reassess dependencies and routing before escalating cost.
- If context, time, or token limits tighten, preserve critical-path tasks and validation before optional parallel work.

## Related skills

- `agent-workstream-planner` for producing a coordination plan without executing agents
- `task-dependency-mapper` for detailed dependency analysis
- `task-context-packager` for bounded handoff context
- `implementation-plan-writer` for implementation sequencing
- `implementation-checkpoint-planner` for risk-based review gates
