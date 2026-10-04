---
name: claude-api
description: Builds or debugs Anthropic Claude integrations using @anthropic-ai/sdk — messages, tool use, extended thinking, prompt caching, streaming. Use when editing src/lib/ai/clients/anthropic.ts or adding Claude-based agents and tools.
---

# Claude API (Cursor)

## Canonical source

**`.claude/skills/claude-api/SKILL.md`** contains model IDs, message format notes, tool-use loops, caching, and a table of **authoritative docs.anthropic.com URLs**.

## In Cursor

1. Read the canonical skill section for your task (tool use, streaming, caching, etc.).
2. Use **WebFetch** or **WebSearch** on the listed Anthropic URLs when model names or API fields may have changed.
3. Keep client access through `anthropicClient` from `src/lib/ai/clients/anthropic.ts` and `env` from `@/lib/env`.
