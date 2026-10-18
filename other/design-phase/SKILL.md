---
name: design-phase
description: Routes product design work from brand identity through a design system, accepted compositions, and quality-checked variant rounds in the real app to committed Design-Owned UI Code, backlog linkage, and a delivery handoff.
disable-model-invocation: true
---

# Design Phase

A Durable Workflow Graph. It turns brand evidence into UI code that lives on
the real route, passes the Quality Gate, and is committed by Promote.
`delivery-phase` then adds logic and data to that code.

## Bootstrap

1. Load [the design router](phases/router.md) on every invocation and resume,
   including direct entry into any gate.
2. Recompute the route from durable evidence and the design handoff; the
   transcript is never required.
3. Load exactly the one gate the router selects, or return its single
   terminal, checkpoint, or blocked outcome.
4. After the gate writes its durable outcome, stop or re-enter this bootstrap.

The router is the sole route authority. Gate files own executable work and
every child-skill activation. The user stops the run at three checkpoints:
brand, compose, and verdict.
