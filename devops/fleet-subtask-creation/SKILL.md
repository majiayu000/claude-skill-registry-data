---
name: fleet-subtask-creation
description: How engineers know when and how to create subtasks for other agents — discovering docs/security/test gaps during work and routing them properly via fleet_task_create.
---

# Subtask Creation — Engineer's Delegation Skill

You're implementing a feature. You discover: there's no documentation for this API. Or: this touches authentication and needs security review. Or: the test coverage for this module is below 50%. These aren't YOUR tasks — they're tasks for other agents. Create subtasks.

## When to Create Subtasks

| Discovery | Target Agent | Subtask Type |
|-----------|-------------|-------------|
| Missing documentation | technical-writer | docs task |
| Security concern in code you're touching | devsecops-expert | security review |
| Test gap found during implementation | qa-engineer | test task |
| Infrastructure need (deployment, CI) | devops | infra task |
| UX concern in user-facing change | ux-designer | UX review |
| Design question needing architectural input | architect | design task |

## fleet_task_create vs fleet_request_input

**fleet_task_create** — Creates a full task on the board. Use when:
- The work is substantial (not a quick question)
- The other agent needs their own task lifecycle (stages, review)
- You want it tracked in the sprint

**fleet_request_input** — Creates a lightweight contribution request. Use when:
- You just need a quick answer or input
- The other agent can respond in one heartbeat cycle
- No separate task lifecycle needed

## How to Create a Proper Subtask

Follow the PM's triage discipline — set ALL fields:

```
fleet_task_create(
    title="Document: fleet_contribute API endpoint",
    description="The fleet_contribute MCP tool has no user-facing documentation. "
                "Need: endpoint reference, parameters, example usage, error codes.",
    agent_name="technical-writer",
    task_type="subtask",
    parent_task="your-task-id",    # Links to your task
    task_stage="reasoning",         # Writer will plan before writing
    task_readiness=80,
    story_points=2,
    delivery_phase="mvp",           # Match your task's phase
)
```

### The Fields That Matter

| Field | Why It Matters |
|-------|---------------|
| agent_name | Routes to the right specialist |
| parent_task | Links child to parent — fleet-ops reviews the relationship |
| task_type="subtask" | Skips contribution requirements (subtasks are small) |
| task_stage | Set based on clarity — if you know exactly what's needed, set to reasoning or work |
| story_points | Helps PM with sprint capacity |
| delivery_phase | Match your parent task's phase |

## The Cascade Depth Limit

The fleet has a maximum cascade depth of 3. Your subtask can have sub-subtasks, but no deeper:

```
Epic (depth 0)
├── Story (depth 1)
│   ├── Task (depth 2)
│   │   ├── Subtask (depth 3) ← maximum
│   │   └── Subtask (depth 3)
│   └── Task (depth 2)
```

If `fleet_task_create` with a parent at depth 3 is called, it will be blocked with a cascade error.

## After Creating

1. Post a comment on your own task noting the subtask: "Created subtask for docs: {task_id}"
2. Continue your work — don't wait for the subtask unless it blocks you
3. If the subtask IS blocking (you need security clearance before proceeding): `fleet_pause(reason="Waiting for security review subtask {id}")`

## What NOT to Create Subtasks For

- **Things you should do yourself** — writing your own tests, writing inline comments, running linters
- **Questions you can answer** — don't create a task just to ask "how does this work?" Use code-explorer sub-agent.
- **PM work** — don't create task management subtasks. PM handles triage and assignment.
- **Scope expansion** — if you're discovering new features during implementation, that's scope creep. `fleet_escalate` to PM/PO.
