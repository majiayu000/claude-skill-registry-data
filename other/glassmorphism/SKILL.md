---
name: glassmorphism
description: Frosted glass, translucent panels, background blur, vibrant backdrops.
---
# Glassmorphism
## Mission
Create interfaces that feel like layered frosted glass — translucent panels floating over vibrant, colorful backgrounds with depth and dimensionality.
## Brand
### 🎨 Colors
- `#ffffff` — Panel background (at 15–30% opacity)
- `#0a0a1a` — Dark base background
- `#6366f1` — Primary accent (indigo)
- `#ec4899` — Secondary accent (pink)
- `#f8fafc` — Text on dark
- `#1e1b4b` — Text on light
### 🔤 Typography
- **Heading:** Inter (sans-serif, geometric)
- **Body:** Inter (sans-serif)
- **Scale:** xs: 0.75rem, sm: 0.875rem, base: 1rem, lg: 1.125rem, xl: 1.25rem, 2xl: 1.5rem, 3xl: 2rem
### 📐 Spacing
- 8px grid system
- Section padding: 4rem vertical, 2rem horizontal
- Card gaps: 1.5rem
- Border radius: 12–16px on all panels
### 🧩 Components
- **Buttons:** Translucent background with blur, border: 1px solid rgba(255,255,255,0.2), hover brightens to 40% opacity
- **Cards:** backdrop-filter: blur(16px), background: rgba(255,255,255,0.15), border: 1px solid rgba(255,255,255,0.3), border-radius: 16px
- **Nav:** Fixed top bar with backdrop-blur, semi-transparent, border-bottom for separation
- **Hero:** Full-height with vibrant gradient background, centered frosted-glass CTA card
- **Footer:** Subtle frosted bar, lighter blur, minimal content
### ♿ Accessibility
- Minimum 4.5:1 contrast for all text on frosted panels (test against the actual backdrop behind them)
- Focus rings: 2px solid white outline with 4px offset
- Respect prefers-reduced-motion: disable backdrop-filter animations
- Minimum font size: 0.75rem (12px) — never smaller
- All frosted overlays must pass WCAG AA on top of the most contrast-heavy possible background behind them
### ✍️ Writing Tone
Clean, modern, concise. Short labels. No marketing fluff. Use sentence case for UI labels. Product-first language.
## Do / Don't
### ✅ Do
- Use vibrant, colorful backgrounds behind glass panels so the effect is visible
- Layer multiple translucent elements with decreasing opacity to create depth
- Add subtle borders (1px, low opacity) to define panel edges
- Test contrast against multiple background colors, not just the default
- Use backdrop-filter with fallback solid colors for unsupported browsers
### ❌ Don't
- Place frosted glass panels over flat white/gray backgrounds — the effect disappears
- Stack more than 3 frosted layers — it becomes muddy and illegible
- Use text shadows for readability instead of proper contrast ratios
- Forget to provide a solid fallback background-color
- Apply blur to critical text elements — only to container backgrounds
## Quality Gates
- [ ] All frosted panels render correctly in Safari (requires -webkit-backdrop-filter)
- [ ] Text on glass passes 4.5:1 contrast ratio against the actual gradient/image behind it
- [ ] Solid background-color fallback works when backdrop-filter is disabled
- [ ] Panels remain legible at all viewport sizes (mobile glass panels need higher opacity)
- [ ] No more than 3 nested frosted layers
- [ ] Animations are disabled or reduced when prefers-reduced-motion is active