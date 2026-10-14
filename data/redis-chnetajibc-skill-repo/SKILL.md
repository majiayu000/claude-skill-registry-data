---
name: redis
description: "Redis operations: data structures, expiry, persistence, Lua/transactions, clustering, cache patterns. Use for caching, queues, rate limiting, sessions; research version docs first."
---

# redis

Memory is fast and forgetful: design expiry, eviction, and persistence before trusting it.

## Activate when

- Adding caching, distributed locks, rate limiters, sessions, or lightweight queues on Redis.

## Do NOT activate for

- Durable system-of-record storage (see fundamentals, postgres-operations).

## Procedure

1. Version: detect server version; research in https://redis.io/docs/ for that version (commands and clustering behavior evolve).
2. Structures: pick by access (strings, hashes, sorted sets for rankings/queues, streams for logs/queues, HyperLogLog/bitmaps for analytics); set TTLs deliberately; eviction policy matched to workload.
3. Correctness: Lua scripts or transactions for check-and-set; Redlock-style locks only with fencing for truly exclusive work; idempotent consumers for stream/queue use.
4. Persistence/HA: RDB+AOF per durability needs; replicas + sentinel/cluster understood before promising failover.
5. Security: AUTH/ACLs, no public exposure, sensitive values encrypted client-side where required.
6. Verify: eviction/expiry behavior tested, failover drill, memory-growth monitored, lock contention measured.

## References
- `../fundamentals/`, `../database-security/`.
- Registry: `../../research/documentation-search/references/framework-registry.yaml` (redis).
