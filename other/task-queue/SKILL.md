---
name: mk:task-queue
description: Task claiming and ownership tracking for parallel agent execution. Agents claim tasks from a shared queue with file ownership enforcement. Use during parallel execution phases when multiple agents work simultaneously.
source: local
keywords:
  - task-queue
  - ownership-tracking
  - parallel-execution
  - claim-task
  - file-ownership
when_to_use: Auto-invoked when multiple agents claim tasks during parallel execution. Not user-callable directly.
user-invocable: false
owner: git
criticality: medium
status: active
runtime: claude-code
---

# Task Queue & Ownership Tracker

Manages task assignment and file ownership during parallel execution.

## Task Queue

Tasks are tracked in `session-state/task-queue.json`:

```json
{
  "tasks": [
    {
      "id": 1,
      "description": "Implement API endpoints",
      "owner": null,
      "status": "pending",
      "ownership": ["src/api/*", "src/routes/*"],
      "blocked_by": []
    },
    {
      "id": 2,
      "description": "Implement UI components",
      "owner": null,
      "status": "pending",
      "ownership": ["src/components/*", "src/pages/*"],
      "blocked_by": []
    }
  ]
}
```

## Task Lifecycle

```
pending → claimed (agent assigned) → in_progress → completed
                                   → blocked (dependency not met)
```

## Claiming Protocol

1. Agent requests next available task
2. Queue returns lowest-ID task where: `status=pending` AND `blocked_by` all completed
3. Agent declares ownership globs
4. Queue checks for overlap with other in_progress tasks
5. If overlap: REJECT claim, report conflict to orchestrator
6. If no overlap: ASSIGN task, set `status=in_progress`, record `owner`

## Ownership Enforcement

Each task declares file ownership via glob patterns.
Before any file write, check if the file matches the agent's declared ownership.

| Action | Owned File? | Result |
|--------|------------|--------|
| Read | Any | Always allowed |
| Write/Edit | Owned | Allowed |
| Write/Edit | Not owned | STOP — report ownership violation |
| Write/Edit | Overlapping | STOP — report conflict to orchestrator |

## Integration

- **Orchestrator** creates the task queue when decomposing parallel work
- **Parallel agents** claim and complete tasks
- **Orchestrator** monitors queue for completion and triggers integration test
- Queue is ephemeral (session-state/) — recreated per parallel execution

## Team Coordination

Team-mode coordination rules (file ownership, commit discipline, completion messages) live
in `.claude/skills/team-config/references/team-coordination.md`, loaded by `mk:team-config`
on team activation.

## Gotchas

- **Race condition on claims:** Two agents reading `task-queue.json` simultaneously may both claim the same task. Mitigation: orchestrator is the sole claim-serializer — agents REQUEST claims through orchestrator, never self-claim directly
- **Ownership globs must not overlap:** `src/api/*` and `src/api/auth/*` overlap — the more specific glob must be in the SAME task, not split across agents
- **Queue file doesn't auto-create:** Orchestrator must create `session-state/task-queue.json` before dispatching parallel agents. If missing, agents should STOP and report, not create it themselves
- **Completed tasks are not removed:** Tasks stay in queue with `status=completed` for audit trail. Queue is cleaned up only when the parallel execution phase ends
