---
name: agentmemory
description: Persistent cross-session memory for AI coding agents. Use when working across multiple sessions, recalling past context, saving decisions, or searching historical observations.
---

# Agentmemory Skill

Provides persistent memory capabilities for coding agents using the agentmemory MCP server.

## When to Activate

- Starting a new session that builds on previous work
- User asks "remember this", "do you recall", "what did we do last time"
- Before making architectural decisions that past context could inform
- After discovering a bug, to save the pattern for future prevention
- After making a design decision, to persist the rationale
- When the user asks about project history or session timeline

## Core Tools

### memory_save
Save an insight, decision, or fact to long-term memory.

```
memory_save(
  content: "We chose jose over jsonwebtoken for Edge Runtime compatibility",
  concepts: ["jwt-auth", "edge-runtime", "jose-library", "auth-middleware"],
  files: ["src/middleware/auth.ts"],
  type: "architecture"
)
```

### memory_recall
Search past observations by exact keywords.

```
memory_recall(query: "jwt auth setup", limit: 5)
```

### memory_smart_search
Hybrid semantic+keyword search. Use for fuzzy or conceptual queries.

```
memory_smart_search(query: "how did we handle database performance", limit: 10)
```

### memory_sessions
List recent sessions with status and observation counts.

```
memory_sessions(limit: 10)
```

### memory_file_history
Get past observations about specific files across all sessions. Call before editing a file.

```
memory_file_history(files: ["src/middleware/auth.ts"])
```

### memory_lesson_save / memory_lesson_recall
Save and retrieve lessons learned with confidence scoring.

```
memory_lesson_save(
  content: "Always validate JWT expiry before decoding payload",
  concepts: ["jwt-validation", "security"],
  domain: "backend"
)
memory_lesson_recall(query: "jwt security", limit: 5)
```

### memory_governance_delete
Delete specific memories. Requires explicit user confirmation.

### memory_patterns
Detect recurring patterns across sessions.

### memory_consolidate
Run the 4-tier memory consolidation pipeline.

## Behavior Rules

1. **Proactive recall**: Before implementing new features or fixing bugs, check agentmemory for relevant past context.
2. **Auto-save**: After discovering a bug, making an architectural decision, or learning a project convention, save it.
3. **Session awareness**: Use `memory_sessions` when the user asks about project history or past work.
4. **File context**: Use `memory_file_history` before editing files to surface past issues or decisions about that file.
5. **Never hallucinate**: Only present what the MCP tools return. Report "no results found" when appropriate.
6. **Tool prefix**: All agentmemory tools use the `agentmemory_memory_` prefix in the tool list. Use the exact names as listed.

## Integration Notes

- Server runs on `http://localhost:3111` by default
- Real-time viewer at `http://localhost:3113`
- Start the server with `npx @agentmemory/agentmemory`
- 53 MCP tools available when server is running
- 22 auto-capture hooks via plugin record session lifecycle automatically
