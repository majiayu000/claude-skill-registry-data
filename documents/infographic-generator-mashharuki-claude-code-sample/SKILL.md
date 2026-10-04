---
name: infographic-generator
description: >-
  Turn raw content — stats, a process, a timeline, a concept, research notes,
  an article, a report — into a single self-contained HTML infographic that is
  clean, accurate, and presentation-ready (viewable in a browser and exportable
  to PNG/PDF or a Claude Artifact). Use this skill whenever the user asks for an
  "インフォグラフィック" / "infographic", a "図解" / visual explainer, a one-pager
  or "1枚もの", a visual summary of data or a document, a "まとめ画像" for slides
  or social media, or wants to "見える化 / ビジュアル化 / 図解して" some information —
  even if they don't say the word "infographic". Prefer this over ad-hoc HTML or
  image generation because code output keeps every number exact, stays editable
  ("make the font bigger", "swap the accent color"), and exports losslessly.
  Not for multi-slide decks (use a slides skill), editable diagrams / flowcharts
  as source-of-truth (use a drawio skill), or dashboards wired to live data.
model: opus
---

# Infographic Generator

Produce **one focused HTML infographic** that communicates a single message with
verified data, strong visual hierarchy, and a restrained palette. Output is a
self-contained `.html` file (all CSS inline, fonts from Google Fonts, charts as
hand-computed inline SVG) so it renders anywhere, exports to PNG/PDF via the
bundled script, and can be published as an Artifact.

Default content language is **Japanese** unless the source material or the user
is in another language. Design the layout and typography for Japanese text
(line-break behavior, no reliance on italic, generous line-height).

## Why code, not image generation

Image models mangle Japanese glyphs, invent numbers, and draw charts whose bars
don't match the quoted percentages. Rendering real text and SVG keeps every
statistic exact and every element editable. Only reach for an image-gen path if
the user explicitly wants an illustrative "poster" look with no real data.

## Workflow

Work through these steps in order. Steps 1–4 are quick; don't skip them — an
infographic fails at the planning stage, not the CSS stage.

### 1. Frame the piece

Establish, from the request or by asking one compact round of questions:

- **The one message.** An infographic carries exactly one idea. If the content
  has two, say so and either split into two infographics or pick the primary.
- **Audience & tone** — business, consumer, education, healthcare, tech. This
  drives palette and font choice.
- **Aspect ratio / medium:**
  - `16:9` landscape (1600×900) — slides, embedding in docs. *Default.*
  - `9:16` portrait (1080×1920) — stories, mobile, long timelines.
  - `1:1` square (1200×1200) — X / Instagram / LinkedIn posts.
  - `A4 portrait` (1240×1754 @150dpi) — printed handout.
- **Language** of the finished piece.

### 2. Organize the source content

Extract the real substance into a short working list before touching layout:

- Copy **every statistic, date, name, and quote verbatim**. "73%増" stays
  "73%増" — never round, re-derive, or infer a number that isn't stated. If a
  figure is missing or ambiguous, ask rather than guess.
- **Curate hard.** An infographic is a headline, not a spreadsheet. Cut
  anything that doesn't serve the one message. Soft caps by type, so each unit
  keeps room to breathe:
  - Statistical: 1 hero stat + **≤6** supporting stats, **≤1** chart.
  - Process / flow: **≤7** steps.
  - Concept / explainer: **≤6** satellites / layers / stages.
  - Comparison: **≤6** criteria rows.
  - Timeline: **≤7** entries for a single-screen (16:9 / 1:1) piece; up to
    **~10** only for a tall 9:16 scroll where the spine still gives each entry
    real spacing. If you have more, group them ("2018–2020: …") or drop the
    minor ones — and say in your summary what you cut and why.
- **Strip secrets** — API keys, tokens, internal URLs, personal data that
  wandered in from pasted logs or docs.
- Note the **source and date** for the footer. Every infographic gets an
  attribution line; unsourced numbers read as fabricated.

### 3. Classify the type and choose a layout

Match the content to one type, then pick its layout blueprint. Read
`references/infographic-types.md` for the full taxonomy and blueprints.

| Content shape | Type | Layout starting point |
|---|---|---|
| Headline numbers, proportions, comparisons of magnitude | **Statistical** | KPI-card grid + hero number; charts only if ≥5 points |
| Ordered steps, how-to, a pipeline, problem→solution | **Process / flow** | Numbered step cards with connectors |
| Events over time, history, a roadmap | **Timeline** | Vertical spine, alternating entries |
| A vs B, before/after, pros/cons, plan tiers | **Comparison** | Two/three colour-coded columns, check/✕ marks |
| How something works, a concept, parts of a whole | **Concept / explainer** | Hub-and-spoke, layered, or annotated diagram |

Offer the user 2–3 layout options in a sentence each when the choice isn't
obvious, then proceed with their pick (or the best default if they defer).

