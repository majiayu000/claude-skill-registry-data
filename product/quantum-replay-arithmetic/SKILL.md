---
name: quantum-replay-arithmetic
description: "Co-design reversible GCD walks, transcript encodings and payload replay for structural point-addition gains; compare full arithmetic families and cleanup."
---

# Widerchäuer (quantum-replay-arithmetic)

Change the walk, the information it records, or the way its consumer reconstructs arithmetic. Read [both arithmetic papers](references/paper.md).

Read the [shared contract](../quantum-structural-lanes/references/lane-contract.md) before a trial. Start with the five-line post; the shared native-test order, stop rules and promotion gate apply.

## Practical lane
Audit the active dispatcher before designing: list recurrence, transcript alphabet, packing/decoder, coefficient or payload updates, register alternation, square/reduction and both divisions. Mark each proposed feature already present, absent or uncertain. Reintroducing an inherited feature is not a contribution.

Compare coherent families rather than mixing incompatible fragments: compressed multi-step history, fixed-alternation history, and in-place multiplication/division with delayed coefficient reconstruction. Preserve a common input/output and cleanup contract. A classical-addend circuit and a quantum-addressed window circuit have different interfaces and costs.

First experiment: build a small independent arithmetic model for one transition plus reverse replay. Test complete histories for small odd moduli and supported inputs, including zero payload, terminal states and signed/canonical boundaries. For the chosen family, specify how full-width convergence and register capacity are justified.

Then test one complete numerator/denominator boundary before replacing the point adder. Price the decoder, packed history, both arithmetic directions, payload corrections and temporary products. If comparing fused replay, isolate its cost using an otherwise identical family; do not credit unrelated square or lookup changes to the recurrence.

## Structural extension
Design the transcript for the exact next consumer rather than reconstructing generic decisions. Consider eliminating full-width comparisons or materialized coefficients. A larger transcript can win if it removes more expensive work; measure the complete tradeoff.

Retain the papers' structured counterexamples as regressions. Fresh random passes cannot erase known failures. Deliver recurrence/inverse specifications, transcript occupancy, full-width regressions and whole point-add resources. Falsify on noninvertible state transitions, unbounded history, unsupported exceptional inputs or unfavorable full-path economics.
