---
name: frontend-performance
description: Optimize web application performance including loading, rendering, and interaction metrics. Improve Core Web Vitals and user experience.
triggers:
- /web performance
- /performance optimize
---

# Frontend Performance Optimization

This skill covers techniques for optimizing web application performance to improve loading speed, rendering efficiency, and user experience metrics.

## When to use this skill

Use this skill when you need to:
- Improve page load times
- Optimize Core Web Vitals
- Reduce bundle sizes
- Implement caching strategies
- Profile and fix performance bottlenecks

## Prerequisites

- Understanding of browser rendering pipeline
- Performance profiling tools (Lighthouse, Chrome DevTools)
- Knowledge of JavaScript bundling
- Access to application metrics (Real User Monitoring)

## Guidelines

### Core Web Vitals

**Largest Contentful Paint (LCP)**
- Target: < 2.5 seconds
- Measures: Loading performance
- Optimize: Server response, resource loading, render-blocking

**First Input Delay (FID) / Interaction to Next Paint (INP)**
- Target: < 100ms (FID) / < 200ms (INP)
- Measures: Interactivity
- Optimize: JavaScript execution, main thread availability

**Cumulative Layout Shift (CLS)**
- Target: < 0.1
- Measures: Visual stability
- Optimize: Image dimensions, font loading, dynamic content

### Loading Performance

**Resource Optimization**
```javascript
// Lazy load non-critical resources
const image = new Image();
image.loading = 'lazy';
image.src = '/large-image.jpg';

// Preload critical resources
<link rel="preload" href="/critical.css" as="style">
<link rel="preconnect" href="https://api.example.com">

// Prefetch next page resources
<link rel="prefetch" href="/next-page.js">
```

**Code Splitting**
```javascript
// React lazy loading
const HeavyComponent = React.lazy(() => import('./HeavyComponent'));

// Route-based splitting
const routes = {
  '/dashboard': () => import('./pages/Dashboard'),
  '/profile': () => import('./pages/Profile'),
};

// Dynamic imports
async function loadFeature() {
  const feature = await import('./feature');
  feature.init();
}
```

**Bundle Optimization**
- Tree shaking: Remove unused code
- Minification: Uglify, Terser
- Compression: Gzip, Brotli
- Split vendor and application code

```javascript
// webpack.config.js
module.exports = {
  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all',
        },
      },
    },
  },
};
```

### Rendering Performance

**CSS Optimization**
```css
/* Contain paint for isolated sections */
.card {
  contain: layout style paint;
}

/* Use transform for animations */
.animated {
  will-change: transform;
  transform: translateZ(0);
}

/* Avoid layout thrashing */
/* ❌ Bad: Read then write repeatedly */
const height = element.offsetHeight;
element.style.height = (height + 10) + 'px';

/* ✅ Good: Batch reads and writes */
const height = element.offsetHeight;
requestAnimationFrame(() => {
  element.style.height = (height + 10) + 'px';
});
```

**JavaScript Optimization**
```javascript
// Debounce expensive operations
const debouncedSearch = debounce((query) => {
  performSearch(query);
}, 300);

// Use requestIdleCallback for non-critical work
requestIdleCallback(() => {
  analytics.track('page_view');
});

// Virtualize long lists
import { FixedSizeList } from 'react-window';

<FixedSizeList
  height={500}
  itemCount={10000}
  itemSize={50}
>
  {Row}
</FixedSizeList>
```

**Web Workers**
```javascript
// Offload heavy computations
const worker = new Worker('worker.js');

worker.postMessage({ data: largeDataset });
worker.onmessage = (e) => {
  displayResults(e.data);
};
```

### Image Optimization

**Modern Formats**
```html
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="Description" width="800" height="600">
</picture>
```

**Responsive Images**
```html
<img 
  srcset="small.jpg 300w, medium.jpg 600w, large.jpg 900w"
  sizes="(max-width: 600px) 300px, (max-width: 900px) 600px, 900px"
  src="large.jpg"
  alt="Description"
>
```

**SVG Optimization**
- Minify SVG markup
- Remove unnecessary metadata
- Use sprite sheets for icons

### Caching Strategies

**Service Worker**
```javascript
// Cache-first strategy
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});

// Stale-while-revalidate for API calls
const staleWhileRevalidate = new workbox.strategies.StaleWhileRevalidate({
  cacheName: 'api-cache',
});

workbox.routing.registerRoute(
  ({url}) => url.pathname.startsWith('/api/'),
  staleWhileRevalidate
);
```

**HTTP Caching**
```
Cache-Control: public, max-age=31536000, immutable  # Static assets
Cache-Control: no-cache                              # Dynamic content
Cache-Control: stale-while-revalidate=86400         # Freshness + background update
```

### Measurement and Monitoring

**Lighthouse CI**
```javascript
// lighthouserc.js
module.exports = {
  ci: {
    collect: {
      url: ['http://localhost:3000/'],
      numberOfRuns: 3,
    },
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'first-contentful-paint': ['error', { maxNumericValue: 2000 }],
      },
    },
  },
};
```

**Real User Monitoring**
```javascript
// Send Core Web Vitals to analytics
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

function sendToAnalytics(metric) {
  analytics.track('web_vitals', {
    name: metric.name,
    value: metric.value,
    id: metric.id,
  });
}

getCLS(sendToAnalytics);
getFID(sendToAnalytics);
getLCP(sendToAnalytics);
```

## Examples

See the `examples/` directory for:
- `webpack-config/` - Optimized webpack configurations
- `image-optimization/` - Image loading strategies
- `service-worker/` - Caching implementations
- `performance-budget.json` - Performance budget configuration

## References

- [Web.dev Performance](https://web.dev/performance-scoring/)
- [Chrome DevTools Performance](https://developer.chrome.com/docs/devtools/performance/)
- [Lighthouse documentation](https://developer.chrome.com/docs/lighthouse/)
- [Web Vitals](https://web.dev/vitals/)
- [PageSpeed Insights](https://pagespeed.web.dev/)
