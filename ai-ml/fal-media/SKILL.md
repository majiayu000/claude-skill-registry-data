---
name: fal-media
description: >-
  Use when generating images or video via fal (FLUX, Veo, etc.) for brand, web, ads, or OpenMontage pipelines.
---

# fal Media

Thin adapter for digital workers. See `skills/org/TOOL-REGISTRY.md`.

## Preferred access
fal API + OpenMontage / inference-sh craft packs

## Env / secrets
`FAL_KEY` or `FAL_AI_API_KEY`

Resolve via `skills/integrations/obsidian-secrets/` then `.env.local`.

## MCP
— (HTTP API; OpenMontage may wrap)

## Primary ops
1. Respect MODEL-REGISTRY generation_profile (brand-stills, hero-video, ad-creative)
2. Default video model Veo 3.1 when profile says so
3. Record generation_used + cost notes on handoff

## Fallback
`INFSH_API_KEY` / inference-sh skills

## Common failures
Missing key → secrets; do not claim renders that were not run
