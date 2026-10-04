---
name: "brand-and-content-system"
description: "Extract real brands (Wayback for rebuilds). Copy system, headline/CTA rules, trust surfaces, legal pages, SEO+structured data, anti-AI-slop, microcopy, DESIGN.md, W3C DTCG tokens, pSEO 5 types, GEO/AI search."
metadata:
  version: "2.1.0"
  updated: "2026-05-03"
  effort: "medium"
  model: "haiku"
license: "Rutgers"
compatibility:
  claude-code: ">=2.0.0"
  agentskills: ">=1.0.0"
submodules:
  - ai-search-geo.md
  - build-breaking-rules.md
  - documentation-and-codebase-hygiene.md
  - email-templates.md
  - grammar-audit.md
  - per-route-metadata.md
  - seo-and-keywords.md
  - social-automation.md
priority: 3
pack: "content"
stage: stable
triggers:
  - "brand"
  - "content"
  - "copy"
paths:
  - "org:website_build"
  - "org:website_build"
---

# 09 — Brand and Content System

Extract real brand assets and apply the full copy system (anti-slop, SEO, trust surfaces, GEO) to every website build surface.

> **Model migration note (pass-77, 2026-06-09)**: `DALL-E` → **GPT Image 1.5** + `GPT-4o` → **GPT Image 2 vision**. Per `platform.openai.com/docs/deprecations`. Brand extraction protocol unchanged.

## Brian's Brand Voice

- Slogans: "Open-Source Wizardry. 100% Wizardry. 0% Robes." / "Often imitated, never duplicated."
- Newsletter: "Lab Insights Journal" | Handle: @HeyMegabyte | Email: hey@megabyte.space / brian@megabyte.space
- Tone: professional but irreverent, "Hey" not "Hi", first-person Megabyte Labs
- Always "cross-platform" + "open-source" | Install Doctor: "single command" / "one-liner"
- Hero: "[Topic] **Innovation**" | Footer CTA: "Let's Talk" | Rates: $140/hr ($70 nonprofit), $100/mo WordPress
- Social: all platforms, "Megabyte Minis" YouTube, Dev.to, Patreon
- Psychology: reciprocity (teach), social proof near CTAs, authority (depth/numbers), unity ("we/us"), Peak-End Rule

## Brand Extraction (Rebuilds)

1. Screenshot existing (Wayback if down). Extract logo/colors/fonts/tone. Never discard equity.

2. **Color extraction (NON-NEGOTIABLE)** — Screenshot with Playwright, GPT Image 2 vision extracts hex (logo priority), cross-ref logo, build palette, validate WCAG AA. NEVER invent, NEVER use Emdash defaults for clients, NEVER infer from category.

3. **Second-pass verification (BUILD-BREAKING — pre-deploy)** — After GPT Image 2 vision returns `{primary, secondary, accent}`:
   - Load logo PNG via sharp, sample dominant chroma via k-means k=5 ignoring transparent + near-white/near-black (top-3 cluster centroids in HSL)
   - For EACH color, compute min HSL hue-distance to top-3 logo chromas — if `min_hue_distance > 30°` AND saturation>0.2, FAIL w/ diagnostic
   - Re-run GPT Image 2 vision w/ corrective prompt naming top-3 logo chromas + demanding `primary` derived from one
   - Validator: `validate-color-from-logo.mjs` in `build_validators.ts` between brand-research and template-pick
   - NEVER ship primary color failing hue-distance check

4. **Logo-luminance + source-theme drives theme (NON-NEGOTIABLE)** — Two-signal:
   - Signal A: logo dominant-color luminance (WCAG formula)
   - Signal B: source-site dominant background luminance (Playwright screenshot of `body` background)
   - BOTH agree → match; disagree → source-site wins UNLESS source design score <7/10 (then logo wins)
   - High-quality source (≥7/10 via GPT Image 2 vision `detail:low`) → match source theme verbatim
   - Set theme BEFORE template selection. Reject palette where logo-on-bg contrast <4.5:1 (WCAG AA).
   - "Dark-first" applies to accent-rich Emdash/SaaS brands, NOT to logo-driven non-profit/serif clients or high-quality light-themed source brands

