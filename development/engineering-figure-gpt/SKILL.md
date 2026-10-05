---
name: engineering-figure-gpt
description: Use when the user needs publication-style engineering, computer-science, data-science, AI, electronics, or mathematical-modeling figures. Prefer this skill for new conceptual figures, preservation-first image correction/revision/restyling/redrawing, exact benchmark/ablation/sensitivity plots, and mixed conceptual-plus-quantitative figures. Conceptual figures use GPT image generation with explicit publication-quality contracts; exact quantitative geometry stays local and deterministic. The portable image path can reuse the active Codex/CC Switch provider and supports explicitly trusted OpenAI-compatible relays.
---

# Engineering Figure GPT

Use this skill once the figure goal is reasonably clear.

## Choose the workflow

- `image` — new architecture, workflow, graphical abstract, modeling framework, mechanism, schematic.
- `edit` — modify an existing figure with `correct`, `revise`, `restyle`, or `redraw`.
- `plot` — exact bars, trends, heatmaps, scatter, ablation, benchmark, sensitivity/robustness, multi-panel quantitative figures.
- `mixed` — render exact quantitative panels locally and conceptual panels separately; never let image generation redraw the exact panels.

Never use image generation for exact numeric geometry, axes, uncertainty bars, measured coordinates, benchmark values, or formulas that must remain exact.

## Conceptual image contract

An API success is not automatically a successful research figure. Build conceptual requests as:

```text
domain/content template
+ publication image-quality contract
+ user style constraints
+ edit preservation contract (for existing images)
```

Quality profiles are in `assets/prompt-templates/image-quality-contracts.json`:

- `draft` — structural exploration.
- `paper` — default paper-ready conceptual output.
- `final` — strongest final-export constraints.

For `paper`/`final`, require: safe margins; no clipping; one clear reading direction; large high-contrast label regions; essential labels readable around 50% native size/intended paper width; crisp consistent arrows/borders; disciplined alignment/spacing; restrained semantic colors; no unreadable micro-text, blur, ghosting, decorative pseudo-technical fine print, glossy 3D, cinematic lighting, noisy texture, or poster gradients unless explicitly requested.

Read `references/image-quality-contract.md` when image quality or output size matters.

## Default workflow

1. Inspect the user's text, brief, data, reference image, or requested change.
2. Use `references/figure-brief-spec.md` when a structured figure contract is useful.
3. Choose `image`, `edit`, `plot`, or `mixed`.
4. For new conceptual figures, select the closest template from:
   - `assets/prompt-templates/engineering-figure-templates.json`
   - `assets/prompt-templates/mathematical-modeling-templates.json`
5. Route generation through `scripts/efg.py image` so the selected quality contract is injected.
6. For existing images, choose the narrowest edit mode and explicitly preserve everything that should not change.
7. After generation/editing, apply `references/visual-qa.md`.
8. If a concrete raster size/format/aspect matters, verify the actual returned artifact with `scripts/efg.py verify-image`.
9. Fix localized failures with `edit --mode correct` rather than blindly regenerating the full figure.
10. Keep exact plots deterministic and values source-faithful.

## Image mode

Preserve user terminology, scientific relationships, variables, units, notation, and standard abbreviations. Do not invent measurements, formulas, benchmark values, causal claims, modules, thresholds, interfaces, or hardware specifications.

```bash
python scripts/efg.py image \
  "A retrieval system with OCR, embedding, reranking, and answer synthesis" \
  --figure-template system-architecture \
  --quality-profile paper \
  --lang en \
  --save-prompt output/final-prompt.txt \
  --dry-run
```

Remove `--dry-run` only for a live request. Raw prompts routed through `efg image` also receive the quality contract.

Default execution hints when the user does not override runtime parameters:

- `draft` → `quality=low`, `size=1024x1024`.
- `paper` → `quality=high`, `size=1536x1024`.
- `final` quality profile → `quality=high`, `size=2048x1152`.

The `final` quality profile strengthens prompt/render defaults; model-tier routing is controlled separately by `--final` / `--highres`.

For Chinese/bilingual figures, read `references/chinese-labels.md`. Keep Chinese labels concise, provide extra horizontal room, preserve established English abbreviations and mathematical symbols, and do not solve density by shrinking essential text into micro-labels.

## Edit mode

Editing is a first-class workflow. Do not treat a small correction as a new generation.

```bash
python scripts/efg.py edit figure.png \
  "Change Encoder to Cross-Attention Encoder only" \
  --mode correct \
  --preserve "all arrow endpoints" \
  --save-prompt output/edit-prompt.txt
```

Modes:

- `correct` — smallest possible localized fix; preserve canvas, layout, unaffected labels, arrows, palette, typography, and style.
- `revise` — requested local content/structural change; preserve unaffected content and established visual language.
- `restyle` — visual style only; scientific content, labels, relationships, and claims stay locked.
- `redraw` — clean reconstruction; layout may improve, but scientific meaning, canonical labels, and supported relationships remain authoritative.

Use repeatable `--preserve` and `--allow-change` to define the change boundary. Extra `--reference-image` files may guide style/reconstruction but must not silently override the primary figure's scientific content.

### GPT Image 2 edit policy

For `gpt-image-2`, **do not send `input_fidelity`**. GPT Image 2 processes every input image at high fidelity automatically and the API does not allow changing this parameter.

When `--size` is not supplied, `efg edit` and the portable generator inspect the primary source image:

- if its width/height already satisfy GPT Image 2 output constraints, preserve the exact source canvas;
- if the aspect ratio is supported but the pixel dimensions are not legal, choose the nearest legal canvas and emit an explicit warning;
- if exact canvas preservation cannot be safely resolved, fail or require an explicit legal `--size` rather than silently changing the figure.

