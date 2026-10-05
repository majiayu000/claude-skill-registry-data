---
name: decision-gate-notebook
description: "House pattern for a human-in-the-loop gate at a pipeline inflection point: a read-only Quarto/R notebook re-plots what a stage just wrote, surfaces the numbers behind N explicit calls, and records the verdict in analysis_config.yaml so the next stage refuses to run until APPROVED. For the live-kernel variant see interactive-breakpoint-explorer."
license: MIT
---

# Decision-Gate Review Notebook

## Overview

A pipeline has moments where a machine should stop and a person should look. Which
contrasts do we freeze into the signature? Which significance gate? Do we drop the
ambiguous ortholog mappings? These are judgment calls that an expensive, hard-to-reverse
downstream stage leans on — and burying them in a script's defaults means nobody actually
*looked*.

This skill is the house pattern for those moments: a **read-only review notebook** that
re-plots what the stage just wrote, lays out the numbers behind each call, and **sets the latch
in `analysis_config.yaml`**, where the next stage reads `status: APPROVED` and otherwise refuses
to run. The notebook is the eyes; the config is the gate; the numbered script is the hands. The
reasoning behind the call is a topic note under `docs/_internal/<stage-stem>/`.

**When to use this skill:**
- A pipeline reaches an inflection point a human must sign off on before a costly / irreversible stage (freezing a signature, exporting a projection, committing an annotation).
- You want the sign-off to be *auditable and reproducible* — recorded in config and version-controlled — not a chat message.
- You want the review to render both inline on GitHub (committed GFM markdown + PNGs) and as a standalone HTML.

**When NOT to use this skill:**
- Throwaway exploration with nothing downstream waiting → just use the console.
- A stage that writes authoritative state → use `analysis-code-conventions` (the notebook must stay read-only).
- A plain results/methods write-up with no decision to gate → a normal `.qmd` report, no `decisions.[stage]` block.

---

## Decision Tree

```
Pipeline stage just finished. Should the next stage run automatically?
│
├─ Next stage is cheap + fully determined by config  → no gate, just run it
│
├─ Next stage is expensive / hard to reverse, and a
│  person must choose among options first
│        │
│        ├─ The choice is captured by a few config knobs  → DECISION-GATE NOTEBOOK (this skill)
│        │     notebook re-plots the evidence → human sets decisions.[stage].status: APPROVED
│        │     → next stage reads the gate and runs
│        │
│        └─ The choice needs a bespoke interactive app (live UMAP, brushing)
│              → interactive-breakpoint-explorer  (live kernel, jscatter brushing)
│
└─ You just want to write up results  → ordinary .qmd report, no gate
```

---

## The three parts

### 1. The notebook — read-only, own folder, IDE-agnostic root

Each review notebook lives in **its own folder** so its rendered outputs stage as one unit:

```
02_analysis/notebooks/
├── render.R                                  # one renderer for all notebooks
└── [NN]_[stage]_review/
    ├── [NN]_[stage]_review.qmd               # source
    ├── [NN]_[stage]_review.md                # committed GFM (renders on GitHub)
    ├── [NN]_[stage]_review.html              # committed standalone HTML
    └── [NN]_[stage]_review_files/figure-gfm/ # committed PNGs the .md references
```

Copy `assets/notebook.qmd` as the starting point. Its setup chunk is the load-bearing part —
it resolves the compartment root in a way that works **whether the notebook is knitted,
quarto-rendered, or run line-by-line in radian from any directory**, and it forces a headless
PNG device so figures render on a container with no X11.

The notebook **only reads** `03_results/` + `02_analysis/config/analysis_config.yaml`. It never
writes anything a later stage consumes. It re-plots live from the checkpoints/tables (through
`figure-style`), so the review always reflects the current config rather than a baked-in PNG.

### 2. The config decision block — the machine-readable call

The human's decision is recorded in `analysis_config.yaml` under a `decisions.[stage]` block.
Copy `assets/decisions-config-snippet.yaml`. The shape:

```yaml
decisions:
  projection:                 # [stage] key — one block per gated inflection point
    status: PROPOSED          # PROPOSED | APPROVED  — the gate the next stage checks
    # ---- the actual calls the notebook is asking the human to make ----
    contrasts_primary: [WT_heat, KO_heat, Interaction]
    gate: fdr_logfc
    ortholog_ambiguity:
      drop_interaction_if_trivial: false
      trivial_min_genes: 10
    record: docs/_internal/<stage-stem>/<topic>.md   # where the reasoning lives
```

The notebook reads these same keys and shows the human exactly what `status: APPROVED` would
freeze — so the plots and the config never drift apart.

**Every key in this block is read by something** — the notebook, or the downstream stage's
guard. Keep it that way. The reasoning behind the call is a different artifact: the evidence
weighed, the alternative rejected, who decided and when belong in a topic note under
`docs/_internal/<stage-stem>/` (skill: `reasoning-trace`), which is versioned and survives the
next edit to this config. `status` is a latch; the note is the record.

