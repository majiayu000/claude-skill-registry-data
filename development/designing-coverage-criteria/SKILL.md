---
name: designing-coverage-criteria
kind: skill
status: ready
provenance:
  principles:
  - P058
  - P066
  - P079
  - P082
  - P083
  - P097
  - P098
  - P100
  claims:
  - C00004
  - C00005
  - C00006
  - C00001
  - C00002
  - C00222
  - C00234
  - C00235
  source_anchors:
  - 140e06385751-c0000
  authored_from_digest: 7550cd591eb9ef7ae02a16b5fa06d46a43deab14903dc64b9664f6123f8ec077
---

# Designing coverage criteria

## Purpose

Turn "how should I test this?" into a defensible coverage-criterion choice by modelling the
artifact as one of four abstract structures and reasoning about test effectiveness through the RIPR
model. Grounds the advice in Ammann & Offutt's *Introduction to Software Testing* (P066, P058).

## When to use

- The developer needs to decide what "enough testing" means for a piece of code or a specification.
- Code has loops, compound boolean conditions, or rich data flow and a single coverage number is
  being used blindly.
- The developer is choosing between branch, condition/MC-DC, prime-path, or data-flow coverage.

## Procedure

1. **Model the artifact as one of four structures** and let the model pick the criterion family
   (P066): input space (partitioning), a **graph** (control- or data-flow), a **logic expression**
   (predicates and clauses), or **syntax** (grammar / mutation).
2. **For graph criteria, build the graph first, then cover it** (P079, P082): nodes with non-empty
   initial and final sets and edges. Use Node/Edge coverage for straight-line and branching code;
   prefer **Prime Path Coverage** for loop-bearing graphs — a prime path is a maximal simple path,
   which keeps the number of test requirements manageable while still exercising loops (P082).
3. **For logic criteria, advance from reaching a location to infecting state** via truth-value
   combinations, preferring the semantic (Active Clause Coverage) approach; recommend **Correlated
   Active Clause Coverage** as the most practical ACC flavour, and note that General ACC does not
   subsume Predicate Coverage (P097, P100).
4. **For data flow, base coverage on def-use pairs**: a def stores a value, a use reads it, and a
   def reaches a use along a def-clear path (du-paths). Focus integration testing on data-flow
   couplings, which are fault-rich (P098).
5. **Reason about effectiveness with RIPR** — reachability, infection, propagation, revealability:
   input-space criteria assure none of these, graph/logic criteria assure reachability (and, for
   logic, infection), so a passing suite at a weak criterion does not imply faults will propagate to
   an observable failure (P058).
6. **Choose strength contextually** using the subsumption hierarchy (see reference), not a blanket
   target; name the criterion and the RIPR gap it leaves.

## Inputs

- The code or specification under test, its control/data-flow shape (loops, predicates, def-use),
  and the developer's cost/rigor constraints.

## Output

A named coverage criterion (and the artifact model behind it), the test requirements it generates,
and the RIPR limitation that remains — with a contextual recommendation on rigor.

## References

- `references/coverage-criteria-subsumption.md` — the subsumption hierarchy and the RIPR model.

## Provenance

Distilled from Ammann & Offutt, *Introduction to Software Testing* (four structures, RIPR, graph /
logic / data-flow coverage, prime paths, ACC). Principles P058, P066, P079, P082, P083, P097, P098,
P100; claims C00004, C00005, C00006, C00001, C00002, C00222, C00234, C00235; chunk anchor
140e06385751-c0000. Source is distillation-only — no verbatim quotation.
