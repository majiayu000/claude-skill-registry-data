---
name: roku
description: Roku-style streaming media aesthetic — deep purple gradients, dark mode, bold cards, binge-ready.
---
# Roku
## Mission
Capture the immersive, lean-back experience of a streaming media platform. Deep purples, cinematic gradients, and bold poster-card layouts that make content feel premium and binge-worthy.
## Brand
### 🎨 Colors
- `#6B2FA0` — Deep purple (primary)
- `#8B45C7` — Vibrant purple (secondary)
- `#0A0A0F` — Near-black background
- `#1A1A2E` — Card surface
- `#E0B0FF` — Soft lavender (accent)
- `#FFFFFF` — Text
### 🔤 Typography
- Heading font: Poppins (Google Fonts)
- Body font: Inter (Google Fonts)
- Type scale: `0.75rem` / `0.875rem` / `1rem` / `1.25rem` / `1.5rem` / `2rem` / `3rem`
### 📐 Spacing
- Grid system: CSS Grid with `repeat(auto-fill, minmax(280px, 1fr))` for poster cards
- Section padding: `5rem` vertical, `2rem` horizontal
- Card gaps: `1.5rem`
### 🧩 Components
- Buttons: Pill-shaped, purple-to-magenta gradient, `0.25rem` border-radius, white text, `scale(1.05)` on hover
- Cards: `16:9` poster ratio, rounded corners (`0.5rem`), gradient overlay on hover revealing title + play button
- Nav: Sticky top bar with `backdrop-filter: blur(12px)`, semi-transparent dark background, logo left, nav links right
- Hero: Full-viewport featured content carousel, large title overlaid on gradient fade from bottom
- Footer: Dark with subtle purple top-border glow, 3-column link grid
### ♿ Accessibility
- Contrast: white on purple/black passes AAA; all overlays tested at 4.5:1 minimum
- Focus states: `3px` lavender outline with `2px` offset
- Reduced motion: carousel auto-advance pauses; hover scales removed
- Font size minimums: `0.875rem` for all body text
### ✍️ Writing Tone
- Cinematic and evocative — pitch content like a trailer
- Short, punchy titles; descriptive but concise synopses
- Labels: "Watch Now," "Continue Watching," "Add to List," "More Like This"
## Do / Don't
### ✅ Do
- Use deep purple-to-black radial gradients as section backgrounds
- Design all cards at a consistent 16:9 or 2:3 poster aspect ratio
- Add a subtle purple glow (`box-shadow`) behind featured content
- Use `backdrop-filter: blur()` for nav and overlay panels
- Lazy-load card images with a purple skeleton shimmer placeholder
### ❌ Don't
- Use pure black (`#000`) — always tint toward purple (`#0A0A0F`)
- Let cards stretch beyond their aspect ratio on any breakpoint
- Overwhelm with animations — one primary motion per viewport
- Use serif fonts anywhere — streaming is modern and sans-serif
- Forget hover states on cards — every card must feel interactive
## Quality Gates
- [ ] All cards maintain their aspect ratio from 320px to 4K viewports
- [ ] Gradient overlays render without banding (use `dither` or slight noise)
- [ ] Nav blur backdrop works in Safari (`-webkit-backdrop-filter`)
- [ ] Skeleton shimmer animation respects `prefers-reduced-motion`
- [ ] All interactive elements have visible focus indicators
- [ ] Page works with keyboard navigation (tab through cards, enter to select)