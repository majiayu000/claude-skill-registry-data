---
name: senternet-create-site
description: Orchestrate the full Senternet site build by running foundation, favicon, SEO, analytics, CSP, prerender, image, and performance skills in order.
---

# Create a Complete Optimized Marketing Site

Spin up or upfit a fully optimized marketing site by executing all site skills in sequence.

---

## Mode Detection

Before asking anything, check whether the user provided a path to an existing directory:

- **Existing directory** — run in **upfit mode**: navigate to that directory and detect what's already implemented before each step. Skip steps that are complete, patch steps that are partial.
- **No directory provided** — run in **create mode**: ask the intake questions below and build from scratch. If the user does not have a design zip, directory, or HTML export, default to a barebones Hello World site using the requested project and directory names.

## Framework Track

Every site runs on one framework track, held in `$FRAMEWORK` for the whole run: `vite` (Vite + React on Firebase Hosting) or `nextjs` (Next.js App Router on Firebase App Hosting). Read `/senternet-site-framework` for the decision guidance and the full convention map — it is the source of truth this orchestrator branches on.

- **Upfit mode** — detect the track before asking anything, using the detection rules in `/senternet-site-framework` (`.site-framework.json` first, then `next.config.*` / `app/layout.tsx`, then `vite.config.*`). Never ask the user which framework an existing repo uses when the repo already answers it. If nothing is detectable, or both frameworks are present with no marker file, ask.
- **Create mode** — ask intake question 0 below.

Once `$FRAMEWORK` is known, it applies to every step. Where a step below lists a Next.js variant, take that path when `$FRAMEWORK` is `nextjs`; otherwise take the Vite path. Where a step lists no variant, it is identical on both tracks.

If the user asks for a framework other than these two, follow the "Other frameworks" section of `/senternet-site-framework`: offer the closest supported track, and if they still want the other framework, translate each step through the convention map and tell them which steps were translated rather than executed verbatim.

## Upfit Feature Inventory

In upfit mode, surface a visible feature inventory before the optional phases so the user can see what is already enabled and what is still available to add.

- For each optional capability, detect whether the repo already has it.
- Report each one as either `enabled` or `available`.
- If one or more optional capabilities are `available`, present them to the user as a single enablement menu instead of separate yes/no prompts.
- Only offer options for capabilities that are not already enabled.

Optional capabilities to inventory in upfit mode:

- Transactional email via Resend
- Reddit pixel for ad campaigns
- Spanish `/es/` multilingual support
- Ad landing pages for paid campaigns
- SEO blog
- Competitor comparison / alternative pages
- reCAPTCHA Enterprise protection for forms

---

## Intake Questions

**If creating new**, ask:
0. **Framework** — `Vite + React` (default) or `Next.js (App Router)`. Present it as a real choice with the tradeoff in one line each:
   - **Vite + React on Firebase Hosting** *(recommended for marketing sites)* — static files on a CDN, no cold starts, cheapest to run, and every skill in this suite targets it first.
   - **Next.js on Firebase App Hosting** — server rendering, route handlers instead of Cloud Functions, middleware and nonce-based CSP, on-demand regeneration. Costs cold starts and a heavier build.
   
   If the user has no opinion, take Vite. If they name a different framework, follow the "Other frameworks" guidance in `/senternet-site-framework`. Record the answer as `$FRAMEWORK`.
1. **Site name** (e.g. `myapp-site`) — used as the directory name
2. **App/product name** (e.g. `MyApp`) — used in copy, meta tags, schema.org
3. **Domain** (e.g. `myapp.com`) — used in canonical URLs, sitemap, IndexNow, and Firebase Hosting domain setup; default canonical host is `www.myapp.com` unless they explicitly want apex canonical
4. **Design export** — path to the zip file, directory, or HTML file exported from Claude Design (or another design tool). If they do not have one, skip this input and create a barebones Hello World site instead.
5. **App Store URL** (if iOS app, e.g. `https://apps.apple.com/app/...`) — used in CTA links
6. **Twitter/X handle** (e.g. `@MyAppHQ`) — used in Twitter Card meta tags
7. **Multilingual?** (yes/no) — whether to add Spanish (`/es/`) support
8. **Local dev port** — default `3000`. Ask which port to use, and explain they may want a different one if they run multiple sites locally (e.g. 3001, 3002, 3003). Pass the answer to the scaffold skill for the chosen track as `$PORT`.

