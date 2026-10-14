---
name: library-selection
description: "Library selection: check existing capability, framework-native, stdlib, existing dep first. Evaluate maintenance, security, license, cost, API, types, docs, compat. Ask: need dep at all?"
---

# library-selection

The best dependency is the one you don't add. The second best is the boring, maintained one.

## Activate when

- Facing "which library for X?" or proposing a new dependency.

## Do NOT activate for

- Post-selection auditing (see dependency-evaluation); API usage questions (see documentation-search).

## Inspection

State the job-to-be-done, then check in order: existing project capability → framework-native solution → standard library → already-installed dependency → new candidate.

## Decision rules

- Most problems already have a working answer in the repo or framework — prove otherwise before shopping.
- Compare at most 3 candidates on: maintenance, security history, license, bundle/runtime cost, API quality, type support, docs, version compat with the pinned stack.
- Boring wins ties: larger user base, longer history, smaller API surface.
- Reject: abandoned projects, license conflicts, weight 10× the need, framework-incompatible majors.

## Procedure

1. Document the need and the in-repo/framework alternatives ruled out (with reasons).
2. Score candidates; pick with evidence, not popularity vibes.
3. Prototype the top candidate against the real use case before committing.
4. Verify: prototype meets acceptance, evaluation recorded, handoff to dependency-evaluation for the audit.

## Failure modes

- Shopping before checking the repo; choosing by stars/downloads alone; ignoring bundle cost; two libraries doing the same job; selection without a prototype.

## Escalation

Security/supply-chain depth → dependency-evaluation + security/secrets-supply-chain.

## References

- Related: `../dependency-evaluation/`, `../../core/dependency-research/`.
