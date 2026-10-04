---
name: "site-generation"
description: "End-to-end AI website generation pipeline. Claude Opus 4.8 emits Bolt-style <boltArtifact> envelopes (multi-file, plan-first) that customize Vite+React+Tailwind templates from pre-researched business data. Pre-research via APIs, media acquisition, brand extraction, visual inspection via GPT Image 2 vision, R2 upload (per-file content-type by extension), D1 status updates. Supports all business types: SaaS, portfolio, non-profit, restaurant, salon, medical, legal, retail, tech."
metadata:
  version: "2.0.0"
  updated: "2026-04-30"
  effort: "xhigh"
  model: "claude-opus-4-8"
  context: "fork"
license: "Rutgers"
compatibility:
  claude-code: ">=2.0.0"
  agentskills: ">=1.0.0"
submodules:
  - bolt-artifact-protocol.md
  - build-breaking-rules.md
  - build-prompts.md
  - domain-features.md
  - homepage-block-library.md
  - local-seo.md
  - media-acquisition.md
  - non-technical-owner-onboarding.md
  - page-set-expansion.md
  - quality-gates.md
  - research-pipeline.md
  - small-business-mode.md
  - source-fidelity-loop.md
  - template-improvements-100.md
  - template-system.md
priority: 3
pack: "website-build"
stage: stable
triggers:
  - "site generation"
  - "bolt artifact"
  - "boltArtifact"
paths:
  - "org:website_build"
---

# 15 — Site Generation

Run the end-to-end AI website generation pipeline: research→media→Bolt artifact emission→R2 upload→D1 status for all business types.

> **Model migration note (pass-78, 2026-06-09)**: `DALL-E` → **GPT Image 1.5** + `GPT-4o` → **GPT Image 2 vision**. Per `platform.openai.com/docs/deprecations`. Generation pipeline unchanged.

## Submodules

- **research-pipeline** — API-driven business research, scraping, enrichment
- **media-acquisition** — image/video/logo sourcing across 17 engines (Flux 1.1 Pro Ultra, Ideogram 3.0, Recraft V3, GPT Image 1.5, Sora) — Pexels-first / AI-fallback, pHash dedup
- **build-prompts** — master prompt + enhancement phases
- **quality-gates** — Lighthouse CI v0.15+, axe-core / playwright v4.11+ WCAG 2.2 AA, source-parity diff, 3-tier visual regression, console-error gate, Recommendations Loop
- **domain-features** — category-specific for 18+ business types
- **template-system** — Vite + React + Tailwind + shadcn/ui starter
- **local-seo** — citation building, GBP sync, review generation, trust badges, local conversion tracking
- **bolt-artifact-protocol** — `<boltArtifact>` XML envelope spec — ordered file/shell actions, PLAN.md-first, runtime parser + executor, ~$6/site at 80K output tokens
- **blog-import.mjs** — RSS-first crawl + Squarespace JSON fallback → strip CMS residue → GPT Image 2 vision-mini typed-block restructure → pHash dedup → `src/data/blog-posts.ts`
- **validate-assets.mjs** — post-build R2/dist gate — 13 mandatory files + every img/link/script/source ref resolves OR matches allowlist

## Dual-Template Architecture (TWO REPOS — NEVER CONFUSE)

- **Local Business**: `megabytespace/template.projectsites.dev` — Vite + React + Tailwind + shadcn/ui, 15 local components, CSS var brand slots. Use for: restaurant, salon, medical, legal, fitness, contractor, retail, etc.
- **SaaS**: `megabytespace/saas-starter` — Hono + D1 + Clerk + Stripe + Inngest + Resend on CF Workers. Use for: SaaS products, APIs, dev tools, platforms.

### Template selection (from `_form_data.json.category`)

- `restaurant|cafe|salon|spa|medical|dental|legal|fitness|automotive|construction|photography|real_estate|education|financial|retail|pet_services|wedding|church|nonprofit|government` → `template.projectsites.dev`
- `saas|api|platform|devtool|marketplace` → `saas-starter`
- Unknown → local business

