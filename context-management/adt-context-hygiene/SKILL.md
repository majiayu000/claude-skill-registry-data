---
name: context-hygiene
description: Keep sessions focused and efficient — prune stale outputs, preserve active state, recommend compaction
triggers:
  - clean context
  - session bloated
  - context too long
  - prune session
  - switch task
---

# Context Hygiene

Identify what must stay active, mark stale outputs for removal, and decide whether to compact or start a fresh session.

## Steps

1. **Identify active state** — current task, files, decisions that must be preserved
2. **Mark stale content** — completed threads, resolved questions, old tool outputs
3. **Decide action** — compact current session or recommend a fresh session
4. **Preserve explicitly** — write down active task state before any pruning

## Output

```text
Keep:    <active task, key files, open decisions>
Prune:   <stale outputs, resolved threads>
Action:  compact | fresh session
```

## Rules

- Never compact away active task state
- Never preserve irrelevant historical chatter
- Write active state explicitly before recommending a fresh session
- Prefer compaction when the active task is still in progress
