---
name: senternet-site-init
description: Generate AGENTS.md, CLAUDE.md, and README.md for a completed site.
---

# Initialize Project Documentation

Generate project documentation for the completed site. Produces three files:
- `AGENTS.md` — comprehensive codebase context for AI agents
- `CLAUDE.md` — one-liner that points to AGENTS.md
- `README.md` — human-facing project overview

## Steps

### 1. Analyze the codebase

Read these files to understand the project:
- `package.json` — app name, scripts, all dependencies
- `src/App.tsx` — routes and page structure
- `vite.config.ts` — build config, plugins, env var handling
- `firebase.json` and `.firebaserc` — hosting config and project names
- `.env.production` (and `.env.development` if present) — which services are enabled
- `scripts/prerender.mjs` — all prerendered routes and the ROUTES array
- `scripts/generate-sitemap.mjs` — sitemap routes, SITE_URL, LOCALES
- `index.html` — meta tags, structured data, third-party scripts present

### 2. Create `AGENTS.md`

Write a complete `AGENTS.md`. Use the actual values you read from the project — do not use placeholder text.

Structure it as follows:

---

#### What this project is

One paragraph: the site's purpose, product name, target audience, and production domain.

#### Tech stack

- **Vite + React + TypeScript** — scaffolded with `outDir: 'build'`
- **Tailwind CSS v4** — imported via `@import "tailwindcss"` in `src/index.css`
- **Firebase Hosting** — static hosting, `build/` as public dir
- **Puppeteer prerendering** — every route gets a real HTML snapshot at build time

List the actual version of each major dependency from `package.json`.

#### Critical architectural decisions

For each item below, state the rule and why it matters — these are traps that cost hours if ignored:

**`hydrateRoot` not `createRoot`** — `src/main.tsx` must use `hydrateRoot` so React attaches to prerendered DOM without replacing it. Using `createRoot` destroys the LCP from the initial HTML paint.

**`outDir: 'build'`** — Firebase and prerender scripts expect `build/`, not Vite's default `dist/`. Changing this breaks both.

**`htmlPlugin` in `vite.config.ts`** — rewrites `VITE_BASE_URL` into meta tag `content` and canonical `href` at build time, conditionally injects or strips the GA block based on `VITE_GA_ID`, and injects `<link rel="modulepreload">` tags for all JS chunks. Describe what transformations it actually performs based on what you read.

**`app-ready` event** — `main.tsx` dispatches `document.dispatchEvent(new Event('app-ready'))` after hydration (with a 1s timeout fallback). The prerender script waits for this before capturing HTML. If a route renders as `✗ EMPTY`, the page component is not calling this dispatch in its `useEffect`.

**`window.__PRERENDERING__ = true`** — set by the prerender script before visiting each route. Use this flag to skip animations, API calls, or interactivity that breaks in headless Chrome.

#### Build pipeline

Show the actual command chains from `package.json`:

```
npm run build:prod
→ [list each step in order]

npm run deploy:prod
→ [list each step in order]
```

#### The three-file rule

Every new page/route must update all three of these files together — missing any one leaves the page without static HTML for crawlers, without a sitemap entry, or both:

1. `src/App.tsx` — add the `<Route>`
2. `scripts/prerender.mjs` — add to the `ROUTES` array
3. `scripts/generate-sitemap.mjs` — add to the `ROUTES` array

Optionally: `scripts/generate-share-images.mjs` — add a share image block if the page needs an OG image.

#### Environment variables

List every variable from `.env.*` files with what it controls and which environments it appears in.

#### Third-party services

List each service wired into the site (GA4, Reddit pixel, IndexNow, etc.) and where it's configured (which file, which env var).

#### Firebase projects

List dev and prod project names from `.firebaserc`. Note which deploy script targets which project.

#### Target Lighthouse scores (mobile)

- Performance ≥ 94
- Accessibility ≥ 98
- Best Practices ≥ 96
- SEO = 100

---

### 3. Create `CLAUDE.md`

Write a `CLAUDE.md` containing only this line:

```
See AGENTS.md for rules
```

If a `CLAUDE.md` already exists, replace its contents entirely.

