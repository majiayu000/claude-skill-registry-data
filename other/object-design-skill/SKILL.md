---
name: object-design-skill
description: Apply responsibility-driven design with object stereotypes, value objects, entities, aggregates, and encapsulation - language-agnostic
license: Apache-2.0
compatibility: opencode
category: Code Quality
---

## What I do

Design objects by responsibility (RDD/CRC), assign stereotypes, honor Tell-Don't-Ask, Design by Contract, composition over inheritance, Law of Demeter, and value objects. House additions below; textbook mechanics assumed known.

## When to use me

- Modeling a new domain: finding objects and responsibilities, choosing entity vs value object
- Reviewing object interactions (feature envy, inappropriate intimacy, `get`-then-act chains)

## House Learnings

#### Learning: `primitive-obsession-report-type`
Raw `String` for a type code crossing API/service/domain layers has zero compile-time safety — a typo like `"pfd"` silently falls through dispatch and lands in the DB. Replace with a `str`-based Enum value object end-to-end: dispatch via `_GENERATORS[report_type]`, persist `report_type.value`, and `ReportType("pfd")` raises at the boundary instead of corrupting data.

#### Learning: `enum-strategy-resolution`
An enum can be both a type identifier (value object) AND a strategy dispatcher: each member carries `content_type`, `extension`, and `serialize(data)` via properties backed by module-level `_CONTENT_TYPES`/`_SERIALIZERS` maps — eliminating external mapping tables and switch dispatch.

> Removed 2026-09: RDD/CRC walkthroughs, stereotype catalog, DbC pre/post-condition examples, composition-vs-inheritance and Law-of-Demeter explanations, encapsulation levels, entity-vs-value-object tutorials — textbook the model knows; the two codified learnings are this config's additions.
