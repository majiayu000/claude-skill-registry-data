---
name: rails-database-engineering
description: Use when changing Rails database schemas, migrations, indexes, constraints, transactions, locking, query strategy, connection pools, backfills, or production database operations.
license: MIT
---

# Rails Database Engineering

## Purpose
Treat the database as a production contract, not an implementation detail. Deciding what the schema should represent (entities, keys, normalization, hierarchies, history, denormalization) belongs to `rails-data-modeling`; this skill evolves and enforces it safely.

```text
"Should this fact be a separate relation?"  -> rails-data-modeling
"How do I migrate it safely?"               -> rails-database-engineering
```

Reason across:
```text
application code
  -> Active Record
  -> transaction / lock
  -> connection pool
  -> SQL/query plan
  -> schema/index/constraint
  -> deployment and migration ordering
```

Primary references:
- https://guides.rubyonrails.org/active_record_migrations.html
- https://api.rubyonrails.org/classes/ActiveRecord/Transactions/ClassMethods.html
- https://api.rubyonrails.org/classes/ActiveRecord/Locking/Pessimistic.html
- https://api.rubyonrails.org/classes/ActiveRecord/ConnectionAdapters/ConnectionPool.html
- https://api.rubyonrails.org/classes/ActiveRecord/Relation.html
- https://www.postgresql.org/docs/current/sql-createindex.html

## Activate when
- adding, changing, or removing schema elements
- adding indexes or unique constraints
- changing column nullability or types
- writing production data backfills
- changing transaction or isolation behavior
- adding row locking
- diagnosing deadlocks, lock waits, or serialization failures
- changing connection pool sizing
- diagnosing pool exhaustion
- changing bulk SQL/Active Record operations
- reviewing query plans or query performance
- introducing database-specific SQL
- designing zero-downtime or expand/contract migrations
- changing multiple-database/shard behavior

## Repository inspection
Inspect:

1. Ruby/Rails/runtime version
2. database adapter and database version when available
3. schema.rb/structure.sql
4. db/migrate and migration conventions
5. application models and associations
6. existing indexes, foreign keys, check constraints, and unique constraints
7. database.yml/config/database configuration
8. connection pool settings per process/role/shard
9. deployment/release order
10. background jobs touching the same data
11. transaction and lock usage
12. large-table/data-volume assumptions
13. existing backfill tooling
14. read/write role or shard configuration
15. query logs/profiles when optimizing queries

Do not choose a migration strategy from the migration file alone. Determine existing data, traffic, deployment ordering, and database behavior.

## Schema changes are deployment contracts
Prefer a multi-phase migration for production changes that cannot be safely applied atomically:

```text
expand
  -> deploy compatible application
  -> backfill
  -> validate
  -> contract
```

The old and new application versions may overlap during a rolling deployment. A migration is safe only if each intermediate database state is compatible with the application versions that can run against it.

Do not combine destructive schema changes with the first deploy that stops using the old column unless the deployment topology guarantees no overlap.

## Migration immutability
Once a migration has been applied in shared environments, treat it as historical record.

Do not rewrite an old production migration to change its meaning. Add a new migration unless the migration is demonstrably local and unapplied.

Rails identifies migrations by timestamp and runs them in version order. Rails also updates schema.rb after db:migrate.

## Reversibility
Prefer `change` when Rails can infer the reverse operation.

When the operation is not automatically reversible, use `reversible` or explicit `up`/`down` methods.

For destructive operations, explicitly decide whether rollback is meaningful. Rails supports `ActiveRecord::IrreversibleMigration` when a down migration cannot safely recreate destroyed state.

Never promise rollback safety if the migration destroyed data.

## DDL transactions
Rails wraps migrations in transactions when the database supports transactional DDL. Some operations cannot run inside a transaction and require `disable_ddl_transaction!`. Rails documents both behaviors.

When disabling migration transactions:
- understand the partial-application failure state;
- document manual recovery;
- avoid assuming the migration is atomic;
- use explicit validation/recovery steps.

## Indexes
An index is a write/storage/cost trade-off, not a free optimization.

