---
name: service-worker-offline
description: Use when making a web app work without a network connection using a service worker — caching the app shell and selected content for offline use, an explicit "save for offline" action, queuing user actions while offline and syncing them later, cache versioning and updates, and testing offline behaviour with Playwright. Also use when users see an old version after deploys, offline answers are lost, or the cache grows without limit.
---

# Service worker and offline use

Default: a hand-written service worker (or Workbox) that precaches the app shell at install, caches content on demand when the user asks, records writes in IndexedDB while offline and replays them when online, with a versioned cache name per deploy.

## Strategy per resource

| Resource | Strategy |
|---|---|
| App shell (HTML, JS, CSS) | Precache at install, versioned; serve cache-first |
| API reads for content the user saved | Cache on an explicit "save for offline" action; network-first with cache fallback |
| API writes (answers, progress) | Never cache; queue in IndexedDB when offline |
| Authenticated or personal HTML | Do not put in shared caches; scope per user or do not cache |

## Saving content deliberately

Let the user choose what to take offline ("save before going out"): fetch the selected sets and store them; show what is saved and how much space it uses; allow removing it. Implicit caching of everything fills storage and surprises users.

## Offline writes

1. Write the action (e.g. an answer with timestamp and a client-generated ID) to IndexedDB immediately and update the UI.
2. When `online` fires (and on app start), send queued actions in order; the server treats the client ID as an idempotency key so retries do not duplicate.
3. Remove items only after the server confirms.

## Updates

- Change the cache name on every deploy (include the build hash); delete old caches in `activate`.
- A new worker waits until all tabs close. Either show "update available — reload" (call `skipWaiting` on user confirmation) or skip waiting automatically if mixing versions is safe.
- Never cache the service worker script itself with a long HTTP cache lifetime.

## Verification loop (Playwright)

1. Load the app, save a content set, wait for the worker to be ready.
2. `context.setOffline(true)`; reload; the shell and saved content work.
3. Perform an action offline; it appears as pending.
4. `context.setOffline(false)`; the queue flushes; the server has the record exactly once.

## Pitfalls

- **Scope:** a worker controls only paths under its own location; serve it from the site root for a whole-site scope.
- **HTTPS only** (except `localhost`).
- **Opaque responses** (cross-origin without CORS) take storage quota without being inspectable; avoid caching them.
- **Storage eviction:** browsers may clear storage under pressure; request persistence (`navigator.storage.persist()`) and handle missing data gracefully.
- **Debugging:** the browser's application panel shows workers and caches; "update on reload" helps during development only.
