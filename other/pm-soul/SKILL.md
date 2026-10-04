---
name: pm-soul
description: "Use when preserving product intent, acceptance criteria, decision memory, open loops, roadmap context, or the product-manager continuity layer of an agent team."
---

# PM Soul

## Procedure

1. Read `.agentlas/project-soul-memory.md` when present.
2. Extract user promise, target audience, current decision state, open loops,
   and acceptance criteria.
3. Connect sitemap changes to product intent.
4. Emit `## Memory Events` for durable updates instead of silently rewriting
   shared memory.

## Output

Return `intent`, `acceptance_criteria`, `open_loops`, `drift_risks`, and
`memory_events`.
