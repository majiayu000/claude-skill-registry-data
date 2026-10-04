---
name: industrial
description: Factory/warehouse, exposed structure, metal, concrete, raw.
---
# Industrial
## Mission
Embrace raw, unpolished aesthetics — exposed structural elements, utilitarian typography, and materials like metal, concrete, and steel that celebrate function over decoration.
## Brand
### 🎨 Colors
- `#1a1a1a` — Near-black (primary)
- `#4a4a4a` — Gunmetal gray (secondary)
- `#c44536` — Rust red (accent)
- `#f5f0eb` — Raw concrete (background)
- `#e0e0e0` — Light steel (text on dark)
- `#8b4513` — Oxidized copper (highlight)
### 🔤 Typography
- **Heading:** Bebas Neue (condensed, bold, industrial) or Oswald
- **Body:** IBM Plex Mono or Space Mono (monospace, technical feel)
- **Scale:** xs: 0.75rem, sm: 0.875rem, base: 1rem, lg: 1.125rem, xl: 1.25rem, 2xl: 1.5rem, 3xl: 2.5rem
### 📐 Spacing
- Tight, efficient spacing: 0.5rem–1.5rem gaps
- Section padding: 4rem vertical, 1.5rem horizontal
- Card gaps: 1rem
- Border radius: 0–2px (sharp, angular, no softness)
### 🧩 Components
- **Buttons:** Heavy borders (2–3px), industrial stencil feel, sharp corners, monospace text, hover fills with rust/oxide color
- **Cards:** Border-heavy with visible structural lines, dark backgrounds, angular cutouts (clip-path), rivet/bolt-like decorative corners
- **Nav:** Heavy top bar with visible structural dividers, all-caps monospace labels, industrial iconography
- **Hero:** Full-width construction imagery or concrete texture, massive condensed headline, exposed grid lines
- **Footer:** Heavy border-top, structural column layout, minimal decoration
### ♿ Accessibility
- Minimum 4.5:1 contrast — dark backgrounds with light text are the norm
- Focus states: thick (3px) high-contrast border, angular not rounded
- Minimum font size: 0.875rem (14px) — monospace reads smaller than proportional
- Reduced motion: no heavy parallax or structural animation
### ✍️ Writing Tone
Direct, utilitarian, no-nonsense. Short declarative sentences. Technical terminology welcomed. All-caps for labels and navigation. No marketing speak. Sentence case for body, uppercase for UI labels.
## Do / Don't
### ✅ Do
- Use visible structural elements — borders, dividers, grid lines — as core design elements
- Embrace monospace and condensed typography for an engineered feel
- Add texture: subtle concrete, metal grain, or paper texture backgrounds
- Use angular shapes, diagonal cuts, and sharp corners consistently
- Expose the "bones" of the layout — visible grid lines are a feature
### ❌ Don't
- Add drop shadows — industrial is flat and physically grounded
- Use rounded corners anywhere — sharp angles define the style
- Choose decorative or script fonts — typography should feel engineered
- Add gradients — stick to flat, solid colors
- Include playful illustrations — the tone is serious and functional
## Quality Gates
- [ ] No rounded corners — all border-radius values are 0–2px
- [ ] All text passes 4.5:1 contrast (monospace needs extra care at small sizes)
- [ ] Texture overlays don't exceed 200KB total
- [ ] No drop shadows or soft UI elements
- [ ] Monospace body text is legible at 14px minimum
- [ ] Angular clip-paths render correctly across browsers