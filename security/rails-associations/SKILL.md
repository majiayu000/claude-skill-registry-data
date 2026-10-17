---
name: rails-associations
description: Use when designing or reviewing deep Active Record association contracts including cardinality, ownership, inverse relationships, through joins, polymorphism, dependent lifecycle, autosave, counters, touch, callbacks, and association testing.
license: MIT
---

# Rails Associations

## Purpose

Treat Active Record associations as executable relationship contracts, not merely convenience methods.

An association defines how records are connected, how foreign keys are interpreted, how objects are traversed and mutated, and what lifecycle behavior occurs when records are added, removed, destroyed, or saved.

Active Record query semantics belong to rails-active-record; schema constraints, foreign keys, indexes, transactions, locks, and migrations belong to rails-database-engineering.

## Activate when

- adding or changing belongs_to, has_one, has_many, has_many :through, or HABTM
- changing association options such as class_name, foreign_key, primary_key, inverse_of, source, or source_type
- marking or migrating away from deprecated Active Record associations
- introducing polymorphic associations
- changing dependent behavior
- changing association creation/removal or collection mutation
- changing autosave, inverse, validation, counter cache, or touch behavior
- adding association callbacks or extensions
- debugging missing, duplicated, stale, or unexpectedly saved associated records
- reviewing N+1 behavior caused by association traversal
- changing join-model ownership in a through association
- changing association tests or fixtures/factories around relationship semantics

## Boundary ownership

| Concern | Primary owner |
|---|---|
| Which relationship should exist: cardinality, ownership, join entity, polymorphism choice | rails-data-modeling |
| Association cardinality and object relationship | rails-associations |
| Relation/query composition and materialization | rails-active-record |
| Foreign keys, indexes, constraints, migrations | rails-database-engineering |
| Validation/error semantics | rails-validations |
| Authorization/tenant scope | rails-security |
| File attachment lifecycle | rails-active-storage |
| Background association deletion | rails-active-job |
| Query cost/N+1 measurement | rails-performance |
| Non-persisted model relationships | rails-active-model |

An association does not itself establish authorization, database integrity, or business workflow ownership.

```text
rails-data-modeling         -> decide the relationship (cardinality, ownership, join entity or polymorphism)
rails-associations          -> express it in Rails (declarations, options, dependent and inverse behavior)
rails-database-engineering  -> enforce it in the database (foreign keys, unique indexes, safe migrations)
```

Compose these skills; do not re-decide a relationship here that `rails-data-modeling` has settled.

## Repository inspection

Before changing an association inspect:

1. Ruby and Rails versions.
2. Both sides of the relationship.
3. Actual foreign-key columns and primary keys.
4. Nullability, indexes, uniqueness, and foreign keys.
5. Existing association options and scopes.
6. Validation and callback behavior.
7. Dependent behavior and database cascades.
8. Existing through/join models.
9. Polymorphic type columns and allowed classes where applicable.
10. Existing inverse_of/autoloading conventions.
11. Factory/fixture construction paths.
12. Query/loading paths and strict-loading expectations.
13. Tenant and authorization boundaries.
14. Cleanup/audit/event behavior.
15. Tests that exercise creation, mutation, deletion, and loading.

Inspect both directions. A change that looks local in one model can change generated methods, autosave, validation, or deletion semantics on the other side.

## Cardinality and ownership

Choose the association from the database/domain ownership, not from method-name convenience.

Typical contracts:

- belongs_to: the foreign key is held by the declaring record
- has_one: one associated record is expected from the declaring side
- has_many: the associated table can reference many records
- has_many :through: traversal and optional join-model behavior are explicit
- has_one :through: singular traversal through an intermediate association
- HABTM: direct many-to-many where a join model carries no domain behavior.

For every relationship state:

- state expected cardinality
- identify foreign-key ownership
- determine whether absence is valid
- determine whether uniqueness is required
- determine whether the database enforces the relationship.

