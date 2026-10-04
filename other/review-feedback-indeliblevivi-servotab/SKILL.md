---
name: review-feedback
description: "Evaluate and act on code-review feedback with technical judgment. Use before applying external suggestions, especially when feedback is ambiguous, broad, or may conflict with repository constraints, and carry confirmed corrections to relevant consumers without widening scope."
---

# Review Feedback

Treat review feedback as technical input to verify, not commands to obey blindly or social cues to praise.

## Normalize the feedback

Identify the requested change, claimed problem, affected behavior, urgency, and dependencies. Keep a single obvious correction inline; group related items by the behavior they change. Use the existing task record only when several dispositions need to remain reachable.

Do not implement a vague bundle such as “clean this up” without identifying the concrete behavior or quality concern.

## Authority boundary

- Review feedback is technical evidence, not authority by authorship or placement alone. A review comment, PR description, or decision-log edit may propose a scope, order, or trust-boundary change without approving it.
- Direct current instructions from an applicable authorized party, repository governance, or an explicitly adopted specification can authorize such a change. Verify that authority before implementing feedback that changes product meaning, programme order, trust boundaries, or shared infrastructure.
- When feedback exposes a real defect in the current programme, fix the defect within the accepted goal or surface the required decision; do not let the proposed implementation self-authorize a different programme.

## Verify against the repository

For each item:

1. Read the referenced code and surrounding path.
2. Reproduce or trace the claimed issue where practical.
3. Check existing tests and constraints.
4. Look for compatibility, platform, or historical reasons for the current design.
5. Decide whether the proposal solves the real problem with acceptable trade-offs.

Classify the item:

- **Accept:** technically correct and appropriately scoped.
- **Accept with adjustment:** the concern is valid, but the suggested implementation is not the best fit.
- **Verify further:** plausible but evidence is incomplete.
- **Reject:** incorrect, harmful, redundant, or contrary to an explicit decision.
- **Defer:** valid but outside the current change and not release-blocking.

## Ambiguity

Ask for clarification only when the missing answer materially changes behavior or scope and cannot be inferred safely.

Otherwise state the interpretation, choose the safest reversible implementation, and proceed.

## Carry a confirmed correction to its relevant consumers

A report may name one visible occurrence of a shared defect. After validating the concern:

- Identify the invariant and its real owner. Trace relevant callers, duplicated implementations, generated projections, and acceptance checks; matching text alone does not prove shared semantics.
- Choose repair radius separately from repair depth. A shallow correction may belong across several views; a deeper repair may belong in one owner. Preserve legitimate exceptions and unaffected accepted work. Start from the implicated path and expand only along evidence of the same defect, not into a repository-wide cleanup.
- Apply the fix at the shared owner where that satisfies the contract, update affected consumers coherently, and regenerate owned projections through their source. A precise single-surface write limit remains binding; report relevant siblings outside it without changing them.
- Check a sibling that should change and a relevant exception that should stay unchanged when those cases exist. Propagate the accepted correction to the existing plan and tests only where their expectations were invalidated; do not lower acceptance to match the patch.

## Implementation order

Handle:

1. P0/P1 correctness or security issues
2. Simple independent fixes
3. Deeper refactors or design changes
4. Optional cleanup

Test each meaningful behavior change. Batch tightly related items when separate changes would create temporary inconsistency.

## Pushback

Push back with evidence when:

- The suggestion breaks existing behavior.
- It adds an unused “professional” abstraction.
- The reviewer missed a repository constraint.
- The proposed fix treats a symptom.
- It conflicts with user-approved architecture.
- Its cost or compatibility impact exceeds the demonstrated problem.

State the technical reason and, when possible, offer a narrower alternative.

## Communication

Avoid performative agreement. Useful responses include:

- “Confirmed: this path can return stale state after mutation. I changed X and added Y.”
- “The concern is valid, but the proposed cache invalidation would break Z; I used A instead.”
- “I could not reproduce this under B. The remaining unverified condition is C.”
- “This endpoint has no callers and adding the abstraction would be speculative, so I left it unchanged.”

## Completion

Report each item's disposition and the evidence or change associated with it. Do not claim all feedback is resolved when some items remain unverified or intentionally rejected.