5. **Logo-vs-container contrast (BUILD-BREAKING — every render)** — Every logo render (header, footer, hero, modal, splash, mobile menu, sidebar) MUST contrast container bg by ≥4.5:1 on logo's dominant chroma (not transparent pixels)
   - Forbidden: white-text-logo on white/cream | dark-text-logo on dark/navy | low-saturation-logo on same-hue bg
   - Resolution: header AND footer themes chosen AFTER logo luminance scan. Dual-theme site needing SAME logo → ship TWO files (`brand-mark-light.svg` for dark bg, `brand-mark-dark.svg` for light bg) + CSS `<picture><source media>` swaps
   - Automate via skill 12 logo-variant-generator (Real-ESRGAN inversion or `magick -channel RGB -negate`; color logos w/ text → GPT Image 1.5 w/ "same logo on transparent bg w/ text inverted to <opposite-luminance>")
   - Validator: `validate-logo-contrast.mjs` — Claude Sonnet 4.6 vision samples logo bbox + container computed bg at 6bp + pixel sampling, fails if <4.5:1

6. **Brand-element extraction (logo is gold mine — extract DNA)** — GPT Image 2 vision returns `{font_family_guess, suggested_heading_font, suggested_body_font, font_weight, letterspacing, has_icon_mark, icon_mark_description, icon_mark_dominant_color, decorative_motif_description, motif_extractable (bool)}`
   - Matched Google Font → `--font-heading` site-wide
   - `motif_extractable=true` → crop icon-only region (`magick logo.png -alpha extract -trim +repage`), upscale 2-4× via Real-ESRGAN / GPT Image 1.5 variation, save as `assets/brand-splash.png` + `assets/brand-mark.png`

7. **Logo singularity (BUILD-BREAKING — exactly ONE logo file per container)** — Every logo container renders EXACTLY ONE logo asset
   - Never composite two logo sources side-by-side; never stack icon-mark + wordmark as separate `<img>` tags; never render `apple-touch-icon.png` next to `logo.svg` in same container
   - Composition at asset-prep time via `magick logo-mark.png logo-wordmark.png +append`, NOT at render time
   - Validator: `validate-logo-singularity.mjs` parses `dist/` HTML; count>1 descendant `<img>` or inline `<svg>` in same logo container = FAIL

8. **Logo (NON-NEGOTIABLE)** — Every project needs premium logo. See Skill 12 for full process.

9. **Audit** — logo found + rated ≥7/10 + works 16-512px, colors EXTRACTED, palette WCAG AA, typography + tone + messages identified.

## Brand Extraction from Physical Assets (LOCAL BUSINESS — NO WEBSITE)

- Street View Static API: `https://maps.googleapis.com/maps/api/streetview?size=1200x800&location={lat},{lng}&source=outdoor`
- Places photos: filter `types: ["exterior", "storefront"]`
- GPT Image 2 vision on storefront — prompt: `"Extract brand identity from this business storefront photo. Return JSON: {sign_text, sign_font_style, primary_color (hex), secondary_color (hex), accent_color (hex), logo_description, overall_aesthetic, confidence (0-1)}"`
- Business cards: GPT Image 2 vision extracts logo (crop region), colors (exact hex), font, tagline, NAP for verification.
- Color extraction priority: 1. Signage → 2. Logo → 3. Storefront awning/trim → 4. Interior decor → 5. Vehicle wrap → 6. Business card → 7. Category default (LAST RESORT). Each tagged with `color_source`.
- Font matching from signage: Script → Dancing Script | Serif → Playfair Display | Modern sans → Inter | Hand-lettered → Caveat. Never use exact proprietary fonts.

## Brand Inference (New Products)