Before adding one, inspect:
- query predicates and joins;
- ordering/grouping requirements;
- selectivity and data distribution;
- existing composite/partial indexes;
- write frequency;
- index storage and maintenance cost.

Index column order must reflect actual query shapes. Do not add independent indexes simply because columns appear in WHERE clauses.

## PostgreSQL production indexes
PostgreSQL `CREATE INDEX CONCURRENTLY` avoids locks that prevent concurrent inserts, updates, and deletes, but requires more work and cannot run inside a transaction block. A failed concurrent build can leave an invalid index requiring cleanup.

When adding a large-table production index on PostgreSQL:

```text
assess lock risk
-> decide concurrent build
-> disable migration DDL transaction if required
-> create index concurrently
-> verify valid/usable index
-> handle invalid-index failure explicitly
```

Do not use `algorithm: :concurrently` or raw SQL merely by habit. Confirm adapter/version support and the migration transaction behavior first.

## Constraints over application-only validation
When a business invariant must hold for all writers, prefer a database constraint in addition to application validation.

Examples:
- unique business key -> unique index/constraint;
- required state -> NOT NULL;
- permitted relation -> foreign key;
- bounded numeric/text condition -> CHECK constraint.

Model validation improves application UX; a database constraint is the final concurrency-safe enforcement boundary.

Test both application behavior and database constraint behavior.

## Foreign keys and referential integrity
Use foreign keys when the relationship must be structurally enforced at the database boundary.

Before adding one to an existing table:
1. audit orphan rows;
2. clean invalid data;
3. add the constraint using a production-safe strategy;
4. validate it where the database supports deferred validation;
5. verify application code handles constraint violations.

Do not assume `dependent:` options are equivalent to database foreign keys.

## Nullability changes
Changing a nullable column to NOT NULL is a data migration, not just a schema edit.

Safer pattern:

```text
add/write-compatible default path
-> backfill existing NULL rows
-> prevent new NULL writes
-> validate no NULLs remain
-> add NOT NULL
```

Do not add `null: false` to a large populated table without proving existing and concurrent writes are safe.

## Type changes
Column type changes can rewrite large tables, lock writes, or silently change interpretation.

Before changing type:
- assess current values;
- assess table size;
- assess database-native cast behavior;
- assess lock duration;
- consider dual-write/dual-read or expand/contract;
- verify rollback/recovery.

## Data backfills
Backfills must be designed for production load.

Prefer:
- batches;
- bounded transactions;
- deterministic ordering/cursors;
- resumability/checkpoints;
- idempotency;
- throttling when necessary;
- metrics/progress reporting;
- a clear completion criterion.

Avoid loading millions of records into Ruby memory just to transform them.

Active Record bulk methods such as `update_all` operate with a single SQL statement and bypass model callbacks/validations; the repository must explicitly account for those skipped behaviors.

Never mix irreversible destructive cleanup into a backfill unless the data-recovery story is explicit.

## Transactions
Use a transaction when several database mutations must succeed or fail together.

Do not treat a transaction as a lock or distributed coordination primitive.

Transactions define database atomicity. They do not automatically make external API calls, jobs, caches, or other systems atomic with the database.

Use `after_commit` when an external side effect must occur only after successful commit. Rails provides `after_commit` and related callbacks for this boundary.

Keep transactions short. Avoid network calls or long CPU work while holding a transaction unless the architecture explicitly requires it.

## Isolation
Isolation level is a correctness decision.

Before changing it, identify the anomaly you are preventing:

```text
dirty read
non-repeatable read
phantom read
lost update
write skew
serialization anomaly
```

Choose the least expensive isolation/locking model that guarantees the required invariant, based on the actual database adapter/version.

Do not raise isolation merely because concurrency feels unsafe.

## Pessimistic locking
Rails supports row locking through `lock!`, `with_lock`, and relation-level `lock` clauses. `with_lock` runs the block inside a transaction and locks the record before yielding.

Use row locks when two transactions can otherwise modify the same state concurrently and the lock boundary is the invariant.

Keep the locked section short.

