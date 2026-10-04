---
name: vizuara-ramco-pdf
description: >
  Produce a polished A4 PDF in the exact Vizuara × Ramco house style — terracotta
  accent (#BF654E), Helvetica Neue, section-number badges, status pills
  (DONE/~50%/PLANNED/TO BE DECIDED), sage exit-criteria callouts, gantt timelines,
  and hairline tables. Authors HTML+CSS and renders it to PDF with headless Chrome
  (the same path that produced the reference doc). Use when the user wants a Vizuara
  proposal, engagement roadmap, milestone report, or any client-facing PDF that must
  match the established Vizuara×Ramco look.
---

# Vizuara × Ramco — House-Style PDF

Generate client-facing PDFs that are visually indistinguishable from the reference
`Vizuara-Ramco-Engagement-Roadmap.pdf`. You write an **HTML file** that links
`report.css`, then render it to an **A4 PDF** with headless Chrome. The CSS is the
whole design system — you almost never touch it; you assemble components.

## How to use it

1. **Copy the assets** next to where you're working (or point the `<link>` at them):
   - `assets/report.css` — the stylesheet (do not restyle; reuse the classes).
   - `assets/template.html` — a working document showing every component. Start here.
2. **Write the document** as HTML using the component classes below. Keep `report.css`
   in the same folder as your HTML (the `<link rel="stylesheet" href="report.css">`
   is relative).
3. **Render to PDF:**
   ```bash
   python3 scripts/render.py mydoc.html mydoc.pdf
   ```
   `render.py` finds Chrome/Chromium/Edge automatically and prints A4 with no
   browser header/footer (Skia/PDF, exactly like the original).
4. **Verify** by rendering the PDF pages to PNG and eyeballing them against the
   reference before handing over (see *Testing* below). Fix, re-render, repeat.

## The design system (already encoded in report.css)

**Page.** A4, white background, 48pt (64px) left/right margins. Body is 11px
Helvetica Neue in `#404247`, line-height 1.5. Bold words go near-black `#262626`.

**Palette (CSS variables in `:root`):**

| Role | Var | Hex |
|---|---|---|
| Heading ink | `--ink` | `#262626` |
| Body | `--body` | `#404247` |
| Muted / eyebrow | `--muted` | `#8a9096` |
| **Terracotta accent** | `--terra` | `#BF654E` |
| Terracotta text-on-tint | `--terra-ink` | `#a4513d` |
| Sage (active/done bar, callout border) | `--sage` / `--sage-2` | `#6e8e63` / `#7d9a75` |
| Green pill | `--green-pill-bg/tx` | `#e3f1e3` / `#4a793f` |
| Green callout panel | `--green-call-bg` | `#e9efe7` |
| Amber (in-progress ~50%, milestone) | `--amber-bg/tx` | `#faedcf` / `#a8791d` |
| Lilac (future / to-be-decided) | `--lilac-bg/tx` | `#efe8f2` / `#7959a7` |
| Grey pill (planned) | `--grey-pill-bg/tx` | `#e6e9ec` / `#7c848d` |
| Hairline / empty gantt cell | `--rule` / `--rule-soft` | `#e6e9ec` / `#eff1f3` |

**Components** (all in `template.html`, copy-paste and edit):

- **Cover** `.cover` — top terracotta rule `.cover-rule`; wordmark
  `<div class="wordmark"><span class="v">VIZUARA</span><span class="x">×</span>RAMCO</div>`;
  tracked eyebrow `.eyebrow`; big title `.cover-title`; lead `.cover-lead` (grey with
  a near-black bold lead-in); 2×2 `.meta-grid` (`.meta-label` terracotta small-caps +
  `.meta-value` bold + `.meta-sub` muted); sage `.point-box`; italic `.cover-foot`.
- **Section header** `.section-head` = `.section-num` (terracotta rounded-square badge,
  white number) + `.section-title`. Optional `.section-sub` caption underneath.
- **Subsection** `.subsection-head` = terracotta `.subsection-num` ("4.1") +
  `.subsection-title` + optional `.pill`. Meta line `.subsection-meta` with a
  terracotta `.tag`.
- **Status pills** `.pill` + modifier: `.pill--done` (green), `.pill--progress`
  (amber, for "~50%" / "IN PROGRESS"), `.pill--planned` (grey), `.pill--tbd` (lilac
  "TO BE DECIDED"), `.pill--optional`, `.pill--terra`.
- **Tables** `.tbl` — header row has a terracotta bottom border; rows are hairline-
  separated; `td.k` is a bold key cell; `tr.band` is an uppercase terracotta group
  divider (COMMITTED / OPTIONAL / FUTURE). Put a pill in the status column.
- **Gantt** `.gantt` — row label `td.rowhead` + month cells; `.bar.active` (sage),
  `.bar.milestone` (amber with a dot), `.bar.future` (lilac), plain `.bar` (empty).
  Followed by a `.legend`. To make consecutive active months read as one continuous
  band, either drop the inter-cell gap or span them.
- **Callouts** `.callout` (sage exit-criteria panel; `.callout-label` = green
  small-caps like "EXIT CRITERIA"; `.check` = green ✔) and `.callout--status` (neutral
  grey, for to-be-decided items).
- **Bullets** `ul.dot` / `ul.dash` (terracotta markers); `.lead` bolds the run-in term.
- **Appendix** `.eyebrow.terra` "APPENDIX" label + `.appendix-badge` (dark letter badge).
- **Figures** `figure.fig > img` — drop in a PNG from the **`wisprflow-figure`** skill;
  `figcaption` is a muted caption. This is how editorial charts enter the PDF.
- **Footer** `.doc-foot` — hairline rule + tiny muted line.

## Rules for staying on-style

- Terracotta `#BF654E` is the **only** brand accent — use it for the wordmark's
  VIZUARA, section badges, subsection numbers, small-caps labels and rules. Never
  introduce a new accent hue; status colours (green/amber/lilac/grey) are reserved
  for pills, callouts and the gantt.
- Prepared-by line convention is "Raj · Rajat · …". Documents are
  "commercial-in-confidence and prepared solely for <client>".
- Keep it calm and sparse: lots of white space, hairlines not boxes, one idea per
  callout. Never use drop shadows, gradients, or emoji.
- Every embedded chart/figure must be produced by the **wisprflow-figure** skill so
  the editorial figures match the report.

## Testing (always do this before handing over)

```bash
python3 scripts/render.py assets/template.html /tmp/test.pdf     # 1. render
python3 - <<'PY'                                                  # 2. pages -> PNG
import fitz; d=fitz.open("/tmp/test.pdf")
[p.get_pixmap(matrix=fitz.Matrix(2,2)).save(f"/tmp/t{i}.png") for i,p in enumerate(d)]
PY
```
Open the PNGs and confirm: cover wordmark colours, terracotta badges, pill colours,
sage callout, gantt bars, hairline tables. `render.py` needs Google Chrome (or
Chromium/Edge) installed; the PNG step needs `pip install pymupdf`.
