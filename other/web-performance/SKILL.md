---
name: Web Performance
description: This skill activates when users discuss site speed, Core Web Vitals, optimization, bundle size, lazy loading, or performance issues. Provides guidance on measuring, analyzing, and optimizing web performance with focus on LCP, FID, CLS, and modern performance patterns.
---

# Web Performance Optimization

Optimize web applications for speed, Core Web Vitals, and user experience.

## When This Activates

- "slow site", "performance", "optimization", "speed"
- "Core Web Vitals", "LCP", "FID", "CLS", "Lighthouse"
- "bundle size", "lazy loading", "code splitting"
- User reports poor performance scores
- Discussing how to improve site speed

---

## Core Web Vitals (Google's Metrics)

### 1. Largest Contentful Paint (LCP)

**Target**: < 2.5 seconds

**What it measures**: Time until largest content element renders

**Common causes of poor LCP:**
- Slow server response time
- Render-blocking JavaScript/CSS
- Large images without optimization
- Client-side rendering

**How to fix:**

```typescript
// 1. Image optimization with next/image
import Image from 'next/image';

<Image
  src="/jewelry/ring.jpg"
  alt="Luxury Ring"
  width={800}
  height={800}
  priority // Load immediately for above-fold
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,..."
/>

// 2. Preload critical resources
<link
  rel="preload"
  href="/fonts/archivo.woff2"
  as="font"
  type="font/woff2"
  crossOrigin="anonymous"
/>

// 3. Optimize server response (WordPress)
// Add page caching, CDN, database optimization
```

### 2. First Input Delay (FID) / Interaction to Next Paint (INP)

**Target**: < 100ms (FID) or < 200ms (INP)

**What it measures**: Time from user interaction to browser response

**Common causes:**
- Long-running JavaScript
- Heavy JavaScript execution
- Large bundle blocking main thread

**How to fix:**

```typescript
// 1. Defer non-critical JavaScript
<script src="analytics.js" defer></script>

// 2. Use Web Workers for heavy computation
// worker.ts
self.addEventListener('message', (e) => {
  const result = expensiveCalculation(e.data);
  self.postMessage(result);
});

// main.ts
const worker = new Worker('/worker.js');
worker.postMessage(inputData);
worker.onmessage = (e) => {
  console.log('Result:', e.data);
};

// 3. Break up long tasks
async function processLargeDataset(items: any[]) {
  const chunkSize = 50;

  for (let i = 0; i < items.length; i += chunkSize) {
    const chunk = items.slice(i, i + chunkSize);
    await processChunk(chunk);

    // Yield to browser
    await new Promise(resolve => setTimeout(resolve, 0));
  }
}
```

### 3. Cumulative Layout Shift (CLS)

**Target**: < 0.1

**What it measures**: Visual stability (unexpected layout shifts)

**Common causes:**
- Images without dimensions
- Ads/embeds without reserved space
- Web fonts causing FOIT/FOUT
- Dynamic content insertion

**How to fix:**

```tsx
// 1. Always specify image dimensions
<img
  src="product.jpg"
  width="800"
  height="600"
  alt="Product"
  style={{ aspectRatio: '4/3' }}
/>

// 2. Reserve space for dynamic content
<div style={{ minHeight: '400px' }}>
  {isLoading ? <Skeleton /> : <ProductGrid products={products} />}
</div>

// 3. Optimize font loading
// In CSS
@font-face {
  font-family: 'Archivo';
  src: url('/fonts/archivo.woff2') format('woff2');
  font-display: swap; /* Prevents invisible text */
  font-weight: 400;
}

// Preload critical fonts
<link
  rel="preload"
  href="/fonts/archivo.woff2"
  as="font"
  type="font/woff2"
  crossOrigin="anonymous"
/>
```

---

## Bundle Optimization

### Analyze Bundle Size

