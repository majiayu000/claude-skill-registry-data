---
name: redis-caching-patterns
version: 1.0.0
category: technical
description: Redis caching strategies for MCP servers - cache invalidation, TTL management, pub/sub patterns, and performance optimization
triggers:
  - "Redis caching"
  - "cache strategy"
  - "cache invalidation"
  - "TTL management"
  - "Redis pub/sub"
  - "cache performance"
dependencies:
  - mcp-server-dev
author: Engineering Standards Committee
last_updated: 2025-12-29
---

# Redis Caching Patterns Skill

## Description

This skill provides battle-tested Redis caching strategies for high-performance MCP servers managing fleet-scale operations. It covers intelligent cache invalidation, TTL optimization, real-time pub/sub patterns, and performance monitoring.

**Core Capabilities:**
- Cache invalidation strategies (time-based, event-based, manual)
- TTL optimization for different data types (ephemeral vs persistent)
- Pub/sub patterns for real-time agent notifications
- Cache-aside, write-through, and read-through patterns
- Performance monitoring and cache hit ratio optimization
- Distributed caching for multi-instance MCP servers

---

## When to Use This Skill

**Use this skill when you need to:**
- Design caching strategies for MCP resources or tools
- Optimize performance for fleet-scale operations (100+ miners)
- Implement real-time updates via Redis pub/sub
- Reduce gRPC call overhead with intelligent caching
- Handle cache invalidation when data changes
- Monitor cache effectiveness and tune TTLs

**Trigger Phrases:**
- "Design cache strategy for fleet metrics"
- "Implement Redis caching for miner status"
- "Add pub/sub for real-time updates"
- "Optimize cache TTL for this data"
- "Handle cache invalidation when config changes"

**Don't use this skill for:**
- In-memory caching (use Map or LRU cache instead)
- Session storage (use Redis but different patterns)
- Message queuing (use Bull or BullMQ instead)
- Database replacement (cache is supplementary)

---

## Prerequisites

### Knowledge Requirements
1. **Redis Fundamentals**
   - Key-value storage and data structures
   - TTL (time-to-live) and expiration
   - Pub/sub messaging patterns
   - Redis commands (GET, SET, SETEX, DEL, PUBLISH, SUBSCRIBE)

2. **Caching Theory**
   - Cache-aside (lazy loading) pattern
   - Write-through vs write-back caching
   - Cache invalidation strategies
   - Cache stampede prevention

3. **MCP Server Architecture**
   - Resource caching needs (see mcp-server-dev skill)
   - Tool optimization opportunities
   - Real-time update requirements

### Environment Setup
```typescript
// Required dependencies
{
  "ioredis": "^5.3.2",
  "@types/ioredis": "^5.0.0"
}
```

### Project Context
- Understanding of data access patterns (read-heavy vs write-heavy)
- Knowledge of data freshness requirements
- Integration points with gRPC client (see grpc-client-dev skill)

---

## Workflow

### Phase 1: Cache Strategy Design

#### 1.1 Data Classification

**Pattern: Classify Data by Caching Characteristics**

```typescript
// src/cache/cache-strategy.ts

export enum CacheStrategy {
  // Short TTL: Data changes frequently (5-30 seconds)
  EPHEMERAL = 'EPHEMERAL',

  // Medium TTL: Data changes occasionally (1-5 minutes)
  MODERATE = 'MODERATE',

  // Long TTL: Data rarely changes (10-60 minutes)
  STABLE = 'STABLE',

  // Event-based: Invalidate on specific events
  EVENT_DRIVEN = 'EVENT_DRIVEN',

  // No cache: Always fetch fresh
  NO_CACHE = 'NO_CACHE'
}

export interface CacheConfig {
  strategy: CacheStrategy;
  ttl: number; // seconds
  invalidateOn?: string[]; // Event names
  namespace: string; // Key prefix
}

// Example: Fleet data classification
const CACHE_CONFIGS: Record<string, CacheConfig> = {
  'miner:status': {
    strategy: CacheStrategy.EPHEMERAL,
    ttl: 10, // 10 seconds
    namespace: 'cache:miner:status'
  },
  'fleet:summary': {
    strategy: CacheStrategy.EPHEMERAL,
    ttl: 30, // 30 seconds
    namespace: 'cache:fleet'
  },
  'miner:config': {
    strategy: CacheStrategy.EVENT_DRIVEN,
    ttl: 300, // 5 minutes fallback
    invalidateOn: ['miner:config:updated'],
    namespace: 'cache:miner:config'
  },
  'firmware:versions': {
    strategy: CacheStrategy.STABLE,
    ttl: 3600, // 1 hour
    namespace: 'cache:firmware'
  }
};
```

