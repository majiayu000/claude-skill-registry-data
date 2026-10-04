---
name: context-compression
description: When conversation context is getting long, when approaching token limits, when the user says "compress," "summarize context," "too long," "running out of context," "compact," or when you notice degraded performance due to context length. Implements a 3-layer compression pipeline (MicroCompact, AutoCompact, Full Compact).
metadata:
  version: 1.0.0
  inspired_by: 3-layer Context Compression pipeline
---

# Context Compression — 3-Layer Pipeline

You are a context compression engine. When conversations grow long, you systematically reduce context size while preserving all decision-critical information.

## When To Trigger

- Conversation exceeds ~50 turns
- User mentions context is getting long or responses are degrading
- You notice you're losing track of earlier decisions
- User explicitly asks for compression
- Before a complex multi-step task that needs headroom

## The Three Layers

### Layer 1: MicroCompact (Light Touch)
**Goal:** Remove noise without losing any information.

Do this:
- Strip redundant confirmations ("Yes, that looks good", "Sure, I'll do that")
- Collapse repeated tool outputs into summaries ("Read 12 files — all TypeScript, avg 200 lines")
- Remove failed attempts that were superseded by successful ones
- Collapse verbose error messages into one-line summaries
- Remove conversational filler ("Let me think about this...", "Great question...")

**Compression ratio:** ~30-40% reduction
**Information loss:** Zero

### Layer 2: AutoCompact (Structural)
**Goal:** Restructure retained information for density.

Do this:
- Convert sequential discoveries into a structured summary:
  ```
  ## What We Know
  - The API uses Express with 14 endpoints
  - Auth is JWT-based, tokens expire in 24h
  - Database is Postgres via Drizzle ORM
  - Tests use Vitest, 73% coverage

  ## Decisions Made
  - Using server components by default
  - API routes return { data } or { error }
  - Commit style: conventional commits

  ## Current Task
  - Building the user dashboard
  - Blocked on: auth middleware refactor
  - Next step: implement session management
  ```
- Group related file reads into summaries
- Merge multiple rounds of the same type of work into outcomes
- Replace code snippets with references ("see src/auth.ts:45-67")

**Compression ratio:** ~60-70% reduction
**Information loss:** Minimal — details available via file re-reads

### Layer 3: Full Compact (Aggressive)
**Goal:** Maximum compression. Only essential state survives.

Do this:
- Reduce to three sections only:
  ```
  ## State
  [What exists right now — files created/modified, current branch, build status]

  ## Intent
  [What the user wants to achieve — the goal, not the steps]

  ## Constraints
  [Critical decisions, patterns, rules that must be followed]
  ```
- Everything else is discardable and can be re-derived from the codebase
- No code snippets — just file paths
- No exploration history — just conclusions

**Compression ratio:** ~85-90% reduction
**Information loss:** Moderate — but all recoverable from codebase

## How To Apply

When triggered, assess which layer is appropriate:

| Situation | Layer |
|-----------|-------|
| "Getting long but still fine" | Layer 1 |
| "Losing context, need clarity" | Layer 2 |
| "About to hit limits, need maximum headroom" | Layer 3 |
| User says "compact" or "compress" | Layer 2 (default) |
| User says "hard compress" or "nuke context" | Layer 3 |

## Output

After compression, present the compressed context to the user:

```
Context compressed (Layer [N]):
- Before: ~[X] turns, ~[Y]k tokens (estimated)
- After: ~[Z]k tokens (estimated)
- Preserved: [list key items kept]
- Dropped: [list what was removed]

Compressed context follows:
---
[compressed context block]
---

Does this capture everything important? Anything I should keep that I dropped?
```

## Rules

- Never compress away: user decisions, architectural choices, active task state, error patterns that haven't been resolved
- Always compress away: greetings, confirmations, exploration that led nowhere, superseded attempts
- When in doubt, keep it in Layer 1/2 and let the user decide
- After compression, re-read any critical files to refresh your understanding
- Flag if compression might lose something important: "I'm about to drop [X] — should I keep it?"
