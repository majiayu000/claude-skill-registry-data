---
name: flow-lenses
description: Examine a bounded flow through the ten Flow Lenses and return candidate gaps. Use when the `requirements-grill` checkpoint records a response set, `create-architecture` step 3 scans closed decisions, or `brainstorm` checks its own shapes.
---

# Flow Lenses

Examine one bounded flow end to end: control flow, state consistency, and failure recovery. Return candidate gaps to the caller. The caller owns every question to the user and every durable write; this skill only examines and reports.

The caller supplies the flow and the evidence it holds. Ground each concern in the actual system: read the code, artifacts, or recorded decisions that a lens needs. Name a mechanism only for a risk that the evidence supports.

## Lenses

1. Entry points and path convergence: where can this behavior start? Do equivalent actions reach the same rules, or take divergent/bypass paths?
2. Critical execution paths: what must happen, in which order? Where does execution branch, wait, delegate or continue asynchronously?
3. State ownership and authority: what state changes, who owns it, who may change it, and which representation is authoritative?
4. Transaction and side-effect boundaries: what commits together? Which effects occur outside that boundary? What intermediate states can become visible?
5. Concurrency and stale state: what if two actors run this simultaneously, or state changes between validation and execution?
6. Idempotency and retries: what happens when a request is repeated, execution resumes, or an acknowledgement is lost after success?
7. Partial failure and recovery: what remains after failure at each boundary? Can we safely retry, reconcile, compensate or roll back?
8. Execution lifetime and durability: what survives a disconnect, cancellation or process crash? Who owns unfinished work?
9. Lifecycle and dependency transitions: what happens during creation, update, replacement and removal? What still depends on the old state?
10. Completion and observability: what proves the requested outcome occurred? Can an operator distinguish accepted, applied, running, failed and partially complete?

## Output

Return two parts to the caller.

**Lens coverage**: one line per lens: covered with evidence, covered with an explicit unknown, or not applicable with the reason.

**Candidate gaps**: one entry per material gap, a missing decision the flow needs before it counts as understood:

- **Lens**: the lens number and label.
- **Evidence**: the file, line, artifact, or recorded decision that shows the gap; or `Unknown:` and what is missing.
- **Guarantee at stake**: what the flow can fail to guarantee if the gap stays open.
- **Altitude**: the Altitude of the question the gap implies: L1 Outcome, L2 Shape, or L3 Modules, as the [Altitude Ladder](../requirements-grill/phases/router.md#altitude-ladder) defines them.

Gaps stay candidates. The caller decides how each gap reaches the user and records any accepted decision.

Completion: each applicable lens is covered by evidence or an explicit unknown; each non-applicable lens has a reason; each material gap is a candidate gap with all four fields.
