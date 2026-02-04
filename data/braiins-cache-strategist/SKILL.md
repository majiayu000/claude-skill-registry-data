---
name: braiins-cache-strategist
version: 1.0.0
category: performance
complexity: simple
status: active
created: 2025-12-18
author: braiins-pool-mcp-server

description: |
  Designs Redis caching strategies for Braiins API data, optimizing for
  data freshness vs. API rate limits and response latency.

triggers:
  - "design cache strategy"
  - "set TTL for"
  - "optimize caching"
  - "cache key pattern"
  - "Redis caching"
  - "cache configuration"

dependencies: []
---

# Braiins Cache Strategist Skill

## Description

Design Redis caching strategies optimized for Braiins Pool API data. This skill helps determine appropriate TTL values, cache key patterns, and invalidation strategies based on data volatility and API rate limits.

## When to Use This Skill

- When implementing caching for a new MCP tool
- When optimizing existing cache performance
- When designing cache key patterns
- When determining TTL values for different data types
- When planning cache invalidation strategies

## When NOT to Use This Skill

- When implementing cache client code (use Redis documentation)
- When designing tool handlers (use mcp-tool-builder)
- When debugging cache issues (use root-cause-tracing)

## Prerequisites

- Understanding of the data being cached
- Knowledge of API rate limits (from API.md)
- Redis is available in the environment

---

## TTL Strategy Matrix

Based on data volatility and API rate limits from API.md:

| Data Type | Resource | TTL | Rationale |
|-----------|----------|-----|-----------|
| **User Stats** | `/user/overview` | 30s | Hashrate changes frequently; users expect near real-time |
| **User Rewards** | `/user/rewards` | 60s | Historical data; less volatile |
| **Worker List** | `/workers` | 30s | Worker status can change rapidly |
| **Worker Detail** | `/workers/{id}` | 60s | Detailed metrics update less often |
| **Worker Hashrate** | `/workers/{id}/hashrate` | 120s | Historical timeseries; stable data |
| **Pool Stats** | `/pool/stats` | 60s | Pool-wide aggregations; moderate change rate |
| **Network Stats** | `/network/stats` | 300s | Bitcoin network changes slowly (10 min blocks) |

**Rate Limit Consideration**: API.md specifies 1 request/30s for user endpoints. Cache TTLs are set to match or exceed this to prevent hitting rate limits.

---

## Cache Key Patterns

### Pattern Structure

```
braiins:{resource_type}:{scope}:{identifier}:{filter_hash}
```

Components:
- **braiins**: Namespace prefix
- **resource_type**: API resource (user, workers, pool, network)
- **scope**: Account scope (usually account hash)
- **identifier**: Specific resource ID
- **filter_hash**: Optional hash of filter/query params

### Standard Patterns

```
# User overview (no identifier needed, scoped by auth token)
braiins:user:overview:{accountHash}

# User rewards with time range
braiins:user:rewards:{accountHash}:{paramsHash}

# Worker list (paginated, filtered)
braiins:workers:list:{accountHash}:p{page}:{filtersHash}

# Worker detail
braiins:workers:detail:{accountHash}:{workerId}

# Worker hashrate timeseries
braiins:workers:hashrate:{accountHash}:{workerId}:{paramsHash}

# Pool stats (global, no scope)
braiins:pool:stats

# Network stats (global, no scope)
braiins:network:stats
```

### Account Hash Generation

Never use raw API tokens or account IDs in cache keys:

```typescript
import crypto from 'crypto';

function generateAccountHash(apiToken: string): string {
  // Use first 8 chars of SHA256 hash
  return crypto
    .createHash('sha256')
    .update(apiToken)
    .digest('hex')
    .substring(0, 8);
}

// Usage:
// Token: "sk_live_abc123..." -> Hash: "a7f2b9c1"
// Key: "braiins:user:overview:a7f2b9c1"
```

### Filter Hash Generation

For requests with variable query parameters:

```typescript
function generateFilterHash(params: Record<string, unknown>): string {
  const sortedJson = JSON.stringify(
    Object.keys(params)
      .sort()
      .reduce((acc, key) => {
        acc[key] = params[key];
        return acc;
      }, {} as Record<string, unknown>)
  );

  return crypto
    .createHash('sha256')
    .update(sortedJson)
    .digest('hex')
    .substring(0, 8);
}

// Usage:
// { status: "active", sortBy: "hashrate" } -> "b3c4d5e6"
// Key: "braiins:workers:list:a7f2b9c1:p1:b3c4d5e6"
```

---

## Cache Key Security

### Key Sanitization Rules

**Rule 1**: Never include raw user input directly in keys
```typescript
// BAD: Direct user input
const key = `braiins:worker:${userInput.workerId}`;

// GOOD: Sanitize first
const sanitizedId = workerId.replace(/[^a-zA-Z0-9\-_]/g, '');
const key = `braiins:worker:${sanitizedId}`;
```

