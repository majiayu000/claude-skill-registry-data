---
name: handwritten
description: Personal script feel, marker/pen texture, human warmth.
---
# Handwritten
## Mission
Bring human warmth and personal connection to digital interfaces through script typography, textured strokes, and an intentionally imperfect, handcrafted aesthetic.
## Brand
### 🎨 Colors
- `#2d1810` — Dark brown (primary text)
- `#fef7f0` — Warm cream (background)
- `#e85d3a` — Marker orange (accent)
- `#2a9d8f` — Ink teal (secondary)
- `#f4a261` — Warm amber (highlight)
- `#264653` — Charcoal (dark accent)
### 🔤 Typography
- **Heading:** Caveat (Google Fonts, handwriting script) or Reenie Beanie
- **Body:** Gaegu (soft handwriting) or Nunito Sans for readable body
- **Scale:** xs: 0.75rem, sm: 0.875rem, base: 1rem, lg: 1.125rem, xl: 1.25rem, 2xl: 1.5rem, 3xl: 2rem
### 📐 Spacing
- Organic spacing — not rigid grid: 1rem–2.5rem gaps
- Section padding: 3rem vertical, 1.5rem horizontal
- Card gaps: 1.5rem with slight rotation (1–3deg) for a pinned-note feel
- Border radius: 4–8px (slightly irregular via clip-path or pseudo-elements)
### 🧩 Components
- **Buttons:** Marker-like underline on hover, handwritten text, slightly rounded, warm fill
- **Cards:** Paper texture background (subtle noise), slightly rotated (0.5–2deg), shadow like a sticky note
- **Nav:** Minimal, handwritten logo, horizontal rule that looks like a pen stroke (wavy SVG path)
- **Hero:** Large handwritten headline, ample whitespace, subtle paper texture background
- **Footer:** Simple, small handwritten "thanks" or signature, minimal links
### ♿ Accessibility
- Handwriting fonts must remain legible — minimum 1rem (16px) for body text, 1.5rem for headings
- 4.5:1 contrast maintained — handwriting fonts are often thinner and need higher contrast to compensate
- Focus states: thick, visible outline (3px), not handwritten
- Prefers-reduced-motion: no paper flips, no text wave animations
### ✍️ Writing Tone
Warm, personal, conversational. First-person where appropriate. Use contractions. Write like you're leaving a note for a friend. Short sentences. Occasional em dashes for asides. Labels in sentence case.
## Do / Don't
### ✅ Do
- Use one handwriting font for headings, a clean sans-serif for body text — never two competing scripts
- Add subtle paper textures (noise, grain) to backgrounds for tactile warmth
- Keep line lengths short (45–65 chars) to mimic note-taking
- Use slight rotation on cards to feel like pinned sticky notes
- Pair handwritten elements with ample whitespace to avoid visual clutter
### ❌ Don't
- Use handwriting fonts for long-form body text — limit to headings and short UI labels
- Apply all-caps to handwriting fonts — they become illegible
- Mix more than one handwriting font on a single page
- Use script fonts at sizes below 14px
- Over-animate handwriting strokes — subtle is enough
## Quality Gates
- [ ] Handwriting font loads within 2s (use font-display: swap)
- [ ] All handwriting text passes 4.5:1 contrast at rendered weight
- [ ] Body text is in a readable sans-serif, not a handwriting font
- [ ] Mobile: handwriting headings don't overflow or break mid-word
- [ ] No more than one handwriting font family used per page
- [ ] Fallback serif font is defined and legible when web font fails