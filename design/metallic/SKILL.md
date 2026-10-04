---
name: metallic
description: Chrome/silver gradients, reflective surfaces, and premium tech aesthetic with liquid-metal depth.
---
# Metallic
## Mission
Convey premium, high-tech sophistication through reflective surfaces, chrome gradients, and the illusion of polished metal.
## Brand
### 🎨 Colors
- `#E8E8E8` — Primary (bright silver)
- `#B8B8B8` — Secondary (mid-tone metal)
- `#6B6B6B` — Accent (dark steel)
- `#1A1A1A` — Background (onyx black)
- `#F5F5F5` — Text on dark (near-white)
- `#0D0D0D` — Text on light (deep charcoal)
### 🔤 Typography
- Heading: **Orbitron** (Google Fonts) — futuristic geometric sans
- Body: **Inter** (Google Fonts) — clean, precise sans-serif
- Scale: xs 0.75rem | sm 0.875rem | base 1rem | lg 1.125rem | xl 1.5rem | 2xl 2.25rem | 3xl 3rem
### 📐 Spacing
- Grid: 12-column, 24px gutter, precise alignment
- Section padding: 5rem vertical, 2rem horizontal
- Card gaps: 2rem in a rigid grid
### 🧩 Components
- Buttons: linear-gradient chrome finish (light → mid → light), 4px radius, subtle inner highlight, dark text on light gradient
- Cards: dark backgrounds with 1px semi-transparent white border, subtle reflection streak (gradient overlay at 15% opacity)
- Nav: frosted-glass effect (backdrop-filter blur), thin 1px bottom border silver gradient
- Hero: dark background with radial gradient spotlight, headline with linear-gradient text (chrome effect), subtle particle/sparkle accents
- Footer: solid dark steel, subtle top gradient border
### ♿ Accessibility
- Contrast ratio 4.5:1 minimum — verify gradient backgrounds produce sufficient contrast
- Focus states: 2px solid white ring with 2px offset on dark, 2px solid dark ring on light
- Respect `prefers-reduced-motion` — disable shimmer/reflection animations
- Minimum body font size 16px (1rem)
### ✍️ Writing Tone
- Precise, technical, confident. Short declarative sentences. Feature-forward, benefit-light.
- Labels in title case. Numbers use monospace styling. Avoid exclamation marks.
## Do / Don't
### ✅ Do
- Use linear gradients to simulate brushed metal and chrome reflections
- Apply subtle inner shadows and highlights for debossed/embossed effects
- Keep backgrounds dark to make metallic surfaces pop
- Use thin 1px borders in semi-transparent white for depth
- Add subtle specular highlight streaks on key surfaces (hero, cards)
### ❌ Don't
- Use flat colors where gradients can create depth
- Apply heavy box-shadows — metallic depth comes from gradients, not drop shadows
- Mix warm tones (gold, copper) — stay in silver/chrome/steel family
- Use thick borders — thin and precise
- Overuse animation — subtle is premium; gaudy is cheap
## Quality Gates
- [ ] At least 3 distinct gradient styles (chrome button, card highlight, text effect) are present
- [ ] All interactive elements have hover/active states with gradient shifts
- [ ] No element uses flat background colors — gradients or semi-transparent overlays only
- [ ] Thin borders (≤1px) separate all major sections
- [ ] Contrast verified on gradient backgrounds at all breakpoints
- [ ] `prefers-reduced-motion` disables shimmer and reflection animations