---
name: managed-database-selection
description: "The most expensive database mistakes are made before a single row is written, by"
---

# Managed Database Selection (Verbose)

## Core Patterns

### The Access Pattern Comes First

The most expensive database mistakes are made before a single row is written, by
choosing the engine from familiarity or hype and then discovering the data does
not fit. Invert it. Write down the access pattern first:

- Read/write ratio, and whether either is bursty
- Query shapes: point lookup by key, range scan, join across entities, aggregate
- Item/row size and total data volume
- Cardinality and how the working set grows
- Consistency requirement: read-after-write? cross-region? eventual acceptable?
- Latency budget and throughput ceiling

Only now does the choice become mechanical. The access pattern selects the *family*;
the specific managed engine is a follow-on decision about operations and cost.

### Matching Pattern to Family

| Family | Access pattern it serves | Costs / constraints | Managed examples |
|---|---|---|---|
| Relational | Joins, multi-row transactions, ad-hoc and evolving queries, referential integrity | Vertical scaling first; sharding is manual effort | RDS, Aurora, Cloud SQL, AlloyDB, Azure SQL |
| Document | Self-contained aggregates of variable shape, read/written whole | Cross-document joins are weak; easy to denormalize into anomalies | DocumentDB, MongoDB Atlas, Firestore, Cosmos DB |
| Key-value | Point lookups by known key, extreme throughput, simple values | No secondary query without extra indexes; partition key is the design | DynamoDB, Bigtable, Memorystore, Cosmos DB |
| Wide-column | Massive write volume, queries always by partition key, time-bucketed rows | Query flexibility is near zero off the key; tombstone/compaction care | Cassandra, Keyspaces, Bigtable, Scylla |
| Time-series | Append-only events/metrics, time-range queries, downsampling and retention | Not for mutable relational data; late-arriving data needs handling | Timestream, TimescaleDB, InfluxDB |

**nosql-database-selection** goes deeper on the non-relational branch; this skill
is about picking among *managed* offerings once the family is known.

### Relational as the Default

Relational databases earn their default status through a specific property: they
let you defer query design. Normalize the entities and the engine will answer
queries you did not anticipate, because the query planner composes joins and
indexes at read time. Non-relational stores trade this away. In a key-value or
wide-column store the partition key *is* the schema — you must know the queries
before you model, and a new access pattern often means a new table or a full
migration.

So the rule is: start relational, and move off it only when a concrete pattern
forces the move — write volume beyond what one primary sustains, data too large to
fit the vertical-scaling ceiling, a shape (documents, wide time-bucketed rows)
that relational serves awkwardly, or a latency/throughput target a single primary
cannot hit. "We might need to scale someday" is not that force.

### Operational Model Within a Family

Choosing relational does not end the decision — the operational shape still varies:

```
Instance-based (RDS, Cloud SQL)
  you choose instance class; storage attached; you plan capacity
  predictable cost, hands-on scaling, well understood

Cloud-native distributed (Aurora, AlloyDB, Spanner)
  storage decoupled from compute; read replicas scale reads cheaply
  higher price floor; some (Spanner) add horizontal write scale + global consistency

Serverless (Aurora Serverless, DynamoDB on-demand)
  capacity tracks load automatically
  ideal for spiky/unpredictable or dev workloads; watch cost under sustained load
```

Match the model to the traffic *curve*, not the peak. A steady, predictable
workload is cheapest on a right-sized instance. A spiky or unpredictable one wastes
money on a provisioned peak and belongs on serverless or on-demand capacity.

### Replication, HA, and DR Are Three Different Things

These get conflated, and the conflation causes data-loss incidents.

| Mechanism | Purpose | What it is NOT |
|---|---|---|
| Read replica | Offload read traffic; may lag | Not a backup; not automatic failover |
| Multi-AZ standby | Automatic failover for HA | Not a read scaler (often can't be read) |
| Cross-region replica | Disaster recovery; read locality | Not synchronous; expect lag and possible loss |
| Snapshot / PITR | Backup and point-in-time restore | Not high availability |

Two failure modes follow directly. First, treating a read replica as a backup: a
bad `DELETE` replicates to it just as fast as to the primary. Second, reading your
own write from an async replica and getting a stale result — because replication
lag is real and unbounded under load. If a flow needs read-after-write, route it to
the primary or use a session-consistency guarantee, do not assume the replica has
caught up.

### Consistency and Locality Set the Ceiling

Consistency is the axis that most narrows the field, so decide it explicitly.

- **Strong, single-region** — any relational primary gives this within a region.
- **Strong, global** — a small club (Spanner-class systems using synchronized
  clocks / consensus). You pay for it in write latency, because a write must reach
  a quorum across regions before it commits.
- **Eventual** — opens the widest, cheapest set of options, and is correct for
  plenty of workloads (feeds, catalogs, analytics) that do not need to read the
  latest write immediately.

Locality interacts with this: putting data close to users lowers read latency but,
if you also want strong global consistency, raises write latency. You rarely get
low-latency writes *and* strong global consistency *and* multi-region — pick two,
knowingly. See **cloud-provider-tradeoffs** for how each provider's flagship
offering resolves this, and **distributed-caching-design** for absorbing read load
without changing the database's consistency model.

## Common Anti-Patterns

❌ **Choosing the engine before writing down the access pattern.** The data ends up
fighting the store.
✅ Document read/write ratio, query shapes, and consistency needs first; let them
select the family.

❌ **Reaching for a NoSQL store "to scale" and then running relational queries on
it** — ad-hoc filters, joins, aggregates it cannot serve without full scans.
✅ Use a non-relational store only when the access pattern is genuinely key/partition
oriented; otherwise stay relational.

❌ **Forcing relational data into key-value** and hand-rolling transactions and
integrity the engine used to provide.
✅ Keep transactional, relationship-heavy data in a relational engine.

❌ **Treating a read replica as a backup or as failover.** It faithfully replicates
your mistakes and does not promote itself.
✅ Separate read replicas, multi-AZ standby, cross-region DR, and snapshots — provision
each for its own job.

❌ **Reading your own write from an async replica** and being surprised by staleness.
✅ Route read-after-write to the primary, or use an explicit consistency guarantee.

❌ **Provisioning for peak on a spiky workload.** You pay for idle capacity all day.
✅ Use serverless/on-demand for spiky traffic; reserve right-sized instances for steady load.

❌ **Assuming strong global consistency is free.** It costs cross-region write latency
and a narrow engine choice.
✅ Decide the consistency requirement up front and accept its latency and cost.

## Database Selection Checklist

- [ ] Access pattern written down before any engine is named
- [ ] Data-model family chosen from the pattern (relational / document / key-value / wide-column / time-series)
- [ ] Relational used unless a concrete pattern forces otherwise
- [ ] Operational model (instance / distributed / serverless) matched to the traffic curve
- [ ] Consistency requirement (strong single-region / strong global / eventual) stated explicitly
- [ ] Read replicas, multi-AZ HA, cross-region DR, and backups each provisioned for their own purpose
- [ ] Read-after-write paths routed to the primary or given a consistency guarantee
- [ ] Backup and point-in-time-restore configured and test-restored
- [ ] Cost modeled against the traffic curve, not the peak
- [ ] Cross-reference: nosql-database-selection, distributed-caching-design, cloud-provider-tradeoffs
