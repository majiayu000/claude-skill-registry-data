---
name: food-ppt
description: "Turn a food & nutrition review report, evidence brief, or manuscript into a fully EDITABLE PowerPoint (.pptx) that opens in PowerPoint / Keynote / Google Slides with every title, bullet, table, and figure as a native editable object — nothing flattened to an image. Converts the outputs of food-research, food-deep-research, food-paper, and food-pipeline (or any Word/PDF/Markdown/txt source) into a well-designed deck: it plans the outline, writes concise grounded slide text with presenter notes on every slide, places figures as movable picture objects, builds the .pptx via python-pptx, and QA-checks editability. Design informed by taste-skill. Use to make slides, a presentation, a PPT, or a deck from a report or paper. Triggers: make a PPT, create slides, presentation from my report, turn this review into slides, build a deck, PPTX from my paper, journal-club slides, conference presentation."
metadata:
  version: "1.0.0"
  verified: "2026-07"
  subagents: [ppt_coordinator, outline_planner, slide_writer, figure_placer, deck_builder, deck_qa]
  related_skills: [food-research, food-deep-research, food-paper, food-pipeline, food-figure, agri-ppt]
  references:
    - references/source-to-slides.md
    - references/templates.md
    - references/deck-spec.md
    - references/slide-design.md
    - references/editability-and-qa.md
---

# Food-Ppt — Editable Presentations from Food & Nutrition Reports

Turn a **review report, evidence brief, or manuscript** into a **fully editable
`.pptx`** — every title, bullet, table, and figure is a **native PowerPoint object the
author can edit**, never a flattened image. Original work; the schema→builder→QA
architecture and design sensibility are informed by the open-source (MIT) `ppt-master`,
`GordenPPTSkill`, and `codex-ppt-skill` skills and the `taste-skill` and
`ui-ux-pro-max-skill` design guides (see the repo README Acknowledgements). No
third-party templates are bundled.

## What it converts
The outputs of the suite's other skills, or any report/paper the user supplies:
- **`food-review`** panel report / Review & Response Report → a review-findings deck.
- **`food-research` / `food-deep-research`** evidence brief or literature review → a
  synthesis deck.
- **`food-paper`** manuscript (or sections) → a paper-presentation / journal-club deck.
- **`food-pipeline`** — offered at FINALIZE to package the finished work as slides.

## Required content for a proposal / paper deck
- **Experimental-design flow diagram** — a **`flow`** slide near the front, built from
  **`food-figure`**'s blueprint (`experimental-flow.md`) and rendered as **native,
  movable PowerPoint shapes** (one box per step, one arrow per transition — never a
  flattened image), so the audience grasps the design at a glance. **Mandatory** for
  any deck from a research proposal or research paper.
- **Results slides illustrate the result** — each is a **`result`** slide: a
  **figure** (from `food-figure`, theme-matched) where feasible, or a **scientific
  table** when the numbers are the point, **plus a Key findings** panel of takeaways.
- **Big numbers and parallel facts get their own design** — a single striking figure
  goes on a **`metric`** big-number hero; a set of parallel facts (objectives,
  contributions, study parameters, KPIs) goes on a **`cards`** accent-bar grid, not a
  bullet list (`references/slide-design.md`).
- **Executive summary** — a closing summary slide is **required** in every deck.
- **Theme-matched figures** — figures use the deck theme's palette so they match the
  slides.

## Editable-first (non-negotiable) — `references/editability-and-qa.md`
Build with **python-pptx** so the deck is genuinely editable: **real text frames**
for titles/bullets, **native tables** (editable cells) for data, and figures placed as
**movable/resizable picture objects**. **Never** render a slide to a background image,
never bake text into a picture, never deliver a PDF in place of a `.pptx`. If a figure
exists only as a raster, embed it as a picture object (still movable/replaceable) and
say so; prefer a vector/redrawable source where available.

## Subagents (dispatch via the Agent tool)
1. **`ppt_coordinator`** — takes the source report/manuscript + audience/length, runs the flow, returns the `.pptx` + a slide-by-slide summary.
2. **`outline_planner`** — reads the source and builds the **slide outline** (`references/source-to-slides.md`): one idea per slide, a clear narrative arc, target slide count for the audience.
3. **`slide_writer`** — writes concise, **grounded** slide text (bullets ≤ ~1 line each), speaker notes carrying the detail; every claim/number traces to the source — no new facts, no invented data.
4. **`figure_placer`** — selects figures/tables from the source (or calls **`food-figure`**) and maps them to slides as editable picture objects / native tables.
5. **`deck_builder`** — assembles the **deck-spec JSON** (`references/deck-spec.md`) and runs **`python3 scripts/build_pptx.py <spec>.json --out <deck>.pptx`**.
6. **`deck_qa`** — verifies editability, checks text overflow / slide density, and confirms every slide's content is faithful to the source (`references/editability-and-qa.md`).

## Templates & design (`references/templates.md`, `references/slide-design.md`)
**Pick one of 17 editable themes** — slate (default) · sage · burgundy · teal · graphite
· ocean · terracotta · forest · consulting · dashboard · azure · geometric · indigo ·
scholar · claret · apricot · **midnight** (a dark theme) — with the deck-spec `"theme"`
field (catalog: `templates/INDEX.md`; preview: `templates/theme-previews.svg`). Most
recreate the look of the open-source `GordenPPTSkill` gallery (in English) as original
theme definitions; `midnight` recreates a Grok-generated dark deck. **`ppt_coordinator`
auto-picks a theme from the deck's text via `scripts/suggest_theme.py` and offers the
top few as options** for the user to choose. A theme is a palette +
type + layout style (cover brand bar + side panel, full-bleed section dividers, accent
edge stripe, underlined titles, big-number heroes, accent-bar cards, footer + slide
numbers, styled tables) applied as **editable shapes** — no bundled template files,
nothing flattened. `ppt_coordinator` chooses the theme from topic/audience or asks.
Restrained academic look informed by `taste-skill` and `ui-ux-pro-max-skill`: a real
type scale (strong size + weight contrast), one accent + ink/greys, whitespace, one idea
per slide, and layout variety — never the templated "AI deck" look.

## Grounding & privacy (inherited)
Slides are **only** as true as the source — never add a finding, number, or citation
that isn't in it (`food-paper/references/faithfulness-and-citation.md`). Apply the
academic-style + `human-writing.md` pairing to slide prose. Run
`scripts/privacy_scan.py` on the deliverable; keep the mandatory **AI-use disclosure**
on a closing slide when the deck presents AI-assisted work.

## Requirements
`python-pptx` (`pip install python-pptx`). Figures come from the source or `food-figure`.
