---
name: origami
description: Folded-paper geometry with sharp angles, layered depth, and crafted precision.
---
# Origami
## Mission
Transform flat screens into crafted spatial experiences — every fold, crease, and angle feels hand-made, deliberate, and structurally honest.
## Brand
### 🎨 Colors
- `#F7F4F0` — Background (rice paper)
- `#2D2D2D` — Primary (sumi ink)
- `#E8573A` — Accent (vermillion red)
- `#4A7C59` — Secondary (pine green)
- `#F0EAD6` — Surface (washi)
- `#1A1A1A` — Text (charcoal)
### 🔤 Typography
- Headings: **Josefin Sans** (geometric, crisp)
- Body: **Karla** (sans-serif, clean and narrow)
- Scale: xs 0.75rem / sm 0.875rem / base 1rem / lg 1.25rem / xl 1.5rem / 2xl 2rem / 3xl 2.75rem
### 📐 Spacing
- 4px grid, with intentional 45° diagonal spacing where fold lines cross
- Section padding: 4rem vertical, 2rem horizontal
- Card gaps: 2rem
- Max content width: 64rem
### ��� Components
- **Buttons**: Sharp corners (0px radius), flat color fill, 2px bottom/right offset for "folded" depth on hover
- **Cards**: Polygon clip-paths for folded corners, subtle gradient to simulate paper thickness, 0px border-radius
- **Nav**: Angular slash separators, geometric logo mark, sticky with thin bottom rule
- **Hero**: Large geometric dividers (CSS clip-path triangles), bold diagonal layouts, single declarative headline
- **Footer**: Folded-paper footer with upward triangle notch, minimal links in structured grid
### ♿ Accessibility
- Contrast ratio ≥ 4.5:1 on all text
- Focus ring: 2px solid #E8573A, sharp corners (0px radius), 2px offset
- Reduced motion: disable all clip-path and transform animations
- Minimum font size: 0.875rem
- All geometric shapes that convey meaning need aria-label or role="img" with title
### ✍️ Writing Tone
Precise, economical, confident. Short declarative statements. No filler words. Labels are single words where possible. Verbs over adjectives.
## Do / Don't
### ✅ Do
- Use CSS clip-path and polygon shapes for section dividers and card corners
- Create depth with layered z-index and subtle box-shadows (not gradients alone)
- Align elements to angular guides — 45° and 30° diagonals
- Use mono-weight lines and borders (1-2px consistent throughout)
- Let negative space form geometric shapes between content blocks
### ❌ Don't
- Use border-radius on any structural element (buttons, cards, inputs)
- Apply blur or soft shadows — keep edges crisp
- Use cursive, script, or overly round typefaces
- Mix more than 3 distinct polygon shapes per page
- Overlap elements without clear z-index hierarchy
## Quality Gates
- [ ] No border-radius values on structural components
- [ ] At least 3 clip-path/polygon shapes on the page
- [ ] Diagonal lines align to 30° or 45° angles (check with dev tools)
- [ ] Focus rings are visible with sharp corners
- [ ] All geometric decorative elements have appropriate aria attributes
- [ ] Layout holds at 320px with polygon shapes adjusting or simplifying