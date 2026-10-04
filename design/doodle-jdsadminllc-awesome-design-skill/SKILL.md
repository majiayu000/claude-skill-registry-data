---
name: doodle
description: Hand-drawn sketch style with playful lines and imperfect charm
---
# Doodle
## Mission
Bring the warmth of a sketchbook to the screen — hand-drawn lines, imperfect shapes, and the charm of something made by a human hand.
## Brand
### 🎨 Colors
- `#FFFDF7` — Paper background (warm cream)
- `#2C2C2C` — Ink (primary text and lines)
- `#FF6B6B` — Marker accent (coral)
- `#4ECDC4` — Highlighter accent (teal)
- `#FFE66D` — Highlighter accent (yellow)
- `#C4A484` — Pencil (secondary lines)
### 🔤 Typography
- Heading font: Caveat (Google Fonts — handwriting)
- Body font: Architects Daughter (Google Fonts)
- Type scale: xs 0.75rem / sm 0.875rem / base 1rem / lg 1.25rem / xl 1.75rem / 2xl 2.25rem / 3xl 3rem
### 📐 Spacing
- Grid: Intentionally loose — 12-column but elements feel hand-placed with slight rotation and offset
- Section padding: 4rem top/bottom (varies slightly per section)
- Card gap: 2rem with slight random rotation (±2deg)
### 🧩 Components
- Buttons: Hand-drawn outline (rough-edged SVG border), white fill with marker-color text, slight rotation on hover (±1deg)
- Cards: "Torn paper" edge effect, hand-drawn border, slightly rotated, drop-shadow offset like paper
- Nav: Hand-drawn underline on active link, sketch-style logo, sticky with paper texture background
- Hero: Large hand-drawn heading with marker-color fills, doodle illustrations (stars, squiggles, arrows) floating around
- Footer: Torn-paper top edge, sketch-style "Thanks!" closing, hand-drawn social icons
### ♿ Accessibility
- All text passes 4.5:1 contrast (ink on paper = high contrast; verify marker colors on paper)
- Focus rings: Hand-drawn style dashed outline, 3px
- Reduced motion: remove rotation animations and floating doodles
- Minimum font size 0.875rem (handwriting fonts need slightly larger size for legibility)
### ✍️ Writing Tone
- Warm, personal, conversational — write like you're leaving a note for a friend
- Use lowercase freely, contractions, and occasional exclamations
- Labels: casual imperatives — "scribble something!", "jot it down"
## Do / Don't
### ✅ Do
- Use hand-drawn SVG borders, underlines, and dividers (rough paths with slight wobble)
- Apply subtle rotation to cards and images (±1-3 degrees)
- Layer doodle illustrations: arrows, stars, squiggles, thought bubbles as decorative elements
- Use marker-like highlight effects behind key text (CSS background with rough edges)
- Maintain a paper-texture background (CSS noise or subtle grain overlay)
### ❌ Don't
- Use perfect geometric shapes — everything should have slight irregularity
- Apply precise alignment — elements should feel placed by hand
- Use cold pure white backgrounds — always warm toward cream
- Add glossy or metallic effects — stick to paper/ink/marker material language
- Over-animate — subtle wobbles and floats only, nothing mechanical
## Quality Gates
- At least 3 hand-drawn decorative elements (borders, dividers, or illustrations)
- No perfect right angles — all corners slightly rounded or irregular
- Background has warm paper tone (not pure white)
- All text passes 4.5:1 contrast
- Page respects prefers-reduced-motion
- Handwriting fonts render legibly at all sizes (test at 0.875rem minimum)