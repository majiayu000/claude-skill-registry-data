---
name: paper
description: Layered paper texture with tactile depth, stacked sheets, and stationery charm.
---
# Paper
## Mission
Bring the tangibility of physical stationery to the screen — stacked sheets, torn edges, and layered depth that makes digital feel touchable.
## Brand
### 🎨 Colors
- `#FAFAF6` — Background (bright white paper)
- `#3A3A3A` — Primary (graphite)
- `#4A90D9` — Accent (fountain pen blue)
- `#F5A623` — Secondary (highlighter yellow)
- `#F2EFE9` — Surface (cream sheet)
- `#1C1C1C` — Text (ink black)
### 🔤 Typography
- Headings: **DM Serif Display** (serif, editorial)
- Body: **DM Sans** (sans-serif, clean pairing)
- Scale: xs 0.75rem / sm 0.875rem / base 1rem / lg 1.25rem / xl 1.5rem / 2xl 2.25rem / 3xl 3rem
### 📐 Spacing
- 8px grid, with intentional 2-4px offsets between "sheets"
- Section padding: 5rem vertical, 2rem horizontal
- Card gaps: 1.5rem
- Max content width: 70rem
### 🧩 Components
- **Buttons**: Slight 2px radius, subtle 1px shadow (1px blur, 1px y-offset), hover lifts shadow to 2px blur
- **Cards**: White surface, 1px border #E0DCD3, stack effect via negative margin or CSS grid overlap, 4px radius
- **Nav**: Thin bottom border, text links, clean sans-serif, no background until scroll
- **Hero**: Large serif headline, optional torn-paper edge (CSS mask-image), clean photography
- **Footer**: Stacked-sheet effect at page bottom, subtle gradient for "page curl"
### ♿ Accessibility
- Contrast ratio ≥ 4.5:1 on all body text
- Focus ring: 2px solid #3A3A3A with 2px offset, 4px radius
- Reduced motion: disable page-load stagger animations and hover lift effects
- Minimum font size: 0.875rem (14px)
- Decorative paper edges hidden from screen readers
### ✍️ Writing Tone
Warm, personal, considered. Hand-written feel without being casual. Use full words ("and" not "&"). Punctuation is precise. Headlines feel typeset, not typed.
## Do / Don't
### ✅ Do
- Stack elements with z-index and subtle box-shadows to create paper depth
- Use CSS background-image with subtle noise texture (SVG or base64 under 2KB)
- Stagger card animations on load (50ms delay between each)
- Add "torn edge" dividers using mask-image or SVG clip-path
- Underline links with a highlighter-yellow background-color, not text-decoration
### ❌ Don't
- Use gradients as the primary depth mechanism — shadows and borders first
- Overlap more than 3 visible "sheets" at any scroll position
- Use border-radius larger than 4px on any element
- Animate with durations under 200ms — paper moves deliberately
- Use dark mode unless it evokes "black paper" with white ink
## Quality Gates
- [ ] Stacked-sheet effect (z-index + shadow) visible on cards or sections
- [ ] Noise/grain texture present and under 2KB
- [ ] Highlighter-style link underlines implemented via background-color
- [ ] Focus states match the 4px radius and graphite color
- [ ] No CSS animation-duration under 200ms
- [ ] Page readable at 320px with serif headings rendering cleanly