---
name: monochrome
description: Single-hue palette with grayscale sophistication, tonal depth, and texture-driven contrast.
---
# Monochrome
## Mission
Achieve sophistication through restraint — a single hue explored across its full tonal range, using texture and weight instead of color variety.
## Brand
### 🎨 Colors
- `#0F172A` — Primary (slate-900, near-black)
- `#334155` — Secondary (slate-700)
- `#64748B` — Accent (slate-500)
- `#F8FAFC` — Background (slate-50)
- `#0F172A` — Text (slate-900)
- `#94A3B8` — Muted text (slate-400)
### 🔤 Typography
- Heading: **Cormorant Garamond** (Google Fonts) — elegant, high-contrast serif
- Body: **Inter** (Google Fonts) — clean workhorse sans-serif
- Scale: xs 0.75rem | sm 0.875rem | base 1rem | lg 1.125rem | xl 1.25rem | 2xl 2rem | 3xl 2.75rem
### 📐 Spacing
- Grid: asymmetric 2-column (60/40) on desktop, 8px base unit
- Section padding: 5rem vertical, 3rem horizontal on desktop
- Card gaps: 2rem with alternating widths per row for visual rhythm
### 🧩 Components
- Buttons: solid dark fill, 0px radius, subtle 1px lighter border, monospace-styled text, letter-spacing 0.05em
- Cards: no background fill — use 1px hairline border in mid-tone, generous padding, text-only content
- Nav: minimal — logo left, 3 text links right, thin 1px bottom rule spanning full width
- Hero: oversized serif headline occupying 70% of viewport height, single supporting line below, no imagery
- Footer: compact single line, small muted text, top hairline rule
### ♿ Accessibility
- Contrast minimum 7:1 (WCAG AAA) — achievable since all pairs are light/dark grayscale
- Focus states: 2px offset ring in darkest tone, inverted on dark backgrounds
- Respect `prefers-reduced-motion` — remove letter-spacing transitions
- Minimum body font size 16px (1rem)
### ✍️ Writing Tone
- Elegant, measured, literary. Evocative without being verbose. Trust the reader's intelligence.
- Labels in sentence case. No marketing adjectives. Periods at end of CTAs.
## Do / Don't
### ✅ Do
- Explore the full tonal range — use at least 6 distinct steps on the gray scale
- Use typographic contrast (serif headings vs sans body) as the primary visual interest
- Add texture through subtle grain overlays, paper-like backgrounds, or noise
- Vary font weights dramatically — light (300) headings against regular (400) body
- Use asymmetric layouts to create rhythm without color
### ❌ Don't
- Introduce any color beyond the single-hue grayscale palette
- Use gradients — flat tones only
- Apply drop shadows — use hairline borders or nothing for separation
- Center-align text — asymmetric alignment creates visual interest
- Use icons or decorative graphics — typography and space carry the design
## Quality Gates
- [ ] Exactly one hue family across all elements — no secondary/accent colors
- [ ] At least 6 distinct tonal values present (checked via contrast audit)
- [ ] No box-shadows used anywhere — borders and spacing only
- [ ] Serif/sans-serif pairing creates clear typographic hierarchy
- [ ] Textures (noise, grain, or paper) appear on at least 2 surfaces
- [ ] All text passes WCAG AAA contrast (7:1 minimum)