**If upfitting an existing directory**, ask only what's missing or cannot be detected:
- Detect `$FRAMEWORK` first (see **Framework Track** above), then read the files that track actually uses.
- Read `package.json`, `.firebaserc`, `.firebase-domain.json`, and the env files to infer app name, domain, canonical host, and analytics IDs before asking.
- On the Vite track also read `firebase.json`, `index.html`, and `.env.production`. On the Next.js track read `apphosting.yaml`, `next.config.*`, `app/layout.tsx`, and `config/routes.mjs` instead.
- Only ask for values that can't be found in the project files.

---

## Detection Rules (apply before every step)

Before executing each step, run the detection check listed for that step:

- **Already implemented** → skip the step; print a one-line note (e.g. `✓ firebase.json exists — skipping Firebase setup`).
- **Partially implemented** → patch only what's missing; note what was added.
- **Not present** → execute the full step.

---

## Prerequisite: GitHub Setup *(optional)*

**Detection:**
- `.git/` directory exists → skip `git init`; check remote with `git remote -v`
- `.gitignore` exists → update it to include recommended entries (env files, credentials, build output, editor dirs, OS files) without removing existing entries
- GitHub remote is already set → skip remote creation

Execute `/senternet-site-github-setup` for any missing pieces.

Ask: "Do you want to set up a git repo and GitHub remote now?" only if `.git/` does not exist. If it does, skip the question entirely.
In upfit mode, include GitHub setup in the same feature inventory so the user can see whether the repo and remote are already enabled or still available to add.

---

## Prerequisite: Google Cloud & Firebase Authentication

**Detection:**
- Run `gcloud auth list` — if an active account is shown, skip gcloud auth
- If `gcloud auth list` fails or shows no credentialed account in this shell, do not stop there: run `gcloud auth login` with the standard scopes, then re-run `gcloud auth list` in the same shell before falling back to full auth
- If the machine is headless or browser launch fails, add `--no-browser` so gcloud prints device-flow instructions, then wait for the user to complete the browser/device step and re-run `gcloud auth list`
- Run `firebase projects:list` — if it succeeds, skip firebase login
- If `firebase projects:list` fails because the Firebase session expired or no active Firebase account is available, run `firebase login --reauth` first, then re-run `firebase projects:list` before falling back to full auth
- Auth checks are account-scoped; all project-specific `gcloud` and `firebase` commands later in the workflow must include `--project "$PROJECT_ID"` (or the current `$PREFIX-dev` / `$PREFIX-prod` project).

Execute `/senternet-site-gcloud-auth` for any missing auth.

---

## Phase 1: Project Foundation

Phase 1 is mandatory for every new site. Do not consider the site created until all three foundation pieces are in place:
- The framework scaffold for `$FRAMEWORK`
- Design system/components
- Firebase config and deploy wiring for the track's host

### Step 1: Framework Scaffold

Run the scaffold skill for the chosen track:

| `$FRAMEWORK` | Skill | Host wired in Step 3 |
|---|---|---|
| `vite` | `/senternet-site-vite-setup` | Firebase Hosting |
| `nextjs` | `/senternet-site-nextjs-setup` | Firebase App Hosting |

Whichever runs must leave `.site-framework.json` in the site root before Phase 1 ends. Every later step reads it, so a missing marker file means every subsequent detection has to re-derive the track.

#### Vite track detection

- `package.json` with `vite` and `react` in dependencies → skip scaffolding
- `vite.config.ts` exists → check for `htmlPlugin`, `outDir: 'build'`, `manualChunks`; patch only missing pieces
- `src/main.tsx` exists with `hydrateRoot` → skip; without it → patch
- `src/App.tsx` renders a `ScrollToTop` component (a `useLocation` + `useEffect(() => window.scrollTo(0, 0), [pathname])` helper) inside `<BrowserRouter>` → skip; without it → patch it in. This is a consistent bug on existing sites: React Router preserves scroll position across navigation, so clicking a link while scrolled down lands the user partway down the next page. Always verify it is present and wired inside the router.
- `.env.development` and `.env.production` exist → skip env file creation

