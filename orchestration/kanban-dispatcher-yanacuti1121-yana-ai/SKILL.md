---
name: kanban-dispatcher
description: SQLite task board for structured multi-agent parallelization. Workers claim tasks, send heartbeats, request approval gates, and spawn child tasks. Use when orchestrating 3+ parallel agents on a complex project with dependencies.
license: MIT
source: https://github.com/NousResearch/hermes-agent
---

# Kanban Dispatcher

Structured task board that prevents parallel agents from stepping on each other. Each worker claims one task, heartbeats to stay alive, and can spawn child tasks.

**Trigger phrases:** "parallel tasks", "kanban", "task board", "orchestrate agents", "dispatch workers", "multi-agent project"

---

## Core State Machine

```
PENDING → IN_PROGRESS (worker claims)
       → BLOCKED (needs human input)
       → DONE (worker completes)
       → FAILED (worker errors)
```

---

## Worker Contract

Every worker agent MUST follow this sequence:

```python
# 1. Show current task at session start
kanban_show()

# 2. Heartbeat every 2-3 tool calls (proves liveness)
kanban_heartbeat(note="Running tests in src/auth/")

# 3. If blocked, surface to human
kanban_block(reason="Missing API key — need STRIPE_SECRET_KEY in .env")

# 4. Spawn child task if work decomposes
kanban_create(
    title="Fix type errors in auth module",
    assignee="implementer",
    parents=["TASK-001"],           # blocks parent until done
    context="See src/auth/types.ts line 42"
)

# 5. Complete with structured output
kanban_complete(
    summary="Implemented OAuth2 flow, 14 tests pass",
    metadata={"files_changed": ["src/auth/oauth.ts"], "tests_added": 14}
)
```

---

## Orchestrator Pattern

```python
# Create task board
kanban_create(title="Implement user auth", assignee="implementer")
kanban_create(title="Write auth tests",    assignee="tester",      parents=["TASK-001"])
kanban_create(title="Auth code review",    assignee="reviewer",    parents=["TASK-002"])

# Dispatch workers in parallel
delegate_task(goal="Work the kanban board as implementer", role="implementer")
delegate_task(goal="Work the kanban board as tester",      role="tester")

# Workers auto-sequence via parent dependencies
# tester waits for implementer to complete TASK-001
# reviewer waits for tester to complete TASK-002
```

---

## Approval Gate

```python
kanban_request_approval(
    task_id="TASK-003",
    summary="About to apply irreversible migration — please confirm",
    context="Backup at /tmp/backup.sql"
)
# Worker blocks here until human calls kanban_approve("TASK-003")
```

---

## Heartbeat Protocol

Workers MUST heartbeat — stale tasks get reclaimed after 5 minutes:

```python
# Call every 2-3 tool calls during long operations
kanban_heartbeat(note="Still running cargo build...")
```

---

## Task Roles

| Role | Toolsets | Focus |
|------|----------|-------|
| `implementer` | terminal, file | Write code, run tests |
| `tester` | terminal, file | Write tests, verify coverage |
| `reviewer` | read-only | Spec compliance + code quality |
| `documenter` | file | Update docs, changelogs |

---

## Anti-Fake-Pass

```
❌ Worker never heartbeats — task reclaimed after timeout
❌ Completing task before child tasks finish
❌ > 3 levels of child task nesting
❌ Blocking without a human-resolvable question
❌ Summary "done" — not a summary
```

## See Also
- `core/skills/claude-swarm-orchestration/SKILL.md` — auto-decompose approach
- `core/skills/subagent-dependency/SKILL.md` — DAG-based orchestration
