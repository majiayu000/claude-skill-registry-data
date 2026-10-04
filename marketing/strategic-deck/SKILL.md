---
name: strategic-deck
description: Build a 25-30 slide strategic pitch / audit deck — gradient hero and divider slides, cream content slides with a vertical accent bar, ink headlines, a highlight accent for "the bet", and a five-act narrative arc (audit - marketing - market - bet - go-to-market). Use whenever the user asks to "build a strategic deck", "audit company X and recommend a bet", "make a strategic pitch deck", "rebuild this deck for [different company]", or any pitch/audit/strategy slide deliverable. Also triggers on "marketing assessment deck", "client assessment deck", "30-slide deck".
---

# Strategic Deck

A reusable design system + pattern library for 25-30 slide strategic decks. Built with `pptxgenjs`. Renders in LibreOffice for QA. Default palette below is one worked example (originally built for an indigo+amber brand) — resolve your own palette from the design-system brand SSOT per "Palette" below; the roles and contrast reasoning are what's reusable, not the specific hex values.

---

## Quick reference

| Task | Where to look |
|------|---------------|
| Build a new deck | No template ships with this skill — implement directly with `pptxgenjs`, following "Slide patterns" and "Design system" below as the spec |
| Choose brand colors | "Palette" section — resolve from the design-system brand SSOT, or reuse the worked example as-is |
| Add a slide pattern | "Slide patterns" section — each is described precisely enough to implement directly |
| Render & QA | `npm install` — run your deck script — convert to PDF/JPG — visually inspect |
| Per-client colors | Your own project's brand notes, if you keep one — this skill has no built-in brand registry |
| Common pitfalls | See "Pitfalls" section below |

---

## When to use this skill

**Use it when the user wants:**
- A strategic audit deck on a company
- A marketing assessment deck for a prospect or client
- A pitch deck framed as "current state - my bet"
- A multi-act narrative deck (typically 5 sections x 4-6 slides each)
- Anything that should match this skill's visual language (gradient heroes, cream content slides, vertical accent bars)

**Don't use it for:**
- One-off pitch decks under 10 slides — overkill
- Quick content slides — use Marp with a lightweight theme instead
- Decks where the user wants a completely different visual system

---

## Design system

### Palette

This skill does not hardcode a brand. Resolve real values from the brand-token SSOT at `{agency-root}/design-system/brands/` (see `{agency-root}/design-system/brands/neutral.json` for the generic fallback, and `skills/html-plan-style/SKILL.md` → "Brand Resolution at Generation Time" for the established idiom other skills use to consume that SSOT). Map the brand's `roles` — `primary`, `primary-dark`, `secondary`, `accent`, `bg`, `surface`, `border`, `text-muted` — onto the PRIMARY/PRIMARY_DEEP/LAVENDER/AMBER/BG/... slots below.

**Worked example** (the palette this skill was originally designed against — an indigo+amber brand; use as-is if no brand SSOT entry exists yet, or as a reference for how the roles map):

```
PRIMARY      1B1F3B   Deep Indigo — accents, kickers, card outlines, dark backgrounds
PRIMARY_DEEP 141730   Deeper Indigo — gradient anchor, darkest fills
LAVENDER     3D4266   Mid-Navy — secondary accent, muted text
AMBER        F5A623   Warm Amber — complementary highlight, BET / WIN / RECO callouts
AMBER_DARK   D98D0B   Darker Amber — hover/active states
BG           F8F6F1   Off-White Cream — default content slide background
BG_ALT       EFEADF   Surface Cream — secondary card backgrounds
TEXT         1B1F3B   Deep Indigo — body text (same as PRIMARY)
MUTED        3D4266   Mid-Navy — captions, footnotes
BORDER       E0DBCE   Cream border — card outlines on white bg
SUBTLE       F5F3EE   Very pale cream — table alt rows
```

