---
name: task-handoff
description: "Tier-A structured agent handoff protocol — no new infrastructure required, just discipline with the shared task store as the single coordination layer. When Agent A completes work that unblocks Agent B, Agent A writes outcome and next steps to the task store, creates Agent B's task, marks its own done, and moves on. Conversation context is not a handoff mechanism. Trigger when: an agent finishes a task and needs to unblock a downstream agent; you need to pass work between agents in a multi-step pipeline; you are setting up a multi-agent workflow and want to define explicit ownership boundaries; the user asks how to hand off work between agents. Key capabilities: the task store is the only source of truth (not memory, not chat history); blocked status is a hard gate that prevents work from starting; handoff is explicit and auditable (each agent writes before spawning the next); failure propagates upward if a downstream agent exhausts retries. Also for: establishing team conventions for how agents should communicate before Tier-B (file-based FIFO queue) is introduced; auditing a pipeline to see where work actually stalled; setting up governance gates between phases (e.g. design → dev → QA → ship). Ideal for any multi-agent workflow where one agent's output feeds into another agent's input."
---

Tier-A structured agent handoff — no new infrastructure, just discipline with the task store. The task store is the coordination layer; conversation context is not.

## Protocol

When Agent A completes work that unblocks Agent B:

1. **Agent A writes its outcome to the task store** — status, findings, any blockers, next steps
2. **Agent A creates Agent B's task** in the task store with `assigned_agent` set
3. **Agent A marks its own task `done`** and records the handoff ID in `notes`
4. **Agent B reads from the task store** to find its assignment — not from memory or conversation

## Example: Feature implementation → QA review

```
# Agent A (dev): marks feature done, creates QA task
ts-create "myproject" "qa-review-api" "QA the REST API implementation" "phase1" "high"
# -> returns downstream_id

# Agent A sets blocked_by to empty (upstream gates were cleared)
sqlite3 ~/.claude/task-store.db "UPDATE tasks SET blocked_by='[]' WHERE id='$downstream_id'"

# Agent A marks own task done
ts-status "$upstream_id" "done"

# Agent B (QA): reads task store for its assignment
ts-project "myproject" | grep "qa-review-api"
# -> finds task, starts work

# After QA, Agent B writes gate verdict
ts-gate "$feature_task_id" "passed" "qa-agent"
```

## Key Rules

- **Task store is the source of truth** — not conversation, not memory
- **`blocked` status is a hard gate** — never advance to `in_progress` while blocked
- **Handoffs are explicit** — always write to task store before spawning downstream
- **Failure propagates** — if Agent B fails after retries, escalate to PD/council

## Anti-patterns

- Spawning an agent without checking the task store first
- Storing state in conversation context (it gets lost between sessions)
- Advancing a blocked task to `in_progress`
- Skipping gate verification for "quick" downstream tasks

## Relationship to Tier-B (future)

Tier-B adds a file-based FIFO queue (`~/.claude/agency-rooms/{room}/queue/`) so agents can poll asynchronously. Tier A is the prerequisite — implement this first to establish the discipline.
