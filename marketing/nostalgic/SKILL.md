---
name: nostalgic
description: Film-grain warmth, vintage photography aesthetics, and memory-evoking soft focus.
---
# Nostalgic
## Mission
Wrap users in the warmth of half-remembered moments — faded photographs, sun-bleached paper, and the soft imperfections that make digital feel human.
## Brand
### 🎨 Colors
- `#F4E4C1` — Background (aged paper)
- `#5C4033` — Primary (sepia brown)
- `#C97B5D` — Accent (faded terracotta)
- `#8B7355` — Secondary (warm taupe)
- `#E8D5B7` — Surface (parchment)
- `#2B1D14` — Text (deep espresso)
### 🔤 Typography
- Headings: **Playfair Display** (serif, elegant vintage)
- Body: **Lora** (serif, warm readable)
- Scale: xs 0.75rem / sm 0.875rem / base 1rem / lg 1.25rem / xl 1.5rem / 2xl 2.25rem / 3xl 3rem
### 📐 Spacing
- 4px baseline grid
- Section padding: 6rem vertical, 2.5rem horizontal
- Card gaps: 2rem
- Max content width: 68rem
### �� Components
- **Buttons**: Slightly irregular border-radius (4px/6px alternating), warm beige bg, hover shifts to sepia, no shadow
- **Cards**: Parchment surface, 1px border #D4C4A8, subtle inner shadow for depth, 2px radius
- **Nav**: Centered or left-aligned, thin bottom border, serif links, slow fade transitions
- **Hero**: Full-bleed desaturated photo, vignette overlay, single-line title
- **Footer**: Aged-paper bg, thin rule separator, 2-3 links in small serif
### ♿ Accessibility
- Contrast ratio ≥ 4.5:1 for all body text against backgrounds
- Focus ring: 2px dashed #5C4033 with 3px offset
- Reduced motion: disable all CSS transitions and image parallax
- Minimum font size: 0.875rem
- All images require alt text; decorative images use empty alt
### ✍️ Writing Tone
Warm, personal, slightly poetic. First-person welcome on landing pages. Usewords like "remember," "once," "gather." Avoid marketing jargon. Em dashes over colons.
## Do / Don't
### ✅ Do
- Apply a subtle CSS grain overlay (SVG filter or pseudoelement) across the page
- Use desaturated, warm-toned photography with soft focus
- Add micro-interactions with300ms+ ease-out curves — nothing snappy
- Layer texture: paper backgrounds, uneven borders, subtle noise
- Let images dominate — text is annotation, not the hero
### ❌ Don't
- Use pure black (#000) or pure white (#FFF) anywhere
- Use crisp, hard-edged box-shadows
- Animate with linear or ease-in timing functions
- Use neon, saturated, or cool-toned accent colors
- Over-explain — let mood carry the message
## Quality Gates
- [ ] CSS grain/noise overlay present and under 20KB
- [ ] No pure black or pure white in any color declaration
- [ ] All photographs are desaturated to match palette (verify with color picker)
- [ ] Focus states visible and distinct on all interactive elements
- [ ] Page reads correctly at320px with serif body text
- [ ] Transition durations ≥ 300ms throughout