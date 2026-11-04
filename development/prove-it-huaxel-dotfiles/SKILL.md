---
name: prove-it
description: Produce reproducible evidence for a specific claim that software or a workflow works. Use for “give me irrefutable proof,” “prove this works,” “show evidence, not assurances,” or requests to substantiate correctness, reliability, or a measured improvement. Prioritize empirical checks and appropriate formal verification over repeated review. Not a demand for impossible certainty or a formal proof of every routine edit.
license: MIT
---

# Prove It

Replace reassurance with a check the user can rerun. “Irrefutable” is a challenge to strengthen evidence, not permission to overstate certainty. Inspired by pstack’s empirical and formal-verification practices; see [source notes](UPSTREAM.md).

## State the claim

Identify what must work, for whom, and under which conditions. Turn broad claims into falsifiable observations or invariants. Inspect the relevant code, artifact, environment, and existing verification before selecting a method. Do not substitute an easier claim or ask the user to answer something you can measure.

Separate assumptions from facts. Identify what would falsify the claim and where the observation must occur: return value, persisted data, real UI, external effect, or behavior after restart.

## Build the strongest practical check

- **Empirical:** Exercise the real path against identified inputs and source. Observe actual outputs and side effects, including relevant failure, retry, cancellation, or recovery behavior. Build/type checks and mocks support narrower claims; they do not prove the real path works.
- **Property-based:** Challenge a grounded invariant across generated inputs or event sequences. Keep counterexamples and state the sampled domain and limits.
- **Formal:** Use a model checker, SMT-backed verifier, or proof assistant when it addresses consequential cases ordinary testing cannot reach efficiently. State assumptions and bounds. Match model steps to real code and its atomicity; checking an abstract model alone does not verify its implementation.

Choose methods by the claim, not prestige or tool count. See [evidence design](references/evidence.md) for negative controls, model correspondence, and measurement pitfalls. Respect required project reviews; use additional review for missing assumptions or boundaries, not as a substitute for running available checks.

## Execute, do not just prescribe

Run the selected checks when access and authorization permit. Prefer a deterministic script or existing project check over a one-time screenshot or verbal assertion. Use a safe known-bad fixture or broken variant when practical to show that the check detects the relevant failure. A full mutation campaign remains explicit opt-in.

Use isolated fixtures and bounded runtime. Do not exercise production writes, publish, deploy, spend money, or contact upstream merely to obtain evidence. Preserve concurrent work and existing artifacts. If blocked, state exactly which claim remains unverified and why; a suggested command is not a completed check.

When a check fails, retain the counterexample. Do not weaken the claim, suppress failures, narrow coverage, or silently change the implementation to manufacture success. If fixing is authorized, preserve failing evidence and demonstrate the corrected result against the same check.

## Report the proof boundary

Keep commands, relevant output, source/input identity, tool versions, assumptions, and exclusions sufficient to reproduce the result. Reuse the project’s artifact conventions; do not create a new reporting bureaucracy.

For each important claim, say whether it was **demonstrated in the measured scope**, **proved under stated assumptions**, or **not established**. Explain the gap between the evidence and the broader claim. Neither reviewer agreement, a green suite, nor a passing bounded model proves the entire system correct.
