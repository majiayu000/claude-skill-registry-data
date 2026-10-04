---
name: codex
description: OpenAI-style dark code aesthetic with electric blue accents
---
# Codex
## Mission
A developer-first dark aesthetic inspired by code editors and AI terminals — clean, minimal, and high-contrast.
## Brand
### 🎨 Colors
- `#0D1117` — Primary background (deep code-editor dark)
- `#161B22` — Secondary background (cards, panels)
- `#58A6FF` — Accent (electric blue, links, buttons)
- `#C9D1D9` — Primary text (soft white)
- `#8B949E` — Secondary text (muted gray)
- `#1F6FEB` — Interactive elements (hover states)
### 🔤 Typography
- Heading font: JetBrains Mono (Google Fonts)
- Body font: Inter (Google Fonts)
- Type scale: xs 0.75rem / sm 0.875rem / base 1rem / lg 1.125rem / xl 1.5rem / 2xl 2rem / 3xl 2.5rem
### 📐 Spacing
- Grid: 12-column CSS grid, 1rem gap
- Section padding: 4rem top/bottom
- Card gap: 1.5rem
### 🧩 Components
- Buttons: Monospace font, 1px electric-blue border, 8px radius, hover fills background
- Cards: `#161B22` background, 1px `#30363D` border, 12px radius, subtle backdrop-blur
- Nav: Fixed top, `#0D1117` with bottom border `#30363D`, logo left, links right
- Hero: Large monospace heading with cursor-blink animation, code-snippet background texture
- Footer: Minimal, single-line centered text in secondary color
### ♿ Accessibility
- Minimum contrast ratio 4.5:1 for all text
- Visible focus ring: 2px `#58A6FF` outline with 2px offset
- Respects `prefers-reduced-motion` by disabling cursor blink and transitions
- Minimum font size 0.75rem (12px)
### ✍️ Writing Tone
- Technical but approachable — use developer terminology naturally
- Favor precision over marketing fluff; verbs over adjectives
- Labels use sentence case; no ALL CAPS buttons
## Do / Don't
### ✅ Do
- Use monospace for code snippets, headings, and UI labels
- Keep backgrounds deep dark with subtle layering for depth
- Use electric blue sparingly — only for interactive elements and key highlights
- Maintain generous whitespace around content blocks
- Leverage hover transitions on all interactive elements
### ❌ Don't
- Use gradients — flat colors only
- Add shadows heavier than subtle inner glows
- Mix serif fonts into the design
- Overload pages with dense text — favor scanning layouts
- Use bright white (`#FFFFFF`) for body text — stick to `#C9D1D9`
## Quality Gates
- All text passes 4.5:1 contrast ratio check
- Focus states visible on every interactive element
- Page respects prefers-reduced-motion
- No font smaller than 0.75rem
- All buttons have hover and active states
- Dark background is consistent across all sections (no light-mode leaks)