Execute `/senternet-site-vite-setup` for any missing pieces.

#### Next.js track detection

- `package.json` with `next` in dependencies and `app/layout.tsx` present → skip scaffolding
- `next.config.ts` exists → check for `headers()`, `poweredByHeader: false`, and the absence of `output: 'export'`; patch only missing pieces
- `apphosting.yaml` exists at the repo root → check that `NEXT_PUBLIC_BASE_URL` is listed with `BUILD` availability; patch if not
- `config/routes.mjs` exists → skip the route manifest; verify it covers every directory under `app/` that has a `page.tsx`
- `app/sitemap.ts` and `app/robots.ts` exist → skip (Steps 6 and 7 below are already satisfied on this track)
- `.env.development` and `.env.production` exist → skip env file creation
- `hydrateRoot`, an `app-ready` dispatch, a `ScrollToTop` component, or `react-router-dom` found in a Next.js repo → these are Vite-track artifacts that do not belong here; flag them rather than adding more

Execute `/senternet-site-nextjs-setup` for any missing pieces.

#### Both tracks

Pass the local dev port from the intake questions to the scaffold skill as `$PORT` (default `3000`). On upfit runs, if `package.json`'s `dev` script and the env files already pin a port, reuse that value instead of re-prompting.

### Step 2: Site Design

**Detection:**
- `src/styles/design-system.css` (Vite) or `app/globals.css` carrying the design tokens (Next.js) exists → skip design extraction
- `src/pages/` + `src/components/` (Vite) or `app/` + `components/` (Next.js) contain React components → skip component conversion
- Ask about design export only if components are absent and the user actually has a design export

On the Next.js track, converted components land in `app/<segment>/page.tsx` and `components/`, and only the leaves that need state or event handlers get `'use client'`. Do not mark whole pages as client components.

**No design export fallback:**
- If the user does not have a design zip, directory, or HTML export, do not invoke `/senternet-site-design`
- Create a minimal Hello World home page using the requested site name and app/product name
- Keep the site intentionally barebones; the goal is a working scaffold rather than an extracted visual design

Execute `/senternet-site-design` if components are missing or the user wants to re-import a new design.

### Step 3: Firebase Hosting

This step is required for every site, including brand-new creates. Never skip it just because the app already runs locally.

**Detection (both tracks):**
- `.firebaserc` exists → check for dev/prod project entries; add missing entries
- `.firebase-domain.json` exists with `status: connected` and the expected apex/canonical pair → skip the custom domain handoff
- `.firebase-domain.json` exists with `status: pending-dns` → keep moving on later phases and revisit the domain verification after other Firebase-safe steps finish
- `deploy:prod` script in `package.json` → skip script addition

**Vite track:**
- `firebase.json` exists → check for caching headers, security headers, `cleanUrls`; patch missing config keys

**Next.js track:**
- `apphosting.yaml` exists → check `runConfig` and the `env` entries; patch missing keys. In a monorepo it belongs in the app directory, not the repo root.
- `firebase apphosting:backends:list --project $PREFIX-prod` returns a backend for this repo → skip backend creation
- A GitHub remote must exist before the backend can be created, because App Hosting deploys from a connected branch. If there isn't one, run the GitHub prerequisite first instead of deferring it.
- **Root `package.json` has `workspaces` but the repo has no `turbo.json` or `nx.json` → the build will fail.** App Hosting needs a supported monorepo tool (Turborepo or Nx) on top of workspaces; workspaces alone are not enough. Add Turborepo per step 6b of `/senternet-site-nextjs-setup` before creating the backend, and set the backend's root directory to the app's path.
- `firebase.json` on this track carries the `apphosting` block (`backendId`, `rootDir`) for CLI deploys — but never hosting headers, which belong in `next.config.ts`

Execute `/senternet-site-firebase` for any missing pieces, including the custom-domain handoff when `.firebase-domain.json` is absent or still pending. Follow its **Next.js track / App Hosting** section when `$FRAMEWORK` is `nextjs`.

