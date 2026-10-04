---
name: gemini-api
description: Builds or debugs Google Gemini via @google/generative-ai — generateContent, function calling, grounding, multimodal input, streaming. Use when editing src/lib/ai/clients/google.ts or adding Gemini features.
---

# Gemini API (Cursor)

## Canonical source

**`.claude/skills/gemini-api/SKILL.md`** includes **ai.google.dev** links and patterns for models 2.5/3.x family features.

## In Cursor

1. Read the relevant section in the canonical skill (grounding, vision, streaming, etc.).
2. Use **WebFetch** on the official Gemini docs URLs from that skill when verifying current model IDs or API shapes.
3. Use `googleClient` and `getGeminiModel()` from `src/lib/ai/clients/google.ts`; never read `process.env.GOOGLE_AI_API_KEY` directly in feature code.
