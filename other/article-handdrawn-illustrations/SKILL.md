---
name: article-handdrawn-illustrations
description: Turn a supplied article or one explicit idea into sparse hand-drawn explanatory body illustrations with fresh physical metaphors and a deadpan black character performing the core action. Use for Chinese article illustrations, body-image shot lists, conceptual hand-drawn explainers, or editing an accepted image in this visual system; do not use for sourced infographics, social carousels, slide decks, posters, logos, generic illustration, or generic publication planning.
---
# Article Hand-drawn Illustrations

## Catalog

- Display name: Article Hand-drawn Illustrations
- Categories: Layout & Design
- Status: Ready
- Route label: GPT Image 2 article-body illustrations
- Tone: orange
- Short description: Turn an article's key ideas into sparse, memorable hand-drawn body illustrations.
- Similar skills: make-infographic, create-social-carousel, create-image-deck

## What this skill does

- Reads an article and selects only the passages where an illustration materially improves understanding.
- Converts each selected idea into a fresh low-tech physical metaphor instead of a formal diagram or slide.
- Generates separate, inspectable images in a coherent white-background hand-drawn system.

## How to use

For best results, provide the complete article or substantive body text rather than only a title. Also state the audience, desired quantity, language, ratio, any exact short labels, supplied references, and whether you want a shot list only or final images. A single explicit idea is sufficient when you only need one image.

#### Example

```text
下面是完整文章。请挑出最值得配图的 4 个认知锚点，先给 shot list，再生成 4 张 16:9 白底手绘正文插图。每张只讲一个观点，中文标注尽量少。
```

## Workflow

1. Read the supplied article or idea. Separate the author's explicit claims from interpretation; do not invent research, quotations, facts, or missing sections. If the user supplied only a title or fragment for a multi-image request, recommend that they provide the full article because passage selection and narrative coverage would otherwise be unreliable. Continue from a single explicit idea when one image is enough.
2. Select cognitive anchors rather than distributing images evenly. Prefer a core judgment, turning point, input/output loop, before/after contrast, handoff, common failure, or state change. Default to 4–6 images for a substantive article, 1–3 for short text, and never exceed 8 without an explicit requested count.
3. When planning is requested, stop after an ordered shot list. For each image record its target passage, one core idea, structural relationship, fresh physical metaphor, the black character's indispensable action, up to five short label candidates, and acceptance checks. Do not generate when the user asked only for suggestions or a shot list.
4. Lock one visual system: pure white background; thin, slightly uneven black hand-drawn lines; at least one calm region of whitespace; restrained orange for the main path, red for a warning or key result, and optional blue for secondary state; no gradients, shadows, paper texture, dense UI, formal flowchart, slide grid, commercial vector finish, or decorative title.
5. Invent each metaphor from the current source. Translate the abstraction into one physical action such as sorting, mending, carrying, filtering, folding, weighing, or opening; combine it with only one or two ordinary low-tech objects. The recurring solid-black, white-dot-eyed, thin-limbed, serious character must perform the explanatory action. If removing the character leaves the metaphor fully intact, revise the composition.
6. Generate each image separately through `gpt-image` v1.0 / GPT Image 2 with `quality: "medium"`, `imageSize: "2K"`, the requested ratio or `16:9`, and `batchCount: 1`. Use one durable operation key per image, require a non-empty `executionId`, and poll only that accepted execution to a terminal state. Never combine multiple illustrations into one generated sheet.
7. Inspect every terminal result for source fidelity, one-idea focus, fresh metaphor, character action, whitespace, crop, palette restraint, unintended titles/logos, and readable short labels. Prefer zero to five labels; if generated Chinese is wrong or crowded, reduce or remove optional labels and regenerate only the failed image with a new linked operation key.
8. Preserve accepted results and do not overwrite existing workspace assets without explicit authorization. Deliver images in source order with passage placement, purpose, receipt/status, QA result, and any unresolved text limitation. Do not publish or imply editable-vector delivery.


## User-facing output

- Media type: Ordered shot list and separately generated article-body images
- Default quantity: 4–6 for a substantive article; 1–3 for short text or one explicit idea
- Content per image: One cognitive anchor, one fresh physical metaphor, and one indispensable character action
- Default layout: 16:9 with a pure white background and substantial whitespace
- Model policy: GPT Image 2 Medium/2K, one image per operation, bounded issue-specific replacement
- Downstream use: Chinese articles, blogs, Notion documents, methods, workflow writing, and educational body content