### 3. The gate — the next stage refuses until APPROVED

The downstream script guards on the block at the top, before doing any work:

```r
dcn <- yaml::read_yaml(here("02_analysis/config/analysis_config.yaml"))$decisions$projection
if (!identical(dcn$status, "APPROVED"))
  stop("Stage 18 is gated: set decisions.projection.status: APPROVED in analysis_config.yaml ",
       "after reviewing 02_analysis/notebooks/17_signature_review/. Nothing is frozen until then.")
```

Until the human flips `status` to `APPROVED`, the stage stops. This is the whole point — the
gate is code, not discipline.

---

## Quick Start

```bash
# 1. scaffold a review notebook for stage NN
mkdir -p 02_analysis/notebooks/17_signature_review
cp $SKILL/assets/notebook.qmd 02_analysis/notebooks/17_signature_review/17_signature_review.qmd
cp $SKILL/assets/render.R     02_analysis/notebooks/render.R          # once per project

# 2. add the gate block to config (append decisions-config-snippet.yaml, rename [stage])
#    then guard the downstream stage on decisions.[stage].status == "APPROVED"

# 3. edit the .qmd — re-plot what the stage wrote, ask the N questions

# 4. render both targets (run from the COMPARTMENT ROOT)
Rscript 02_analysis/notebooks/render.R 02_analysis/notebooks/17_signature_review/17_signature_review.qmd both
#   → commit the .md + _files/figure-gfm/*.png (renders inline on GitHub) and the .html
```

**Verify it worked:**

```bash
# figures are committed PNGs (GitHub strips base64 data-URIs), not svg/base64
ls 02_analysis/notebooks/17_signature_review/17_signature_review_files/figure-gfm/*.png
grep -q 'figure-gfm/.*\.png' 02_analysis/notebooks/17_signature_review/17_signature_review.md && echo "GFM refs committed PNGs — OK"
```

---

## Progressive Depth

### Basic usage — the setup chunk that makes it robust

The one piece you must not simplify. It does three jobs: force a headless PNG device, resolve
the compartment root from a sentinel, and bind `here()` to that root (never `getwd()`).

```r
#| label: setup
#| include: false
knitr::opts_chunk$set(echo = FALSE, message = FALSE, warning = FALSE,
                      fig.align = "center", out.width = "80%",
                      dev = "ragg_png", dpi = 150)   # headless PNG → _files/figure-gfm/
options(bitmapType = "cairo")                        # any bare png()/ggsave() stays headless-safe

# Resolve the compartment root: the notebook's own dir when knitr knows it (render),
# else walk up from the wd to a sentinel (interactive line-by-line). Bind here() to the
# resolved root so source()/readRDS() work from ANY launch directory.
.find_root <- function(sentinel = "02_analysis/config/analysis_config.yaml") {
  start <- tryCatch(dirname(knitr::current_input(dir = TRUE)), error = function(e) NA_character_)
  if (is.na(start) || !nzchar(start)) start <- getwd()
  d <- normalizePath(start, mustWork = FALSE)
  while (!file.exists(file.path(d, sentinel))) {
    parent <- dirname(d)
    if (identical(parent, d))
      stop("compartment root (", sentinel, ") not found above ", start,
           "\n  -> launch radian from inside the compartment, or render via notebooks/render.R")
    d <- parent
  }
  d
}
.root <- .find_root()
knitr::opts_knit$set(root.dir = .root)   # render pass runs from the compartment root
if (interactive()) setwd(.root)          # line-by-line runs agree with render
here <- function(...) file.path(.root, ...)   # anchored to root, never getwd()
```

Why each line earns its place is in `references/root-resolution.md` — read it before you
"simplify" the chunk, because the obvious simplifications reintroduce the bug it fixes.

### Intermediate usage — the review body

Structure the body as *question → evidence → reading*, one section per call the human must
make. Each section: a short framing of the decision, a plot re-built live from the checkpoint
(through `figure-style`), a table, and a "what we see" paragraph. Pull the proposed answer
straight from the config (`decisions.[stage]`) with inline R so the prose tracks whatever you
tweak — never hardcode the set you're proposing to freeze. End with a green-light box that
states the single edit (`status: APPROVED`) and the command that then runs.

### Advanced usage — headless / no-VS-Code operation

The pattern is deliberately IDE-agnostic. Under `docker exec` + nvim + tmux, with no VS Code:
launch `radian` from the compartment root, run chunks by sending lines to the radian pane
(`tmux send-keys`, or R.nvim/Nvim-R), and view plots via **httpgd** served over http to the
host browser. `Rscript render.R` produces the committed GFM/HTML the same way it does under
VS Code. Nothing here needs a Jupyter kernel — the knitr engine sends R to a plain R session.
See `references/headless-workflow.md`.

---

## Verification Checklist

After authoring a decision-gate notebook, confirm:

