---
name: caching
description: Design and implement caching strategies across all layers — in-memory, distributed (Redis/Memcached), CDN, HTTP cache headers, and application-level memoization
layer: utility
category: performance
triggers:
  - "cache this"
  - "add caching"
  - "caching strategy"
  - "redis cache"
  - "CDN caching"
  - "HTTP cache headers"
  - "memoize"
  - "cache invalidation"
inputs:
  - Resource or endpoint to cache
  - Current latency or load characteristics
  - Data freshness requirements (real-time, near-real-time, stale-ok)
  - Infrastructure available (Redis, Memcached, CDN provider, edge)
outputs:
  - Caching strategy document with layer recommendations
  - Implementation code for chosen cache layer(s)
  - Cache invalidation plan
  - TTL and eviction policy recommendations
  - Monitoring and hit-rate tracking guidance
linksTo:
  - api-designer
  - data-modeling
  - performance-profiler
linkedFrom:
  - optimize
  - ship
preferredNextSkills:
  - performance-profiler
  - testing-patterns
fallbackSkills:
  - optimize
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: selective
sideEffects:
  - May add Redis or cache dependencies to project
  - May modify HTTP response headers
  - May add middleware or proxy configuration
---

# Caching Strategies Skill

## Purpose

Caching is the single highest-ROI performance optimization in most systems. This skill designs multi-layer caching strategies, implements them correctly, and — critically — plans cache invalidation so stale data does not become a silent bug.

## Key Concepts

### The Caching Pyramid (Top = Fastest, Bottom = Slowest)

```
     [Browser Cache]         ← HTTP headers, Service Worker
      [CDN / Edge]           ← Vercel Edge, Cloudflare, Fastly
    [Reverse Proxy]          ← Nginx, Varnish
   [Application Cache]       ← In-memory (LRU), Redis, Memcached
  [Database Query Cache]     ← Materialized views, query result cache
 [Source of Truth (DB/API)]  ← Always correct, slowest
```

### Cache Taxonomy

| Strategy | TTL | Invalidation | Best For |
|----------|-----|-------------|----------|
| **Write-through** | N/A | On write | Consistency-critical data |
| **Write-behind** | N/A | Async after write | High write throughput |
| **Cache-aside (Lazy)** | Time-based | TTL expiry + manual | Read-heavy, tolerance for staleness |
| **Read-through** | Time-based | TTL expiry | Transparent to caller |
| **Refresh-ahead** | Time-based | Pre-emptive refresh | Predictable access patterns |

### The Two Hard Problems

1. **Cache Invalidation** — When does cached data become wrong?
2. **Naming/Keying** — How do you ensure the right data maps to the right key?

## Workflow

### Step 1: Profile Before Caching

Never cache blindly. Identify:
- Which endpoints/queries are slowest?
- Which are called most frequently?
- What is the read:write ratio?
- What is the acceptable staleness window?

```
Latency Budget Analysis:
  Target: < 200ms p95
  Current: 850ms p95
  Breakdown:
    DB query: 600ms (cacheable — read:write = 50:1)
    API call: 200ms (cacheable — changes hourly)
    Compute:   50ms (memoizable — pure function)
```

### Step 2: Choose Cache Layer(s)

**Decision Matrix:**

```
Is it static content (images, JS, CSS)?
  → CDN + immutable cache headers

Is it per-user, session-scoped?
  → In-memory (server) or browser cache

Is it shared across users, read-heavy?
  → Redis / Memcached with cache-aside

Is it an expensive pure computation?
  → Memoization (in-process LRU)

Is it an API response with known TTL?
  → HTTP Cache-Control headers + stale-while-revalidate
```

### Step 3: Implement

#### HTTP Cache Headers

```typescript
// Next.js API route or middleware
export function GET(request: Request) {
  const data = await fetchData();

  return Response.json(data, {
    headers: {
      // Public: CDN can cache. max-age: browser TTL. s-maxage: CDN TTL.
      'Cache-Control': 'public, max-age=60, s-maxage=300, stale-while-revalidate=600',
      // Vary ensures different cached versions per relevant header
      'Vary': 'Accept-Encoding, Authorization',
    },
  });
}
```

**Cache-Control Cheat Sheet:**

| Directive | Meaning |
|-----------|---------|
| `public` | Any cache (CDN, proxy) may store |
| `private` | Only browser may store |
| `no-cache` | Must revalidate before use (NOT "don't cache") |
| `no-store` | Truly never cache |
| `max-age=N` | Fresh for N seconds (browser) |
| `s-maxage=N` | Fresh for N seconds (shared/CDN cache) |
| `stale-while-revalidate=N` | Serve stale for N seconds while refreshing in background |
| `immutable` | Never changes (use with hashed filenames) |

#### Redis Cache-Aside Pattern

```typescript
import { Redis } from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

interface CacheOptions {
  ttl: number;          // seconds
  prefix?: string;
  serialize?: (v: unknown) => string;
  deserialize?: (v: string) => unknown;
}

async function cacheAside<T>(
  key: string,
  fetcher: () => Promise<T>,
  options: CacheOptions
): Promise<T> {
  const fullKey = options.prefix ? `${options.prefix}:${key}` : key;
  const serialize = options.serialize ?? JSON.stringify;
  const deserialize = options.deserialize ?? JSON.parse;

  // 1. Try cache
  const cached = await redis.get(fullKey);
  if (cached !== null) {
    return deserialize(cached) as T;
  }

  // 2. Cache miss — fetch from source
  const data = await fetcher();

  // 3. Write to cache (don't await — fire and forget for speed)
  redis.setex(fullKey, options.ttl, serialize(data)).catch((err) => {
    console.error(`Cache write failed for ${fullKey}:`, err);
  });

  return data;
}

// Usage
const user = await cacheAside(
  `user:${userId}`,
  () => db.user.findUnique({ where: { id: userId } }),
  { ttl: 300, prefix: 'app' }
);
```

