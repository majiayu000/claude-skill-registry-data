---
name: dependency-rule-review
kind: skill
status: ready
provenance:
  principles:
  - P040
  - P041
  claims:
  - C00473
  - C00477
  - C00359
  - C00394
  evidence:
  - E00105
  - E00108
  - E00079
  - E00086
  source_anchors:
  - 91e37e1ca511-c0006
  - 91e37e1ca511-c0001
  - 91e37e1ca511-c0002
  authored_from_digest: 0aec8def0c546b24875afbdb6bb734b136b281485f0894d3a9ffa6cd16f9b395
---

# Dependency Rule review

## Purpose

Check that source-code dependencies point inward toward policy and that high-level policy depends
on abstractions, not detail. The Dependency Rule requires dependencies to point only inward —
from lower-level mechanisms toward higher-level business rules — so inner policy layers know
nothing of the outer layers that use them. The Dependency Inversion Principle reinforces this:
both policy and detail depend on abstractions, so volatile implementations can change without
disturbing stable business rules. This skill finds and explains violations of that direction.

## When to use

- Reviewing layering or dependency direction between business rules and infrastructure.
- Business logic appears to import or depend on frameworks, the database, or the UI.
- A change to a low-level mechanism forces edits to core business rules.

Do not invoke when the codebase has no separable policy/detail distinction (e.g. a trivial
script).

## Procedure

1. **Identify policy vs. detail.** Separate the high-level business rules (policy) from the
   low-level mechanisms (database, UI, frameworks, I/O). Policy is what the system *is for*;
   detail is *how* it currently runs.
2. **Map the dependency arrows.** For each dependency that crosses the policy/detail line, note
   its direction in source code (who imports/references whom).
3. **Flag inward-rule violations.** A dependency that points outward — policy importing or naming
   a concrete detail — violates the Dependency Rule. Record it as a finding.
4. **Check abstraction ownership (DIP).** Where policy must invoke detail, confirm policy depends
   on an abstraction it owns, and the detail implements that abstraction. If policy depends
   directly on a concrete class, the inversion is missing.
5. **Explain the coupling risk.** Tie each violation to the consequence: stable business rules
   are now coupled to a volatile mechanism and will be disturbed when that mechanism changes.
6. **Recommend the inversion.** Propose the abstraction (interface/port) to introduce and which
   side should own it, so the arrow flips to point inward. State the trade-off: the added
   indirection buys insulation of business rules from mechanism churn.

## Inputs

- The code or design under review, with its layers and the dependencies between business rules
  and infrastructure.

## Output

A findings list of dependency-direction and inversion violations, each naming the offending
dependency, the rule broken, the coupling consequence, and the abstraction to introduce to point
the dependency inward.

## References

- [Clean Architecture dependency rule](../../references/clean-architecture-dependency-rule.md) —
  the Dependency Rule, Dependency Inversion, and the details-as-plugins checklist.

## Provenance

Distilled from principle(s) **P034/P035**, claims **C01246/C01250/C01132/C01167**, evidence **E00228/E00229/E00207/E00213**, anchored in the cited architecture sources (`sources/anchors/`). Source is `distillation-only`: content is paraphrased, never quoted verbatim.
