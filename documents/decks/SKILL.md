---
name: decks
description: >-
  Presentations and slide decks: HTML decks edited in the browser, markdown-to-
  slides conversion, Bento decks, themed presets and chart-and-report templates.
  Use when the deliverable is a deck, a slide, a talk or a defence presentation.
  One contract; the engines live under parts/.
---

# decks — presentations

> Home branch in Memora: `root/skill/decks`. Pick the engine by what the owner
> needs at the end, not by what is easiest to generate.

## Choosing a part

| Part | What it covers |
|---|---|
| `parts/dashi-ppt/` | Preset visual themes: offline HTML deck, editable in the browser, exportable to PPTX and PDF through the host |
| `parts/slides/` | Strategic HTML decks with Chart.js, design tokens, responsive layouts, copywriting formulas and slide strategies |
| `parts/md-slides/` | Markdown already written → slides (`---` or `# ` boundaries, optional speaker notes) |
| `parts/bento-slides/` | Bento presentations — single-file `.bento.html` decks whose document is JSON in a `#bento-doc` block |

**Two engines are missing on purpose.** A native `.pptx` engine is source-available
under terms that forbid repackaging, and the chart-gallery templates are
noncommercial-only; neither can ship in a kit licensed CC BY 4.0. When the
deliverable must be a real PowerPoint file or needs those chart pages, install the
engine from its own source first and record the install in `PROVENANCE.md`;
otherwise build the deck as HTML and export.

## Rules

- **The end format decides the engine**: a deck someone edits in the browser is
  `dashi-ppt`, markdown already written is `md-slides`, a single self-contained
  file is `bento-slides`, a designed HTML deck is `slides`.
- **Know which folder is which in `dashi-ppt/project`.** `src/` and
  `dist/theme-runtime/` are the part: the prebuilt runtime ships with the skill and
  templates import it, so it stays committed. `output/` holds generated decks —
  regenerated, never committed. `node_modules` is restored by `npm ci` and never
  travels into a synced skill.
- **Copy on a slide goes through `antislop`**: a deck is the most slop-prone
  artifact in a workspace, and `parts/slides/` copywriting formulas do not replace
  that filter.
- **Ask before you build**: the output format, the audience and register, a theme
  that implies a brand, and any deck that will be published outside the workspace.
- **What the deck decided** — theme, structure, what was cut — becomes a memory
  node under `root/skill/decks`; the deck file itself stays with the project.

## Related

`design` (brand, layout, data on screen), `documents` (the paper a deck defends),
`antislop` (copy and visual tells), `media` (images and audio).
