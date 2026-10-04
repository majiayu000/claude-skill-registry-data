---
name: agentic
description: Dark AI/tech aesthetic with neon accents for futuristic agent-driven interfaces.
---
# Agentic
## Mission
Convey cutting-edge AI capability through dark, high-tech interfaces with purposeful neon highlights.
## Brand
### 🎨 Colors
- `#0a0a0f` — Background (deep void black)
- `#00ff88` — Primary neon green
- `#7b61ff` — Secondary purple accent
- `#ff3366` — Accent / error pink
- `#e0e0e0` — Text primary
- `#666680` — Text muted
### 🔤 Typography
- Headings: Space Grotesk (Google Fonts)
- Body: JetBrains Mono (Google Fonts)
- Scale: xs 0.75rem, sm 0.875rem, base 1rem, lg 1.25rem, xl 1.5rem, 2xl 2rem, 3xl 3rem
### 📐 Spacing
- Grid: 8px base unit, 24px column gutters
- Section padding: 4rem vertical, 2rem horizontal
- Card gaps: 1rem
### 🧩 Components
- Buttons: Rounded (8px), neon border 1px solid primary on hover, dark fill, all-caps labels
- Cards: `#12121a` background, 1px `#1e1e2e` border, 12px radius, subtle inner glow
- Nav: Fixed top, frosted dark glass (`backdrop-filter: blur(12px)`), 1px bottom border
- Hero: Full-viewport dark gradient with animated particle or grid background, large neon headline
- Footer: Minimal, `#0d0d14` background, small muted text, neon accent links on hover
### ♿ Accessibility
- Minimum contrast ratio 4.5:1 for body text against `#0a0a0f`
- Focus states: 2px neon green outline with 4px offset
- Reduced motion: Disable background animations, use instant transitions
- Minimum font size 0.75rem (12px)
### ✍️ Writing Tone
- Voice: Confident, precise, technical but not cold
- Labels: Sentence case, action-oriented (e.g. "Deploy agent" not "Click here")
- No marketing fluff; prefer direct statements
## Do / Don't
### ✅ Do
- Use neon accents sparingly — only on interactive elements and key data
- Maintain deep contrast between background and content layers
- Use monospace for code, logs, and data displays
- Animate with purpose: transitions under 200ms, subtle scale on hover
- Keep layouts asymmetric and forward-leaning
### ❌ Don't
- Overuse neon — it loses impact when everything glows
- Use pure white (`#ffffff`) — always tint slightly toward the palette
- Add drop shadows — use inner glows and borders instead
- Use serif fonts — they break the tech aesthetic
- Add decorative elements that don't serve function
## Quality Gates
- [ ] All interactive elements have visible focus indicators
- [ ] Neon colors pass 3:1 contrast against background (AA for UI components)
- [ ] Animations respect `prefers-reduced-motion`
- [ ] Monospace elements use tabular-nums for data alignment
- [ ] No pure white or pure black outside the defined palette
- [ ] Dark theme tested on OLED and standard LCD displays