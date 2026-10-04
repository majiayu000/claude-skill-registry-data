---
name: neon
description: Glow effects, dark backgrounds, electric colors, and nightlife energy with cyberpunk edge.
---
# Neon
## Mission
Electrify the screen — dark canvases lit by glowing type and borders, channeling nightlife, cyberpunk, and synthwave energy.
## Brand
### 🎨 Colors
- `#FF00FF` — Primary (magenta neon)
- `#00FFFF` — Secondary (cyan neon)
- `#39FF14` — Accent (electric green)
- `#0A0A0A` — Background (near-black)
- `#FFFFFF` — Text (white, for readability)
- `#FF6EC7` — Muted text (soft pink glow)
### 🔤 Typography
- Heading: **Monoton** (Google Fonts) — neon-sign display, or **Audiowide** for cyberpunk
- Body: **Rajdhani** (Google Fonts) — narrow, tech-forward sans-serif
- Scale: xs 0.75rem | sm 0.875rem | base 1rem | lg 1.125rem | xl 1.5rem | 2xl 2.5rem | 3xl 4rem
### 📐 Spacing
- Grid: center-aligned single column, max-width 900px
- Section padding: 6rem vertical, 2rem horizontal
- Card gaps: 3rem — generous spacing lets glow effects spread without collision
### 🧩 Components
- Buttons: transparent background, 2px glowing border (box-shadow + text-shadow), 4px radius, hover intensifies glow and fills background at 15% opacity
- Cards: dark semi-transparent background (rgba 0,0,0,0.4), 1px glowing border, subtle inner glow, backdrop-filter blur
- Nav: fixed top, transparent background with text-only links that glow on hover, thin bottom border with gradient glow
- Hero: dark background with radial glow spotlight, massive glowing headline, animated scanlines overlay optional
- Footer: minimal, small muted text with subtle top border glow, social links as glowing icons
### ♿ Accessibility
- Body text must be white (#FFFFFF) on dark background — contrast 15:1 minimum
- Glow effects must not be the sole indicator of interactive state — pair with underline or fill
- Focus states: 2px solid white ring with glow — unambiguous and bright
- Respect `prefers-reduced-motion` — disable pulsing, flickering, and scanline animations
- Minimum body font size 16px (1rem)
### ✍️ Writing Tone
- Energetic, futuristic, punchy. Rhythm-driven. Use line breaks like a DJ drops a beat.
- Labels in lowercase or ALL CAPS. CTAs are verbs. Ellipses are allowed... sparingly.
## Do / Don't
### ✅ Do
- Use CSS text-shadow for glowing typography — stack multiple shadows (0 0 10px, 0 0 40px, 0 0 80px)
- Apply box-shadow glow rings to borders and interactive elements
- Keep backgrounds near-black (#0A0A0A to #111111) — true black kills the glow effect
- Pair neon colors against dark — magenta on black, cyan on black, green on black
- Add subtle grain or scanline overlays for cyberpunk texture
### ❌ Don't
- Use white or light backgrounds — neon doesn't glow on light surfaces
- Apply heavy borders — 1-2px max, the glow carries the weight
- Mix more than 3 neon colors on one page
- Use serif typefaces — everything must feel digital and forward
- Overuse glow such that text becomes illegible — body text stays white, glow is for accents
## Quality Gates
- [ ] Background is near-black (#0A0A0A to #111111) across all surfaces
- [ ] At least 3 elements use stacked text-shadow for glow effect
- [ ] All interactive elements have glow-based hover states
- [ ] Body text is white (#FFFFFF) for maximum readability
- [ ] No light backgrounds anywhere — dark mode only
- [ ] `prefers-reduced-motion` disables all pulsing/flickering animations