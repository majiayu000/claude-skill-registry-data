---
name: redis-streams
description: Redis Streams Engineer — Institutional capability and runbook for redis-streams.
---

# SKILL: Redis Streams Engineer
## Domain: Durable Messaging, Consumer Groups, Rate Limiting, Cache Patterns

**Activation triggers:** Redis streams, consumer groups, rate limiting, session
cache, Redis pub/sub, message queue, job queue, leaky bucket, token bucket,
Redis data structures.

---

## Redis Use Cases in Integral Market

```
Feature                    | Data Structure  | TTL
────────────────────────────|─────────────────|──────────
Rate limiting               | Hash + Script   | Per window
Session / refresh tokens    | Hash            | Token expiry
Domain events               | Stream (xadd)   | maxlen cap
Live price pub/sub          | Pub/Sub         | None (fire-forget)
Analytics cache             | String (JSON)   | 5 min
Provider list cache         | String (JSON)   | 60 sec
User permission cache       | Hash            | 5 min
WebSocket channel routing   | Set             | Connection lifetime
Background job queue        | Stream          | maxlen cap
```

---

## Redis Connection (aioredis)

```python
# app/core/redis.py
import aioredis
from app.core.config import settings

_redis: aioredis.Redis | None = None

async def get_redis() -> aioredis.Redis:
    global _redis
    if _redis is None:
        _redis = await aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            max_connections=20,
            socket_timeout=5,
            socket_connect_timeout=5,
        )
    return _redis

async def close_redis() -> None:
    global _redis
    if _redis:
        await _redis.close()
        _redis = None
```

---

## Rate Limiting with Redis (Sliding Window)

```python
# app/core/rate_limiter.py
import time
import hashlib
from aioredis import Redis

class SlidingWindowRateLimiter:
    """Token-efficient sliding window rate limiter using Redis sorted sets."""

    async def is_allowed(
        self,
        redis: Redis,
        key: str,
        limit: int,
        window_seconds: int,
    ) -> tuple[bool, int]:
        """Returns (allowed, remaining_count)."""
        now = time.time()
        window_start = now - window_seconds

        pipe = redis.pipeline(transaction=True)
        # Remove expired entries
        pipe.zremrangebyscore(key, 0, window_start)
        # Count current entries
        pipe.zcard(key)
        # Add this request
        pipe.zadd(key, {f"{now}:{hashlib.md5(str(now).encode()).hexdigest()[:8]}": now})
        # Set expiry
        pipe.expire(key, window_seconds + 1)
        results = await pipe.execute()

        current_count = results[1]
        if current_count >= limit:
            return False, 0
        return True, limit - current_count - 1
```

---

## Consumer Group Pattern (Durable Events)

```python
# app/workers/event_consumer.py
import asyncio
import json
import logging
from aioredis import Redis

logger = logging.getLogger(__name__)

async def run_consumer(
    redis: Redis,
    stream: str,
    group: str,
    consumer: str,
    handler: callable,
) -> None:
    """
    Consumer group worker — exactly-once delivery guarantee per group.
    - Each message delivered to exactly one consumer in the group
    - Messages persist until explicitly ACKed
    - Pending/failed messages can be claimed and retried
    """
    # Create group, start from beginning if new
    try:
        await redis.xgroup_create(stream, group, id="$", mkstream=True)
    except Exception:
        pass  # Group already exists

    while True:
        try:
            # ">" means: deliver only new, undelivered messages to this consumer
            messages = await redis.xreadgroup(
                groupname=group,
                consumername=consumer,
                streams={stream: ">"},
                count=50,
                block=5000,
            )

            if not messages:
                continue

            for stream_name, entries in messages:
                for entry_id, data in entries:
                    try:
                        await handler(data)
                        # ACK only after successful processing
                        await redis.xack(stream, group, entry_id)
                    except Exception:
                        logger.exception("Handler failed, NOT acking", extra={
                            "stream": stream,
                            "entry_id": entry_id,
                        })
                        # Message stays in PEL (pending entries list) for retry

        except asyncio.CancelledError:
            break
        except Exception as exc:
            logger.exception("Consumer loop error", extra={"error": str(exc)})
            await asyncio.sleep(5)

# Reclaim and retry stuck messages (pending > 30s)
async def reclaim_stuck_messages(redis: Redis, stream: str, group: str, consumer: str) -> int:
    pending = await redis.xautoclaim(
        stream, group, consumer,
        min_idle_time=30_000,   # 30 seconds in ms
        start_id="0-0",
        count=100,
    )
    return len(pending[1])   # number of reclaimed messages
```

---

## Cache-Aside Pattern

```python
# app/core/cache_patterns.py
import json
from typing import TypeVar, Callable, Awaitable
from aioredis import Redis

T = TypeVar("T")

async def get_or_set(
    redis: Redis,
    key: str,
    factory: Callable[[], Awaitable[T]],
    ttl: int,
    serializer=json.dumps,
    deserializer=json.loads,
) -> T:
    """Cache-aside: fetch from cache, compute and store if missing."""
    cached = await redis.get(key)
    if cached is not None:
        return deserializer(cached)

    value = await factory()
    await redis.setex(key, ttl, serializer(value, default=str))
    return value

# Usage:
async def get_provider_list(redis: Redis, db: AsyncSession) -> list[dict]:
    return await get_or_set(
        redis=redis,
        key="cache:providers:active",
        factory=lambda: _fetch_providers_from_db(db),
        ttl=60,
    )
```

---

## Redis Key Naming Convention

```python
# Always use structured key namespaces to avoid collisions
# Format: <namespace>:<entity>:<identifier>[:<field>]

KEY_PATTERNS = {
    # Rate limiting
    "rl:{ip}":                    "rate limit counter for IP",
    "rl:middleware:{ip}":         "middleware rate limit",
    "rl:login:{ip}":              "auth login rate limit",

    # Cache
    "cache:providers:active":     "list of active copy providers",
    "cache:performance:{acct_id}":"performance summary for account",
    "cache:user:{user_id}:perms": "user permissions",

    # Events / queues
    "events:trade":               "trade domain events stream",
    "events:signal":              "copy signal events stream",
    "events:notification":        "notification events stream",

    # Sessions
    "session:{token_hash}":       "refresh token session",

    # WebSocket routing
    "ws:user:{user_id}:channels": "active WS channel subscriptions",
}
```

---

## Anti-Patterns

```
✗ Using pub/sub for critical events (fire-and-forget — message lost if no subscriber)
✗ No maxlen on streams (unbounded growth → OOM)
✗ ACKing before processing (lost messages on failure)
✗ One Redis connection per request (use connection pool)
✗ Storing large objects in Redis (keep values < 1MB)
✗ Key names without namespace (collision with other services)
✗ No TTL on cache keys (stale data accumulates forever)
✗ String keys for rate limiting (use sorted sets for sliding window)
✗ KEYS * in production (blocks Redis for O(N) scan)
```
