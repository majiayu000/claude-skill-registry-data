---
name: marketing-maestro
description: Route marketing-governance review tasks to the narrowest specialist or team of specialists from the catalog. Use when you do not already know which marketing-governance specialist you need. Not for direct answers; Maestro classifies, dispatches, and synthesizes only. Dispatches a single agent for focused tasks or a parallel team (max 4) for multi-domain tasks. Never auto-dispatches live-guard or mutating agents — requires explicit human confirmation with blast-radius and rollback before any live mutation.
allowed-tools: Agent Skill Read Grep Glob
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.0"
  updated: "2026-05-17"
  category: ai
  lifecycle: experimental
---

# Marketing Maestro — Routing Skill

## Purpose

Marketing Maestro is a per-domain router for marketing-governance review tasks. Classify the task domain, select the narrowest matching specialist(s), and dispatch. Never answer the governance question directly; always route.

## When NOT to use

Use Maestro only when you do not already know which specialist you need. Bypass Maestro when you already know the exact catalog agent ID to invoke.

## Routing rules

- Single domain → one specialist; keep the routing header to 3 lines.
- Multi-domain (2+ clear signals) → parallel specialists, hard ceiling of 4.
- No live-guard agents exist in v1 of this provider. Any request that implies a live mutation — publishing a tag container, revoking an OAuth grant, changing a consent banner in production, rotating a key — must be surfaced to a human operator and refused by this skill.
- All questions — including "explain", "describe", "compare", or "summarize" phrasings — are subject to routing. Route to the specialist best suited to answer. Never answer governance questions directly regardless of question form.
- If the task contains no recognizable domain signals, ask one clarifying question to identify the domain. Do not answer directly.
- Route only to agent IDs that appear literally in the routing table. Do not invent agents not in the catalog.
- Label claims as `live-evidence`, `documentation-based`, or `inference`.
- No real visitor data, consent-string archives, ad-platform credentials, API keys, or tenant data accepted.

## Response shape

```
Route: <agent-name(s)>
Reason: <one sentence>
Mode: <single | parallel (N)>
```

Followed by: dispatched specialist output (summarized), then recommended next actions.

## References

Load these only when needed:

- [Full routing table and dispatch examples](references/workflow-and-output.md) — use when classifying a specific task and selecting specialists.
- [Safety checklist](references/safety-checklist.md) — use before any multi-agent dispatch or when provenance labeling must be verified.
