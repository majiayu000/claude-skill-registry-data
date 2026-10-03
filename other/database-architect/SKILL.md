---
name: database-architect
description: Expert database architecture and design guidance — schema/data modeling, ER diagrams, indexing, query optimization, partitioning, replication and high availability, transactions and locking, connection pooling, migrations, and multi-tenancy patterns across PostgreSQL, MySQL, MongoDB, and Redis. Use this whenever the user asks about designing a schema, a slow or N+1 query, choosing between SQL and NoSQL, sharding, read replicas, a database migration, or says something like "why is this query slow" or "how should I structure this table" — even without the word "database" in the request.
---

# Database Architecture

Approach every database task as the engineer who has debugged a production outage caused by a missing index at 2am, and a data-loss incident caused by a migration with no rollback plan. The database is the most durable part of the system — it outlives every framework, every language, and every application rewrite. Design it with that lifespan in mind, not the lifespan of this sprint.

---

## Step 0: Understand the Data Before Touching the Schema

Before designing any schema or query, answer:

1. **What are the read patterns?** What queries run most frequently, and what does a typical one look like?
2. **What are the write patterns?** Insert-heavy? Update-heavy? Append-only? Bulk loads?
3. **What's the read/write ratio?** 80/20 read-heavy changes storage and indexing decisions completely from 20/80 write-heavy.
4. **What are the consistency requirements?** Can the system tolerate stale reads? Does any path need serializable transactions?
5. **What's the expected data volume and growth rate?** A schema that's fine at 1M rows can fall over at 1B — but over-engineering for scale you'll never hit wastes real effort too.

Design for the actual access patterns, not the entity relationships in isolation — a textbook-perfect 3NF schema that requires five joins for the one query that runs 10,000 times a second is not a well-designed schema.

---

## Choosing the Right Database

| Use Case | Database | Why |
|---|---|---|
| Relational data with ACID transactions | PostgreSQL | Best-in-class open-source RDBMS; rich feature set (JSONB, window functions, extensions); strong community |
| Simple relational, read-heavy, broad ecosystem | MySQL | Widely supported; performant for read-heavy workloads |
| Document store, flexible schema, horizontal scale | MongoDB | Good for hierarchical, variable-structure data; native sharding |
| Cache, session store, rate limiting, pub/sub | Redis | In-memory; sub-millisecond latency; rich data structures |
| Full-text search | Elasticsearch | Inverted index; powerful query DSL; aggregations |
| Time-series data | TimescaleDB / InfluxDB | Optimized for time-ordered inserts and range queries |
| Graph relationships | Neo4j / Amazon Neptune | When relationship traversal is the primary access pattern, not a rare join |

**Don't pick a database because it's fashionable.** Pick it because its access patterns, consistency model, and operational characteristics match the requirements from Step 0. A surprising amount of "we need MongoDB for scale" turns out to be solvable with a well-indexed Postgres table and a read replica.

---

## Relational Data Modeling

**Core principles:**
- Start with third normal form (3NF) — eliminate redundancy, enforce referential integrity by default
- Denormalize deliberately, not accidentally — only after a join is *provably* too expensive for the access pattern, and document why so the next engineer doesn't "fix" it back to normalized
- Every table has a primary key — surrogate keys (UUID or auto-increment integer) for application-level identity; natural keys for uniqueness constraints only
- Foreign keys enforce referential integrity at the database level — application-code-only enforcement fails the moment there's a second write path (a script, an admin tool, a different service)
- Nullable columns are a design decision, not a default — null means "unknown," not "empty"; be deliberate about which
- `created_at` / `updated_at` on every table — non-negotiable; you will need them for debugging, auditing, or a migration you haven't thought of yet

**Naming conventions:**
- Tables: singular noun, snake_case (`user`, `order_item`, `payment_method`)
- Columns: snake_case, descriptive (`user_id`, `created_at`, `is_active`)
- Foreign keys: `{referenced_table}_id` (`user_id`, `order_id`)
- Junction tables: `{table_a}_{table_b}` (`user_role`, `order_product`)
- Indexes: `idx_{table}_{columns}` (`idx_user_email`, `idx_order_created_at`)

---

## ER Diagram Approach

1. **Identify entities** — the nouns in the domain: User, Order, Product, Payment
2. **Identify relationships** — one-to-one, one-to-many, many-to-many
3. **Identify attributes** — what data lives on the entity vs. what's derived (never store what you can compute, unless you've measured that computing it is the bottleneck)
4. **Identify cardinality** — a User has many Orders; an Order belongs to one User
5. **Identify invariants** — business rules the schema must enforce: an Order must have at least one item; a Payment must reference a valid Order

Many-to-many relationships resolve to a junction table with its own primary key and any relationship-specific attributes (e.g., `quantity` on `order_product`).

---

## Indexing Strategy

The single highest-leverage performance tool, and the most commonly misapplied.

**Index by default:**
- Every primary key (automatic)
- Every foreign key column — unindexed foreign keys cause full table scans on joins, which is one of the most common causes of "this got slow as the table grew" reports
- Every column used in a frequent `WHERE`, `ORDER BY`, or `GROUP BY`
- Every column with a uniqueness constraint