**Decision Matrix:**

| Data Type | Change Frequency | Read Pattern | Recommended Strategy | TTL |
|-----------|------------------|--------------|---------------------|-----|
| Miner status | Every 1-5s | Very high (100+ req/s) | EPHEMERAL | 10s |
| Fleet metrics | Every 10-30s | High (10-50 req/s) | EPHEMERAL | 30s |
| Miner config | On update | Medium (1-10 req/s) | EVENT_DRIVEN | 5m |
| Firmware list | Daily | Low (<1 req/s) | STABLE | 1h |
| Pool URLs | Rarely | Low | STABLE | 12h |

#### 1.2 Key Naming Convention

**Pattern: Hierarchical Namespace with Versioning**

```typescript
// src/cache/keys.ts

export class CacheKeys {
  private static VERSION = 'v1';

  /**
   * Generate cache key for miner status
   */
  static minerStatus(minerId: string): string {
    return `${this.VERSION}:cache:miner:${minerId}:status`;
  }

  /**
   * Generate cache key for fleet summary
   */
  static fleetSummary(tenantId?: string): string {
    const tenant = tenantId || 'global';
    return `${this.VERSION}:cache:fleet:${tenant}:summary`;
  }

  /**
   * Generate cache key for miner config
   */
  static minerConfig(minerId: string): string {
    return `${this.VERSION}:cache:miner:${minerId}:config`;
  }

  /**
   * Generate pattern for deleting all miner keys
   */
  static minerPattern(minerId: string): string {
    return `${this.VERSION}:cache:miner:${minerId}:*`;
  }

  /**
   * Generate pattern for fleet keys
   */
  static fleetPattern(tenantId?: string): string {
    const tenant = tenantId || '*';
    return `${this.VERSION}:cache:fleet:${tenant}:*`;
  }
}
```

**Rationale:**
- **Version prefix**: Allows global cache invalidation by bumping version
- **Hierarchical structure**: Enables pattern-based deletion
- **Scoped by entity**: Easy to invalidate all keys for a miner/fleet
- **No colons in IDs**: Prevents key conflicts

---

### Phase 2: Cache Implementation Patterns

#### 2.1 Cache-Aside (Lazy Loading)

**Pattern: Read-Through with Fallback**

```typescript
// src/cache/cache-aside.ts
import Redis from 'ioredis';

export class CacheAsideService {
  constructor(private redis: Redis) {}

  /**
   * Get from cache with fallback to source
   */
  async getOrFetch<T>(
    key: string,
    fetchFn: () => Promise<T>,
    ttl: number
  ): Promise<T> {
    // Try cache first
    const cached = await this.redis.get(key);

    if (cached) {
      try {
        return JSON.parse(cached) as T;
      } catch (error) {
        // Invalid JSON in cache, fall through to fetch
        await this.redis.del(key);
      }
    }

    // Cache miss - fetch from source
    const data = await fetchFn();

    // Store in cache with TTL
    await this.redis.setex(
      key,
      ttl,
      JSON.stringify(data)
    );

    return data;
  }

  /**
   * Get miner status with cache-aside pattern
   */
  async getMinerStatus(
    minerId: string,
    fetchStatus: () => Promise<MinerStatus>
  ): Promise<MinerStatus> {
    return this.getOrFetch(
      CacheKeys.minerStatus(minerId),
      fetchStatus,
      10 // 10 second TTL
    );
  }
}
```

**Usage in MCP Resource:**
```typescript
// Example: MCP resource using cache-aside
@resource({
  uri: "braiins:///miner/{minerId}/status",
  mimeType: "application/json"
})
async getMinerStatus(minerId: string): Promise<MinerStatus> {
  return this.cacheService.getMinerStatus(minerId, async () => {
    // Only called on cache miss
    const status = await this.grpcClient.getStatus(minerId);
    return status;
  });
}
```

