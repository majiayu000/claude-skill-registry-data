---
name: ascii-wireframe
description: >
  Author UI wireframes as Unicode box-drawing TEXT (┌─┐│└┘) that embeds directly into proposal.md,
  tasks.md, specs, and PR/issue bodies — the corpus's native text medium. Use this skill whenever the
  request is for a "wireframe", "mockup", "ASCII layout", "box-drawing UI sketch", "text wireframe",
  "low-fi mockup", "lay out a screen", or any low-fidelity sketch of a UI/page/screen/form/dashboard
  that should live inside a markdown doc rather than a browser. Trigger broadly — even when the user
  says "sketch the settings page" or "show me roughly how the checkout flow lays out" without the
  word "wireframe". Ships a glyph canon (4 border families, 30 component recipes, composition rules)
  for hand-authoring, plus an optional `scripts/bin/wireframe-render` for spec-driven generation. Do
  NOT use for rich explanatory HTML diagrams (use `wayfinder`) or production UI (use
  `frontend-design`).
license: MIT
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---


# ASCII Wireframe — Box-Drawing UI Sketches in Text

The corpus's identity is text-first: ASCII tokens, markdown-in-terminal, artifacts that live in
`proposal.md` / `tasks.md` / specs / PR bodies and diff cleanly line-by-line. A box-drawing
wireframe is exactly that medium — a low-fi layout sketch rendered as a 2D grid of Unicode
box-drawing characters that needs zero browser, zero screenshot infra, and renders identically in a
terminal and on GitHub via a fenced code block.

> The glyph vocabulary and component recipes derive from `mualat/wiretext` (MIT) —
> `src/utils/boxDrawing.ts`. This skill ports the canon into the corpus's text-first workflow.

## When to Use

Reach for a text wireframe when the goal is to sketch *where things go* on a screen and have that
sketch live inside a doc. Three skills sit in adjacent space — pick by fidelity and medium:

| You want... | Use | Medium |
|---|---|---|
| A low-fi layout sketch inside a spec or PR | **ascii-wireframe** (here) | box-drawing text |
| A rich, styled explanatory diagram (architecture, diff review, plan) | `wayfinder` | self-contained HTML |
| Production-grade UI / real components / brand styling | `frontend-design` | React / CSS |

The deciding question is the medium, not the subject. If the artifact must survive as plain text in
a git-diffable markdown file and render in a terminal, it belongs here. If it needs color, real
fonts, or interactivity, it does not — escalate to `wayfinder` or `frontend-design`.

Typical triggers: `/bootstrap:user-stories` layout sketches, `/audit:redesign` before/after mockups,
a "here's roughly how this screen lays out" block in a proposal or other Markdown artifact.

## Hand-authoring from the canon

For nearly every wireframe, hand-author the box-drawing text directly. The full glyph vocabulary,
all 30 component recipes (button, input, table, modal, progress bar, tabs, sidebar, ...), and the
composition rules live in `references/box-drawing-canon.md`. Read it before sketching — it has the
exact corner/edge glyphs per border family and a worked example for each component, so you compose
recognizable widgets instead of inventing shapes.

The one correctness rule worth internalizing up front (full detail in the canon): writing a
*space* never erases an existing glyph, but any *non-space* glyph overwrites by draw order
(last writer wins). So to keep a box wall intact, stop a connector one cell short of it — borders
are not auto-preserved at crossings. The canon's "spaces never erase" rule has the full picture.

## CanvasObject JSON schema

`scripts/bin/wireframe-render` (built separately) renders a flat `CanvasObject[]` JSON array to the
box-drawing string. The model is fully declarative — a wireframe IS the array, and rendering is a
pure function of it (no classes, no refs, round-trips through JSON losslessly). These are the fields
the renderer reads (derived from wiretext `src/types/index.ts`):

| Field | Type | Applies to | Notes |
|---|---|---|---|
| `id` | string | all | unique per object |
| `type` | `box` \| `text` \| `line` \| `arrow` \| `component` \| `pencil` | all | dispatches the renderer |
| `position` | `{ col, row }` | all | top-left cell, 0-indexed |
| `width`, `height` | number | box/component/line/arrow | in grid cells |
| `zIndex` | number | all | stack order; higher draws later (on top) |
| `borderStyle` | `single` \| `double` \| `rounded` \| `heavy` | box/component | default `single` |
| `fill` | `solid` \| `transparent` | box/component | `solid` clears the interior; `transparent` lets lower objects show through |
| `label` | string | box, button, input, select, modal, card, browser, ... | centered or positioned per component |
| `content` | string | text | multi-line via `\n` |
| `componentType` | one of the 30 (see canon) | component | selects the recipe |
| `columns` | string[] | table | column headers |
| `navItems` | string[] | navbar | nav labels |
| `tabs` | string[] | tabs | tab labels |
| `listItems` | string[] | list | + `listOrdered: boolean` for `1.` vs `•` |
| `progress` | number (0-100) | progress | fill percentage |
| `sliderValue` | number (0-100) | slider | thumb position |
| `toggled` | boolean | toggle | on/off |
| `checked` | boolean | checkbox/radio | `[✓]`/`(●)` vs `[ ]`/`(○)` |
| `accordionItems`, `sidebarItems`, `breadcrumbItems`, `dropdownItems` | string[] | respective component | item labels |
| `badgeText`, `tagText`, `tooltipText` | string | badge/tag/tooltip | content |
| `stepperValue`, `currentPage`, `totalPages` | number | stepper / pagination | values |
| `endPosition` | `{ col, row }` | line/arrow | other endpoint (or use `rotation`) |

Minimal spec — a labeled box with a button inside it:

```json
[
  { "id": "panel", "type": "box", "position": { "col": 0, "row": 0 },
    "width": 24, "height": 7, "borderStyle": "rounded", "fill": "solid",
    "label": "Settings" },
  { "id": "save", "type": "component", "componentType": "button",
    "position": { "col": 6, "row": 3 }, "width": 12, "height": 3,
    "borderStyle": "single", "label": "Save" }
]
```

Render it (reads stdin, or pass a file path):

```bash
echo '<json>' | node scripts/bin/wireframe-render
node scripts/bin/wireframe-render spec.json
```

## When to reach for wireframe-render

Hand-authoring is the default — it is faster than building a JSON spec for a small sketch, and the
result is what you'd type by hand anyway. Reach for `wireframe-render` when alignment arithmetic
starts to dominate: a 4-column table with a header rule, a multi-section dashboard where columns
must line up, repeated cards on a grid, or anything where one off-by-one cell would be tedious to
fix by hand. The renderer computes the tight bounding box and trims trailing whitespace for you, so
the output drops straight into a fenced block.

Rule of thumb: a single box, form, or small modal → hand-author from the canon. A composed layout
with several aligned regions → write the `CanvasObject[]` spec and render it.

## Export to PR

A short wireframe can sit inline in a fenced block. A tall one bloats the PR/issue diff view — wrap
it in a GitHub collapsible `<details>` block so it stays folded until clicked. The exact wrapper
(plus the plain-text / markdown / HTML export forms) is in `references/box-drawing-canon.md` under
Export Wrappers.
