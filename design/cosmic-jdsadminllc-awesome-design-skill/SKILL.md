---
name: cosmic
description: Deep space aesthetic with purple nebula gradients and mysterious atmosphere
---
# Cosmic
## Mission
Transport users into deep space through rich purple-indigo gradients, starfield textures, and a sense of infinite mystery.
## Brand
### 🎨 Colors
- `#0B0B1A` — Deep space background (near-black indigo)
- `#1A1A3E` — Secondary background (dark nebula)
- `#8B5CF6` — Primary accent (vivid purple)
- `#6366F1` — Secondary accent (indigo)
- `#A78BFA` — Soft accent (lavender glow)
- `#E0E7FF` — Text (ethereal white)
### 🔤 Typography
- Heading font: Space Grotesk (Google Fonts)
- Body font: Inter (Google Fonts)
- Type scale: xs 0.75rem / sm 0.875rem / base 1rem / lg 1.125rem / xl 1.75rem / 2xl 2.5rem / 3xl 3.5rem
### 📐 Spacing
- Grid: 12-column, 1.5rem gap, centered container
- Section padding: 6rem top/bottom
- Card gap: 2rem
### 🧩 Components
- Buttons: Ghost-style with 1px purple border and glow effect (box-shadow in accent color), rounded 12px, hover fills with gradient
- Cards: Translucent dark backgrounds (`rgba(26, 26, 62, 0.8)`) with backdrop-blur, 1px `#8B5CF6` border at 20% opacity, 16px radius
- Nav: Minimal, transparent with backdrop-blur, white text links, subtle star-dot separators
- Hero: Massive heading with text-glow, animated starfield or particle background, slow parallax nebula layers
- Footer: Dark fade-to-black, subtle constellation-line graphic, minimal links
### ♿ Accessibility
- All text passes 4.5:1 contrast (light text on dark = verify `#E0E7FF` on `#0B0B1A`)
- Focus rings: 2px `#8B5CF6` glow with 2px offset
- Reduced motion: disable parallax, particle effects, and glow animations; keep static starfield
- Minimum font size 0.75rem
### ✍️ Writing Tone
- Evocative and atmospheric — use cosmic metaphors sparingly but effectively
- Short, weighty statements; let whitespace carry meaning
- Labels use lowercase or sentence case; avoid shouting
## Do / Don't
### ✅ Do
- Layer depth through parallax, translucent cards, and soft glow effects
- Use CSS animations for slow, ambient motion (stars twinkling, nebula drifting)
- Keep text minimal — let the atmosphere do the heavy lifting
- Apply text-shadow glow to key headings for ethereal effect
- Use star/constellation/dot patterns as subtle decorative elements
### ❌ Don't
- Use bright, saturated colors outside the purple-indigo spectrum
- Add fast or jarring animations — everything must feel slow and cosmic
- Overcrowd with content — cosmic design needs empty space
- Use harsh white (`#FFFFFF`) — always warm it to `#E0E7FF`
- Include cartoonish space elements (clip-art rockets, planets) — keep abstract
## Quality Gates
- All text passes 4.5:1 contrast against dark backgrounds
- Focus states visible against dark backgrounds
- Page respects prefers-reduced-motion (disable parallax, particles, glows)
- No font smaller than 0.75rem
- Animations run at 60fps (no janky particle effects)
- At least one atmospheric element present (starfield, nebula gradient, or parallax)