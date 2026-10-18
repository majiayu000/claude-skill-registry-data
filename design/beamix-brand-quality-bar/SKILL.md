---
name: beamix-brand-quality-bar
last_updated: 2026-05-17
description: "Beamix billion-dollar-feel design rules: color palette v4.0 (blue #3370FF accent), typography system (InterDisplay + Inter + Fraunces + Geist Mono), spacing, animation budget, and empty-state requirements. Use before any design implementation or design review."
tags: [design, beamix-specific, frontend, brand]
source: beamix-authored 2026-05-16
risk: low
---

# Beamix Brand Quality Bar

## Quick reference

> Stripe / Linear / Apple / Anthropic-grade. Every space, button, letter intentional. If it would embarrass at YC demo day, it ships at half quality.

## When to use

- Before implementing any UI component or page
- Reviewing a design deliverable from product-designer or design-critic
- Checking whether a Framer marketing change or Next.js dashboard update is on-brand
- Settling color, font, or spacing questions without asking Adam

## When NOT to use

- For agent-to-agent communication design (this covers user-facing product and marketing surfaces only)

## The quality bar

Every pixel, space, button, and letter must be intentional. The reference quality is Stripe/Linear/Apple/Anthropic. Ask: "Would this ship on stripe.com?" If not, it's not done.

Specific failure patterns to eliminate:
- Placeholder color ("I'll fix the blue later")
- Generic shadows (box-shadow: 0 2px 4px rgba(0,0,0,0.1) is not a design decision)
- Inconsistent spacing (pick from the 8pt grid and stay there)
- Mixing font weights without a reason
- Animations that run on every page load without adding meaning

## Color palette (v4.0 — locked)

### Use these

| Token | Hex | When to use |
|-------|-----|-------------|
| Background | `#FFFFFF` | Primary page background |
| Surface Alt | `#F7F7F7` | Section backgrounds, alternating panels |
| Primary Text | `#0A0A0A` | All headings and body copy |
| Muted Text | `#6B7280` | Descriptions, captions, secondary labels |
| Card Border | `#E5E7EB` | Card and input borders |
| **Primary Accent** | **`#3370FF`** | CTAs, links, logo mark, active states, charts |
| Secondary CTA | `#0A0A0A` | Secondary action buttons |
| Warm surface | `#F7F6F2` | Empty states, onboarding, first-run — never grey-on-grey |

### Score colors (data viz only — never buttons or links)

| Level | Hex | Range |
|-------|-----|-------|
| Excellent | `#06B6D4` | 75–100 |
| Good | `#10B981` | 50–74 |
| Fair | `#F59E0B` | 25–49 |
| Critical | `#EF4444` | 0–24 |

### Dark mode accent

| Token | Hex |
|-------|-----|
| Primary Accent (dark) | `#5A8FFF` |

### Retired — do not use

```
Navy #023C65
Yale Blue #25426A
Blue Slate #536D84
Old orange #F97316
Old indigo #6366F1
Old orange accent #FF3C00
Old background #FAFAF9
Cyan as accent #06B6D4 (score use only — never as CTA or link)
```

Any PR using these colors is returned BLOCK by design-critic.

## Typography

| Font | Use | Do NOT use for |
|------|-----|---------------|
| `InterDisplay-Medium` | All headings (48–72px), tight tracking -2px | Body copy, UI labels |
| `Inter` | Body (16–20px), UI labels, captions | Headings |
| `Fraunces` | Dark sections + testimonial carousel only, white text | Any light-background section |
| `Geist Mono` | Code blocks, scan data, JSON output | Regular copy |

### Type scale

| Level | Size | Weight | Line Height |
|-------|------|--------|------------|
| Hero / Display | 56–72px | InterDisplay-Medium | ~1.05 |
| H1 | ~40px | InterDisplay-Medium | 1.1 |
| H2 | ~28px | Inter 600 | 1.2 |
| H3 | ~20px | Inter 600 | 1.3 |
| Body | ~16px | Inter 400 | 1.6 |
| UI Label / Caption | ~13px | Inter 500 | 1.4 |
| Section Eyebrow | 12px | Inter 600 uppercase | — |

**Capitalization:** H1 Title Case. H2–H6 Sentence case.
**Reading width:** Body 560px max. Headlines 640px max.

**Retired fonts (never use):** Montserrat, Outfit, Source Serif, DM Serif, PT Sans, Plus Jakarta Sans, Figtree.

## Buttons

| Type | Shape | Background | Text |
|------|-------|-----------|------|
| Primary marketing | Pill (999px radius) | `#3370FF` | `#FFFFFF` |
| Secondary marketing | Pill (999px radius) | `#0A0A0A` | `#FFFFFF` |
| Product utility | Rounded-lg (8px radius) | Context | Context |

Primary and secondary marketing buttons never have a border — fill only.

## Spacing system (8pt grid)

```
4px   — icon internal padding, tight inline gaps
8px   — component internal padding (card headers, input padding)
16px  — standard component padding, row gaps in forms
24px  — section internal spacing
32px  — between components in a section
48px  — between page sections (mobile)
64px  — between page sections (desktop)
96px  — hero to first section
```

Deviations from the 8pt grid require an explicit reason in the PR description.

## Animation budget

Not every page gets motion. Motion must add meaning.

| Tier | Budget | When to use |
|------|--------|-------------|
| Tier 1 | One signature animation | Hero section, onboarding completion |
| Tier 2 | Subtle transitions only | Page transitions, state changes |
| Tier 3 | No animation | Data tables, dense dashboards |

Animation rules:
- Duration: 200–400ms for UI interactions. 600–1200ms for hero/intro animations.
- Easing: `ease-out` for elements entering. `ease-in` for elements leaving.
- No animation that repeats on every page load without user trigger (except hero — one per session)
- Respect `prefers-reduced-motion` — all animations must have a static fallback

