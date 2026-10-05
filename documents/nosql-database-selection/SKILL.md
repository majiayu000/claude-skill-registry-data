---
name: nosql-database-selection
description: "Relational modelling lets you defer query design: normalize the entities, and"
---

# NoSQL Database Selection (Verbose)

## Core Patterns

### Access-Pattern-First Selection

Relational modelling lets you defer query design: normalize the entities, and
the optimizer will find a plan for whatever you ask later. Non-relational stores
remove that safety net. There is no join and often no ad-hoc filter, so the
physical layout *is* the query plan. Design it from the queries or you will
discover, in production, that a required read is impossible without a full scan.

The method, in order:

**1. Enumerate every access pattern.** Reads and writes, with shape, rate, and
latency budget. Be exhaustive; the one you forget is the one that breaks the
design.

| # | Pattern | Shape | Rate | Budget | Consistency |
|---|---|---|---|---|---|
| 1 | Get order by id | Point read | 4k/s | p99 < 10 ms | Strong |
| 2 | Customer's orders, newest first, paged | Range on sorted key | 800/s | p99 < 30 ms | Eventual ok |
| 3 | Orders in state SHIPPED older than 2 days | Filtered index scan | 1/min | seconds | Eventual ok |
| 4 | Decrement stock on checkout | Conditional write | 300/s | p99 < 20 ms | Strong |
| 5 | Revenue by region by month | Aggregation | 20/day | seconds | Stale ok |
| 6 | Full-text search on product name | Inverted index | 200/s | p99 < 100 ms | Eventual ok |

**2. Split by workload class.** Patterns 5 and 6 are not OLTP. Aggregation
belongs in a warehouse or a column store (see `dimensional-modeling`); full-text
belongs in a search engine fed by change data capture. Forcing them into the
operational store is the most common cause of "our NoSQL database is slow".

**3. Identify the constraints that eliminate candidates.** Pattern 4 needs a
conditional write with a real guarantee — a store with last-write-wins eventual
consistency will oversell inventory. Pattern 1's 10 ms p99 at 4k/s rules out
anything needing a cross-region quorum on the read path.

**4. Only now name products**, and evaluate each against the surviving list.

If you are starting from an existing relational schema or an unclear domain, run
`data-model-discovery` first — you cannot enumerate access patterns for a domain
you have not mapped.

### Store Families and Their Query Shapes

| Family | Data model | Excels at | Fails at | Typical |
|---|---|---|---|---|
| Key-value | Opaque value by key | Point get/put, sub-ms, cache and session | Anything not keyed; range scans; secondary access | Redis, Memcached, DynamoDB (KV mode) |
| Document | JSON-ish nested docs | Fetching a whole aggregate in one read; heterogeneous fields; per-field secondary indexes | Cross-document joins; large multi-doc transactions; deep aggregation | MongoDB, Couchbase, Firestore |
| Wide-column | Partition key + clustering key → columns | Massive write rates; point and range reads on a designed key; predictable latency at scale | Ad-hoc queries; joins; anything not anticipated in the key | Cassandra, ScyllaDB, HBase, DynamoDB |
| Graph | Nodes and edges with properties | Variable-depth traversal, path finding, recommendation over relationships | Bulk scans; aggregation over all nodes; high-volume simple writes | Neo4j, Neptune, JanusGraph |
| Time-series | Timestamped points per series | Append-heavy ingest; time-range rollups; downsampling and retention | Updates and deletes of individual points; joins; referential integrity | TimescaleDB, InfluxDB, Prometheus |
| Search | Inverted index | Full-text relevance, faceting, fuzzy matching | Being a system of record; transactional writes | Elasticsearch, OpenSearch |

Two heuristics do most of the work:

- **Start from what a store cannot do.** Elimination is faster than comparison
  and far less susceptible to marketing.
- **A graph database earns its place at three-plus hops of variable depth.** One
  or two fixed hops is a join, and a relational database does joins well. "Our
  data is connected" describes every dataset ever.

### Modelling the Queries: DynamoDB Single-Table Design

In a wide-column store you cannot join at read time, so you pre-join at write
time: items that are read together are stored together, under a shared partition
key, ordered by a sort key you design.

Take patterns 1, 2 and 3 above.

```
PK                 SK                       GSI1PK          GSI1SK        attrs
CUSTOMER#42        PROFILE                  -               -             name, email, tier
CUSTOMER#42        ORDER#2026-03-01#9912    STATUS#SHIPPED  2026-03-01    total, status
CUSTOMER#42        ORDER#2026-02-17#9744    STATUS#DELIVERED 2026-02-17   total, status
ORDER#9912         META                     -               -             total, addr, status
ORDER#9912         ITEM#001                 -               -             sku, qty, price
ORDER#9912         ITEM#002                 -               -             sku, qty, price
```

- **Pattern 1** — `GetItem(PK=ORDER#9912, SK=META)`, or `Query(PK=ORDER#9912)`
  to get the order and all its line items in one round trip. That is the join,
  performed at write time.