Each type has a ready skeleton in `assets/templates/`. Copy the closest one and
adapt — don't build from a blank file.

### 4. Lock the visual system

- **Palette: one primary, one accent, one neutral. 3 colours max.** Fewer
  colours make the emphasis land. Pick a ready, contrast-checked set from
  `references/color-palettes.md` matched to the audience.
- **Type: 2 typefaces maximum** — one for headings, one for body. Vetted
  Japanese-capable pairings and a size scale are in `references/typography.md`.
- **Spacing rhythm:** ≥20px between elements, ≥40px between sections. Whitespace
  is the tool that guides the eye — protect it.

### 5. Build the HTML

Start from the chosen template. Assemble:

1. **Header** — the title in one line, optional one-line context beneath.
2. **Hero callout** — the single most important number or statement, visually
   dominant (largest, highest, in the accent colour).
3. **3–6 body sections** — each with a short heading, *one* concept, one visual
   element (icon, mini-chart, number), and terse labels.
4. **Footer** — source + date in small (~11px) muted text; optional credit.

For a **concept / explainer**, the diagram *is* the infographic — it must be
the visually dominant element, not a row of small icons. Build it either as one
inline `<svg>` (hub-and-spoke, cycle, annotated illustration) or as styled HTML
boxes joined by real connectors (arrows/lines drawn with CSS or a thin SVG
overlay). Either is fine; what matters is that the relationships are *drawn*,
the connectors don't cross, and the diagram occupies the majority of the
canvas. The `concept-explainer.html` template shows the SVG route; the RAG-style
left-to-right connected-card flow is the HTML route.

Rules that keep it from looking amateur:

- **Charts are inline SVG computed from the real numbers.** A bar for 42% is
  0.42 of the axis length — verify proportions against the quoted figures. Use a
  chart only when a trend or 5+ values need it; 1–4 figures hit harder as big
  numbers. See `references/chart-selection.md`.
- **Icons:** one consistent set (inline SVG, or Font Awesome free via CDN).
  Never use the same icon for two different concepts.
- **Text is real text**, never baked into an image. That's the whole point.
- One visual weight system: title > hero > section head > body > caption,
  consistently applied.
- Self-contained: inline all CSS, load fonts from
  `fonts.googleapis.com`, embed any raster as a data URI. The file must render
  offline-ish from a double-click.

### 6. Self-review before showing the user

Do one focused pass, not an open-ended polish loop — render once, check the
list below, fix what's actually broken, render again if you changed layout, and
stop. Two render cycles is normal; five means you're fiddling.

Run through `references/quality-checklist.md`. The high-frequency failures:

- A number in the graphic doesn't match the source, or a chart bar doesn't
  match its percentage.
- No source/date footer.
- More than 3 colours or 2 fonts crept in.
- A section is doing two jobs, or the whole piece has two messages.
- Cramped sections with no breathing room, or one column far heavier than the
  other.
- Contrast below WCAG AA on any text.

Fix issues before presenting. State briefly what type/layout/palette you chose
and why.

### 7. Deliver and iterate

- Save the `.html` to the working directory (or where the user wants it). The
  HTML is the primary deliverable — it is complete on its own.
- **Export (optional):** `python scripts/render.py <file.html> --format png --width <W> --height <H>`
  produces a PNG or PDF via Playwright. If the script reports Playwright is
  missing, **don't fight it** — don't hand-roll a headless-browser command or
  try alternative renderers. Just tell the user the HTML is ready and that a
  browser's `Ctrl/Cmd-P → Save as PDF` (or publishing as an Artifact) gives
  them an image. One render attempt, then move on.
- Offer to publish it as an **Artifact** for a shareable link.
- Iteration requests ("bigger hero number", "calmer palette", "add a step")
  are cheap edits to the HTML — that's why this is code.

## Reference files

Read these as the step calls for them — don't front-load all of them.

- `references/infographic-types.md` — the 8-type taxonomy, each with a layout
  blueprint and a when-to-use note.
- `references/design-principles.md` — hierarchy, single-message rule, whitespace
  numbers, data-ink, reading-flow (Z / F pattern), Japanese-text specifics.
- `references/color-palettes.md` — ~10 ready 3-colour palettes by audience, each
  with hex values and contrast ratios.
- `references/typography.md` — Japanese-capable heading/body font pairs, the
  type scale, sizing minimums.
- `references/chart-selection.md` — data shape → chart type, and the
  number-as-text vs chart decision.
- `references/quality-checklist.md` — the veto list for step 6.

## Templates

`assets/templates/` holds a self-contained starting file per type:
`statistical-dashboard.html`, `process-flow.html`, `vertical-timeline.html`,
`comparison.html`, `concept-explainer.html`. Each has the design tokens as CSS
variables at the top, a working example with placeholder content, and the
footer already wired.
