---
name: seo-optimization
description: Audit and improve SEO for the Angular customer-web app in the monorepo — Title/Meta service usage, structured data, sitemaps, Open Graph, Core Web Vitals, and local-business schema. Use this whenever the user mentions SEO, search rankings, Google indexing, meta tags, meta description, structured data, schema markup, sitemap.xml, robots.txt, Open Graph, canonical URLs, Lighthouse SEO score, or wants customer-web to rank better or be more discoverable. Trigger even if the user just says "SEO for customer-web" or "improve search rankings" without listing specifics.
---

# SEO Optimization — Angular (customer-web)

Scope: `apps/frontend/customer-web` (Angular standalone components, Tailwind v4). Does not apply to `admin-web` (not indexed, behind auth) unless explicitly asked.

## Read this first: customer-web is CSR-only today

As of this writing, `customer-web` has **no `@angular/ssr`, no `platform-server`, no `server.ts`** — it's a client-side-rendered SPA shipping one static `index.html` for every route. This caps what's achievable here in a way Next.js's App Router (the sibling template's target) doesn't have to contend with:

- **Open Graph/Twitter card tags cannot vary per route.** Facebook, X/Twitter, LinkedIn, and Slack's link-preview crawlers do not execute JavaScript — they read the static `index.html` response as-is. A CSR app can only ship one fixed set of OG tags for the whole site; a shared link to any inner page previews with the homepage's title/image, not that page's own.
- **JSON-LD and per-route `<title>`/`<meta description>` injected at runtime are invisible to non-JS-executing crawlers** and are a gamble even for JS-executing ones (Google generally renders JS, but on its own schedule via a second rendering pass — indexing can lag, and rich-result eligibility for JSON-LD is inconsistent for client-injected data).
- **The sitemap can't be generated per-request** — it has to be a build-time or CI-time static file.

