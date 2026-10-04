---
name: phxstack-build
description: Implement an approved local spec in small verified steps. Use after the developer approves a phxstack spec, or for a clear small change that needs no spec.
---

# phxstack-build

Implement the smallest verified next step.

1. Read the approved `.phxstack/specs/<slug>.md`; for a clear small change,
   use the request as the task. Inspect the working tree and `LEARNED.md`.
2. For Elixir work, read the relevant `phxstack-elixir` references and
   `reference/verify.md`. For browser UI, use installed `impeccable` directly.
3. Implement one coherent step and run its relevant verification.
4. Mark the completed step in the local spec when one exists. Continue only
   with the next planned step.

Pause only for a real choice or necessary unplanned work: an architectural or
product decision, new dependency, public API or schema change, destructive
operation, or an amendment to the approved spec. Report the evidence and the
smallest decision needed.

Report:

```text
CHANGED
VERIFIED
```

