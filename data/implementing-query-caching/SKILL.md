---
name: implementing-query-caching
description: Implement query result caching with Redis and proper invalidation strategies for Prisma 6. Use when optimizing frequently accessed data, improving read-heavy application performance, or reducing database load through caching.
allowed-tools: Read, Write, Edit
version: 1.0.0
---

# Query Result Caching with Redis

Efficient query result caching for Prisma 6 applications using Redis: cache key generation, invalidation strategies, TTL management, and when caching provides value.

---

<role>
Implement query result caching with Redis for Prisma 6, covering cache key generation, invalidation, TTL strategies, and identifying when caching delivers value.
</role>

<when-to-activate>
User mentions: caching, Redis, performance optimization, slow queries, read-heavy applications, frequently accessed data, reducing database load, improving response times, cache invalidation, cache warming, or optimizing Prisma queries.
</when-to-activate>

<overview>
Query caching reduces database load and improves read response times, but adds complexity: cache invalidation, consistency challenges, infrastructure. Key capabilities: Redis-Prisma integration, consistent cache key patterns, mutation-triggered invalidation, TTL strategies (time/event-based), and identifying when caching provides value.
</overview>

<workflow>
**Phase 1: Identify Cache Candidates**
Analyze query patterns for read-heavy operations; identify data with acceptable staleness; measure baseline query performance; estimate cache hit rate and improvement.

**Phase 2: Implement Cache Layer**
Set up Redis with connection pooling; create cache wrapper around Prisma queries; implement consistent cache key generation; add cache read with database fallback.

**Phase 3: Implement Invalidation**
Identify mutations affecting cached data; add invalidation to update/delete operations; handle bulk operations and cascading invalidation; test across scenarios.

**Phase 4: Configure TTL**
Determine appropriate TTL per data type; implement time-based expiration; add event-based invalidation for critical data; monitor hit rates and adjust.
</workflow>

<decision-tree>
## When to Cache

**Strong Candidates:**

- Read-heavy data (>10:1 ratio): user profiles, product catalogs, configuration, content lists
- Expensive queries: large aggregations, multi-join, complex filtering, computed values
- High-frequency access

: homepage data, navigation, popular results, trending content

**Weak Candidates:**

- Write-heavy data (<3:1 ratio): analytics, activity logs, messages, live updates
- Frequently changing: stock prices, inventory, bids, live scores
- User-specific: shopping carts, drafts, recommendations, sessions
- Fast simple queries: primary key lookups, indexed queries, already in DB cache

**Decision Tree:**

```
Read/write ratio > 10:1?
├─ Yes: Strong candidate
│  └─ Data stale 1+ minutes acceptable?
│     ├─ Yes: Long TTL (5-60min) + event invalidation
│     └─ No: Short TTL (10-60sec) + aggressive invalidation
└─ No: Ratio > 3:1?
   ├─ Yes: Moderate candidate, if query > 100ms → short TTL (30-120sec)
   └─ No: Skip; optimize query/indexes/pooling instead
```

</decision-tree>

<examples>
## Basic Cache Implementation

**Example 1: Cache-Aside Pattern**

```typescript
import { PrismaClient } from '@prisma/client';
import { Redis } from 'ioredis';

const prisma = new PrismaClient();
const redis = new Redis({
  host: process.env.REDIS_HOST,
  port: parseInt(process.env.REDIS_PORT || '6379'),
  maxRetriesPerRequest: 3,
});

async function getCachedUser(userId: string) {
  const cacheKey = `user:${userId}`;
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);

  const user = await prisma.user.findUnique({
    where: { id: userId },
    select: { id: true, email: true, name: true, role: true },
  });

  if (user) await redis.setex(cacheKey, 300, JSON.stringify(user));
  return user;
}
```

**Example 2: Consistent Key Generation**

