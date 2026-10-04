---
name: add-pwa-feature
description: Add Progressive Web App capabilities — manifest, service worker, offline cache, install prompt, or background sync. Use when building mobile-first features.
---

# add-pwa-feature

Adds PWA capabilities to the application. Can be invoked incrementally — each call adds one capability (manifest, offline, push, install prompt, background sync).

## Inputs to gather

- **Capability** — one of: `manifest`, `offline-cache`, `push-notifications`, `install-prompt`, `background-sync`
- **Cache strategy** — for offline: `cache-first` (static assets) or `stale-while-revalidate` (API data)
- **Sync queue** — for background-sync: which mutations to queue offline

## Steps

### manifest (first time only)

1. Create `apps/web/public/manifest.json`:
   ```json
   {
     "name": "عقاركم — منصة العقارات",
     "short_name": "عقاركم",
     "description": "منصة إدارة العقارات السعودية",
     "start_url": "/home/platform",
     "display": "standalone",
     "orientation": "portrait",
     "dir": "rtl",
     "lang": "ar",
     "theme_color": "#0F172A",
     "background_color": "#FFFFFF",
     "icons": [
       { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
       { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" }
     ]
   }
   ```

2. Add `<link rel="manifest" href="/manifest.json">` to `index.html`.

### offline-cache

1. Create `apps/web/public/sw.js` (service worker):
   - Cache app shell (HTML, CSS, JS bundles) on install
   - Stale-while-revalidate for API responses
   - Fallback offline page for navigation requests

2. Register in `apps/web/src/main.tsx`:
   ```typescript
   if ("serviceWorker" in navigator) {
     navigator.serviceWorker.register("/sw.js");
   }
   ```

3. Add offline indicator component:
   ```tsx
   function OfflineBanner() {
     const [online, setOnline] = useState(navigator.onLine);
     // Listen to online/offline events
     return !online ? <Banner>أنت غير متصل</Banner> : null;
   }
   ```

### background-sync

1. Queue failed mutations in IndexedDB when offline
2. Service worker: listen for `sync` event → replay queued mutations
3. Show sync indicator: "جاري مزامنة X تغييرات..."

### install-prompt

1. Listen for `beforeinstallprompt` event
2. Show custom install banner: "أضف عقاركم للشاشة الرئيسية"
3. Store dismissal in localStorage (don't show again for 30 days)

## Verification checklist

- [ ] Manifest loads correctly (check DevTools → Application → Manifest)
- [ ] Service worker registers and caches shell assets
- [ ] App works offline (shows cached data + offline banner)
- [ ] Offline mutations queue and replay on reconnect
- [ ] Install prompt appears on mobile browsers
- [ ] `/typecheck` passes

## Anti-patterns

- Don't cache API responses aggressively — use stale-while-revalidate with short TTL
- Don't cache authenticated endpoints indefinitely — respect auth tokens
- Don't block app startup waiting for service worker — register async
- Don't show install prompt immediately — wait until user has visited 3+ times