**Rule 2**: Maximum key length
```typescript
const MAX_KEY_LENGTH = 200;

function createCacheKey(parts: string[]): string {
  const key = parts.join(':');
  if (key.length > MAX_KEY_LENGTH) {
    // Hash the key if too long
    const hash = crypto.createHash('sha256').update(key).digest('hex');
    return `braiins:hashed:${hash}`;
  }
  return key;
}
```

**Rule 3**: Character allowlist
```typescript
const VALID_KEY_CHARS = /^[a-zA-Z0-9:\-_]+$/;

function validateCacheKey(key: string): boolean {
  return VALID_KEY_CHARS.test(key) && key.length <= MAX_KEY_LENGTH;
}
```

---

## Caching Workflow

### Step 1: Determine Data Category

| Category | Characteristics | Base TTL |
|----------|-----------------|----------|
| **Real-time** | Changes every second | 15-30s |
| **Near real-time** | Changes every minute | 30-60s |
| **Historical** | Changes hourly/daily | 120-300s |
| **Static** | Rarely changes | 3600s+ |

### Step 2: Consider Rate Limits

From API.md Section 9:
- User endpoints: 1 req/30s
- Worker list: 1 req/30s
- Worker detail: 1 req/60-120s
- Pool/network: 1 req/60s

**Rule**: Cache TTL >= API rate limit interval

### Step 3: Design Key Pattern

```typescript
interface CacheKeyConfig {
  resource: string;
  scope: 'global' | 'account' | 'worker';
  identifiers: string[];
  hasFilters: boolean;
}

function designCacheKey(config: CacheKeyConfig): string {
  const parts = ['braiins', config.resource];

  if (config.scope === 'account') {
    parts.push('{accountHash}');
  }

  parts.push(...config.identifiers);

  if (config.hasFilters) {
    parts.push('{filtersHash}');
  }

  return parts.join(':');
}
```

### Step 4: Document Strategy

Create entry in cache configuration:

```typescript
// src/cache/cacheConfig.ts
export const CACHE_CONFIG = {
  userOverview: {
    keyPattern: 'braiins:user:overview:{accountHash}',
    ttl: 30,
    description: 'User hashrate, rewards, worker counts',
    invalidateOn: ['manual_refresh', 'payout_received'],
  },

  workerDetail: {
    keyPattern: 'braiins:workers:detail:{accountHash}:{workerId}',
    ttl: 60,
    description: 'Individual worker status and metrics',
    invalidateOn: ['worker_status_change', 'manual_refresh'],
  },

  poolStats: {
    keyPattern: 'braiins:pool:stats',
    ttl: 60,
    description: 'Global pool statistics',
    invalidateOn: ['new_block_found'],
  },
} as const;
```

---

## Cache Implementation Patterns

### Pattern 1: Cache-First with Fallthrough

```typescript
async function getWithCache<T>(
  cacheKey: string,
  ttl: number,
  fetchFn: () => Promise<T>,
): Promise<T> {
  // Try cache first
  try {
    const cached = await redisManager.get<T>(cacheKey);
    if (cached !== null) {
      logger.debug('Cache hit', { key: cacheKey });
      return cached;
    }
  } catch (cacheError) {
    logger.warn('Cache read failed, falling through to API', { error: cacheError });
  }

  // Cache miss - fetch from API
  logger.debug('Cache miss', { key: cacheKey });
  const data = await fetchFn();

  // Store in cache (don't fail on cache errors)
  try {
    await redisManager.set(cacheKey, data, ttl);
  } catch (cacheError) {
    logger.warn('Cache write failed', { error: cacheError });
  }

  return data;
}
```

### Pattern 2: Stale-While-Revalidate

For near-real-time data where some staleness is acceptable:

```typescript
interface CachedData<T> {
  data: T;
  cachedAt: number;
  ttl: number;
}

async function getWithStaleWhileRevalidate<T>(
  cacheKey: string,
  ttl: number,
  staleThreshold: number, // Additional seconds to serve stale data
  fetchFn: () => Promise<T>,
): Promise<T> {
  const cached = await redisManager.get<CachedData<T>>(cacheKey);

  if (cached) {
    const age = Date.now() - cached.cachedAt;
    const isStale = age > cached.ttl * 1000;
    const isTooStale = age > (cached.ttl + staleThreshold) * 1000;

    if (!isStale) {
      // Fresh data
      return cached.data;
    }

    if (!isTooStale) {
      // Stale but acceptable - return and revalidate in background
      setImmediate(async () => {
        try {
          const fresh = await fetchFn();
          await redisManager.set(cacheKey, {
            data: fresh,
            cachedAt: Date.now(),
            ttl,
          });
        } catch (error) {
          logger.warn('Background revalidation failed', { error });
        }
      });
      return cached.data;
    }
  }

  // No cache or too stale - must fetch
  const data = await fetchFn();
  await redisManager.set(cacheKey, {
    data,
    cachedAt: Date.now(),
    ttl,
  });
  return data;
}
```

