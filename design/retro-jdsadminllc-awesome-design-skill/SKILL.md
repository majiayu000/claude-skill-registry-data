---
name: retro
description: 80s/90s throwback with arcade fonts, CRT scanlines, neon grids, and pixel-perfect nostalgia.
---
# Retro
## Mission
Transport users to the golden age of computing — arcade cabinets, CRT monitors, and neon-drenched synthwave aesthetics. Every pixel should feel like it has a memory.
## Brand
### 🎨 Colors
- `#FF00FF` — Neon magenta (primary)
- `#00FFFF` — Cyan (secondary)
- `#0D0221` — Deep CRT black (background)
- `#39FF14` — Neon green (accent)
- `#FFD700` — Amber/gold (highlights)
- `#FFFFFF` — Text (when not on dark)
### 🔤 Typography
- Heading font: Press Start 2P (Google Fonts)
- Body font: VT323 (Google Fonts)
- Type scale: `0.625rem` / `0.75rem` / `1rem` / `1.25rem` / `1.5rem` / `2rem` / `3rem`
### 📐 Spacing
- Grid system: 8px baseline grid (pixel-snapped)
- Section padding: `4rem` vertical, `2rem` horizontal
- Card gaps: `1rem` with `2px` solid neon borders
### 🧩 Components
- Buttons: 3D beveled edges (`box-shadow` inset/outset), neon border glow on hover, `Press Start 2P` at `0.75rem`
- Cards: Dark backgrounds with `2px` neon borders, slight `box-shadow` glow in accent color
- Nav: Horizontal pixel-art divider, monospace links with `::after` blinking cursor on hover
- Hero: Large pixel-art heading over a CSS grid background or scanline overlay, marquee-style subtitle
- Footer: Simple monospace credit line, CRT curvature vignette at page edges
### ♿ Accessibility
- Contrast: neon-on-black meets WCAG AAA for large text, AA for body — test all color pairs
- Focus states: thick `3px` neon outline, never remove `:focus-visible`
- Reduced motion: disable scanline animations and blinking cursors
- Font size minimums: never go below `0.75rem` for interactive text
### ✍️ Writing Tone
- Arcade-announcer energy: brief, punchy, excitable
- Use ALL CAPS for headings and CTAs sparingly
- Labels: "INSERT COIN" for sign-up, "PLAY" for submit, "HIGH SCORES" for testimonials
## Do / Don't
### ✅ Do
- Use a CSS scanline overlay (`repeating-linear-gradient`) over the entire viewport
- Add CRT curvature with a subtle `border-radius` and radial-gradient vignette on a fixed overlay
- Animate neon glows with `@keyframes` on the `box-shadow` property
- Use `image-rendering: pixelated` on any raster images
- Layer multiple `text-shadow` values for authentic neon glow effects
### ❌ Don't
- Mix smooth border-radius with pixel-art elements — stay sharp or stay curved, not both
- Use modern sans-serif fonts like Inter or system-ui anywhere
- Over-animate — the 80s were static; neon flicker should be subtle
- Forget to add a dark overlay behind text on neon backgrounds
- Use gradients that weren't possible on 8-bit hardware (stick to hard stops)
## Quality Gates
- [ ] Scanline overlay renders at all viewport sizes without moiré artifacts
- [ ] Neon glow animations respect `prefers-reduced-motion: reduce`
- [ ] All text passes 4.5:1 contrast ratio against its immediate background
- [ ] Pixel font loads with `font-display: swap` and a system monospace fallback
- [ ] No layout shift when web fonts load (match fallback size to Press Start 2P)
- [ ] Page renders legibly without the scanline overlay (test by removing it)