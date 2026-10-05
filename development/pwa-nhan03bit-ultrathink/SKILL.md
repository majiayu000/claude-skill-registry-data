---
name: pwa
description: Progressive Web Apps with service workers, web app manifest, offline-first architecture, and push notifications
layer: domain
category: mobile
triggers:
  - "PWA"
  - "progressive web app"
  - "service worker"
  - "offline first"
  - "web app manifest"
  - "install prompt"
  - "workbox"
  - "cache strategy"
inputs:
  - requirements: Offline capabilities, push notifications, installability
  - framework: Next.js | React | SvelteKit | Vanilla (optional)
  - caching_strategy: Cache-first | Network-first | Stale-while-revalidate
  - features: Background sync, push notifications, share target, file handling
outputs:
  - manifest: Web app manifest configuration
  - service_worker: Service worker with caching strategies
  - install_prompt: Install experience implementation
  - offline_strategy: Offline data handling and sync
linksTo:
  - react
  - nextjs
  - caching
  - performance-profiler
linkedFrom:
  - cook
  - plan
  - nextjs
preferredNextSkills:
  - nextjs
  - caching
fallbackSkills:
  - react
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects: []
---

# Progressive Web Apps (PWA) Skill

## Purpose

Build Progressive Web Apps that work offline, are installable on home screens, and provide native-like experiences using web technologies. This skill covers the Web App Manifest, Service Worker lifecycle, caching strategies (Workbox), background sync, push notifications, and the install experience. PWAs bridge the gap between web and native without app store requirements.

## Key Concepts

### PWA Requirements

```
REQUIRED (for installability):
  - HTTPS (or localhost for development)
  - Web App Manifest with required fields
  - Service Worker with fetch handler
  - At least one icon (192x192 and 512x512)

ENHANCED CAPABILITIES:
  - Offline support via caching strategies
  - Push notifications
  - Background sync
  - Share target (receive shared content)
  - File handling
  - Shortcuts (quick actions from icon)
  - Badging API (notification badge on icon)
```

### Caching Strategies

```
CACHE FIRST (Cache Falling Back to Network):
  Best for: Static assets, fonts, images, CSS, JS bundles
  Behavior: Check cache first. If miss, fetch from network and cache.
  Tradeoff: Fast but may serve stale content.

NETWORK FIRST (Network Falling Back to Cache):
  Best for: API responses, dynamic content, user-specific data
  Behavior: Try network first. If offline/slow, fall back to cache.
  Tradeoff: Always fresh when online, cached when offline.

STALE-WHILE-REVALIDATE:
  Best for: Semi-dynamic content (avatars, product lists, articles)
  Behavior: Return cached immediately, fetch update in background.
  Tradeoff: Instant but may show stale data briefly.

NETWORK ONLY:
  Best for: Analytics pings, real-time data, payment processing
  Behavior: Always fetch from network. No caching.

CACHE ONLY:
  Best for: Pre-cached app shell, offline fallback page
  Behavior: Only serve from cache. Never network.
```

## Patterns

### Web App Manifest

```json
{
  "name": "My Application",
  "short_name": "MyApp",
  "description": "A progressive web application",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#0066cc",
  "orientation": "portrait-primary",
  "scope": "/",
  "icons": [
    {
      "src": "/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ],
  "shortcuts": [
    {
      "name": "New Post",
      "short_name": "New",
      "url": "/new",
      "icons": [{ "src": "/icons/new.png", "sizes": "96x96" }]
    }
  ],
  "screenshots": [
    {
      "src": "/screenshots/home.png",
      "sizes": "1280x720",
      "type": "image/png",
      "form_factor": "wide",
      "label": "Home screen"
    }
  ]
}
```

### Service Worker with Workbox

```typescript
// sw.ts (compiled with workbox-webpack-plugin or @vite-pwa/workbox)
import { precacheAndRoute } from 'workbox-precaching';
import { registerRoute } from 'workbox-routing';
import {
  CacheFirst,
  NetworkFirst,
  StaleWhileRevalidate,
} from 'workbox-strategies';
import { ExpirationPlugin } from 'workbox-expiration';
import { CacheableResponsePlugin } from 'workbox-cacheable-response';

// Precache app shell (injected at build time)
precacheAndRoute(self.__WB_MANIFEST);

// Cache static assets (Cache First)
registerRoute(
  ({ request }) =>
    request.destination === 'style' ||
    request.destination === 'script' ||
    request.destination === 'font',
  new CacheFirst({
    cacheName: 'static-assets',
    plugins: [
      new ExpirationPlugin({ maxEntries: 60, maxAgeSeconds: 30 * 24 * 60 * 60 }),
      new CacheableResponsePlugin({ statuses: [0, 200] }),
    ],
  }),
);

// Cache images (Cache First with size limit)
registerRoute(
  ({ request }) => request.destination === 'image',
  new CacheFirst({
    cacheName: 'images',
    plugins: [
      new ExpirationPlugin({ maxEntries: 100, maxAgeSeconds: 7 * 24 * 60 * 60 }),
    ],
  }),
);

// Cache API responses (Network First)
registerRoute(
  ({ url }) => url.pathname.startsWith('/api/'),
  new NetworkFirst({
    cacheName: 'api-responses',
    networkTimeoutSeconds: 5,
    plugins: [
      new ExpirationPlugin({ maxEntries: 50, maxAgeSeconds: 24 * 60 * 60 }),
    ],
  }),
);

// Cache pages (Stale While Revalidate)
registerRoute(
  ({ request }) => request.mode === 'navigate',
  new StaleWhileRevalidate({
    cacheName: 'pages',
    plugins: [
      new CacheableResponsePlugin({ statuses: [200] }),
    ],
  }),
);

// Offline fallback
self.addEventListener('fetch', (event) => {
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request).catch(() => caches.match('/offline.html')),
    );
  }
});
```