### Pattern 3: Cache Invalidation

```typescript
async function invalidateCache(pattern: string): Promise<number> {
  // Get all keys matching pattern
  const keys = await redisManager.keys(pattern);

  if (keys.length === 0) {
    return 0;
  }

  // Delete all matching keys
  await redisManager.del(...keys);

  logger.info('Cache invalidated', { pattern, count: keys.length });
  return keys.length;
}

// Usage:
// Invalidate all worker data for an account
await invalidateCache('braiins:workers:*:a7f2b9c1:*');

// Invalidate specific worker
await invalidateCache('braiins:workers:*:a7f2b9c1:worker-123');

// Invalidate all pool stats
await invalidateCache('braiins:pool:*');
```

---

## Quality Checklist

When designing cache strategy for a new endpoint:

- [ ] TTL is >= API rate limit interval
- [ ] Cache key includes all discriminating parameters
- [ ] User input in keys is sanitized/hashed
- [ ] Key length is <= 200 characters
- [ ] Fallthrough to API on cache errors
- [ ] Cache errors don't break the request
- [ ] Invalidation strategy is documented
- [ ] Metrics are logged (hit/miss rates)

---

## Examples

### Example 1: getUserOverview Caching

**Data Characteristics**:
- Real-time hashrate data
- Changes every few seconds
- One per authenticated user
- No query parameters

**Cache Design**:
```typescript
// Cache configuration
const config = {
  keyPattern: 'braiins:user:overview:{accountHash}',
  ttl: 30, // 30 seconds (matches rate limit)
  scope: 'account',
};

// Implementation
async function getUserOverview(accountHash: string): Promise<UserOverview> {
  const cacheKey = `braiins:user:overview:${accountHash}`;

  return getWithCache(
    cacheKey,
    30,
    () => braiinsClient.getUserOverview(),
  );
}
```

---

### Example 2: listWorkers Caching with Filters

**Data Characteristics**:
- Paginated list
- Filterable by status, search, sort
- Changes when workers connect/disconnect

**Cache Design**:
```typescript
// Cache configuration
const config = {
  keyPattern: 'braiins:workers:list:{accountHash}:p{page}:{filtersHash}',
  ttl: 30,
  scope: 'account',
};

// Implementation
async function listWorkers(
  accountHash: string,
  params: ListWorkersInput,
): Promise<WorkerList> {
  const { page, pageSize, ...filters } = params;
  const filtersHash = generateFilterHash(filters);
  const cacheKey = `braiins:workers:list:${accountHash}:p${page}:${filtersHash}`;

  return getWithCache(
    cacheKey,
    30,
    () => braiinsClient.listWorkers(params),
  );
}
```

---

### Example 3: getNetworkStats Caching (Global)

**Data Characteristics**:
- Global Bitcoin network data
- Same for all users
- Changes with network difficulty/blocks
- Very stable (block time ~10 minutes)

**Cache Design**:
```typescript
// Cache configuration
const config = {
  keyPattern: 'braiins:network:stats',
  ttl: 300, // 5 minutes
  scope: 'global',
};

// Implementation
async function getNetworkStats(): Promise<NetworkStats> {
  const cacheKey = 'braiins:network:stats';

  // Use stale-while-revalidate for better UX
  return getWithStaleWhileRevalidate(
    cacheKey,
    300,    // TTL: 5 minutes
    60,     // Serve stale for 1 more minute
    () => braiinsClient.getNetworkStats(),
  );
}
```

---

## Common Pitfalls

**Pitfall 1: TTL shorter than rate limit**
```typescript
// BAD: Will hit rate limits
ttl: 15 // API rate limit is 30s

// GOOD: Respects rate limits
ttl: 30 // Matches API rate limit
```

**Pitfall 2: Forgetting filter parameters in key**
```typescript
// BAD: Different filters return same cached data
const key = `braiins:workers:list:${accountHash}`;

// GOOD: Include filter state
const key = `braiins:workers:list:${accountHash}:${filtersHash}`;
```

**Pitfall 3: Raw tokens in cache keys**
```typescript
// BAD: Security risk - token in key
const key = `braiins:user:${apiToken}`;

// GOOD: Hash the token
const key = `braiins:user:${hashToken(apiToken)}`;
```

**Pitfall 4: Failing request on cache errors**
```typescript
// BAD: Cache error breaks the request
const cached = await redis.get(key); // Throws if Redis down

// GOOD: Fallthrough on cache errors
try {
  const cached = await redis.get(key);
  if (cached) return cached;
} catch {
  // Continue to API call
}
```

---

## Version History

- **1.0.0** (2025-12-18): Initial skill definition

---

## References

- [API.md Section 9](../../../API.md#9-rate-limiting--caching) - Rate limiting specs
- [ARCHITECTURE.md](../../../ARCHITECTURE.md) - Caching layer design
- [Redis Best Practices](https://redis.io/docs/manual/patterns/)
