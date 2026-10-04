---
name: "cinematic-website-prime-directive"
description: "One-line-prompt → cinematic, gorgeous, functional, well-tested, deployed website. Pre-hydrated SPA + full PWA kit + JSON-LD rich snippets + third-party integrations. React 19+Vite default (Angular optional). 100 concrete improvements grouped into 10 categories that EVERY single-prompt site build must satisfy before being marked done. Trigger whenever the user says 'make a website for X', 'build a site for X', 'rebuild X.com', or any equivalent one-liner."
when_to_use: "Any one-line website prompt: 'Make a website for X', 'Build a site for Y', 'Rebuild Z.com', or equivalent. Trumps generic 06-build-and-slice-loop."
effort: "xhigh"
model: "inherit"
priority: 2
pack: "website-build"
stage: stable
triggers:
  - "make a website"
  - "build a site"
  - "rebuild"
  - "make site for"
  - "build site for"
paths:
  - "org:website_build"
---

# Cinematic Website Prime Directive

One-line prompt → satisfy all 100 build-breaking rules across 10 categories before DONE.

> **Start here**: `website-build-manifest` is the cross-linked acceptance index for the whole one-prompt build (phase order, per-page/per-site gates, architecture, quality bar, `EMDASH_*` config). Load it first, then this skill's 100 rules + the detail rules it links.

## 1. Cinematic Visual Doctrine (1-10)

1. Dark-first (`#060610` base) + bold accent (`#00E5FF` / `#7C3AED` / `#50AAE3`) — never neutral grey
2. Fluid `clamp()` type — body 16-19px, display 64-128px, ratio 1.25-1.333
3. Sora + Space Grotesk + JetBrains Mono (variable woff2 subsets preloaded)
4. Layered surfaces: opaque base + semi-transparent panels + glassmorph cards via `backdrop-filter`
5. OKLCH palette w/ `color-mix(in oklch, ...)` derived shades — no static rgb tints
6. `text-wrap: balance` headings, `text-wrap: pretty` body — no orphans
7. One signature motion per page (scroll-driven parallax, view-transition swap, popover anchor)
8. Hero MUST use AI-generated brand-aligned image, never stock placeholder
9. Asymmetric hero grids, never centered-stack default
10. Every section pair has visual rhythm: dense → breath → dense

## 2. Pre-Hydrated SPA + Routing (11-20)

11. React 19 + Vite + Tailwind v4 + TanStack Router (default)
12. Astro 5 + React islands for marketing-static-heavy
13. Next.js 15 App Router only when SSR/ISR adds real value
14. Angular 22 + Ionic + Spartan UI only when user says "Angular" or signal-heavy enterprise
15. View Transitions API (`@view-transition { navigation: auto; }`) for SPA page swaps
16. Selective hydration per island (Astro) or RSC boundaries (Next)
17. Prefetch on link hover via TanStack Router or Astro `prefetch="hover"`
18. Speculation Rules `<script type="speculationrules">` `prerender` `eagerness:"moderate"`
19. Route code-split via `React.lazy` + Vite `manualChunks` — no single chunk >250KB gz
20. Static HTML shell prerendered w/ H1 + meta tags — never script-injected

## 3. PWA Kit (21-30)

21. `site.webmanifest` w/ `name`, `short_name`, `description`, `theme_color`, `background_color`, `display:"standalone"`
22. `screenshots[]` ≥3 entries w/ `form_factor:"wide"` + `form_factor:"narrow"`
23. `shortcuts[]` for top 3 actions, `share_target`, `file_handlers`, `protocol_handlers`
24. Maskable icons 192/512 + monochrome notification icon
25. Workbox v7 SW: `StaleWhileRevalidate` HTML/JS, `CacheFirst` + `ExpirationPlugin` images
26. `offline.html` shell w/ branded copy + link to cached pages
27. A2HS install banner via `beforeinstallprompt` + iOS separate UI
28. iOS splash via `apple-touch-icon` 180×180 + `apple-touch-startup-image`
29. iOS Safari 18.4 Declarative Web Push opt-in (PWA-installed only)
30. Kill-switch SW (unregister + clear caches) as fallback

