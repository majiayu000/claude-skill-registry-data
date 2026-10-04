---
name: neobrutalism
description: Modern brutalism — bold black borders, primary colors, zero rounding, raw HTML aesthetics, and unapologetic digital honesty.
---
# Neobrutalism
## Mission
Embrace the raw structure of the web — thick borders, primary colors, hard shadows, and zero decoration — for designs that feel honest, loud, and unmistakably digital.
## Brand
### 🎨 Colors
- `#FFD700` — Primary (gold yellow)
- `#FF4500` — Secondary (orange-red)
- `#1E90FF` — Accent (dodger blue)
- `#FFFDF7` — Background (warm off-white)
- `#000000` — Text (pure black)
- `#555555` — Muted text (dark gray)
### 🔤 Typography
- Heading: **Space Grotesk** (Google Fonts) — bold, quirky grotesk
- Body: **Space Mono** (Google Fonts) — monospace for raw digital feel, or **Inter** for readability
- Scale: xs 0.75rem | sm 0.875rem | base 1rem | lg 1.25rem | xl 2rem | 2xl 3rem | 3xl 4rem
### 📐 Spacing
- Grid: explicit CSS Grid, visible gaps, 16px base unit
- Section padding: 4rem vertical, 2rem horizontal
- Card gaps: 1.5rem with visible grid lines or borders between all elements
### 🧩 Components
- Buttons: solid background with 3px black border, 4px black box-shadow offset (4px 4px 0 #000), 0px radius, hover slides shadow to 2px/2px
- Cards: white/colored background, 3px black border, 6px 6px 0 black solid shadow, 0px radius, bold inner padding
- Nav: visible black bottom border (3px), all links in bold monospace, active link has solid background fill
- Hero: massive bold headline (3xl+), 3px black rule below, subhead in monospace, CTA as chunky bordered button
- Footer: thick black top border, 2-3 columns separated by visible vertical rules, monospace small text
### ♿ Accessibility
- Contrast minimum 4.5:1 — black borders/text against warm white passes easily
- Focus states: 3px black dashed outline with 2px offset — highly visible
- Respect `prefers-reduced-motion` — disable shadow-offset transitions, keep the hard look
- Minimum body font size 16px (1rem)
### ✍️ Writing Tone
- Direct, bold, unpretentious. Short declarative sentences. No softening words.
- Labels in ALL CAPS or lowercase — never title case. CTAs are imperative verbs. Use monospace for code-like elements.
## Do / Don't
### ✅ Do
- Use 3px+ solid black borders on every distinct element
- Apply hard box-shadows (no blur, offset 4-8px) in black on interactive elements
- Keep border-radius at 0px everywhere — sharp corners are the rule
- Use bold primary colors (yellow, red, blue) against warm off-white backgrounds
- Make interactive states obvious — shadows shift, backgrounds fill, borders thicken
### ❌ Don't
- Use any border-radius values — 0px or nothing
- Apply drop shadows with blur — solid offset shadows only
- Use gradients or opacity fades
- Add subtle hover transitions — states should pop instantly
- Nest soft elements inside hard ones — maintain consistent visual language
## Quality Gates
- [ ] All elements have border-radius: 0px — verified globally
- [ ] Every interactive element has a ≥2px solid border
- [ ] At least 3 elements use hard offset box-shadows (no blur radius)
- [ ] Color palette limited to 3 bold hues + black + off-white
- [ ] No gradients, opacity transitions, or soft shadows anywhere
- [ ] Typography uses bold weights (≥600) for all headings