This matters most for `correct`: a one-label fix should not unexpectedly turn a landscape figure into a different canvas.

Read `references/edit-mode.md`.

## Visual QA and correction loop

Before final handoff, check in this order:

1. scientific fidelity;
2. text integrity;
3. layout integrity;
4. arrows/line quality;
5. color/contrast;
6. raster clarity at native and approximately 50% scale;
7. source-vs-result preservation for edits.

Reject malformed labels, clipping, overlap, wrong/missing arrows, invented detail, blur/ghosting, unreadable micro-text, or unrelated edit changes.

Failure routing:

- typo / wrong arrow / minor clipping → `correct`
- requested scientific content change → `revise`
- style-only issue → `restyle`
- globally unusable layout → `redraw` or regenerate from a revised brief

Read `references/visual-qa.md`.

## Final/high-resolution output

Model tier, rendering quality, and actual raster dimensions are separate concerns.

Routine model:

```text
--model -> OPENAI_IMAGE_MODEL -> gpt-image-2
```

Final/high-resolution model routing:

```text
--model -> OPENAI_IMAGE_HIGHRES_MODEL
```

If `--final` / `--highres` has no explicit image model and no configured `OPENAI_IMAGE_HIGHRES_MODEL`, fail closed. Do not silently lower the model, quality, requested size, or provider.

The requested canvas is controlled separately with `--size`. For GPT Image 2, concrete sizes must obey its model constraints: each edge at most 3840 px, both edges divisible by 16, long/short ratio at most 3:1, and total pixels between 655,360 and 8,294,400. Do not call an output 2K/4K/final-size merely because a model name suggests high resolution.

```bash
python scripts/efg.py verify-image output/figure.png \
  --expected-size 1536x1024 \
  --require-format png
```

Live `efg image` / `efg edit` requests automatically verify that returned raster files are readable and that concrete requested size/format settings were honored. Metadata verification does not replace visual QA.

Read `references/highres-policy.md`.

## Codex + CC Switch / relay behavior

For command-line Codex users, the portable image path resolves connection settings in this order:

```text
explicit CLI override
-> active Codex provider (~/.codex/config.toml + auth.json)
-> legacy OPENAI_* fallback
-> official OpenAI default
```

If CC Switch already selected the Codex provider, do not ask the user to duplicate the same Base URL/key.

```bash
python scripts/codex_provider_config.py
python scripts/efg.py provider-check
```

A non-OpenAI endpoint selected by the active Codex provider is already user-selected. A custom URL supplied independently through `--base-url` or `OPENAI_BASE_URL` still requires `--allow-third-party` or `OPENAI_ALLOW_THIRD_PARTY=1`, because it may receive the API key and edit images.

A provider that works for Codex text may still lack `/images/generations` or `/images/edits`; a compatibility probe also cannot guarantee every image parameter is implemented correctly. Verify real outputs when fidelity/size matters.

Read `references/codex-cc-switch.md`.

## Plot mode

Numeric truth overrides aesthetics. Never alter supplied values to improve appearance.

```bash
python scripts/efg.py plot request.json \
  --spec-out output/spec.json \
  --out-path output/figure \
  --formats png pdf svg
```

If a normalized spec already exists:

```bash
python scripts/efg.py render output/spec.json --out-path output/figure --formats png pdf svg
```

Supported intent includes grouped bars/error bars, trend curves/uncertainty shadows, heatmaps, scatter, legend-only panels, empty layout panels, and multi-panel figures. Read `references/publication-plot-api.md` for the request/spec contract.

## Mathematical modeling

Read `references/mathematical-modeling.md` for modeling tasks.

Rules:

- make Q1/Q2/Q3 handoffs explicit only when they really exist;
- preserve model names, variables, symbols, units, constraints, and abbreviations;
- do not let the image model typeset long formulas that must be exact;
- keep forecast curves, residuals, Pareto fronts, sensitivity indices, robustness curves, heatmaps, confusion matrices, benchmarks, and exact evaluation values local/deterministic;
- never fabricate coefficients, optimal values, weights, rankings, or results.

## Mixed / editable handoff

For mixed figures, render quantitative panels first, generate conceptual panels separately, then compose without raster-redrawing the exact plots. When final typography/formulas/composition need deterministic editing, use `references/editable-figure-handoff.md`.

For reusable or showcase work, preserve the evidence chain described in `references/reproducibility-chain.md`.

## Unified CLI

```bash
python scripts/efg.py prompt --figure-template problem-analysis --quality-profile paper --lang zh "建模背景"
python scripts/efg.py image "建模背景" --figure-template full-modeling-pipeline --lang zh --dry-run
python scripts/efg.py edit figure.png "只修正第二个模块的错别字" --mode correct --dry-run
python scripts/efg.py provider-check
python scripts/efg.py verify-image output/figure.png --expected-size 1536x1024 --require-format png
python scripts/efg.py plot request.json --spec-out output/spec.json --out-path output/figure --formats png pdf svg
python scripts/efg.py render output/spec.json --out-path output/figure --formats png pdf svg
python scripts/efg.py check
```

## Runtime references

Load only the current task's relevant file:

- `references/figure-brief-spec.md`
- `references/image-quality-contract.md`
- `references/edit-mode.md`
- `references/visual-qa.md`
- `references/highres-policy.md`
- `references/chinese-labels.md`
- `references/codex-cc-switch.md`
- `references/publication-plot-api.md`
- `references/mathematical-modeling.md`
- `references/editable-figure-handoff.md`
- `references/reproducibility-chain.md`
