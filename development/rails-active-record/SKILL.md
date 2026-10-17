---
name: rails-active-record
description: Use when implementing or reviewing deep Active Record model, relation, query, persistence lifecycle, scope, callback, bulk-write, deletion, or loading behavior. Also covers routine model, migration, query, scope, callback, and transaction changes.
license: MIT
---

# Rails Active Record

## Purpose

Treat Active Record as both an object/persistence protocol and a query-building system whose behavior must remain explicit at the model, relation, and database boundaries.

This skill owns Active Record object and Relation semantics; rails-database-engineering owns production database mechanics such as schema migration, indexes, constraints, transaction isolation, locking, connection pools, and query-plan operations. rails-associations and rails-validations remain specialized ownership boundaries.

## Activate when

- changing ActiveRecord::Base or ApplicationRecord model behavior
- adding or changing scopes or Relation composition
- changing query loading, projection, ordering, grouping, joins, or aggregation
- changing persistence lifecycle behavior
- changing save, update, destroy, or delete semantics
- introducing or reviewing Active Record callbacks
- changing bulk update/delete/import behavior
- changing eager loading, strict loading, or N+1 behavior
- reviewing default_scope or unscoped behavior
- changing serialized or typed Active Record attributes
- debugging differences between in-memory model state and persisted database state
- reviewing Active Record code for accidental materialization or hidden queries

Routine model, migration, or query changes also route here; start them from `references/routine-changes.md`.

## Boundary ownership

| Concern | Primary skill |
|---|---|
| What the schema should represent: entities, keys, normalization, history, denormalization | rails-data-modeling |
| Active Record model and Relation semantics | rails-active-record |
| Associations/cardinality/dependent relationships | rails-associations |
| Model validation/error semantics | rails-validations |
| Non-persisted Rails model protocol | rails-active-model |
| Schema/migration/index/constraint engineering | rails-database-engineering |
| Query performance measurement/N+1 investigation | rails-performance |
| Request input/output boundary | rails-action-controller |
| Domain workflow extraction | ruby-domain-modeling / ruby-service-objects |
| Async lifecycle/retries | rails-active-job |

Do not collapse these skills into one model abstraction merely because they all touch Active Record.

```text
rails-data-modeling  -> defines what is modeled: facts, tables, keys, constraints
rails-active-record  -> defines how Active Record operates on it: relations, persistence, callbacks
```

When a change adds a table, moves a fact, or adds a cached or copied value, settle the model with `rails-data-modeling` first.

## Repository inspection

Before implementation inspect:

1. Ruby and Rails versions and the resolved Active Record version.
2. ApplicationRecord inheritance and abstract classes.
3. Relevant model, schema, migrations, indexes, and constraints.
4. Associations and dependent behavior.
5. Validations and validation contexts.
6. Callbacks, especially transactional callbacks.
7. Scopes, default_scope, and relation extensions.
8. Existing query objects/services/repositories.
9. Factories/fixtures and test helpers.
10. Existing query/load behavior, including includes, preload, eager_load, and strict_loading.
11. Batch processing conventions.
12. Bulk write/delete/import conventions.
13. Observability/query logging and performance tooling.
14. Security or tenant-scoping conventions.
15. Neighboring models before introducing shared abstractions.

Never infer database semantics from model code alone.

## Decision rules

1. Classify the change before editing: model boundary, Relation/query semantics, scope/default_scope, loading, persistence lifecycle, callbacks, bulk writes/deletes, transactions, tenant scope, or testing. A change can touch several.
2. Load the matching reference below and apply it before changing behavior. Routine model, migration, and query edits load `references/routine-changes.md` first and escalate to the deeper references only when those boundaries are in play.
3. Hand schema, index, constraint, locking, and isolation work to rails-database-engineering, and measured query cost to rails-performance.

## Critical invariants

- Treat ActiveRecord::Relation as a lazy query description until a terminal operation; do not turn a composable Relation into an Array or scalar without preserving the caller contract.
- Never use default_scope as an authorization mechanism.
- Do not use callbacks to hide multi-record workflows, authorization decisions, unrelated integrations, request-specific behavior, or job orchestration.
- Use after_commit or after_rollback when an effect depends on transaction outcome; after_save does not mean the transaction committed.
- A bulk operation is not automatically equivalent to iterating through model instances: validations, callbacks, timestamps, and dirty tracking may not run.
- Never replace destroy_all with delete_all just for speed without reviewing lifecycle, dependency, and audit contracts.
- Do not treat in-memory model state as authoritative database state after independent or concurrent writes.
- Dynamic SQL identifiers require an explicit allowlist; values stay parameterized.