### Auto-sync

After ANY change to skills 05-15, evaluate: "Does this improve template?" If yes → push to appropriate template repo same prompt.

## Generation Protocol

Model emits ONE `<boltArtifact>` XML envelope with ordered `<boltAction type="file" filePath="…">` and `<boltAction type="shell">` actions. See `bolt-artifact-protocol.md`.

- First action ALWAYS `PLAN.md` (route tree, design-token diff, media count, file count, validators)
- Runtime parser validates first-action-is-PLAN.md + required-files + `npm…build` shell action; failures re-prompt (max 2 retries)
- Executor modes: `container` (default — `git clone template → npm install → vite build → upload dist/`) | `r2-files` (pre-built static)

## Pipeline

```
Phase 0: Pre-Research + Media Acquisition (ALL BUILD MODES)
  → Google Places, scraping, social verification, brand extraction, media discovery
  → Download ALL images from original; stock via Pexels/Pixabay; AI via GPT Image 1.5 / Stability AI
  → YouTube/Pexels video embeds
  → Output: _research.json, _scraped_content.json, _assets/
  → HARD GATE: <10 images = build NOT complete

Phase 1: Claude Opus 4.8 Bolt-Artifact Emission (Worker OR Container)
  → Reads all _ context files; emits ONE <boltArtifact> envelope
  → First action ALWAYS PLAN.md
  → Customizes pre-installed Vite+React+Tailwind+shadcn/ui template
  → Builds 1:N-page site MATCHING source sitemap (every URL recreated, max 1000)
  → Clean URL slugs (never copy CMS garbage like -1 suffixes)

Phase 2: Post-Build Verification (Worker)
  → Screenshot via microlink.io → GPT Image 2 vision scoring
  → D1 status update → email notification
```

CRITICAL — In manual/prompt-based builds (no container), Phase 0 runs INLINE as first step. Agent MUST: (1) WebFetch original site pages + extract all image URLs; (2) download images to `public/`; (3) search + download stock photos; (4) generate AI images if API keys available. ALL BEFORE writing any React code. Text-only site = failed build.

## Context Files (written before model runs)

- `_research.json` — business profile + hours + phone + address + reviews + geo
- `_brand.json` — colors + fonts + personality + logo URL + color_source
- `_citations.json` — APA 7th bibliography keyed by refId per `citations.md`
- `_scraped_content.json` — all pages by URL
- `_assets.json` — image manifest w/ metadata
- `_image_profiles.json` — GPT Image 2 vision analysis per image: quality + placement + colors
- `_videos.json` — YouTube/Pexels embed URLs + metadata
- `_places.json` — Google Places enrichment: photos + reviews + rating
- `_form_data.json` — user-submitted from `/create`
- `_domain_features.json` — category-specific feature requirements

## Build Rules (NON-NEGOTIABLE)

### Images

- USE ALL images in `assets/`. Never external URLs (hotlinking blocked).
- Hero: `assets/hero-*`. Gallery: full-width slider w/ ALL images. No image left unused.
- Minimum count: `max(30, original_image_count × 1.4, page_count × 6_home_or_4_sub)` — 4-page rebuild ⇒ 30-50 images; 50-page ⇒ 200+; 500-page ⇒ 2000+
- Per-page floor: home ≥6, every sub-page ≥4. Minimum 5 AI-generated GPT Image 1.5 originals per site.
- All images through optimization pipeline (skill 12): WebP + AVIF at 320/640/1280/1920w, blur placeholders, dominant color extraction. Use `<ResponsiveImage>`, never raw `<img>` w/ PNG/JPG src.
- Dedupe via 301 not deletion — md5-hashed twins keep canonical, emit `{deleted-url:canonical}` to Worker redirect map.

### Video