Explicit database-specific clauses such as PostgreSQL `FOR UPDATE NOWAIT` can be appropriate when the failure-fast behavior is part of the contract. Rails exposes custom locking clauses.

Do not use locks to compensate for missing unique constraints or idempotency.

## Deadlocks
Deadlocks are a coordination problem.

Reduce risk by:
- acquiring locks in a consistent order;
- keeping transactions short;
- reducing the number of locked rows;
- avoiding unnecessary lock escalation;
- separating unrelated operations;
- using retry only when the operation is safely retryable.

Never blindly retry arbitrary transaction failures because retrying a non-idempotent operation can duplicate side effects.

## Query strategy
Use the database for set operations when practical.

Distinguish:

```text
relation.size  -> SQL COUNT when unloaded
relation.to_a  -> loads records
update_all     -> single SQL UPDATE, skips callbacks/validations
```

Rails' current Relation API documents that `size` counts when the relation is not loaded, while loaded relations use in-memory length. It also documents that `update_all` issues one SQL UPDATE without instantiating models or running callbacks/validations.

Use `to_sql`, database query plans, logs, and benchmarks to validate actual query behavior.

## Query plans
When optimizing a query:

```text
identify workload
-> capture generated SQL
-> EXPLAIN / EXPLAIN ANALYZE in a representative environment
-> inspect index/scan/join/cardinality estimates
-> change query/index
-> re-measure
```

Do not claim an index improved performance without workload evidence.

Never run `EXPLAIN ANALYZE` against production casually; it executes the query.

Set a statement timeout for the session before running it, so a slow plan cannot hold a connection open for the full query.

## Connection pools
Connection pooling is a capacity boundary.

Each concurrent execution context can need a database connection. Pool sizing must account for:
- web worker/process count;
- threads per process;
- job worker concurrency;
- async execution;
- replicas/roles;
- multiple databases/shards;
- database server connection limits.

Rails currently exposes pool controls including `checkout_timeout`, `max_connections`, `min_connections`, `idle_timeout`, `keepalive`, and `max_age`. The current connection pool API documents a default maximum of 5 connections unless configured otherwise.

Do not increase pool size in isolation. Confirm the database server can support the aggregate number of connections across all application processes/roles.

Pool timeout errors often indicate a capacity mismatch, long-held connections, slow queries, or excessive concurrency rather than simply a pool-size bug.

Use `with_connection`/normal framework-managed checkout semantics instead of leaking checked-out connections.

## Bulk writes
Choose explicitly between:
- callbacks/validations required -> normal model operations;
- pure data mutation -> `update_all`/`insert_all`/`upsert_all` where supported and understood.

Bulk writes bypass portions of the model lifecycle. Test the database state and any downstream side effects separately.

## Multi-database and roles
When Rails uses multiple databases, replicas, or shards, identify:
- writer vs reader role;
- connection pool per role/database;
- transaction connection;
- read-after-write requirements;
- failover behavior.

Do not assume a query on a replica observes a just-committed writer mutation immediately.

## Production migration checklist
```text
data size known
traffic known
old/new app compatibility known
lock impact known
transaction behavior known
rollback/recovery known
backfill plan known
constraint validation known
index strategy known
deployment order known
observability known
```

## References

Load only when needed; the reference is one level deep. Consult a listed pattern only when the change needs its implementation shape.

| Load when | Reference | Covers | Patterns |
|---|---|---|---|
| a change touches `db/seeds.rb`, files it loads, or `bin/rails db:seed` | [references/seed-data.md](references/seed-data.md) | Rerunnable seeds; reference versus sample data; secrets outside seeds; seed verification | none |
| a change sets a transaction isolation level, uses row or advisory locks, or diagnoses a deadlock, lock-wait, or serialization failure | [references/isolation-and-locking.md](references/isolation-and-locking.md) | Isolation levels (`READ COMMITTED` / `REPEATABLE READ` / `SERIALIZABLE`); Row locks (`FOR UPDATE` family); Advisory locks (`pg_advisory_lock`); Optimistic vs pessimistic; Deadlock diagnosis; `SET LOCAL` per-transaction configuration | `isolation-level-contract` |
| a change uses PostgreSQL features that Active Record does not abstract (`LISTEN`/`NOTIFY`, declarative table partitioning, materialized views, GIN/BRIN/partial/expression indexes, `CREATE INDEX CONCURRENTLY`, stored procedures, `EXPLAIN ANALYZE`) | [references/postgres-features.md](references/postgres-features.md) | PostgreSQL advanced features; `LISTEN/NOTIFY`; partitioning; materialized views; index types; concurrent index creation; stored procedures; `scenic` and `pg_partman` integrations | none |