```bash
# Webpack Bundle Analyzer
npm install --save-dev webpack-bundle-analyzer

# In webpack.config.js
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');

module.exports = {
  plugins: [
    new BundleAnalyzerPlugin({
      analyzerMode: 'static',
      reportFilename: 'bundle-report.html',
    }),
  ],
};

# View report
npm run build && open dist/bundle-report.html
```

### Tree Shaking

```typescript
// ❌ Bad: Imports entire library
import _ from 'lodash';
const result = _.debounce(fn, 300);

// ✅ Good: Import only what you need
import { debounce } from 'lodash-es';
const result = debounce(fn, 300);

// Or use native alternatives
const debounce = (fn: Function, ms: number) => {
  let timeout: NodeJS.Timeout;
  return (...args: any[]) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), ms);
  };
};
```

### Code Splitting

```tsx
// Route-based splitting
import { lazy, Suspense } from 'react';

const ProductPage = lazy(() => import('./pages/ProductPage'));
const CheckoutPage = lazy(() => import('./pages/CheckoutPage'));

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/products/:id" element={<ProductPage />} />
        <Route path="/checkout" element={<CheckoutPage />} />
      </Routes>
    </Suspense>
  );
}

// Component-based splitting
const HeavyChart = lazy(() => import('./HeavyChart'));

function Dashboard() {
  return (
    <div>
      <Suspense fallback={<div>Loading chart...</div>}>
        <HeavyChart data={data} />
      </Suspense>
    </div>
  );
}
```

---

## Image Optimization

### Formats

| Format | Use Case | Compression |
|--------|----------|-------------|
| **WebP** | Modern browsers | 25-35% smaller than JPEG |
| **AVIF** | Cutting edge | 50% smaller than JPEG |
| **JPEG** | Fallback | Good for photos |
| **PNG** | Transparency | Lossless, larger |
| **SVG** | Icons, logos | Vector, scalable |

### Responsive Images

```html
<!-- Serve different sizes based on viewport -->
<picture>
  <source
    srcset="
      /images/ring-400.avif 400w,
      /images/ring-800.avif 800w,
      /images/ring-1200.avif 1200w
    "
    type="image/avif"
  />
  <source
    srcset="
      /images/ring-400.webp 400w,
      /images/ring-800.webp 800w,
      /images/ring-1200.webp 1200w
    "
    type="image/webp"
  />
  <img
    src="/images/ring-800.jpg"
    srcset="
      /images/ring-400.jpg 400w,
      /images/ring-800.jpg 800w,
      /images/ring-1200.jpg 1200w
    "
    sizes="(max-width: 768px) 100vw, 800px"
    alt="Luxury Ring"
    width="800"
    height="800"
    loading="lazy"
  />
</picture>
```

### Lazy Loading

```tsx
// Native lazy loading
<img src="image.jpg" loading="lazy" alt="Product" />

// Intersection Observer for custom control
import { useEffect, useRef, useState } from 'react';

function LazyImage({ src, alt }: { src: string; alt: string }) {
  const [isLoaded, setIsLoaded] = useState(false);
  const imgRef = useRef<HTMLImageElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsLoaded(true);
            observer.disconnect();
          }
        });
      },
      { rootMargin: '100px' } // Load 100px before entering viewport
    );

    if (imgRef.current) {
      observer.observe(imgRef.current);
    }

    return () => observer.disconnect();
  }, []);

  return (
    <img
      ref={imgRef}
      src={isLoaded ? src : '/placeholder.jpg'}
      alt={alt}
      style={{ filter: isLoaded ? 'none' : 'blur(20px)' }}
    />
  );
}
```

---

## JavaScript Performance

### Debouncing & Throttling

```typescript
// Debounce: Wait for user to stop typing
function debounce<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: NodeJS.Timeout;

  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

// Usage: Search as user types
const handleSearch = debounce((query: string) => {
  fetchSearchResults(query);
}, 300);

// Throttle: Limit execution frequency
function throttle<T extends (...args: any[]) => any>(
  fn: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle = false;

  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      fn(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

// Usage: Scroll event
const handleScroll = throttle(() => {
  console.log('Scrolled');
}, 100);
```

