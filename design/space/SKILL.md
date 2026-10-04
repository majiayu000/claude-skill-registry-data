---
name: space
description: Deep space exploration — starfields, nebula gradients, cosmic vastness, and the beauty of the void.
---
# Space
## Mission
Capture the awe of looking into deep space. Starfield backgrounds, nebula-like gradients, vast negative space, and a sense of scale that makes users feel like explorers of the cosmos.
## Brand
### 🎨 Colors
- `#0B0D17` — Void black (background)
- `#1A1040` — Deep nebula purple
- `#0D2B5E` — Cosmic blue
- `#E8D5FF` — Starlight (text)
- `#FF6B9D` — Nebula pink (accent)
- `#4DE8FF` — Bright star cyan (highlights)
### 🔤 Typography
- Heading font: Space Grotesk (Google Fonts)
- Body font: Space Grotesk (Google Fonts)
- Type scale: `0.75rem` / `0.875rem` / `1rem` / `1.125rem` / `1.25rem` / `1.5rem` / `2.25rem`
### 📐 Spacing
- Grid system: CSS Grid, `2rem` gutter — content floats in negative space
- Section padding: `8rem` vertical (vast emptiness is the point), `2rem` horizontal
- Card gaps: `2rem`
### 🧩 Components
- Buttons: Subtle gradient (purple to blue), pill-shaped, `0.25rem` border-radius, glow on hover
- Cards: Semi-transparent dark panels with `1px` subtle border, `backdrop-filter: blur(8px)`, starlight text
- Nav: Minimal — floating logo + links, transparent background, `backdrop-filter`, no bottom border
- Hero: Massive heading floating in negative space, CSS animated starfield background, slow parallax nebula blobs
- Footer: "Lost in space" minimalism — just a logo and "🌌" centered in void
### ♿ Accessibility
- Contrast: starlight `#E8D5FF` on void = 11:1 (AAA); cyan highlights tested at 4.5:1 on void
- Focus states: `2px` cyan glow ring with `3px` offset
- Reduced motion: starfield becomes static; parallax and glow animations disabled
- Font size minimums: `0.875rem` body, `1rem` preferred for readability on dark
### ✍️ Writing Tone
- Poetic, awe-inspired, expansive — match the scale of the cosmos
- Use cosmic metaphors sparingly but effectively
- Labels: "Begin Journey," "Explore," "Launch," "Discover," "Transmit"
## Do / Don't
### ✅ Do
- Generate CSS-only starfields with `box-shadow` arrays or `radial-gradient` dots
- Use large `radial-gradient` blobs in nebula colors as section backgrounds
- Add slow, subtle parallax to background elements (stars move slower than nebulas)
- Maintain vast vertical spacing — `8rem`+ between sections
- Use `mix-blend-mode: screen` or `overlay` for glowing elements
### ❌ Don't
- Crowd content — space is mostly void; let your layout breathe
- Use fast animations — everything in space moves slowly and deliberately
- Add harsh white borders or dividers — use subtle color transitions
- Use earthy or warm-dominant palettes — space is cool-toned
- Overload the starfield — too many stars looks like noise, not cosmos
## Quality Gates
- [ ] Starfield renders without visible repeating patterns (use prime number coordinates)
- [ ] Nebula gradients don't band — add subtle noise overlay if needed
- [ ] All text passes 4.5:1 contrast on the darkest background behind it
- [ ] Parallax and animations respect `prefers-reduced-motion`
- [ ] Starfield doesn't cause GPU overdraw — test on low-power devices
- [ ] Content is readable at all breakpoints with the vast vertical spacing