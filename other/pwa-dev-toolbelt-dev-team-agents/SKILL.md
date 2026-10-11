---
name: pwa
description: PWA — manifest, service worker caching strategies, update lifecycle.
---

## Manifest (`manifest.json` / `manifest.webmanifest`)

Required fields: `name`, `short_name`, `description`, `start_url`, `display`, `theme_color`, `background_color`, `scope`

Provide icons at 192×192 and 512×512 (PNG); include a maskable icon variant.

## Service Worker

Choose a caching strategy per resource type:

| Resource | Strategy |
|----------|----------|
| App shell (HTML, JS, CSS) | Cache First |
| API responses | Network First with cache fallback |
| Static assets (images, fonts) | Stale While Revalidate |

Use Workbox (via Vite PWA plugin, `@angular/service-worker`, Nuxt PWA module, etc.) unless there is a specific reason not to.

Handle the SW update lifecycle: detect when a new version is available and prompt the user to reload — never silently swap the service worker while the app is open.

## PWA Checklist

- [ ] Lighthouse PWA audit passes (installable + PWA optimized)
- [ ] HTTPS enforced (required for service worker registration)
- [ ] Offline fallback page defined and cached
- [ ] Install prompt handled (`beforeinstallprompt` event)
- [ ] Push notifications configured if required (request permission only on explicit user action — never on page load)
