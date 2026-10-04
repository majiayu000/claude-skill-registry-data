---
name: regen-seo-audit
description: >
  Run a technical SEO audit on regencivics.earth or a specific page. Covers
  meta tags, OG/Twitter card images, structured data (Event, Article, Organization,
  BreadcrumbList), sitemap and robots, internal link patterns, headings/landmarks,
  and the Vite + Wouter SSG limits. Also generates the fix list as a FIXES_TO_MAKE
  doc when the audit finds work. Triggers on: "SEO audit", "SEO check", "audit
  the SEO", "meta tags", "structured data", "schema markup", "OG image", "open
  graph", "Twitter card", "sitemap", "robots.txt", "search ranking", "Google
  rankings", "page rank", "meta description", "canonical URL", "rich results",
  or any request to improve search visibility on the site.
---

# ReGen Civics Technical SEO Audit

## What this skill does

Audit one page or the whole site against a tactical SEO checklist tuned to
the actual constraints of regencivics.earth: a Vite + Wouter SPA with no
SSR, hosted on Railway, content driven by tRPC. Spit out a prioritized fix
list so Rye (or Claude Code) can ship the changes.

This is NOT a generic SEO skill. It assumes the site, the stack, the voice
rules, and the FIXES_TO_MAKE doc convention.

## Stack constraints to understand first

- **Vite SPA, no SSR.** Initial HTML payload is whatever's in
  `client/index.html`. Search engines index the rendered page, but the more
  meta is in the static HTML the better for crawl efficiency, social
  preview, and bots that don't run JS.
- **Wouter for routing.** Per-route meta has to be set client-side via a
  helper (e.g. `<Helmet>` from `react-helmet-async` if installed, or by
  directly mutating `document.head` in a `useEffect`). Check
  `client/src/lib/seo.ts` or similar before rolling new patterns.
- **R2 for images.** OG images live at `assets.regencivics.earth/...`,
  proxied through `/api/img` for resize. Static OG images can sit at the
  R2 root path; dynamic OG (per quest, per event) goes through the proxy.
- **Public routes only.** Anything behind auth (forum, profile, admin) gets
  `noindex, nofollow`. Don't waste crawl budget on private surfaces.

## The audit checklist

Run through these in order. Capture findings into a table with: Issue,
Page(s), Severity (Critical / High / Medium / Low), Recommended fix.

### 1. Per-page meta (every public route)

- [ ] `<title>` set, unique, under 60 chars, ends with " | ReGen Civics"
- [ ] `<meta name="description">` set, 140-160 chars, contains the page's
      core promise + a CTA verb (apply, join, explore, contribute)
- [ ] `<link rel="canonical">` set to the absolute https URL of the page
- [ ] `<meta name="robots">` if it should not be indexed (auth pages, draft
      pages, the dashboard)

### 2. Open Graph + Twitter cards

