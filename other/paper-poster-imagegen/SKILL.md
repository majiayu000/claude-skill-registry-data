---
name: paper-poster-imagegen
description: Generate, critique, and iterate image-generation prompts for high-fidelity academic paper poster reference mockups before implementing HTML/PDF/PPTX. Use when Codex is asked to create a poster concept image, imagegen prompt, visual reference draft, layout mockup, or "生图" design for ACL/EMNLP/NeurIPS-style A0 posters from a paper, figures, metrics, logos, QR codes, or an existing poster screenshot.
---

# Paper Poster ImageGen

## Purpose

Use image generation to create a reference design image that is structurally close to a final editable poster. Do not treat the generated image as the source of truth for text, numbers, equations, or plots. The source of truth remains the paper, local assets, and later HTML/PPT implementation.

The goal is to make the first generated mockup already express:

- Correct poster logic and reading order.
- Realistic A0 portrait density.
- Placeholders for actual paper figures/tables rather than invented visuals.
- Balanced sections with no obvious overflow or large accidental whitespace.
- Typography, QR/logo placement, and metric hierarchy close to what can be implemented.

## Before Generating

Create a concise poster brief from the paper and assets:

1. Title, subtitle, authors, affiliations, conference mark.
2. Four top metric cards: label, value, comparison, icon concept.
3. One thesis strip sentence.
4. Section order and one-sentence purpose for each section.
5. Paper figures/tables that must appear, with preferred placement.
6. Logos and QR codes that must appear.
7. Things to avoid from prior drafts or user feedback.

If exact content is not available, use readable placeholders in the prompt rather than inventing false values. For text-heavy elements, ask for "structured text blocks and table-like layouts" and later replace with real HTML/PPT text.

## Poster Layout Target

Default to an A0 portrait academic poster with a clean ACL/top-conference style:

- Canvas aspect: A0 portrait, approximately `841mm x 1189mm` or `3179 x 4494` CSS px.
- Palette: white/light-blue panels, deep navy section headers, restrained green/red accents for results.
- Header: left conference/logo block, center title/subtitle/authors, right QR codes or institutional marks.
- Metric strip: four parallel cards with icons, large green numbers, and one-line comparison text.
- Thesis strip: one centered claim below metrics.
- Main body: three columns, center column wider for method and mechanism figures.
- Bottom: one concise conclusion/takeaway section; no metadata footer unless required.

Recommended content flow:

- Left: motivation, problem/failure mode, method core or design constraints.
- Center: method overview, key mismatch/diagnostic figure, mechanism evidence.
- Right: main results, generalization, robustness/sensitivity, conclusion.

## Prompting Rules

- Specify the exact section list and order. Image models otherwise invent sections.
- Describe panels as stable rectangles with navy headers and consistent spacing.
- Ask for real paper-figure screenshots or provided figure thumbnails to be placed as framed images, not redrawn from scratch.
- Preserve coherent figures. Do not ask the model to split or crop a figure just to fill space unless the crop remains complete and intentional.
- Do not ask for small dense paragraphs everywhere. Use large readable text blocks and figure/table placeholders.
- Keep fonts moderate-weight and professional. Avoid comic, handwritten, overly heavy display text, and tiny author/affiliation text.
- Make the generated mockup balanced but not overly packed. If blank space exists, fill it by enlarging important figures or adding paper-backed context, not generic text.
- QR codes should be large enough to scan and have simple captions when useful.
- Every chart/table-like area must have a clear title or caption explaining what it measures.
- No decorative footers, random contact strips, unindexed extra boxes, or duplicated result tables.

## Image Model Limitations

Expect image models to distort exact text, equations, QR codes, and table numbers. Therefore:

- Use generated output for layout, hierarchy, and visual density.
- Replace text, figures, equations, QR codes, and logos with real assets in HTML/PPT.
- Do not accept generated numbers or baselines as factual.
- Do not judge a poster solely by aesthetic polish; verify whether the structure can be implemented.

## Iteration Workflow

1. Generate one reference mockup from the structured prompt.
2. Compare it against the paper and target implementation constraints.
3. Identify failure types:
   - Missing original paper figures.
   - Coherent figure split/cropped incorrectly.
   - Section order or numbering is illogical.
   - Text too small or too heavy.
   - QR/logos too small or misplaced.
   - Large whitespace handled by generic filler text.
   - Result table duplicated or chart lacks explanation.
4. Revise the prompt with explicit negative constraints and section sizing.
5. Only after layout is credible, implement in HTML/PPT with real assets.

For a copy-ready prompt template and review checklist, read `references/prompt-template.md`.