After this step, verify these files exist and are correct before moving on:
- `firebase.json` (Vite) or `apphosting.yaml` (Next.js)
- `.firebaserc`
- `.firebase-domain.json` if the canonical domain was connected
- `package.json` with `deploy:prod` wired to the track's deploy command

---

## Phase 2: SEO Foundation

### Step 4: Favicon Assets

**Detection:**
- `public/favicon.svg`, `public/favicon.png`, `public/favicon.ico`, and `public/apple-touch-icon.png` all exist → skip icon generation
- `index.html` or `src/components/MetaTags.tsx` already links the favicon files → skip head tag patch
- **Next.js:** `app/icon.png`, `app/apple-icon.png`, and `app/favicon.ico` exist → skip. These file conventions auto-emit the `<link>` tags, so no head patch is needed or wanted.

Execute `/senternet-site-favicon` for any missing pieces.

### Step 5: Meta Tags

**Detection:**
- `index.html` contains `og:title` → OG tags present; check for Twitter Card, PWA, canonical, favicon — add only what's missing
- `src/components/MetaTags.tsx` exists → skip component creation
- Schema.org `<script type="application/ld+json">` in `index.html` → skip structured data

**Next.js detection instead:**
- `app/layout.tsx` exports `metadata` with `metadataBase`, `openGraph`, and `twitter` → base tags present
- Every `page.tsx` exports its own `metadata` (or `generateMetadata`) with a unique title, description, and `alternates.canonical` → skip per-page work; patch any page missing one
- A JSON-LD `<script>` in the layout or home page → skip structured data
- Do **not** create `src/components/MetaTags.tsx` on this track — a client component that mutates `document.head` fights the Metadata API and loses on the first server render

Execute `/senternet-site-metatags` for any missing pieces.

### Step 6: robots.txt

**Detection:**
- `public/robots.txt` exists → skip; verify it points to the sitemap — update if not
- **Next.js:** `app/robots.ts` exists and returns the sitemap URL on the canonical host → skip. Do not also ship `public/robots.txt`; two sources for the same path is a silent conflict.

Execute `/senternet-site-robots` if missing or malformed.

### Step 7: Sitemap

**Detection:**
- `scripts/generate-sitemap.mjs` exists → skip script creation; verify routes include `/`, `/privacy`, `/terms`
- `public/sitemap.xml` exists → regenerate only if routes have changed
- `build:prod` script calls `generate-sitemap` → skip wiring

**Next.js detection instead:**
- `app/sitemap.ts` exists and reads `config/routes.mjs` → skip
- `config/routes.mjs` covers every `page.tsx` under `app/`, with legal pages marked `indexable: false` → skip
- There is no generate step to wire into `build:prod` on this track, and no `public/sitemap.xml` to commit

Execute `/senternet-site-sitemap` for any missing pieces.

### Step 8: IndexNow

**Detection:**
- Any `public/*.txt` file matching a 32-char hex key → IndexNow key already exists; skip key generation
- `scripts/indexnow.mjs` exists → skip script creation
- `deploy:prod` script calls `indexnow` → skip wiring
- **Next.js:** the script reads the URL list from `config/routes.mjs` rather than parsing `public/sitemap.xml`, and runs after the rollout completes rather than after `firebase deploy`

Execute `/senternet-site-indexnow` for any missing pieces.

---

## Phase 3: Analytics, Email & Tracking

### Step 9: Analytics Setup (Google Analytics or PostHog)

**Provider selection:**
- If the user has already picked a provider, go straight to it: `/senternet-site-google-analytics` (GA4) or `/senternet-site-posthog`.
- If the provider is undecided, run `/senternet-site-analytics` to choose, then continue with the selected skill.
- Detecting an existing provider: a non-empty `VITE_GA_ID` (or `<!-- GA_START -->` marker) means GA4 is already wired; a non-empty `VITE_POSTHOG_KEY` or `src/lib/analytics.ts` with a PostHog init means PostHog is already wired. Skip selection when one is already present.

The detection and execution rules below apply to the **GA4** path. For the PostHog path, follow `/senternet-site-posthog` and skip the Firebase web-app / Measurement ID steps.

