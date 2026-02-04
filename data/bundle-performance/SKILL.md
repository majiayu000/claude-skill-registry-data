---
name: bundle-performance
description: Monitor JavaScript bundle size and execution performance. Use when tracking bundle size, identifying large chunks, or optimizing load performance.
triggers:
  - "bundle size"
  - "large bundle"
  - "JavaScript size"
  - "chunk optimization"
  - "code splitting"
  - "Long Tasks"
priority: 2
---

# Bundle Performance

Monitor JavaScript bundle size and its impact on performance.

## Why Bundle Size Matters

| Bundle Size | LCP Impact | INP Impact |
|-------------|------------|------------|
| <100KB | Minimal | Minimal |
| 100-300KB | Moderate | Noticeable |
| 300-500KB | Significant | Degraded |
| >500KB | Severe | Poor |

## Performance Budgets

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| Initial JS | <200KB | <500KB | >500KB |
| Per-route chunk | <100KB | <200KB | >200KB |
| Total JS | <500KB | <1MB | >1MB |
| First Load | <3s on 3G | <5s | >5s |

## Build-Time Analysis

### Vite

```typescript
// vite.config.ts
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          utils: ['lodash', 'date-fns'],
        },
      },
    },
  },
  plugins: [
    visualizer({
      filename: 'dist/stats.html',
      gzipSize: true,
      brotliSize: true,
    }),
  ],
});
```

### Webpack (Next.js)

```javascript
// next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
  // your config
});

// Run: ANALYZE=true npm run build
```

## Runtime Monitoring

### Resource Timing API

```typescript
function trackBundleLoading() {
  const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      if (entry.name.endsWith('.js')) {
        trackResourceLoad({
          name: new URL(entry.name).pathname,
          size_bytes: (entry as PerformanceResourceTiming).transferSize,
          duration_ms: entry.duration,
          type: 'javascript',
        });
      }
    }
  });

  observer.observe({ type: 'resource', buffered: true });
}
```

### Long Tasks API

```typescript
function trackLongTasks() {
  const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      trackLongTask({
        duration_ms: entry.duration,
        start_time_ms: entry.startTime,
        // Attribution for debugging
        name: (entry as any).attribution?.[0]?.name || 'unknown',
        container_type: (entry as any).attribution?.[0]?.containerType,
      });

      // Alert on very long tasks
      if (entry.duration > 100) {
        captureMessage('Long task detected', {
          level: 'warning',
          extra: {
            duration_ms: entry.duration,
            route: window.location.pathname,
          },
        });
      }
    }
  });

  observer.observe({ type: 'longtask', buffered: true });
}
```

## Dynamic Import Tracking

```typescript
// Track lazy-loaded chunks
async function trackedImport<T>(
  importFn: () => Promise<T>,
  chunkName: string
): Promise<T> {
  const startTime = performance.now();

  try {
    const module = await importFn();
    const duration = performance.now() - startTime;

    trackChunkLoad({
      chunk_name: chunkName,
      duration_ms: duration,
      success: true,
    });

    return module;
  } catch (error) {
    trackChunkLoad({
      chunk_name: chunkName,
      success: false,
      error_type: error instanceof Error ? error.name : 'unknown',
    });
    throw error;
  }
}

// Usage
const HeavyComponent = lazy(() =>
  trackedImport(
    () => import('./HeavyComponent'),
    'HeavyComponent'
  )
);
```

## CI/CD Integration

### Size Limit

```json
// package.json
{
  "size-limit": [
    {
      "path": "dist/**/*.js",
      "limit": "200 KB"
    },
    {
      "path": "dist/vendor*.js",
      "limit": "100 KB"
    }
  ]
}
```

### bundlewatch

```json
// bundlewatch.config.json
{
  "files": [
    {
      "path": "./dist/main*.js",
      "maxSize": "150kB"
    },
    {
      "path": "./dist/vendor*.js",
      "maxSize": "100kB"
    }
  ],
  "ci": {
    "trackBranches": ["main"],
    "repoBranchBase": "main"
  }
}
```

## Third-Party Script Tracking

```typescript
function trackThirdPartyScripts() {
  const entries = performance.getEntriesByType('resource') as PerformanceResourceTiming[];

  const thirdParty = entries.filter((entry) => {
    const url = new URL(entry.name);
    return url.hostname !== window.location.hostname;
  });

  const summary = {
    count: thirdParty.length,
    total_size_bytes: thirdParty.reduce((sum, e) => sum + e.transferSize, 0),
    total_duration_ms: thirdParty.reduce((sum, e) => sum + e.duration, 0),
    scripts: thirdParty.map((e) => ({
      url: e.name,
      size_bytes: e.transferSize,
      duration_ms: e.duration,
    })),
  };

  trackThirdPartyImpact(summary);
}
```

## Optimization Strategies

| Strategy | Impact | Implementation |
|----------|--------|----------------|
| Code splitting | High | Route-based chunks |
| Tree shaking | High | ES modules, sideEffects |
| Dynamic imports | High | Lazy load non-critical |
| Compression | High | Brotli/gzip |
| Modern/legacy | Medium | module/nomodule |
| Vendor chunking | Medium | Manual chunks |
| Preload critical | Medium | modulepreload |

## Anti-Patterns

- Loading entire SDK in main bundle
- Not code-splitting routes
- Importing entire lodash/moment
- Missing tree-shaking (CommonJS)
- Not monitoring bundle size in CI
- Third-party scripts without budget

## Related Skills

- See `skills/core-web-vitals` for LCP/INP impact
- See `skills/hydration-performance` for JS impact on hydration
- See `skills/synthetic-monitoring` for lab testing

## References

- `references/performance.md` - Performance budgets
- `references/frameworks/*.md` - Framework-specific optimization
