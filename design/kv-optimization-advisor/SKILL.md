---
name: kv-optimization-advisor
description: Automatically optimizes Cloudflare KV storage patterns, suggesting parallel operations, caching strategies, and storage choice guidance
triggers: ["KV operations", "storage access patterns", "sequential storage calls", "large data patterns"]
---

# KV Optimization Advisor SKILL

## Activation Patterns

This SKILL automatically activates when:
- KV `get`, `put`, `delete`, or `list` operations are detected
- Sequential storage operations that could be parallelized
- Large data patterns that might exceed KV limits
- Missing caching opportunities for repeated KV calls
- Storage choice patterns (KV vs R2 vs D1)

## Expertise Provided

### KV Performance Optimization
- **Parallel Operations**: Identifies sequential KV calls that can be parallelized
- **Request-Scoped Caching**: Suggests in-memory caching during request processing
- **Storage Choice Guidance**: Recommends KV vs R2 vs D1 based on use case
- **Value Size Optimization**: Monitors for large values that impact performance
- **Batch Operations**: Suggests batch operations when appropriate
- **TTL Optimization**: Recommends optimal TTL strategies

### Specific Checks Performed

#### ❌ KV Performance Anti-Patterns
```typescript
// These patterns trigger immediate alerts:
// Sequential KV operations (multiple network round-trips)
const user = await env.USERS.get(id);      // 10-30ms
const settings = await env.SETTINGS.get(id); // 10-30ms
const prefs = await env.PREFS.get(id);     // 10-30ms
// Total: 30-90ms just for storage!

// Repeated KV calls in same request
const user1 = await env.USERS.get(id);
const user2 = await env.USERS.get(id);     // Same data fetched twice!
```

#### ✅ KV Performance Best Practices
```typescript
// These patterns are validated as correct:
// Parallel KV operations (single network round-trip)
const [user, settings, prefs] = await Promise.all([
  env.USERS.get(id),
  env.SETTINGS.get(id),
  env.PREFS.get(id),
]);
// Total: 10-30ms (single round-trip)

// Request-scoped caching
const cache = new Map();
async function getCached(key: string, env: Env) {
  if (cache.has(key)) return cache.get(key);
  const value = await env.USERS.get(key);
  cache.set(key, value);
  return value;
}
```

## Integration Points

### Complementary to Existing Components
- **edge-performance-oracle agent**: Handles comprehensive performance analysis, SKILL provides immediate KV optimization
- **cloudflare-architecture-strategist agent**: Handles storage architecture decisions, SKILL provides immediate optimization
- **workers-binding-validator SKILL**: Ensures KV bindings are correct, SKILL optimizes usage patterns

### Escalation Triggers
- Complex storage architecture questions → `cloudflare-architecture-strategist` agent
- KV performance troubleshooting → `edge-performance-oracle` agent
- Storage migration strategies → `cloudflare-architecture-strategist` agent

## Validation Rules

### P1 - Critical (Performance Killer)
- **Sequential Operations**: Multiple sequential KV calls that could be parallelized
- **Repeated Calls**: Same KV key fetched multiple times in one request
- **Large Values**: Values approaching 25MB KV limit

### P2 - High (Performance Impact)
- **Missing Caching**: Repeated expensive KV operations without caching
- **Wrong Storage Choice**: Using KV for data that should be in R2 or D1
- **No TTL Strategy**: Missing or inappropriate TTL configuration

### P3 - Medium (Optimization Opportunity)
- **Batch Opportunities**: Multiple operations that could be batched
- **Suboptimal TTL**: TTL values that are too short or too long
- **Missing Error Handling**: KV operations without proper error handling

## Remediation Examples

### Fixing Sequential Operations
```typescript
// ❌ Critical: Sequential KV operations (3x network round-trips)
export default {
  async fetch(request: Request, env: Env) {
    const userId = getUserId(request);
    
    const user = await env.USERS.get(userId);      // 10-30ms
    const settings = await env.SETTINGS.get(userId); // 10-30ms
    const prefs = await env.PREFS.get(userId);     // 10-30ms
    
    // Total: 30-90ms just for storage!
    return new Response(JSON.stringify({ user, settings, prefs }));
  }
}

// ✅ Correct: Parallel operations (single round-trip)
export default {
  async fetch(request: Request, env: Env) {
    const userId = getUserId(request);
    
    // Fetch in parallel - single network round-trip time
    const [user, settings, prefs] = await Promise.all([
      env.USERS.get(userId),
      env.SETTINGS.get(userId),
      env.PREFS.get(userId),
    ]);
    
    // Total: 10-30ms (single round-trip)
    return new Response(JSON.stringify({ user, settings, prefs }));
  }
}
```

### Fixing Repeated Calls with Caching
```typescript
// ❌ High: Same KV data fetched multiple times
export default {
  async fetch(request: Request, env: Env) {
    const userId = getUserId(request);
    
    // Fetch user data multiple times unnecessarily
    const user1 = await env.USERS.get(userId);
    const user2 = await env.USERS.get(userId);  // Duplicate call!
    const user3 = await env.USERS.get(userId);  // Duplicate call!
    
    // Process user data...
    return new Response('Processed');
  }
}

// ✅ Correct: Request-scoped caching
export default {
  async fetch(request: Request, env: Env) {
    const userId = getUserId(request);
    
    // Request-scoped cache to avoid duplicate KV calls
    const cache = new Map();
    
    async function getCachedUser(id: string) {
      if (cache.has(id)) return cache.get(id);
      const user = await env.USERS.get(id);
      cache.set(id, user);
      return user;
    }
    
    const user1 = await getCachedUser(userId);  // KV call
    const user2 = await getCachedUser(userId);  // From cache
    const user3 = await getCachedUser(userId);  // From cache
    
    // Process user data...
    return new Response('Processed');
  }
}
```

