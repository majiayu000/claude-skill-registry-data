---
name: soft
description: Gentle rounded corners, pastel gradients, pill-shaped everything — cushioned, calming, and kind.
---
# Soft
## Mission
Create interfaces that feel like a deep breath. Generous border-radius, pastel color palettes, pill-shaped components, and cushioned spacing that makes every interaction feel gentle and forgiving.
## Brand
### 🎨 Colors
- `#A8D8EA` — Soft sky blue (primary)
- `#FFD3E0` — Blush pink (secondary)
- `#FFF9F0` — Cream (background)
- `#FFFFFF` — Card surface
- `#C9E4C5` — Sage green (accent/success)
- `#5A5A6E` — Soft charcoal (text)
### 🔤 Typography
- Heading font: Nunito (Google Fonts)
- Body font: Nunito Sans (Google Fonts)
- Type scale: `0.75rem` / `0.875rem` / `1rem` / `1.125rem` / `1.25rem` / `1.5rem` / `2rem`
### 📐 Spacing
- Grid system: CSS Grid with `2rem` gutter — generous, uncrowded
- Section padding: `5rem` vertical, `2rem` horizontal
- Card gaps: `2rem` — let elements breathe
### 🧩 Components
- Buttons: Fully pill-shaped (`border-radius: 9999px`), pastel fill with matching darker text, gentle `scale(1.03)` on hover
- Cards: Large rounded corners (`1rem`), soft shadow (`0 4px 20px rgba(0,0,0,0.04)`), white on cream background
- Nav: Rounded pill container with `backdrop-filter: blur(16px)`, centered logo + links, sticky
- Hero: Centered heading with pastel gradient blob decorations behind text, soft floating animation
- Footer: Rounded top corners on footer container, pastel background, pill-shaped social icon buttons
### ♿ Accessibility
- Contrast: soft charcoal `#5A5A6E` on cream = 5.8:1 (AA); test pastel-on-pastel combinations carefully
- Focus states: `3px` soft charcoal ring with `3px` offset, rounded to match pill aesthetic
- Reduced motion: disable blob animations and hover scales
- Font size minimums: `0.875rem` for body — round fonts need slightly more space
### ✍️ Writing Tone
- Warm, encouraging, inclusive — use "we" and "you" naturally
- Gentle CTAs, never aggressive: "Try it out," "See how it works," "Take your time"
- Labels: "Continue," "Explore," "Learn more," "We're here to help"
## Do / Don't
### ✅ Do
- Use `border-radius: 9999px` for all buttons, inputs, and chips
- Pair pastel fills with darker text from the same hue family for readability
- Add pastel gradient blobs (`radial-gradient` with `blur`) as background decorations
- Use `box-shadow` values that feel like soft light, not hard drop shadows
- Maintain generous padding — `1rem` minimum inside any container
### ❌ Don't
- Use sharp corners (`border-radius: 0`) anywhere — even `2px` borders get `0.25rem` radius
- Choose saturated or neon colors — pastels only, keep saturation under 40%
- Overlap elements tightly — soft design needs breathing room
- Use heavy font weights — stay at 400/600, never exceed 700
- Add harsh borders — use `0px` or `1px` at most, in a slightly darker pastel
## Quality Gates
- [ ] All interactive elements have `border-radius ≥ 0.5rem`
- [ ] All text passes 4.5:1 contrast against its background
- [ ] No hard black (`#000`) or pure white (`#FFF`) anywhere — always tint toward pastel
- [ ] Pastel gradients render without banding (test on 8-bit displays)
- [ ] Focus rings are visible and match the rounded aesthetic
- [ ] Background blob decorations don't overflow or cause horizontal scroll