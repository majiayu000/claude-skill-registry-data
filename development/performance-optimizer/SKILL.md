---
name: performance-optimizer
description: Expert performance analysis and optimization. Use when analyzing performance issues, optimizing slow code, reducing bundle size, or improving application speed.
allowed-tools: Bash, Read, Grep, Glob
---

# Performance Optimization Skill

Expert knowledge for analyzing and optimizing application performance across frontend, backend, and database layers.

## Performance Analysis Workflow

### 1. Measure First
Never optimize without measuring. Use profiling tools to identify actual bottlenecks.

### 2. Identify Bottlenecks
Find the slowest operations that impact user experience most.

### 3. Optimize High-Impact Areas
Focus on changes that provide the biggest improvement for least effort.

### 4. Measure Again
Verify that optimizations actually improved performance.

## Frontend Performance

### Bundle Size Optimization

**Analyze Bundle**
```bash
# Next.js
npm run build -- --profile

# Webpack Bundle Analyzer
npm install --save-dev webpack-bundle-analyzer
npx webpack-bundle-analyzer build/stats.json

# Check bundle size
ls -lh build/static/js/*.js
```

**Optimization Techniques**

1. **Code Splitting**
```typescript
// Dynamic imports for route-based splitting
const Dashboard = lazy(() => import('./pages/Dashboard'));

// Component-based splitting
const HeavyComponent = lazy(() => import('./components/HeavyComponent'));

// Usage
<Suspense fallback={<Loading />}>
  <Dashboard />
</Suspense>
```

2. **Tree Shaking**
```typescript
// ❌ Bad - imports entire library
import _ from 'lodash';

// ✓ Good - imports only what's needed
import debounce from 'lodash/debounce';
```

3. **Remove Unused Dependencies**
```bash
# Analyze dependencies
npx depcheck

# Remove unused packages
npm uninstall unused-package
```

### React Performance

**1. Memoization**
```typescript
// Memoize expensive calculations
const expensiveValue = useMemo(() => {
  return computeExpensiveValue(a, b);
}, [a, b]);

// Memoize callbacks
const handleClick = useCallback(() => {
  doSomething(a, b);
}, [a, b]);

// Memoize components
const MemoizedComponent = memo(Component, (prev, next) => {
  // Return true if props are equal (skip re-render)
  return prev.id === next.id;
});
```

**2. Virtual Scrolling for Long Lists**
```typescript
import { FixedSizeList } from 'react-window';

<FixedSizeList
  height={600}
  itemCount={1000}
  itemSize={50}
  width="100%"
>
  {({ index, style }) => (
    <div style={style}>Item {index}</div>
  )}
</FixedSizeList>
```

**3. Lazy Load Images**
```typescript
// Native lazy loading
<img src="image.jpg" loading="lazy" alt="Description" />

// Or use Intersection Observer
const LazyImage = ({ src, alt }) => {
  const [imageSrc, setImageSrc] = useState(null);
  const imgRef = useRef();

  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        setImageSrc(src);
        observer.disconnect();
      }
    });

    observer.observe(imgRef.current);
    return () => observer.disconnect();
  }, [src]);

  return <img ref={imgRef} src={imageSrc} alt={alt} />;
};
```

**4. Debounce/Throttle Expensive Operations**
```typescript
import { debounce } from 'lodash';

// Debounce search input
const handleSearch = debounce((query) => {
  fetchResults(query);
}, 300);

// Throttle scroll handler
const handleScroll = throttle(() => {
  updateScrollPosition();
}, 100);
```

### Image Optimization

```bash
# Optimize images
npm install --save-dev imagemin imagemin-mozjpeg imagemin-pngquant

# Use modern formats
- WebP for photos (smaller than JPEG)
- AVIF for even better compression
- SVG for icons and logos

# Responsive images
<picture>
  <source srcset="image.avif" type="image/avif" />
  <source srcset="image.webp" type="image/webp" />
  <img src="image.jpg" alt="Description" />
</picture>
```

### Critical CSS

```html
<!-- Inline critical CSS -->
<style>
  /* Above-the-fold styles */
</style>

<!-- Defer non-critical CSS -->
<link rel="preload" href="styles.css" as="style" onload="this.rel='stylesheet'">
```

## Backend Performance

### Database Optimization

**1. Query Optimization**
```sql
-- ❌ N+1 Query Problem
-- Fetches users, then makes separate query for each user's posts
SELECT * FROM users;
-- Then for each user:
SELECT * FROM posts WHERE user_id = ?;

-- ✓ Solution: Use JOIN or eager loading
SELECT users.*, posts.*
FROM users
LEFT JOIN posts ON posts.user_id = users.id;
```

**2. Add Indexes**
```sql
-- Find slow queries
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Add index for frequently queried columns
CREATE INDEX idx_users_email ON users(email);

-- Composite index for multiple columns
CREATE INDEX idx_posts_user_created ON posts(user_id, created_at);
```

**3. Use Database Connections Pooling**
```typescript
// Configure connection pool
const pool = new Pool({
  max: 20,  // Maximum connections
  min: 5,   // Minimum connections
  idle: 10000  // Close idle connections after 10s
});
```

