---
name: pwa-shell
description: "How this arcade ships as an installable PWA: the service worker's cache strategy and version bump, the deliberate no-skipWaiting decision and the update prompt that completes it, what is safe to precache and what is not, and the stale-build trap that makes a fix look like it did not work. Use when touching public/sw.js, the manifest, offline behaviour, caching, or when a change you just built is not showing up in the browser."
---

# The app shell

`public/sw.js` precaches the whole arcade and serves it cache-first, because
both games are static files with no backend. Once installed it works offline
permanently, both games and fonts included.

## The version is the deploy

`CACHE_VERSION` at the top of `sw.js` is the only thing that invalidates a
cache. Bump it on every deploy that changes a precached file. Nothing enforces
this. CI does not check it, and forgetting means returning visitors keep the
old shell until something else evicts it.

It is at `v3`. It has moved twice, so the habit exists; it is not automatic.

## What can be precached, and what cannot

`SHELL` lists hand-authored paths only: the hub, both games' HTML, the
manifest and the icons. All eleven were verified against production and return
200.

**Payload's JS and CSS are deliberately absent.** They carry Vite build hashes
that change every deploy, so a literal list would be wrong the moment it was
written. They are picked up by the runtime cache on first visit, which is the
same visit that loads the page listing them.

Install uses individual `cache.add` calls each with a `.catch`, so one 404
degrades that entry rather than failing the whole install. Do not replace this
with `cache.addAll`, which is atomic and would silently leave a player with no
offline support at all because one icon moved.

## Updates: the two halves

`sw.js` does not call `skipWaiting()` on install. That is deliberate and should
stay: activating a new shell mid-run swaps the code out from under a game in
progress and loses it.

The consequence is the half that was missing until it was fixed. A waiting
worker only takes over once **every** tab on the origin has closed. An
installed PWA on a phone is suspended, not closed, so "close every tab" can
mean never. A player could sit on a months-old build with nothing on screen
to say so.

So the flow is: detect the waiting worker, tell the player, let them choose.

- `src/ui/swUpdate.ts` — `onUpdateReady` and `activateUpdate`
- `src/ui/UpdateBar.tsx` — the prompt, mounted on its own root from `main.tsx`
- `sw.js` — a `message` handler that calls `skipWaiting()` only when asked

Three rules that are easy to get wrong and are covered by tests:

1. **Check `registration.waiting` on load, not only `updatefound`.** The update
   often downloaded on a previous visit. Handling only the event means a player
   who reloaded once never sees the prompt again.
2. **Wait for state `installed`, not `updatefound`.** Prompting earlier offers a
   reload to a worker that has not finished downloading.
3. **Reload on `controllerchange`, guarded.** Reloading straight after
   `postMessage` serves the old shell again from the old worker; reloading
   unguarded is a loop, because that event also fires on a page's first-ever
   registration and Chrome has fired it more than once.

The bar mounts on its own React root rather than inside `App`, because `App`
gets `inert` while the result modal is open. That would make the prompt
unreachable exactly when a run has just ended and a player is most able to
take an update.

## Two traps that cost real time

**The service worker returns a build you already replaced.** This is the single
most common way to conclude a fix did not work when it did. After a rebuild:

```js
const rs = await navigator.serviceWorker.getRegistrations();
await Promise.all(rs.map(r => r.unregister()));
const ks = await caches.keys();
await Promise.all(ks.map(k => caches.delete(k)));
location.reload();
```

**`dist/` is stale until `npm run build` runs.** `tools/serve.js` serves the
built output, not `src/`. A change you just made is not on screen until you
build.

## Verifying it

Registration needs http, never `file://`, so use `node tools/serve.js` rather
than opening the file. `npm run dev` is Vite, and registration is guarded by
`import.meta.env.DEV` there on purpose: a worker registered against the dev
server caches module URLs that stop existing on the next restart, and then you
debug the cache instead of the code.

**The in-app browser pane cannot register a service worker at all.** Verified:
a valid same-origin script served 200 with `text/javascript` fails with "An
unknown error occurred when fetching the script", and a `blob:` worker is
refused too. That console error is the environment, not a fault in the app.
Do not chase it there. The update flow's logic is unit-tested against fakes for
this reason; the rest needs a real browser and two deploys.

## Hosting

Netlify. `netlify.toml` sets `Cache-Control: public, max-age=0,
must-revalidate` on `/sw.js`, which is what lets a new worker be discovered at
all. A service worker script served from cache cannot announce its own
replacement. Any host swap has to carry that header rule or updates stop
reaching anyone, and the failure is silent: everything keeps working, on the
old build, forever.
