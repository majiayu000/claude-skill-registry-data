---
name: rails-data-modeling
description: Use when deciding what a Rails application's relational schema should represent before writing models or migrations, including entities versus values, keys, normalization, nullability, integrity constraints, type hierarchies, JSON columns, history, soft deletion, and deliberate denormalization.
license: MIT
---

# Rails Data Modeling

## Purpose

Decide what the database should represent before deciding how Rails maps it. Start from the business facts the system must record, not from "which model should I create". The relational model owns correctness; Active Record, associations, and migrations implement it.

```text
business facts
  -> entities and value concepts
  -> ownership and cardinality
  -> keys and functional dependencies
  -> normalized schema (3NF by default)
  -> constraints for every invariant
  -> Rails mapping (models, associations, types)
  -> read and write paths, then indexes
  -> denormalization only for a stated need
  -> history and evolution of existing data
```

## Activate when

- designing tables for a new feature or domain area
- a model is gaining columns that belong to a different concept, or a "god table" is growing
- choosing keys: bigint, UUID, composite, natural, or public identifiers
- choosing between STI, delegated types, polymorphic associations, separate tables, or composition
- deciding whether data belongs in a JSON/JSONB column or in relational columns and tables
- modeling history, snapshots, effective dates, soft deletion, or multi-tenant ownership
- adding a cached, derived, or duplicated value such as a total, counter, or summary
- reviewing a schema for update anomalies, missing constraints, or unclear `NULL` meaning
- mapping a legacy schema, or modernizing Rails guidance written for older Rails versions

## Boundary ownership

| Concern | Primary skill |
|---|---|
| What the schema represents: entities, keys, normalization, constraints to require, history, denormalization policy | rails-data-modeling |
| Association declarations, options, and dependent behavior | rails-associations |
| Migrations, indexes, constraint rollout, backfills, locking, and deploy safety | rails-database-engineering |
| Relation, query, and persistence-lifecycle semantics | rails-active-record |
| Ruby domain objects, aggregates, and invariants in code | ruby-domain-modeling |
| Validation errors and user feedback | rails-validations |
| Tenant access enforcement on every read and write path | rails-authorization |

This skill decides the target model and the constraints it needs; `rails-database-engineering` decides how to get an existing database there safely.

## Repository inspection

1. Resolve the Rails and database versions from `Gemfile.lock` and `config/database.yml`; several choices below depend on them.
2. Read `db/schema.rb` or `db/structure.sql`, existing constraints, indexes, and foreign keys.
3. Read the models touched: associations, validations, callbacks, enums, serialized and JSON attributes, and STI or delegated types.
4. Read the domain glossary and decision records (see `ruby-domain-modeling`).
5. Identify the real read and write paths: controllers, jobs, reports, imports, and external synchronization.
6. Estimate data volume and growth for tables being split, merged, or backfilled.
7. Check tenancy conventions: which column scopes data, and how uniqueness is scoped today.

Never infer database behavior from model code alone.

## Decision framework

Walk every new piece of data through these questions, in order, and record the answers in the change or its spec. Each answer constrains the next.

```text
 1. What business fact is this?                       -> name it in the domain glossary
 2. Does it have independent identity?                 -> entity (table) or value (columns)
 3. Does it have an independent lifecycle?             -> separate table, or owned by its aggregate
 4. Who owns it?                                       -> aggregate root; tenant column
 5. What determines its value?                         -> functional dependency; which table stores it
 6. What is its cardinality?                           -> 1:1, 1:N, N:M (join model)
 7. Is it optional, and what would absence mean?       -> NOT NULL, or one stated meaning for NULL
 8. Must it be unique, and within what scope?          -> unique index, composite with tenant or parent
 9. Should it be normalized?                           -> 3NF unless a recorded reason says otherwise
10. Is it historical or current state?                 -> snapshot, effective-dated rows, or plain column
11. Is a JSON column justified?                        -> only if never joined, filtered, sorted, or constrained
12. What database constraint enforces it?              -> FK, NOT NULL, UNIQUE, CHECK, EXCLUDE
13. How will Rails represent it?                       -> model, association, enum, value object, type
14. Which queries and write paths does it serve?       -> indexes, counters, caches, and who writes it
```

A question you cannot answer from the requirements or the repository goes to `planning-interview`, not to a guess.

## Decision rules

