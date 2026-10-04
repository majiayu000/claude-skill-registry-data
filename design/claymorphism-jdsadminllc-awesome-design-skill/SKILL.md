---
name: claymorphism
description: Soft 3D, puffy elements with inner and outer shadows for a playful, tactile feel.
---
# Claymorphism
## Mission
Make digital interfaces feel physical and playful — like pressing into soft clay — through layered inner and outer shadows that create puffy, extruded 3D elements.
## Brand
### 🎨 Colors
- `#f0f4ff` — Background (soft pastel blue)
- `#a8d8ea` — Primary clay blue
- `#ffb3ba` — Accent clay pink
- `#bae1ff` — Secondary clay blue
- `#ffffba` — Highlight yellow
- `#e8dff5` — Soft purple clay
### 🔤 Typography
- Headings: Fredoka (Google Fonts)
- Body: Nunito (Google Fonts)
- Scale: xs 0.75rem, sm 0.875rem, base 1rem, lg 1.125rem, xl 1.375rem, 2xl 1.75rem, 3xl 2.25rem
### 📐 Spacing
- Grid: 12-column, 24px gutters
- Section padding: 4rem vertical, 2rem horizontal
- Card gaps: 1.5rem
### 🧩 Components
- Buttons: Puffy — 16px border-radius, solid clay fill, `box-shadow: inset 0 -4px 0 rgba(0,0,0,0.1), 0 4px 12px rgba(0,0,0,0.1)`, press animation reduces inner shadow
- Cards: Large 20-24px border-radius, clay fill, `box-shadow: inset 0 2px 4px rgba(255,255,255,0.5), 0 8px 24px rgba(0,0,0,0.08)`, 24px internal padding
- Nav: Soft pill-shaped container with clay shadow, centered or floating, pastel background
- Hero: Playful — large Fredoka headline, soft gradient or solid pastel background, puffily animated illustration
- Footer: Rounded clay block, soft shadows, simple links, pastel tone
### ♿ Accessibility
- Minimum contrast ratio 4.5:1 for body text against pastel backgrounds
- Focus states: 3px colored outline with 2px offset, using the primary clay color
- Reduced motion: Disable all shadow animations and press effects, use static shadows only
- Minimum font size 0.75rem (12px) for body, 0.875rem recommended
### ✍️ Writing Tone
- Voice: Playful, friendly, encouraging — like a children's book narrator
- Labels: Rounded, friendly language, emoji welcome but not required
- Short sentences, upbeat endings
## Do / Don't
### ✅ Do
- Use both inner and outer shadows on every major element
- Keep the color palette soft and pastel — nothing harsh or saturated
- Add a subtle press/tap animation (reduce inner shadow on active)
- Use generous border-radius (16px minimum for interactive elements)
- Layer multiple clay elements with varying shadow depths for visual hierarchy
### ❌ Don't
- Use sharp corners — border-radius below 12px breaks the puffy illusion
- Add dark, heavy shadows — keep them light and soft (max 15% opacity)
- Use neon or highly saturated colors — they clash with the pastel palette
- Apply claymorphism to text directly — only to containers
- Overdo it — not every element needs to be clay; let some surfaces stay flat
## Quality Gates
- [ ] All interactive elements have both inner and outer shadows
- [ ] No border-radius below 12px on any component
- [ ] Shadow colors use rgba with ≤ 15% black opacity
- [ ] Body text passes 4.5:1 contrast against its background
- [ ] Press animations respect prefers-reduced-motion
- [ ] Color palette contains only pastels — no saturated or neon values