#### 2.2 Write-Through Caching

**Pattern: Update Cache on Write**

```typescript
// src/cache/write-through.ts

export class WriteThroughService {
  constructor(
    private redis: Redis,
    private repository: MinerRepository
  ) {}

  /**
   * Update miner config with write-through
   */
  async updateMinerConfig(
    minerId: string,
    config: MinerConfig
  ): Promise<void> {
    // Write to source of truth (database)
    await this.repository.update(minerId, config);

    // Update cache immediately
    const key = CacheKeys.minerConfig(minerId);
    await this.redis.setex(
      key,
      300, // 5 minute TTL
      JSON.stringify(config)
    );
  }

  /**
   * Read with guaranteed fresh data
   */
  async getMinerConfig(minerId: string): Promise<MinerConfig | null> {
    const key = CacheKeys.minerConfig(minerId);
    const cached = await this.redis.get(key);

    if (cached) {
      return JSON.parse(cached) as MinerConfig;
    }

    // Cache miss - fetch and populate
    const config = await this.repository.findById(minerId);
    if (config) {
      await this.redis.setex(key, 300, JSON.stringify(config));
    }

    return config;
  }
}
```

#### 2.3 Event-Based Invalidation

**Pattern: Invalidate on Data Change**

```typescript
// src/cache/invalidation.ts

export class CacheInvalidationService {
  constructor(private redis: Redis) {}

  /**
   * Invalidate miner-related caches
   */
  async invalidateMiner(minerId: string): Promise<void> {
    const keys = [
      CacheKeys.minerStatus(minerId),
      CacheKeys.minerConfig(minerId)
    ];

    await this.redis.del(...keys);
  }

  /**
   * Invalidate all fleet caches
   */
  async invalidateFleet(tenantId?: string): Promise<void> {
    const pattern = CacheKeys.fleetPattern(tenantId);

    // Find all matching keys
    const keys = await this.scanKeys(pattern);

    if (keys.length > 0) {
      await this.redis.del(...keys);
    }
  }

  /**
   * Scan for keys matching pattern (cursor-based to avoid blocking)
   */
  private async scanKeys(pattern: string): Promise<string[]> {
    const keys: string[] = [];
    let cursor = '0';

    do {
      const [nextCursor, batch] = await this.redis.scan(
        cursor,
        'MATCH',
        pattern,
        'COUNT',
        100
      );

      cursor = nextCursor;
      keys.push(...batch);
    } while (cursor !== '0');

    return keys;
  }
}

// Integration with repository
export class MinerRepository {
  async update(minerId: string, data: Partial<MinerEntity>): Promise<MinerEntity> {
    // Update database
    const updated = await this.db.update(minerId, data);

    // Invalidate caches
    await this.cacheInvalidation.invalidateMiner(minerId);
    await this.cacheInvalidation.invalidateFleet(); // Fleet metrics include this miner

    return updated;
  }
}
```

---

### Phase 3: Redis Pub/Sub for Real-Time Updates

#### 3.1 Publisher Pattern

**Pattern: Publish Events on Data Change**

```typescript
// src/cache/publisher.ts

export class CacheEventPublisher {
  constructor(private redis: Redis) {}

  /**
   * Publish miner status update
   */
  async publishMinerStatus(minerId: string, status: MinerStatus): Promise<void> {
    const channel = `events:miner:${minerId}:status`;
    const message = JSON.stringify({
      minerId,
      status,
      timestamp: new Date().toISOString()
    });

    await this.redis.publish(channel, message);
  }

  /**
   * Publish fleet-wide event
   */
  async publishFleetEvent(event: string, data: unknown): Promise<void> {
    const channel = 'events:fleet';
    const message = JSON.stringify({
      event,
      data,
      timestamp: new Date().toISOString()
    });

    await this.redis.publish(channel, message);
  }
}

// Usage in gRPC stream handler
export class MinerStatusStream {
  async handleStatusUpdate(minerId: string, status: MinerStatus): Promise<void> {
    // Update cache
    const key = CacheKeys.minerStatus(minerId);
    await this.redis.setex(key, 30, JSON.stringify(status));

    // Publish event for real-time subscribers
    await this.publisher.publishMinerStatus(minerId, status);
  }
}
```

