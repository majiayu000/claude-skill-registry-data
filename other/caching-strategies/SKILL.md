---
name: caching-strategies
description: When improving read performance and reducing database load.
version: 2.0.0
category: architecture
tags: [architecture, performance, caching]
skill_type: architecture
author: skiLLM
license: MIT
compatible_agents: [claude-code, cursor, copilot, codex]
estimated_context_tokens: 1800
dangerous: false
requires_review: false
security_level: safe
dependencies: [database-query-optimization]
triggers: [performance, latency, database load, cache, redis]
permissions:
  filesystem: { read: true, write: true }
  network: { outbound: true }
  shell: { execute: true }
input_requirements: [slow read endpoints, cache infrastructure]
output_contract: [cache never source of truth, always has fallback, ttl enforced]
failure_conditions: [cache becomes source of truth, no fallback logic, infinite ttl]
last_updated: 2026-05-15
---

# Caching Strategies

## Purpose
Databases are slow; caches are fast. This skill teaches teams to strategically cache frequently accessed data in fast storage (Redis, Memcached) to intercept requests before they hit the database, dramatically reducing latency and database load. Caching is NOT a substitute for proper database optimization.

## When to use
- System is experiencing high latency on read-heavy API endpoints
- Database CPU/Memory usage is constantly peaking due to repeated queries
- Designing a new system expecting massive read throughput
- Content rarely changes but reads happen constantly

## When NOT to use
- Before optimizing database queries (optimize first, cache second)
- For data that changes frequently or is highly personalized
- When consistency is more important than performance
- As a quick fix for poor application architecture

## Inputs required
- Slow query logs or endpoint metrics
- Cache infrastructure (Redis, Memcached)
- Read/write patterns of the data
- Acceptable staleness window (TTL)

## Workflow
1. **Identify Bottlenecks**: Profile APIs to find read-heavy, slow-changing data (user profiles, static config, product catalogs)
2. **Measure Access Patterns**: How often is data read vs. written? How large? How old can it be?
3. **Select Strategy**:
   - *Cache-Aside*: App checks cache; on miss, fetches DB, writes cache
   - *Write-Through*: App writes to cache and DB simultaneously
   - *Write-Behind*: App writes to cache only; batch updates to DB later (use cautiously)
4. **Set Eviction Policy**: Assign Time-To-Live (TTL) values based on business tolerance for stale data
5. **Handle Invalidation**: Implement cache invalidation logic on mutations (UPDATE/DELETE)
6. **Prevent Stampedes**: Implement caching locks or staggered TTLs to prevent multiple clients fetching from DB simultaneously when a key expires
7. **Add Monitoring**: Track cache hit rates, eviction rates, and staleness

## Rules
- MUST treat cache as ephemeral (can disappear at any time)
- MUST NOT cache highly personalized or sensitive data (PII) in shared caches
- MUST ALWAYS implement fallback to primary data store on cache failure
- MUST set TTL values (no infinite cache)
- MUST invalidate cache on mutations (UPDATE, DELETE operations)
- MUST use separate caches for different data types/sensitivity levels
- MUST NOT use cache as source of truth

## Anti-patterns
- **Infinite TTL**: Storing keys without expiration (leads to unbounded memory, stale data)
- **Premature Caching**: Adding Redis before the database is properly indexed
- **No Fallback**: Cache failure crashes the application
- **Over-Caching**: Caching everything including rarely-used data (wastes cache memory)
- **Forgetting Invalidation**: Updating database but not cache (stale data served indefinitely)
- **Cache Stampede**: All requests hit cache miss simultaneously, causing DB spike
- **Storing Mutable Objects**: Storing references to objects that change, returning stale mutations

## Failure conditions
- Cache becomes source of truth (data lost if cache clears)
- No fallback logic when cache is unavailable
- Cache miss causes cascading database failures
- Stale data leads to data corruption
- Cache stampede (all requests simultaneously fetch from DB)