## References

Load only the reference for the boundary being changed, before changing behavior there. Each reference is self-contained and one level deep; none links to another. Consult a listed pattern from the pattern catalog only when the change needs its implementation shape.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| a change alters model ownership, Relation composition, query shape, scopes/default_scope, or projections | [references/relations-and-queries.md](references/relations-and-queries.md) | Model boundary; Relation semantics; Query composition; Scopes and default_scope; Projection and calculations | `active-record-model-boundary`, `active-record-relation-composition`, `active-record-query-contract`, `active-record-scope-contract` |
| a change alters eager/strict loading, N+1 behavior, batching, or query cost | [references/loading-and-performance.md](references/loading-and-performance.md) | Loading strategy; Performance and capacity | `active-record-strict-loading` |
| a change alters save/update/destroy semantics, callbacks, dirty tracking, or transaction participation | [references/persistence-lifecycle-and-callbacks.md](references/persistence-lifecycle-and-callbacks.md) | Persistence lifecycle; Callbacks; Dirty and persistence state; Transactions and consistency | `active-record-persistence-lifecycle`, `active-record-callback-contract` |
| a change uses update_all, delete_all, destroy_all, insert/upsert, or alters deletion behavior | [references/bulk-writes-and-deletion.md](references/bulk-writes-and-deletion.md) | Bulk writes and deletes; Deletion semantics | `active-record-bulk-write-boundary`, `active-record-deletion-contract` |
| a query crosses tenant, authorization, unscoped, raw SQL, or dynamic identifier boundaries | [references/security-and-tenant-scope.md](references/security-and-tenant-scope.md) | Security and tenant scope | none |
| choosing or writing tests for Active Record behavior | [references/testing.md](references/testing.md) | Testing | `active-record-testing` |
| the change is a routine model, migration, scope, callback, or query edit | [references/routine-changes.md](references/routine-changes.md) | Routine model, migration, and query changes | none |

## Reference example

Deep Active Record work: composable scopes, strict loading to surface N+1, and a deliberate, commented bulk-write bypass.

```ruby
class Invoice < ApplicationRecord
  has_many :line_items, inverse_of: :invoice

  scope :unpaid, -> { where(paid_at: nil) }
  scope :overdue, ->(as_of: Date.current) { unpaid.where(due_on: ...as_of) }

  def self.account_digest(account)
    where(account_id: account.id)
      .includes(:line_items)   # eager load planned up front
      .strict_loading          # any unplanned lazy load raises instead of N+1-ing
      .map { |invoice| [invoice.reference, invoice.total_cents] }
  end
end

# Bulk writes skip the model lifecycle by contract; state that explicitly:
#   Invoice.insert_all!(rows, record_timestamps: true)  # no validations/callbacks
#   invoice.update_columns(paid_at: Time.current)       # deliberate callback bypass
```

## Agent review checklist

- [ ] Rails/Active Record version resolved
- [ ] model and ApplicationRecord boundary inspected
- [ ] schema/constraints checked
- [ ] relation laziness/materialization understood
- [ ] query composition preserves cardinality and ordering
- [ ] scope/default_scope semantics are explicit
- [ ] loading strategy is justified
- [ ] projection/materialization contract is correct
- [ ] persistence lifecycle is understood
- [ ] callbacks are intrinsically owned and scoped
- [ ] bulk operation semantics are explicit
- [ ] deletion semantics preserve dependents/audits
- [ ] dirty state is not confused with persistence
- [ ] transaction boundary is explicit
- [ ] tenant/authorization predicates are authoritative
- [ ] tests prove the relevant lifecycle/query contract
- [ ] performance claims have evidence when material

## Failure modes

Avoid:

