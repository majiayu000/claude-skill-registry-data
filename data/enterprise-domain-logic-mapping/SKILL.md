---
name: enterprise-domain-logic-mapping
kind: skill
status: ready
provenance:
  principles:
  - P060
  - P016
  claims:
  - C00600
  - C00601
  - C00364
  - C00442
  evidence:
  - E00133
  - E00134
  - E00080
  - E00100
  source_anchors:
  - 8afa2d6eafa0-c0002
  - 91e37e1ca511-c0001
  - 91e37e1ca511-c0004
  authored_from_digest: 6fa6337fc60f3a47ed67e9b35425c654e6908b316e12eb93a268a27b525369d6
---

# Enterprise domain-logic mapping

## Purpose

Layer an enterprise application and organize its domain logic by the complexity of the business
logic, not by habit. Layering into presentation, domain, and data-source layers localizes change
and lets each layer be reasoned about on top of a coherent layer below — at the cost of added
indirection. Within the domain layer, the organization (Transaction Script, Domain Model, or Table
Module) should be chosen by how complex the business logic is, because each pattern's cost-benefit
shifts as the logic grows. This skill maps the application to those layers and the right
domain-logic pattern.

## When to use

- Reviewing or designing the internal structure of an enterprise/business application.
- The caller asks how to organize business logic of varying complexity.
- A complex domain is being forced into procedural scripts, or trivial logic into a heavy model.

Do not invoke when the application has negligible business logic (a pure CRUD pass-through).

## Procedure

1. **Check the layering.** Confirm presentation, domain, and data-source concerns are separated
   into layers. Mixed concerns (e.g. business rules in the UI or SQL in the domain) are the first
   finding; layering localizes change.
2. **Acknowledge the indirection cost.** Note that layering adds indirection; recommend it where
   localized change is worth that cost, not as an unconditional good.
3. **Gauge domain-logic complexity.** Assess how complex the business logic is and how it is
   expected to grow.
4. **Choose the domain-logic pattern by complexity.**
   - *Transaction Script* — simple, mostly procedural logic per use case; cheap to start, but
     costs rise as logic and duplication grow.
   - *Domain Model* — rich, interrelated business rules; higher up-front cost, but it scales with
     complexity.
   - *Table Module* — a single class per table mediating a record-set; a middle option that fits
     table-oriented logic and tooling.
   Match the pattern to the assessed complexity, and state the cost-benefit shift if the logic
   grows.
5. **Flag mismatches.** A complex domain on Transaction Scripts (duplication, tangle) or trivial
   logic on a full Domain Model (over-engineering) are both findings; recommend the pattern that
   fits the actual complexity.
6. **Tie it to persistence.** Where a rich Domain Model is chosen, hand off to
   `persistence-mapping-review` to keep the model isolated from the database.

## Inputs

- The application's current or proposed internal structure and a description of its business-logic
  complexity.

## Output

A layering-and-domain-logic assessment: whether the layers are separated, which domain-logic
pattern fits the assessed complexity, the mismatches found, and the indirection/cost trade-off
each choice carries.

## References

- [Enterprise and integration patterns map](../../references/enterprise-and-integration-patterns-map.md)
  — the layering and domain-logic patterns and when each applies.

## Provenance

Distilled from principle(s) **P050/P022**, claims **C00008/C00009/C01215/C01216**, evidence **E00004/E00005/E00225/E00226**, anchored in the cited architecture sources (`sources/anchors/`). Source is `distillation-only`: content is paraphrased, never quoted verbatim.
