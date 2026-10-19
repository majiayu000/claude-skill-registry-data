---
name: mongodb-development
description: >
  Design, model, index, and query production document databases using MongoDB.
  Use when deciding between embedding and referencing relationships (1:1, 1:N, N:N),
  applying the Equality-Sort-Range (ESR) rule to compound indexes, building TTL or partial
  indexes, optimizing aggregation pipelines ($match, $project, $lookup, $group),
  enforcing JSON Schema validation, configuring replica set write and read concerns,
  executing multi-document ACID transactions, or diagnosing query plans with explain().
compatibility: >
  Agent Skills-compatible coding agents designing or querying MongoDB 6.0+ or Atlas databases. Tooling is required only for executable validation.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "mongodb, nosql, document-database, indexing, esr-rule, aggregation, acid-transactions"
  topics: "databases"
---

# MongoDB Document Database Engineering

MongoDB is a document-oriented database that stores records as flexible, binary JSON (BSON) structures. Designing performant, resilient MongoDB systems requires choosing appropriate document relationships (embedding vs referencing), engineering compound indexes under the Equality-Sort-Range (ESR) rule, optimizing multi-stage aggregation pipelines, and configuring cluster write/read concerns for data safety.

## Purpose & Overview

This skill guides the schema design, query optimization, and transaction management of MongoDB databases. It covers document modeling trade-offs (bounded embedding vs referencing for 1:N and N:N relations), compound index creation following the ESR rule, TTL and partial indexes, aggregation pipeline execution plans, JSON Schema collection validation, replica set write and read concerns (`w: "majority"`), multi-document ACID transactions, and query diagnostics with `explain("executionStats")`.

---

## Core Principles & Rules

1. **Follow the Equality-Sort-Range (ESR) rule for compound indexes**: When querying with equality filters, sorting, and range conditions, always order compound index fields as:
   - First: **Equality** fields (exact match: `{ status: "active" }`)
   - Second: **Sort** fields (ordering: `{ createdAt: -1 }`)
   - Third: **Range** fields (inequality operators: `{ age: { $gte: 21 } }`)
2. **Never embed unbounded arrays (Anti-Pattern: 1-to-Squillions)**: Documents have a hard 16MB BSON size limit. Never embed arrays that can grow indefinitely (e.g., logging events, comments, sensor readings) inside a parent document. Reference the parent ID from child documents instead.
3. **Embed for atomic updates and co-located access**: Embed subdocuments when data is accessed together in 90%+ of queries, updated together atomically, and has a bounded size (e.g., user addresses, order line items).
4. **Always use `explain("executionStats")` to verify index coverage**: Never deploy a query without inspecting execution plans. Verify that `stage` is `IXSCAN` (Index Scan) rather than `COLLSCAN` (Collection Scan), and confirm `totalDocsExamined` is close or equal to `nReturned`.
5. **Use `w: "majority"` write concern for durable writes**: Ensure writes are acknowledged by a majority of replica set voting members before returning to prevent data rollback during primary failover.
6. **Place `$match` and `$project` at the earliest aggregation stages**: Filter out unwanted documents and project only needed fields as early in the pipeline as possible to minimize RAM usage before memory-intensive `$sort` or `$group` stages.
7. **Multi-document transactions must be short-lived**: Multi-document ACID transactions hold locks and pin the WiredTiger cache. Keep transactions under 60 seconds, touch minimal documents, and avoid long external network calls inside a transaction block.

---

## Standard Workflows & Procedures

### Workflow 1: Schema Design & Relationship Selection

1. Identify application query patterns: read-to-write ratio, joined queries, and write atomicity requirements.
2. For **1:1** relations: Embed by default unless fields are rarely queried or large (use subset pattern).
3. For **1:Few (Bounded 1:N)**: Embed as an array of subdocuments (e.g., max 10 shipping addresses).
4. For **1:Many (Unbounded 1:N)**: Reference parent in child documents (`parent_id` foreign key).
5. For **N:N**: Reference two-way or one-way array of IDs, or use a junction collection with metadata.
6. Attach a JSON Schema validator to the collection via `createCollection` or `collMod`.

### Workflow 2: Compound Index Creation with ESR

1. Analyze query shape:
   ```javascript
   db.orders.find({ tenantId: "tenant_1", status: "completed", amount: { $gte: 100 } })
     .sort({ createdAt: -1 })
   ```
2. Break down query components:
   - Equality: `tenantId`, `status`
   - Sort: `createdAt`
   - Range: `amount`