### Install Prompt

```typescript
'use client';

import { useEffect, useState } from 'react';

interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
}

export function useInstallPrompt() {
  const [deferredPrompt, setDeferredPrompt] = useState<BeforeInstallPromptEvent | null>(null);
  const [isInstalled, setIsInstalled] = useState(false);

  useEffect(() => {
    // Check if already installed
    if (window.matchMedia('(display-mode: standalone)').matches) {
      setIsInstalled(true);
      return;
    }

    const handler = (e: Event) => {
      e.preventDefault();
      setDeferredPrompt(e as BeforeInstallPromptEvent);
    };

    window.addEventListener('beforeinstallprompt', handler);
    window.addEventListener('appinstalled', () => setIsInstalled(true));

    return () => window.removeEventListener('beforeinstallprompt', handler);
  }, []);

  async function install() {
    if (!deferredPrompt) return false;
    await deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    setDeferredPrompt(null);
    return outcome === 'accepted';
  }

  return {
    canInstall: !!deferredPrompt && !isInstalled,
    isInstalled,
    install,
  };
}

// Usage
function InstallBanner() {
  const { canInstall, install } = useInstallPrompt();

  if (!canInstall) return null;

  return (
    <div className="p-6 rounded-xl shadow-sm border bg-blue-50">
      <p className="text-base">Install this app for a better experience</p>
      <button
        onClick={install}
        className="mt-4 px-6 py-4 min-h-[2.625rem] text-base rounded-lg
                   bg-blue-600 text-white hover:bg-blue-700
                   focus-visible:ring-2 focus-visible:ring-offset-2
                   transition-all duration-200"
      >
        Install App
      </button>
    </div>
  );
}
```

### Background Sync

```typescript
// In service worker
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-pending-actions') {
    event.waitUntil(syncPendingActions());
  }
});

async function syncPendingActions() {
  const db = await openDB('pending-actions');
  const actions = await db.getAll('queue');

  for (const action of actions) {
    try {
      await fetch(action.url, {
        method: action.method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(action.body),
      });
      await db.delete('queue', action.id);
    } catch {
      // Will retry on next sync event
      break;
    }
  }
}

// In application code
async function submitFormOfflineCapable(data: FormData) {
  try {
    await fetch('/api/submit', { method: 'POST', body: data });
  } catch {
    // Queue for background sync
    const db = await openDB('pending-actions');
    await db.add('queue', {
      url: '/api/submit',
      method: 'POST',
      body: Object.fromEntries(data),
      timestamp: Date.now(),
    });

    // Register sync
    const registration = await navigator.serviceWorker.ready;
    await registration.sync.register('sync-pending-actions');
  }
}
```

### Next.js PWA Setup

```typescript
// next.config.ts
import withPWA from 'next-pwa';

const config = withPWA({
  dest: 'public',
  register: true,
  skipWaiting: true,
  disable: process.env.NODE_ENV === 'development',
  runtimeCaching: [
    {
      urlPattern: /^https:\/\/api\.example\.com\/.*/i,
      handler: 'NetworkFirst',
      options: {
        cacheName: 'api-cache',
        expiration: { maxEntries: 50, maxAgeSeconds: 86400 },
      },
    },
  ],
})({
  // Standard Next.js config
});

export default config;
```

## Best Practices

1. **HTTPS is mandatory** -- service workers only work over HTTPS (or localhost)
2. **Cache the app shell** -- precache HTML, CSS, JS for instant load
3. **Network-first for API data** -- always try fresh data first, cache as fallback
4. **Provide an offline page** -- show a meaningful offline experience, not a browser error
5. **Keep service worker small** -- heavy SW delays page load; use Workbox for code splitting
6. **Handle SW updates gracefully** -- prompt users to refresh when a new version is available
7. **Test offline thoroughly** -- use Chrome DevTools offline mode during development
8. **Responsive icons** -- provide maskable icons for Android adaptive icons
9. **Background sync for forms** -- queue submissions when offline, sync when back online
10. **Measure with Lighthouse** -- PWA audit checks all requirements automatically

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| No offline fallback | Browser error page when offline | Add offline.html and SW fallback |
| Caching auth-gated content | Stale or wrong user data served | Exclude auth routes from cache |
| SW caches HTML forever | Users never see updates | Use Stale-While-Revalidate for pages |
| No SW update strategy | Users stuck on old version | Prompt to refresh on new SW activation |
| Missing maskable icon | Poor appearance on Android | Provide icon with `"purpose": "maskable"` |
| Not testing offline | Broken offline experience shipped | Test in Chrome DevTools offline mode |