### 4. Create `README.md`

Write a `README.md` with these sections (use real values from the project — no placeholders):

**Project name and tagline** — one sentence describing what the site is for.

**Live URLs** — production URL. Add staging/dev URL if a dev Firebase project exists.

**Quick start**
```bash
npm install
npm run dev        # http://localhost:5173
```

**Build and deploy**
```bash
npm run build:prod     # sitemap → tsc → vite build → prerender
npm run deploy:prod    # build:prod → firebase deploy → IndexNow
```

**Scripts** — table of all npm scripts from `package.json` and what each does.

| Script | What it does |
|---|---|
| `dev` | … |
| `build:prod` | … |
| … | … |

**Architecture** — brief bullet list matching the tech stack section in AGENTS.md.

**The three-file rule** — copy from AGENTS.md verbatim (keep it in both places so it's impossible to miss).

**Firebase projects** — table of environment → project name → deploy script.

## Verification

After writing all three files:
1. Confirm `AGENTS.md` has no placeholder text — every value should be the real project value
2. Confirm `CLAUDE.md` contains only `See AGENTS.md for rules`
3. Confirm `README.md` has correct domain, project names, and script list

## Framework: Next.js track

Docs that describe the wrong track are worse than no docs — every trap listed in the Vite version is either absent or inverted here. Detect the track from `.site-framework.json` before writing anything.

### Read these instead

`package.json`, `next.config.ts`, `apphosting.yaml`, `app/layout.tsx`, `config/routes.mjs`, `app/sitemap.ts`, `app/robots.ts`, `.firebaserc`, `.env.*`, and the `app/` tree (every directory containing a `page.tsx` is a route).

### Tech stack section

- **Next.js (App Router) + TypeScript** — default `.next/` output, never overridden
- **Tailwind CSS v4** — imported via `@import "tailwindcss"` in `app/globals.css`
- **Firebase App Hosting** — SSR on Cloud Run, deployed from the connected git branch
- **Built-in static rendering** — no prerender step exists

### Critical architectural decisions section

Replace the Vite traps entirely. The ones that cost hours on this track:

**No `hydrateRoot`, no `app-ready`, no `window.__PRERENDERING__`.** These are Vite-track artifacts. Finding one in this repo means a Vite-track step was applied to the wrong project.

**Server components by default.** `'use client'` belongs on the leaf that needs state or handlers, never on a page. Pushing it up the tree ships the whole subtree to the browser and gives back the main reason to be on this framework.

**Static vs dynamic rendering.** `npm run build` prints a route table; marketing routes must be `○` (static), not `ƒ` (dynamic). A stray `cookies()`, `headers()`, or unsuspended `useSearchParams()` read silently flips a page to per-request rendering and a cold start.

**`metadataBase` in `app/layout.tsx`.** Without it, relative OG image URLs ship as relative paths that crawlers cannot fetch.

**`apphosting.yaml` is the real production env.** A variable in `.env.production` but not in `apphosting.yaml` is `undefined` in the deployed build. Client-read variables need the `NEXT_PUBLIC_` prefix *and* `BUILD` availability. Secrets are `secret:` refs with `RUNTIME` availability only.

**Headers live in `next.config.ts`, not `firebase.json`.** `firebase.json` `headers` is not read on this track.

### Build pipeline section

```
npm run build      → next build (renders static HTML for every static route)
npm run deploy:prod → firebase apphosting:rollouts:create → wait for READY → node scripts/indexnow.mjs
```

Note that pushing to the connected branch also triggers a rollout.

### Page-add rule section

Use the **one-file rule**, not the three-file rule:

1. `app/<segment>/page.tsx` — the page plus its own `export const metadata`
2. `config/routes.mjs` — add the route (`indexable: false` for legal pages)

`app/sitemap.ts`, `app/robots.ts`, and `scripts/indexnow.mjs` all read the manifest, so there is no third list and no prerender array.

### README section

Quick start is `npm run dev`; the local production check is `npm run build && npm start` (not a served `build/` directory). Keep the Lighthouse targets as-is.

See `/senternet-site-framework` for the full convention map.
