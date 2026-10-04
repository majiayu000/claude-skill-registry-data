---
name: memory-recall
description: >
  Retrieve task-relevant project and global memory without loading everything.
  Load when the user asks what we decided, recall prior context, find memory
  about a feature, explain past rationale, resume a task, or check deferred ideas.
license: MIT
metadata:
  author: dvy1987
  version: "1.2"
  category: project-specific
  resources:
    references:
      - examples.md
---

# Memory Recall

You retrieve the smallest useful memory slice for the task. Your job is relevance, not exhaustive history.

## Workflow

1. Identify the recall target: feature, decision, bug, user preference, deferred option, learning, or session.
2. Read `docs/memory/MEMORY-ROUTING.md` and `docs/memory/project-index.md`.
2.5. If `docs/knowledge-graph/graph.json` exists, run `query_graph.py` with recall topic — add matching memory/skill paths to candidates.
3. Select candidate files and sections by tags, status, date, and scope.
4. Read only selected sections from project memory.
5. If user preferences or global process rules may matter, read `~/.agent-loom/memories/MEMORY-ROUTING.md` and `global-index.md`.
6. Pull only applicable global entries.
7. Return a concise summary with source paths.
8. Flag contradictions, stale entries, and triggered revisit conditions.

## Retrieval Priority

1. Current state and latest handoff.
2. Active decisions with matching tags.
3. Deferred items and open questions.
4. Learnings relevant to the task.
5. Session history only if the above is insufficient.
6. Global preferences/rules only if task-relevant.

## Hard Rules

- Do not load full logs by default.
- Do not treat archived or superseded memory as current.
- Do not hide uncertainty; if memory is stale, say so.
- Do not write memory during recall unless the user also asks to update it.

## Output Format

```markdown
Memory recalled for: <topic>
Sources: <paths/sections>
Relevant context:
- <fact with source>
Decisions:
- <decision/status/revisit trigger>
Deferred / open:
- <item or none>
Staleness / contradictions:
- <issue or none>
```

## Example

User: "Why did we choose local and global memory?"

Output: summarize the decision, cite `decision-log.md`, include alternatives, and list revisit triggers.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| Skip memory — just code | Next agent loses decisions, blockers, and approved scope. |
| Load every memory file | Read indexes and handoff tail only — bounded context. |
| Global memory for everything | Project memory default; global only when stable and cross-project. |
| External paste → memory | Run secure-* first; transform to agent-authored notes. |

## Verification

- [ ] Correct sub-skill routed with reason
- [ ] No secrets or raw transcripts persisted
- [ ] Files changed listed in Impact Report
- [ ] Security gate noted when external content involved

## Red Flags

- Full agent-handoffs or session-log loaded by default
- Superseded decision presented as current policy
- Stale memory cited without flagging uncertainty
- Recall bypasses MEMORY-ROUTING intent table

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

After completing, report:
```markdown
Recall complete
Topic: <topic>
Files read: <count>
Relevant entries: <count>
Stale entries: <count>
Writes performed: none
```
