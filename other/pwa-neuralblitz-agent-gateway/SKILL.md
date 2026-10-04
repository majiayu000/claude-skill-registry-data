---
name: pwa
description: Progressive Web Apps with offline support and installability
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: web-development
---
## What I do
- Build installable web apps
- Implement offline functionality
- Create service workers
- Configure web app manifests
- Handle background sync

## When to use me
When creating web apps that work offline and can be installed.

## Service Worker
```javascript
self.addEventListener('install', e => {
  e.waitUntil(caches.open('v1').then(c => c.addAll(['/'])));
});

self.addEventListener('fetch', e => {
  e.respondWith(caches.match(e.request).then(r => r || fetch(e.request)));
});
```
