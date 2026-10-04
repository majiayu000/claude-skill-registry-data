---
name: landing-page-experiment
description: Build a complete A/B test of three landing-page messaging variants. Generates three HTML variants, the cookie-based router that randomly assigns visitors and respects direct links, and a simple admin dashboard tracking views, conversions, CTR, and time on page. Use when the user wants to validate messaging before building the product, says "build me a landing page," "test 3 variants," "stand up a waitlist with an A/B test," or similar.
---

# Landing Page Experiment

Generate a working three-variant landing-page A/B test with routing logic and an analytics dashboard.

## When to trigger this skill

The user wants any of:

- "Build a landing page for [product] and test three messaging angles"
- "Stand up a waitlist with an A/B test"
- "Three variants of [page] with different value props"
- "Landing page experiment for [audience]"

Do NOT trigger this skill when:

- The user just wants copy, no code (use `components/04-launch/*` instead)
- The user wants a single landing page with no variants (this skill always builds three)
- The user wants a multi-page funnel (this skill is single-page only)

## Inputs you need

**Required:**
- Product description (one paragraph)
- Target customer (the persona, ideally from `skills/user-persona/`)
- Three messaging angles to test (e.g. "time saved," "outcomes delivered," "peace of mind")

**Strongly recommended (ask if missing):**
- Brand color (hex)
- Pricing tiers (or "waitlist only, no pricing yet")
- Three to five feature bullets, the same across all variants

## Workflow

### 1. Confirm the matchup

Restate the three messaging angles in your own words and ask for confirmation before generating. Variants are easier to interpret if the angles are genuinely distinct, not three flavors of the same idea.

### 2. Generate the three variants

For each variant (A, B, C):

- Read `template/variant.html` and copy it to `~/landing-experiment/<slug>/variant-{a,b,c}.html`.
- Replace placeholders: `{{HEADLINE}}`, `{{SUBHEAD}}`, `{{FEATURE_N}}`, `{{CTA_TEXT}}`, `{{ACCENT_COLOR}}`.
- **Hold these constant across all three variants:** pricing tiers, feature bullets, layout, CTA text, page structure.
- **Vary only:** headline, subheadline, the order or framing of feature bullets, any hero quote.

### 3. Wire the router

Copy `scripts/router.js` to `~/landing-experiment/<slug>/router.js`. No edits needed unless the user wants different routes. Default behavior:

- First visit to root (`/`): randomly assigns the visitor to variant A, B, or C and sets a cookie that lasts 30 days
- Subsequent visits: the visitor sees the same variant they were assigned to
- Direct links (`/variant-a`, `/variant-b`, `/variant-c`): override the random assignment for testing or for channel-specific traffic
- Tracking parameter `?v=a` appears in every variant's URL after the redirect

### 4. Generate the admin dashboard

Copy `template/admin.html` to `~/landing-experiment/<slug>/admin.html`. It uses localStorage tracking by default (easy to swap to Plausible / PostHog / Google Analytics later).

The dashboard shows per variant:

- Unique views
- CTA conversions
- Click-through rate
- Average time on page
- A description of what's different about this variant
- A link to the live variant
- CSV export of the raw data

### 5. QA check

Before reporting done, verify:

- All three variants share identical pricing, feature bullets, and CTA text
- Router cookie persists across page reloads
- Each variant URL includes the tracking parameter
- The admin page is password-gated (placeholder password — the user replaces it)
- Mobile responsive at 375px width

If any of these fail, fix before delivering.

### 6. Present

Tell the user:

- Where the files live
- That they need at least 100 visitors per variant (300 total) before drawing conclusions
- That they should persist the variant via cookie so the same visitor doesn't see the page switch on them (already wired in `router.js`)
- That they should swap localStorage tracking for a real analytics tool before going live

## Variant generation rules

Pulled from the Escape Velocity Prompt Library; these are what make the test interpretable.

**Vary across variants:**
- Primary value prop (time savings vs quality vs outcomes)
- Audience language (technical vs business vs emotional)
- Emotional vs rational appeal
- Headline framing (painpoint-led vs end-state-led vs cost-of-inaction-led)

**Hold constant across variants:**
- Pricing
- The features listed
- Visual layout and structure
- CTA text (varying this confuses the read)
- Page length