## 4. Structured Data + Rich Snippets (31-40)

31. 5+ JSON-LD blocks per route minimum
32. Always: `WebSite` + `Organization` + `WebPage` + `BreadcrumbList` + `FAQPage`
33. Page-type add-ons: `LocalBusiness`, `Product`, `BlogPosting`, `HowTo`, `Person`
34. Author schema (`Person` + `sameAs`) + `dateModified` on every content page (EEAT)
35. JSON-LD facts MUST also appear as visible HTML body text
36. Validate every route against Google Rich Results Test API before deploy
37. Schema.org `citation: CreativeWork[]` array for every quantitative claim
38. Itemprop attributes mirror JSON-LD on key elements
39. No duplicate `@id` across blocks; use stable IRIs
40. `inLanguage` on every block; `isAccessibleForFree:true` on public content

## 5. SEO + AI Search / GEO (41-50)

41. Title 50-60 chars HARD, meta desc 120-156 chars HARD, keyphrase 0.5-3%
42. OG card 1200×630 ≤100KB BRANDED (not scraped photo)
43. Twitter Card meta on every route
44. `sitemap.xml` w/ `<lastmod>` on every URL
45. `robots.txt` triple-state: Allow OR Disallow per GPTBot, ClaudeBot, Claude-User, Claude-SearchBot, PerplexityBot, Google-Extended, CCBot, Bytespider — never default
46. `humans.txt`, `.well-known/security.txt`, `browserconfig.xml`, `llms.txt` (OPTIONAL)
47. Quotable answer blocks 40-60 words per page (LLM citation magnet)
48. `FAQPage` w/ 5+ Q&A blocks (highest AI citation rate)
49. Lead paragraph answers query directly in <40 words
50. Per-route canonical URL (custom hostname when `primary_hostname` set)

## 6. Third-Party Integrations (51-60)

51. GA4 + GTM snippet (head + noscript fallback)
52. PostHog snippet w/ `persistence:'memory'` (cookie-free), autocapture on
53. Sentry `@sentry/cloudflare` v10 + `withSentry` + OIDC DSN
54. Workers Tracing `[observability] enabled = true` + OTLP export to Axiom
55. AI Gateway binding for every LLM call
56. Turnstile invisible (`data-appearance="interaction-only"`) on every form — NEVER visible
57. Stripe checkout / Resend transactional / Clerk auth (M2M JWT) stubs where appropriate
58. Calendly / Cal.com inline booking when applicable
59. Google Maps embed via Maps Embed API, lazy-loaded
60. Live chat (Crisp / Plain) only when support is stated goal. **Cmd+K opens AI chat or command palette AND focuses text input same frame** — `autofocus` + `requestAnimationFrame(() => inputRef.current?.focus({preventScroll:true}))` after open-state flip, re-press = re-focus + `select()`, Esc returns focus to trigger. Playwright build gate: `await page.keyboard.press('Meta+K'); await expect(input).toBeFocused();`

## 7. Performance + Core Web Vitals (61-70)

61. LCP ≤2.0s (target ≤1.5s)
62. CLS ≤0.05 — every image, iframe, ad slot has explicit dimensions
63. INP ≤100ms (target — 200ms is fail)
64. `fetchpriority="high"` on LCP `<img>` AND its `<link rel="preload">`
65. AVIF primary + WebP fallback + JPEG legacy — no JPEG XL
66. Font woff2 subset w/ `unicode-range` per script
67. JS budget ≤200KB gz / route, no single chunk >250KB gz
68. CSS ≤50KB gz, fonts ≤100KB woff2 preload
69. Largest image ≤200KB. Hero image ≤150KB.
70. Long Animation Frames API instrumented for INP debugging