**Composite indexes:**
- Column order matters — the leftmost-prefix rule applies; order by selectivity and actual query shape
- `(user_id, created_at)` serves queries filtering on `user_id` alone or `user_id + created_at`; it does *not* serve a query filtering on `created_at` alone
- Verify with `EXPLAIN` / `EXPLAIN ANALYZE` that the planner is actually using the index you added — an unused index is pure write-cost with zero read benefit

**Index costs — the part people forget:**
- Every index slows every write on that table, since inserts/updates/deletes must maintain it
- Over-indexed tables suffer write amplification; audit periodically (`pg_stat_user_indexes` in Postgres) and drop indexes with zero scans
- Partial indexes shrink index size for sparse conditions: `CREATE INDEX ON orders (status) WHERE status = 'pending'`
- Covering indexes include every column the query needs, eliminating the heap fetch entirely

**Rule:** add indexes for queries you actually run against production-scale data; remove ones the query planner never touches.

---

## Query Optimization

When a query is slow:

1. **`EXPLAIN ANALYZE`** — the actual execution plan, not the estimate
2. **Sequential scans on large tables** — usually means a missing or unused index
3. **Nested loop joins on large result sets** — often a missing index on the join column, or a query returning far more rows than it needs to
4. **Estimated vs. actual row counts** — a big gap means stale statistics; run `ANALYZE`
5. **N+1 queries** — loading a list, then querying each item individually in a loop; fix with a join or a single `IN` query. This is the single most common performance bug in application code that talks to a database, and it's invisible in local dev with 10 rows and catastrophic in prod with 10,000.
6. **`LIMIT` early** — filter and paginate before joining where the query plan allows it
7. **Avoid `SELECT *`** — pulling columns you don't need costs transfer bandwidth and blocks the planner from using a covering index

**Pagination:**
- Offset pagination degrades with depth — `OFFSET 10000` still scans and discards 10,000 rows before returning anything
- Cursor-based pagination (`WHERE id > :cursor ORDER BY id LIMIT 20`) is O(1) regardless of page depth — use it for any dataset that will grow past a few thousand rows

---

## Transactions, Isolation, and Locking

Transactions aren't just "wrap it in BEGIN/COMMIT" — the isolation level decides what bugs are possible.

| Isolation Level | Prevents | Allows | Use when |
|---|---|---|---|
| Read Committed (Postgres default) | Dirty reads | Non-repeatable reads, phantom reads | Most application code; fine for single-row operations |
| Repeatable Read | + Non-repeatable reads | Phantom reads (mostly, engine-dependent) | Reports/analytics needing a consistent snapshot mid-transaction |
| Serializable | Everything | Nothing — behaves as if transactions ran one at a time | Financial operations, inventory decrements, anything where a race condition means real money or data loss |

**Practical rules:**
- Keep transactions short — a long-running transaction holds locks and blocks other writers; never do a network call or external API request inside an open transaction
- Watch for deadlocks in code that touches multiple tables — always acquire locks in the same order across every code path that touches those tables, or the database will eventually deadlock two concurrent requests against each other
- `SELECT ... FOR UPDATE` for pessimistic locking (safe under contention, costs throughput); optimistic locking via a `version` column for low-contention cases (cheaper, requires retry logic on conflict)

---

## Replication & High Availability

- **Primary-replica replication** — writes go to the primary, reads can be distributed to replicas. This buys read scalability, but replicas lag: a write followed immediately by a read from a replica can return stale data ("read-your-own-writes" bugs). Route anything that must see its own just-written data back to the primary, or use synchronous replication for that path.
- **Failover** — know your RTO/RPO before choosing sync vs. async replication. Async is faster and cheaper but can lose the last few transactions on primary failure; sync is safer but adds write latency.
- **Sharding** — only when a single primary can no longer hold the write volume or dataset size, not preemptively. Pick a shard key that matches the dominant access pattern (e.g., `tenant_id`) — a bad shard key just relocates the hot-spot problem instead of solving it.

---

## Partitioning

Partition when a single table is too large to maintain efficiently — not before; partitioning adds real operational complexity.

- **Range partitioning** — by date or sequential ID; most common for time-series/audit data; old partitions can be detached and archived cheaply
- **List partitioning** — by categorical value (region, status); useful when queries always filter on the partition key
- **Hash partitioning** — even distribution across partitions; useful for write distribution when there's no natural range key

Partitioning doesn't replace indexing — you still index within partitions. It helps with query pruning (skip irrelevant partitions), bulk deletes (detach + drop a partition instead of a slow `DELETE`), and maintenance (vacuum partitions independently).

---

## Connection Pooling

Every database connection has real memory and CPU cost on the server side — opening a new connection per request exhausts the connection limit long before it exhausts application throughput.

- Use a pooler: PgBouncer (Postgres), ProxySQL (MySQL), or the driver/ORM's built-in pool
- Size the pool to the database's actual connection limit divided across app instances, not to "however many the app wants" — an unbounded pool from every app replica is a classic way to take down the database during a traffic spike
- Transaction-mode pooling (PgBouncer) is more efficient but breaks session-level features (prepared statements, advisory locks, `SET` session variables) — know which mode you're in before relying on those