#### 3.2 Subscriber Pattern

**Pattern: Subscribe to Events for Real-Time MCP Resources**

```typescript
// src/cache/subscriber.ts

export class CacheEventSubscriber {
  private subscriber: Redis;
  private handlers: Map<string, ((message: string) => void)[]> = new Map();

  constructor(redisConfig: RedisOptions) {
    // Create dedicated Redis connection for pub/sub
    this.subscriber = new Redis(redisConfig);
  }

  /**
   * Subscribe to miner status events
   */
  async subscribeMinerStatus(
    minerId: string,
    handler: (status: MinerStatus) => void
  ): Promise<void> {
    const channel = `events:miner:${minerId}:status`;

    if (!this.handlers.has(channel)) {
      await this.subscriber.subscribe(channel);

      this.subscriber.on('message', (ch, message) => {
        if (ch === channel) {
          const handlers = this.handlers.get(channel) || [];
          handlers.forEach(h => h(message));
        }
      });
    }

    const handlers = this.handlers.get(channel) || [];
    handlers.push((message: string) => {
      try {
        const parsed = JSON.parse(message);
        handler(parsed.status);
      } catch (error) {
        console.error('Failed to parse status message:', error);
      }
    });
    this.handlers.set(channel, handlers);
  }

  /**
   * Unsubscribe from channel
   */
  async unsubscribe(channel: string): Promise<void> {
    await this.subscriber.unsubscribe(channel);
    this.handlers.delete(channel);
  }

  /**
   * Dispose all subscriptions
   */
  async dispose(): Promise<void> {
    for (const channel of this.handlers.keys()) {
      await this.subscriber.unsubscribe(channel);
    }
    this.handlers.clear();
    await this.subscriber.quit();
  }
}
```

---

### Phase 4: Performance Optimization

#### 4.1 Cache Stampede Prevention

**Pattern: Single-Flight for Expensive Operations**

```typescript
// src/cache/single-flight.ts

export class SingleFlightCache {
  private inflightRequests: Map<string, Promise<unknown>> = new Map();

  constructor(private redis: Redis) {}

  /**
   * Ensure only one request fetches data at a time
   */
  async getOrFetchSingleFlight<T>(
    key: string,
    fetchFn: () => Promise<T>,
    ttl: number
  ): Promise<T> {
    // Check cache first
    const cached = await this.redis.get(key);
    if (cached) {
      return JSON.parse(cached) as T;
    }

    // Check if fetch is already in progress
    const inflight = this.inflightRequests.get(key);
    if (inflight) {
      return inflight as Promise<T>;
    }

    // Start fetch and store promise
    const fetchPromise = (async () => {
      try {
        const data = await fetchFn();
        await this.redis.setex(key, ttl, JSON.stringify(data));
        return data;
      } finally {
        this.inflightRequests.delete(key);
      }
    })();

    this.inflightRequests.set(key, fetchPromise);
    return fetchPromise;
  }
}
```

#### 4.2 Cache Warming

**Pattern: Proactive Cache Population**

```typescript
// src/cache/warming.ts

export class CacheWarmingService {
  constructor(
    private redis: Redis,
    private minerRepo: MinerRepository,
    private grpcClient: BraiinsMinerClient
  ) {}

  /**
   * Warm cache for all active miners
   */
  async warmMinerCaches(): Promise<void> {
    const miners = await this.minerRepo.findAll({ status: 'active' });

    // Warm in parallel with controlled concurrency
    const concurrency = 10;
    for (let i = 0; i < miners.data.length; i += concurrency) {
      const batch = miners.data.slice(i, i + concurrency);

      await Promise.allSettled(
        batch.map(miner => this.warmMinerCache(miner.id))
      );
    }
  }

  /**
   * Warm cache for a specific miner
   */
  private async warmMinerCache(minerId: string): Promise<void> {
    try {
      const status = await this.grpcClient.getMinerStatus(minerId);

      const key = CacheKeys.minerStatus(minerId);
      await this.redis.setex(key, 30, JSON.stringify(status));
    } catch (error) {
      console.error(`Failed to warm cache for ${minerId}:`, error);
    }
  }

  /**
   * Schedule periodic cache warming
   */
  startPeriodicWarming(intervalMs: number = 60000): NodeJS.Timer {
    return setInterval(() => {
      void this.warmMinerCaches();
    }, intervalMs);
  }
}
```