**Env var naming:** analytics IDs are `VITE_*` on the Vite track and `NEXT_PUBLIC_*` on the Next.js track. On the Next.js track, every one of them must also appear in `apphosting.yaml` with `BUILD` availability, or it will be `undefined` in the deployed client bundle even though `.env.production` has it.

**GA4 detection:**
- `index.html` contains `<!-- GA_START -->` comment marker → GA block already present
- `.env.production` contains a non-empty `VITE_GA_ID=G-...` value → skip env var setup
- `vite.config.ts` has `htmlPlugin` handling GA injection → skip plugin verification
- **Next.js:** a `<Script src="https://www.googletagmanager.com/gtag/js...">` (from `next/script`) in `app/layout.tsx` and a non-empty `NEXT_PUBLIC_GA_ID` in both `.env.production` and `apphosting.yaml` → skip. There is no `htmlPlugin` and no GA comment marker on this track, and no prerender strip step is needed.
- The Firebase project already has a web app configured, the Hosting site association is complete, and `.env.production` already has a non-empty GA ID → skip Firebase web-app setup
- The Firebase project still needs a web app or Hosting association → run `/senternet-site-firebase` and follow its automated Firebase CLI flow

Execution rule (GA4 path):
- Resolve the production Firebase project ID first if you need it for the manual instructions, but do not use it to call `analyticsDetails` or `addGoogleAnalytics`.
- If the Firebase project still needs the web app or Hosting association, run `/senternet-site-firebase` first.
- Once the web app is created and the config is captured, either accept an existing Measurement ID or continue with the existing Measurement ID retrieval / env wiring step.
- Do not stop at the front-end GA markers alone. The step is not complete until the Firebase project has a web app, the Hosting association is in place, and `.env.production` has the Measurement ID.

### Step 9b: GDPR cookie consent for GA *(recommended when GA4 is enabled)*

**Detection:**
- A cookie consent module / banner exists (e.g. `cookie-consent`, `CookieConsentBanner`, `lib/cookie-consent.ts`) that gates gtag until accept → skip
- Geo endpoint exists (`/api/geo` or equivalent) returning `consentRequired` → skip wiring; verify EU/GB set and GA inject path
- GA still loads from a static `index.html` block or unconditional `next/script` with no consent check → run the skill to gate it

When GA4 is present (or just wired in Step 9), execute `/senternet-site-gdpr` unless the user explicitly declines (e.g. Ahrefs-only / cookieless analytics, or EEA traffic is out of scope). Skip when the only analytics is cookieless.

### Step 9c: CCPA opt-out for California *(recommended when GA4 is enabled)*

**Detection:**
- Consent module already understands a `ccpa` regime (or California region) and disables gtag on reject → skip
- Geo endpoint returns state/region and a `regime` of `gdpr` | `ccpa` | `none` → verify CCPA path; patch if only GDPR exists
- GA loads with no way for a California visitor to stop it → run the skill

When GA4 is present, execute `/senternet-site-ccpa` unless the user explicitly declines (no CA traffic, or cookieless analytics only). Prefer one shared consent module with `/senternet-site-gdpr` rather than two banners. CCPA is opt-out (GA may run until Reject); do not reuse GDPR's "block until Allow all" rule for California.

### Step 10: Transactional Email via Resend *(optional — for forms, notifications, or onboarding)*

**Detection:**
- `functions/src/index.ts` contains `RESEND_API_KEY` or `sendResendEmail` → skip
- `firebase.json` has a `functions` block and root `package.json` deploy script already includes `hosting,functions` → skip wiring
- **Next.js:** the send path is a route handler at `app/api/<name>/route.ts`, not a Cloud Function, and `RESEND_API_KEY` is a `secret:` ref in `apphosting.yaml` with `RUNTIME` availability. Detect the route handler and the secret ref instead. Do not add a `functions/` directory to a Next.js site just to send an email.

In upfit mode, include transactional email in the optional-feature menu if it is not already detected. If the user selects it, execute `/senternet-site-email-resend`.

### Step 10b: Stripe Payments *(optional — for selling a license, subscription, or product)*