## Empty states

Every list, table, or data view must have an intentional empty state. No blank white space.

Empty state requirements:
- Illustration or icon (on-brand, not stock)
- Headline: specific to what's missing ("No scans yet" not "No data")
- Action: one clear CTA that resolves the empty state
- Copy: voice canon compliant (no buzzwords, direct, warm)

```tsx
// Example empty state component
<EmptyState
  icon={<ScanIcon />}
  headline="No scans yet"
  body="Your first GEO scan shows where AI search engines rank your business."
  action={<Button variant="primary">Start your first scan</Button>}
/>
```

## See also

- `design-taste-frontend` — [[design-taste-frontend]]
- `high-end-visual-design` — [[high-end-visual-design]]
- `minimalist-ui` — [[minimalist-ui]]
- `wcag-audit-patterns` — [[wcag-audit-patterns]]

## Expanded palette — Design Vision 2026-06-05 (DESIGN-VISION.md §3 is authoritative)

> The laws here are non-negotiable. When this file and DESIGN-VISION.md disagree on the product, DESIGN-VISION.md wins.

### The signature law — blue = you, violet = the agents

The split is not aesthetic preference; it is a product promise baked into the visual language. Every time a user sees the split they learn what Beamix does for them.

| Color | Hex | Role | Hard rule |
|-------|-----|------|-----------|
| **Blue (accent)** | `#3370FF` | Your actions: primary CTAs, links, active nav, focus ring, hero metric | The ONLY primary/CTA color. One per surface. |
| Blue tint | `#EEF2FF` | Hover fills, tag backgrounds, info badge ground | Never on buttons |
| Blue deep | `#2454D6` | Pressed state, dark-surface CTA | Accent family only |
| **Violet (agent)** | `#6E56F0` | Agent runs, automations, AI chat, scan-engine diagram, score-reveal gradient | **NEVER a button.** Not a link. Agent surfaces only. |
| Violet tint | `#EEEAFD` | Agent status badge ground, agent card tint | Background/indicator only |

The one sanctioned gradient: `#3370FF → #6E56F0` (hero, AI surface, score-reveal only).

### Warm off-white surface

`--color-surface-warm: #F7F6F2` — use instead of `#F7F7F7` when the intent is warmth (empty states, onboarding, first-run). Avoids grey-on-grey-on-grey wash.

### Washes — background and illustration fills ONLY

Never on text, buttons, interactive elements, or data visualization.

| Token | Hex | Allowed use |
|-------|-----|-------------|
| `--color-wash-sky` | `#EAF0FB` | Hero bg, empty-state illustration fill |
| `--color-wash-lavender` | `#ECE7FB` | Agent/AI section wash |
| `--color-wash-blush` | `#FBEAF0` | Warm accent moment (testimonial, onboarding) |
| `--color-wash-mint` | `#E6F5EE` | Success / positive moment bg |

### Status pill set

Always: tinted ground + saturated text. Never loud fills. Both vars required per pill.

| State | Text token | Background token |
|-------|-----------|-----------------|
| Info | `--color-status-info` `#3370FF` | `--color-status-info-bg` `#EEF2FF` |
| Agent | `--color-status-agent` `#6E56F0` | `--color-status-agent-bg` `#EEEAFD` |
| Positive | `--color-status-positive` `#0E9E6E` | `--color-status-positive-bg` `#E6F5EE` |
| Warning | `--color-status-warning` `#B8770B` | `--color-status-warning-bg` `#FDF3E0` |
| Critical | `--color-status-critical` `#DC2626` | `--color-status-critical-bg` `#FDECEC` |
| Neutral | `--color-status-neutral` `#6B7280` | `--color-status-neutral-bg` `#F3F4F6` |

### Data-viz series

`data-1 #3370FF` · `data-2 #6E56F0` · `data-3 #06B6D4` · `data-4 #10B981` · `data-5 #F59E0B` · `data-6 #EF4444` · grid `#EAEAEA`. Default to the blue/violet pair + desaturated tints. Pastel multi-band, not loud.

### Dark panels

`--color-panel-dark #14140F` · `--color-panel-navy #0E1424` — select contrast sections (testimonials, scan-engine diagram, dark hero). Fraunces is allowed here (and only here on the product). Never use a reference's maroon/plum — take the dark-panel move, keep the Beamix palette.

### Character — in moments only

Animated character appears **only** at: empty states · first-run · loading · 404. No persistent companion. See `project_beamie_deferred` decision.

### Motion — minimal, transitions only

`ease-out` hovers and page transitions everywhere. No choreographed set-pieces. `prefers-reduced-motion` fallback always required. **One exception:** the free-scan score-reveal (animated ring + engine ledger) — the acquisition dopamine moment, already shipped. Nothing else in the product animates beyond transitions.

### Fraunces — editorial moments only

Dark panels · testimonial carousel · hero display · report covers · score-reveal verdict · the mixed sans+italic-serif headline device. **Never** in product UI chrome (nav, cards, tables, forms, dashboards).

## Anti-patterns

- Using orange, navy, or cyan as accent colors (all retired)
- Using `#3370FF` for data visualization (accent is for actions, not data)
- Using Fraunces on light backgrounds (testimonial / dark section only)
- Using violet `#6E56F0` on a button or link — ever
- Using washes (`#EAF0FB` etc.) on text, buttons, or data elements
- Generic drop shadows without a specific reason
- Animation on every render without `prefers-reduced-motion` check
- Empty white space where an empty state should be
- Body copy wider than 560px (hurts readability)
- Mixing font weights in a single heading (pick one weight per level)
