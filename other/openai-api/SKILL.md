---
name: openai-api
description: Builds or debugs OpenAI Chat Completions, Responses API, and OpenAI Agents SDK patterns — function calling, structured output, streaming, handoffs. Use when extending src/lib/ai/clients/openai.ts or adding OpenAI-first agents.
---

# OpenAI API (Cursor)

## Canonical source

**`.claude/skills/openai-api/SKILL.md`** lists **platform.openai.com** and **openai.github.io/openai-agents-python** references and implementation patterns.

## In Cursor

1. Read the canonical skill for the surface you need (`agents` vs `chat`).
2. Fetch current OpenAI docs (model list, API reference) before relying on model IDs or parameters.
3. OpenAI REST + Agents SDK entry: `src/lib/ai/clients/openai.ts` (`openaiClient`, `createAgent`, `createRunner`, re-exports `run`, `tool`, `fileSearchTool`).