Do not model one-to-one semantics with has_one alone when the database permits multiple child rows.

## Decision rules

1. Settle cardinality and ownership above, then classify the change: association declarations (belongs_to, has_one, has_many, through, polymorphic, inverse), persistence effects (autosave, dependent lifecycle, counter caches and touch, callbacks, extensions), or loading, security, performance, and testing.
2. Load the matching reference below before changing behavior; any dependent or autosave change needs the lifecycle reference.
3. Back every association invariant that must hold under concurrency with a database constraint owned by rails-database-engineering.

## Critical invariants

- Do not model one-to-one semantics with has_one alone when the database permits multiple child rows.
- Do not assume belongs_to validation replaces a database foreign key.
- Do not accept arbitrary client-provided polymorphic type names for constantization or lookup.
- Do not combine database cascading and application destruction callbacks without proving their combined semantics.
- Do not use association callbacks for multi-record workflows, external API calls, authorization engines, or background job orchestration.

## References

Load only the reference for the boundary being changed, before changing behavior there. Each reference is self-contained and one level deep; none links to another. Consult a listed pattern from the pattern catalog only when the change needs its implementation shape.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| a change declares or alters an association's type, options, through path, polymorphism, or inverse | [references/declarations.md](references/declarations.md) | belongs_to contract; has_one and uniqueness; has_many collection semantics; Through associations; Polymorphic associations; Inverse associations | `association-cardinality-contract`, `through-association-contract`, `polymorphic-association-boundary`, `association-inverse-contract` |
| a change alters autosave or nested writes, dependent behavior, counter caches or touch, association callbacks, or extensions | [references/persistence-effects.md](references/persistence-effects.md) | Autosave and nested persistence; Dependent lifecycle; Counter caches and touch; Association callbacks; Association extensions | `association-autosave-contract`, `association-dependent-lifecycle`, `association-counter-touch-contract`, `association-callback-contract` |
| a change alters association loading, crosses tenant or authorization boundaries, has capacity impact, or needs association tests | [references/loading-security-testing.md](references/loading-security-testing.md) | Loading and inverse-aware performance; Security and tenant isolation; Performance and capacity; Testing | `association-loading-contract`, `association-testing` |

## Reference example

Associations declared with inverse_of and counter_cache, including a distinct through-association for a many-to-many read.

```ruby
class Clinic < ApplicationRecord
  has_many :appointments
  has_many :patients, -> { distinct }, through: :appointments
  has_one :address, as: :addressable, dependent: :destroy
end

class Appointment < ApplicationRecord
  belongs_to :clinic, inverse_of: :appointments
  belongs_to :patient, counter_cache: true
end

class Patient < ApplicationRecord
  has_many :appointments
  has_many :clinics, through: :appointments
end

# inverse_of keeps both in-memory sides coherent:
#   clinic.appointments.build(patient: patient).patient.clinic == clinic  # => true
```

## Agent review checklist

- [ ] both association directions inspected
- [ ] cardinality is explicit
- [ ] foreign-key ownership is correct
- [ ] database integrity complements the association
- [ ] through/join ownership is explicit
- [ ] polymorphic classes are bounded
- [ ] inverse behavior is understood
- [ ] autosave semantics are intentional
- [ ] dependent lifecycle is explicit
- [ ] counter/touch coupling is justified
- [ ] association callbacks are narrow
- [ ] loading behavior is measured
- [ ] tenant/security ownership is authoritative
- [ ] relationship mutations are tested
- [ ] deletion and failure paths are tested

## Failure modes

Avoid:

- using has_one without database uniqueness when one-to-one is a hard invariant
- treating association declarations as foreign-key constraints
- choosing HABTM when the join has domain behavior
- accepting arbitrary polymorphic type names
- assuming through-association changes destroy target records
- adding inverse_of without verifying both directions
- assuming parent save persists every associated change
- using dependent callbacks and database cascades without combined-lifecycle analysis
- using counter_cache or touch as an authoritative business source
- putting external side effects in association callbacks
- globally eager-loading associations to mask N+1 problems
- assuming an association proves tenant authorization.

