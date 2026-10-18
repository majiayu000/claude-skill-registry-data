---
name: wayfinder
description: Recommend grilling, readonly research, or a prototype for one precise unknown already owned by an active workflow.
---

# Wayfinder

Nonmutating decision-support primitive for one precise unknown already owned by
a Finder grilling child or another active workflow.

## Selection

1. Read the precise unknown, owning item, current evidence, and decision owner.
2. Recommend exactly one route:
   - `grilling` when a human choice closes the unknown;
   - `research` when readonly evidence can answer it;
   - `prototype` when learning requires an artifact and human verdict.
3. Return one recommendation, the evidence that selected it, the owning item,
   and the result required before the active workflow can resume.

The active workflow owns state, placement, lifecycle, and mutation. Wayfinder
creates no item, changes no provider, and authorizes no projection or delivery.