#### 4.3 Monitoring and Metrics

**Pattern: Track Cache Performance**

```typescript
// src/cache/metrics.ts

export class CacheMetrics {
  private hits: number = 0;
  private misses: number = 0;
  private errors: number = 0;

  recordHit(): void {
    this.hits++;
  }

  recordMiss(): void {
    this.misses++;
  }

  recordError(): void {
    this.errors++;
  }

  getHitRatio(): number {
    const total = this.hits + this.misses;
    return total > 0 ? this.hits / total : 0;
  }

  getStats(): CacheStats {
    return {
      hits: this.hits,
      misses: this.misses,
      errors: this.errors,
      hitRatio: this.getHitRatio(),
      total: this.hits + this.misses
    };
  }

  reset(): void {
    this.hits = 0;
    this.misses = 0;
    this.errors = 0;
  }
}

// Instrumented cache service
export class InstrumentedCacheService {
  private metrics = new CacheMetrics();

  async get<T>(key: string): Promise<T | null> {
    try {
      const value = await this.redis.get(key);

      if (value) {
        this.metrics.recordHit();
        return JSON.parse(value) as T;
      } else {
        this.metrics.recordMiss();
        return null;
      }
    } catch (error) {
      this.metrics.recordError();
      throw error;
    }
  }

  getMetrics(): CacheStats {
    return this.metrics.getStats();
  }
}
```

---

## Examples

### Example 1: Complete MCP Resource with Caching

```typescript
// src/mcp/resources/fleet-summary.ts

@resource({
  uri: "braiins:///fleet/summary",
  name: "Fleet Summary",
  description: "Aggregated metrics for all managed miners",
  mimeType: "application/json"
})
async getFleetSummary(tenantId?: string): Promise<FleetSummary> {
  return this.singleFlightCache.getOrFetchSingleFlight(
    CacheKeys.fleetSummary(tenantId),
    async () => {
      // Expensive operation - aggregates data from all miners
      const miners = await this.minerRepo.findByTenant(tenantId);

      const summary = {
        totalMiners: miners.length,
        onlineMiners: miners.filter(m => m.online).length,
        totalHashrate: miners.reduce((sum, m) => sum + m.hashrate, 0),
        avgTemperature: miners.reduce((sum, m) => sum + m.temperature, 0) / miners.length
      };

      return summary;
    },
    30 // 30 second TTL
  );
}
```

### Example 2: Real-Time Updates via Pub/Sub

```typescript
// src/mcp/resources/miner-status-stream.ts

@resource({
  uri: "braiins:///miner/{minerId}/status/stream",
  name: "Miner Status Stream",
  mimeType: "application/json"
})
async getMinerStatusStream(minerId: string): Promise<AsyncIterable<MinerStatus>> {
  const channel = `events:miner:${minerId}:status`;
  let subscriber: Redis;

  return {
    [Symbol.asyncIterator]() {
      return {
        async next() {
          if (!subscriber) {
            subscriber = new Redis(redisConfig);
            await subscriber.subscribe(channel);
          }

          return new Promise((resolve) => {
            subscriber.once('message', (ch, message) => {
              if (ch === channel) {
                const status = JSON.parse(message).status;
                resolve({ value: status, done: false });
              }
            });
          });
        },
        async return() {
          if (subscriber) {
            await subscriber.unsubscribe(channel);
            await subscriber.quit();
          }
          return { value: undefined, done: true };
        }
      };
    }
  };
}
```

---

## Quality Standards

### Cache Implementation Checklist

- [ ] **TTL Configuration**
  - [ ] TTLs are appropriate for data change frequency
  - [ ] No infinite TTLs (always expire eventually)
  - [ ] Different TTLs for different data types