3. Formulate the index conforming strictly to ESR:
   ```javascript
   db.orders.createIndex({
     tenantId: 1,
     status: 1,
     createdAt: -1,
     amount: 1
   })
   ```

### Workflow 3: Diagnosing Slow Queries with `explain()`

1. Run explain with full execution statistics:
   ```javascript
   db.orders.find(query).sort(sort).explain("executionStats")
   ```
2. Evaluate execution metrics:
   - `executionStages.stage`: Must be `IXSCAN` + `FETCH` or pure `IXSCAN` (covered query).
   - `totalDocsExamined`: Should closely match `nReturned`. If `totalDocsExamined >> nReturned`, the index is inefficient.
   - `totalKeysExamined`: Check if excess index keys were evaluated.
   - `executionStages.sortStage`: If `SORT` appears, the sort was done in RAM instead of via index.

---

## Real-World Examples & Patterns

### 1. JSON Schema Collection Validation & ESR Compound Index

```javascript
// 1. Create collection with strict schema validation
db.createCollection("orders", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["tenantId", "customerId", "status", "totalAmount", "items", "createdAt"],
      properties: {
        tenantId: { bsonType: "string" },
        customerId: { bsonType: "string" },
        status: {
          enum: ["PENDING", "PROCESSING", "COMPLETED", "CANCELLED"]
        },
        totalAmount: { bsonType: "number", minimum: 0 },
        items: {
          bsonType: "array",
          minItems: 1,
          items: {
            bsonType: "object",
            required: ["sku", "quantity", "price"],
            properties: {
              sku: { bsonType: "string" },
              quantity: { bsonType: "int", minimum: 1 },
              price: { bsonType: "number", minimum: 0 }
            }
          }
        },
        createdAt: { bsonType: "date" }
      }
    }
  },
  validationAction: "error"
});

// 2. Create compound index applying ESR (Equality, Sort, Range)
// Query: find orders for tenantId with status, ordered by createdAt, filtering totalAmount > X
db.orders.createIndex(
  { tenantId: 1, status: 1, createdAt: -1, totalAmount: 1 },
  { name: "idx_orders_tenant_status_date_amount" }
);

// 3. Create partial unique index (e.g. unique idempotencyKey for pending orders only)
db.orders.createIndex(
  { idempotencyKey: 1 },
  {
    unique: true,
    partialFilterExpression: { idempotencyKey: { $exists: true } }
  }
);

// 4. Create TTL index for transient session tokens (expires 24 hours after createdAt)
db.sessions.createIndex(
  { createdAt: 1 },
  { expireAfterSeconds: 86400 }
);
```

### 2. High-Performance Aggregation Pipeline

Optimized pipeline performing early `$match`, pushing sorting to index, and joining with `$lookup`:

```javascript
db.orders.aggregate([
  // Stage 1: Filter early using index (Equality & Range)
  {
    $match: {
      tenantId: "tenant_99",
      status: "COMPLETED",
      createdAt: {
        $gte: ISODate("2026-01-01T00:00:00Z"),
        $lt: ISODate("2026-02-01T00:00:00Z")
      }
    }
  },
  // Stage 2: Prune unnecessary fields to minimize RAM footprint
  {
    $project: {
      customerId: 1,
      totalAmount: 1,
      createdAt: 1
    }
  },
  // Stage 3: Aggregate totals per customer
  {
    $group: {
      _id: "$customerId",
      totalSpent: { $sum: "$totalAmount" },
      orderCount: { $sum: 1 }
    }
  },
  // Stage 4: Filter aggregated results
  {
    $match: {
      totalSpent: { $gte: 500 }
    }
  },
  // Stage 5: Lookup customer profile using sub-pipeline to avoid full joins
  {
    $lookup: {
      from: "customers",
      let: { custId: "$_id" },
      pipeline: [
        { $match: { $expr: { $eq: ["$customerId", "$$custId"] } } },
        { $project: { name: 1, email: 1, tier: 1 } }
      ],
      as: "customer"
    }
  },
  // Stage 6: Unwind single customer record
  {
    $unwind: "$customer"
  },
  // Stage 7: Sort top spenders (allowDiskUse if > 100MB)
  {
    $sort: { totalSpent: -1 }
  },
  {
    $limit: 20
  }
]);
```

### 3. Multi-Document ACID Transaction with Session (Python / PyMongo)