### Fixing Storage Choice
```typescript
// ❌ High: Using KV for large files (wrong storage choice)
export default {
  async fetch(request: Request, env: Env) {
    const fileId = new URL(request.url).searchParams.get('id');
    
    // KV is for small key-value data, not large files!
    const fileData = await env.FILES.get(fileId);  // Could be 10MB+
    
    return new Response(fileData);
  }
}

// ✅ Correct: Use R2 for large files
export default {
  async fetch(request: Request, env: Env) {
    const fileId = new URL(request.url).searchParams.get('id');
    
    // R2 is designed for large objects/files
    const object = await env.FILES_BUCKET.get(fileId);
    
    if (!object) {
      return new Response('Not found', { status: 404 });
    }
    
    return new Response(object.body);
  }
}
```

### Fixing TTL Strategy
```typescript
// ❌ Medium: No TTL strategy (data never expires)
export default {
  async fetch(request: Request, env: Env) {
    const cacheKey = `data:${Date.now()}`;
    
    // Data cached forever - may become stale
    await env.CACHE.put(cacheKey, data);
  }
}

// ✅ Correct: Appropriate TTL strategy
export default {
  async fetch(request: Request, env: Env) {
    const cacheKey = 'user:profile:123';
    
    // Cache user profile for 1 hour (reasonable for user data)
    await env.CACHE.put(cacheKey, data, {
      expirationTtl: 3600  // 1 hour
    });
    
    // Cache API response for 5 minutes (frequently changing)
    await env.API_CACHE.put(apiKey, response, {
      expirationTtl: 300  // 5 minutes
    });
    
    // Cache static data for 24 hours (rarely changes)
    await env.STATIC_CACHE.put(staticKey, data, {
      expirationTtl: 86400  // 24 hours
    });
  }
}
```

### Fixing Large Value Handling
```typescript
// ❌ High: Large values approaching KV limits
export default {
  async fetch(request: Request, env: Env) {
    const reportId = new URL(request.url).searchParams.get('id');
    
    // Large report (20MB) - close to KV 25MB limit!
    const report = await env.REPORTS.get(reportId);
    
    return new Response(report);
  }
}

// ✅ Correct: Compress large values or use R2
export default {
  async fetch(request: Request, env: Env) {
    const reportId = new URL(request.url).searchParams.get('id');
    
    // Option 1: Compress before storing in KV
    const compressed = await env.REPORTS.get(reportId);
    const decompressed = decompress(compressed);
    
    // Option 2: Use R2 for large objects
    const object = await env.REPORTS_BUCKET.get(reportId);
    
    return new Response(object.body);
  }
}
```

## Storage Choice Guidance

### Use KV When:
- **Small values** (< 1MB typical, < 25MB max)
- **Key-value access patterns**
- **Eventually consistent** data is acceptable
- **Low latency** reads required globally
- **Simple caching** needs

### Use R2 When:
- **Large objects** (files, images, videos)
- **S3-compatible** access needed
- **Strong consistency** required
- **Object storage** patterns
- **Large files** (> 1MB)

### Use D1 When:
- **Relational data** with complex queries
- **Strong consistency** required
- **SQL operations** needed
- **Structured data** with relationships
- **Complex queries** and joins

## MCP Server Integration

When Cloudflare MCP server is available:
- Query KV performance metrics (latency, hit rates)
- Analyze storage usage patterns
- Get latest KV optimization techniques
- Check storage limits and quotas

## Benefits

### Immediate Impact
- **Faster Response Times**: Parallel operations reduce latency by 3x or more
- **Reduced KV Costs**: Fewer operations and better caching
- **Better Performance**: Proper storage choice improves overall performance

### Long-term Value
- **Consistent Optimization**: Ensures all KV usage follows best practices
- **Cost Efficiency**: Optimized storage patterns reduce costs
- **Better User Experience**: Faster response times from optimized storage

## Usage Examples

### During KV Operation Writing
```typescript
// Developer types: sequential KV gets
// SKILL immediately activates: "⚠️ HIGH: Sequential KV operations detected. Use Promise.all() to parallelize and reduce latency by 3x."
```

### During Storage Architecture
```typescript
// Developer types: storing large files in KV
// SKILL immediately activates: "⚠️ HIGH: Large file storage in KV detected. Use R2 for objects > 1MB to avoid performance issues."
```

### During Caching Implementation
```typescript
// Developer types: repeated KV calls in same request
// SKILL immediately activates: "⚠️ HIGH: Duplicate KV calls detected. Add request-scoped caching to avoid redundant network calls."
```

## Performance Targets

### KV Operation Latency
- **Excellent**: < 10ms (parallel operations)
- **Good**: < 30ms (single operation)
- **Acceptable**: < 100ms (sequential operations)
- **Needs Improvement**: > 100ms

### Cache Hit Rate
- **Excellent**: > 90%
- **Good**: > 75%
- **Acceptable**: > 50%
- **Needs Improvement**: < 50%

This SKILL ensures KV storage performance by providing immediate, autonomous optimization of storage patterns, preventing common performance issues and ensuring efficient data access.