**Detection:**
- `functions/src/*` references `STRIPE_SECRET_KEY` or `stripe.checkout` → skip
- `firebase.json` rewrites include a Stripe function (e.g. `createCheckoutSession`) → skip wiring
- **Next.js:** checkout and webhook live at `app/api/checkout/route.ts` and `app/api/stripe-webhook/route.ts`; `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET` are `secret:` refs in `apphosting.yaml`. The webhook handler must read the raw request body (`await req.text()`) before verifying the signature — parsing it as JSON first breaks verification.

In upfit mode, include "Payments via Stripe" in the optional-feature menu if it is not already detected. If the user selects it, execute `/senternet-site-stripe`. Receipt-email and signed-download-URL fulfillment depend on `/senternet-site-email-resend`, so run that first (or alongside) when the user chooses those.

### Step 11: Reddit Pixel *(optional — only if running Reddit ads)*

**Detection:**
- `src/components/RedditPixel.tsx` exists → skip
- `index.html` contains Reddit pixel bootstrap stub → skip
- `VITE_REDDIT_PIXEL_ID` in `.env.production` → skip

In upfit mode, include Reddit pixel in the optional-feature menu if it is not already detected. If the user selects it, execute `/senternet-site-ads-reddit-pixel`.

---

## Phase 4: Build Pipeline

### Step 12: Prerendering

**Vite track only.** Skip this step entirely when `$FRAMEWORK` is `nextjs` — Next.js emits static HTML for every route it can, so a Puppeteer pass over the built output adds build time and a second, divergent copy of every page. Never install Puppeteer or create `scripts/prerender.mjs` on the Next.js track.

**Detection:**
- `scripts/prerender.mjs` exists → skip script creation; verify ROUTES list covers current routes
- `build:prod` and `build:dev` scripts call `prerender` → skip wiring

Execute `/senternet-site-prerender` for any missing pieces.

**Next.js equivalent check** — do this instead, and treat a failure here the way you would treat a `✗ EMPTY` prerender result:

- `npm run build` and read the route table it prints. Every marketing route should be marked static (`○`) or ISR, not dynamic (`ƒ`). A page that went dynamic by accident (usually a `cookies()`/`headers()`/`searchParams` read, or `'use client'` too high in the tree) is rendering per request and paying a cold start for content that never changes.
- `npm start`, then `curl -s localhost:$PORT/<route>` for each route and confirm the response body contains the page's real headline and meta tags. This is exactly the crawler's view.

---

## Phase 5: Images

### Step 13: WebP Conversion

**Detection:**
- `scripts/convert-images.mjs` exists → skip
- `convert-images` npm script in `package.json` → skip
- `public/images/` directory exists → skip directory creation
- **Next.js:** `next/image` already emits WebP/AVIF and responsive `srcset` at request time, so the conversion script and the hand-written `<picture>` pattern are redundant. Instead verify every content image uses `next/image` with explicit `width`/`height` (or `fill` plus `sizes`), and that the LCP image sets `priority`. Only keep a conversion script for images referenced outside the framework (share images, favicons, CSS backgrounds).

Execute `/senternet-site-image-webp` for any missing pieces.

### Step 14: Share Images

**Detection:**
- `scripts/generate-share-images.mjs` exists → skip
- `public/share/home.png` exists → skip generation
- `index.html` `og:image` points to `/share/home.png` → skip update
- **Next.js:** the generated PNGs still land in `public/share/`; the reference moves to `openGraph.images` in each page's `metadata` (resolved against `metadataBase`) instead of `index.html`

Execute `/senternet-site-share-images` for any missing pieces.

---

## Phase 6: Performance

This phase is mandatory for every site. Do not mark the site complete until Lighthouse optimization has been executed against a locally served production build, the reported regressions have been addressed, and the site is retested.

### Step 15: Lighthouse Optimization

**Detection:**
- `vite.config.ts` has `modulepreload` injection and `manualChunks` → still run `/senternet-site-lighthouse` against the local production build to verify actual performance, image, caching, and LCP discovery behavior
- `index.html` has `<link rel="modulepreload">` → still run `/senternet-site-lighthouse` locally
- CSS has `@media (prefers-reduced-motion)` or mobile animation disabling → still run `/senternet-site-lighthouse` locally

Execute `/senternet-site-lighthouse` unconditionally in this phase against a locally served `build/` output, then fix any reported Lighthouse issues before proceeding.

