---
name: task-system
description: "File-backed task management with dependencies and parallel execution. Use for complex work with 3+ interdependent tasks."
context: fork
globs: []
alwaysApply: false
---

# Task System — File-Backed Task Management

Use this skill for complex work with multiple interdependent tasks. Tasks are stored as JSON files, survive session restarts, and support automatic parallel execution based on dependency graphs.

---

## When to Use

| Scenario | Use |
|----------|-----|
| 1-2 simple tasks | TodoWrite |
| 3+ tasks with dependencies | **Task System** |
| Tasks need to survive restart | **Task System** |
| Parallel execution needed | **Task System** |
| Multiple agents collaborating | **Task System** |

---

## Task Schema

```json
{
  "id": "T-001",
  "subject": "Build frontend",
  "description": "Implement ReviewCard component with mocked data",
  "status": "pending",
  "activeForm": "Building ReviewCard component",
  "blockedBy": [],
  "blocks": ["T-003"],
  "owner": "Aphrodite",
  "metadata": {},
  "threadID": "session-abc",
  "timeout_ms": 180000,
  "retry_policy": { "count": 3, "backoff": "exponential" },
  "fallback_agent": "talos",
  "partial_ok": false,
  "session_id": null,
  "session_resume": null
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Auto-generated: `T-{sequential}` |
| `subject` | string | Yes | Imperative: "Run tests", "Build component" |
| `description` | string | Yes | Detailed description of the task |
| `status` | enum | Yes | `pending`, `in_progress`, `completed`, `deleted` |
| `activeForm` | string | No | Present continuous: "Running tests" |
| `blockedBy` | string[] | Yes | Task IDs that must complete first |
| `blocks` | string[] | Yes | Task IDs that this task blocks |
| `owner` | string | No | Agent name responsible |
| `metadata` | object | No | Additional context |
| `threadID` | string | Yes | Session ID (auto-set) |
| `timeout_ms` | integer | No | Timeout in milliseconds for this task (default: 120000 = 2min). 0 = no timeout |
| `retry_policy` | object | No | `{ count: number, backoff: "exponential"\|"fixed" }`. Default: `{ count: 3, backoff: "exponential" }` |
| `fallback_agent` | string | No | Agent name to use if all retries fail. Default: null (escalate to Zeus) |
| `partial_ok` | boolean | No | If true, partial results are acceptable on timeout. Default: false |
| `session_id` | string | No | Alias of the session running this task (e.g. "hermes-1"). Set automatically |
| `session_resume` | string | No | Session alias to resume instead of starting fresh (e.g. "hermes-1") |

---

## Storage

Tasks are stored as JSON files:
```
.pantheon/tasks/
├── T-001.json
├── T-002.json
├── T-003.json
└── ...
```

**Persistence:** Tasks survive session restarts. Delete manually when feature is merged.

---

## Dependency Graph & Parallel Execution

Tasks with empty `blockedBy` run in parallel. Dependent tasks wait until blockers complete.

```
[Build Frontend]    ──┐
                      ├──→ [Integration Tests] ──→ [Deploy]
[Build Backend]     ──┘
```

**Execution flow:**
```
1. T-001 (blockedBy: []) → runs immediately
2. T-002 (blockedBy: []) → runs immediately (parallel with T-001)
3. T-003 (blockedBy: [T-001, T-002]) → waits for both
4. When T-001 + T-002 complete → T-003 unblocks automatically
5. T-004 (blockedBy: [T-003]) → waits for T-003
```

---

## Task Lifecycle

### Create
```
TaskCreate({
  subject: "Build frontend",
  description: "Implement ReviewCard with mocked data",
  blockedBy: [],
  blocks: ["T-003"],
  owner: "Aphrodite"
})
→ Returns: { id: "T-001", ... }
```

### Update
```
TaskUpdate({
  id: "T-001",
  status: "in_progress",
  activeForm: "Building ReviewCard component"
})
```

### List
```
TaskList()
→ Returns all active tasks with status:
  T-001 [in_progress] Build frontend        blockedBy: []
  T-002 [pending]     Build backend         blockedBy: []
  T-003 [pending]     Integration tests     blockedBy: [T-001, T-002]
```

### Get
```
TaskGet({ id: "T-001" })
→ Returns full task object
```

---

## Difference from TodoWrite

| Feature | TodoWrite | Task System |
|---------|-----------|-------------|
| Storage | Session memory | File system (`.pantheon/tasks/`) |
| Persistence | Lost on close | Survives restart |
| Dependencies | None | Full support (`blockedBy`) |
| Parallel execution | Manual | Automatic optimization |
| Multi-agent | Single agent | Multiple agents with owners |
| Best for | Simple sequential work | Complex interdependent work |

---

## Timeout & Retry

Every task can have timeout and retry policies:

```json
{
  "timeout_ms": 180000,
  "retry_policy": { "count": 3, "backoff": "exponential" },
  "fallback_agent": "talos"
}
```

### How it works:

1. Task starts → timeout timer begins
2. If timeout expires → retry with backoff:
   - Exponential: 5s, 15s, 45s (multiply by 3 each retry)
   - Fixed: 10s, 10s, 10s (constant delay)
3. If all retries fail → use `fallback_agent` if configured
4. If no fallback → escalate to Zeus (user decision)

### Partial results (partial_ok: true):

If a task times out but `partial_ok` is true, Zeus can use whatever results were produced and re-delegate the remaining scope.

---

## Session Reuse

Tasks can resume previous sessions to avoid re-reading context:

```json
{
  "session_resume": "hermes-1",
  "session_id": "hermes-2"
}
```

- `session_id` — set automatically when a task starts (alias: `{agent}-{N}`)
- `session_resume` — set manually to continue from a previous session

Session aliases are tracked in-memory by Zeus during a session. Stale references auto-clean.

---

## Example: Full Workflow

```
Zeus creates tasks for "Add Product Reviews":

TaskCreate({ subject: "Create reviews schema", owner: "Demeter" })
→ T-001

TaskCreate({ subject: "Implement POST /reviews", owner: "Hermes", blockedBy: ["T-001"] })
→ T-002

TaskCreate({ subject: "Implement GET /reviews", owner: "Hermes", blockedBy: ["T-001"] })
→ T-003

TaskCreate({ subject: "Build ReviewCard component", owner: "Aphrodite", blockedBy: ["T-001"] })
→ T-004

TaskCreate({ subject: "Integration tests", owner: "Hermes", blockedBy: ["T-002", "T-003", "T-004"] })
→ T-005

TaskList():
  T-001 [pending] Create reviews schema    blockedBy: []
  T-002 [pending] Implement POST /reviews  blockedBy: [T-001]
  T-003 [pending] Implement GET /reviews   blockedBy: [T-001]
  T-004 [pending] Build ReviewCard         blockedBy: [T-001]
  T-005 [pending] Integration tests        blockedBy: [T-002, T-003, T-004]

Execution:
  → T-001 runs (no blockers)
  → T-001 completes
  → T-002, T-003, T-004 unblock → run in parallel
  → All three complete
  → T-005 unblocks → runs
  → T-005 completes → all done
```

---

## Wisdom Accumulation Integration

When a task completes, extract learnings and pass to the next task:

```
T-001 complete → extract learnings → store in learnings.md
T-002 starts → inject learnings.md → avoids repeating T-001 mistakes
```

---

## Cleanup

After the feature is merged:
```
rm -rf .pantheon/tasks/T-*.json
rm -rf .pantheon/learnings/<feature>/
```

Tasks are temporary — they exist only for the duration of the feature implementation.