## Reference example

A production-safe migration: concurrent index outside a transaction, plus a check constraint enforcing the invariant the model only suggests.

```ruby
class AddConcurrentIndexAndConstraint < ActiveRecord::Migration[8.0]
  disable_ddl_transaction! # required for algorithm: :concurrently

  def up
    add_index :invoices, :customer_id, algorithm: :concurrently
    add_check_constraint :invoices, "total_cents >= 0", name: "invoices_total_cents_nonnegative"
  end

  def down
    remove_check_constraint :invoices, name: "invoices_total_cents_nonnegative"
    remove_index :invoices, :customer_id, algorithm: :concurrently
  end
end

# Model-level validation gives feedback; the constraint survives concurrent writers:
#   validates :total_cents, numericality: { greater_than_or_equal_to: 0 }
```

## Agent review checklist
- [ ] runtime and database versions resolved
- [ ] schema and existing constraints/indexes inspected
- [ ] migration is compatible with rolling deploys
- [ ] destructive changes are separated from application cutover where needed
- [ ] transaction/DDL behavior is understood
- [ ] index lock/build strategy is justified
- [ ] application validation vs DB constraint boundary is explicit
- [ ] backfill is resumable and bounded
- [ ] locking/isolation semantics are explicit
- [ ] deadlock/retry behavior is safe
- [ ] query plan evidence exists for performance changes
- [ ] connection pool capacity matches concurrency
- [ ] bulk-operation callback/validation semantics are understood
- [ ] multi-database/role behavior is considered
- [ ] focused tests and migration checks exist

## Anti-patterns
- editing already-applied production migrations
- adding a large-table index without lock analysis
- running long backfills in one transaction by default
- loading all rows into Ruby memory for a migration
- relying only on model validation for concurrency-critical invariants
- increasing connection pool size without aggregate capacity analysis
- using row locks without defining the invariant
- broad retry of any transaction/DB exception
- calling external services inside long database transactions
- assuming replicas are immediately consistent
- using `update_all` while depending on callbacks/validations
- running `EXPLAIN ANALYZE` against production casually

## Source foundation

Primary Rails references:
- https://guides.rubyonrails.org/active_record_migrations.html
- https://api.rubyonrails.org/classes/ActiveRecord/Transactions/ClassMethods.html
- https://api.rubyonrails.org/classes/ActiveRecord/Locking/Pessimistic.html
- https://api.rubyonrails.org/classes/ActiveRecord/ConnectionAdapters/ConnectionPool.html
- https://api.rubyonrails.org/classes/ActiveRecord/Relation.html

Primary PostgreSQL reference:
- https://www.postgresql.org/docs/current/sql-createindex.html

Use the installed Rails, adapter, and database versions as the compatibility authority for version-sensitive migration and locking behavior.

## Verification
Migration/database changes require both code-level and database-level verification appropriate to the contract: migration syntax/status, schema diff, constraint/index presence, targeted model/query tests, transaction/locking tests where relevant, and production rollout/recovery evidence for operational migrations.

## Rails database/schema changes

For database changes:
- resolve Rails, adapter, and database versions first;
- inspect schema, existing indexes/constraints, data volume, and deployment order;
- treat migrations as rolling-deployment contracts;
- separate expand/backfill/cutover/contract when compatibility requires it;
- preserve database invariants with constraints where the database is the authoritative writer boundary;
- use bounded/idempotent backfills;
- make transaction, locking, isolation, and deadlock semantics explicit;
- size connection pools against aggregate application concurrency and database limits;
- require query-plan evidence for query/index performance claims;
- test migration and database behavior at the owning boundary.