**Next.js:** run it against `npm run build && npm start` instead of a served `build/` directory. Chunking, modulepreload, and font optimization are the framework's job here, so the fixes that matter are different: shrink the client-component boundary, add `priority` to the LCP image, use `next/font` rather than a `<link>` to a font CDN, and check the build's route table for pages that went dynamic. The score targets are the same.

### Step 16: Mobile Optimization

**Detection:**
- `public/images/` contains a `-sm.webp` hero variant → skip mobile hero creation
- `index.html` has `<link rel="preload" media="...">` responsive preload → skip
- Images have `loading="lazy"` where appropriate → skip

Execute `/senternet-site-mobile-optimize` for any missing pieces.

### Step 17: Mobile Navigation

**Detection:**
- `src/components/Layout.tsx` has `hidden md:flex` on the desktop nav and an `md:hidden` hamburger button → skip
- Layout imports `useState` and toggles a `mobile-menu` panel → skip
- Header nav is desktop-only with no responsive collapse → run

Execute `/senternet-site-mobile-nav` for any missing pieces.

---

## Phase 7: Optional Features

### Step 18: Multilingual (if requested)

**Detection:**
- `src/i18n.ts` exists → already multilingual; skip
- `src/App.tsx` contains `LanguageProvider` → skip
- Prerender script contains `/es/` routes → skip
- **Next.js:** an `app/[locale]/` segment (with `generateStaticParams` returning the locale list) plus middleware-based locale routing → skip. `hreflang` comes from `alternates.languages` in each page's `metadata` rather than from injected `<link>` tags.

If not present, include Spanish (`/es/`) support in the optional-feature menu in upfit mode. Execute `/senternet-site-multilingual` if the user selects it.

### Step 19: Ad Landing Pages

**Detection:**
- `src/components/LandingPage.tsx` exists → skip base component
- A campaign-specific landing page route exists in `App.tsx` → skip
- **Next.js:** `components/LandingPage.tsx` plus an `app/lp/<campaign>/page.tsx` per campaign. Campaign pages are usually `noindex` — set `robots: { index: false }` in their `metadata` and mark them `indexable: false` in `config/routes.mjs`.

In upfit mode, include ad landing pages in the optional-feature menu if they are not already detected. Execute `/senternet-site-ads-landing` if the user selects them.

### Step 20: SEO Blog

**Detection:**
- A blog route and blog index component exist in `src/` → skip
- `src/data/` contains post data → skip
- **Next.js:** `app/blog/page.tsx`, `app/blog/[slug]/page.tsx` with `generateStaticParams` and `generateMetadata`, and post data under `content/` or `data/` → skip. Post URLs come from the same `generateStaticParams` list that feeds `config/routes.mjs`, so the sitemap picks them up without a separate array.

In upfit mode, include the SEO blog in the optional-feature menu if it is not already detected. Execute `/senternet-site-seo-blog` if the user selects it.

### Step 21: Compare Pages

**Detection:**
- `src/components/ComparePages.tsx` exists → skip
- Competitor/alternative routes exist in `App.tsx` → skip
- **Next.js:** `app/vs/[competitor]/page.tsx` and `app/alternatives/[competitor]/page.tsx` with `generateStaticParams` → skip

In upfit mode, include competitor comparison / alternative pages in the optional-feature menu if they are not already detected. Execute `/senternet-site-compare-pages` if the user selects them.

### Step 22: reCAPTCHA Enterprise for Forms

**Detection:**
- `gcloud recaptcha keys list --project "$PROJECT_ID"` shows existing local/dev/prod form keys → skip
- `recaptchaenterprise.googleapis.com` is already enabled → skip API enablement

In upfit mode, include reCAPTCHA Enterprise in the optional-feature menu if it is not already detected. Execute `/senternet-recaptcha-enterprise` if the user selects it.

---

## Step 23: Content Security Policy

Run this after every third-party integration is wired (analytics, GDPR/CCPA consent, Resend, Stripe, Reddit pixel, reCAPTCHA) and before the verification build, so the policy is generated against the services the site actually loads. This step is not optional: every Senternet site ships a CSP.

