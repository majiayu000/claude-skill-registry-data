---
name: flagship-build
description: Build a 1-of-1 bespoke flagship demo site (NOT a template variant). Use when user wants premium $5K-15K-tier showcase site that must look like it cost $50K+. Distilled from SkynetLabs niche-demo audit 2026-05-10 — found template DNA killed pitch credibility. Trigger phrases — "flagship build", "bespoke flagship", "premium demo", "/flagship-build", "build amazing site for [niche]".
---

# Flagship Build — 1-of-1 Bespoke Demo

You are senior creative director + full-stack engineer building bespoke flagship for niche `[<NICHE>]`. NOT template variant. Buyer test: "Would top agency in this niche pay $15K to license this design?"

## Hard constraints (kill deal if violated)

- ZERO template DNA. Layout grid, hero pattern, section order, motion language MUST feel original to niche. Compare against your shipped niche demos and DIVERGE.
- Real or cinematic-AI imagery only. NO Unsplash stock heroes.
- Hero contains ONE memorable scenario buyer describes to friend in one sentence.
- Lighthouse mobile ≥95. LCP ≤2.5s. Bundle ≤180KB initial JS.
- ABSOLUTE: zero demo poison ("Demonstration", "fictional"), zero Gmail, zero 555 phone. ABA / HIPAA / DSGVO compliance per niche.

## Phase 1 — concept (research before code)

Spawn 6 parallel research agents:

1. Top 10 design references in niche (Awwwards / FWA / Behance picks)
2. Top 5 actual high-paying clients in niche (real businesses for benchmark)
3. Buyer pain language (Reddit + niche forums + 1-star competitor reviews)
4. Compliance + legal disclaimers required
5. Conversion-rate benchmarks (form fill / call / book)
6. Pricing benchmarks for design work in niche

Synthesize 1-page concept doc:

- Emotional promise (1 line)
- Visual metaphor (1 line)
- 3 reference sites + what to steal from each
- Buyer's "I want THAT" moment

## Phase 2 — design system

Distinct from prior Skynet demos:

- Palette: 1 primary surface + 2 accents + 1 ink. WCAG AA contrast.
- Type pair: 1 display + 1 body. Real licensed OR Google variable.
- Layout grid: NOT 12-col bootstrap. Editorial / magazine / brutalist / cinematic-letterbox / asymmetric.
- Motion language: scroll-driven OR magnetic OR ambient parallax. Reduced-motion fallback.
- Hero scenario: 30-sec script. What buyer SEES in first 3 / 8 / 30 sec.

## Phase 3 — assets

- Hero imagery: AI-generate (Midjourney/SD3/DALLE3) with locked style frame, 12 candidates, pick 1, Topaz upres. OR real photographer.
- Founder/practitioner portrait: AI-consistent character w/ locked seed OR real shoot.
- 6-12 supporting photos / case-study imagery
- 1 hero video loop OR R3F scene
- Logo / wordmark (custom, NOT auto-generated)

## Phase 4 — build

- Next.js 15 App Router + React 19
- Tailwind v4 OR custom CSS where bespoke
- GSAP ScrollTrigger OR Framer Motion (pick 1, not both)
- R3F where hero requires (lazy + dynamic ssr:false + mobile fallback)
- Custom layout components — do NOT inherit Skynet `template/`
- Real form wired (Web3Forms / Formspree / custom endpoint)
- SEO + JSON-LD + OG image (custom hero-derived)

## Phase 5 — content

- 6 named-fictional case studies w/ outcome metrics
- 12 testimonials w/ full names + photo + occupation + quote
- 5 blog/insight stubs w/ real-feel headlines
- About / founder bio (3 paragraphs, voice-distinct)
- FAQ (8 Q&A, niche-specific concerns)
- Trust strip (real licenses + bar admissions + accreditations as image badges, NOT text)

## Phase 6 — conversion

- Calendar embed (Calendly mock or real) on hero + footer
- Lead magnet PDF (Beehiiv embed)
- Inquiry form w/ qualifier fields (budget / timeline / project type)
- Sticky CTA on mobile

## Phase 7 — performance

- Lighthouse mobile ≥95 OR fix
- LCP ≤2.5s
- JS bundle ≤180KB
- Image LCP element preloaded
- Fonts subset + display:swap

## Phase 8 — ship

- Deploy Vercel prod (set `git config user.email you@example.com`)
- Custom subdomain `flagship-<niche>.vercel.app` OR own .com
- Loom 2-min walkthrough recorded (or transcript ready for you to record)
- Lead magnet PDF uploaded
- Beehiiv 7-email nurture sequence drafted
- Pitch doc generated (1-pager + 3 case studies)

## Output deliverables

- Live URL
- Loom walkthrough URL (or script)
- Lead magnet PDF
- Pitch doc (PDF)
- Concept doc (PDF)
- Lighthouse report (mobile + desktop)
- Asset bundle (every image / video / 3D file)

## Tier S target list (pick 5)

1. **realestate** — luxury agent, $25K anchor, cinematic property reveal
2. **beauty** (med-spa) — $15K clinic, slow-mo serum + 3D molecule
3. **restaurant** — $8K Michelin-track, chef-at-pass cinematic
4. **law** — $12K boutique partner, marble corridor + verdict ribbon
5. **eventvenue** — $10K, 4-season time-lapse + tour fly-through

## Pricing (commercial wrapper)

| Tier      | Price                              | Volume target       |
| --------- | ---------------------------------- | ------------------- |
| Lite      | $497                               | 20/mo Fiverr        |
| Pro       | $1,497                             | 6/mo Upwork         |
| Flagship  | $4,997-14,997                      | 1-2/mo direct pitch |
| Ecosystem | $14,997-29,997 + $1.5K/mo retainer | 1/mo                |

Year-1 ARR target: ~$500K.

## Sales motion

Demo URL → Loom walkthrough → cold DM/email → calendar book → 30-min discovery → custom proposal → close.

Lead magnets per flagship:

- realestate → "Luxury agent site teardown PDF"
- restaurant → "Reservation funnel checklist"
- law → "Compliant law site checklist"
- beauty → "Med-spa lead-gen audit"
- eventvenue → "Inquiry-form conversion guide"

Beehiiv capture → 7-email nurture → discovery call ask.