- **Pattern 2** — `Query(PK=CUSTOMER#42, SK begins_with "ORDER#",
  ScanIndexForward=false, Limit=20)`. Newest first, paged, one request. The date
  sits in the sort key *before* the id precisely so lexical order equals
  chronological order.
- **Pattern 3** — `Query(GSI1, GSI1PK=STATUS#SHIPPED, GSI1SK < 2026-03-18)`.
  A secondary index is a second physical layout of the same items, maintained
  for you, to serve an access pattern the main key cannot.

What this makes explicit:

1. **The key encodes the query.** `ORDER#<date>#<id>` is chosen because you must
   list a customer's orders in date order. Sort by total instead and the key
   changes. This is why the design must follow the patterns.
2. **Entity type lives in the key prefix**, not in a separate table. One physical
   table, many logical entities, distinguished by `PK`/`SK` prefixes.
3. **Duplication is the point.** Order status appears on both the customer-scoped
   item and the order item. You are trading write cost and consistency work for
   read cost, deliberately.

And what it costs:

- **New access patterns can require a migration.** If someone later needs orders
  by warehouse, you add a GSI or backfill. A normalized relational schema would
  have absorbed that with a `WHERE` clause.
- **It is hard to read.** Onboarding onto a single-table design is materially
  slower than onto a normalized schema, and the model lives in code and docs
  rather than in the schema itself.
- **It presumes stability.** Adopt it when access patterns are known and settled
  — a mature, high-scale service. For a product still discovering its domain,
  the rigidity costs more than the read efficiency saves.

**Partition key selection is the load-bearing decision.** The key must spread
traffic. `PK = CUSTOMER#<id>` is fine when no customer dominates; `PK = TENANT#<id>`
in a system where one tenant is 60% of traffic creates a hot partition that no
amount of provisioned capacity fixes, because a single partition has a hard
throughput ceiling. Mitigations: add a suffix shard (`TENANT#7#3` across N
shards, scatter-gather on read), or key by a finer-grained entity. Equally,
partitions must be bounded — a key like `ORDERS#ALL` grows without limit and
eventually cannot be queried usefully.

### "We Need NoSQL for Scale" Is Usually Wrong

For OLTP workloads below a few terabytes, a single well-tuned relational primary
on modern hardware handles tens of thousands of transactions per second, with
read replicas for read-heavy fan-out. Meanwhile you keep:

- Joins, so you are not writing them in application code
- Multi-row ACID transactions, so invariants hold without compensating logic
- Foreign keys, uniqueness, and check constraints enforced by the engine
- Ad-hoc query capability for the questions nobody anticipated
- Decades of tooling for backup, replication, migration, and query analysis

Nearly every "we outgrew Postgres" story that turns out to be true involves
either write throughput past what one primary can absorb, or a working set far
larger than one machine's memory. Most that turn out to be false involve a
missing index, an N+1 query, or analytics running on the OLTP primary — none of
which a different database fixes. See `sql-optimization` before migrating.

Real reasons to leave relational:

| Reason | Signal | Where to go |
|---|---|---|
| Write throughput beyond one primary | Sustained writes saturating the primary after tuning and batching | Wide-column |
| Multi-region active-active writes | Users on two continents both writing, low latency required | Wide-column with tunable consistency |
| Genuinely variable documents | Attributes differ per record and cannot be usefully normalized | Document |
| Extreme point-read latency | Sub-millisecond p99 by key at very high rate | Key-value |
| Time-series volume | Millions of points/s, append-only, retention and rollup | Time-series |
| Deep traversal | Variable-depth path queries over a large graph | Graph |
| Operational preference | Small team, no DBA, wants a managed store with no capacity planning | Managed KV/document |

That last one is legitimate and under-discussed: choosing DynamoDB because
nobody wants to run a database is a defensible decision, provided you know you
are paying for it in modelling rigidity.

Also worth noting: modern Postgres covers several of these adjacently — `JSONB`
for semi-structured documents, TimescaleDB for time-series, `pgvector` for
embeddings, `tsvector` for modest full-text. One database you operate well often
beats three you operate poorly.

### Consistency Models

| Model | Guarantee | Cost | Breaks |
|---|---|---|---|
| Linearizable / strong | Every read sees the latest committed write, globally ordered | Highest latency; requires quorum; unavailable during partitions | Availability under partition (the CAP trade) |
| Sequential | All nodes see operations in the same order, not necessarily real-time | Moderate | Real-time recency |
| Causal | Causally related operations are seen in order everywhere | Modest; needs version tracking | Concurrent unrelated writes still conflict |
| Read-your-writes | A client sees its own writes | Session pinning or a token | Other clients may still see stale data |
| Eventual | Replicas converge given no new writes | Lowest latency, highest availability | Ordering, recency, and read-your-writes |

Concretely, what eventual consistency breaks:

- **Read-your-writes.** User edits a profile, the write goes to region A, the
  reload reads region B, and the old value appears. Users read this as a bug and
  they are right to. Fix by pinning a session to a replica or by reading
  strongly for a short window after a write.