**The single highest-leverage recommendation for real SEO here is enabling Angular SSR** (`ng add @angular/ssr`) or at minimum build-time prerendering of the known static routes (Angular's prerender/SSG option, which `ng add @angular/ssr` also sets up). Say this plainly in any audit before diving into the CSR-workaround checklist below — don't let the workarounds read as "SEO solved" when they're a materially weaker substitute for SSR. If the user explicitly wants to stay CSR-only, the sections below are what's actually achievable; if they're open to SSR, lead with that and this skill's checklist still applies on top of it (SSR fixes the crawler-visibility problem, it doesn't replace metadata/sitemap/structured-data work).

## Workflow

1. **Locate the app and confirm SSR status.** Check for `apps/frontend/customer-web/server.ts` and an `@angular/ssr` dependency in `package.json` before doing anything else — the audit's severity framing depends on this.
2. **Run the audit checklist below** against the current codebase — read files, don't assume. Use `grep`/`rg` to find gaps (missing `alt`, missing per-route title, raw `<img>` instead of `NgOptimizedImage`).
3. **Report findings as a checklist** (✅ / ⚠️ / ❌) before making changes, unless the user asked you to just fix everything directly.
4. **Fix in priority order**: SSR/prerender feasibility (flag, don't silently skip) → per-route Title/Meta → sitemap/robots → structured data → Open Graph → images → Core Web Vitals → semantic HTML. Content structure/topical authority (section 8) is editorial — surface as recommendations, don't auto-generate marketing copy.
5. Keep changes TypeScript-strict, no `any`, minimal comments, standalone components + Signals — consistent with `rules/frontend.md`.

---

## 1. Per-route Title & Meta tags (highest priority within CSR)

Angular's `Title` and `Meta` services (`@angular/platform-browser`) are the equivalent of the Metadata API — but since there's no server render, they must run early and synchronously enough that a JS-executing crawler's first paint already reflects them.

**Preferred: a custom `TitleStrategy`** (one central place, not scattered `ngOnInit` calls per component) so every route's `data` drives its title/description declaratively:

```typescript
// src/app/core/seo/route-seo.strategy.ts
import { Injectable, inject } from '@angular/core';
import { Title, Meta } from '@angular/platform-browser';
import { TitleStrategy, RouterStateSnapshot } from '@angular/router';

@Injectable({ providedIn: 'root' })
export class RouteSeoStrategy extends TitleStrategy {
  private readonly title = inject(Title);
  private readonly meta = inject(Meta);

  override updateTitle(snapshot: RouterStateSnapshot): void {
    const routeTitle = this.buildTitle(snapshot) ?? 'Business Name';
    this.title.setTitle(`${routeTitle} | Business Name`);

    const description = this.deepestChild(snapshot)?.data['description'] as string | undefined;
    if (description) {
      this.meta.updateTag({ name: 'description', content: description });
    }

    const canonical = `${window.location.origin}${snapshot.url}`;
    this.meta.updateTag({ rel: 'canonical', href: canonical } as never);
  }

  private deepestChild(snapshot: RouterStateSnapshot) {
    let route = snapshot.root;
    while (route.firstChild) route = route.firstChild;
    return route;
  }
}
```

Register it in `app.config.ts`: `{ provide: TitleStrategy, useClass: RouteSeoStrategy }`. Each route then carries `data: { title: 'Services', description: '...' }`.

Checklist:
- ⚠️ Every route has a unique `title`/`description` in its route `data` — no duplicates across routes.
- ⚠️ `<meta name="description">` exists as a real DOM node with correct content when the app is fully rendered — check with a headless browser or "View Rendered Source" in devtools, not View Source (which shows the pre-JS static shell and will never reflect this).
- ❌ Never leave the canonical `<link>` unset — for a CSR app all routes otherwise share the static `index.html`'s implicit canonical, which is wrong for every route but the homepage.

---

## 2. Sitemap & robots.txt (build-time static files)

No `sitemap.ts`/`robots.ts` file-convention API exists here — these are plain static assets served from Angular's public assets directory (`public/` in newer Angular CLI layouts, `src/assets` in older ones — check `angular.json`'s `assets`/`root` config for this project's actual layout).

**Static routes**: hand-maintain `public/robots.txt` and a static `public/sitemap.xml` for fixed pages (home, services, contact).

**Dynamic routes** (service/listing/blog detail pages pulled from `customer-api`): a static file can't reflect the DB, so generate `sitemap.xml` at build/CI time with a small script that calls the API and writes the file into the build output before/after `ng build` — mirroring the pattern this repo already uses for `docs:export`/`docs:site` (`dev-ops/scripts/*.ts` run via `tsx`, wired into a root `package.json` script). Do not hand-roll this inside a component; it has no runtime DOM to run in on a CSR app anyway.

`public/robots.txt`:
```
User-agent: *
Allow: /

Sitemap: https://example.co.za/sitemap.xml
```

Checklist:
- ❌ Never let a non-production build's `robots.txt` (if a separate one exists) leak into a production deploy — check the Angular build's `fileReplacements`/asset config per environment (see `CLAUDE.md`'s known gap: `environment.prod.ts` isn't currently wired via `fileReplacements` — the same gap likely affects any environment-specific static asset swap, so verify robots.txt truly differs per environment before trusting it does).
- ⚠️ Dynamic routes come from the DB via the generation script, not hardcoded — otherwise the sitemap goes stale.

---

## 3. Structured data (JSON-LD)

Almost every customer-facing app in this portfolio is a **local service business** — `LocalBusiness` schema is high-value and often skipped. On a CSR app this has to be injected into `document.head` at runtime via a service (there is no server render to embed it in the initial HTML):

```typescript
// src/app/core/seo/json-ld.service.ts
import { Injectable, inject, DOCUMENT } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class JsonLdService {
  private readonly document = inject(DOCUMENT);

  setLocalBusiness(): void {
    const data = {
      '@context': 'https://schema.org',
      '@type': 'LocalBusiness',
      name: 'Business Name',
      image: 'https://example.co.za/logo.png',
      telephone: '+27...',
      address: {
        '@type': 'PostalAddress',
        streetAddress: '...',
        addressLocality: '...',
        addressRegion: 'KZN',
        postalCode: '....',
        addressCountry: 'ZA',
      },
      areaServed: 'Durban, KZN',
      priceRange: '$$',
    };
    const script = this.document.createElement('script');
    script.type = 'application/ld+json';
    script.text = JSON.stringify(data);
    this.document.head.appendChild(script);
  }
}
```

Call this once (e.g. in `app.component.ts`'s constructor, or per-route for `Service`/`Article` schema on detail pages — remove the previous route's script on navigation so schemas don't stack).

Other schema types worth checking for by page type:
- Booking/quote flow → `Service` + `Offer`
- Reviews shown on-page → `AggregateRating` (only if reviews are real and displayed — never fabricate ratings, this violates Google's structured data guidelines)
- Blog/content pages → `Article` or `BlogPosting`

Checklist:
- ❌ Do not claim "JSON-LD is crawler-visible" the way the SSR version of this checklist would — client-injected JSON-LD is a best-effort measure on a CSR app, not a guarantee. Say so in the audit.
- ⚠️ Validate with Google's Rich Results Test (it renders JS, so client-injected JSON-LD will show up there even though that doesn't guarantee indexing behavior matches).

---

## 4. Open Graph & Twitter Cards — the sharpest CSR limitation

Because OG/Twitter tags live in the static `index.html` and social crawlers don't execute JS, **a CSR Angular app effectively has one shared OG image/title/description for the entire site**, set directly in `apps/frontend/customer-web/src/index.html`:

```html
<meta property="og:title" content="Business Name — Short Value Prop" />
<meta property="og:description" content="One or two sentences, unique to the site as a whole." />
<meta property="og:image" content="https://example.co.za/og-image.png" />
<meta property="og:type" content="website" />
<meta property="og:locale" content="en_ZA" />
<meta name="twitter:card" content="summary_large_image" />
```

There is no per-route equivalent without SSR/prerendering — updating `Meta` at runtime (section 1) does not help here since the crawler never runs that code. If per-page social previews matter (they usually do for a service business sharing individual service pages), this is the concrete, specific case to point to when recommending SSR.

Checklist:
- ⚠️ OG image is a real static asset (1200×630) in `public/`, not a screenshot.
- ⚠️ `og:locale` set to `en_ZA` (or the target locale) for local businesses.
- ❌ Flag explicitly if the user expects per-page social previews — that requires SSR/prerendering, not a `Meta` service call.

---

## 5. Images & media

- ⚠️ Every image should use Angular's built-in `NgOptimizedImage` directive (`import { NgOptimizedImage } from '@angular/common'`, `<img ngSrc="..." width="…" height="…" priority>` for the LCP image) — flag any plain `<img>` found via grep.
- ❌ No missing/empty `alt` attributes. Decorative images use `alt=""`, never omit it.
- ⚠️ `priority` set on the Largest Contentful Paint image (usually the hero) so it isn't lazy-loaded; every other image left to lazy-load by default.

---

## 6. Core Web Vitals / performance

- ⚠️ Fonts self-hosted (`@font-face` pointing at a hashed asset built through `angular.json`'s asset pipeline), not a render-blocking `<link>` to Google Fonts — same principle as `next/font`, no CLI-generated equivalent, so this is manual.
- ⚠️ Route-level lazy loading (`loadComponent`/`loadChildren`) for anything not needed on first paint — check `app.routes.ts`.
- ⚠️ `provideRouter` preloading strategy is deliberate (`PreloadAllModules` for a small app is fine; a large app should use a custom/quicklink-style strategy) — an unset default means no preloading at all, hurting perceived nav speed without helping initial load.
- ⚠️ Bundle budgets configured in `angular.json` (`budgets` under the `build` target) so a regression fails the build, not just a Lighthouse run.
- If Lighthouse/PageSpeed Insights is available, run it and report Core Web Vitals scores before/after — CSR apps typically score worse on LCP/INP than an equivalent SSR app doing the same work, which is expected, not a sign the fix was wrong.

---

## 7. Semantic HTML & URL structure

- ⚠️ One `<h1>` per route, logical heading order (no skipping levels).
- ⚠️ Nav/footer use `<nav>`, `<footer>`, `<main>` — not generic `<div>` soup.
- ⚠️ Angular Router paths are human-readable and kebab-case (`/services/garden-maintenance`, not `/services/:id` with a numeric id in the URL).
- ⚠️ Trailing slash / www vs non-www consistency is enforced at the hosting/DNS layer (Angular's router doesn't own this on a static SPA) — check the Coolify/Azure Static Web App redirect rules and DNS/CNAME setup so canonical and actual served URL match.

---

## 8. Content structure & topical authority

Technical SEO gets a page crawled and indexed (to the extent a CSR app can be). Topical authority is what makes it rank against local competitors who've been publishing longer — this is the part most technical audits skip, and it's independent of the CSR/SSR question.

- **Pillar/cluster structure**: one broad pillar page per core service category, linking out to narrower cluster pages targeting specific queries. Clusters link back to the pillar; related clusters cross-link.
- **Internal links use `routerLink`**, not a plain `<a href>` re-navigating the whole app or a JS-only click handler — `routerLink` renders a real `href` in the DOM, which is what makes the link graph crawlable, not just clickable, even before any JS runs.
- **Location depth, not a thin area list**: for local businesses, real per-suburb content ("Garden Services in Umhlanga") outperforms one generic "areas we serve" page. A templated paragraph with the suburb name swapped in counts as thin/duplicate content and can hurt more than help.
- **FAQ content + `FAQPage` schema**: genuine answers to real customer questions.
- **E-E-A-T (Experience, Expertise, Authoritativeness, Trust)**: matters most for YMYL content — a medical practice site needs visible practitioner credentials and registration numbers, not just a booking form. Testimonials/reviews must be real and attributable (never fabricate — ties back to the `AggregateRating` warning in section 3).
- **Avoid thin pages**: a service page with a heading, a stock photo, and a lead-gen form has little for Google to rank on. Flag pages under ~150–200 words of substantive unique copy.

When auditing, call out thin/duplicate content and missing pillar structure as recommendations for the user to action (write copy, define the cluster map) — don't generate marketing copy unprompted.

---

## Reporting format

When auditing, report like this:

```
## SEO Audit — apps/frontend/customer-web

❌ CSR-only (no @angular/ssr) — OG/Twitter tags, per-route metadata, and JSON-LD are all
   working around this limitation rather than solving it; recommend `ng add @angular/ssr`
✅ RouteSeoStrategy wired, per-route title/description present
❌ No sitemap.xml or robots.txt found under public/
⚠️ og:* tags in index.html are generic site-wide (expected on CSR — flagged, not a bug)
⚠️ 4 <img> tags not using NgOptimizedImage (hero.component.html, gallery.component.html)
✅ LocalBusiness JSON-LD present on homepage, missing on /contact
⚠️ No pillar/cluster structure — 6 service pages exist as flat siblings with no cross-linking
❌ /areas-we-serve uses one templated paragraph per suburb — thin/duplicate content risk
```

Then fix in priority order from the workflow above, confirming scope with the user first if the fix set is large — and lead with the SSR recommendation if it's missing, every time, rather than letting the CSR-workaround fixes read as a complete solution.
