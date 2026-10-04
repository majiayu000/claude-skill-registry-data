---
name: builders-deck-style
description: Use when building, updating, or styling any monday Builders presentation, slide deck, internal pitch, kickoff doc, or HTML deliverable that should match the official Builders brand. Provides the canonical color palette, typography, gradient stroke, cover decorations, card patterns, and layout primitives sourced from the 2026 Builders Kickoff master deck. Invoke when user mentions "Builders deck", "Builders style", "match the deck", "make it on-brand", "kickoff style", or asks to design a slide/page that should look like internal monday Builders material.
---

# monday Builders Deck Style

Visual language for any Builders-branded deck or PDF deliverable. Brand-only — no narrative, no data sources, no specific deck structure.

## Color palette

```css
:root {
 --bg: #000000;
 --bg-light: #FFFFFF;
 --card: #1A1A1A;
 --card-light: #FFFFFF;
 --text: #FFFFFF;
 --text-muted: rgba(255,255,255,0.65);

 --y: #FBC926;   /* yellow — primary brand accent */
 --g: #59E36C;   /* green — acceleration / "we are it" */
 --c: #4DDDD5;   /* cyan */
 --b: #5C5CE0;   /* indigo — filled key boxes */
 --p: #9B7BFC;   /* purple */
 --pink: #FF158A; /* hot pink */
 --red: #DF2F4A;  /* incidents / critical */
}
```

**Signature gradient** (ribbons, card outlines, page numbers, dividers):

```css
background: linear-gradient(180deg, #FBC926 0%, #59E36C 33%, #4DDDD5 66%, #9B7BFC 100%);
```

For SVG strokes, use `<linearGradient>`. Always vertical (180deg) unless following a curved path.

## Typography

Family stack: `'Figtree', 'Inter', system-ui, sans-serif`.

| Role | Weight | Size (16:9) | Notes |
|---|---|---|---|
| Marquee headline | 200 | 60-100pt | White, left-aligned, generous tracking |
| Slide title | 300-400 | 36-48pt | White |
| Card heading | 600 | 20-28pt | White |
| Body | 400-500 | 14-18pt | White or muted |
| Emphasis (`.em`) | 700 | inherit | Often colored (yellow/green/cyan) |
| Eyebrow label | 500 uppercase | 12-14pt | Yellow (`--y`), letter-spaced |
| Numerals (stat hero) | 700 | 80-160pt | White or accent-colored |

Headlines lean left. Use generous negative space rather than centering everything.

## Page formats

| Format | Size | Use |
|---|---|---|
| **16:9 widescreen** | 1920×1080 | Internal presentations, kickoff decks |
| **A4 portrait** | 210×297mm | Shareholder-style PDFs |
| **A4 landscape** | 297×210mm | Internal summary PDFs |

Default to dark theme. Light theme is the exception (shareholder distribution).

## Signature decorations

### Cover ribbons (only on cover)
- Right-edge SVG, 4 stacked cloud/pill outlines
- Each ribbon ~25-30% slide height; together they fill ~80% vertically
- Anchored to right edge, can extend slightly off-canvas
- 2-3px stroke using the signature gradient (no fill, transparent interiors)
- **Cover only** — never on interior pages

### Page numbers
- White digit inside a small gradient-stroke circle (yellow→green)
- Bottom-right corner, ~28-32px diameter

### Logo lockup
- Top-left corner, generous margin (40-60px)
- Use on cover and section dividers only
- Don't repeat on every interior page

## Layout primitives

### `.card` — base dark card with gradient outline

```css
.card {
 background: var(--card);
 border-radius: 20px;
 padding: 36px;
 border: 1px solid transparent;
 background-image:
   linear-gradient(var(--card), var(--card)),
   linear-gradient(180deg, #FBC926, #59E36C, #4DDDD5, #9B7BFC);
 background-origin: border-box;
 background-clip: padding-box, border-box;
}
```

### Pattern variants
- **Stat card** — big accent-colored numeral + label + blurb. Solid colored left border (4-6px) instead of gradient when in dense grids.
- **Quote card** — gradient outline, italic body text, oversized `"` mark in accent color.
- **Key box** — solid `--b` (indigo) fill, yellow eyebrow, large white headline. High-emphasis proof points.
- **Trend card** — split layout (left: label+stat+body; right: SVG chart). Locked white background regardless of theme.
- **Comparison pair** — two side-by-side cards contrasting two columns (Developer/Agent, Today/Tomorrow, Before/After).
- **Category row** — 4-5 horizontal cards with bold heading + 1-line desc. Taxonomies and frameworks.
- **Code snippet card** — dark fill, monospace, syntax-highlighted (teal keywords, yellow strings).
- **Section divider** — plain dark bg, very large left-aligned headline (weight 200, 80-100pt). Optional eyebrow. No ribbons, no decorations — typography breathing in negative space.

### Full CSS reference
Read [references/base.css](references/base.css) for the complete implemented stylesheet with all components.

### Ribbon SVG asset
The cover ribbon SVG is at [assets/ribbon.svg](assets/ribbon.svg).

## Publishing

Save HTML to `content/slides/<slug>.html` before publishing.

When asked to share or publish, use meethtml.com:
```bash
curl -s -X POST https://api.meethtml.com/api/v1/publish \
  -H "Content-Type: application/json" \
  -d '{"html":"<FULL_HTML>","title":"<TITLE>"}'
```

## Compositional rules

- **Lean left** — headlines anchor left, leaving right ~30-40% as breathing space (or ribbons on covers)
- **Negative space over density** — Builders decks are confident, not crowded. Drop content rather than shrink it.
- **One color story per slide** — pick ONE accent per slide and use consistently (left borders, eyebrows, em spans). Don't rainbow.
- **Gradient is the brand** — reserve the full 4-stop gradient for hero/structural moments. Don't apply to body copy or many small elements.
- **Match complexity to message** — hero slides earn elaborate decorations; data slides should be restrained.

## Anti-patterns (don't do these)

- Centered headlines on every slide (breaks lean-left rhythm)
- Gradient on body text or many small UI elements
- Cover ribbons on interior pages
- Mixing accent colors within a single card
- Generic fonts (Arial, Roboto) — Figtree/Inter only
- Light theme on internal decks (default is dark)
- Logo on every page
