---
name: context
description: Optimize context window usage — compact stale data, compress via summarization, preserve active state
triggers:
  - optimize context
  - context too large
  - compact
  - session slow
  - free up context
  - context pressure
---

# Context

Keep the context window focused on what matters right now.

## When to Use

- Session feels slow or responses degrade
- Switching between unrelated tasks
- After completing a major task and pivoting
- Context approaching 60–70% capacity

## Compression Strategies

Choose based on how much to recover:

| Strategy                                                        | Savings | Risk   |
| --------------------------------------------------------------- | ------- | ------ |
| **Prune** — drop tool outputs, resolved threads                 | 10–30%  | Low    |
| **Summarize** — replace resolved subtasks with 3-bullet summary | 30–60%  | Low    |
| **Checkpoint** — save state to file, fresh session              | 100%    | Medium |

### Summarize pattern

Replace a completed subtask block with:

```markdown
## [SUMMARIZED] Auth refactor — 2026-04-10

- Replaced JWT middleware with JWKS-based validation
- 3 new tests; all green
- Gotcha: validateToken() is now async
```

### Checkpoint pattern

When severely bloated, save state before starting fresh:

```text
.agents/plans/checkpoint-<date>.md:
  - Active task: <what you're doing>
  - Branch: <name>
  - Completed: <bullet list>
  - Next step: <exact next action>
  - Key decisions: <anything not in git>
```

## Context Prioritization

Keep in context (highest priority first):

1. Current task and next step
2. Active file contents being modified
3. In-progress plan and pending items
4. Key decisions not yet committed
5. Recent error messages (if debugging)

Drop first:

1. Old search results and grep outputs
2. File reads that are no longer being modified
3. Completed todo items and resolved threads
4. Verbose tool execution logs

## Steps

1. Estimate current context usage (% of limit)
2. Identify stale context using the drop-first list above
3. Apply the appropriate compression strategy
4. Verify active state preserved: branch, files, plan, decisions
5. Report what changed

## Output

```text
Before: ~N% used
Compacted: <what was removed>
After: ~N% used
Preserved: <key items kept>
Checkpoint: <file path if saved>
```

## Rules

- Never compact active task state
- Preserve: current branch, active files, in-progress plan, key decisions
- Remove: old search outputs, completed todos, resolved threads
- At 80%+ capacity: checkpoint immediately, don't wait for degradation
- Save critical state to a plan file before compacting if work is in progress
