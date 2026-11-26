---
name: quantum-verified-architecture-search
description: "Run evaluator-guided structural circuit search with independent value, phase and scratch checks, architecture diversity and frozen confirmation evidence."
---

# Bauinspäkter (quantum-verified-architecture-search)

Search over representations and reversible state transitions rather than merely tuning emitted constants. Read [the two search papers](references/paper.md).

Read the [shared contract](../quantum-structural-lanes/references/lane-contract.md) before a trial. Start with the five-line post; the shared native-test order, stop rules and promotion gate apply.

## Practical lane
Separate candidate proposal from the trusted evaluator. Freeze evaluator source, interface and baseline; candidates may not modify the oracle or score function. Verify that the chosen simulator supports the candidate gate set and measurement semantics. A simulator for reversible logic plus restricted phase/measurement operations is not a universal quantum simulator.

Describe each architecture by algorithm, state representation, history, cleanup and interface. Keep known-good incumbent variants distinct from structural forks. A literature-informed lineage is not blank-slate. Select mutations that change a cost term: reconstruct a stored decision, fuse a producer with its consumer, change representation across a region, or remove a cleanup dependency.

First experiment: challenge the evaluator with three deliberately wrong toy candidates—correct values with wrong relative phase, correct values with dirty scratch, and an arithmetic error—plus a known-good control. Fix evaluator blind spots before search.

For each proposal, run cheap semantic and resource falsifiers, preserve rejected artifacts, and require a bounded next milestone. Use independent fresh confirmation after freezing the candidate. Keep deterministic regression inputs, matched-input comparisons and official hash-derived packets as distinct evidence. Do not optimize against held-out confirmation inputs or label a chosen clean packet an all-input proof.

## Structural integration
Retain nondominated candidates and evidence about why each mechanism changes the resource model. Recombine only compatible interfaces; validate composition as a new candidate. Refactor the best mechanism into a readable implementation with the same emitted semantics before delivery.

If advisors are authorized, give them bounded design or refutation questions; record actual model receipts. Advice is not validation. Do not start workers, paid calls or an unattended loop merely by loading this skill. Finish with reproducible candidate artifacts, evaluator receipts, negative results and the exact promotion state.
