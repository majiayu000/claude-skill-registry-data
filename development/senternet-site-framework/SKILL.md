---
name: senternet-site-framework
description: The framework contract for Senternet sites — pick and record a track (Vite or Next.js), detect the active track in an existing repo, and translate every site convention between tracks.
---

# Site Framework Contract

Every Senternet site runs on one **track**. A track is a framework plus a host plus the set of conventions the other site skills assume. This skill is the single source of truth for which tracks exist, how to choose one, how to detect the one already in use, and how each convention maps between them.

Read this before running any site skill on a project whose framework you have not confirmed.

## Supported tracks

| Track | Framework | Host | Scaffold skill |
|---|---|---|---|
| `vite` | Vite + React + TypeScript + React Router | Firebase Hosting (static CDN) | `/senternet-site-vite-setup` |
| `nextjs` | Next.js (App Router) + TypeScript | Firebase App Hosting (SSR on Cloud Run) | `/senternet-site-nextjs-setup` |

Both tracks must deliver the same outcome: real HTML for every route, correct per-page metadata, a sitemap and robots.txt, IndexNow submission, security headers, and the target Lighthouse scores.

## Choosing a track

Default to **`vite`**. It is the cheaper, faster, more predictable track for a marketing site: static files on a CDN, no cold starts, no per-request compute, and every skill in this suite is written against it first.

Choose **`nextjs`** when the site needs something the static track cannot do:

- Server rendering or incremental regeneration for content that changes without a deploy
- Server-side API endpoints in the same codebase (form handlers, webhooks, auth callbacks) instead of separate Firebase Functions
- Per-request logic: geo/locale redirects, A/B assignment, personalization, gated content
- Middleware, and with it a per-request nonce CSP instead of a hash list
- A large or frequently changing content set where a Puppeteer prerender pass over every route has become the slow part of the build

Do not choose `nextjs` for "it might need SSR later." Moving a static marketing site onto SSR later is a smaller job than paying for cold starts and a heavier build the whole time.

## Recording the track

Whichever track is chosen, the scaffold skill writes `.site-framework.json` in the site root:

```json
{
  "framework": "vite",
  "renderMode": "static-prerender",
  "host": "firebase-hosting"
}
```

or

```json
{
  "framework": "nextjs",
  "renderMode": "ssr-app-hosting",
  "host": "firebase-app-hosting"
}
```

Every later skill reads this file first. It exists so upfit runs never have to guess, and so a half-migrated repo (both `vite.config.ts` and `next.config.ts` present) has a declared answer.

## Detecting the track in an existing repo

1. `.site-framework.json` exists → use its `framework` value. Stop here.
2. `next.config.{ts,js,mjs}` exists, or `package.json` has `next` in `dependencies`, or an `app/` directory contains `layout.tsx` → `nextjs`. Write `.site-framework.json` to record it.
3. `vite.config.{ts,js}` exists, or `package.json` has `vite` in `devDependencies` → `vite`. Write `.site-framework.json` to record it.
4. Neither → the repo has not been scaffolded. Ask which track to use and run the matching scaffold skill.
5. Both, and no marker file → stop and ask the user which one is authoritative. Do not guess, and do not run skills against both.

## Convention map

When a skill's steps are written for one track, use this table to translate them to the other. Anything not listed here is identical across tracks.

| Concern | `vite` track | `nextjs` track |
|---|---|---|
| Build output dir | `build/` (explicit `outDir` override) | `.next/` (framework-managed — never override) |
| Dev server | `vite --port $PORT` | `next dev --port $PORT` |
| Production build | `tsc -b && vite build && node scripts/prerender.mjs` | `next build` |
| Deploy | `firebase deploy --only hosting --project $PREFIX-prod` | push to the connected branch, or `firebase apphosting:rollouts:create` |
| Routing | `<Route>` entries in `src/App.tsx` | `app/<segment>/page.tsx` directories |
| Route manifest | `ROUTES` duplicated in `scripts/prerender.mjs` and `scripts/generate-sitemap.mjs` | `config/routes.mjs`, imported everywhere |
| Static HTML for crawlers | `scripts/prerender.mjs` (Puppeteer) | built-in static rendering — no prerender step exists |
| Hydration contract | `hydrateRoot` + `app-ready` event + `window.__PRERENDERING__` | framework-managed — none of these exist |
| Base `<head>` tags | `index.html` | `app/layout.tsx` (`export const metadata`) |
| Per-page metadata | `<MetaTags>` component in each page | `export const metadata` / `generateMetadata()` in each `page.tsx` |
| Structured data (JSON-LD) | `<script type="application/ld+json">` in `index.html` | `<script type="application/ld+json" dangerouslySetInnerHTML>` in the layout or page |
| Env vars | `VITE_*`, read via `import.meta.env` | `NEXT_PUBLIC_*` (client) / plain names (server), read via `process.env` |
| Env var delivery in prod | `.env.production`, baked at build | `apphosting.yaml` `env:` entries with `availability: [BUILD, RUNTIME]` |
| Secrets | Firebase Functions + Secret Manager | `apphosting.yaml` `secret:` refs → Secret Manager |
| Build-time HTML rewriting | `htmlPlugin` in `vite.config.ts` | not needed — metadata and env are resolved by the framework |
| Response headers / caching | `firebase.json` `headers` array | `async headers()` in `next.config.ts` |
| `firebase.json` role | Hosting config: public dir, rewrites, headers | only the `apphosting` block (`backendId`, `rootDir`) for CLI deploys |
| Monorepo support | any layout; the build is just `vite build` | workspaces require Turborepo or Nx — see below |
| CSP | static SHA-256 hash list | per-request nonce from `middleware.ts` |
| Sitemap | `scripts/generate-sitemap.mjs` → `public/sitemap.xml` | `app/sitemap.ts` reading `config/routes.mjs` |
| robots.txt | `public/robots.txt` | `app/robots.ts` |
| Favicon | `public/favicon.*` + `<link>` tags | `app/icon.png`, `app/apple-icon.png`, `app/favicon.ico` (file conventions, auto-linked) |
| Images | `<picture>` + `scripts/convert-images.mjs` | `next/image` (WebP/AVIF and responsive sizes are automatic) |
| Server-side code | Firebase Functions in `functions/` | route handlers at `app/api/<name>/route.ts` |
| Client interactivity | every component is a client component | components are server components until marked `'use client'` |
| Scroll reset on navigation | `ScrollToTop` component (required, easy to miss) | built into the router |
| Page-add checklist | the three-file rule | the one-file rule |