1. **List the facts first.** A fact is stored once, where its determinant lives.
2. **Separate entities from values.** Things with identity and a lifecycle (Order, Invoice, Membership) get tables. Values defined only by their content (Money, Address, DateRange) are columns owned by an entity, read through a value object, unless they need their own lifecycle or sharing.
3. **Normalize to 3NF by default.** Remove repeating groups (1NF), attributes that depend on only part of a composite key (2NF), and attributes that depend on another non-key attribute (3NF). Depart from it only by a recorded decision.
4. **Keep identity and uniqueness separate.** The primary key is persistence identity; business uniqueness (email, SKU, slug) is a unique constraint. Do not make a mutable business value the primary key.
5. **Give `NULL` one meaning.** When a column could mean "unknown", "not applicable", and "not yet", use an explicit state instead of `NULL`.
6. **Back every invariant with a constraint.** Validations add user feedback, not integrity.
7. **Choose hierarchies and flexible data deliberately.** STI, delegated types, polymorphic associations, and JSON columns each trade integrity or queryability for convenience; record the choice.
8. **Preserve history on purpose.** A value recording what was true at a moment (the price on an order line) is a separate fact from the current value, not a normalization error.
9. **Denormalize only with an owner.** Every cached, counted, or copied value names its source, update path, repair path, and behavior on failure.
10. **Design indexes from access paths.** Normalization decides which facts exist; indexes follow the queries and write paths that use them.
11. **Treat existing data as part of the model.** A schema change is done only when existing rows satisfy it; plan backfills and constraint rollout with `rails-database-engineering`.

## Version-sensitive compatibility

Resolve the Rails version from `Gemfile.lock` before choosing an API.

- **Current Rails**: use the modern API: relation methods, `update`, `self.table_name =`, `enum :status, {...}`, native composite primary keys, `id: :uuid`, check, unique, and exclusion constraints.
- **Legacy Rails**: recognize historical APIs (`find(:all, conditions: ...)`, `update_attributes`, `set_table_name`, `set_primary_key`, `ActiveRecord::Observer`, plugin-based composite keys) so you can read and upgrade old code and old guidance.
- **Never generate a legacy API in a modern application** unless repository evidence (the resolved version, or an established local convention during an upgrade) requires it. Older books and blog posts are sources of concepts, never of syntax.

The removed-API table and the version each feature needs are in `references/legacy-schemas-and-api-drift.md`.

## Critical invariants

- Model the business facts before choosing Rails models.
- Normalize for correctness first; denormalize only for a stated requirement or measured workload.
- A Rails association or validation is not an integrity guarantee; the database constraint is.
- A `has_one` needs a unique index on its foreign key, or the database allows many.
- Tenant-scoped business keys need a composite unique index that includes the tenant column.
- JSON columns never hold identifiers, statuses, or timestamps the application joins, filters, sorts, or constrains on.
- Never "normalize away" a historical snapshot.
- Never teach or generate removed Rails APIs; see the legacy reference for replacements.

## References

Load only the reference for the decision in front of you; each is one level deep. Consult a listed pattern only when the change needs its implementation shape.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| identifying facts, dependencies, normal forms, or choosing keys | [references/normalization-and-keys.md](references/normalization-and-keys.md) | Functional dependencies; 1NF, 2NF, 3NF, BCNF; anomalies; primary key strategies; natural, surrogate, and public keys | `value-object` |
| relating tables, deciding nullability, or choosing constraints | [references/relationships-and-integrity.md](references/relationships-and-integrity.md) | Foreign key ownership; one-to-one; join models; `NULL` semantics; constraint matrix; multi-tenant keys | `bounded-context-contract` |
| choosing STI, delegated types, polymorphism, enums, JSON columns, or value-object mapping | [references/types-hierarchies-and-flexible-data.md](references/types-hierarchies-and-flexible-data.md) | Hierarchy decision table; enum options; JSON boundary; value-object mapping | `value-object` |
| modeling history, snapshots, soft deletion, derived values, or denormalization | [references/history-and-denormalization.md](references/history-and-denormalization.md) | Snapshots; temporal data; soft deletion; derived versus stored; controlled denormalization | none |
| mapping a legacy schema or modernizing older Rails guidance | [references/legacy-schemas-and-api-drift.md](references/legacy-schemas-and-api-drift.md) | Legacy mapping APIs; removed and replaced APIs; version-gated features | none |
| deciding aggregate ownership, the Rails representation, indexes, write paths, counters, or how the model evolves | [references/aggregates-access-and-evolution.md](references/aggregates-access-and-evolution.md) | Aggregate ownership; Rails mapping matrix; query-driven index design; write paths; counter caches and aggregates; schema evolution | `postgres-index-from-query-evidence`, `association-counter-touch-contract`, `expand-contract-migration` |
| a worked example is closer to the task than the rules | [references/worked-examples.md](references/worked-examples.md) | Commerce snapshots; SaaS multi-tenancy; JSON versus relational; UUID versus bigint; composite primary keys; a reconciled order total | `value-object` |

