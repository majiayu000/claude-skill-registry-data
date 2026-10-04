---
name: pixel
description: 8-bit retro gaming aesthetic with blocky pixel-art borders, chunky UI, and arcade nostalgia.
---
# Pixel
## Mission
Channel the golden age of arcade cabinets and 8-bit consoles — where every pixel is intentional, UI is chunky, and nostalgia hits hard.
## Brand
### 🎨 Colors
- `#1A1A2E` — Background (dark arcade)
- `#E94560` — Primary (neon red)
- `#0F3460` — Secondary (deep blue)
- `#16C79A` — Accent (retro green)
- `#FFD700` — Highlight (coin gold)
- `#EAEAEA` — Text (white-ish)
### 🔤 Typography
- Headings: **Press Start 2P** (pixel, display only)
- Body: **Fira Code** (monospace, readable)
- Scale: xs 0.75rem / sm 0.875rem / base 1rem / lg 1.125rem / xl 1.25rem / 2xl 1.5rem / 3xl 2rem
### 📐 Spacing
- 8px grid (single pixel block unit)
- Section padding: 4rem vertical, 1.5rem horizontal
- Card gaps: 1rem
- Max content width: 60rem
### 🧩 Components
- **Buttons**: Chunky, 0px radius, 4px solid border, 4px drop shadow (no blur, solid offset), press effect moves element down 4px
- **Cards**: Solid border (4px), 0px radius, dark bg, neon accent border on hover, pixel-perfect corners
- **Nav**: Chunky horizontal bar, monospace links, active state uses inverted colors
- **Hero**: Dark background with pixel-art decorative border (CSS border-image or SVG), large pixel heading, single CTA
- **Footer**: 4px top border, pixel-art divider line, compact monospace links
### ♿ Accessibility
- Contrast ratio ≥ 4.5:1 on all text — neon on dark passes easily
- Focus ring: 4px solid #FFD700, 0px radius, 4px offset from element
- Reduced motion: disable screen shake and button press animations
- Minimum font size: 0.875rem — Press Start 2P reserved for headings ≥ 1.5rem only
- Monospace body text aids dyslexic readers with consistent letter spacing
### ✍ Writing Tone
Punchy, energetic, arcade-style. ALL CAPS for buttons and labels. Short commands. "INSERT COIN" energy. Use > arrows and█ blocks for flair.
## Do / Don't
### ✅ Do
- Use CSS `box-shadow` with 0 blur and positive offsets for chunky depth
- Apply `image-rendering: pixelated` to all images and icons
- Use `border-image` with pixel-art patterns for decorative section borders
- Keep borders either 2px or 4px — never odd pixel widths
- Animate with `steps()` timing function for frame-by-frame feel
### ❌ Don't
- Use border-radius on any element — pixels have corners
- Anti-alias text — use `-webkit-font-smoothing: none` for pixel fonts
- Use gradients — flat colors only
- Mix pixel and modern smooth aesthetics in the same view
- Exceed 4px for any border or shadow — keep the grid tight
## Quality Gates
- [ ] No border-radius anywhere in the stylesheet
- [ ] All images and icons use `image-rendering: pixelated`
- [ ] Press Start 2P font loads and renders properly on headings
- [ ] Button press animations use `steps()` timing function
- [ ] No CSS gradients in any declaration
- [ ] Layout works at 320px with monospace body text and pixel headings