## 8. Accessibility WCAG 2.2 AA (71-80)

71. axe-core 0 violations at all 6 bp (375, 390, 768, 1024, 1280, 1920)
72. Contrast ≥4.5:1 body, ≥3:1 large text + UI components
73. Target size ≥24px (2.5.8 — axe auto-tests)
74. Focus appearance (2.4.11) visible at every interactive — manual review
75. Focus not obscured (2.4.12/13) — sticky headers must not clip focused
76. Dragging alternative (2.5.7) — every drag has click/tap equivalent
77. Consistent help (3.2.6) — contact/help link same location every page
78. Redundant entry (3.3.7) — never re-ask info given
79. Accessible auth (3.3.8/9) — no cognitive-test CAPTCHA; offer passkeys
80. Lighthouse a11y ≥95

## 9. Testing + Verification (81-90)

81. Playwright E2E 6bp covering homepage → key flow → conversion
82. Tests start at homepage, navigate by clicking nav (never `page.goto` for internal)
83. Vitest 5 unit tests for utilities + Zod schemas
84. Lighthouse CI: Perf ≥90, A11y ≥95, BP ≥95, SEO ≥95
85. AI vision QA ≥9/10 per route (visual-qa agent w/ Opus 4.8)
86. Percy AI Visual Review for full-page regression
87. Yoast GREEN on every content page
88. Build validator: every internal asset resolves, every hyperlink valid, every quantitative claim cited
89. CSP report-uri capturing violations during E2E
90. `wrangler tail` clean during smoke tests (no Worker errors)

## 10. Deploy + Observability + Done (91-100)

91. Atomic deploy via Workers Builds (preferred) or `wrangler deploy` + version metadata
92. Gradual deployment (1% → 10% → 100%) w/ auto-rollback on error spike
93. CDN purge paired w/ every deploy
94. `/health` endpoint returns `{status, version, timestamp}`
95. D1 backups: Time Travel 30-day PIT + R2 long-term archive
96. `secrets.required` validated at deploy
97. Self-Verify Statement per route (URL + smoke test result + 3 screenshots)
98. Sentry / PostHog / Workers Tracing / AI Gateway / GA4 all firing — verify in dashboard
99. Browser console: zero errors, zero CSP violations, zero failed resources
100. DONE = deployed at real URL + every Hard Gate green + Self-Verify per route + announced

Anything less than all 100 — plus always-on rules 111-118 (§12) — is in-progress.

## 11. Source-Site Enhancement (101-110 — fires when prompt names existing domain)

101. **Phrase detect** — `rebuild | optimize | enhance | modernize | recreate | clone | better version of {domain}` OR bare-domain prompt where domain resolves 200 = enhancement mode. Output = `union(SOURCE_URLS, STANDARD_PAGE_SET[org_type], DEMOGRAPHIC_LOCALES, JEWELS) − CRUFT_URLS`. See `rules/source-site-enhancement.md`.

102. **Crawl FIRST** — `sitemap.xml → robots.txt → HTML BFS → Wayback fallback → CMS index endpoints (Squarespace /config/pages, WP wp-sitemap-posts-*.xml, Wix _api/v1/sitemap.xml)` → `_url_inventory.json`. Every URL classified `keep | merge | 301 | drop`.

103. **Org-type page-set floor** per `15-site-generation/page-set-expansion.md`:

- nonprofit: 14 standard (home, about, mission, programs, services, team, volunteer, donate, contact, blog, faq, news, financials, annual-report) + 10 jewels
- local-business: ~12 standard + service × city pSEO
- saas: home, product, pricing, features, customers, blog, docs, changelog, security, status, integrations, roadmap, api-docs
- portfolio: home, about, work, blog, contact + per-project pages

104. **Demographic-i18n auto-trigger** via ACS B16001 lookup on service area — every language ≥10% community share gets `/{locale}/*` full route mirror with hreflang cross-refs. Newark NJ ⇒ en+es+pt automatic.

