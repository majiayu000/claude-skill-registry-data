---
name: academic-figure-prompt
description: Create, review, or freeze detailed English prompts for AI image tools to generate academic paper or thesis figures, including framework diagrams, network architecture diagrams, pipeline flowcharts, module detail diagrams, comparison/ablation figures, and data pattern grids. Use when the user asks for paper figure prompts, academic diagram prompts, AI-generated manuscript/PPT figures, image2/gpt-image prompt refinement for academic figures, or when manuscript-to-ppt-workflow needs a confirmed generated academic visual before calling openrouter-icu-image. This skill must align intent and palette first, write a draft prompt artifact, then stop for human confirmation.
---

# Academic Figure Prompt

This skill adapts the upstream `LigphiDonk/academic-figure-generator/academic-figure-prompt` workflow for this repo's staged PPT pipeline.

Use it to turn confirmed research facts and slide intent into a high-density English image prompt. Do not call image generation from this skill. For `manuscript-to-ppt-workflow`, this is a human-alignment gate after asset/layout planning and before content fidelity QA checks the prompt.

## Required Inputs

Before writing a prompt, identify:

- figure purpose: overview, architecture, module detail, comparison/ablation, or data pattern;
- slide or manuscript anchor and the exact claim/source facts it may visualize;
- target audience, aspect ratio, and whether the output is decorative, explanatory, or evidence-adjacent;
- palette choice or reference image;
- editability expectations after insertion into PPT.

If figure intent, source facts, or palette are ambiguous, use `codex-deep-interview` before generating the prompt. Ask only the smallest set of questions needed to avoid guessing.

## PPT Stage Gate

When used inside `manuscript-to-ppt-workflow`, do not proceed unless these confirmed artifacts exist:

- `align/ppt_production_brief_v*.md`
- `align/fact_ledger_v*.md`
- `align/PPT_storyboard_v*.md`
- confirmed asset/layout plan, usually `align/PPT_asset_audit_v*.md` or `align/visual_enrichment_plan_v*.md`

Write or update:

- `align/academic_figure_prompt_v*.md`

The artifact must include:

```yaml
stage: academic_figure_prompt
stage_status: draft | confirmed
requires_confirmed:
  - ppt_production_brief
  - fact_ledger
  - storyboard
  - asset_layout_plan
allowed_next_stage: ppt-content-fidelity-qa-stage
confirmed_by: <user/date or empty>
source_skill: https://github.com/LigphiDonk/academic-figure-generator/tree/main/academic-figure-prompt
```

Use `stage_status: draft` until the user explicitly confirms the prompt. Stop after writing the draft. Do not call `openrouter-icu-image` or run content fidelity QA in the same turn.

## Palette Alignment

If the user has not specified a palette or reference image, present these options and wait for a choice before writing the prompt:

| # | Scheme | Style | Primary | Secondary | Accent |
|---|---|---|---|---|---|
| A | Okabe-Ito academic standard | Nature/Science/CVPR, colorblind-friendly | Steel Blue `#0072B2` | Warm Orange `#E69F00` | Bluish Green `#009E73` |
| B | Blue mono | restrained module/detail diagrams | Navy `#0072B2` | Medium Blue `#4A90D9` | Light Blue `#A0C4E8` |
| C | Teal + Amber | modern ICLR/NeurIPS style | Deep Teal `#00897B` | Amber `#FFB300` | Soft Grey `#ECEFF1` |
| D | Navy + Coral | stable IEEE journal style | Deep Navy `#1A3A5C` | Coral `#E05A47` | Warm Sand `#F5ECD7` |
| E | Slate + Violet | cool medical/bioinformatics style | Slate Blue `#3F51B5` | Muted Violet `#7E57C2` | Pale Lavender `#EDE7F6` |
| F | Forest + Gold | natural-science journal style | Forest Green `#2E7D32` | Gold `#C49A00` | Cream `#F9F6EE` |
| G | Minimal Grey | arXiv technical report style | Charcoal `#263238` | Steel `#546E7A` | one user-specified accent |
| H | Custom | user-provided or reference-derived colors | custom | custom | custom |

