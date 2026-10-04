---
name: designing-data-contracts
description: Define and enforce data contracts between producers and consumers — explicit schema, semantics, ownership, SLAs, and versioning — to prevent silent upstream changes from breaking downstream pipelines. Use when a producer schema change could break consumers, defining an interface between teams/services and the warehouse, or adding schema enforcement at ingestion.
---

# Designing Data Contracts

## When to use

- An upstream (service, event, API, file) feeds downstream pipelines and a change
  could break them silently.
- Defining the interface between a producing team/system and the warehouse.
- Adding schema/quality enforcement at the ingestion boundary.
- Do NOT use for internal model-to-model changes within one dbt project (use
  tests + `handling-schema-evolution`).

## What a contract specifies

- **Schema**: fields, types, nullability, and allowed values.
- **Semantics**: what each field means and its unit/grain.
- **Guarantees**: freshness/SLA, volume expectations, uniqueness of keys.
- **Ownership**: who produces it and who to contact.
- **Versioning + change policy**: how breaking changes are communicated.

## Workflow

```
- [ ] Write the contract as a versioned, checked-in schema (not tribal knowledge)
- [ ] Enforce it at the ingestion boundary (validate on arrival)
- [ ] Classify changes: additive (safe) vs breaking (needs a new version)
- [ ] On violation, reject/quarantine and alert the producer
- [ ] Version and communicate breaking changes ahead of time
```

1. **Make it explicit and versioned.** Store the contract as code (JSON Schema,
   Avro/Protobuf schema, or a YAML spec) next to the pipeline, reviewed like any
   API.
2. **Enforce at the boundary.** Validate incoming data against the contract on
   arrival; reject or quarantine violations instead of loading them.
3. **Classify changes.** Additive/optional fields = backward compatible. Removing
   fields, renaming, tightening types/nullability = breaking → new version.
4. **Fail loudly to the producer**, not silently downstream.

## Patterns

**Contract as JSON Schema (enforced on ingest):**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["order_id", "amount", "ordered_at"],
  "properties": {
    "order_id": { "type": "string" },
    "amount": { "type": "number", "minimum": 0 },
    "ordered_at": { "type": "string", "format": "date-time" },
    "coupon": { "type": ["string", "null"] }
  },
  "additionalProperties": false
}
```

**Enforcement point** — validate each record on ingest; route failures to a
`quarantine` location with the reason, and alert the producing team. This turns a
silent downstream break into an immediate, owned signal at the source.

**Schema registry** (Kafka/Avro) — enforce compatibility (`BACKWARD`) at publish
time so producers cannot ship an incompatible schema.

## Common pitfalls

- **Contract as documentation only** — if it isn't enforced in code, it drifts and
  breaks silently.
- **Enforcing deep in the warehouse** — catch violations at the boundary, before
  bad data spreads.
- **No versioning** — every change becomes an emergency; version and deprecate
  gracefully.
- **`additionalProperties` unrestricted** when you need strictness — unexpected
  fields slip through; set it false where appropriate.
- **No owner** — a rejected batch with no one to call stalls the pipeline.
- **Breaking changes with no lead time** — coordinate producer/consumer via
  versioned schemas and a deprecation window.