105. **Jewel discovery** (org-type-specific high-value pages absent from source):

- nonprofit: `/parish-toolkit|/planned-giving|/financials|/annual-report|/donate/refurbish|/ways-to-give|/transcript|/alumni|/press|/testimonials|/partners`
- saas: `/changelog|/security|/status|/integrations|/customers|/roadmap|/api-docs`
- local: `/specials|/gallery|/team|/reviews|/insurance|/financing`
- portfolio: `/now|/uses|/colophon|/reading-list`

106. **IA normalize** — `/home → /`, `/our-mission-1 | /blog-1 | /testpage | /new-page-* → drop or 301`, flat `/health-clinic → /services/health-clinic` nested + index when 9+ services. CRUFT_PATTERNS auto-301 to canonical.

107. **Squarespace random-ID slugs** → semantic + 301. Same for Wix `_compiler/page-data` dupes + WP `?p=123` permalinks.

108. **Jewel content authority** via Form 990 / Charity Navigator / Candid / Wayback / Newspapers.com / LinkedIn — never stub, every quantitative claim APA-cited per `rules/citations.md`.

109. **Hard gate page count** — deployed site MUST have `keep_count + standard_gap_count + jewel_count + locale_count*(keep+standard+jewel)` pages. Nonprofits min: `keep + 14 standard + 10 jewels`. Build fails when deployed-route-count < expected.

110. **Monitor-fire on first tool-call message** — rebuild prompt is multi-faceted (≥7 independent work units: crawl → classify → org-type-infer → demographic-i18n → jewel-content-author → IA-normalize → Squarespace-dedupe → deploy-verify). Sequential = build fail. See `rules/source-site-enhancement.md` § Parallel-agent playbook.

## 12. Current-Platform Motion + Asset Discipline (111-118 — always on, every build)

111. **Scroll-driven animation = progressive enhancement** — `animation-timeline: view()` / `scroll()` ONLY inside `@supports (animation-timeline: view())`. Firefox: unsupported as of late 2026 — verify at caniuse before relying. Never animation-only state.
112. **JS fallback auto-disables when CSS wins** — IntersectionObserver reveal runs only where native support is absent: `if (!CSS.supports('animation-timeline: view()')) observe(...)`. Double-driving one element = double motion = fail.
113. **`@starting-style` first-paint entrances** — transition-based, zero JS; pair `transition-behavior: allow-discrete` for display/dialog/popover entry+exit. Baseline mid-2024 (Chrome 117 / Safari 17.5 / Firefox 129) — still verify at caniuse.
114. **Canvas nebula/particle hero layer** — zero-dep 2D canvas: DPR capped at 2, particle density scaled to viewport area, `prefers-reduced-motion` → ONE rich static frame (no rAF loop). Reference impl: claude.megabyte.space hero — `heroNebula` fn in `public/index.html` (heymegabyte/claude.megabyte.space).
115. **rAF pauses on BOTH signals** — `document.hidden` (visibilitychange) AND element-offscreen (IntersectionObserver on the canvas). Either alone still burns battery + CPU.
116. **Bento asymmetry recipe** — auto-fill `minmax()` grid + 1-2 span-2 anchor cards + accent wash on the anchors. A uniform card wall is slop (extends rule 9's anti-centered-stack mandate).
117. **Kinetic gradient type** — `background-clip: text` + `background-size: 200%` (or larger) + slow `background-position` pan; gate on `prefers-reduced-motion: no-preference`.
118. **Immutable assets MUST be content-versioned** — any `Cache-Control: immutable` / 1yr asset ships as hashed filename or `?v=<version>` bumped on EVERY change, INCLUDING any `_headers` Early-Hints preload of the same URL (CF 103 Early Hints cache also lags a deploy briefly). Reference incident (claude.megabyte.space, 2026-10-04): a stylesheet served `immutable, max-age=1yr` on an UNVERSIONED URL left returning visitors on stale CSS indefinitely.