- [ ] **Invalidation**
  - [ ] Event-based invalidation for mutable data
  - [ ] Pattern-based deletion uses SCAN (not KEYS)
  - [ ] Cascade invalidation (miner → fleet)

- [ ] **Performance**
  - [ ] Cache stampede prevention implemented
  - [ ] Parallel operations use Promise.allSettled
  - [ ] Connection pooling for Redis (ioredis default)

- [ ] **Monitoring**
  - [ ] Cache hit ratio tracked
  - [ ] Metrics logged periodically
  - [ ] Target: >80% hit ratio for ephemeral data

- [ ] **Error Handling**
  - [ ] Redis errors don't break application
  - [ ] Fallback to source on cache failure
  - [ ] Errors logged for debugging

---

## Common Pitfalls

### ❌ Pitfall 1: Using KEYS for Pattern Deletion

**Problem**: KEYS blocks Redis and causes timeouts

```typescript
// BAD: Blocks Redis
const keys = await redis.keys('cache:miner:*');
await redis.del(...keys);
```

**Solution**: Use SCAN with cursor

```typescript
// GOOD: Non-blocking scan
async function deletePattern(pattern: string): Promise<void> {
  let cursor = '0';
  do {
    const [nextCursor, keys] = await redis.scan(cursor, 'MATCH', pattern, 'COUNT', 100);
    cursor = nextCursor;
    if (keys.length > 0) {
      await redis.del(...keys);
    }
  } while (cursor !== '0');
}
```

### ❌ Pitfall 2: Cache Stampede on Popular Keys

**Problem**: Many requests simultaneously fetch same data

```typescript
// BAD: Every request fetches on cache miss
const cached = await redis.get(key);
if (!cached) {
  // 100 requests simultaneously call expensive fetchData()
  const data = await fetchData();
  await redis.set(key, JSON.stringify(data));
}
```

**Solution**: Use single-flight pattern

```typescript
// GOOD: Only one request fetches
return singleFlightCache.getOrFetchSingleFlight(key, fetchData, ttl);
```

### ❌ Pitfall 3: Forgetting to Invalidate on Update

**Problem**: Stale data served after updates

```typescript
// BAD: Cache not invalidated
async function updateMiner(minerId: string, config: MinerConfig) {
  await db.update(minerId, config);
  // Cache still has old data!
}
```

**Solution**: Always invalidate on write

```typescript
// GOOD: Write-through with invalidation
async function updateMiner(minerId: string, config: MinerConfig) {
  await db.update(minerId, config);
  await redis.del(CacheKeys.minerConfig(minerId));
  await redis.del(CacheKeys.fleetSummary()); // Cascade
}
```

---

## Integration with MCP Server

### Complete Caching Layer

```typescript
// src/cache/index.ts - Central caching service

export class MCPCacheService {
  private cacheAside: CacheAsideService;
  private writeThrough: WriteThroughService;
  private invalidation: CacheInvalidationService;
  private singleFlight: SingleFlightCache;
  private publisher: CacheEventPublisher;
  private subscriber: CacheEventSubscriber;
  private metrics: InstrumentedCacheService;

  constructor(redis: Redis) {
    this.cacheAside = new CacheAsideService(redis);
    this.writeThrough = new WriteThroughService(redis, minerRepo);
    this.invalidation = new CacheInvalidationService(redis);
    this.singleFlight = new SingleFlightCache(redis);
    this.publisher = new CacheEventPublisher(redis);
    this.subscriber = new CacheEventSubscriber(redisConfig);
    this.metrics = new InstrumentedCacheService(redis);
  }

  // Expose all caching patterns through unified interface
}
```

---

## References

- **Redis Documentation**: https://redis.io/docs/
- **ioredis Library**: https://github.com/redis/ioredis
- **Caching Best Practices**: https://aws.amazon.com/caching/best-practices/
- **MCP Server Integration**: See `.claude/skills/mcp-server-dev/` skill
- **gRPC Client Caching**: See `.claude/skills/grpc-client-dev/` skill

---

**Version History**:
- 1.0.0 (2025-12-29): Initial release - Cache patterns, pub/sub, performance optimization