- [ ] `og:title`, `og:description`, `og:url`, `og:type`, `og:image` all set
- [ ] `og:image` is at least 1200x630, hosted on R2 or CDN, absolute URL
- [ ] `twitter:card` = `summary_large_image`
- [ ] `twitter:title`, `twitter:description`, `twitter:image` set (can mirror
      og: but Twitter's parser sometimes prefers explicit twitter: tags)
- [ ] OG image actually shows the page's content, not a generic logo. Quests
      should have quest-specific images. Events should have event posters.
      Land projects should have project cards.

### 3. Structured data (JSON-LD)

Pick one or more types per page and inject as `<script type="application/ld+json">`:

| Page                        | Schema type(s)                                  |
| --------------------------- | ----------------------------------------------- |
| `/`                         | `Organization` + `WebSite` (with `SearchAction`) |
| `/events/:slug`             | `Event` (with `location`, `startDate`, `offers`) |
| `/projects/:slug`           | `Article` or `LocalBusiness` per project type   |
| `/quests/:id`               | `Quest`-style `HowTo` or `Article`              |
| `/blog/:slug`               | `Article` with `author`, `datePublished`       |
| `/jobs/:slug` (if any)      | `JobPosting`                                    |
| Any list page               | `BreadcrumbList`                                |
| `/economy`, `/governance`   | `Article` with `mainEntity`                     |

Validate each block at search.google.com/test/rich-results before claiming
done. Don't generate JSON-LD that Google's validator rejects.

### 4. Sitemap + robots

- [ ] `sitemap.xml` exists at the site root, lists every public route with
      `lastmod`, generated at build time (script in `scripts/`) or
      server-rendered through an Express route
- [ ] `robots.txt` allows public, disallows `/forum/draft`, `/admin`,
      `/api`, `/dashboard`, `/profile`
- [ ] `robots.txt` references the sitemap with `Sitemap: https://regencivics.earth/sitemap.xml`
- [ ] Submit sitemap once via Search Console (manual step, captured in
      handoff doc)

### 5. Internal link health

- [ ] Every public page is reachable from the homepage in 3 clicks max
- [ ] Critical pages (`/apply`, `/economy`, `/governance`, `/projects`,
      `/quests`) appear in the global nav OR the footer
- [ ] No orphaned routes (live in `client/src/App.tsx` but unreachable)
- [ ] No broken internal links (`/path-that-404s`). Check the `useLocation`
      target of every `<Link>` against the App.tsx route table

### 6. Headings + landmarks

- [ ] One `<h1>` per page, descriptive, contains the page's primary phrase
- [ ] Heading order (h1 then h2 then h3) is hierarchical, no skips
- [ ] Page has a single `<main>` element
- [ ] `<nav>` and `<footer>` landmarks exist on every page
- [ ] Decorative images have `alt=""`. Content images have descriptive alt
      (50-125 chars, no "image of ...")

### 7. Performance signals (light pass)

For deep performance audits, hand off to the `core-web-vitals` skill. The
SEO-relevant checks here:

- [ ] LCP element on each page is identifiable and not blocked by a layout
      shift
- [ ] No render-blocking scripts in `<head>` beyond Vite's required ones
- [ ] Images use `loading="lazy"` below the fold
- [ ] Preload hints for hero images on landing pages

### 8. Mobile + accessibility (SEO-adjacent)

- [ ] Viewport meta tag set in `client/index.html`
- [ ] Tap targets at least 44x44 px on mobile (already audited in
      `regen-ship-gate`, but recheck for landing pages)
- [ ] Color contrast on all text passes WCAG AA (use `regen-form-design`
      checklist or web-quality-audit skill for the deep dive)

### 9. Voice rules (SEO copy)

Meta titles and descriptions must follow the project Writing Rules. Most
common slip:

- Don't pack keywords. "Regenerative Civics | Regen Movement | Land
  Projects | ReGen Civics" reads as spam. Write a sentence a human would
  say.
- Em-dashes banned. Zero. Use a colon or period.
- No contrast framing in meta descriptions. "Not just a fund. A movement."
  is banned. State what it IS.

## Output format: the audit report

When run as a full audit, produce `docs/planning/FIXES_TO_MAKE_YYYY-MM-DD_seo.md`
(use the `regen-fixes-handoff` skill for the doc structure). Tier the
findings:

- **Critical:** missing canonical URLs, missing OG images, broken JSON-LD
  that fails the validator, robots.txt blocking the homepage
- **High:** generic OG image on a high-traffic page, missing per-route
  meta, no sitemap, h1 missing
- **Medium:** thin meta descriptions, internal links to deprecated routes,
  duplicate titles across routes
- **Low:** alt text improvements, lazy-load gaps, breadcrumb schema
  missing on list pages

For each row include the Evidence column (file:line, screenshot, validator
URL output) per the ship-gate convention.

## When run on a single page

If Rye says "audit the SEO on /economy" or similar, run only the relevant
checks against that one route, return a focused report (5-15 line list),
and offer to ship the easy fixes inline if scope permits.

## Quick wins to surface first

If asked "what's the highest-leverage SEO move right now," default to:

1. Add a per-route `useSeo()` helper if it doesn't exist, that sets
   title/description/OG/canonical from a single config object per page
2. Generate dynamic OG images for quests, events, and land projects via
   `/api/og?type=quest&id=...` returning a 1200x630 PNG (or a static set
   committed to R2 if dynamic generation is too much scope)
3. Ship a `sitemap.xml` route at the Express layer, queried from the
   tRPC routes that already enumerate public events / projects / quests
4. Add JSON-LD to the four highest-traffic pages: home, /apply, /economy,
   /governance

## Cross-references

- Use `web-quality-audit` for the full Lighthouse + a11y pass
- Use `core-web-vitals` for performance deep-dive
- Use `regen-fixes-handoff` for the audit report doc
- Use `regen-ship-gate` before claiming any fix VERIFIED
