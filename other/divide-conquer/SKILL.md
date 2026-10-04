---
name: divide-conquer
description: >
  Split a large task into independent subtasks, delegate them to child sessions
  for parallel execution, and merge the results. Use when a task can be broken
  into non-overlapping pieces that don't depend on each other's output.
  Not for consensus/review (use consensus-delegation) or benchmarks (use bench).
  Triggers: "분할 정복", "병렬 처리", "parallel execution", "split and process".
---

# Divide-Conquer

The Divide-Conquer pattern splits a complex task into independent subtasks, delegates them to parallel child sessions, collects their results, and merges them into a final output.

## 6-Stage Workflow

```
┌─────────────────────────────────────────────────────┐
│                    Parent Session                    │
│                                                      │
│  1. Decompose: break task into independent pieces    │
│  2. Assign: pick assistant(s) + workspace strategy   │
│  3. Spawn: batch children (respect concurrency limit)│
│  4. Monitor: poll/check each child                   │
│  5. Merge: assemble results into final output        │
│  6. Verify: final quality check                      │
└──────────┬──────────┬──────────┬─────────────────────┘
           │          │          │
     ┌─────▼─────┐ ┌─▼────────┐ ┌▼──────────┐
     │ Child 1   │ │ Child 2  │ │ Child N   │
     │ (Module A)│ │(Module B)│ │(Module C) │
     └───────────┘ └──────────┘ └───────────┘
```

1. **Decomposition**: Divide the task into non-overlapping, independent units. See [decomposition-rules.md](references/decomposition-rules.md).
2. **Assignment**: Assign subtasks to suitable assistants (homogeneous or heterogeneous). Before creating a child, inspect `agent__listAgents(type="sessions")` and reuse an Idle child with the same assistant ID when its workspace contract is compatible.
3. **Workspace Strategy**: Decide whether children share the parent workspace (`workspaceOverride`) or use isolated workspaces (**default: isolated** for plain `spawnSession`; org members inherit the org root unless overridden).
4. **Spawn & Monitor**: Spawn sessions in batches respecting the concurrency limit (default: `maxConcurrentActiveSessions` is 4).
5. **Merge**: Assemble output artifacts based on merge patterns. See [merge-patterns.md](references/merge-patterns.md).
6. **Verify**: Run build/tests to ensure integration integrity. Retries failed subtasks if needed. For strict proof-before-done (path invariants, reject/re-steer), follow **`delegation-eval-loop`** after `delegate` mechanics.

## 🛠️ MCP Tools Guide

- **Discovery**: Use `agent__listAgents(type="configs")` to find assistant IDs.
- **Delegation**: Use `agent__messageToSession(..., reset=true)` to assign fresh work to a suitable Idle matching-role child. Use `agent__spawnSession(..., waitForResult=false)` only when no suitable child exists, a different role or workspace is needed, or another parallel capacity slot is required.
- **Monitoring**: Check status via `agent__listAgents(type="sessions")` and wait for completion via `agent__checkSession(sessionId, wait=true)`.
- **Rework**: Use `agent__messageToSession(sessionId, message)` to wake/retry paused/error sessions.
- **Cancellation**: Use `agent__stopSession(sessionId)` to abort hung subtasks.

## ⚖️ `consensus-delegation` vs `divide-conquer`

| Aspect | Consensus Delegation | Divide-Conquer |
|--------|----------------------|----------------|
| **Goal** | Get multiple perspectives on one query | Complete a large task by dividing work |
| **Subtasks** | Same task, different angles (e.g. security, perf) | Different, non-overlapping work scopes |
| **Output** | Comparison, synthesis, final decision | Combined/merged physical artifacts |
| **Recovery** | Dialogue to resolve conflicts | Rework specific failed subtasks |
