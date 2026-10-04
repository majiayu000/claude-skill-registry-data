---
license: Apache-2.0
name: pwa-expert
description: Progressive Web App development with Service Workers, offline support, and app-like behavior. Use for caching strategies, install prompts, push notifications, background sync. Activate on "PWA", "Service Worker", "offline", "install prompt", "beforeinstallprompt", "manifest.json", "workbox", "cache-first". NOT for native app development (use React Native), general web performance (use performance docs), or server-side rendering.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
category: Frontend & UI
tags:
  - pwa
  - progressive-web-app
  - service-worker
  - offline
  - installable
---

# Progressive Web App Expert

Build installable, offline-capable web apps with Service Workers, smart caching, and native-like experiences.

## Decision Points

### Resource Caching Strategy Selection

```
REQUEST TYPE?
├─ Static assets (CSS, JS, fonts, images)
│  └─ CACHE-FIRST: Check cache → fallback to network
├─ API data that changes frequently
│  ├─ User expects fresh data?
│  │  └─ NETWORK-FIRST: Try network → fallback to cache
│  └─ Performance over freshness?
│     └─ STALE-WHILE-REVALIDATE: Serve cache → update in background
└─ Authentication/Real-time data
   └─ NETWORK-ONLY: Always fetch, no cache
```

### Connectivity Detection Logic

```
CONNECTIVITY STATUS?
├─ navigator.onLine === false
│  └─ Serve from cache OR show offline page
├─ Request fails (fetch throws)
│  ├─ Resource in cache?
│  │  └─ Serve cached version
│  └─ No cache available?
│     └─ Show offline fallback
└─ Online AND request succeeds
   └─ Update cache with fresh data
```

### Install Prompt Timing

```
beforeinstallprompt FIRED?
├─ User just arrived (< 30 seconds on site)?
│  └─ DEFER: Store prompt, don't show yet
├─ User engaged (scrolled, clicked, 2+ page views)?
│  ├─ Mobile device?
│  │  └─ SHOW: Mobile users expect app install
│  └─ Desktop?
│     └─ CONTEXTUAL: Show near task completion
└─ User dismissed before?
   └─ WAIT: Don't show again for 7+ days
```

## Failure Modes

### Stale Cache Syndrome
**Symptom:** Users see outdated content, complain "app isn't working"
**Detection:** User reports + cache timestamp > expected refresh interval
**Fix:** Force cache update with `caches.delete()` + trigger fresh fetch

### Service Worker Registration Failure
**Symptom:** PWA features not working, install prompt never appears
**Detection:** Console error "Failed to register service worker" OR `navigator.serviceWorker` undefined
**Fix:** Check HTTPS requirement (HTTP only works on localhost), validate SW file path, verify manifest linked in HTML

### Zombie Service Worker
**Symptom:** App updates not appearing, old SW keeps running
**Detection:** `registration.waiting` exists but `skipWaiting()` not called
**Fix:** Implement update flow with `postMessage()` to SW + `skipWaiting()` + `clients.claim()`

### Manifest Validation Failure
**Symptom:** "Add to Home Screen" never appears, PWA audit fails
**Detection:** DevTools Application tab shows manifest errors OR Lighthouse PWA score < 80
**Fix:** Validate required fields (name, start_url, display, icons 192x192 + 512x512), ensure HTTPS, check icon paths exist

### Cache Storage Explosion
**Symptom:** App slows down, storage quota exceeded errors
**Detection:** Cache storage > 50MB OR "QuotaExceededError" in console
**Fix:** Implement cache expiration (`maxEntries`, `maxAgeSeconds`), clean old cache versions in SW activate event

## Worked Examples

### Complete PWA Setup for Recovery Support App

**Scenario:** Convert existing Next.js recovery support app to installable PWA with offline meeting finder

**Step 1: Assess Current State**
- Check: HTTPS? ✓ (required for SW)  
- Check: manifest.json? ✗ (need to create)
- Check: Service Worker? ✗ (need to implement)

**Step 2: Decision - Caching Strategy**
```
Meeting data API → Changes daily → NETWORK-FIRST
User profile images → Rarely change → CACHE-FIRST  
Static assets → Never change per version → CACHE-FIRST
Meeting search → Mix strategy → STALE-WHILE-REVALIDATE
```

**Step 3: Create manifest.json**
```json
{
  "name": "Recovery Meetings Finder",
  "short_name": "Meetings",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#1a1410",
  "theme_color": "#1a1410",
  "icons": [
    {"src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png"}
  ]
}
```

**Step 4: Implement Service Worker**
```javascript
// public/sw.js - Network-first for API
self.addEventListener('fetch', (event) => {
  if (event.request.url.includes('/api/meetings')) {
    event.respondWith(networkFirst(event.request));
  }
});
```

**Expert catches:** Novice would miss offline fallback page, expert adds catch-all route to serve cached "/offline" for navigation requests that fail.

## Quality Gates

- [ ] Lighthouse PWA audit score ≥ 80/100
- [ ] Service Worker registers without console errors  
- [ ] Manifest.json validates (name, start_url, display, icons present)
- [ ] App works offline (test with DevTools Network → Offline)
- [ ] Install prompt appears on supported devices/browsers
- [ ] Cache strategy appropriate for each resource type
- [ ] Update flow notifies users when new version available
- [ ] Icons display correctly in system app drawer/desktop
- [ ] App launches in standalone mode when installed
- [ ] Background sync queues actions when offline (if implemented)

## Not-For Boundaries

**Do NOT use this skill for:**

- **Native mobile app development** → Use `react-native-expert` or `flutter-expert` instead
- **General web performance optimization** → Use `web-performance-expert` for non-PWA performance issues  
- **Server-side rendering problems** → Use `nextjs-expert` or framework-specific skills
- **Push notification infrastructure** → Use `push-notification-expert` for complex notification systems
- **Simple marketing sites** → PWA overhead not justified; use standard web development
- **Legacy browser support** → PWAs require modern browser features; use progressive enhancement approaches

**When to delegate:**
- Complex background sync with database conflicts → `data-sync-expert`
- Advanced caching with CDN integration → `cdn-expert` 
- Cross-platform native features → `capacitor-expert` or `electron-expert`
## Imported bundle navigation

These preserved source files add depth when their stated topic is needed.

- [references/background-sync.md](references/background-sync.md) — Background Sync.
- [references/install-prompt.md](references/install-prompt.md) — Install Prompt Implementation.
- [references/nextjs-integration.md](references/nextjs-integration.md) — Next.js PWA Integration.
- [references/offline-handling.md](references/offline-handling.md) — Offline Handling.
- [references/service-worker-patterns.md](references/service-worker-patterns.md) — Service Worker Patterns.
- [references/update-flow.md](references/update-flow.md) — PWA Update Flow.