---

## MongoDB Data Modeling

Flexible schema is a feature, not permission to be careless.

- **Embed** when nested data is always accessed with the parent and doesn't grow unboundedly (an address inside a user document)
- **Reference** when nested data is large, grows unboundedly, or is queried independently (orders referencing products)
- Avoid deeply nested documents — updates to nested arrays get expensive and indexing gets harder the deeper you go
- Same indexing principles as relational — every query field needs an index, and the leftmost-prefix rule still applies to compound indexes
- Use MongoDB's JSON Schema validation to enforce structure at the database level rather than trusting the application layer alone

---

## Redis Usage Patterns

Redis is a data structure server, not just a cache — use the structure that fits:

| Pattern | Data Structure | Example |
|---|---|---|
| Cache | String (with TTL) | Session data, rendered HTML fragments |
| Rate limiting | String (INCR + EXPIRE) | API calls per user per minute |
| Leaderboard | Sorted Set | Top users by score |
| Pub/Sub messaging | Pub/Sub | Real-time notifications |
| Job queue | List (LPUSH/BRPOP) | Background task dispatch |
| Distributed lock | String (SET NX PX) | Prevent duplicate job execution |
| Feature flags | Hash | Per-user feature toggles |

**Never use Redis as a primary database** unless persistence (RDB snapshots or AOF) is explicitly configured and tested — by default, a restart loses everything in memory.

**Cache invalidation:** decide the strategy up front — TTL expiry (simple, tolerates staleness), write-through (cache updated on every write, always fresh, more write cost), or explicit invalidation on write (fresh, but a missed invalidation path is a hard-to-find bug). "Cache invalidation is one of the two hard problems" is a cliché because it's true — pick deliberately, don't default into it.

---

## Multi-Tenancy Patterns

If the user is building a SaaS product, this decision shapes everything downstream:

| Pattern | Isolation | Cost | Use when |
|---|---|---|---|
| Shared schema, `tenant_id` column | Lowest — relies on every query filtering correctly | Cheapest to operate | Many small tenants, cost-sensitive |
| Schema-per-tenant | Medium | Moderate | Mid-size tenant count, some compliance need for logical separation |
| Database-per-tenant | Highest | Most expensive | Few large tenants, strict compliance/data-residency requirements |

Shared-schema is the most common choice but the riskiest to get wrong — a single missing `WHERE tenant_id = ?` is a cross-tenant data leak. Consider row-level security (Postgres `RLS`) as a database-enforced backstop rather than trusting every query in the codebase to remember the filter.

---

## Migration Strategy

Every schema change is a migration. Every migration must be:

- **Versioned** — sequential, immutable files in source control (Flyway, Liquibase, Alembic, Prisma Migrate, or the framework's built-in tool)
- **Reversible** — a tested `down` script that restores the previous state
- **Tested in CI** — run against a real database before merge, not just eyeballed
- **Safe on live data** — large alterations lock the table; avoid that with:
  - Add nullable columns first (no lock), backfill, then add constraints
  - `CREATE INDEX CONCURRENTLY` in Postgres to avoid locking the table during index creation
  - Batch large backfills — never update millions of rows in one transaction; it holds locks and can bloat the WAL/redo log badly enough to affect replicas

**Zero-downtime column rename** (never do this in one migration against a live system with running app code):
1. Add the new column (nullable)
2. Deploy code that writes to both old and new columns
3. Backfill the new column from the old
4. Deploy code that reads from the new column only
5. Drop the old column

---

## Security

- Least-privilege database users — the application's connection role should not be able to `DROP TABLE`; migrations run under a separate, more-privileged role
- Encrypt at rest and in transit (TLS to the database) — table stakes, not a nice-to-have
- Identify sensitive columns (passwords — hashed, never plaintext; tokens; PII) explicitly and handle them deliberately: encryption at the column level, masking in non-prod environments, and exclusion from casual `SELECT *` debugging queries and logs
- Row-level security (Postgres `RLS`) as a database-enforced tenant/ownership boundary, not just an application-layer check

---

## Bundled Reference

Read [migration-safety.md](./references/migration-safety.md) before planning a production schema or data migration.

## Definition of Done — Database Work

- [ ] Schema reviewed against actual access patterns, not just entity relationships
- [ ] All foreign keys indexed; all frequent query-pattern columns indexed and verified with `EXPLAIN ANALYZE`
- [ ] Transaction isolation level chosen deliberately for anything involving money, inventory, or other race-sensitive state
- [ ] Connection pooling configured and sized to the database's real connection limit
- [ ] Migrations are reversible, tested in CI, and lock-safe for large tables
- [ ] Sensitive columns (passwords, tokens, PII) identified and handled — hashed, encrypted, or excluded from logs as appropriate
- [ ] Replication/failover strategy matches the RTO/RPO the system actually needs
- [ ] Backup and point-in-time recovery tested, not just configured
- [ ] Monitoring on: slow query log, connection count, index hit ratio, replication lag
