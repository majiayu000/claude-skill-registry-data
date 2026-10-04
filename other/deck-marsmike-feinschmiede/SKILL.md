---
name: deck
description: Build a brand-perfect PowerPoint deck via the master-template renderer. Use when the user asks to create a deck or presentation.
---

# deck — master-template renderer

Generate a brand-perfect `.pptx` by composing **plans** against a brand pack's `master.pptx`. The master supplies typography, colors, footers, slide-number chrome — the renderer only fills placeholders and clones bespoke shapes.

## Quick Start

```python
from pathlib import Path
from feinschliff import FillPlan, render

render(
    Path("feinschliff/brands/feinschliff"),
    [FillPlan(layout="Title Slide", fills={0: "Q3 update", 1: "Roadmap"})],
    Path("out.pptx"),
)
```

Author the call in `feinschliff/.debug/<topic>-<date>/build.py` and run it with `feinschliff build.py` — the plugin's launcher execs the venv Python directly, no CLI in between.

## Brand packs

Each pack ships under `feinschliff/brands/<name>/` with a `master.pptx` (or `.ref` pointer) and catalog files. Built-in packs: `feinschliff` (default), `annual-review`, `geometric`, `scientific`, `shapes`, `gs-ramspau`. Corporate / private packs surface through sibling `feinschliff-*` plugin directories (`$FEINSCHLIFF_BRAND_PATH`). Run `python -m feinschliff.master_template.catalog <brand_pack>` to list layouts + snippets for any pack.

## Mental model

A deck is a list of plans, in slide order:

- **`FillPlan(layout, fills)`** — pick a layout by name (see `<brand>/layouts.yaml`), fill placeholders by `idx`. Values: `str`, `list[str]`, `PictureRef`, or `ChartSpec`. Charts and pictures replace the OBJECT placeholder.
- **`ClonePlan(source_idx, replacements)`** — XML-clone a bespoke source slide from `<brand>/snippets.yaml`. `replacements` is a queue per old-string; repeating `("Milestone", ...)` consumes successive occurrences in document order.
- **`render(..., theme=Path|dict)`** — optional. Patches the master's `theme1.xml` `<a:clrScheme>` from a small JSON. One `master.pptx`, N visual variations; the file on disk is never touched.

## Flow

1. **Interview** if the brief is thin. Topic + audience are the minimum; [references/storyline.md](references/storyline.md) maps audience to a default slide count.
2. **Draft the storyline** per [references/storyline.md](references/storyline.md) — emit the brief block + numbered slides block, pick a frame, tag each row with `role` and `act`, write claim-style titles.
3. **Pick layouts** per [references/layouts.md](references/layouts.md). For bespoke shapes (timelines, funnels, infographics) clone from `<brand>/snippets.yaml` — see [references/clones.md](references/clones.md) for the text-anchor recipe.
4. **Approval gate** — show storyline + chosen layouts, ask "ok?". Don't render until approved.
5. **Render** with the Quick Start snippet. Respect the verbosity tier when sizing fills. See [references/gotchas.md](references/gotchas.md) for pitfalls.
6. **Verify and loop** — convert to PDF and read the pages against the defect classes in [references/verify.md](references/verify.md). Fix and re-render until clean; the reference describes the `/loop`-driven iteration.
