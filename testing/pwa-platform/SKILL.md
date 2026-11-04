---
name: pwa-platform
description: >-
  PWA plumbing for apps/pwa: web app manifest, vite-plugin-pwa / Workbox strategy, update prompt, offline
  behaviour, iOS and Android install quirks, safe areas, Vercel headers and rewrites, demo state persistence
  and persona switching. Use when touching vite.config.ts, the manifest, the service worker, install or
  offline, or when asked "does it work offline / can I install it?".
---

# PWA platform

Owner: the `pwa-engineer` agent. The jury opens a link on an unknown phone, possibly on poor conference Wi-Fi.
The prototype must load fast, survive a flaky network, and install cleanly.

## Manifest (`vite-plugin-pwa` `manifest` option)

| Field                             | Value                                                                                                    |
| --------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `name`, `short_name`              | our working name (never "mObywatel" alone; the `prototype-guardrails` skill)                             |
| `lang`, `dir`                     | `pl`, `ltr`                                                                                              |
| `start_url`, `scope`              | `/`, `/` (keep `?osoba=` params working, see below)                                                      |
| `display`                         | `standalone`                                                                                             |
| `orientation`                     | `portrait`                                                                                               |
| `theme_color`, `background_color` | from `@mobywatel/brand` tokens (import in `vite.config.ts`, no literals)                                 |
| `icons`                           | 192 and 512 PNG, plus a 512 `purpose: "maskable"`; files in `public/icons/` (the `brand-designer` agent) |
| `description`                     | one plain-Polish sentence including "nieoficjalny prototyp"                                              |

## Service worker strategy

- `registerType: 'prompt'`: never swap code under a user mid-matter. Show an "Nowa wersja – odśwież" toast
  (`useRegisterSW` from `virtual:pwa-register/react`) in `src/pwa/`.
- `workbox.globPatterns`: the app shell, fonts, icons and all content JSON, so every persona and scenario
  works offline after the first load.
- `navigateFallback: '/index.html'` for SPA routes. Exclude `/api/` from the fallback.
- Runtime caching only for the optional LLM proxy: `NetworkOnly` (never cache conversations).
- `devOptions.enabled: false` by default. **`pnpm dev` never proves SW or offline behaviour.**
- When offline and the user asks the live assistant, fall back to scripted mode and say so in plain Polish.

## Offline test procedure

1. `pnpm run build && pnpm preview`, then open the app and wait for "ready to work offline" (log or toast).
2. DevTools › Application: manifest has no errors, the SW is activated, and the precache lists the content.
3. Network › Offline, then reload and walk one full matter.
4. Automated: a Playwright flow loads `/`, waits for `navigator.serviceWorker.ready`, then
   `context.setOffline(true)`, reloads, and completes a scenario. It lives in `apps/pwa/e2e/offline.spec.ts`
   (owner: the `qa-engineer` agent).
5. Update flow: build, load, change a string, rebuild, then reload once and expect the update toast.

## iOS (Safari) specifics

- No install prompt event. Show an "Add to Home Screen" instruction sheet (Share › Do ekranu początkowego)
  when `navigator.standalone` is false on iOS. Show it once, and it can be dismissed.
- `apple-touch-icon` (180 px) and `<meta name="apple-mobile-web-app-capable" content="yes">`,
  `apple-mobile-web-app-status-bar-style`, `apple-mobile-web-app-title`.
- Layout: `viewport-fit=cover`, `env(safe-area-inset-*)` paddings, `100dvh` not `100vh`.
- An installed app has **its own storage**, separate from Safari. The demo state starts fresh after install.
- Speech recognition support differs (the `ai-assistant` skill), so always offer text.

## Android / Chromium

- Capture `beforeinstallprompt`, show our own "Zainstaluj" button in settings and after the first completed
  matter. Never show it on first paint.

## Demo state

- Persona via URL: `/?osoba=marta` selects the persona and stores it. A persona switcher in settings and on
  the start screen lets the jury try others.
- State (completed matters, reminders, settings) in IndexedDB via `src/platform/storage`, versioned with a
  schema number. Reset on mismatch.
- **"Zresetuj demo"** in settings clears state and returns to the start screen. The jury will poke at it, so
  make reset easy to find.
- Settings (senior mode, text size, language) persist separately from demo state and survive reset.

## Vercel

`apps/pwa/vercel.json`:

- SPA rewrite: everything except files and `/api/*` → `/index.html`.
- Headers: `sw.js` and `manifest.webmanifest` with `Cache-Control: no-cache`; hashed assets `immutable`. Add
  `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin` and a CSP that allows
  only self (plus the proxy if used).
- Deploying and production: the `competition-submission` skill.

## Checks

- Lighthouse (mobile) on the preview or deployed URL: performance ≥ 90, accessibility 100, best practices ≥
  95, installable. The `web-vitals-a11y-audit` skill helps when available.
- JS budget: initial route under ~200 kB gzip. Lazy-load the assistant and each matter.
- Verify with the `verify-change` skill, using a build and not the dev server.
