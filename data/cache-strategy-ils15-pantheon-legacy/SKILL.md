---
name: cache-strategy
description: "Cache patterns for Redis, CDN, TTL, and invalidation. Use for architecture decisions on caching strategies."
context: fork
globs: ["**/*.py", "**/*.ts"]
alwaysApply: false
---

# Cache Strategy — Architecture Patterns

Use this skill for cache architecture decisions. Covers Redis patterns, CDN strategies, TTL management, cache invalidation, and session stores. Used by Demeter during schema design and Hermes during implementation.

---

## Cache Patterns

### 1. Read-Through Cache

The cache sits between the application and the database. On a cache miss, the cache loads the data from the database.

```python
import redis
import json
from typing import Optional

class ReadThroughCache:
    def __init__(self, redis_client: redis.Redis, ttl: int = 300):
        self.redis = redis_client
        self.ttl = ttl
    
    async def get(self, key: str, loader) -> Optional[dict]:
        """Get from cache. If miss, load from source and cache."""
        cached = await self.redis.get(key)
        if cached:
            return json.loads(cached)
        
        # Cache miss — load from source
        data = await loader()
        if data:
            await self.redis.setex(key, self.ttl, json.dumps(data))
        return data
```

**When to use:** Read-heavy workloads (products, reviews, user profiles)

### 2. Write-Through Cache

Data is written to both the cache and the database simultaneously.

```python
class WriteThroughCache:
    async def set(self, key: str, data: dict, saver):
        """Write to cache and database simultaneously."""
        # Write to database first
        await saver(data)
        # Then update cache
        await self.redis.setex(key, self.ttl, json.dumps(data))
    
    async def delete(self, key: str, deleter):
        """Delete from both cache and database."""
        await deleter()
        await self.redis.delete(key)
```

**When to use:** Data that must be consistent (user accounts, orders)

### 3. Write-Behind (Write-Back) Cache

Data is written to the cache first, then asynchronously flushed to the database.

```python
import asyncio
from collections import OrderedDict

class WriteBehindCache:
    def __init__(self, flush_interval: int = 5):
        self.write_queue = OrderedDict()
        self.flush_interval = flush_interval
    
    async def set(self, key: str, data: dict):
        """Write to cache only. Flush to DB asynchronously."""
        self.write_queue[key] = data
        if len(self.write_queue) >= 100:
            await self._flush()
    
    async def _flush(self):
        """Flush all pending writes to database."""
        batch = dict(self.write_queue)
        self.write_queue.clear()
        # Batch write to database
        await self._batch_save(batch)
```

**When to use:** High-write workloads (analytics, metrics, logs)

---

## TTL Strategies

| Strategy | TTL | Use Case |
|----------|-----|----------|
| **Short-lived** | 1-5 min | Real-time data (stock prices, live scores) |
| **Medium-lived** | 5-30 min | User sessions, API responses |
| **Long-lived** | 1-24 hours | Product catalogs, static content |
| **Never expire** | No TTL | Reference data (countries, currencies) |

### TTL Calculation

```python
def calculate_ttl(data_freshness: str, access_frequency: str) -> int:
    """Calculate optimal TTL based on data characteristics."""
    base_ttl = {
        "real-time": 60,
        "frequent": 300,
        "occasional": 1800,
        "rare": 3600,
    }
    
    frequency_multiplier = {
        "high": 0.5,   # Halve TTL for high-frequency access
        "medium": 1.0,
        "low": 2.0,    # Double TTL for low-frequency access
    }
    
    return base_ttl[data_freshness] * frequency_multiplier[access_frequency]
```

---

## Cache Invalidation Patterns

### 1. Time-Based Invalidation

Simplest approach — data expires after TTL.

```python
# Redis automatically handles this with EXPIRE
await redis.setex("user:123", 300, json.dumps(user_data))
```

### 2. Event-Based Invalidation

Invalidate cache when data changes.

```python
async def update_user(user_id: str, data: dict):
    await db.update_user(user_id, data)
    # Invalidate cache
    await redis.delete(f"user:{user_id}")
    # Invalidate related caches
    await redis.delete(f"user:{user_id}:profile")
    await redis.delete(f"user:{user_id}:preferences")
```

### 3. Tag-Based Invalidation

Group cache entries by tag and invalidate all entries with a tag.

```python
import redis

class TaggedCache:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
    
    async def set(self, key: str, data: dict, tags: list[str], ttl: int = 300):
        """Set cache entry with tags."""
        await self.redis.setex(key, ttl, json.dumps(data))
        for tag in tags:
            await self.redis.sadd(f"tag:{tag}", key)
    
    async def invalidate_tag(self, tag: str):
        """Invalidate all cache entries with a tag."""
        keys = await self.redis.smembers(f"tag:{tag}")
        if keys:
            await self.redis.delete(*keys)
            await self.redis.delete(f"tag:{tag}")

# Usage
cache = TaggedCache(redis_client)
await cache.set("product:123", product_data, tags=["products", "category:electronics"])

# When product catalog updates:
await cache.invalidate_tag("products")
```

---

## CDN Cache Headers

```python
from fastapi.responses import JSONResponse

@router.get("/products/{product_id}")
async def get_product(product_id: str):
    product = await get_product_from_db(product_id)
    
    response = JSONResponse(content=product)
    # CDN headers
    response.headers["Cache-Control"] = "public, max-age=3600, stale-while-revalidate=300"
    response.headers["ETag"] = f'"{product["updated_at"]}"'
    response.headers["Vary"] = "Accept-Encoding"
    
    return response
```

### Cache-Control Directives

| Directive | Meaning |
|-----------|---------|
| `public` | Cacheable by any cache |
| `private` | Cacheable only by browser |
| `max-age=N` | Cache for N seconds |
| `no-cache` | Must revalidate before using cache |
| `no-store` | Do not cache at all |
| `stale-while-revalidate=N` | Serve stale for N seconds while revalidating |
| `stale-if-error=N` | Serve stale for N seconds if origin errors |

---

## Session Store (Redis)

```python
from fastapi import FastAPI, Request
from redis.asyncio import Redis
import uuid

app = FastAPI()
redis_client = Redis(host="localhost", port=6379, db=0)

@app.middleware("http")
async def session_middleware(request: Request, call_next):
    session_id = request.cookies.get("session_id")
    
    if not session_id:
        session_id = str(uuid.uuid4())
    
    # Load session from Redis
    session_data = await redis_client.get(f"session:{session_id}")
    request.state.session = json.loads(session_data) if session_data else {}
    
    response = await call_next(request)
    
    # Save session to Redis (TTL = 24 hours)
    await redis_client.setex(
        f"session:{session_id}",
        86400,
        json.dumps(request.state.session)
    )
    response.set_cookie("session_id", session_id, httponly=True, secure=True)
    
    return response
```

---

## When to Cache

| Scenario | Cache? | Pattern |
|----------|--------|---------|
| Read-heavy, rarely changing | ✅ Yes | Read-through, long TTL |
| Write-heavy, real-time | ❌ No | Direct DB access |
| Expensive computation | ✅ Yes | Read-through, medium TTL |
| User-specific data | ✅ Yes | Read-through, short TTL |
| Static content | ✅ Yes | CDN, long TTL |
| Financial transactions | ❌ No | Direct DB, no cache |

---

## Integration with Demeter and Hermes

**Demeter** uses this skill during schema design to decide what needs caching.
**Hermes** uses this skill during implementation to apply cache patterns.
