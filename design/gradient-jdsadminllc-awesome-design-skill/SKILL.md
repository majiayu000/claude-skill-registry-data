---
name: gradient
description: Bold color transitions, mesh gradients, flowing color, vibrant.
---
# Gradient
## Mission
Use bold, intentional color transitions to create depth, energy, and visual direction — gradients are the primary design element, not decoration.
## Brand
### 🎨 Colors
- `#ff6b6b` — Coral (gradient start)
- `#4ecdc4` — Teal (gradient mid)
- `#7c3aed` — Violet (gradient end)
- `#1a1a2e` — Dark background
- `#ffffff` — Text on dark
- `#111827` — Text on light
### 🔤 Typography
- **Heading:** Space Grotesk (geometric, modern)
- **Body:** DM Sans (clean, neutral)
- **Scale:** xs: 0.75rem, sm: 0.875rem, base: 1rem, lg: 1.125rem, xl: 1.25rem, 2xl: 1.5rem, 3xl: 2.25rem
### 📐 Spacing
- 8px grid system
- Section padding: 5rem vertical, 2rem horizontal
- Card gaps: 2rem
- Border radius: 8–12px
### 🧩 Components
- **Buttons:** Gradient-filled with smooth color transitions (e.g., coral→violet), white text, subtle box-shadow on hover
- **Cards:** Dark background with gradient border (via border-image or pseudo-element), subtle inner gradient for depth
- **Nav:** Solid dark background, gradient accent line at bottom (2px), logo may use gradient text
- **Hero:** Full-viewport gradient mesh background, animated gradient shift on scroll
- **Footer:** Dark background with subtle gradient top border, minimal content
### ♿ Accessibility
- All gradient-over-text must pass 4.5:1 contrast at every point in the transition
- Focus states: high-contrast outline (not gradient) — 3px solid #ffffff or #000000
- Prefers-reduced-motion: disable gradient animation, use static gradients
- Never convey information through color alone — always pair with icons/labels
### ✍️ Writing Tone
Energetic and bold. Short, punchy headlines. Active verbs. Modern tech voice. Labels in sentence case.
## Do / Don't
### ✅ Do
- Test gradients at the endpoints — the lightest and darkest points must meet contrast minimums
- Use gradients to direct visual flow (top-to-bottom for hero, left-to-right for CTAs)
- Keep gradient angle consistent across related components
- Add subtle noise/texture overlays to prevent banding on large gradient surfaces
- Use conic and radial gradients for decorative accents, not core UI
### ❌ Don't
- Place white text over a gradient that fades to a light color — test every point
- Use more than 3 color stops in a single gradient without a clear reason
- Animate gradients continuously — it's distracting and impacts performance
- Apply gradients to small text or icons where the effect is invisible
- Use low-contrast gradient borders that blur into the background
## Quality Gates
- [ ] All gradient-text combinations pass 4.5:1 contrast at the lightest point of the gradient
- [ ] No visible color banding on large gradient surfaces (test on 10-bit displays)
- [ ] Gradient direction is consistent: CTAs use one angle, hero sections use another
- [ ] Fallback solid color is defined for all gradient elements
- [ ] Gradient animations respect prefers-reduced-motion
- [ ] Print stylesheet renders gradients as solid colors