```typescript
import crypto from 'crypto';

function generateCacheKey(entity: string, query: Record<string, unknown>): string {
  const sortedQuery = Object.keys(query)
    .sort()
    .reduce((acc, key) => {
      acc[key] = query[key];
      return acc;
    }, {} as Record<string, unknown>);

  const queryHash = crypto
    .createHash('sha256')
    .update(JSON.stringify(sortedQuery))
    .digest('hex')
    .slice(0, 16);
  return `${entity}:${queryHash}`;
}

async function getCachedPosts(filters: {
  authorId?: string;
  published?: boolean;
  tags?: string[];
}) {
  const cacheKey = generateCacheKey('posts', filters);
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);

  const posts = await prisma.post.findMany({
    where: filters,
    select: { id: true, title: true, createdAt: true },
  });

  await redis.setex(cacheKey, 120, JSON.stringify(posts));
  return posts;
}
```

**Example 3: Cache Invalidation on Mutation**

```typescript
async function updatePost(postId: string, data: { title?: string; content?: string }) {
  const post = await prisma.post.update({ where: { id: postId }, data });

  await Promise.all([
    redis.del(`post:${postId}`),
    redis.del(`posts:author:${post.authorId}`),
    redis.keys('posts:*').then((keys) => keys.length > 0 && redis.del(...keys)),
  ]);
  return post;
}
```

**Note:** redis.keys() with patterns is slow on large keysets; use SCAN or maintain key sets.

**Example 4: TTL Strategy**

```typescript
const TTL = {
  user_profile: 600,
  user_settings: 300,
  posts_list: 120,
  post_detail: 180,
  popular_posts: 60,
  real_time_stats: 10,
};

async function cacheWithTTL<T>(
  key: string,
  ttlType: keyof typeof TTL,
  fetchFn: () => Promise<T>
): Promise<T> {
  const cached = await redis.get(key);
  if (cached) return JSON.parse(cached);

  const data = await fetchFn();
  await redis.setex(key, TTL[ttlType], JSON.stringify(data));
  return data;
}
```

</examples>

<constraints>
**MUST:**
* Use cache-aside pattern (not cache-through)
* Consistent cache key generation (no random/timestamp components)
* Invalidate cache on all mutations affecting cached data
* Graceful Redis failure handling with database fallback
* JSON serialization (consistent with Prisma types)
* TTL on all cached values (never infinite)
* Thorough cache invalidation testing

**SHOULD:**

- Redis connection pooling (ioredis)
- Separate cache logic from business logic
- Monitor cache hit rates; adjust TTL accordingly
- Shorter TTL for frequently changing data
- Cache warming for predictably popular data
- Document cache key patterns and invalidation rules
- Use

Redis SCAN vs KEYS for pattern matching

**NEVER:**

- Cache authentication tokens or sensitive credentials
- Use infinite TTL
- Pattern-match invalidation in hot paths
- Cache Prisma queries with skip/take without pagination in key
- Assume cache always available
- Store Prisma instances directly (serialize first)
- Cache write-heavy data
  </constraints>

<validation>
**Cache Hit Rate:** Monitor >60% for effective caching; <40% signals strategy reconsideration or TTL adjustment.

**Invalidation Testing:** Verify all mutations invalidate correct keys; test cascading invalidation for related entities; confirm bulk operations invalidate list caches; ensure no stale data post-mutation.

**Performance:** Measure query latency with/without cache; target >50% latency reduction; monitor P95/P99 improvements; verify caching doesn't increase memory pressure.

**Redis Health:** Monitor connection pool utilization, memory usage (set maxmemory-policy), connection failures; test application behavior when Redis is unavailable.
</validation>

---

## References

- [Redis Configuration](./references/redis-configuration.md) — Connection setup, serverless
- [Invalidation Patterns](./references/invalidation-patterns.md) — Event-based, time-based, hybrid
- [Advanced Examples](./references/advanced-examples.md) — Bulk invalidation, cache warming
- [Common Pitfalls](./references/common-pitfalls.md) — Infinite TTL, key inconsistency, missing invalidation