- treating ActiveRecord::Relation as a plain Array before the contract requires materialization
- changing a composable relation into pluck prematurely
- adding default_scope for authorization
- disabling strict loading instead of fixing an N+1 boundary
- assuming callbacks run for bulk operations
- replacing destroy with delete for an unmeasured speed gain
- using model callbacks for multi-record workflows
- assuming after_save means the database transaction is committed
- assuming an in-memory model is current database truth
- forwarding dynamic order or column input directly into SQL
- claiming preload/eager loading improved performance without evidence
- hiding tenant predicates inside default_scope and treating that as complete authorization.

## Verification

Run, as applicable:

1. focused model/query tests
2. callback and lifecycle tests
3. request/integration tests for security-visible query changes
4. query-count or performance tests when material
5. schema/constraint checks for coupled persistence changes
6. bin/validate
7. branch CI.

Report actual verification evidence. Never infer Active Record behavior from a green unit test that does not exercise the relevant query/lifecycle boundary.

## Source foundation

Primary current Rails sources:

- Active Record Basics: https://guides.rubyonrails.org/active_record_basics.html
- Active Record Query Interface: https://guides.rubyonrails.org/active_record_querying.html
- Active Record Callbacks: https://guides.rubyonrails.org/active_record_callbacks.html
- Active Record Associations: https://guides.rubyonrails.org/association_basics.html
- Active Record Validations: https://guides.rubyonrails.org/active_record_validations.html

Current Rails documentation explicitly covers CRUD/model persistence, Relations, batch iteration, strict loading, scopes/default_scope, projections such as pluck, and transactional callbacks. Version-sensitive behavior must still be checked against the repository's resolved Rails version.

## Composition

This skill composes with rails-associations, rails-validations, rails-active-model, rails-database-engineering, rails-performance, rails-security, rails-test-engineering, ruby-clean-code, and ruby-tdd-refactoring.

## Rails Active Record changes

For deep Active Record changes:
- inspect the resolved Rails/Active Record version, ApplicationRecord inheritance, model/schema/migrations, associations, validations, callbacks, scopes, default_scope, query consumers, loading conventions, bulk operations, security/tenant rules, performance evidence, and tests before implementation;
- classify the boundary as model ownership, Relation semantics, query composition, scope/default_scope, loading, persistence lifecycle, callbacks, bulk writes/deletes, or Active Record testing;
- keep rails-active-record focused on Active Record object/Relation semantics while delegating schema, indexes, constraints, transactions, locking, isolation, and query-plan mechanics to rails-database-engineering;
- treat ActiveRecord::Relation as a query description until an intended terminal/materializing operation; do not change a composable Relation into an Array or scalar result without preserving the caller contract;
- make ordering and cardinality explicit whenever a query is part of a contract; joins, distinct, grouping, and projections can change result shape;
- use scopes for composable named semantics and treat default_scope as high-risk implicit behavior; never use default_scope as an authorization mechanism;
- choose preload/includes/eager_load/joins/strict_loading from the actual consumer path; do not globally preload graphs or disable strict loading to silence regressions;
- use pluck/pick and other projections only when the caller actually needs scalar data; projection is a contract change, not a generic optimization;
- inspect the exact persistence method before changing it because validations, callbacks, timestamps, dirty state, and transactions differ across write APIs;
- use model callbacks only for lifecycle behavior intrinsic to the record; keep multi-record workflows, authorization, and external integrations outside callbacks;
- use after_commit or after_rollback when an effect depends on transaction outcome, and retain idempotency/correlation for retried external effects;
- do not assume bulk update/delete/import/upsert operations execute per-record validations or callbacks; review database constraints and audit/event semantics before using them;
- do not replace destroy_all with delete_all solely for speed; inspect dependent, callback, storage, auditing, and database-cascade behavior;
- do not treat in-memory model state as authoritative database state after independent or concurrent writes; reload or query authoritative state when required;
- keep tenant predicates and authorization authoritative outside hidden scope assumptions and review unscoped/raw SQL/dynamic identifiers as security boundaries;
- for large datasets, prefer bounded batch processing such as find_each/find_in_batches when their ordering and concurrency semantics fit the workload;
- test Relation type/composition, persistence success/failure, callback commit/rollback, bulk lifecycle, strict loading, deletion/dependents, and tenant boundaries at the owning test layer;
- never claim an Active Record query or loading optimization improved performance without query/runtime evidence.
