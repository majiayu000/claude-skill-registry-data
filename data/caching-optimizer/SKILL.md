---
name: caching-optimizer
description: "Optimize caching strategies for performance. Use when analyzing cache effectiveness, implementing multi-layer caching, optimizing Redis/memory caches, or troubleshooting slow response times."
---

# Caching Optimizer

> Intelligent caching strategy optimization for applications and APIs

## Quick Commands

```bash
# Analyze cache effectiveness
npx @j0kz/caching-optimizer analyze

# Generate caching strategy
npx @j0kz/caching-optimizer suggest --profile=api

# Clear and warm cache
npm run cache:clear && npm run cache:warm

# Monitor cache metrics
npx @j0kz/caching-optimizer monitor
```

## Core Functionality

### Key Features

1. **Cache Analysis**: Hit/miss ratios and effectiveness
2. **Strategy Optimization**: LRU, LFU, TTL recommendations
3. **Multi-Layer Caching**: Memory, Redis, CDN coordination
4. **Cache Warming**: Preload frequently accessed data
5. **Invalidation Strategies**: Smart cache busting

## Detailed Information

For comprehensive details, see:

```bash
cat .claude/skills/caching-optimizer/references/caching-patterns.md
```

```bash
cat .claude/skills/caching-optimizer/references/redis-optimization.md
```

```bash
cat .claude/skills/caching-optimizer/references/cdn-strategies.md
```

## Usage Examples

### Example 1: Implement Multi-Layer Cache

```javascript
import { CachingOptimizer } from '@j0kz/caching-optimizer';

const optimizer = new CachingOptimizer({
  layers: [
    { type: 'memory', size: '100MB', ttl: 300 },
    { type: 'redis', size: '1GB', ttl: 3600 },
    { type: 'cdn', ttl: 86400 }
  ]
});

// Automatic layer selection
const data = await optimizer.get('user:123', async () => {
  return await fetchUserFromDB(123);
});
```

### Example 2: Cache Effectiveness Analysis

```javascript
const metrics = await optimizer.analyze({
  period: '24h',
  breakdown: true
});

console.log(`Hit Rate: ${metrics.hitRate}%`);
console.log(`Miss Rate: ${metrics.missRate}%`);
console.log(`Eviction Rate: ${metrics.evictionRate}%`);

// Get recommendations
const suggestions = optimizer.suggest(metrics);
suggestions.forEach(s => console.log(s));
```

## Caching Strategies

### Common Patterns

1. **Cache-Aside (Lazy Loading)**
   ```javascript
   const data = cache.get(key) || await loadAndCache(key);
   ```

2. **Write-Through**
   ```javascript
   await Promise.all([
     cache.set(key, data),
     database.save(key, data)
   ]);
   ```

3. **Write-Behind (Write-Back)**
   ```javascript
   cache.set(key, data);
   queue.push({ action: 'save', key, data });
   ```

### Cache Keys Strategy

```javascript
// Hierarchical keys for batch invalidation
const keyPatterns = {
  user: 'user:{id}',
  userPosts: 'user:{userId}:posts',
  post: 'post:{id}',
  postComments: 'post:{postId}:comments:{page}'
};
```

## Configuration

```json
{
  "caching-optimizer": {
    "default": {
      "strategy": "lru",
      "maxSize": "512MB",
      "ttl": 3600,
      "compression": true
    },
    "layers": {
      "memory": {
        "enabled": true,
        "maxSize": "128MB"
      },
      "redis": {
        "enabled": true,
        "cluster": false,
        "db": 0
      },
      "cdn": {
        "enabled": true,
        "provider": "cloudflare"
      }
    },
    "monitoring": {
      "metrics": ["hitRate", "missRate", "latency"],
      "alertThreshold": {
        "hitRate": 0.8,
        "latency": 100
      }
    }
  }
}
```

## Cache Invalidation

```javascript
// Tag-based invalidation
await optimizer.tag(['user:123', 'posts']).set(key, data);
await optimizer.invalidateTag('user:123');

// Pattern-based invalidation
await optimizer.invalidatePattern('user:123:*');

// Time-based invalidation
await optimizer.set(key, data, { ttl: 3600, slide: true });
```

## Notes

- Supports Redis, Memcached, and in-memory caching
- Automatic cache stampede prevention
- Compression for large values
- Distributed caching support for microservices