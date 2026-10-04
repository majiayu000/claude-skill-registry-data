---
name: redis-patterns
description: Redis patterns for caching, sessions, pub/sub, and data structures. Covers ioredis, node-redis, and Redis 7+ features.
stacks: [redis]
packages: [redis, ioredis, "@redis/client"]
tags: [redis, cache, pubsub]
---

## Use this skill when

- Implementing caching with Redis (cache-aside, write-through)
- Setting up pub/sub or BLPOP-based work queues
- Using Redis data structures (Sorted Sets, Streams, Hash, Sets)
- Configuring ioredis for Node.js production environments
- Designing key naming conventions and TTL strategies
- Implementing distributed locks with atomic SET NX EX

## Do not use this skill when

- The task requires a message broker with guaranteed delivery — use BullMQ or a dedicated queue
- The task is about Redis configuration at the server/infrastructure level

## Instructions

1. Identify the use case: caching, pub/sub, queue, session, or rate limiting
2. Choose the appropriate Redis data structure for the access pattern
3. Design key naming with namespace:entity:id convention
4. Always set TTL — never leave keys without expiry unless intentionally (queue patterns)
5. Validate error handling and graceful shutdown behavior

## Capabilities

### Connection (ioredis — recommended for Node.js)
- Singleton client with lazyConnect enabled to defer connection until first command
- retryStrategy with exponential backoff for transient failures
- connectionName for identifying the process in Redis CLIENT LIST output
- Separate subscriber connection for pub/sub (cannot mix subscribe mode with regular commands)
- For BullMQ: `maxRetriesPerRequest: null` is mandatory

### Cache-Aside Pattern
- Check Redis first; on miss, fetch from source, store in Redis with TTL, return value
- Always serialize/deserialize with JSON.parse/JSON.stringify
- TTL strategy: short TTL (seconds) for volatile data, longer (minutes/hours) for stable data
- Invalidation by prefix: SCAN + DEL pattern (never KEYS * in production)

### Pub/Sub Pattern
- Publisher uses regular Redis connection
- Subscriber requires a dedicated connection (once subscribed, cannot run other commands)
- Subscribe to channels before publishing to avoid message loss
- Each subscriber connection handles one subscribe() call

### BLPOP Wake Queue (pipeline pattern)
- Producer sends LPUSH to a list key; consumer blocks on BRPOP/BLPOP
- Enables instant wake-up without polling
- Consumer loop: BLPOP with timeout, process item, loop again
- maxRetriesPerRequest must be null for BullMQ to work correctly

### Data Structures
- **Sorted Sets**: leaderboards, rate limiting with sliding window, scheduled job priority
- **Streams (XADD/XREAD)**: event sourcing, consumer groups, persistent message log
- **Hash (HSET/HGETALL)**: user session storage, object attributes with partial updates
- **Sets**: unique values, tag membership, set operations (union, intersect, diff)
- **Lists**: FIFO/LIFO queues, recent activity log with LPUSH + LTRIM

### Batch Operations
- Pipeline: group 3+ sequential commands into a single round-trip using redis.pipeline()
- Multi/Exec: atomic transaction for operations that must succeed or fail together
- Use pipeline for performance; use multi/exec for atomicity

### Distributed Locks
- SET key value NX EX seconds: acquire lock atomically
- Lua script for safe release: check owner before deleting to prevent releasing another owner's lock
- Always set expiry on locks to prevent deadlock on crash

### Lua Scripts
- Define reusable scripts with redis.defineCommand() for automatic EVALSHA caching
- Use for atomic read-modify-write operations that cannot be expressed with MULTI/EXEC

### Key Naming Convention
- Pattern: `scope:entity:id` — examples: `session:user:123`, `cache:products:featured`, `lock:payment:456`
- Consistent separator (colon) enables prefix-based scanning and invalidation

### Error Handling
- Always attach error event handler on Redis client — unhandled errors crash the process
- Log ready, reconnecting, and close events for operational visibility
- Distinguish between connection errors (retry) and command errors (fail fast)

### Graceful Shutdown
- Use redis.quit() — waits for pending commands to complete before closing
- Use redis.disconnect() — immediate close without waiting (use only in emergency)
- Integrate with PM2 SIGTERM handler: quit() then allow process.exit()

## Behavioral Traits
- Always sets TTL on every SET command — no exception unless the key is a queue
- Uses SCAN instead of KEYS * in production to avoid blocking the server
- Keeps subscriber connections separate from command connections
- Attaches error event handler before connecting
- Uses pipeline for batching, multi/exec for atomicity
- Validates that BullMQ clients have maxRetriesPerRequest: null
- Uses Lua scripts for operations requiring atomic read-modify-write

## Knowledge Base

### TTL Strategy Guide
- User session: 24 hours to 7 days (depends on remember-me behavior)
- API response cache: 1 minute to 1 hour (depends on data freshness requirements)
- Rate limit window: matches the window size (60 seconds for per-minute limits)
- Distributed lock: slightly longer than the expected operation duration
- BLPOP queue keys: no TTL (persistent until consumed)

### Redis Eviction Policies
- allkeys-lru: evict least recently used keys from all keys (good for caching)
- volatile-lru: evict LRU from keys with TTL set (protects queue keys without TTL)
- noeviction: return error on write when memory full (required for BullMQ)
- allkeys-lfu: evict least frequently used (better than LRU for repeated access patterns)

### Common Mistakes
- Using KEYS * in production: blocks Redis for the duration of the scan on large keyspaces
- Missing error handler on Redis client: unhandled error events crash the Node.js process
- Mixing subscribe mode and command mode on one connection: pub/sub requires dedicated connection
- Missing TTL on cache keys: causes unbounded memory growth
- Using redis.disconnect() in graceful shutdown: drops in-flight commands; use redis.quit()
- Omitting maxRetriesPerRequest: null for BullMQ: causes connection failures under load

## Constraints
- Always set TTL on every SET command unless the key is intentionally persistent (queue or lock)
- Never use KEYS * in production code — use SCAN with cursor
- Subscriber connection must be dedicated — never mix subscribe with regular commands
- BullMQ clients must have maxRetriesPerRequest: null
- Error event handler must be attached to every Redis client instance
- Always use quit() for graceful shutdown, not disconnect()

## API Reference

Detailed API documentation: [references/REFERENCE.md](references/REFERENCE.md).

**When to read**: when you need exact method signatures, configuration options, type definitions, or implementation details not covered above.

**How to use**: search or read the reference for specific APIs before writing code. Don't read the entire file — look up only what you need.
