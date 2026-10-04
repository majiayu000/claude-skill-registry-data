---
name: agent-teams
description: Decompose a task into parallel workstreams, assign agent ownership, run integration at dependency boundaries, and synthesize results.
triggers:
  - decompose multi-agent work
  - plan parallel agent teams
  - run multi-agent workflow
---

# Agent Teams

Coordinate multiple agent sessions for parallel implementation, review, and synthesis. Use when the task can be safely decomposed into concurrent workstreams with clear handoffs and one integrator.

## When to Use

- The task is large enough that parallel work will save time or add confidence.
- Independent workstreams can be defined with clear inputs, outputs, and ownership.
- One lead agent can own synthesis, integration, and final verification.

## When NOT to Use

- The task is small, tightly coupled, or faster to complete in one session.
- Multiple agents would fight over the same files or the same mutable context.
- The user wants one narrow implementation rather than orchestration.

## Core Patterns

### Team Structure

1. **Define independent workstreams** — Each track has owner, expected output, handoff condition, and dependencies.
2. **Assign lead integrator** — One agent maintains the task board, resolves blockers, and synthesizes results.
3. **Bounded prompts per agent** — Each agent gets files, constraints, and stop conditions.
4. **Sync at dependency boundaries only** — Not continuously; sync when one track's output feeds another.
5. **Validate together** — Recombine the work, rerun required validation, report integrated outcome.

### Workflow

1. Decide whether parallelism buys time, confidence, or separation of concerns.
2. Split the work into independent tracks with owner, expected output, and handoff condition.
3. Pick a lead agent to maintain the task board, resolve blockers, and synthesize results.
4. Give each agent a bounded prompt with files, constraints, and stop conditions.
5. Run sync points only at dependency boundaries, not continuously.
6. Recombine the work, rerun the required validation, and report the integrated outcome.

## Rules

1. Stop if the task cannot be decomposed without heavy coordination overhead.
2. Stop if no agent can own final integration and verification.
3. Do not use parallel agents as a substitute for a missing implementation plan.
4. Sync points occur only at dependency boundaries, not on a fixed schedule.
5. The lead integrator must verify the combined output against success criteria before declaring done.

## Related Skills

- `adt-orchestrate` — Composite orchestration skill for phased workflows
- `adt-parallel-investigate` — Parallel investigation pattern for multi-agent research
- `adt-route` — Route sub-agents to the right tier
- `team-coordinator` — Alias for agent-teams
