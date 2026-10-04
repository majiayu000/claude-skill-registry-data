---
name: mission-control-record-memory
description: >-
  Persists agent knowledge across sessions using the Mission Control agent
  documents system. Use this skill when depositing session memory before
  shutting down, keeping a WORKING_MD scratchpad up to date, writing daily
  notes, or reading back previously stored memories at session start.
version: 1.0.0
owner: software-factory
risk: low
capabilities:
  - memory-deposit
  - memory-retrieval
  - session-persistence
requires_tools:
  - convex
related_skills:
  - mission-control-register-agent
  - mission-control-heartbeat
---

# Deposit Memories

Persist knowledge across sessions using the agent documents system.

## Write a Memory

```
Mutation: api.agentDocuments.upsert (or create)
Args:
  agentId: Id<"agents">
  type: "WORKING_MD" | "DAILY_NOTE" | "SESSION_MEMORY"
  content: string
  projectId?: Id<"projects">
```

## Read Your Memories

```
Query: api.agentDocuments.getByAgent
Args: { agentId: Id<"agents"> }
```

## Rules

1. **Deposit memories** — persist important context for future sessions; deposit `SESSION_MEMORY` before shutting down.
2. Read your memories back at session start, right after registering.
3. Use `WORKING_MD` for the living scratchpad, `DAILY_NOTE` for day summaries, `SESSION_MEMORY` for handoff context.
