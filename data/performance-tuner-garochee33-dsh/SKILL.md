---
name: performance-tuner
version: "2.0"
trigger: performance tuning, bundle size, caching, lazy loading, optimization
description: Performance optimization, profiling, caching strategies, lazy loading, bundle optimization, and monitoring. Use when optimizing application performance, reducing bundle size, implementing caching, or analyzing bottlenecks.
---

# Performance Tuner

## Caching Strategies

### Redis Caching
```typescript
import { Redis } from 'ioredis';

export class CacheManager {
  private redis = new Redis(process.env.REDIS_URL);
  
  async get<T>(key: string): Promise<T | null> {
    const data = await this.redis.get(key);
    return data ? JSON.parse(data) : null;
  }
  
  async set<T>(key: string, value: T, ttl: number): Promise<void> {
    await this.redis.setex(key, ttl, JSON.stringify(value));
  }
  
  async getOrSet<T>(
    key: string,
    factory: () => Promise<T>,
    ttl: number
  ): Promise<T> {
    const cached = await this.get<T>(key);
    if (cached) return cached;
    
    const value = await factory();
    await this.set(key, value, ttl);
    return value;
  }
}

// Usage with stale-while-revalidate
export class SWRCache {
  async get<T>(key: string): Promise<T> {
    const [fresh, stale] = await Promise.all([
      this.redis.get(`fresh:${key}`),
      this.redis.get(`stale:${key}`)
    ]);
    
    if (fresh) return JSON.parse(fresh);
    
    // Trigger revalidation in background
    if (stale) {
      this.revalidate(key);
      return JSON.parse(stale);
    }
    
    return this.fetchAndCache(key);
  }
}
```

### HTTP Caching Headers
```typescript
export function setCacheHeaders(
  res: Response,
  options: CacheOptions
) {
  if (options.swr) {
    res.setHeader('Cache-Control', 
      `public, s-maxage=${options.stale}, stale-while-revalidate=${options.revalidate}`
    );
  } else if (options.immutable) {
    res.setHeader('Cache-Control', 'public, max-age=31536000, immutable');
  } else {
    res.setHeader('Cache-Control', `public, max-age=${options.maxAge}`);
  }
}
```

## Bundle Optimization

### Dynamic Imports
```typescript
// Lazy load heavy components
const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <ChartSkeleton />,
  ssr: false // Disable SSR for browser-only libraries
});

// Preload on hover
function LinkWithPreload({ href, children }) {
  return (
    <Link 
      href={href}
      onMouseEnter={() => {
        const Component = dynamic(() => import(`./pages${href}`));
      }}
    >
      {children}
    </Link>
  );
}
```

### Tree Shaking
```typescript
// ✅ Good: Named imports
import { map, filter } from 'lodash-es';

// ❌ Bad: Full import
import _ from 'lodash';

// ✅ Good: Barrel exports with care
export { Button } from './Button';
export { Input } from './Input';
```

## Database Query Optimization

### Query Analysis
```typescript
// Explain query plans
const explain = await db.execute(sql`
  EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
  SELECT * FROM users WHERE email = ${email}
`);

// Index usage check
const indexUsage = await db.execute(sql`
  SELECT 
    schemaname,
    tablename,
    attname as column,
    n_tup_read,
    n_tup_fetch
  FROM pg_stats
  WHERE tablename = 'users'
`);
```

### Connection Pooling
```typescript
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,                    // Maximum pool size
  idleTimeoutMillis: 30000,   // Close idle connections
  connectionTimeoutMillis: 2000,
  application_name: 'trinity_app'
});

// Monitor pool
pool.on('connect', () => console.log('New client connected'));
pool.on('error', (err) => console.error('Pool error:', err));
```

## Image Optimization

### Next.js Image
```tsx
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority // Above-the-fold images
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,..."
/>
```

### Responsive Images
```tsx
<Image
  src="/photo.jpg"
  alt="Photo"
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
  fill
  className="object-cover"
/>
```

## Performance Monitoring

### Web Vitals
```typescript
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

function sendToAnalytics(metric) {
  const body = JSON.stringify(metric);
  (navigator.sendBeacon && navigator.sendBeacon('/analytics', body)) ||
    fetch('/analytics', { body, method: 'POST', keepalive: true });
}

getCLS(sendToAnalytics);
getFID(sendToAnalytics);
getFCP(sendToAnalytics);
getLCP(sendToAnalytics);
getTTFB(sendToAnalytics);
```

### Custom Metrics
```typescript
export class PerformanceMonitor {
  measure(name: string, fn: () => Promise<T>): Promise<T> {
    const start = performance.now();
    
    return fn().finally(() => {
      const duration = performance.now() - start;
      
      // Send to monitoring
      this.report({
        name: `timing.${name}`,
        value: duration,
        unit: 'ms'
      });
    });
  }
}
```

## Memory Management

### WeakRef for Caching
```typescript
class WeakCache<K, V extends object> {
  private cache = new Map<K, WeakRef<V>>();
  private finalizer = new FinalizationRegistry<K>(key => {
    this.cache.delete(key);
  });
  
  set(key: K, value: V) {
    this.cache.set(key, new WeakRef(value));
    this.finalizer.register(value, key);
  }
  
  get(key: K): V | undefined {
    const ref = this.cache.get(key);
    return ref?.deref();
  }
}
```