## Verification

Run, as applicable:

1. focused association/model tests
2. schema and foreign-key/index checks
3. query/loading tests for representative traversal
4. authorization/tenant regression tests
5. dependent/delete lifecycle tests
6. autosave/transaction failure tests
7. counter/touch reconciliation tests when used
8. bin/validate
9. branch CI.

Report actual verification evidence; never infer relationship correctness from a passing model boot.

## Rails 8.1 current framework considerations

- Rails 8.1 supports deprecated Active Record associations with reporting modes such as warning, raising, or notification.
- Use association deprecation as migration evidence: identify callers, transition them to the replacement contract, and remove the deprecated boundary only after usage is eliminated.

## Source foundation

Primary current Rails source:

- Active Record Associations Guide: https://guides.rubyonrails.org/association_basics.html

The current guide documents association cardinality, foreign-key integrity, collection mutation methods, through associations, bidirectional/inverse behavior, dependent options, validation, callbacks, association extensions, and association options.

Version-sensitive behavior must be resolved against the repository's actual Rails version.

## Composition

This skill composes with rails-active-record, rails-database-engineering, rails-validations, rails-security, rails-active-job, rails-active-storage, rails-performance, rails-test-engineering, rails-zeitwerk, ruby-clean-code, and ruby-tdd-refactoring.

## Rails Associations changes

For deep Active Record association changes:
- inspect the Rails version, both association directions, foreign-key columns, primary keys, nullability, uniqueness, database foreign keys, scopes, inverse_of, dependent options, callbacks, through/join models, polymorphic types, autosave, counter/touch behavior, tenant ownership, loading paths, and relationship tests before implementation;
- classify the boundary as cardinality/ownership, collection mutation, through join, polymorphic target, inverse/autosave, dependent lifecycle, counter/touch, association callback, loading, or association testing;
- do not infer database integrity from association declarations; use rails-database-engineering for foreign keys, unique constraints, indexes, nullability, and transaction/locking mechanics;
- when has_one means exactly one row, verify database uniqueness rather than relying only on the association declaration;
- keep belongs_to presence/optional semantics aligned with the actual foreign-key and domain contract;
- inspect both sides of every changed relationship; custom foreign_key, class_name, scopes, and through associations can affect inverse inference, autosave, validation, and duplicate queries;
- use inverse_of explicitly when automatic inverse detection is not reliable and verify the resulting identity/autosave behavior;
- treat has_many :through as a join-model contract; do not assume changing a through collection destroys target records;
- prefer a join model over HABTM when the relationship carries attributes, validations, callbacks, authorization, or lifecycle behavior;
- restrict polymorphic target types to an explicit allowed set and never trust client-provided type names for arbitrary constantization;
- treat dependent as lifecycle behavior that must be reconciled with database cascading, foreign-key nullability, attachment cleanup, audits, and transaction boundaries;
- verify asynchronous dependent destruction against the actual Active Job/runtime and database foreign-key contract;
- make autosave/nested persistence ownership explicit; test parent success/failure and associated-record validation failures;
- treat counter_cache and touch as denormalized coupling requiring authoritative-source and reconciliation reasoning;
- keep before_add/after_add/before_remove/after_remove callbacks narrow and deterministic; do not hide external workflows or authorization engines inside them;
- choose association loading from the actual traversal path; review inverse behavior before adding broad eager loading and compose with rails-active-record strict-loading/query guidance;
- keep association validity separate from authorization and tenant isolation; a valid relationship can still cross a security boundary;
- test cardinality, both directions, collection mutation, through changes, polymorphic targets, dependent behavior, autosave failure, security isolation, and representative loading behavior;
- never claim association-performance improvements without measured query/runtime evidence.
