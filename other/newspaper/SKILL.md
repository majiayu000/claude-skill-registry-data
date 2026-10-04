---
name: newspaper
description: Broadsheet layout — serif headings, multi-column grids, ink-and-paper textures, and editorial gravitas.
---
# Newspaper
## Mission
Bring editorial authority to the screen — dense information architecture, serif-dominant typography, and the rhythm of print journalism translated to pixels.
## Brand
### 🎨 Colors
- `#1A1A1A` — Primary (ink black)
- `#8B0000` — Secondary (masthead red)
- `#D4A574` — Accent (aged paper)
- `#FDF8F0` — Background (newsprint cream)
- `#1A1A1A` — Text (ink black)
- `#666666` — Muted text (gray ink)
### 🔤 Typography
- Heading: **Playfair Display** (Google Fonts) — authoritative high-contrast serif
- Body: **Merriweather** (Google Fonts) — readable serif optimized for screen
- Scale: xs 0.75rem | sm 0.8125rem | base 0.9375rem | lg 1.0625rem | xl 1.25rem | 2xl 1.75rem | 3xl 2.5rem
### 📐 Spacing
- Grid: 3-4 column CSS Grid on desktop, 24px gutter, max-width 1140px
- Section padding: 3rem vertical, 1.5rem horizontal
- Card/article gaps: 1.5rem between columns, separated by vertical hairline rules
### 🧩 Components
- Buttons: text-only with underline on hover, or filled dark with 0px radius, serif or small-caps label, newspaper-style ("READ MORE →")
- Cards: article cards — cream background, thin 1px bottom border, headline + dek + byline + dateline structure, no shadows
- Nav: traditional masthead — centered logo/title, horizontal rule above and below, section links in small caps serif
- Hero: lead story — large headline spanning 2-3 columns, hero image with caption, drop cap on opening paragraph
- Footer: multi-column link grid with small serif headings, copyright line, thin top rule
### ♿ Accessibility
- Contrast minimum 4.5:1 — ink-black text on cream paper passes comfortably
- Focus states: 1px ink-black underline with 4px offset — subtle but distinct
- Respect `prefers-reduced-motion` — remove scroll-triggered reveals
- Minimum body font size 15px (0.9375rem) — newspapers run slightly smaller
### ✍️ Writing Tone
- Authoritative, measured, journalistic. Inverted pyramid structure. Attribution matters.
- Headlines in title case. Body follows AP style. CTAs are neutral ("Continue reading", "View more"). No exclamation marks.
## Do / Don't
### ✅ Do
- Use multi-column layouts (3+ columns) for article grids and content sections
- Apply vertical hairline rules between columns and sections
- Include editorial metadata — bylines, datelines, section labels, photo credits
- Use drop caps on opening paragraphs of feature articles
- Layer horizontal rules (thin, thick, double) as primary section dividers
### ❌ Don't
- Use sans-serif for body text — serif is the newspaper voice
- Apply box-shadows or depth effects — print is flat
- Center-align text — newspapers are flush-left, ragged-right
- Use bright or saturated colors beyond masthead red
- Add animations or transitions — newspapers are static, authoritative
## Quality Gates
- [ ] Body text uses serif typeface — no sans-serif body copy
- [ ] Layout uses 3+ columns at desktop breakpoint
- [ ] Horizontal rules appear between every major section
- [ ] At least 2 editorial metadata elements per article (byline, date, section)
- [ ] Background is cream/newsprint (#FDF8F0 or similar) — never pure white
- [ ] No box-shadows, gradients, or animations anywhere