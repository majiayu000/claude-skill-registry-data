---
name: pop
description: Pop art boldness with Ben-Day dots, comic panels, Warhol energy, and graphic punch.
---
# Pop
## Mission
Grab attention and never let go — channel the graphic power of pop art with bold flat colors, halftone patterns, and comic-book storytelling energy.
## Brand
### 🎨 Colors
- `#FFFFFF` — Background (gallery white)
- `#FF003C` — Primary (Warhol red)
- `#FFD500` — Secondary (Lichtenstein yellow)
- `#0066FF` — Accent (comic blue)
- `#FF6B9D` — Surface (pop pink)
- `#000000` — Text (ink black)
### 🔤 Typography
- Headings: **Bebas Neue** (condensed bold, graphic)
- Body: **Archivo** (sans-serif, clean)
- Scale: xs 0.75rem / sm 0.875rem / base 1rem / lg 1.25rem / xl 1.5rem / 2xl 2.5rem / 3xl 4rem
### 📐 Spacing
- 8px grid, but large elements break it intentionally
- Section padding: 4rem vertical, 2rem horizontal
- Card gaps: 1.5rem
- Max content width: 80rem (wide for impact)
### 🧩 Components
- **Buttons**: Bold, flat color fill, 0px radius, thick 3px black border, hover inverts colors, active state shifts 3px down with solid shadow
- **Cards**: Thick black border (3px), 0px radius, white bg, Ben-Day dot pattern accent corner (CSS background), bold interior type
- **Nav**: Bold horizontal bar, thick bottom border, condensed uppercase links, active state underlined with halftone pattern
- **Hero**: Split-color background, oversized headline (4rem+), speech-bubble or comic-panel framing, bold CTA
- **Footer**: Thick black top border, inverted colors (dark bg, white text), minimal links in bold condensed type
### ♿ Accessibility
- Contrast ratio ≥ 7:1 — black on white and white on bold colors
- Focus ring: 3px solid #000000, 0px radius, 3px offset
- Reduced motion: disable color-inversion transitions, keep layouts static
- Minimum font size: 0.875rem
- Bold, high-contrast type aids readability for low-vision users
### ✍️ Writing Tone
Bold, declarative, punchy. Short sentences. Sentence case or ALL CAPS — nothing in between. Comic-book energy: "BAM!", "WOW!", "HERE'S THE THING." No hedging, no qualifiers.
## Do / Don't
### ✅ Do
- Use CSS `background-image` with repeating radial-gradient for Ben-Day dot patterns
- Frame content sections with thick black borders (3px minimum)
- Split backgrounds between two bold colors on diagonal or vertical divides
- Use speech-bubble shapes (CSS border + pseudo-elements) for testimonials or pull quotes
- Invert colors on hover for maximum impact
### ❌ Don't
- Use border-radius — pop art has hard edges
- Use gradients for backgrounds — flat color blocks only
- Fade or soften transitions — use instant color swaps or `steps()` timing
- Use thin borders (under 2px) — if you border something, commit to it
- Use muted, pastel, or desaturated colors anywhere
## Quality Gates
- [ ] Ben-Day dot pattern present via CSS (verify with dev tools)
- [ ] No border-radius anywhere in the stylesheet
- [ ] At least one split-color or diagonal background section
- [ ] Borders are ≥ 2px on all bordered elements
- [ ] No CSS gradients — solid colors only
- [ ] Focus rings are bold black, 0px radius, and highly visible