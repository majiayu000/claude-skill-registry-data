---
name: pwa-service-worker
description: "Progressive Web Apps, Service Worker lifecycle, offline asset caching, and web app manifests."
---

# Progressive Web Apps (PWA) Protocol

Enable offline reliability, app installation, and background sync.

---

## 1. Service Worker Caching Strategies

- **Cache-First**: Static immutable assets (fonts, hashed bundles, logos).
- **Network-First**: Dynamic user data and transaction endpoints.
- **Stale-While-Revalidate**: Read-heavy news feeds and read-only catalogs.

---

## 2. Lifecycle & Updates

Prompt users cleanly when an updated service worker is waiting via `skipWaiting()` and page reload.
