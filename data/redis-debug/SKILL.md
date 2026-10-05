---
name: redis-debug
description: Debug and troubleshoot Redis usage in ettametta. Use when investigating cache issues, pub/sub problems, connection failures, broker connectivity, memory pressure, or key pattern anomalies.
---
# Redis Debugging

## Quick Diagnostics

```bash
redis-cli -p 7204 -a "$REDIS_PASSWORD" ping
redis-cli -p 7204 -a "$REDIS_PASSWORD" info memory
redis-cli -p 7204 -a "$REDIS_PASSWORD" info clients
redis-cli -p 7204 -a "$REDIS_PASSWORD" dbsize
redis-cli -p 7204 -a "$REDIS_PASSWORD" --scan --pattern "analytics:*" | head -20
redis-cli -p 7204 -a "$REDIS_PASSWORD" llen celery
```

## Connection Config

- Image: redis:7-alpine, port 7204 (host) -> 6379 (container)
- URL: `redis://:${REDIS_PASSWORD}@redis:6379/0`
- Always DB 0 — all subsystems share one database
- Celery broker, results, cache, security, chaos, GPU semaphores, pub/sub all on DB 0

## Key Patterns and TTLs

| Key Pattern | TTL | Purpose |
|---|---|---|
| fastapi-cache:* | Default | Response cache |
| analytics:report:{post_id}:{user_id} | 1h | Analytics cache |
| optimization:viral_package:{id}:{niche}:{platform} | 1h | Viral package cache |
| discovery:trends:{niche}:{horizon}:{region} | **None!** | Trend cache (stale risk) |
| active_batch:{strategy} | 24h | Experiment cohort |
| EM_FEATURES:{niche} | 24h | Feature store |
| sentinel:security_logs | None (trim 1000) | Security log list |
| sentinel:security_health:audit:{date} | 7d | Audit results |
| security:requests:{client_ip} | 5m | Rate tracking |
| ettametta:gpu:slots | 7d | GPU semaphore |
| token_blacklist (set) | TTL applied | JWT blacklist (fixed 2026-05-28) |

## Known Issues

### No connection pooling / connection explosion
12+ separate `redis.from_url()` calls, each creating its own pool. No centralized manager.
Affected: OptimizationService, AnalyticsService, SecuritySentinel, GpuQueueManager, ConnectionManager, DistributedEventBus, GlobalFeatureStore, hot-reload, FastAPICache.

### Sync Redis clients blocking event loop
Multiple async services use synchronous `redis.Redis`:
- `src/services/optimization/service.py` line 36
- `src/services/analytics/service.py` line 30
- `src/services/security/service.py` line 19
- `src/services/discovery/service.py` line 213

### Token blacklist TTL
`SADD` with TTL applied (fixed 2026-05-28). Check: `redis-cli -p 7204 scard token_blacklist`

### Discovery cache has no TTL
`discovery:trends:*` keys may never expire.

### localhost-to-redis hostname hack
`settings.REDIS_URL.replace("//localhost", "//redis")` — fragile.

### No retry/circuit breaking on Redis ops
Unlike AI providers (tenacity + CircuitBreaker), Redis operations have no retry logic.

### Blocking BLPOP in async context
GpuQueueManager uses sync `self.redis.blpop()` inside `asynccontextmanager`.

## Redis Wrappers

| File | Purpose |
|---|---|
| src/api/utils/redis.py | Async singleton client |
| src/services/infrastructure/event_bus.py | Redis Streams with consumer groups, DLQ |
| src/api/routes/ws.py | PubSub + Streams for WebSocket broadcasting |
| src/services/infrastructure/global_feature_store.py | HMSET/HGETALL for features |
| src/services/video_engine/synthesis_service.py | BLPOP/RPUSH GPU semaphore |

## Pub/Sub Channels

| Channel | Purpose |
|---|---|
| job_updates | Video job progress |
| system_logs | Real-time log broadcast |
| system_config_reload | Settings hot-reload |

## Streams

| Stream | Consumer Group | Purpose |
|---|---|---|
| VF_FLOW_STREAMS | VF_COORDINATOR_GROUP | Distributed event bus |
| VF_FLOW_DLQ | — | Dead letter queue |

## Debugging Checklist

1. `redis-cli -p 7204 ping`
2. Memory: `redis-cli info memory | grep used_memory_human`
3. Connections: `redis-cli info clients | grep connected_clients`
4. Key count: `redis-cli dbsize`
5. Slow queries: `redis-cli slowlog get 10`
6. Celery queue: `redis-cli llen celery`
7. Token blacklist size: `redis-cli scard token_blacklist`
