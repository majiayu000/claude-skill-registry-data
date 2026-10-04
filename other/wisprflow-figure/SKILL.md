---
name: wisprflow-figure
description: >
  Generate editorial "Wispr Flow" aesthetic figures — warm cream paper (#f8f5e4),
  classical serif display type (Georgia), a muted terracotta/sage/lilac palette on
  ink, a big-number KPI header with a one-sentence caption, a thin sage rule, and a
  single hand-drawn wavy ink baseline. Produces PNG charts (KPI distribution bars,
  horizontal comparison bars, single-metric donut) that drop straight into the
  vizuara-ramco-pdf reports. Use whenever a report, deck, or dashboard needs a calm
  editorial chart or stat figure in the Wispr-Flow / Vizuara house look.
---

# Wispr-Flow Editorial Figures

Every figure a Vizuara report embeds should share one visual signature so the set
reads as a family. That signature — lifted from wisprflow.ai and the proven Vizuara
L1-eval figure — is:

- **Warm cream paper** background `#f8f5e4` (never white).
- **Classical serif** display type — **Georgia** — for the big number, labels, and
  the caption. No sans anywhere in the figure.
- **Muted pastel palette on ink:** terracotta `#bc6e61` (low / below-target),
  sage `#98b096` (boundary / neutral-good), lilac `#d7bedc` (strong / high), all on
  near-black ink `#1b1a17`. A thin **sage rule** `#a3b097` under the header.
- **A big-number header:** a huge serif KPI on the left (e.g. `92.3%`) with a small
  caption under it, and a one/two-line sentence to its right.
- **One hand-drawn touch:** a single **wavy ink baseline** across the bottom. Nothing
  else is decorated — no gridlines, no axis spines, no chart junk.
- Generous whitespace. Calm, editorial, print-first. Landscape 1376×768 by default.

## How to use it

Everything lives in `scripts/wisprflow_figures.py`. Import it, or drive it from a
JSON spec, or copy a function and tweak.

**Render the built-in demos** (one of each type into `examples/`):
```bash
python3 scripts/wisprflow_figures.py demo
```

**From Python** (the normal path — you pick data + colours):
```python
from wisprflow_figures import stat_bars, comparison_bars, donut

stat_bars(
    counts=[5, 53, 121, 183, 290, 1661],      # raw counts are fine
    labels=[0, 1, 2, 3, 4, 5],
    headline="92.3%\ncore correct or better",  # text after \n is the small caption
    sub="Of 2,313 real questions, 2,134 received the correct core answer – "
        "above the 90% target, with 3 hallucinations (0.13%).",  # auto-wraps
    out="fig_accuracy.png",
)

comparison_bars(
    items=[("Manual (today)", 42, "terra"),    # (label, value, colour-name)
           ("Assisted", 71, "sage"),
           ("Chia engine", 93, "lilac")],
    headline="2.2×\nthroughput at the same headcount",
    sub="Journeys completed per analyst-day across the three operating modes.",
    out="fig_throughput.png", unit="/day",
)

donut(78, headline="78%\nof journeys fully automated",
      sub="Share of PO-create journeys the engine runs end-to-end.",
      out="fig_automation.png", color="lilac")
```

**From a JSON spec** (for non-coders):
```bash
python3 scripts/wisprflow_figures.py spec fig.json out.png
# fig.json: {"type":"stat_bars","counts":[...],"labels":[...],
#            "headline":"92.3%\ncore correct or better","sub":"..."}
```

## The three figure types

| Function | Shape | Use for |
|---|---|---|
| `stat_bars` | KPI + vertical distribution bars | a headline % with the rating/score spread behind it (the canonical figure) |
| `comparison_bars` | KPI + horizontal labelled bars | before/after, mode/model comparison, ranked values |
| `donut` | KPI + single ring | one share/percentage on its own |

**Colour semantics** (pass names, not hex): `"terra"` = low/below-target/cost,
`"sage"` = boundary/neutral-good, `"lilac"` = strong/high/result, `"ink"` = emphasis.
For distributions, `stat_bars` auto-colours lows terracotta → boundary sage → highs
lilac; override with the `colors=[...]` argument.

**Headline convention:** `"BIGNUMBER\ncaption"` — the first line is the huge serif
figure, the text after `\n` becomes the small caption beneath it. Keep the `sub`
sentence short (it auto-wraps at ~52 chars/line to stay inside the right margin).

## Extending it

To add a new chart type, compose the shared primitives already in the module so it
inherits the family look automatically:
`_canvas()` (cream page, pixel coords), `_header()` (big KPI + sentence + sage rule),
`_wavy_baseline()` (the hand-drawn bottom line), `_caption()`, `_save()`. Keep the
palette constants and Georgia; add nothing that isn't cream/serif/pastel/ink.

## Getting figures into the report

Save the PNG, then reference it from the PDF skill's HTML:
```html
<figure class="fig">
  <img src="fig_accuracy.png" alt="accuracy">
  <figcaption>Figure 1 — core-correct accuracy across 2,313 questions.</figcaption>
</figure>
```
The `vizuara-ramco-pdf` skill's `figure.fig` styling frames it correctly.

## Requirements
`pip install matplotlib numpy`. Georgia ships with macOS/Windows; on Linux install a
Georgia-compatible serif (e.g. `fonts-liberation` → Liberation Serif) or change the
`SERIF` constant at the top of the module.
