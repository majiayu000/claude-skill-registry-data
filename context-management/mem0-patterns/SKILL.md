---
name: mem0-patterns
last_updated: 2026-05-17
description: "Mem0 episodic memory write/read patterns for Beamix agents: mandatory metadata fields, retry policy, and fallback to Anthropic Memory Tool after 3 failures. Use when any C-suite or lead agent reads or writes episodic memory during pre-flight or post-task."
tags: [memory, beamix-specific, agents, ai]
source: beamix-authored 2026-05-16
risk: low
---

# Mem0 Patterns

## Quick reference

> Mem0 = retrieve-then-write. Always recall before deciding. Anthropic Memory Tool auto-fallback after 3 retries. Vendor lock-in review 2026-11-16.

## When to use

- Writing post-task episodic memory from any C-suite or lead agent
- Reading memories during pre-flight (before executing any task)
- Diagnosing memory retrieval misses or stale facts
- Implementing the retry-with-fallback pattern

## When NOT to use

- For workers (workers do not write to Mem0 directly — parent C-suite writes)
- For code snippets or schema (use pgvector RAG corpus instead)
- For observability data (use `audit_log` table)
- When the information belongs in `DECISIONS.md` (architectural choices go there, not Mem0)

## Mandatory metadata fields

Every Mem0 write MUST include all four fields. Writes missing any of these are rejected by the Beamix wrapper.

```typescript
interface Mem0WriteMetadata {
  source: string;        // format: "{agent_id}+{session_id}+{input-hash}"
  confidence: 'high' | 'medium' | 'low';
  expires_at: string | null;  // ISO date or null (null = never expires)
  agent_id: string;      // which agent wrote this memory
  session_id: string;    // the originating session identifier
}
```

## Write pattern (post-task)

Call after the task is complete, before returning JSON to parent.

```typescript
// Any C-suite agent — post-task write
import { mem0Client } from '@/lib/mem0';

await mem0Client.add({
  user_id: 'adam',
  agent_id: 'cto',
  session_id: currentSessionId,
  app_id: 'beamix',
  messages: [
    {
      role: 'system',
      content: 'CTO decided to use Inngest over Trigger.dev for war-room fan-in durability. Reason: already in stack, free 50K runs/mo, no new vendor.',
    },
  ],
  metadata: {
    source: `cto+${currentSessionId}+${inputHash}`,
    confidence: 'high',
    expires_at: null,  // architectural decision — never expires
    agent_id: 'cto',
    session_id: currentSessionId,
  },
});
```

### Expiry heuristics

| Fact type | expires_at |
|-----------|-----------|
| Architectural decision | `null` (never) |
| Pricing / vendor cost | `+6 months` (costs change) |
| Customer quote / preference | `+90 days` |
| Low-confidence inference | `+30 days` |
| Session context | `+7 days` |

## Read pattern (pre-flight)

Read during pre-flight, BEFORE executing task logic. Use semantic search — never retrieve all memories.

```typescript
// Any C-suite agent — pre-flight read
const memories = await mem0Client.search({
  user_id: 'adam',
  agent_id: 'cto',       // filter by own agent_id by default
  query: taskSummary,    // the incoming ticket title or intent
  limit: 5,              // never more than 5 — keeps prompt tight
});

// Cross-agent read (e.g., CEO reading CTO memories for synthesis)
const crossAgentMemories = await mem0Client.search({
  user_id: 'adam',
  // agent_id omitted → searches across all agents
  query: 'scan rate limit implementation',
  limit: 3,
});
```

## Retry policy with fallback

Mem0 is a cloud dependency. Treat it as potentially unavailable.

```typescript
async function writeWithFallback(payload: Mem0Payload): Promise<void> {
  let attempt = 0;
  const MAX_RETRIES = 3;

  while (attempt < MAX_RETRIES) {
    try {
      await mem0Client.add(payload);
      return;
    } catch (err) {
      attempt++;
      if (attempt === MAX_RETRIES) {
        // Fallback: write to Anthropic Memory Tool
        // This uses the in-session memory, not cloud persistence
        console.warn('[mem0] Failed after 3 retries. Falling back to Anthropic Memory Tool.');
        // Write key fact as a structured memory in the current session
        // Format: "MEMORY: {agent_id} | {fact} | confidence:{confidence} | expires:{expires_at}"
        break;
      }
      await new Promise(r => setTimeout(r, 500 * attempt)); // linear backoff
    }
  }
}
```

The fallback (Anthropic Memory Tool) is in-session only — it does not persist across sessions. Log the fallback in `audit_log` with `status: mem0_fallback` so the watcher knows to retry the write.

## Supabase write-ahead queue (Phase 3 — not yet implemented)

When Mem0 is unavailable, a pending write can be queued in Supabase:

```sql
-- mem0_pending_writes table (design, not yet live)
CREATE TABLE mem0_pending_writes (
  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id    text NOT NULL,
  session_id  text NOT NULL,
  payload     jsonb NOT NULL,
  attempts    int DEFAULT 0,
  last_error  text,
  created_at  timestamptz DEFAULT now()
);
```

Inngest `mem0-retry` function drains this queue. Not implemented in MVP — fallback to Anthropic Memory Tool is the current pattern.

## What NOT to store in Mem0

| Data type | Correct store |
|-----------|--------------|
| Code snippets, function signatures | pgvector `rag_corpus` (codebase corpus) |
| Every tool call output | `audit_log` table |
| Architectural decisions | `DECISIONS.md` (append-only) |
| Customer quotes (curated) | `USER-INSIGHTS.md` |
| Session context (navigation) | `docs/08-agents_work/sessions/<file>.md` |

## See also

- `pgvector-rag-beamix` — [[pgvector-rag-beamix]]
- `anthropic-routines` — [[anthropic-routines]]
- `agent-memory-systems` — [[agent-memory-systems]]

## Anti-patterns

- Writing every tool call to Mem0 — Mem0 is for episodic facts, not execution trace
- Reading all memories without a query (full-scan context bloat)
- Omitting `expires_at` on low-confidence facts (stale facts persist indefinitely)
- Putting code snippets in Mem0 (code changes; semantic search on code = low quality)
- Agent writing memories for another agent without explicit cross-agent intent
- Writing memories before the task completes (write on success, not on start)
