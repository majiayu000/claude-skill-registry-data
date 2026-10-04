---
name: material
description: Google Material Design 3, cards, elevation shadows, rounded corners.
---
# Material
## Mission
Implement Google's Material Design 3 system faithfully — tactile surfaces, meaningful elevation, dynamic color, and consistent component behavior across all platforms.
## Brand
### 🎨 Colors
- `#6750a4` — Primary (M3 default purple)
- `#625b71` — On-surface (text on surface)
- `#ffb4ab` — Error (soft red)
- `#fffbfe` — Surface (light theme)
- `#1c1b1f` — Surface (dark theme)
- `#e8def8` — Primary container
### 🔤 Typography
- **Heading:** Roboto Flex or Google Sans (M3 default)
- **Body:** Roboto Flex (variable, readable)
- **Scale:** xs: 0.75rem (11sp), sm: 0.875rem (14sp), base: 1rem (16sp), lg: 1.125rem, xl: 1.375rem (22sp), 2xl: 1.75rem (28sp), 3xl: 2.25rem (36sp) — follow M3 type scale tokens
### 📐 Spacing
- 8dp grid (8px base unit everywhere)
- Section padding: 24dp vertical, 16dp horizontal (adaptive)
- Card gaps: 16dp
- Border radius: 12–28dp (M3 uses more rounding than M2)
### 🧩 Components
- **Buttons:** Filled tonal, outlined, and text variants; 20–24dp corner radius; 40dp minimum touch target
- **Cards:** Elevated (1–3dp shadow), filled, and outlined variants; 12dp corner radius; surface tint with dynamic color
- **Nav:** Top app bar with centered title, navigation rail or bottom nav, FAB in bottom-right
- **Hero:** Large feature area using M3 tokens, prominent headline (display size), surface container
- **Footer:** Minimal, surface-toned, text links
### ♿ Accessibility
- All interactive elements: minimum 48dp x 48dp touch target
- Dynamic color must pass 4.5:1 contrast in both light and dark themes
- Focus states: visible focus ring (2–4dp outline) on all interactive elements
- Content resizes to 200% without loss of function (WCAG 1.4.4)
- Reduced motion: elevation changes and ripples disabled
### ✍️ Writing Tone
Clear, concise, actionable. Google's voice: helpful, human, humble. Sentence case for all UI labels (M3 standard). Button text is a verb. No jargon without explanation.
## Do / Don't
### ✅ Do
- Use M3 design tokens (color, typography, shape, elevation) — not raw values
- Implement dynamic color (Material You) so the UI adapts to user wallpaper/context
- Maintain consistent elevation system: 0–5 levels with clear visual distinction
- Use tonal palettes (primary container, secondary container) for subtle backgrounds
- Test all components in both light and dark themes
### ❌ Don't
- Mix M2 and M3 patterns — M3 uses more rounding, tonal surfaces, and dynamic color
- Skip elevation for cards — flat cards without shadow are a different variant (outlined), not default
- Use pure black backgrounds in dark theme — M3 uses dark gray (#1c1b1f) with tonal elevation
- Ignore motion guidelines — M3 has specific duration and easing tokens
- Place FABs in non-standard positions (top-left, center) — bottom-right is the canonical position
## Quality Gates
- [ ] All spacing uses 8px (8dp) increments — no arbitrary pixel values
- [ ] Touch targets are at least 48x48dp on all interactive elements
- [ ] Dynamic color tokens adapt correctly in light and dark themes
- [ ] Elevation shadows are consistent: 1dp (cards), 3dp (FAB), 6dp (dialogs), 8dp (nav drawer)
- [ ] UI labels use sentence case (not title case, not all caps)
- [ ] Components follow M3 shape tokens — corner radiuses match spec