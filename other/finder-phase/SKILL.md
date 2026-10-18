---
name: finder-phase
description: Run the shared human-driven Finder engine for one explicit Business or Functional intake.
disable-model-invocation: true
---

# Finder Engine

One durable graph creates or resumes one Fog for an explicit Business Finder or
Functional Finder invocation. Wrappers own their audience language and
projection ceiling. This engine alone owns lifecycle, generic support work,
resume routing, and bounded return.

## Bootstrap

1. Read [the direct-composition contract](references/entrypoint-contract.md).
2. Read [the state graph](references/state-graph.md) and
   [runtime handoff](references/runtime-handoff.md).
3. Reconstruct current state from fresh Fog, child, relation, immutable-evidence,
   provider-readback, and handoff evidence. Treat a suggested route as advisory.
4. Read [the router](phases/router.md) on every entry and cold resume.
5. Load exactly one selected gate, or return the router's one blocked,
   checkpoint, or terminal outcome.
6. After the selected gate writes its durable handoff, stop or re-enter this
   bootstrap.

The router owns transitions. Each gate owns only its bounded action.
`$write-backlog` remains the sole physical provider mutation authority.

## Gates

- [Ensure Fog](phases/ensure-fog.md)
- [Generic Grilling](phases/grilling.md)
- [Research support](phases/research.md)
- [Prototype support](phases/prototype.md)
- [Optional projection reconciliation](phases/reconcile.md)
- [Bounded return](phases/return-target.md)
- [Human steering](phases/human-steering.md)

## Runtime references

- [State graph](references/state-graph.md)
- [Runtime handoff](references/runtime-handoff.md)
- [Root routing boundary](references/root-routing.md)
