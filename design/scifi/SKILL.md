---
name: scifi
description: Futuristic HUD aesthetic — holographic overlays, tech-blue wireframes, data-visualization-ready interfaces.
---
# SciFi
## Mission
Make users feel like they're operating a starship. Holographic overlays, wireframe UI elements, data-dense dashboards, and a cold tech-blue palette that says "the future is now."
## Brand
### 🎨 Colors
- `#00D4FF` — Holographic cyan (primary)
- `#0A1929` — Deep space blue (background)
- `#001E3C` — Panel surface
- `#66E3FF` — Bright cyan (accent)
- `#FF6B35` — Alert orange (warnings/notifications)
- `#E0F7FA` — Pale cyan (text on dark)
### 🔤 Typography
- Heading font: Orbitron (Google Fonts)
- Body font: IBM Plex Mono (Google Fonts)
- Type scale: `0.75rem` / `0.875rem` / `1rem` / `1.125rem` / `1.25rem` / `1.5rem` / `2rem`
### 📐 Spacing
- Grid system: 8px baseline with `1px` wireframe guide lines
- Section padding: `4rem` vertical, `2rem` horizontal
- Card gaps: `1rem` with `1px` cyan borders
### 🧩 Components
- Buttons: Angular cut corners (`clip-path: polygon()`), `1px` cyan border, transparent fill, cyan fill on hover
- Cards: Semi-transparent dark panels (`rgba(0, 30, 60, 0.8)`) with `1px` cyan border, `backdrop-filter: blur(4px)`
- Nav: Left-side vertical HUD rail with icon-only links, cyan glow on active, expandable on hover
- Hero: Large wireframe globe or orbital visualization, title with `text-shadow` cyan glow, diagonal scan-line decoration
- Footer: Minimal — horizontal rule with cyan glow, monospace system status line
### ♿ Accessibility
- Contrast: cyan on dark blue passes WCAG AA for large text; body text needs testing — supplement with pale cyan
- Focus states: cyan `box-shadow` glow with `2px` spread, highly visible
- Reduced motion: disable all particle/glow animations, keep static glows
- Font size minimums: `0.875rem` for body, `0.75rem` for data labels only
### ✍️ Writing Tone
- Technical, precise, systems-oriented
- Use terminology that implies advanced technology: "Initialize," "Engage," "Systems Nominal"
- Labels: "Execute," "Configure," "Access Terminal," "View Telemetry"
## Do / Don't
### ✅ Do
- Use `box-shadow` and `text-shadow` for holographic glow effects
- Build wireframe decorative elements with SVG or CSS borders
- Add subtle floating particle animations to hero/background areas
- Use `backdrop-filter: blur()` behind semi-transparent panels
- Keep data dashboards dense — scifi interfaces show everything at once
### ❌ Don't
- Use rounded corners larger than `2px` — scifi is angular and precise
- Add warm colors except for alerts/warnings (orange) and critical errors (red)
- Over-glow — if everything glows, nothing stands out
- Use serif fonts or handwriting fonts anywhere
- Forget to test cyan-on-blue contrast — it's the most common accessibility failure
## Quality Gates
- [ ] All text passes 4.5:1 contrast (use pale cyan for body, cyan for headings only)
- [ ] Glow animations respect `prefers-reduced-motion: reduce`
- [ ] Semi-transparent panels are legible over background content
- [ ] Focus indicators are clearly visible on the dark background
- [ ] Wireframe decorations don't interfere with text readability
- [ ] Works at 4K — test wireframe line widths at high pixel density