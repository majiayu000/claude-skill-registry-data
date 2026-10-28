---
name: ngautopilot-internal-catalog
description: Internal NgAutoPilot canonical micro-skill catalog boundary. Public discovery should use the curated gateways under .agents/skills instead.
metadata:
  internal: true
---

# Internal canonical catalog

This marker exists only to stop broad third-party recursive discovery from presenting every canonical NgAutoPilot micro-skill as an independent install choice.

The canonical source skills remain below this directory for NgAutoPilot's own catalog, packs, adapters, plugin generation, validation, and release tooling.

Public discovery entrypoints live under `.agents/skills/`.
