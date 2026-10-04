---
name: boundary-and-layering-review
kind: skill
status: ready
provenance:
  principles:
  - P046
  - P016
  claims:
  - C01100
  - C01101
  - C00364
  - C00442
  evidence:
  - E00173
  - E00174
  - E00080
  - E00100
  source_anchors:
  - 8afa2d6eafa0-c0047
  - 91e37e1ca511-c0001
  - 91e37e1ca511-c0004
  authored_from_digest: caeaf7ce573ecb1c1db5632ceb16c8e633ee50b4d08cd11a215b88c64256607e
---

# Boundary and layering review

## Purpose

Keep details at the edges as plugins behind boundaries. The database, the web, and frameworks are
details: the architecture should place them outside boundaries so business rules do not depend on
a particular database engine, delivery mechanism, or third-party framework — and so decisions
about those details can be deferred or changed. This skill reviews where infrastructure choices
sit relative to the business rules and where a boundary is missing.

## When to use

- A design couples core business rules to a specific database, framework, or delivery mechanism.
- The caller asks where infrastructure choices belong in the architecture.
- A framework upgrade or database swap would force changes deep in the business rules.

Do not invoke when the system is intentionally a thin adapter around one vendor with no
independent policy.

## Procedure

1. **Locate the business rules.** Identify the durable policy the system exists to enforce —
   the part that should outlive any particular framework or store.
2. **Locate the details.** Identify the database, web/delivery mechanism, and frameworks. These
   are details, not the architecture.
3. **Check for a boundary between them.** Look for an abstraction (port/interface, gateway,
   repository) that the business rules use, behind which the detail is a replaceable plugin. Its
   absence is the finding.
4. **Flag a framework marriage.** If business rules import framework types or inherit framework
   base classes throughout, flag that the durable rules are now coupled to a third party's
   volatile decisions; recommend keeping the framework at arm's length behind a boundary.
5. **Flag a database leak.** If business rules embed schema, SQL, or ORM specifics, flag that the
   store is no longer a plugin; recommend isolating it behind the boundary so the engine/schema
   can change.
6. **State the trade-off and what it defers.** Note that the added boundary/indirection buys
   independence from engine, delivery, and framework churn and lets those decisions be deferred —
   and that the cost is the indirection itself. Tie the recommendation to the characteristics the
   system actually prioritizes.

## Inputs

- The design or code under review, showing where business rules sit relative to the database,
  delivery mechanism, and frameworks.

## Output

A findings list of missing or violated boundaries (framework marriage, database leak, delivery
coupling), each with the coupling consequence, the boundary/plugin to introduce, and the trade-off
the indirection carries.

## References

- [Clean Architecture dependency rule](../../references/clean-architecture-dependency-rule.md) —
  details-as-plugins and the boundary checklist.

## Provenance

Distilled from principle(s) **P033/P022**, claims **C00957/C00958/C01215/C01216**, evidence **E00193/E00194/E00225/E00226**, anchored in the cited architecture sources (`sources/anchors/`). Source is `distillation-only`: content is paraphrased, never quoted verbatim.
