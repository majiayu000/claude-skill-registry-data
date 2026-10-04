---
name: memphis
description: 80s Memphis design movement — geometric shapes, loud colors, squiggles, and playful rebellion.
---
# Memphis
## Mission
Inject chaotic joy through clashing geometric patterns, irreverent shapes, and an unapologetically loud palette that rejects minimalist restraint.
## Brand
### 🎨 Colors
- `#FF6B6B` — Primary (hot coral)
- `#4ECDC4` — Secondary (teal)
- `#FFE66D` — Accent (sun yellow)
- `#2C2C54` — Background (deep navy)
- `#F7F7F7` — Text on dark (off-white)
- `#1A1A2E` — Text on light (near-black)
### 🔤 Typography
- Heading: **Righteous** (Google Fonts) — bold, playful display
- Body: **Nunito** (Google Fonts) — rounded, friendly sans-serif
- Scale: xs 0.75rem | sm 0.875rem | base 1rem | lg 1.25rem | xl 1.5rem | 2xl 2rem | 3xl 3rem
### 📐 Spacing
- Grid: 8px base, no strict columns — elements float and overlap intentionally
- Section padding: 4rem vertical, 2rem horizontal
- Card gaps: 1.5rem with overlapping allowed
### 🧩 Components
- Buttons: filled squiggly-bordered rectangles, 0px radius, thick 3px outlines, all-caps text
- Cards: rotated 2-5° off-axis, bold drop shadows offset 6px/6px in contrasting color
- Nav: horizontal rule of repeating geometric shapes (circles, triangles, squiggles) as separators
- Hero: large geometric background pattern (confetti dots, zigzag lines), oversized headline at slight angle
- Footer: thick top border in accent color, pattern of alternating shapes
### ♿ Accessibility
- Minimum contrast ratio 4.5:1 for body text against background
- Focus states: 3px dashed outline in accent color with 2px offset
- Respect `prefers-reduced-motion` — disable rotations and floating animations
- Minimum body font size 16px (1rem)
### ✍️ Writing Tone
- Playful, exclamatory, irreverent. Short punchy phrases. Embrace the absurd.
- Labels use sentence case. CTAs can be ALL CAPS. Emoji-friendly.
## Do / Don't
### ✅ Do
- Use bold geometric shapes (circles, triangles, squiggles, zigzags) as decorative elements
- Rotate elements slightly off-grid for intentional chaos
- Layer patterns over patterns — dots over stripes, grids over squiggles
- Pair clashing colors deliberately — teal with coral, yellow with purple
- Use thick outlines (2-4px) on shapes and buttons
### ❌ Don't
- Use rounded corners — everything should be sharp or irregular
- Stick to a rigid grid — Memphis thrives on controlled disorder
- Use muted or pastel palettes — go loud or go home
- Apply drop shadows with blur — use hard offset shadows in contrasting colors
- Mix in serif typefaces — keep everything playful sans-serif or display
## Quality Gates
- [ ] At least 4 distinct geometric decorative shapes appear on every page
- [ ] Color palette uses at least 3 clashing hues
- [ ] No border-radius values exceed 2px anywhere
- [ ] At least one element is intentionally rotated off-axis
- [ ] Thick outlines (≥2px) are used on interactive elements
- [ ] `prefers-reduced-motion` disables all rotation/float animations