Why these roles exist (carries over regardless of which brand's hex values you plug in): PRIMARY anchors dark backgrounds and structural accents; a lighter PRIMARY_DEEP variant gives the gradient somewhere to go without going flat; one high-contrast complementary color (AMBER here) is reserved exclusively for "this is the recommendation" callouts so it never gets diluted by decorative use; BG/BG_ALT/SUBTLE are three cream steps apart just far enough to read as distinct table-row shading without any of them reading as "white."

**To rebrand for a client deck:** resolve the target company's brand from `{agency-root}/design-system/brands/{brand}.json` if one exists, or ask for their brand colors directly. Swap PRIMARY, PRIMARY_DEEP, LAVENDER for the target company's colors. The structure doesn't depend on these specifically.

### Typography

- **Headline font:** DM Serif Display (install locally — download from Google Fonts or your OS font manager)
- **Body font:** Inter (install locally — download from Google Fonts or your OS font manager)
- **Fallback:** Calibri (universal, Vietnamese-friendly)
- **Title sizes:** 56pt (cover), 40-54pt (section dividers), 26-28pt (content slide titles)
- **Body sizes:** 14pt (intro paragraphs), 11-12pt (cards), 10-10.5pt (table cells)
- **Kicker / eyebrow text:** 10-11pt bold uppercase with `charSpacing: 4-8`

### Visual motifs (use consistently)

1. **Vertical accent bar** to the left of every content-slide title — `0.07" wide`, PRIMARY, height matches title block.
2. **Radial gradient** on hero/divider slides — subtle lighter center fading to the deep variant at edges (NOT flat, NOT white center).
3. **Decorative ovals** on hero/divider slides — accent + secondary + white-with-transparency, partially off-slide so they bleed.
4. **Cards with left accent** — content cards have a thin colored vertical strip on the left edge (PRIMARY for default, the complementary highlight color for "win/bet").
5. **No accent lines under titles** — never. They're the AI-deck giveaway.
6. **Footer** on every content slide: "[Deck name] . [page] / [total]" in muted slate.

### Layout grid (16:9, 10" x 5.625")

- Slide margins: 0.4"-0.6" left/right, 0.3"-0.5" top/bottom
- Title block: x=0.6, y=0.4-1.0, w=9
- Content area: x=0.6, y=1.25-4.95, w=8.85
- Footer: y=5.30
- Card gutters: 0.15" between cards in a row

---

## Gradient specification

The hero/divider/closing slides use a radial gradient, NOT a flat fill. Generated as SVG -> PNG via `sharp`. Substitute your resolved PRIMARY / PRIMARY_DEEP hex values for the ones below (this example uses the worked-example indigo palette):

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900">
  <defs>
    <linearGradient id="base" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%"   stop-color="#141730"/>
      <stop offset="55%"  stop-color="#1B1F3B"/>
      <stop offset="100%" stop-color="#242848"/>
    </linearGradient>
    <radialGradient id="glow" cx="50%" cy="50%" r="45%">
      <stop offset="0%"   stop-color="#242848" stop-opacity="1"/>
      <stop offset="100%" stop-color="#1B1F3B" stop-opacity="1"/>
    </radialGradient>
  </defs>
  <rect width="1600" height="900" fill="url(#base)"/>
  <rect width="1600" height="900" fill="url(#glow)"/>
</svg>
```

This produces a subtle lighter-center gradient that adds depth without washing out text. The center is a slightly lighter shade of the brand's dark color, edges are the darkest anchor. No white, no visible spotlight — just warmth.

---

## Slide patterns (the building blocks)

Implement each of these directly in your `pptxgenjs` script — there is no shipped template, so treat the descriptions below as the spec. Reuse / repeat / vary as needed.

### 1. Cover (gradient background)
### 2. Section divider (gradient bg + decorative ovals)
### 3. Standard content slide (cream bg, kicker + title + body)
### 4. Three-card row (icon + title + body)
### 5. Six-card grid (2x3)
### 6. Comparison columns (3 cards horizontally)
### 7. Bordered table (header row + alt-fill rows)
### 8. KPI tile grid (2x3)
### 9. Two-column with chart on left
### 10. Findings/risks list (5+ stacked cards)
### 11. Recommendation hero (gradient bg + 3 dark cards)
### 12. Closing prose (gradient bg + paragraphs + sign-off)

---

## Standard 30-slide structure

```
1.  Cover (gradient)
2.  About this deck (3 cards explaining what this is)
3.  Executive summary (4-5 stacked findings)
4.  PART 1 - divider
5-8.   Part 1 content (company snapshot, products, posture, content audit)
9.  PART 2 - divider
10-13. Part 2 content (channel inventory, SEO gap, brand risk, dev gap)
14. PART 3 - divider
15-17. Part 3 content (competitive map, positioning matrix, options)
18. PART 4 - divider (the pivot to "the bet")
19-24. Part 4 content (global wave, local gap, primitive deep-dive, audience, recommendation, blueprint)
25. PART 5 - divider
26-29. Part 5 content (channels, 90-day plan, KPIs, risks)
30. Closing (gradient + personal note)
```

### Marketing Assessment variant (for a prospect / client assessment)

```
1.  Cover (gradient) — "Marketing Assessment Report"
2.  About this report
3.  Executive scorecard
4.  PART 1 - Current State divider
5-9.   Current state (website, facebook, instagram, google, brand consistency)
10. PART 2 - Process Assessment divider
11-14. Process (customer mgmt, lead gen, decision making, maturity level)
15. PART 3 - Problem Diagnosis divider
16-18. Diagnosis (owner perception, data shows, hidden cost, gap)
19. PART 4 - Recommendations divider
20-24. Recommendations (roadmap, quick wins, foundation, growth, ROI)
25. PART 5 - AI Solutions divider
26-28. AI (mapped to their gaps, examples, SIGNAL method)
29-30. Next steps + closing
```

---

## How to brief a new deck

```yaml
subject:           # Who/what is the deck about?
audience:          # Prospect / investors / internal team
intent:            # "marketing assessment" / pitch / audit / sales
length:            # 20 / 25-30 / 40 slides
arc:               # What's the 5-act narrative? Default: audit - marketing - market - bet - GTM
the_bet:           # If applicable: what's the headline recommendation?
brand_colors:      # Worked-example palette (default) or client-specific, resolved per "Palette" above
language:          # English / Vietnamese / mixed
sources_visible:   # Should source footnotes appear on slides? (default: yes)
risk_tone:         # Constructive ("assessment") / pointed ("paid audit") / neutral
```

---

## Setup

No `template.js` ships with this skill — build the deck script from scratch (or from your own prior deck) using "Slide patterns" and "Design system" above as the spec.

```bash
npm init -y
npm install pptxgenjs react react-dom react-icons sharp
# Write your deck script (e.g. deck.js) implementing the patterns above, then:
node deck.js
```

---

## Rendering & QA workflow

```bash
soffice --headless --convert-to pdf deck.pptx
pdftoppm -jpeg -r 110 deck.pdf slide
ls slide-*.jpg
```

**Visual QA checklist:**
- Title kicker doesn't collide with title text on two-line titles
- Card content doesn't overflow card boundaries
- Footer text and page number have >=0.2" gap
- Decorative ovals don't sit on top of body text
- Gradient is subtle (no white spotlight in center)
- Typography: DM Serif Display for headlines, Inter for body
- Currency: use "VND" string, NOT the dong symbol

---

## Pitfalls (learned the hard way)

1. **Never use "₫" symbol** — LibreOffice renders it wrong. Use "VND".
2. **Never use "#" prefix on hex colors** — corrupts the .pptx file.
3. **Never use 8-char hex with alpha** — corrupts. Use `opacity` property.
4. **Don't reuse `shadow` or `option` objects** — pptxgenjs mutates them in place.
5. **Don't pair `ROUNDED_RECTANGLE` with rectangular accent overlays**.
6. **Don't run a single Edit tool against very long template files** — use sed.
7. **Brand gradient = SVG -> PNG**, not pptxgenjs-native.
8. **Bullets must use `bullet: true`** — never unicode.

---

## Customisation cookbook

Two example alternate palettes, showing how PRIMARY/PRIMARY_DEEP/LAVENDER shift while structure stays fixed:

**Purple variant:**
- PRIMARY: `1B1F3B` -> `6343F0`
- PRIMARY_DEEP: `141730` -> `5427D4`
- LAVENDER: `3D4266` -> `859EFF`
- AMBER stays `F5A623`

**Green variant:**
- PRIMARY: `1B1F3B` -> `00A562`
- PRIMARY_DEEP: `141730` -> `008049`
- LAVENDER: `3D4266` -> `7FCFB0`

---

## File map

```
strategic-deck/
└── SKILL.md              — this file (self-contained spec; no template.js or README.md ship with this skill)
```

---

## See also

- `deck-narrative` — co-load for the deck's ARGUMENT (action titles, Minto
  top-down sequencing, one-message-per-slide, table-vs-chart selection,
  decision-slide construction) before this skill lays out the visuals. If
  exporting `--pptx`, run `deck-narrative/scripts/audit_deck.py` on the
  output before shipping — it mechanically catches system-font leaks
  (Rule 9) and other file-level defects a rendered preview can't show.