- **Counters and balances.** Read-modify-write on an eventually consistent value
  loses updates under concurrency. Use an atomic increment or a conditional
  write with a version, never read-then-write.
- **Inventory and uniqueness.** "Check then reserve" oversells under
  concurrency. This needs a conditional write with a real guarantee, or a
  reservation record with a uniqueness constraint.
- **Cross-entity invariants.** "A customer may have at most one active
  subscription" cannot be enforced across items in an eventually consistent
  store without additional machinery — a single item holding the invariant, or a
  transaction that spans them.

Most stores let you choose per operation. Use strong reads on the few paths that
need them (balance, inventory, auth) and eventual elsewhere; strong reads cost
more in latency and often in price, so paying for them everywhere is waste, and
paying for them nowhere is a correctness bug.

### Polyglot Persistence — And Its Bill

Different patterns genuinely suit different stores: Postgres as the system of
record, Redis for sessions, Elasticsearch for search, a time-series store for
metrics. Each addition brings a real cost: another failure mode, another backup
and restore procedure, another upgrade path, another thing on-call must
understand at 3am, and — hardest — synchronisation between stores, which is a
distributed systems problem in its own right.

The workable pattern is one system of record plus derived stores fed by change
data capture or an outbox, where every derived store can be rebuilt from the
record. If two stores are both authoritative for overlapping data, you have
signed up for reconciling them forever.

## Common Anti-Patterns

❌ **Choosing the store before writing the access patterns.** The design is then
fitted to the product rather than the problem, and the missing pattern surfaces
in production.
✅ Enumerate patterns with shape, rate, and latency budget first; let them
eliminate candidates.

❌ **"We need NoSQL for scale"** with no measured throughput, data size, or
profile of the slow queries.
✅ Measure first. Below a few TB of OLTP, tune the relational database — an
index usually beats a migration.

❌ **Using a document store as a relational database.** Application code fetches
documents in a loop and joins them in memory; ten reads where one join belonged.
✅ Either embed the aggregate so one read serves the query, or use a database
with joins.

❌ **Modelling entities instead of queries in a wide-column store.** One item
type per table, then a scan for every read.
✅ Design the partition and sort keys from the queries; duplicate data to serve
reads.

❌ **Single-table design on a domain still in flux.** Access patterns change
weekly; every change is a migration.
✅ Adopt it when patterns are stable and read efficiency matters. Until then,
prefer a model you can re-query cheaply.

❌ **A partition key with heavy skew.** One tenant, or one popular entity, takes
most of the traffic and throttles regardless of provisioned capacity.
✅ Choose a high-cardinality key, or shard the hot key with a suffix and
scatter-gather.

❌ **Unbounded partitions.** All events under `EVENTS#ALL`, growing forever.
✅ Bound partitions by time or tenant so each stays queryable.

❌ **Analytics against the operational store.** Aggregation queries scan the
table and starve the latency-critical path.
✅ Stream to a warehouse or column store; model it dimensionally.

❌ **Eventual consistency on a correctness-critical path** — balances, stock,
entitlements — with read-then-write update logic.
✅ Atomic or conditional writes, and strong reads where invariants depend on it.

❌ **A graph database for one-hop relationships.** Foreign keys and a join
already do this, faster and with better tooling.
✅ Reserve graph stores for variable-depth traversal.

❌ **Polyglot persistence adopted store-by-store with no ownership plan.** Six
databases, one on-call engineer, no rebuild path.
✅ One system of record; derived stores rebuildable from it via CDC or an outbox.

❌ **Believing schemaless means no schema.** The schema moves into application
code, undeclared, and every reader implements a different version of it.
✅ Enforce a schema at the boundary — validation, versioned documents, a
migration strategy for old shapes.

## NoSQL Selection Checklist

- [ ] Every access pattern written down with shape, rate, and latency budget
- [ ] Consistency requirement stated per pattern, not globally
- [ ] Analytical and full-text patterns routed away from the operational store
- [ ] Current data size and write rate measured, not estimated
- [ ] Relational option evaluated honestly, including tuning and indexing
- [ ] Candidates eliminated by what they cannot do before comparing what they can
- [ ] Partition key chosen for even distribution; skew analysed against real data
- [ ] Partitions bounded in growth
- [ ] Sort key encodes the ordering the read patterns actually need
- [ ] Secondary indexes justified by a named access pattern, and their cost known
- [ ] Duplication and its write-time synchronisation cost accounted for
- [ ] Correctness-critical paths use atomic or conditional writes, not read-then-write
- [ ] Read-your-writes handled for anything a user edits and immediately views
- [ ] Cross-entity invariants have an enforcement mechanism
- [ ] Hot-key and throttling behaviour tested under realistic skew
- [ ] Migration path and exit cost understood before committing
- [ ] Derived stores rebuildable from a single system of record
- [ ] Schema validation enforced somewhere explicit, even if the store is schemaless
- [ ] Backup, restore, and point-in-time recovery tested, not assumed
