---
name: patpat-impact
description: Trace and prove the blast radius of an existing or proposed repository change. Use for downstream-regression questions, risky diffs, contract consumers, or claims that a small change is safe; remain read-only.
---

# Patpat Impact

When invoked directly, read the [operating protocol](../patpat-loop/references/operating-protocol.md) in full. Do not load the router.

Read [repository truth](../patpat-loop/principles/repository-truth.md), [boundary discipline](../patpat-loop/principles/boundary-discipline.md), and [proof over proxy](../patpat-loop/principles/proof-over-proxy.md). Apply the [blast-radius playbook](../patpat-loop/playbooks/blast-radius.md).

The job is the one-safety-fact the change depends on, not a caller list. Grep callers is not the deliverable. Climb the certainty ladder for that fact and say where it stopped: (1) said so (worthless alone) (2) pointed at `file:line` (3) walked the failure and it does not reach (4) ran real code (a script or test that calls the shipped function and fails loud if wrong) (5) reproduced in the running app. Any fact that does not reach ladder step 4 is `unproven`. Do not write it as settled.

Remain read-only. Hand back, small: what it does; the one fact, the step reached, and the proof or unproven; real risks with `file:line`; cleared; cheapest check before merge. Do not turn blast-radius analysis into architecture design or implementation.

## Mutation boundary

Remain read-only with respect to repository implementation and external delivery. Limit incidental verifier artifacts to the declared proof contract, clean them up, and hand any authorized mutation back to `patpat-loop`.