- Walker captures `<video>` + `<source>` + `<iframe src*=youtube|vimeo|wistia|loom>` + `data-video-id` + CSS `background-video` + autoplay-loop hero MP4s + animated WebPs + lottie `.json`
- Output `_videos.json` keyed by source URL w/ `{src, poster, duration, dims, transcript?, captions_vtt?, original_route, slot_hint}`
- Template's `<VideoEmbed>` lazy-loads, poster-first, captions if VTT exists, respects `prefers-reduced-motion`
- Augment via Pexels Video API (free) + YouTube Data API search-by-topic for missing background loops
- Video count gate: every original `<video>` and embed accounted for in `_videos.json`; missing = fail

### GPT Image 1.5 Purpose-Craft (per-slot prompts — never generic)

Every AI-generated image brief MUST include: (1) route + section (`/about hero`); (2) page topic + intent; (3) brand palette tokens by hex from `_brand.json`; (4) composition + aspect ratio; (5) subject specificity (named noun + modifiers + lighting + lens metaphor); (6) negative prompt (no text, no watermarks, no AI artifacts, no extra fingers, no logos).

Build `_image_briefs.json` per site BEFORE generation — one brief per slot, reused across fallback chain (GPT Image 1.5 → Ideogram → Recraft). Generic "create a hero image" = fail; discarded + brief regenerated.

### Per-Route SEO

SPAs swap meta on `useLocation()` change via `<PageHead />` reading `src/data/page-meta.ts`. Each entry: title 50-60ch keyphrase-first | desc 120-156ch | canonical + og:*+ twitter:* + JSON-LD (Org/Service/BlogPosting/BreadcrumbList/FAQPage). Hard gate: every `<Route path>` has `page-meta.ts` entry or data-derived meta.

### Font-Flash Mitigation

`index.html` `<head>`: `<link rel="preload" as="style">` + animate.css + `html:not(.fonts-loaded) body { opacity: 0 }` + inline `document.fonts.ready.then(reveal)` + `setTimeout(reveal, 1200)` safety net.

### Hero Context Match

Every hero image/video literally depicts page topic — `/mass-schedule` gets stained-glass-window, `/donate` gets volunteers-serving. AI-vision QA scores `image_matches_page_topic` 0-10 per hero; <8 = replace.

### Empty-Config Widgets

Gate every third-party widget on env var: `{import.meta.env.VITE_TURNSTILE_SITEKEY ? <div className="cf-turnstile" data-sitekey={...} /> : null}`. Same for Stripe pk, PostHog snippet, Resend embed. Empty `data-sitekey=""` = console error on every render.

### Post-Deploy Parallel Scan (BOTH scripts required — deploy not verified without both)

- `scripts/scan-assets.mjs` — Playwright concurrency 6, captures console errors/warnings + `requestfailed` + `response.status>=400` per route
- `scripts/check-routes.sh` — curl every route + every blog slug for non-200

### Design

- Dark-first, brand-extracted base color (skill 10 — MANDATORY) | 10+ `@keyframes` animations
- Glassmorphism cards (`bg-white/5 backdrop-blur-md border-white/10`) | gradient text on key headings
- Parallax-style depth on hero | 25+ inline SVG decorative elements
- Every interactive element has hover + active + focus states
- Smooth scroll for ALL same-page nav (`scrollIntoView`, never `#href` jumps)

### Content

- Word count MATCH OR EXCEED original — never ship less content; 5000+ words minimum
- Migrate ALL blog posts, news, events, team bios from scraped content
- About page 2000+ words | every claim factually accurate from research
- Blog → individual routes per post with RSS feed
- Addresses → Google Maps links | phone → `tel:` links | email → `mailto:` links

## See submodules for: research-pipeline, media-acquisition, build-prompts, quality-gates, domain-features, template-system, local-seo, bolt-artifact-protocol, page-set-expansion, source-fidelity-loop, build-breaking-rules.
