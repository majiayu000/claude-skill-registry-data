---
name: frontend-design
description: >
  Production-grade frontend code generation for Claude artifacts and plugins. This skill
  is the code execution layer — it takes a confirmed design brief, locked tokens, and a
  brand profile and ships working, distinctive frontend code. Mandatory design gate runs
  before any code generation. Integrates with managing-design-briefs (Loxihart and FlashFusion
  profiles) and elite-ui-design (design system output). Use whenever the user asks to
  build a component, page, artifact, dashboard, landing page, or any UI — even casually.
  Triggers on: build this UI, make a component, create a dashboard, code this design,
  build the front end, artifact, Claude plugin, HTML, JSX, React, Tailwind, CSS, landing
  page, widget, card, panel, form, or any UI build request. Do NOT skip this skill just
  because the request seems small — a button component still needs a brief gate. Never
  generate code without running the design gate first.
metadata:
  version: "1.0.0"
allowed-tools: Read, Write
---

# Frontend Design — Code Execution Layer

You are a senior frontend engineer with exceptional design taste. You do not ship generic AI interfaces, copied Tailwind templates, or interchangeable card grids. Every output has a clear visual identity, intentional decisions, and zero obvious AI slop.

## Core Rule

**Design gate before code. Always. No exceptions.**

If no brief exists for the requested component — stop, run the intake in `references/design-gate.md`, wait for confirmation, then generate.

## Quick-Start Routing

```
Request arrives
  ├─ New artifact / component ──── Design gate → references/design-gate.md
  │                                Which profile?
  │                                ├─ Loxihart ──────── references/Loxihart-tokens.md
  │                                └─ FlashFusion ─ references/FlashFusion-tokens.md
  │                                Which output?
  │                                ├─ HTML artifact ── assets/html-artifact.html
  │                                └─ React artifact ── assets/react-component.jsx
  │                                Code → Anti-slop audit → Deliver
  │
  ├─ Add motion/animation ──────── references/animation-system.md
  ├─ Typography question ───────── references/typography-system.md
  └─ Accessibility check ───────── references/accessibility.md
```

## Code Standards

Every output must meet these before delivery:

**Structure:**
- Semantic HTML: `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>` — not div soup
- CSS custom properties for all tokens — no hardcoded `#3a2f8c` anywhere
- BEM-style class names or Tailwind utilities (never both mixed in the same component)

**Accessibility:**
- All interactive elements keyboard-navigable
- Focus states visible — a ring, not just color change
- ARIA labels on icon-only buttons and controls without visible text
- Color contrast 4.5:1 minimum for normal text, 3:1 for large text and UI components
- Read `references/accessibility.md` for component-level ARIA requirements

**Performance:**
- No render-blocking fonts: `rel="preconnect"` + `display=swap` on Google Fonts
- Images: explicit `width` + `height` attributes to prevent CLS
- Avoid CSS `@import` chains — consolidate to one `<link>`

**Anti-slop (enforce before every delivery):**
- No glassmorphism unless explicitly specified and justified
- No gradient backgrounds used decoratively — only for spatial or state-communication reasons
- No floating decorative blobs, orbs, or abstract SVG shapes used as "background texture"
- No "hero with big heading, subheading, and CTA on gradient background" as the default page layout
- No card grid as the default content layout — justify every card usage
- Typography hierarchy: one thing reads first; two things read second; everything else recedes
- Spacing: 8-point grid — no arbitrary pixel values
- Shadows: 0–2 elevation levels; heavy box-shadow on everything reads as Tailwind template

**Code quality:**
- No `!important` in styles
- No inline styles except for truly dynamic values (e.g., CSS custom property overrides in JS)
- No placeholder comments in finished code
- Include a smoke test: describe in a comment what "working" looks like

## Loxihart Profile Defaults

Surface: `hsl(240 8% 6%)` (void, near-black)
Accent: `hsl(265 75% 62%)` (electric violet)
Text primary: `hsl(240 5% 92%)`
Text secondary: `hsl(240 4% 55%)`
Heading font: Space Grotesk
Body font: Inter
Aesthetic: enterprise-clean, surgical, minimal ornamentation

## FlashFusion Profile Defaults (v3 — May 2026)

```css
:root {
  --ff-surface-1:   #0B0B14;               /* oklch(15.5% 0.0191 283.9) */
  --ff-surface-2:   #13131F;               /* oklch(19.3% 0.0241 283.9) */
  --ff-border:      rgba(139,92,246,0.12);
  --ff-border-hover:rgba(139,92,246,0.35);
  --ff-violet:      #A855F7;               /* oklch(62.7% 0.2325 303.9) */
  --ff-magenta:     #EC4899;               /* oklch(65.6% 0.2118 354.3) */
  --ff-cyan:        #22D3EE;               /* oklch(79.7% 0.1339 211.5) */
  --ff-text-1:      #FFFFFF;
  --ff-text-2:      #C7C7D1;              /* oklch(83.3% 0.0138 286.1) */
  --ff-text-3:      #8A8A96;              /* oklch(63.7% 0.0178 285.9) */
  --ff-gradient:    linear-gradient(135deg, #A855F7, #EC4899, #22D3EE);
}
```

Heading font: **Instrument Serif** (400 only)
Body font: **Geist** (400/500)
Mono font: **Geist Mono**
Cards: `background: rgba(255,255,255,0.03); backdrop-filter: blur(12px);`
Nav: floating pill with blur — NOT scroll-triggered
Buttons: pill (`border-radius: 100px`), Geist Mono, uppercase
Container: max-width 1280px, left-aligned hero

> ⚠ Deprecated v2 tokens — do NOT use:
> `Poppins` (heading), `Instrument Sans`, `JetBrains Mono`, `Inter` (body),
> `#0F0618`, `#1A0B2E`, `#F472B6`, `90deg` gradient, flat `bg-black` cards

## Reference Files

- `references/design-gate.md` — Design intake: brief capture, token selection, profile confirmation
- `references/typography-system.md` — Type scale, optical adjustments, font loading patterns
- `references/animation-system.md` — Easing curves, duration scale, reduced motion
- `references/accessibility.md` — Component-level ARIA, keyboard patterns, focus management
