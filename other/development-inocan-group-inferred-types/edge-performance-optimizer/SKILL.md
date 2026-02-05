---
name: edge-performance-optimizer
description: Automatically optimizes Cloudflare Workers performance during development, focusing on cold starts, bundle size, edge caching, and global latency
triggers: ["bundle size changes", "fetch calls", "storage operations", "dependency additions", "sequential operations"]
---

# Edge Performance Optimizer SKILL

## Activation Patterns

This SKILL automatically activates when:
- New dependencies are added to package.json
- Large files or heavy imports are detected
- Sequential operations that could be parallelized
- Missing edge caching opportunities
- Bundle size increases significantly
- Storage operations without optimization patterns

## Expertise Provided

### Edge-Specific Performance Optimization
- **Cold Start Optimization**: Minimizes bundle size and heavy dependencies
- **Global Distribution**: Ensures edge caching for global performance
- **CPU Time Optimization**: Identifies CPU-intensive operations
- **Storage Performance**: Optimizes KV/R2/D1 access patterns
- **Parallel Operations**: Suggests parallelization opportunities
- **Bundle Analysis**: Monitors and optimizes bundle size

### Specific Checks Performed

#### ❌ Performance Anti-Patterns
```typescript
// These patterns trigger immediate alerts:
import axios from 'axios';              // Heavy dependency (13KB)
import moment from 'moment';             // Heavy dependency (68KB)
import _ from 'lodash';                 // Heavy dependency (71KB)

// Sequential operations that could be parallel
const user = await env.USERS.get(id);
const settings = await env.SETTINGS.get(id);
const prefs = await env.PREFS.get(id);
```

#### ✅ Performance Best Practices
```typescript
// These patterns are validated as correct:
// Native Web APIs instead of heavy libraries
const response = await fetch(url);      // Built-in fetch (0KB)
const now = new Date();                // Native Date (0KB)

// Parallel operations
const [user, settings, prefs] = await Promise.all([
  env.USERS.get(id),
  env.SETTINGS.get(id),
  env.PREFS.get(id),
]);
```

## Integration Points

### Complementary to Existing Components
- **edge-performance-oracle agent**: Handles comprehensive performance analysis, SKILL provides immediate optimization
- **workers-runtime-validator SKILL**: Complements runtime checks with performance optimization
- **es-deploy command**: SKILL ensures performance standards before deployment

### Escalation Triggers
- Complex performance architecture questions → `edge-performance-oracle` agent
- Global distribution strategy → `cloudflare-architecture-strategist` agent
- Performance troubleshooting → `edge-performance-oracle` agent

## Validation Rules

### P1 - Critical (Performance Killer)
- **Large Dependencies**: Heavy libraries like moment, lodash, axios
- **Bundle Size**: Over 200KB (kills cold start performance)
- **Sequential Operations**: Multiple sequential storage/network calls
- **Missing Edge Caching**: No caching for frequently accessed data

### P2 - High (Performance Impact)
- **Bundle Size**: Over 100KB (slows cold starts)
- **CPU Time**: Operations approaching 50ms limit
- **Lazy Loading**: Dynamic imports that hurt cold start
- **Large Payloads**: Responses over 100KB without streaming

### P3 - Medium (Optimization Opportunity)
- **Bundle Size**: Over 50KB (could be optimized)
- **Missing Parallelization**: Operations that could be parallel
- **No Request Caching**: Repeated expensive operations

## Remediation Examples

### Fixing Heavy Dependencies
```typescript
// ❌ Critical: Heavy dependencies (150KB+ bundle)
import axios from 'axios';              // 13KB
import moment from 'moment';             // 68KB  
import _ from 'lodash';                 // 71KB
// Total: 152KB just for utilities!

// ✅ Correct: Native Web APIs (minimal bundle)
// Use fetch instead of axios
const response = await fetch(url);
const data = await response.json();

// Use native Date instead of moment
const now = new Date();
const tomorrow = new Date(Date.now() + 86400000);

// Use native methods instead of lodash
const unique = [...new Set(array)];
const grouped = array.reduce((acc, item) => {
  const key = item.category;
  if (!acc[key]) acc[key] = [];
  acc[key].push(item);
  return acc;
}, {});
// Total: < 5KB for utilities
```

### Fixing Sequential Operations
```typescript
// ❌ High: Sequential KV operations (3x network round-trips)
export default {
  async fetch(request: Request, env: Env) {
    const user = await env.USERS.get(userId);      // 10-30ms
    const settings = await env.SETTINGS.get(id);    // 10-30ms  
    const prefs = await env.PREFS.get(id);         // 10-30ms
    // Total: 30-90ms just for storage!
  }
}

// ✅ Correct: Parallel operations (single round-trip)
export default {
  async fetch(request: Request, env: Env) {
    const [user, settings, prefs] = await Promise.all([
      env.USERS.get(userId),
      env.SETTINGS.get(id),
      env.PREFS.get(id),
    ]);
    // Total: 10-30ms (single round-trip)
  }
}
```