**Detection:**
- `firebase.json` already sets a `Content-Security-Policy` header → audit it against the services wired in this run, extend it for anything missing, and skip the rest
- **Next.js:** `middleware.ts` already generates a per-request nonce and sets the CSP header → audit and extend only

Execute `/senternet-site-csp`. It audits which third-party origins are in use, moves inline scripts out of `index.html` (Vite) or wires the nonce through `<Script>` tags (Next.js), writes the header, and verifies it live.

Every service added after this point must have its origins added to the policy in the same change that adds the service. A new script that is not in the CSP silently fails in production.

---

## Step 24: Verify everything works

**Vite track:**

1. `npm run dev` — dev server starts cleanly
2. `npm run build:prod` — builds, prerenders all routes (check for `✗ EMPTY` failures)
3. *(Optional — only if dev environment exists)* `npm run deploy:dev` — deploys to staging Firebase project
4. *(Optional)* Verify staging URL loads and meta tags are correct
5. Fix any Lighthouse failures found on the local production build before first production deploy
6. Load the local production build and confirm the console is free of CSP violations
7. `npm run deploy:prod` — deploys to production + runs IndexNow
8. *(Optional, upfit only)* If an existing deployed site and production URL are already detectable, run PageSpeed Insights against production after deploy to capture live CDN behavior

**Next.js track:**

1. `npm run dev` — dev server starts cleanly
2. `npm run typecheck` — clean
3. `npm run build` — no errors, and the route table shows the marketing routes as static (`○`), not dynamic (`ƒ`)
4. `npm start`, then `curl` each route and confirm real HTML and correct per-page meta come back
5. Confirm `/sitemap.xml` lists only indexable routes and `/robots.txt` points at the canonical host
6. Fix any Lighthouse failures against the local production server before the first production rollout
7. Deploy by pushing to the connected branch, or `npm run deploy:prod` to force a rollout; watch it reach `READY` before running IndexNow
8. Confirm the `Content-Security-Policy` header comes back on a deployed response and the console is free of CSP violations
9. Verify the deployed backend serves the same HTML the local production server did — a variable missing from `apphosting.yaml` shows up here as an empty analytics ID or a wrong canonical host, and nowhere earlier

---

## Step 25: Initialize Project Documentation

**Detection:**
- `AGENTS.md` exists → skip generation (do not overwrite existing project docs)
- `CLAUDE.md` exists → skip
- `README.md` exists → skip

If any are missing, execute `/senternet-site-init` for only the missing files. The generated docs must describe the track this site actually runs on — tech stack, build pipeline, deploy command, and the page-add rule all differ between tracks, and docs describing the wrong one are worse than no docs.

---

## Page-add rule (enforce for every new page)

**Vite track — the three-file rule.** Every new page/route must update these files together; missing any one breaks crawlers or indexing:

1. `src/App.tsx` — add the `<Route>`
2. `scripts/prerender.mjs` — add to ROUTES array
3. `public/sitemap.xml` (or regenerate via `generate-sitemap.mjs`) — indexable routes only
4. `scripts/generate-share-images.mjs` — add a share image block and run it

**Next.js track — the one-file rule.** Routing, prerendering, and the sitemap all derive from two places:

1. `app/<segment>/page.tsx` — the page, with its own `export const metadata` (unique title, description, `alternates.canonical`, `openGraph.images`)
2. `config/routes.mjs` — add the route, `indexable: false` for legal pages
3. `scripts/generate-share-images.mjs` — add a share image block and run it

`app/sitemap.ts`, `app/robots.ts`, and `scripts/indexnow.mjs` all read `config/routes.mjs`, so there is no third list to keep in sync and no prerender array to update.

## Footer link organization (enforce as links accumulate)

The footer collects links from many skills (AI Disclosure, Other Projects, blog, compare pages, legal pages). Once it holds more than ~4–5 links, divide it into labeled category columns (e.g. **Legal** — Terms, Privacy, AI Disclosure; **Product** — Features, Pricing, Download; **Company** — About, Blog, Other Projects) rather than letting a single flat row grow unbounded. Each new footer link goes into the category it belongs to. See `/senternet-site-design` for the `SiteFooter.tsx` grouping convention. On upfit runs, if the footer already has many links in a flat list, migrate them into grouped columns.
