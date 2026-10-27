---
name: database-sharding
description: "Horizontal database sharding, partition keys, distributed transactions, and rebalancing strategies."
---

# Database Sharding Protocol

1. Select a high-cardinality shard key that aligns with standard query boundaries (e.g. tenant_id).
2. Avoid cross-shard joins and distributed two-phase commit transactions.
3. Plan for consistent hashing to minimize data movement during cluster rebalancing.
