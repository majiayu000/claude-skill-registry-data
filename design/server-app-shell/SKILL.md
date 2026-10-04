---
name: server-app-shell
description: App Shell architecture — the cached HTML/CSS/JS skeleton (header, nav, footer) served instantly via Service Worker while dynamic content streams in. Use when building PWAs, wiring service-worker caches, inlining critical CSS, or adding offline fallbacks and skeleton loading states.
when_to_use: Designing the root layout and service-worker cache strategy for a PWA; separating static shell from dynamic content; adding offline fallback pages; optimising first-paint with inlined critical CSS.
paths:
  - "**/shell/**/*.{jsx,tsx,js,ts}"
  - "**/layout/**/*.{jsx,tsx}"
  - "**/app/**/*.{jsx,tsx}"
---

# App Shell

## What is an App Shell?

App Shell is the minimal HTML/CSS/JS for your UI framework—header, navigation, footer—cached by Service Worker for instant loading (<200ms). Dynamic content loads separately. Core to PWA architecture.

## Key Principles

1. **Separate Static Shell from Dynamic Content**: Shell (nav, layout, critical CSS) cached forever. Content fetched per request via API.

2. **Service Worker Caching**: First visit caches shell assets. Subsequent loads serve from cache instantly, fetch only data.

3. **Instant Perceived Load**: Show shell immediately with skeleton content. Fill with data as it arrives.

## Best Practices

✅ **DO**:
- Cache shell assets with Service Worker
- Inline critical CSS in `<head>`
- Use skeleton screens while content loads
- Version shell assets for cache invalidation
- Prioritize above-fold content

❌ **DON'T**:
- Include personalized content in shell
- Skip Service Worker registration
- Forget offline fallback page
- Cache API responses with shell (different strategy)
- Block render on non-critical resources

## Code Patterns

### App Shell Component

```jsx
// AppShell.jsx
const AppShell = ({ children }) => (
  <div className="app-shell">
    <Header />          {/* Static - cached */}
    <Navigation />      {/* Static - cached */}
    
    <main className="app-shell__content">
      <Suspense fallback={<ContentSkeleton />}>
        {children}      {/* Dynamic - loaded per route */}
      </Suspense>
    </main>
    
    <Footer />          {/* Static - cached */}
  </div>
);
```

### Service Worker Caching

```javascript
// sw.js
const SHELL_CACHE = 'app-shell-v1';
const SHELL_ASSETS = [
  '/',
  '/index.html',
  '/styles/main.css',
  '/scripts/app.js',
  '/images/logo.svg'
];

// Cache shell on install
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(SHELL_CACHE).then(cache => cache.addAll(SHELL_ASSETS))
  );
});

// Serve shell from cache
self.addEventListener('fetch', (event) => {
  // Shell assets: cache-first
  if (SHELL_ASSETS.includes(new URL(event.request.url).pathname)) {
    event.respondWith(
      caches.match(event.request).then(response => 
        response || fetch(event.request)
      )
    );
  }
  // API calls: network-first
  else if (event.request.url.includes('/api/')) {
    event.respondWith(
      fetch(event.request).catch(() => caches.match('/offline.html'))
    );
  }
});
```

### Critical CSS Inlining

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    /* Critical CSS inlined (~5KB) */
    .header { display: flex; height: 60px; background: #fff; }
    .nav { display: flex; gap: 1rem; }
    .skeleton { 
      background: linear-gradient(90deg, #f0f0f0, #e0e0e0, #f0f0f0);
      animation: shimmer 1.5s infinite;
    }
  </style>
  
  <!-- Non-critical CSS loaded async -->
  <link rel="preload" href="/styles/main.css" as="style" 
        onload="this.onload=null;this.rel='stylesheet'">
</head>
<body>
  <div id="root"></div>
  <script src="/scripts/app.js" defer></script>
</body>
</html>
```

### Offline Fallback

```jsx
// OfflinePage.jsx - Cached for offline access
const OfflinePage = () => (
  <div className="offline-page">
    <h1>You're Offline</h1>
    <p>Check your internet connection and try again.</p>
    <button onClick={() => window.location.reload()}>
      Retry
    </button>
  </div>
);
```

## Related Terminologies

- **PWA** - App Shell is core PWA pattern
- **Template** (UI) - Shell is the root template
- **Skeleton** (UI) - Used in shell while loading
- **Router** (Server) - Routes within shell

## Quality Gates

- [ ] Shell cached by Service Worker
- [ ] Critical CSS inlined
- [ ] Skeleton screens for loading
- [ ] Offline fallback page
- [ ] Shell loads in <200ms
- [ ] Assets versioned for cache invalidation

**Source**: `/docs/server/app-shell.md`
