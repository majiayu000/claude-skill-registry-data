---
name: persistence-mapping-review
kind: skill
status: ready
provenance:
  principles:
  - P020
  - P035
  - P045
  - P014
  claims:
  - C02268
  - C02269
  - C02343
  - C02344
  - C02349
  - C02350
  - C00770
  - C01016
  evidence:
  - E00340
  - E00341
  - E00384
  - E00385
  - E00390
  - E00391
  - E00168
  - E00169
  source_anchors:
  - a6c7e769c072-c0001
  - a6c7e769c072-c0002
  - 8afa2d6eafa0-c0011
  - 8afa2d6eafa0-c0038
  authored_from_digest: e7eb526a9baf7b07b04e4e532fc0b3db805ed402ccf91b9256bf46142938c816
---

# Persistence mapping review

## Purpose

Isolate the in-memory domain from the relational database with a mapping layer so the two can
evolve independently and the domain is not shaped by the schema. Structural mapping patterns —
such as Identity Field, Foreign Key Mapping, and Data Mapper — provide reusable ways to move data
between objects and tables without coupling the domain to persistence. This skill reviews whether a
rich domain is entangled with its store and recommends the mapping that decouples them.

## When to use

- The domain model and database schema are entangled or change together.
- The caller is deciding how an application talks to its relational store.
- Schema concerns (foreign keys, identity columns, joins) have leaked into domain classes.

Do not invoke when there is no rich domain model to protect (e.g. simple table-driven reporting).

## Procedure

1. **Confirm there is a model worth protecting.** This review applies when a rich in-memory domain
   exists. If the application is thin table-driven logic, say so and stop.
2. **Find the entanglement.** Look for the domain depending on the schema: SQL or table shapes
   embedded in domain classes, the object structure dictated by table structure, or the two
   changing in lockstep.
3. **Recommend a mapping layer.** Propose separating the domain from the store with a mapping
   layer (e.g. Data Mapper) so neither side dictates the other's shape and each can evolve
   independently.
4. **Select structural mapping patterns.** Where objects must map to tables, name the applicable
   patterns — Identity Field (object identity ↔ primary key), Foreign Key Mapping (references ↔
   foreign keys), Data Mapper (a layer that moves data both ways) — noting the specific choice is
   situational.
5. **State the trade-off.** The mapping layer adds machinery; in return the domain and schema
   decouple and can change independently. Recommend it where that independence is worth the cost.
6. **Make findings actionable.** For each entanglement, name where the schema leaked, the mapping
   pattern to introduce, and the independence it buys.

## Inputs

- The domain model and the relational schema, and how the application currently moves data between
  them.

## Output

A persistence-mapping assessment: where the domain is entangled with the schema, the mapping layer
and structural patterns to introduce, and the independence-versus-machinery trade-off each carries.

## References

- [Enterprise and integration patterns map](../../references/enterprise-and-integration-patterns-map.md)
  — the structural mapping patterns and the domain/persistence separation.

## Provenance

Distilled from principle(s) **P014/P027/P048/P012**, claims **C00788/C00789/C00863/C00864/C00869/C00870**, evidence **E00139/E00140/E00163/E00164/E00169/E00170**, anchored in the cited architecture sources (`sources/anchors/`). Source is `distillation-only`: content is paraphrased, never quoted verbatim.
