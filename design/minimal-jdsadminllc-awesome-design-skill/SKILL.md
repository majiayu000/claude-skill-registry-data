---
name: minimal
description: Extreme reduction — essential-only content, white space dominance, and typographic purity.
---
# Minimal
## Mission
Strip every element to its barest essential, letting content breathe in generous white space with nothing superfluous.
## Brand
### 🎨 Colors
- `#FFFFFF` — Primary (pure white)
- `#F5F5F5` — Secondary (warm gray tint)
- `#000000` — Accent (pure black, used sparingly)
- `#FFFFFF` — Background (white)
- `#1A1A1A` — Text (near-black, never pure black)
- `#757575` — Muted text (medium gray)
### 🔤 Typography
- Heading: **DM Serif Display** (Google Fonts) — elegant, refined serif
- Body: **DM Sans** (Google Fonts) — clean geometric sans-serif
- Scale: xs 0.75rem | sm 0.875rem | base 1rem | lg 1.125rem | xl 1.25rem | 2xl 1.75rem | 3xl 2.5rem
### 📐 Spacing
- Grid: single-column layout, no multi-column except for image-text pairs
- Section padding: 6rem vertical, generous horizontal margins (min 4rem on desktop)
- Card gaps: not applicable — minimalism avoids cards; use simple text blocks
### 🧩 Components
- Buttons: text-only with thin 1px underline on hover, no background, no border, no radius — the word is the button
- Cards: avoid entirely. Use rule-separated text blocks with generous padding instead.
- Nav: minimal top bar — logo left, 3-4 text links right, no background, no border
- Hero: large headline + single-sentence subhead + optional text-link CTA, centered in vast white space
- Footer: single line of small gray text, no columns, no icons
### ♿ Accessibility
- Contrast minimum 7:1 for body text (exceeds WCAG AAA)
- Focus states: subtle 1px underline with 4px offset from text
- Respect `prefers-reduced-motion` — no animations to reduce
- Minimum body font size 18px (1.125rem) — larger than standard for readability
### ✍️ Writing Tone
- Precise, restrained, essential. Every word earns its place. No marketing speak.
- Labels are lowercase. CTAs are verbs only ("read", "write", "see"). No exclamation marks.
## Do / Don't
### ✅ Do
- Remove everything before adding anything — start from zero
- Use generous white space as the primary design element
- Limit type scale to 4 sizes maximum across the entire site
- Prefer rules (horizontal lines) and spacing over boxes and cards
- Use grayscale exclusively — color only when it carries meaning (links, errors)
### ❌ Don't
- Use cards, shadows, borders, or background colors — let content float in space
- Add icons where words suffice
- Use more than one column of text
- Apply hover effects beyond subtle underlines
- Include hero images — the typography is the hero
## Quality Gates
- [ ] No box-shadow, border-radius, or background-color on any content container
- [ ] Maximum 4 distinct type sizes used across entire page
- [ ] Color palette restricted to grayscale + 1 accent color for interactive elements only
- [ ] Every section has at least 4rem of surrounding white space
- [ ] No element uses more than 1 CSS property for its hover state
- [ ] Page weight under 50KB total (HTML + CSS)