### Memoization

```tsx
import { useMemo, useCallback } from 'react';

function ProductList({ products, filters }) {
  // Memoize expensive calculation
  const filteredProducts = useMemo(() => {
    return products.filter((p) => {
      return filters.every((f) => f.fn(p));
    });
  }, [products, filters]);

  // Memoize callback to prevent child re-renders
  const handleAddToCart = useCallback((productId: string) => {
    addToCart(productId);
  }, []);

  return (
    <div>
      {filteredProducts.map((p) => (
        <ProductCard
          key={p.id}
          product={p}
          onAddToCart={handleAddToCart}
        />
      ))}
    </div>
  );
}
```

---

## WordPress-Specific Optimizations

### 1. Caching

```php
// Page caching with W3 Total Cache or WP Rocket
// Object caching with Redis

// Transient API for expensive queries
function get_skyyrose_featured_products() {
    $cache_key = 'skyyrose_featured_products';
    $products = get_transient($cache_key);

    if (false === $products) {
        $products = wc_get_products([
            'meta_key' => '_featured',
            'meta_value' => 'yes',
            'limit' => 8,
        ]);

        set_transient($cache_key, $products, HOUR_IN_SECONDS);
    }

    return $products;
}
```

### 2. Database Optimization

```php
// Optimize WooCommerce queries
add_filter('woocommerce_product_query', function($q) {
    // Only load what you need
    $q->set('fields', 'ids'); // Just IDs instead of full objects
    return $q;
});

// Add database indexes for custom queries
global $wpdb;
$wpdb->query("
    CREATE INDEX idx_skyyrose_collection
    ON {$wpdb->postmeta} (meta_key, meta_value)
    WHERE meta_key = '_skyyrose_collection'
");
```

### 3. Asset Optimization

```php
// Defer non-critical scripts
function skyyrose_defer_scripts($tag, $handle) {
    $defer_scripts = ['elementor-frontend', 'wp-block-library'];

    if (in_array($handle, $defer_scripts)) {
        return str_replace(' src', ' defer src', $tag);
    }

    return $tag;
}
add_filter('script_loader_tag', 'skyyrose_defer_scripts', 10, 2);

// Remove unused CSS
function skyyrose_dequeue_unused_css() {
    if (!is_cart() && !is_checkout()) {
        wp_dequeue_style('wc-blocks-style'); // Don't load WooCommerce blocks CSS
    }
}
add_action('wp_enqueue_scripts', 'skyyrose_dequeue_unused_css', 100);
```

---

## 3D Performance (Three.js / Babylon.js)

### Level of Detail (LOD)

```typescript
import { LOD, Mesh, SphereGeometry, MeshStandardMaterial } from 'three';

function createLODModel() {
  const lod = new LOD();

  // High detail (close)
  const highDetail = new Mesh(
    new SphereGeometry(1, 64, 64),
    new MeshStandardMaterial()
  );
  lod.addLevel(highDetail, 0);

  // Medium detail
  const mediumDetail = new Mesh(
    new SphereGeometry(1, 32, 32),
    new MeshStandardMaterial()
  );
  lod.addLevel(mediumDetail, 50);

  // Low detail (far)
  const lowDetail = new Mesh(
    new SphereGeometry(1, 16, 16),
    new MeshStandardMaterial()
  );
  lod.addLevel(lowDetail, 100);

  return lod;
}
```

### Instancing for Multiple Objects