```python
from pymongo import MongoClient
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern

client = MongoClient("mongodb://mongo1:27017,mongo2:27017/?replicaSet=rs0")

def transfer_credits(client: MongoClient, from_user_id: str, to_user_id: str, amount: float):
    # Enforce majority write concern and read concern for the transaction
    wc_majority = WriteConcern("majority", wtimeout=5000)
    rc_majority = ReadConcern("majority")

    with client.start_session() as session:
        def callback(s):
            users = client.app_db.get_collection(
                "users",
                write_concern=wc_majority,
                read_concern=rc_majority
            )

            # 1. Deduct credits from sender if sufficient balance exists
            sender = users.find_one_and_update(
                {"_id": from_user_id, "balance": {"$gte": amount}},
                {"$inc": {"balance": -amount}},
                session=s
            )
            if not sender:
                raise ValueError("Insufficient balance or sender not found")

            # 2. Add credits to recipient
            recipient = users.find_one_and_update(
                {"_id": to_user_id},
                {"$inc": {"balance": amount}},
                session=s
            )
            if not recipient:
                raise ValueError("Recipient not found")

            # 3. Insert audit log
            client.app_db.audit_logs.insert_one(
                {
                    "from": from_user_id,
                    "to": to_user_id,
                    "amount": amount,
                    "timestamp": datetime.utcnow()
                },
                session=s
            )

        # with_transaction automatically handles transient transaction errors and retries
        session.with_transaction(
            callback,
            read_concern=rc_majority,
            write_concern=wc_majority
        )
```

---

## Common Anti-Patterns & Pitfalls

| Anti-Pattern | Why It Fails | Remediated Practice |
|---|---|---|
| **Unbounded array embedding (1:Squillions)** | Documents grow until hitting the 16MB limit, degrading WiredTiger performance and causing write failures. | Reference parent documents using foreign keys (`parent_id`) in child documents. |
| **Violating the ESR Rule in Compound Indexes** | Placing range fields before sort fields forces in-memory sort stages (`SORT` stage in `explain()`), wasting memory and CPU. | Always order index fields as: Equality, then Sort, then Range. |
| **Omitting Write Concern `majority`** | With default `w: 1`, writes acknowledged by only the primary can be rolled back if the primary crashes before replicating. | Set `w: "majority"` on critical write operations. |
| **Full Collection Scans (`COLLSCAN`)** | Unindexed queries inspect every document in the collection, creating high CPU load and disk I/O bottlenecks. | Verify query coverage with `explain("executionStats")` and add targeted indexes. |
| **Unconstrained `$lookup` in Aggregations** | Unfiltered `$lookup` joins entire collections into memory, causing aggregation stages to exceed the 100MB RAM limit. | Filter early with `$match` and use `$lookup` sub-pipelines with targeted `$project`. |
| **Long-running ACID transactions** | Long transactions pin WiredTiger cache history, causing write stalls and transaction aborts (`NoSuchTransaction`). | Keep transactions under 5 seconds, touching only minimal documents. |

---

## Verification Checklist

- [ ] All compound indexes strictly respect the Equality-Sort-Range (ESR) rule.
- [ ] No collections store unbounded arrays inside documents.
- [ ] Collections enforce schema structure and types using `$jsonSchema`.
- [ ] Every slow or critical query has been analyzed with `explain("executionStats")`.
- [ ] `totalDocsExamined` equals `nReturned` on key query paths (minimal over-fetching).
- [ ] Critical updates use write concern `{ w: "majority" }`.
- [ ] Aggregation pipelines execute `$match` and `$project` at the initial stages.
- [ ] Multi-document transactions use `with_transaction` with retry logic for transient errors.
- [ ] In-memory sort limits (100MB) are avoided through index-assisted sorting.

---

## Tooling & Reference Guides

- **Official Drivers**: `mongodb` (Node.js/TypeScript), `pymongo` / `motor` (Python), `mongo-go-driver` (Go).
- **Diagnostics**: `mongosh` CLI, MongoDB Compass, `db.collection.explain("executionStats")`, MongoDB Atlas Performance Advisor.
- **Data Modeling Tools**: MongoDB Relational Migrator, Hackolade.
- **Documentation**: [MongoDB Indexing Strategies](https://www.mongodb.com/docs/manual/indexes/), [Equality Sort Range Rule](https://www.mongodb.com/docs/manual/tutorial/equality-sort-range-rule/), [MongoDB Aggregation Pipeline Optimization](https://www.mongodb.com/docs/manual/core/aggregation-pipeline-optimization/).
