---
name: mongodb
description: "Design MongoDB documents and indexes, build aggregation pipelines, and investigate query plans or transaction behavior."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["mongodb", "aggregation", "indexes", "nosql", "atlas", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# MongoDB Document Database AI Skill Guide

## Overview & Engine Architecture

MongoDB stores BSON documents in collections. Query shapes drive index design; the aggregation framework transforms streams of documents through stages. Agents model data for the application's access patterns, avoid unbounded arrays, and verify plans with `explain("executionStats")` before shipping hot-path queries.

```
Drivers / ORMs
    -> mongod (replica set / sharded cluster)
        -> databases -> collections -> documents
        -> indexes (B-tree / compound / text / TTL)
        -> aggregation pipeline
```

## When to use this skill

- Designing collections and references vs embedding
- Writing find queries and aggregations
- Diagnosing COLLSCAN and slow operations
- Using multi-document transactions carefully

## Operational directives

1. Index for equality filters first, then sort keys, then range - matching real queries.
2. Prefer embedding for data read together; reference for high-churn or unbounded growth.
3. Cap array sizes; use bucket patterns for time series when appropriate.
4. Use transactions only when multi-document ACID is required - they cost throughput.
5. Never expose cluster credentials in client-side apps; use least-privilege DB users.

## Modeling example

```javascript
// orders collection - embed line items when bounded
{
  _id: ObjectId("..."),
  customerId: ObjectId("..."),
  status: "open",
  items: [
    { sku: "SKU-1", qty: 2, priceCents: 1500 }
  ],
  createdAt: ISODate("...")
}

db.orders.createIndex({ customerId: 1, createdAt: -1 })
db.orders.createIndex({ status: 1 }, { partialFilterExpression: { status: "open" } })
```

## Aggregation sketch

```javascript
db.orders.aggregate([
  { $match: { createdAt: { $gte: ISODate("2026-01-01") } } },
  { $group: { _id: "$customerId", revenue: { $sum: "$totalCents" } } },
  { $sort: { revenue: -1 } },
  { $limit: 50 }
])
```

## Explain checklist

```javascript
db.orders.find({ customerId: id, status: "open" }).sort({ createdAt: -1 }).explain("executionStats")
```

| Signal | Meaning |
| --- | --- |
| COLLSCAN | Missing or unused index |
| IXSCAN + high docsExamined/nReturned | Weak selectivity / wrong index |
| In-memory sort | Add sort keys to compound index |

## Best practices

- Use schema validation (`$jsonSchema`) for critical collections.
- TTL indexes for ephemeral data (sessions, logs).
- Retryable writes and majority read/write concerns for important paths.
- Monitor working set vs RAM on self-hosted deployments.

## Limitations

- Atlas vs self-managed differs in auth, networking, and backup UX.
- Graph use cases may belong in specialized stores.
- Change streams need replica sets and careful resume token handling.

## Related skills

- `@postgresql` - relational alternative when joins dominate
- `@redis` - caching hot Mongo reads
- `@nodejs` - common driver runtime
