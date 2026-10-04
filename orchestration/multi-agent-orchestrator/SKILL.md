---
name: multi-agent-orchestrator
description: "Coordinate multi-agent workflows end to end. Use when a task should be decomposed into parallel sub-work with explicit ownership, dependency ordering, collision avoidance, checkpoint tracking, and final output recomposition."
---

# Multi Agent Orchestrator

## Outcome

Produce a clear execution map so multiple agents can run in parallel without conflicting edits or unclear ownership.

## Orchestration Loop

1. Define mission, success criteria, constraints, and non-goals.
2. Build a dependency graph of independent work packets.
3. Assign one owner per packet with explicit file and responsibility boundaries.
4. Launch packets with exact acceptance tests and return format.
5. Monitor execution, unblock quickly, and re-route when assumptions break.
6. Integrate outputs in dependency order and run final verification.

## Work Packet Contract

For every packet, specify:

- `task_id`
- `owner_role`
- `goal`
- `inputs`
- `allowed_paths`
- `blocked_paths`
- `dependencies`
- `commands_or_tools`
- `done_criteria`
- `return_format`

## Decomposition Rules

- Keep packets small enough to complete in one focused cycle.
- Split by ownership boundaries, not arbitrary file counts.
- Isolate shared files to integration packets whenever possible.
- Prefer many independent packets over one broad packet with ambiguous scope.

## Escalation Rules

- Re-scope immediately if an agent touches unassigned files.
- Pause parallelization if packets contend for the same mutable artifact.
- Create a new packet for new requirements instead of changing goals mid-run.

## Integration Checklist

1. Confirm every packet met `done_criteria`.
2. Validate cross-packet compatibility and interfaces.
3. Run combined tests or end-to-end verification steps.
4. Publish one merge-ready summary with open risks.