### Monorepos on the `nextjs` track

The Vite track does not care how the repo is laid out — the build is a local `vite build` and Firebase Hosting just uploads the resulting directory. App Hosting does care, because it builds the repo remotely and has to resolve the app's dependencies itself.

**A repo with npm/pnpm/yarn `workspaces` needs a supported monorepo tool on top of them — Turborepo or Nx.** Workspaces alone fail to build. Turborepo is the default choice for a Next.js site ([support shipped January 2026](https://firebase.blog/posts/2026/01/apphosting-turborepo/)). That means a root `turbo.json`, `turbo` as a root devDependency, a single lockfile at the repo root, and the backend's root directory pointed at the app (`apps/site`) rather than `/`. `/senternet-site-nextjs-setup` step 6b has the full layout.

Single-package repos need none of this, and Turborepo should not be added to one.

### The three-file rule (`vite`)

Every new page updates all three together:

1. `src/App.tsx` — add the `<Route>`
2. `scripts/prerender.mjs` — add to `ROUTES`
3. `scripts/generate-sitemap.mjs` — add to `ROUTES` (indexable pages only)

### The one-file rule (`nextjs`)

Every new page is a directory with a `page.tsx`, plus one entry in `config/routes.mjs`:

1. `app/<segment>/page.tsx` — the page, with its `export const metadata`
2. `config/routes.mjs` — add the route (with `indexable: false` for legal pages)

`app/sitemap.ts`, `app/robots.ts`, and `scripts/indexnow.mjs` all read `config/routes.mjs`, so a single entry keeps sitemap and IndexNow in sync. Nothing else needs updating — there is no prerender list.

## Rules that hold on every track

These are outcomes, not implementation details. A track is only correct if all of them hold:

- Every indexable route returns fully rendered HTML to a crawler that executes no JavaScript.
- Every route has a unique `<title>`, a description, canonical URL, and OG/Twitter image.
- `og:url` and `<link rel="canonical">` match exactly.
- `noindex` routes are prerendered/rendered but never listed in the sitemap.
- The sitemap, robots.txt, and IndexNow submissions all agree on the canonical host.
- Security headers (`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`) and a CSP without `'unsafe-inline'` in `script-src` are served on every response.
- Hashed static assets get a 1-year immutable cache; HTML does not.
- Mobile Lighthouse: Performance ≥ 94, Accessibility ≥ 98, Best Practices ≥ 96, SEO = 100.

## Other frameworks (Astro, SvelteKit, Remix, Nuxt, plain HTML)

No third track is implemented. If the user asks for one:

1. Say plainly that only the `vite` and `nextjs` tracks are implemented, and that the rest of the suite's steps would need translating by hand as you go.
2. Offer the closest supported track first — Astro and SvelteKit static builds map onto the `vite` track (static output on Firebase Hosting); SvelteKit/Remix/Nuxt with SSR maps onto the `nextjs` track (App Hosting on Cloud Run).
3. If the user still wants the unsupported framework, proceed — but treat the rules above as the contract, translate each skill's steps yourself using the convention map as the pattern, write `.site-framework.json` with the real framework name and the closest `renderMode`, and tell the user which steps you translated rather than executed verbatim.

Never silently run Vite-specific steps against a non-Vite repo. A `vite.config.ts` written into a Next.js project, or a Puppeteer prerender pass over a framework that already emits HTML, is worse than skipping the step.