### Fixing Missing Edge Caching
```typescript
// ❌ Critical: No edge caching (slow globally)
export default {
  async fetch(request: Request, env: Env) {
    const config = await fetch('https://api.example.com/config');
    // Every request goes to origin!
    // Sydney user → US origin = 200ms+ just for config
  }
}

// ✅ Correct: Edge caching pattern
export default {
  async fetch(request: Request, env: Env) {
    const cache = caches.default;
    const cacheKey = new Request('https://example.com/config', {
      method: 'GET'
    });

    // Try cache first
    let response = await cache.match(cacheKey);

    if (!response) {
      // Cache miss - fetch from origin
      response = await fetch('https://api.example.com/config');
      
      // Cache at edge with 1-hour TTL
      response = new Response(response.body, {
        ...response,
        headers: {
          ...response.headers,
          'Cache-Control': 'public, max-age=3600',
        }
      });
      
      await cache.put(cacheKey, response.clone());
    }

    // Sydney user → Sydney edge cache = < 10ms
    return response;
  }
}
```

### Fixing CPU Time Issues
```typescript
// ❌ High: Large synchronous processing (CPU time bomb)
export default {
  async fetch(request: Request, env: Env) {
    const users = await env.DB.prepare('SELECT * FROM users').all();
    // If 10,000 users, this loops for 100ms+ CPU time
    const enriched = users.results.map(user => {
      return {
        ...user,
        fullName: `${user.firstName} ${user.lastName}`,
        // ... expensive computations
      };
    });
  }
}

// ✅ Correct: Bounded operations
export default {
  async fetch(request: Request, env: Env) {
    // Option 1: Limit at database level
    const users = await env.DB.prepare(
      'SELECT * FROM users LIMIT ? OFFSET ?'
    ).bind(10, offset).all();  // Only 10 users, bounded CPU

    // Option 2: Stream processing for large datasets
    const { readable, writable } = new TransformStream();
    // Process in chunks without loading everything into memory

    // Option 3: Offload to Durable Object
    const id = env.PROCESSOR.newUniqueId();
    const stub = env.PROCESSOR.get(id);
    return stub.fetch(request);  // DO can run longer
  }
}
```

## MCP Server Integration

When Cloudflare MCP server is available:
- Query real performance metrics (cold start times, CPU usage)
- Analyze global latency by region
- Get latest performance optimization techniques
- Check bundle size impact on cold starts

## Benefits

### Immediate Impact
- **Faster Cold Starts**: Reduces bundle size and heavy dependencies
- **Better Global Performance**: Ensures edge caching for worldwide users
- **Lower CPU Usage**: Identifies and optimizes CPU-intensive operations
- **Reduced Latency**: Parallelizes operations and adds caching

### Long-term Value
- **Consistent Performance Standards**: Ensures all code meets performance targets
- **Better User Experience**: Faster response times globally
- **Cost Optimization**: Reduced CPU time usage lowers costs

## Usage Examples

### During Dependency Addition
```typescript
// Developer types: npm install moment
// SKILL immediately activates: "❌ CRITICAL: moment is 68KB and will slow cold starts. Use native Date instead for 0KB impact."
```

### During Storage Operations
```typescript
// Developer types: sequential KV gets
// SKILL immediately activates: "⚠️ HIGH: Sequential KV operations detected. Use Promise.all() to parallelize and reduce latency by 3x."
```

### During API Development
```typescript
// Developer types: fetch without caching
// SKILL immediately activates: "⚠️ HIGH: No edge caching for API call. Add Cache API to serve from edge locations globally."
```

## Performance Targets

### Bundle Size
- **Excellent**: < 10KB
- **Good**: < 50KB  
- **Acceptable**: < 100KB
- **Needs Improvement**: > 100KB
- **Action Required**: > 200KB

### Cold Start Time
- **Excellent**: < 3ms
- **Good**: < 5ms
- **Acceptable**: < 10ms
- **Needs Improvement**: > 10ms
- **Action Required**: > 20ms

### Global Latency (P95)
- **Excellent**: < 100ms
- **Good**: < 200ms
- **Acceptable**: < 500ms
- **Needs Improvement**: > 500ms
- **Action Required**: > 1000ms

This SKILL ensures Workers performance by providing immediate, autonomous optimization of performance patterns, preventing common performance issues and ensuring fast global response times.