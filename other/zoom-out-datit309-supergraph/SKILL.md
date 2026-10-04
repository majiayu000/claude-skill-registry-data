---
name: zoom-out
description: One-shot module map — go up a layer of abstraction and get a domain-vocabulary module map of the codebase. Use when lost in unfamiliar code, after a long deep-dive session, or when you need to re-orient before planning.
---

# /supergraph:zoom-out

One prompt. One map. Re-orient fast.

Announce: "🔭 /supergraph:zoom-out — stepping back..."

## Steps

**1. Read CONTEXT.md for domain vocabulary (if exists):**
```bash
head -60 CONTEXT.md 2>/dev/null
```

**2. Get architecture overview:**
Use codebase-memory-mcp with `CBM_PROJECT`: call `get_architecture` for
`overview`, `layers`, `boundaries`, `clusters`, and `hotspots`; then use named
contract recipes `hubs`, `bridges`, and `test-gaps`. If unavailable, label it
`unavailable` and fall back to Serena/filesystem evidence.

**3. Output module map** using domain vocabulary from CONTEXT.md:

```
[Project name] — module map

[Community/Module A]
  └── [file/symbol] — [one-line role in domain terms]
  └── [file/symbol] — [one-line role]

[Community/Module B]
  └── ...

Key flows:
  [User action] → [Module A] → [Module B] → [output]

Hub nodes (high-change risk): [list]
Bridge nodes (coupling chokepoints): [list]
```

No implementation details. Domain language only. If a concept doesn't have a name in CONTEXT.md — use the most natural domain term and suggest adding it.

## Rules

- Use domain vocabulary, not file/class names (prefer "payment processing" over "PaymentService.ts")
- If CONTEXT.md is missing or empty — use the most natural terms you can infer and note at bottom: "CONTEXT.md missing — terms inferred"
- No action items, no recommendations — orientation only
- Follow with: "Ready to /supergraph:plan, /supergraph:analyze, or /supergraph:architecture?"
