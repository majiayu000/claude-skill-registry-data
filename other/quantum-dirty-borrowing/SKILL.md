---
name: quantum-dirty-borrowing
description: "Assess scheduling of already dirty-safe quantum blocks against actual peak ownership and rewrite economics. Use for source-bound borrowing transfers; Bona does not synthesize clean-to-dirty arithmetic."
---

# Dräckfink (quantum-dirty-borrowing)

Change workspace ownership across phases rather than merely shortening a local register. Read [Bona's mechanism and limits](references/paper.md).

Read the [shared contract](../quantum-structural-lanes/references/lane-contract.md) before a trial. Start with the five-line post; the shared native-test order, stop rules and promotion gate apply.

## Scheduler versus arithmetic synthesis
Bona assumes blocks already satisfy a dirty-borrowing contract. It does not synthesize a clean-to-dirty replacement for a data register. Require the exact gadget and identity-on-lender proof before constructing a scheduling graph. A helper named `and_dirty` elsewhere is insufficient: show it actually owns the binding allocation and has a legal host.

If a rewrite is necessary, classify it as a separate arithmetic-synthesis hypothesis and compare its entire added T against the row's remaining budget before building. Use the current front and product budgets in the shared benchmark reference; reopen a rejected attachment only on a changed, quantified premise.

## Practical lane
1. Extract lifetimes from the active emitted circuit, including all phases tied at peak Q. Label each temporary clean-required or dirty-safe; an unused wire is not automatically a clean wire.
2. Build an endpoint/dependency graph. For each proven dirty-safe gadget, find an idle host interval with no operand alias or dependency cycle. Start with unchanged-order placements; price necessary rescheduling separately.
3. First experiment: remap one actual peak allocation into an eligible host, with a machine-readable old/new allocation trace. Check the gadget's forward operator against the intended operation tensor identity on the borrowed state.
4. Remeasure the whole circuit. If another phase still binds, the result is a local mechanism only. Expand only to a bounded set of co-binders with identified compatible hosts.

## Structural extensions
Compare shared workspace scheduling against regeneration and against moving a consumer to expose an interval. These are separate hypotheses: regeneration changes T, rescheduling can change depth and dependency pressure. An allocation diagram without emitted-circuit evidence is insufficient.

Falsify if all peak temporaries require clean state, eligible hosts overlap operands, the splice introduces a cycle, or the unaffected floor prevents the claimed width target. Retain a useful local schedule without labeling it a board gain.

Deliver the dependency graph, borrow/restore boundaries, all peak-owner traces, operator check and full Q/T delta. Do not measure or reset arbitrary borrowed data.