```typescript
import { InstancedMesh, Object3D } from 'three';

// Render 1000 objects efficiently
const geometry = new BoxGeometry(1, 1, 1);
const material = new MeshStandardMaterial({ color: '#B76E79' });
const instancedMesh = new InstancedMesh(geometry, material, 1000);

const dummy = new Object3D();

for (let i = 0; i < 1000; i++) {
  dummy.position.set(
    Math.random() * 100 - 50,
    Math.random() * 100 - 50,
    Math.random() * 100 - 50
  );
  dummy.updateMatrix();
  instancedMesh.setMatrixAt(i, dummy.matrix);
}

instancedMesh.instanceMatrix.needsUpdate = true;
scene.add(instancedMesh);
```

---

## Monitoring & Measurement

### Lighthouse CI

```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI
on: [pull_request]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm run build
      - name: Run Lighthouse CI
        run: |
          npm install -g @lhci/cli
          lhci autorun --config=.lighthouserc.json
```

```json
// .lighthouserc.json
{
  "ci": {
    "collect": {
      "url": ["http://localhost:3000/"],
      "numberOfRuns": 3
    },
    "assert": {
      "assertions": {
        "categories:performance": ["error", { "minScore": 0.9 }],
        "categories:accessibility": ["error", { "minScore": 0.9 }],
        "first-contentful-paint": ["error", { "maxNumericValue": 2000 }],
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }]
      }
    }
  }
}
```

### Real User Monitoring (RUM)

```typescript
// Send Core Web Vitals to analytics
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

function sendToAnalytics(metric: any) {
  const body = JSON.stringify({
    name: metric.name,
    value: metric.value,
    rating: metric.rating,
    delta: metric.delta,
    id: metric.id,
  });

  // Use sendBeacon if available
  if (navigator.sendBeacon) {
    navigator.sendBeacon('/api/analytics', body);
  } else {
    fetch('/api/analytics', { method: 'POST', body, keepalive: true });
  }
}

getCLS(sendToAnalytics);
getFID(sendToAnalytics);
getFCP(sendToAnalytics);
getLCP(sendToAnalytics);
getTTFB(sendToAnalytics);
```

---

## Performance Budget

### Set Limits

| Metric | Budget | Current | Status |
|--------|--------|---------|--------|
| LCP | < 2.5s | 2.1s | ✅ |
| FID | < 100ms | 85ms | ✅ |
| CLS | < 0.1 | 0.05 | ✅ |
| JavaScript | < 200KB | 180KB | ✅ |
| CSS | < 50KB | 45KB | ✅ |
| Images | < 500KB | 450KB | ✅ |
| Total | < 1MB | 875KB | ✅ |

### Enforce in CI

```json
// package.json
{
  "scripts": {
    "build": "next build",
    "analyze": "ANALYZE=true next build",
    "size-limit": "size-limit"
  },
  "size-limit": [
    {
      "path": "dist/**/*.js",
      "limit": "200 KB"
    },
    {
      "path": "dist/**/*.css",
      "limit": "50 KB"
    }
  ]
}
```

---

## Quick Wins Checklist

For SkyyRose (or any site):

- [ ] **Images**: Convert to WebP/AVIF, add `loading="lazy"`
- [ ] **Fonts**: Preload, use `font-display: swap`
- [ ] **JavaScript**: Defer non-critical scripts
- [ ] **CSS**: Inline critical CSS, defer rest
- [ ] **Caching**: Enable page caching (W3TC/WP Rocket)
- [ ] **CDN**: Use CDN for static assets
- [ ] **Database**: Add indexes, enable object caching
- [ ] **3D**: Use LOD, instancing, optimize geometries
- [ ] **Monitoring**: Set up Lighthouse CI, track RUM

---

## When User Reports Performance Issues

1. **Measure first**: Run Lighthouse, check Network tab
2. **Identify bottleneck**: LCP? FID? CLS? Large bundle?
3. **Prioritize**: Focus on highest impact issues
4. **Implement fixes**: One at a time, measure impact
5. **Monitor**: Set up continuous monitoring

Always provide specific, measurable improvements with before/after metrics.