## Validation checklist
- [ ] Cache is treated as optimization layer, not data store
- [ ] Fallback to primary data store on cache miss works
- [ ] TTL is set (no infinite cache)
- [ ] Cache invalidation triggered on data mutations
- [ ] Cache hit rate > 80% for target queries
- [ ] No cache stampede when keys expire simultaneously
- [ ] Sensitive data not cached (or encrypted if cached)
- [ ] Cache memory usage monitored (no unbounded growth)
- [ ] Stale data handling defined (acceptable staleness window)
- [ ] Monitoring dashboards show hit rate and eviction rate

## Output format
- **Cache-Aside wrapper**: Function that checks cache, handles miss, populates cache
- **Invalidation triggers**: ON UPDATE/DELETE, clear cache key
- **Configuration**: TTL values, eviction policy, cache key naming convention
- **Monitoring**: Hit rates, eviction rates, staleness metrics
- **Documentation**: Which data is cached, staleness tolerance, fallback behavior

## Security considerations
- Sensitive data MUST NOT be cached or only in encrypted form
- Cache keys MUST be predictable (not guessable)
- Access control MUST be enforced (not all users can access all cache keys)
- Sensitive data MUST be masked in monitoring logs
- Cache MUST be protected from unauthorized access

## Agent execution notes
- Agent MAY: Add cache checks, implement invalidation, set TTL, add monitoring
- Agent MUST NEVER: Use cache as source of truth, forget fallback logic, set infinite TTL
- Agent MUST ASK: Before caching sensitive data, before major caching strategy change
- Agent MUST VALIDATE: Fallback logic works, TTL configured, invalidation on mutations

## Example

**❌ Anti-pattern (No fallback, infinite TTL, no invalidation):**
```javascript
// WRONG: No fallback if cache fails
const getUser = async (userId) => {
  return redis.get(`user:${userId}`); // Fails if Redis is down
};

// WRONG: Infinite TTL
redis.set(`config:app-settings`, settings); // Never expires = stale data forever

// WRONG: No invalidation on update
async function updateUser(userId, data) {
  await db.users.update(userId, data);
  // Forgot to clear cache - stale data served
}

// WRONG: Cache stampede - all requests hit DB when key expires
const getExpensiveData = async () => {
  const cached = await redis.get('expensive-data');
  if (!cached) {
    // All concurrent requests hit this - DB spike
    const data = await slowQuery();
    await redis.set('expensive-data', data, { ex: 3600 });
    return data;
  }
  return cached;
};
```

**✅ Correct pattern (Fallback, TTL, invalidation, stampede prevention):**
```javascript
// CORRECT: Fallback to database on cache miss or failure
const getUser = async (userId) => {
  try {
    const cached = await redis.get(`user:${userId}`);
    if (cached) return JSON.parse(cached);
  } catch (e) {
    logger.warn('Cache miss, falling back to DB', e);
  }
  
  // Fallback to DB
  const user = await db.users.findById(userId);
  
  // Repopulate cache
  try {
    await redis.setex(`user:${userId}`, 3600, JSON.stringify(user)); // 1 hour TTL
  } catch (e) {
    logger.warn('Failed to cache, but returning DB data', e);
  }
  
  return user;
};

// CORRECT: TTL on all cache entries
redis.setex('config:app-settings', 86400, JSON.stringify(settings)); // 24 hour TTL

// CORRECT: Invalidate cache on mutations
async function updateUser(userId, data) {
  await db.users.update(userId, data);
  await redis.del(`user:${userId}`); // Clear specific key
}

// CORRECT: Prevent cache stampede with locks
const stampedeLock = new Mutex();
const getExpensiveData = async () => {
  const cached = await redis.get('expensive-data');
  if (cached) return JSON.parse(cached);
  
  // Use lock to ensure only one request fetches from DB
  return stampedeLock.runExclusive(async () => {
    // Double-check if another request already populated cache
    const cached = await redis.get('expensive-data');
    if (cached) return JSON.parse(cached);
    
    const data = await slowQuery();
    await redis.setex('expensive-data', 3600, JSON.stringify(data));
    return data;
  });
};
```