- [ ] **Read-only:** the notebook writes nothing under `03_results/` that a later stage reads — grep it for `write`, `saveRDS`, `ggsave` outside the notebook's own `_files/`.
- [ ] **Root robustness:** `cd` into `02_analysis/notebooks/[nb]/`, launch `radian`, source the setup chunk — `here("02_analysis/helpers/figure_style.R")` resolves with no manual `setwd()`.
- [ ] **Headless figures:** rendered `.md` references committed `figure-gfm/*.png` (not `.svg`, not base64 `data:` URIs).
- [ ] **The gate bites:** with `status: PROPOSED`, the downstream stage `stop()`s; flipping to `APPROVED` lets it run.
- [ ] **Config-tracked prose:** the proposed answers in the narrative are read from `decisions.[stage]`, not hardcoded.
- [ ] **Every key has a reader:** each key under `decisions.[stage]` is consumed by the notebook or the stage guard. A key nothing reads belongs in the topic note.
- [ ] **The reasoning is durable:** the evidence weighed and the alternative rejected are written to `docs/_internal/<stage-stem>/`, not left in a YAML string.

---

## Common Pitfalls

### Pitfall: here() bound to getwd() breaks line-by-line runs

- **Symptom:** `source(here("02_analysis/helpers/figure_style.R"))` fails with "cannot open file '.../notebooks/02_analysis/helpers/figure_style.R'" when you run chunks in radian, even though `knitr::opts_knit$set(root.dir=...)` is set.
- **Cause:** `opts_knit$set(root.dir)` only changes the working directory for the *knit/render* pass — it does **not** change `getwd()` in an interactive session. So `here <- \(...) file.path(getwd(), ...)` resolves against wherever you launched radian.
- **Fix:** bind `here()` to the sentinel-resolved `.root`, and `if (interactive()) setwd(.root)`. Both are in `assets/notebook.qmd`.

### Pitfall: figures render as SVG with an X11 warning

- **Symptom:** `Warning: unable to open connection to X11 display ''`, and `_files/figure-gfm/` contains `*.svg`, not `*.png`.
- **Cause:** R's default `bitmapType` is `Xlib`, which needs an X server. On a headless container `png()` fails and knitr silently falls back to `svg`.
- **Fix:** `knitr::opts_chunk$set(dev = "ragg_png")` (+ `options(bitmapType = "cairo")`). `ragg` and cairo are in the image; both are headless.

### Pitfall: GitHub shows broken images

- **Symptom:** the `.md` renders on GitHub but every figure is a broken-image icon.
- **Cause:** the render embedded base64 `data:` image URIs; GitHub strips those from markdown.
- **Fix:** render the GFM target with `rmarkdown::github_document()` (or `quarto render --to gfm`), which writes committed PNG files under `_files/figure-gfm/` and references them by path. Commit that directory. `assets/render.R` does this correctly — do not set knitr `upload.fun`/`image_uri` for the GFM target.

### Pitfall: the notebook drifts from what the stage will actually do

- **Symptom:** the review says "freezing WT_heat, KO_heat" but the export stage freezes a different set.
- **Cause:** the notebook hardcoded the proposed set instead of reading `decisions.[stage]`.
- **Fix:** read `decisions.[stage]` in the notebook and in the downstream stage from the same config keys. The notebook shows the human exactly what `APPROVED` will freeze.

---

## Resources

- **Quarto with R (knitr engine):** https://quarto.org/docs/computations/r.html
- **GitHub-flavored markdown output:** https://pkgs.rstudio.com/rmarkdown/reference/github_document.html
- **ragg headless raster device:** https://ragg.r-lib.org/
- **Bundled templates:** `assets/notebook.qmd`, `assets/render.R`, `assets/decisions-config-snippet.yaml`
- **Deep dives:** `references/root-resolution.md`, `references/headless-workflow.md`

---

## When not to use

- Do not use for throwaway scratch exploration. A decision-gate notebook is a committed, rendered artifact tied to a config gate; if nothing downstream waits on the call, just hack in the console.
- Do not let the notebook COMPUTE anything a later stage depends on. It reads 03_results/ and config and re-plots; authoritative outputs stay in the stages. Use `analysis-code-conventions` for stages that write state.
- Do not use as a general reporting/methods document. This is a decision surface with an APPROVED gate, not a results write-up.
- Do not use for software architecture or design review. Use architecture-first-dev.
- Do not use solely to interpret pathway or TF results. Use bulk-rnaseq-gsea or bulk-rnaseq-activity-inference unless a downstream stage awaits a recorded decision.

---

## See also

- `figure-style` — Prerequisite; the styling/saving contract the notebook re-plots through
- `analysis-code-conventions` — Sibling convention; narrative stages and authoritative data flow
- `interactive-breakpoint-explorer` — Live-kernel variant; brushes a live embedding (jscatter) instead of re-plotting a static snapshot
- `bulk-rnaseq-pathway-explorer` — Alternative; a heavier static, shareable HTML dashboard (UMAP-of-gene-sets, no live kernel) when the review needs to leave the notebook
