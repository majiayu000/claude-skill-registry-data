---
name: kb-memory
description: Use when knowledge base and memory system for AI agents. Covers company
  KB, persistent memory, session recall, and brain architecture for context preservation.
domain: core
author: oyi77
license: Apache-2.0
subdomain: ai-infrastructure
tags:
- knowledge-base
- memory
- context
- persistence
- recall
- brain
version: 2.0.0
category: core
---



# KB-Memory: Knowledge Base & Memory System

Unified skill for agent knowledge persistence and recall. Covers four approaches to maintaining context across sessions.

## When to Use

**Trigger phrases:**
- "save this to memory" / "remember this for later"
- "what do we know about…" / "search the knowledge base"
- "restore context from last session" / "where did we leave off?"
- "update the company KB" / "sync knowledge to brain"

**Use when:**
- A fact, decision, or preference should survive the current session
- You need to recall prior context, decisions, or project state
- Session continuity matters (compaction, resume, handoff)

**Don't use for:**
- One-off lookups that live entirely in the current context window
- General file storage — this is for structured knowledge, not arbitrary files



## Anti-Rationalization Table

| Excuse | Reality | Rule |
|--------|---------|------|
| "I'll remember it" | Human memory is unreliable; agent context windows overflow | Persist everything; retrieval > recall |
| "Vector search is enough" | Vectors miss exact matches, relationships, temporal ordering | Combine vector + graph + keyword; no single index suffices |
| "One big context window" | Large contexts dilute attention and increase cost | Chunk, summarize, and retrieve precisely |

## How to Use

1. **Pick the approach** — Match the need to one of the four approaches below (KB, Company KB, Memory System, Session Brain)
2. **Follow the approach doc** — Each row links a reference file with the exact commands and storage format
3. **Store with structure** — Include entities/relations and timestamps so recall is precise
4. **Recall before acting** — Query memory before duplicating effort or re-deriving decisions
5. **Consolidate** — Promote durable facts from session brain to persistent memory at session end

## Approaches

| Approach | Purpose | Reference |
|----------|---------|-----------|
| **KB** — Static knowledge base | Reference docs, policies, permanent facts | [../core/kb/SKILL.md](./../core/kb/SKILL.md) |
| **Company KB** — Organization wiki | Team docs, product info, internal guides | [../core/company-kb/SKILL.md](./../core/company-kb/SKILL.md) |
| **Memory System** — Persistent agent memory | Cross-session recall, user preferences | [reference/approach/memory.md](./reference/approach/memory.md) |
| **Session Brain** — Session context | Current conversation state, working memory | [reference/approach/session-brain.md](./reference/approach/session-brain.md) |

## How They Fit Together

```
Permanent ←──────────────────────────────────→ Ephemeral
    │                                              │
  Company KB          Memory System          Session Brain
  (team wiki)      (cross-session facts)    (current conv)
    │                                              │
    └── Both backed by KB (base reference docs) ───┘
```

- **KB** — Foundation. Static reference material that doesn't change.
- **Company KB** — Organization-specific information.
- **Memory System** — Learned facts about user, projects, and preferences.
- **Session Brain** — Working memory for the current task.
## Overview

kb-memory is the unified entry point for agent knowledge persistence and recall. It covers four approaches: static KB (reference docs), Company KB (org wiki), Memory System (cross-session learned facts), and Session Brain (working memory for the current conversation) — see the Approaches table above, which links per-approach reference files with exact storage formats and commands. The core discipline is: pick the smallest approach that fits, store with structure (entities/relations/timestamps), recall before acting, and consolidate durable facts into persistent memory at session end. Session recall uses git state (`git log -1 --oneline`) to restore where a session left off; persist with `git add -A` and `git commit -m "memory update"`.

## When NOT to Use

- One-off lookups that live entirely in the current context window — no persistence needed
- Arbitrary file storage — this is structured knowledge, not a file system
- Retrieval from a codebase — use a code-indexing tool instead of a knowledge base
- Ephemeral scratch work — let the session brain hold it, don't persist noise
- When the fact belongs in code/config (env vars, constants) — persist there, not in memory

## Verification

1. Stored entries include entities/relations and timestamps — recall must be precise, not fuzzy
2. A recall query against the right approach returns the expected fact before acting
3. Durable facts from the session were promoted to persistent memory at session end (consolidation step)
4. The chosen approach matches the need: static reference → KB; org facts → Company KB; learned preferences → Memory System; current state → Session Brain
5. No private or sensitive data leaked into shared storage — access boundaries respected (see company-kb privacy section)

## Anti-Rationalization Addendum

| Rationalization | Reality |
|-----------------|---------|
| "I'll store it in the session only, it's short" | Session context vanishes at compaction/handoff; anything needed later must be persisted |
| "One giant memory dump is fine" | Unstructured dumps are unretrievable; structure (entities, relations, timestamps) is what makes recall work |
| "Searching memory is slower than just asking" | Re-deriving decisions duplicates effort and risks drift; retrieval costs less than rework |
| "Company KB and Memory System are the same" | One is org-wide wiki, the other per-agent learned facts; mixing them pollutes both |

