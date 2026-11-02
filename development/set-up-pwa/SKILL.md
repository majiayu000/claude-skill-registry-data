---
name: set-up-pwa
description: Use when making a frontend installable and offline-capable — sets up vite-plugin-pwa (service worker precaching the app shell, web manifest, auto-update), and optionally persists the TanStack Query cache so cached data is available offline, keeping the SW out of API caching.
---

# Set Up PWA

## 1. Audit current state

```bash
cat .claude/stack-profile.md 2>/dev/null || cat ~/.claude/stack-profile.md 2>/dev/null   # frontend.framework, frontend.meta, package_manager
grep -E '"(vite-plugin-pwa|idb-keyval|@tanstack/react-query-persist-client|@tanstack/query-async-storage-persister|@tanstack/query-sync-storage-persister)"' package.json 2>/dev/null
ls public/manifest.webmanifest public/icon-*.png 2>/dev/null
```

Read `frontend.framework` (step 3) and `package_manager` (commands use pnpm). `frontend.meta` of `nuxt` → `@vite-pwa/nuxt`; `next` → a Serwist-based setup: this skill is the Vite path. **Prerequisites:** `scaffold-frontend-project` (Vite). For offline *data*, `set-up-state-management` (we persist its query cache, not SW-cache the API).

## 2. Decide what to do
- No PWA → full setup (installable + offline shell).
- Installable but no offline data → add query persistence (step 7) if the app should read offline.

## 3. Detect framework
`vite-plugin-pwa` is framework-agnostic. The query-persistence step differs (React `PersistQueryClientProvider`; Vue plugin).

## 4. Install
```bash
pnpm add -D vite-plugin-pwa
```
vite-plugin-pwa 2.x supports Vite 8 and pulls in `workbox-build` / `workbox-window` as peers (pnpm installs them automatically; with `auto-install-peers=false`, add both).

## 5. Configure the plugin

```ts
// vite.config.ts
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [
    // ...react()/vue(), tailwindcss(), etc.
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.svg', 'apple-touch-icon.png'],
      manifest: {
        name: 'My App',
        short_name: 'App',
        theme_color: '#0b1220',
        background_color: '#0b1220',
        display: 'standalone',
        icons: [
          { src: '/icon-192.png', sizes: '192x192', type: 'image/png' },
          { src: '/icon-512.png', sizes: '512x512', type: 'image/png' },
          { src: '/icon-maskable.png', sizes: '512x512', type: 'image/png', purpose: 'maskable' },
        ],
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,svg,png,woff2}'], // precache the shell + static assets
      },
      devOptions: { enabled: false }, // turn on only to debug the SW in dev
    }),
  ],
});
```

## 6. Precache the shell — don't SW-cache the API

The service worker precaches the **app shell** (JS/CSS/HTML/fonts/icons) so the app boots offline. Deliberately **do not** add Workbox runtime caching for your API: TanStack Query already owns server data, and a second cache (the SW) competing with the query cache causes stale/confusing reads. Server data offline = query persistence (next step).

## 7. Offline data via TanStack Query persistence (optional)

```bash
pnpm add @tanstack/react-query-persist-client @tanstack/query-async-storage-persister idb-keyval
```
Persist to **IndexedDB**, and only the queries that opt in:
```tsx
// src/libs/persister.ts
import { del, get, set } from 'idb-keyval';
import { createAsyncStoragePersister } from '@tanstack/query-async-storage-persister';

export const persister = createAsyncStoragePersister({
  storage: {
    getItem: (key) => get<string>(key),
    setItem: (key, value) => set(key, value),
    removeItem: (key) => del(key),
  },
  key: 'query-cache',
});
```
```tsx
// React: replace QueryClientProvider with the persisting variant near the root
import { defaultShouldDehydrateQuery } from '@tanstack/react-query';
import { PersistQueryClientProvider } from '@tanstack/react-query-persist-client';
import { queryClient } from '@/libs/queryClient';
import { persister } from '@/libs/persister';

<PersistQueryClientProvider
  client={queryClient}
  persistOptions={{
    persister,
    maxAge: 1000 * 60 * 60 * 24, // 24h
    buster: import.meta.env.VITE_APP_VERSION ?? '', // a new release drops caches of the old data shape
    dehydrateOptions: {
      // allow-list: only queries marked `meta: { persist: true }` are written to disk
      shouldDehydrateQuery: (query) => defaultShouldDehydrateQuery(query) && query.meta?.persist === true,
    },
  }}
>
  <App />
</PersistQueryClientProvider>
```
Mark a query: `useQuery({ queryKey, queryFn, meta: { persist: true } })`. Never mark `auth.me` or anything private. On logout, `await persister.removeClient()` next to `queryClient.clear()` (`set-up-auth`). Set the query client's `gcTime` ≥ `maxAge` (see `set-up-state-management`) so persisted entries aren't garbage-collected first. Vue: `@tanstack/vue-query` has the same persist-client API through its `persistQueryClient` helper. Why IndexedDB and an allow-list: `pwa-patterns.md`.

## 8. Update flow

`registerType: 'autoUpdate'` ships new versions silently on next load. To prompt instead ("New version available — reload"), use `registerType: 'prompt'` + the `virtual:pwa-register` `registerSW({ onNeedRefresh })` hook to show a toast.

## 9. Verify
```bash
pnpm build && pnpm preview
```
Lighthouse → Installable checks pass. Network → `sw.js` is served with `Cache-Control: no-cache` (`set-up-security-headers` sets it), otherwise users keep an old worker for days. DevTools → Network → Offline: reload still boots the shell; persisted queries render their last data.

## References
- ./pwa-patterns.md — precache-shell-not-API, autoUpdate-vs-prompt, maskable icons, query persistence + gcTime, offline testing.
- ../set-up-state-management/SKILL.md — the query cache being persisted; `gcTime`.
- ../_shared/stack-versions.md — tooling versions.