For custom palettes, useful external tools include Coolors, ColorHunt, Adobe Color, ColorBrewer, Viz Palette, and Paletton. If a reference image is provided, extract palette and layout from it and let that override presets.

## Prompt Anatomy

Every English prompt must include four layers:

1. Global description: start with a sentence like `A highly detailed, information-dense academic paper [type] diagram...`, naming the figure type, topic, target publication style, and overall layout.
2. Section-by-section detail: use `=== SECTION NAME ===` blocks. For each section, specify background panel, small-caps section label, module boxes, internal substructure, embedded thumbnails, formulas, dimension labels, and arrows.
3. Global annotations: include tensor/vector dimensions, feedback loops, legends, skip connections, and cross-region links where relevant.
4. Style specifications: end with a complete style block containing exact palette values, typography, line weights, white-space policy, and explicit prohibitions.

Key rule: every module box must contain subcontent. Avoid empty placeholder boxes, vague phrases, `...`, and `etc.`.

## Figure Type Patterns

- Overall framework: input -> stages -> output, with 2-4 submodules per stage, white module fills, colored borders, thin arrows with dimensions, and grey dashed feedback/skip paths.
- Network architecture: input layer -> encoder stack -> core parallel branches -> output heads, with branch border colors, repeated-layer `xN` markers, residual dashed arrows, and dimension labels at conversions.
- Module detail: input -> operation -> intermediate representation -> operation -> output, with formula labels and monochrome thumbnails for intermediate states.
- Comparison/ablation: N columns for variants, shared base in grey, changed parts highlighted with colored borders, optional bottom metric bars.
- Data/behavior patterns: 1xN grid, one category per cell, shared axis if relevant, and small monochrome or two-color visualizations inside each cell.

Useful thumbnail vocabulary: time-series waveform, frequency spectrum bar chart, monochrome attention heatmap, 3D trajectory curve, probability bars, decision tree, confusion matrix, neural network layers, feature vector bar, scatter clusters, receptive field grid, convolution kernel, gradient flow, loss curve, ROC curve, example image, point cloud, and spatial heatmap.

## Quality Checklist

Before presenting the artifact, verify:

- every module has subcontent, not just a labeled box;
- color use is restrained, with at least 70% white or near-white area;
- modules use white fills and colored/grey borders rather than colored fills;
- section labels use small-caps text and grey dividers, not saturated banner bars;
- main arrows have dimension or semantic labels;
- key operations have formula annotations when applicable;
- at least half of major modules contain monochrome or two-color thumbnails;
- all visualized claims trace back to the fact ledger or user-confirmed source;
- the prompt remains readable in grayscale;
- the prompt contains no API parameters, file paths, keys, model names, or runtime instructions.

## Output Format

Use a short Chinese explanation if appropriate, but keep the prompt itself in English:

````markdown
### Figure X.Y - [Chinese or English figure title]

Figure type: [framework / architecture / module detail / comparison / data pattern]
Source anchors: [slide id / section / fact ids]
Palette: [selected scheme]
Recommended aspect ratio: [16:9 / 3:2 / 4:3 / custom]
Generation boundary: [what may be visualized; what must not be invented]

```text
[complete English visual prompt only]
```

Self-check:
- [ ] information density
- [ ] source-fact constraints
- [ ] restrained palette
- [ ] grayscale readability
- [ ] no API/path/model parameters mixed into the prompt
````

## Handoff

Inside `manuscript-to-ppt-workflow`, route the confirmed prompt through `ppt-content-fidelity-qa-stage` before using it for final image generation. After content fidelity QA is confirmed and the user approves image generation, `openrouter-icu-image` may use the confirmed English prompt as the visual prompt. Keep API controls such as `model`, `size`, `quality`, `output_format`, and output path outside the image prompt.
