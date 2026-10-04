---
name: agri-ppt
description: "Turn an agricultural-science review report, evidence brief, or manuscript into a fully EDITABLE PowerPoint (.pptx) — every title, bullet, table, and figure a native editable object, nothing flattened to an image. Same machinery as food-ppt, but for agricultural work: converts the outputs of agri-research, agri-deep-research, agri-paper, and agri-pipeline (or any Word/PDF/Markdown/txt source) into a well-designed, grounded slide deck with presenter notes on every slide. Never invents content beyond the source. Use to make slides, a presentation, a PPT, or a deck from an agricultural report or paper. Triggers: make a PPT for my agronomy paper, slides from my soil science review, presentation from my field-trial report, agricultural journal-club slides, build a deck from my crop research."
metadata:
  version: "1.0.0"
  verified: "2026-07"
  delegates_to: food-ppt
  related_skills: [agri-research, agri-deep-research, agri-paper, agri-pipeline, food-ppt, food-figure]
  references:
    - ../agri-research/references/agriculture-domain.md
---

# Agri-Ppt — Editable Presentations from Agricultural Reports

**Run the `food-ppt` skill exactly** — its subagents (`ppt_coordinator`,
`outline_planner`, `slide_writer`, `figure_placer`, `deck_builder`, `deck_qa`), its
`scripts/build_pptx.py` builder, and its references (source-to-slides, deck-spec,
slide-design, editability-and-qa) — with the agriculture substitutions in
[`agri-research/references/agriculture-domain.md`](../agri-research/references/agriculture-domain.md).
Read that file first. No new machinery here.

## The substitutions
1. **Persona** — present as a **senior agricultural scientist of the specific
   discipline** (agronomy · soil science · horticulture · dairy & animal science ·
   agricultural engineering · agricultural economics). Slide framing and emphasis fit
   that discipline's audience.
2. **Source** — the outputs of `agri-research` / `agri-deep-research` / `agri-paper` /
   `agri-pipeline`, or any user document (**Word · PDF · Markdown · txt**).
3. **Theme** — prefer the agriculture-leaning themes **terracotta** or **forest** (or
   sage/slate) from `food-ppt/templates/INDEX.md`; infer from topic or ask.
4. **Emphasis** — foreground what an agricultural audience needs: site/season/design
   and replication for field trials, the experimental unit, G×E, and units (t/ha,
   kg/ha) — carried from the source, never invented.

## Inherited unchanged (not optional)
Fully **editable** output (native text frames, native tables, movable picture objects;
never a flattened image or a PDF-in-place-of-pptx); **presenter notes on every slide**;
clean, non-generic design (informed by `taste-skill` + `ui-ux-pro-max-skill`, incl.
`metric` big-number heroes and `cards` grids); grounding — slides only as true as the
source, no fabricated finding/number/citation; the academic-style + `human-writing.md`
pairing on slide prose; `scripts/privacy_scan.py` before delivery; and the AI-use
disclosure slide when presenting AI-assisted work. See `food-ppt/SKILL.md`.