## Data-model review procedure

Review a proposed or existing schema in this order, and report findings per step:

1. **Facts**: list every stored fact and its determinant; flag facts stored twice without a snapshot or denormalization record.
2. **Normal form**: flag repeating groups, partial dependencies, and transitive dependencies.
3. **Identity**: check primary keys, business keys, and public identifiers; flag mutable primary keys.
4. **Integrity**: every relationship has a foreign key, every required value `NOT NULL`, every business key a unique index at the right scope, every value domain a check constraint.
5. **Tenancy**: every tenant-owned table carries the tenant column; uniqueness and foreign keys are tenant-scoped.
6. **Flexible data**: JSON columns hold nothing the application joins, filters, sorts, or constrains on; hierarchy and polymorphism choices are justified.
7. **History and derived data**: snapshots preserved, derived values not stored without an owner, soft deletion decided end to end.
8. **Access paths**: indexes match real queries; write paths, hot rows, and counters are accounted for.
9. **Evolution**: the migration path from today's data is safe and staged (with `rails-database-engineering`).
10. **Rails mapping and version**: associations, enums, and types match the schema and the resolved Rails version; no removed APIs.

## Agent review checklist

- [ ] Rails and database versions resolved; version-gated APIs checked
- [ ] facts listed with their determinants and owners
- [ ] entities and values separated; no table for a pure value without reason
- [ ] schema at 3NF, or each departure recorded
- [ ] primary key strategy chosen; business keys have unique constraints
- [ ] every nullable column has a stated meaning
- [ ] every invariant has a database constraint, with tenant scope where needed
- [ ] hierarchy, polymorphism, enum, and JSON choices justified
- [ ] historical snapshots preserved; derived values not stored without an owner
- [ ] each denormalized value has a source, update path, and repair path
- [ ] each index traces to a query or write path
- [ ] aggregate roots own their children's mutations
- [ ] existing data, backfill, and constraint rollout planned with rails-database-engineering
- [ ] no legacy API generated for a modern application

## Failure modes

- starting from a model name instead of the facts the system records
- comma-separated or array columns holding independent facts that are filtered or joined
- copying a parent's attribute into child rows (a 2NF or 3NF violation) without a snapshot reason
- a mutable email, slug, or SKU as primary key
- `has_one` or `validates uniqueness` without the unique index
- nullable columns whose `NULL` means several things
- a JSON column holding the status or foreign key the application queries
- polymorphic associations used only to avoid creating a table, losing foreign keys
- STI across subclasses with mostly disjoint columns
- a stored total or count with no reconciliation path
- `deleted_at` added without deciding uniqueness, dependents, and default scoping
- guidance or generated code using removed APIs such as `update_attributes` or `find(:all, conditions: ...)`

## Verification

- Load the schema in a test database and prove each constraint rejects bad data: insert duplicates, orphans, `NULL`s, and out-of-domain values through SQL or `insert_all`, which skips validations and callbacks.
- Test the Rails mapping at the model and request level, including the validation error for each constrained rule.
- For denormalized values, test the update path and the repair job against a deliberately drifted row.
- For migrations on existing data, follow the verification in `rails-database-engineering`.

## Source foundation

- Rails guides: Active Record Basics, Associations, Migrations, Validations, and Active Record and PostgreSQL (https://guides.rubyonrails.org/). Resolve version-specific behavior against the application's Rails version.
- Relational theory: functional dependencies, normal forms (1NF through BCNF), and update anomalies as described by E. F. Codd and standard database texts.
- The durable Active Record concepts in *Pro Active Record: Databases with Ruby and Rails* (Apress, 2007): the object-relational mapping model, foreign-key ownership, transactions, locking, migrations as schema history, and legacy-schema mapping. Its API examples predate current Rails and are not used; the legacy reference lists their replacements.
