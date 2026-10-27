---
name: redis-caching
description: "Redis data structures, memory eviction policies, pipeline transactions, and TTL key management."
---

# Redis High-Performance Protocol

1. Select specialized data structures: Hashes for objects, Sorted Sets for leaderboards, Bitmaps for presence.
2. Always configure volatile-lru or allkeys-lru eviction policies.
3. Use pipeline batching for multi-key queries to reduce round-trip network latency.
