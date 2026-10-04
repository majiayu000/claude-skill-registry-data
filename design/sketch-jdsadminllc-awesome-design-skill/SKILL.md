---
name: sketch
description: Rough pencil-sketch aesthetic with hand-drawn borders, draft-quality charm, and playful imperfection.
---
# Sketch
## Mission
Make digital interfaces feel hand-crafted. Rough, pencil-drawn borders, slightly irregular shapes, and the charm of a first draft — celebrating imperfection in a pixel-perfect world.
## Brand
### 🎨 Colors
- `#2C2C2C` — Pencil graphite (text)
- `#FFFDF7` — Paper white (background)
- `#F5F0E8` — Warm paper tint
- `#E8E0D0` — Erased/light pencil (borders)
- `#4A90D9` — Blue pencil (links/accent)
- `#D94A4A` — Red pencil (errors/highlights)
### 🔤 Typography
- Heading font: Caveat (Google Fonts)
- Body font: Caveat (Google Fonts)
- Type scale: `0.875rem` / `1rem` / `1.25rem` / `1.5rem` / `1.75rem` / `2.25rem` / `3rem`
### 📐 Spacing
- Grid system: intentionally loose — no rigid grid, elements sit naturally like on paper
- Section padding: `3rem` vertical with `1px` hand-drawn divider between sections
- Card gaps: `1.5rem` — cards sit at slight, varied rotations (±1.5deg)
### 🧩 Components
- Buttons: `2px` rough SVG-filtered borders (feDisplacementMap), slightly rotated, hand-drawn underline on hover
- Cards: Bordered boxes with subtle rotation (alternating ±1deg), sketch-style drop shadow (`2px 2px 0` in graphite)
- Nav: Horizontal list with hand-drawn underline on active item, loose letter-spacing
- Hero: Large hand-lettered heading with doodle decoration (stars, squiggles, arrows), slightly tilted
- Footer: Simple line with "Drawn with ❤️" — like a sketchbook colophon
### ♿ Accessibility
- Contrast: graphite on paper = 12:1 (AAA); blue pencil links at 4.5:1 minimum
- Focus states: `3px` blue pencil dashed outline (hand-drawn feel, still visible)
- Reduced motion: remove sketch-filter animations, keep static irregularities
- Font size minimums: `0.875rem` — handwritten fonts need slightly larger sizes for legibility
### ✍️ Writing Tone
- Warm, personal, conversational — like a note from a friend
- Use contractions, occasional asides, and self-deprecating humor
- Labels: "Jot this down," "Scratch that," "Doodle here," "Send it ✉️"
## Do / Don't
### ✅ Do
- Apply SVG filters (`feDisplacementMap`, `feTurbulence`) to borders for rough edges
- Rotate cards and elements by ±1–2 degrees for sketchbook feel
- Use CSS `border-radius` with slightly uneven values (e.g., `7px 9px 6px 8px`)
- Add hand-drawn decorative elements (arrows, circles, underlines) via SVG or emoji
- Use a paper-texture background (`background-image` with subtle noise)
### ❌ Don't
- Use perfectly straight lines or uniform border-radius — irregularity is the point
- Apply sketch filters to text — keep type clean and readable
- Over-rotate — everything tilted is disorienting; keep it subtle
- Mix in modern sans-serif fonts — commit to the handwriting aesthetic
- Use glassmorphism, gradients, or smooth shadows — they break the sketch illusion
## Quality Gates
- [ ] SVG filters render consistently across Chrome, Firefox, and Safari
- [ ] All text meets 4.5:1 contrast despite the paper background tint
- [ ] Card rotations don't cause horizontal overflow at any breakpoint
- [ ] Hand-drawn decorative elements don't interfere with text readability
- [ ] Focus indicators are visible and distinguishable from sketch borders
- [ ] Page feels intentional, not sloppy — irregularity is systematic, not random