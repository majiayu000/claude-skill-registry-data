---
name: spark-find-simplifications
description: Use when a working Spark implementation should be simplified without changing its observed behavior, ownership, compatibility, or public contract.
---

# Spark simplification search

Simplify only after the behavior and validation baseline are known.

## Procedure

1. Identify the owner, public behavior, compatibility constraints, and tests that establish the current contract.
2. Start from code-review findings or inspect for duplicate branches, overlapping adapters, zero-semantic wrappers, unused metadata, unnecessary abstractions, dead compatibility paths with explicit exit criteria, and state derived in more than one place.
3. For each candidate, state its semantic payload. If deleting or inlining it loses no policy, conversion, owner boundary, invariant, or supported compatibility, prefer removal.
4. Trace polling and opportunistic reconciliation back to the authoritative mutation path. Prefer keeping the owner correct at write time over another cache, scan, or repair loop.
5. Check collection limits before downstream filtering or skipping for fairness and starvation errors.
6. Prefer deleting indirection or moving semantics into the existing owner over introducing another framework, package, schema, facade, budget, or exception.
7. Compare each candidate against production callers and focused validation. Require live call-path evidence before declaring code unreachable.
8. Recommend the smallest independent simplification and the evidence needed to prove equivalence.

Stop when a simplification would alter serialization, authority, lifecycle, or user-visible behavior without explicit acceptance criteria. Return `candidates`, `evidence`, `recommendedSlice`, `validation`, and `rejectedIdeas`.
