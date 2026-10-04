---
name: cafe
description: Warm, cozy coffee-shop aesthetic with earth tones and inviting textures.
---
# Cafe
## Mission
Wrap users in the comfort of a neighborhood coffee shop — warm lighting, rich earth tones, and the kind of design that makes you want to stay awhile.
## Brand
### 🎨 Colors
- `#fefae0` — Cream background
- `#d4a373` — Warm tan / latte
- `#8b5e3c` — Rich brown
- `#4a3525` — Dark roast
- `#ccd5ae` — Sage green
- `#e9edc9` — Light sage
### 🔤 Typography
- Headings: Lora (Google Fonts)
- Body: Nunito (Google Fonts)
- Scale: xs 0.75rem, sm 0.875rem, base 1rem, lg 1.125rem, xl 1.5rem, 2xl 2rem, 3xl 2.75rem
### 📐 Spacing
- Grid: 12-column, generous 32px gutters
- Section padding: 5rem vertical, 2rem horizontal
- Card gaps: 1.5rem
### 🧩 Components
- Buttons: 12px border-radius, warm brown fill, white/cream text, subtle 2px bottom shadow for depth, hover lightens 10%
- Cards: 16px radius, cream or white fill, 1px `#d4a373` border, 24px internal padding, optional subtle `box-shadow`
- Nav: Sticky top, cream background, logo left, centered or right-aligned links, text brown
- Hero: Warm-toned background image or solid cream, centered Lora headline, inviting subtext, 1-2 CTAs
- Footer: Dark roast `#4a3525` background, cream text, 3-column link grid, coffee-shop-style "open hours" block
### ♿ Accessibility
- Minimum contrast ratio 4.5:1 for body text against cream backgrounds
- Focus states: 2px warm brown outline with 2px offset
- Reduced motion: Instant transitions, disable hover lifts
- Minimum font size 0.875rem for body text
### ✍️ Writing Tone
- Voice: Warm, inviting, conversational — like a barista who remembers your order
- Labels: Friendly but clear, sentence case
- Use "we" and "you" — make it personal
## Do / Don't
### ✅ Do
- Use warm, low-saturation photography — natural light, wood textures, ceramic surfaces
- Layer cream-on-brown and brown-on-cream for depth without harsh contrast
- Add subtle texture: paper grain, wood grain, soft noise overlays at 3-5% opacity
- Group content into cozy, contained cards with soft borders
- Use curved, organic shapes — avoid sharp corners
### ❌ Don't
- Use pure white (`#ffffff`) — always warm it with cream
- Add neon or highly saturated colors — they shatter the cozy mood
- Use cold grays or steel blues — no corporate coolness
- Over-animate — a gentle fade is enough, nothing bouncy
- Use thin, spindly fonts — keep everything soft and rounded
## Quality Gates
- [ ] No pure white exists in the palette — all light surfaces are cream-tinted
- [ ] Body text passes 4.5:1 contrast against `#fefae0`
- [ ] All interactive elements have warm-tone focus indicators
- [ ] No sharp border-radius below 8px on any component
- [ ] Motion respects prefers-reduced-motion
- [ ] Photography uses warm color grading (no cool/blue-toned images)