**4. Pagination**
```typescript
// ❌ Bad - loads all records
const users = await User.findAll();

// ✓ Good - paginate
const users = await User.findAll({
  limit: 20,
  offset: page * 20,
  order: [['created_at', 'DESC']]
});
```

### Caching Strategies

**1. In-Memory Cache**
```typescript
const cache = new Map();

async function getData(key) {
  // Check cache first
  if (cache.has(key)) {
    return cache.get(key);
  }

  // Fetch from database
  const data = await db.query(key);

  // Store in cache
  cache.set(key, data);

  return data;
}
```

**2. Redis Cache**
```typescript
import Redis from 'ioredis';
const redis = new Redis();

async function getCachedData(key) {
  // Try cache
  const cached = await redis.get(key);
  if (cached) return JSON.parse(cached);

  // Fetch from database
  const data = await fetchFromDB(key);

  // Cache for 1 hour
  await redis.setex(key, 3600, JSON.stringify(data));

  return data;
}
```

**3. HTTP Caching**
```typescript
// Set cache headers
res.setHeader('Cache-Control', 'public, max-age=3600');
res.setHeader('ETag', generateETag(data));

// Check If-None-Match header
if (req.headers['if-none-match'] === etag) {
  res.status(304).end();
  return;
}
```

### API Optimization

**1. Response Compression**
```typescript
import compression from 'compression';
app.use(compression());
```

**2. Rate Limiting**
```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // Limit each IP to 100 requests per window
});

app.use('/api/', limiter);
```

**3. Return Only Needed Data**
```typescript
// ❌ Bad - returns everything
const user = await User.findById(id);
res.json(user);

// ✓ Good - select specific fields
const user = await User.findById(id)
  .select('id name email avatar');
res.json(user);
```

**4. Batch Requests**
```typescript
// Instead of multiple requests
// GET /api/users/1
// GET /api/users/2
// GET /api/users/3

// Use single batch request
// POST /api/users/batch { ids: [1, 2, 3] }
```

## Algorithm Optimization

### Time Complexity

```typescript
// ❌ O(n²) - Slow for large datasets
function findDuplicates(arr) {
  const duplicates = [];
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] === arr[j]) duplicates.push(arr[i]);
    }
  }
  return duplicates;
}

// ✓ O(n) - Much faster
function findDuplicates(arr) {
  const seen = new Set();
  const duplicates = new Set();

  for (const item of arr) {
    if (seen.has(item)) {
      duplicates.add(item);
    } else {
      seen.add(item);
    }
  }

  return Array.from(duplicates);
}
```

### Space Complexity

```typescript
// ❌ Creates new array on each recursion
function reverseString(str) {
  if (str === '') return '';
  return reverseString(str.slice(1)) + str[0];
}

// ✓ Iterative approach uses O(1) space
function reverseString(str) {
  return str.split('').reverse().join('');
}
```

## Profiling Tools

### Frontend
```bash
# Chrome DevTools
# - Performance tab
# - Lighthouse audit
# - Network tab

# React DevTools Profiler
# - Component render times
# - Identify unnecessary renders

# Web Vitals
npm install web-vitals

import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

getCLS(console.log);
getFID(console.log);
getFCP(console.log);
getLCP(console.log);
getTTFB(console.log);
```

### Backend
```bash
# Node.js profiling
node --prof app.js
node --prof-process isolate-*.log > processed.txt

# Memory profiling
node --inspect app.js
# Open chrome://inspect

# Add timing logs
console.time('operation');
// ... code
console.timeEnd('operation');
```

### Database
```sql
-- PostgreSQL
EXPLAIN ANALYZE SELECT ...;

-- MySQL
EXPLAIN SELECT ...;

-- Check slow query log
-- PostgreSQL: log_min_duration_statement = 1000
-- MySQL: slow_query_log = 1
```

## Performance Budget

Set limits for your application:

```javascript
{
  "budget": {
    "initialLoad": "200KB",
    "timeToInteractive": "3s",
    "firstContentfulPaint": "1.5s",
    "largestContentfulPaint": "2.5s"
  }
}
```

## Quick Wins

### Frontend
- [x] Enable gzip/brotli compression
- [x] Optimize images (use WebP/AVIF)
- [x] Lazy load images and components
- [x] Remove unused CSS/JS
- [x] Use CDN for static assets
- [x] Add browser caching headers
- [x] Minify CSS/JS

### Backend
- [x] Add database indexes
- [x] Implement caching (Redis)
- [x] Use connection pooling
- [x] Enable response compression
- [x] Optimize database queries (fix N+1)
- [x] Add rate limiting
- [x] Use async operations

## Monitoring

```typescript
// Application Performance Monitoring (APM)
// - New Relic
// - DataDog
// - Sentry Performance

// Custom metrics
const startTime = performance.now();
await performOperation();
const duration = performance.now() - startTime;

// Log slow operations
if (duration > 1000) {
  logger.warn('Slow operation detected', {
    operation: 'fetchUserData',
    duration
  });
}
```

## When to Use This Skill

Invoke this skill when you need to:
- Analyze performance bottlenecks
- Optimize slow queries or code
- Reduce bundle size
- Improve page load times
- Fix memory leaks
- Optimize database operations
- Implement caching strategies
- Profile and measure performance

Simply mention performance issues or optimization needs, and I'll apply this knowledge to help improve your application's speed and efficiency.