#### In-Memory LRU Cache

```typescript
class LRUCache<K, V> {
  private cache = new Map<K, V>();

  constructor(private maxSize: number) {}

  get(key: K): V | undefined {
    const value = this.cache.get(key);
    if (value !== undefined) {
      // Move to end (most recently used)
      this.cache.delete(key);
      this.cache.set(key, value);
    }
    return value;
  }

  set(key: K, value: V): void {
    if (this.cache.has(key)) {
      this.cache.delete(key);
    } else if (this.cache.size >= this.maxSize) {
      // Evict least recently used (first entry)
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
    this.cache.set(key, value);
  }
}

// For production, use `lru-cache` package instead of rolling your own
```

#### Next.js / Vercel Specific

```typescript
// next.config.js — static asset caching
const nextConfig = {
  headers: async () => [
    {
      source: '/_next/static/:path*',
      headers: [
        { key: 'Cache-Control', value: 'public, max-age=31536000, immutable' },
      ],
    },
  ],
};

// ISR (Incremental Static Regeneration)
export const revalidate = 60; // Revalidate every 60 seconds

// On-demand revalidation
import { revalidateTag } from 'next/cache';
export async function POST(request: Request) {
  revalidateTag('posts');
  return Response.json({ revalidated: true });
}
```

### Step 4: Cache Invalidation Strategy

**Pattern: Event-Driven Invalidation**

```typescript
// After a write operation, invalidate related cache keys
async function updateUser(userId: string, data: UpdateUserData) {
  const updated = await db.user.update({ where: { id: userId }, data });

  // Invalidate all cache keys related to this user
  const keysToInvalidate = [
    `app:user:${userId}`,
    `app:user-profile:${userId}`,
    `app:user-posts:${userId}`,
  ];

  await Promise.all(keysToInvalidate.map((key) => redis.del(key)));

  // If using tag-based invalidation (Next.js)
  revalidateTag(`user-${userId}`);

  return updated;
}
```

**Pattern: Versioned Keys**

```typescript
// Instead of invalidating, bump a version
const version = await redis.incr(`version:user:${userId}`);
const cacheKey = `user:${userId}:v${version}`;
// Old versions naturally expire via TTL
```

### Step 5: Monitor Cache Health

Key metrics to track:
- **Hit Rate**: Target > 90% for most caches
- **Miss Rate**: Spikes indicate cold cache or invalidation storms
- **Eviction Rate**: High evictions = cache is too small
- **Latency**: p50 and p99 for cache reads
- **Memory Usage**: Track growth over time

```typescript
// Simple hit/miss tracking
let hits = 0, misses = 0;

async function cachedFetch<T>(key: string, fetcher: () => Promise<T>): Promise<T> {
  const cached = await redis.get(key);
  if (cached) {
    hits++;
    return JSON.parse(cached);
  }
  misses++;
  const data = await fetcher();
  await redis.setex(key, 300, JSON.stringify(data));
  return data;
}

// Expose metrics endpoint
function getCacheStats() {
  const total = hits + misses;
  return {
    hits,
    misses,
    hitRate: total > 0 ? (hits / total * 100).toFixed(1) + '%' : 'N/A',
  };
}
```

## Common Pitfalls

1. **Cache Stampede** — Many requests hit an expired key simultaneously. Fix: Use locking (`SETNX`) or `stale-while-revalidate`.
2. **Thundering Herd** — Cold cache after deploy. Fix: Pre-warm critical keys.
3. **Dogpiling** — Multiple processes try to rebuild the same cache entry. Fix: Probabilistic early expiration or mutex.
4. **Over-caching** — Caching data that changes frequently, leading to stale reads. Fix: Measure read:write ratio first.
5. **Key Explosion** — Unique keys per request parameter combo. Fix: Normalize and limit key cardinality.

## Examples

### Example 1: E-commerce Product Page

```
Layer 1: CDN (Vercel Edge) — Cache full HTML for 60s, stale-while-revalidate 300s
Layer 2: Redis — Cache product data for 5 min, invalidate on admin update
Layer 3: DB query cache — Materialized view for price calculations, refresh every minute
Invalidation: Webhook from CMS triggers revalidateTag('product-{id}')
```

### Example 2: User Dashboard (Personalized)

```
Layer 1: Browser — Cache-Control: private, max-age=0, must-revalidate (no shared cache)
Layer 2: Redis — Cache per-user dashboard data for 30s
Layer 3: In-memory — LRU cache for user preferences (small, rarely changes)
Invalidation: Write-through on user action, TTL expiry for background data
```

### Example 3: Public API with Rate Limits

```
Layer 1: CDN — Cache GET responses for 10s with Vary: Authorization
Layer 2: Redis — Cache API responses per unique query hash for 60s
Rate limit: Use Redis INCR with TTL for sliding window rate limiting
Invalidation: Short TTLs only — no explicit invalidation needed
```
