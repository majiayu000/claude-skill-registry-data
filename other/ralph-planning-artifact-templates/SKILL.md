---
name: ralph-planning-artifact-templates
description: Ralph-v2 planning artifact templates and task decomposition scaffolding. Use when creating or updating `plan.md`, `progress.md`, `metadata.yaml`, iteration metadata, or isolated task files during INITIALIZE, UPDATE, TASK_BREAKDOWN, REBREAKDOWN, or SPLIT_TASK.
---

# Ralph Planning Artifact Templates

This skill centralizes the canonical Ralph-v2 planning artifacts so the Planner prompt can stay focused on judgment and decomposition.

## Core Artifacts

- `metadata.yaml`
- `iterations/<N>/metadata.yaml`
- `iterations/<N>/plan.md`
- `iterations/<N>/progress.md`
- `iterations/<N>/tasks/task-<id>.md`

## Session Metadata Template

```yaml
version: 1
session_id: <SESSION_ID>
created_at: <ISO8601>
updated_at: <ISO8601>
iteration: 1
orchestrator:
  state: PLANNING
  current_wave: null
tasks:
  total: 0
  completed: 0
  failed: 0
  pending: 0
session_review:
  cycle: 0
  issue_severity_threshold: "any"
  max_critique_cycles: null
```

## Iteration Metadata Template

```yaml
version: 1
iteration: <N>
started_at: <ISO8601>
planning_complete: false
planning_completed_at: null
completed_at: null
tasks_defined: 0
```

## Plan Template

```markdown
# Plan - Iteration <N>

## Goal
[Concise goal]

## Success Criteria
- [ ] SC-1: [Measurable criterion]

## Target Files
| File | Role | Changes Expected |
|------|------|------------------|

## Context
[Background and constraints]

## Approach
[Strategy and key decisions]

## Waves
| Wave | Tasks | Rationale |
|------|-------|-----------|

## Grounding
[Q-IDs and Issue-IDs that justify the plan]
```

## Progress Template

```markdown
# Progress

## Legend
- `[ ]` Not started
- `[/]` In progress
- `[P]` Pending review
- `[x]` Completed
- `[F]` Failed
- `[C]` Cancelled

## Planning Progress (Iteration <N>)
- [ ] plan-init
- [ ] plan-brainstorm
- [ ] plan-research
- [ ] plan-breakdown

## Implementation Progress (Iteration <N>)
[To be filled]
```

## Task File Template

```markdown
---
id: task-1
iteration: <N>
wave: 1
type: Sequential
created_at: <ISO8601>
updated_at: <ISO8601>
---

# Task: task-1

## Title
[Short title]

## Files
- path/to/file

## Objective
[What this task achieves]

## Grounded In
- Q-000
- ISS-000

## Success Criteria
- [ ] [Measurable criterion]

## Dependencies
depends_on: []
inherited_by: []
```

## Decomposition Rules

- Every task needs at least 2 grounding references, including at least 1 Q-ID.
- `wave` is required for Orchestrator batch routing.
- Prefer parallel waves; add dependencies only when correctness requires them.
- Split oversized tasks into 2-4 narrower tasks while preserving dependency semantics.