- Dev tool → technical/dark/monospace | SaaS → professional/clean/cards | Agency → confident/bold
- E-commerce → friendly/product-focused | Nonprofit → warm/impact imagery | API → technical/docs-forward
- Emdash defaults (NOT for clients): `#00E5FF`, `#50AAE3`, `#060610`. Sora / Space Grotesk / JetBrains Mono.

## Anti-AI-Slop Detection (MANDATORY SCAN)

**Banned copy words:** `delve | leverage | unleash | revolutionize | best-in-class | cutting-edge | discover | innovative | seamless | robust | synergy | elevate | empower | transformative`

**Banned patterns:** "Welcome to" | "Discover [product]" | vague aspirational headlines | hedging ("may help you," "can potentially") | generic superlatives

**Banned design tells:** Inter as sole font | purple-blue gradients | uniform 16px border-radius everywhere | centered everything | Hero/Lucide as sole icon set | abstract 3D blobs | uniform fade-in on all elements | plastic AI stock photos

Fix: ask "Would the founder actually say this?" No → rewrite.

## Copy System

- Headlines — benefit-first, specific, numbers, max 8 words
- Subheadings — expand promise, 15-25 words
- Body — one idea/paragraph, 2-4 sentences, active, concrete, benefit-oriented
- CTAs — specific action verb first, gradient primary + ghost secondary, above fold + page end
- Never: "Click here" | "Submit" | "Learn more"
- Personality mapping — Expert → precise industry terms | Direct → short declarative | Pragmatic → outcomes/implementation
- Vocabulary: always-use / never-use / prefer-over lists | max sentence: 25 words
- Banned structures: passive voice, hedging, em dashes mid-sentence | monthly drift audit

## Microcopy System

- Error messages — [What happened] + [What to do]. Empathetic, solution-oriented. "Payment failed. Try a different card or contact support." Never "Error 500" or jargon. Flesch 70+.
- CTAs — action verb first, max 3 words preferred: "Start building" | "Ship today" | "Get access"
- Empty states — acknowledge absence + suggest action: "No projects yet. Create your first one." Never just "No results"
- Toasts — past tense success ("Project created"), present in-progress ("Saving…"), plain-language errors
- Form labels — noun phrases, sentence case. Helper text: one line, 10 words max

## Machine-Readable Brand Documentation

- **DESIGN.md** (6 sections): 1. Visual Theme | 2. Color Palette (hex + role) | 3. Typography (family + scale + weight) | 4. Spacing + Layout | 5. Components (states + variants + props) | 6. Elevation + Shadows
- **Tokens**: W3C DTCG JSON format, single source of truth. Generated from `tokens.json` → CSS vars + Tailwind config.

## SEO + Structured Data

### Per-page MUST have

- Title 50-60 chars keyphrase-first | meta desc 120-156 chars | canonical
- OG image 1200×630 branded card | one H1 in prerendered HTML
- JSON-LD: WebPage floor; Org/BreadcrumbList/FAQPage/Person/Product/Service only when real entities

### pSEO 5 page types

- Integration (`/integrations/{tool}`) | Comparison (`/compare/{a}-vs-{b}`) | Use-case (`/for/{audience}`) | Template (`/templates/{type}`) | Location (`/{city}-{service}`)
- Each: unique H1 + meta desc + 800+ unique words + 1 unique image + 3+ internal links + 1+ outbound citation. Never templatize verbatim.

### GEO / AI search

- Quotable answer blocks 40-60 words (LLMs cite)
- FAQPage schema highest AI-citation rate
- JSON-LD facts MUST also appear as visible HTML text | lead paragraphs answer query in <40 words
- EEAT: author bio + Person schema + `sameAs` + dated revision + ownership

## Trust Surfaces

- Real testimonials w/ verifiable attribution | license/accreditation badges
- Security.txt + privacy + terms | Person JSON-LD w/ sameAs | About + Team pages with real bios

## Legal Pages (required)

- /privacy | /terms | /accessibility

## See submodules: email-templates, social-automation, seo-and-keywords, documentation-and-codebase-hygiene, per-route-metadata, grammar-audit, build-breaking-rules.
