---
name: redis-debug
description: Debug and troubleshoot Redis usage. Use when investigating cache issues, connection failures, TTL problems, queue bottlenecks, or cache-related data staleness.
---

# Redis Debugging

## Quick Diagnostics

```bash
docker compose exec redis redis-cli ping
docker compose exec redis redis-cli info memory | grep used_memory_human
docker compose exec redis redis-cli info clients | grep connected_clients
docker compose exec redis redis-cli dbsize
docker compose exec redis redis-cli slowlog get 10
```

## Architecture

- Image: redis:alpine, port 7502 (host) -> 6379 (container)
- No password by default, single database (DB 0)

### Usage Patterns

| Consumer | Usage | File |
|---|---|---|
| CacheService | General key-value cache (GET/SET with TTL) | services/cacheService.ts |
| SemanticCacheService | Semantic similarity caching | services/semanticCacheService.ts |
| Rate Limiter | Request counting per user/IP | middleware/rateLimitMiddleware.ts |
| BullMQ | Email job queue | queues/emailQueue.ts |

## Key Files

| File | Purpose |
|---|---|
| src/backend/src/services/cacheService.ts | Redis client singleton, get/set helpers |
| src/backend/src/services/semanticCacheService.ts | Semantic caching for AI responses |
| src/backend/src/queues/connection.ts | BullMQ Redis connection |
| src/backend/src/queues/emailQueue.ts | Email job queue |

## Common Issues

### Redis not connected
initializeCache() catches errors and sets redisClient = null. App continues without cache.

### Cache returning stale data
No automatic invalidation. Check TTL: `docker compose exec redis redis-cli ttl "cache:your-key"`

### Rate limiter not working
If Redis is down, rate limiter behavior depends on implementation.

### Memory pressure
No maxmemory policy set by default.

### Connection pool exhaustion
Single client with reconnect strategy (3 retries, 500ms backoff). Not a pool.
