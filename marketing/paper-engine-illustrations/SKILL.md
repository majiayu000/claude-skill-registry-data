---
name: paper-engine-illustrations
description: Creates and revises branded Paper Engine illustrations featuring Yuki, the recurring polar-bear inventor, in a clean hand-drawn editorial style. Use when the user explicitly requests Paper Engine or Yuki artwork, a recurring mascot illustration, a quirky hand-drawn editorial visual, or a presentation, article, social, profile, or explainer image that should follow this established brand style. Do not use for generic diagrams, ordinary presentation design, unrelated profile images, or general-purpose image generation without a Paper Engine, Yuki, mascot, or matching editorial-style requirement.
license: MIT. See LICENSE
---

# Paper Engine Illustrations

## Core Focus

Design and generate personal-brand illustrations for presentations, explainers, articles, social graphics, profile images, diagrams, and similar visual communication. Default to 16:9 landscape for body images and slides; use another aspect ratio when the requested medium requires it. Transform key judgments, processes, structures, states, or metaphors into clean, quirky, creative, and readable hand-drawn visuals that do not look like instruction manuals or generic commercial illustrations.

The default visual IP is Yuki, the Polar Bear Inventor: a compact off-white polar bear with a fluffy rounded-square silhouette, confident deadpan face, and one backward deep-red cap. Yuki is curious, capable, understated, and slightly mischievous. Whenever a scene has a core action, Yuki must perform it rather than stand aside as decoration. For profile or identity images without a narrative action, make Yuki the clear focal subject.

## Read These References First

Read as needed for the task; don’t overload yourself with context all at once:

- `references/style-dna.md`: Style DNA, colors, text, and don’ts.
- `references/yuki-ip.md`: Yuki character lock, personality, action library, reference-image rules, and don’ts.
- `references/composition-patterns.md`: Composition types, original metaphor techniques, and repetition rules.
- `references/prompt-template.md`: Prompt template for single-image generation.
- `references/qa-checklist.md`: Post-generation review and iteration rules.
- `assets/examples/`: Use only for low-frequency visual calibration; do not include in the default generation workflow. Do not copy the compositions, objects, or annotations from these examples verbatim.

## Workflow

### 1. Digest the Content

First, read the text, links, Notion pages, Markdown files, or screenshots provided by the user. Distill the following:

- What is the core idea?
- Which parts mark cognitive shifts?
- Which content is suitable for visual explanation?
- Which parts are best suited for text alone and do not require visuals?

Don’t distribute visuals evenly. Prioritize “cognitive anchors,” such as: core conclusions, two breaking points, input-output loops, branching paths, before-and-after comparisons, multiple uses of a single concept, follow-up paths, common pitfalls, and changes in character status.

### 2. Develop a Visualization Strategy First

If the user simply asks, “Analyze how to incorporate visuals / Consider where visuals are needed,” start by providing a shot list. For each image, clearly specify:

- Which paragraph it follows
- The image’s theme
- The core message
- The structural type
- What Yuki is doing in the image
- Recommended elements
- Recommended captions in the content's requested language

The default is 4–8 images. For very short articles, use 1–3; for long articles, don’t exceed 9 unless absolutely necessary. Use just enough—avoid turning the main text into a picture book.

### 3. Generating Individual Images

If the user explicitly requests “Generate / Output / Create an image / Help me generate,” do not pause to wait for confirmation. Use the available image-generation tool to generate each image separately; when running in Codex, prefer the built-in `image_gen` tool. Do not combine multiple requested images into a single image unless the user specifically requests a character sheet, storyboard, comparison, or contact sheet.

Choose the execution path based on the available capabilities:

- **Image generation with reference-image support:** Generate the image and always include `assets/character-reference/yuki-master-model-sheet.png` as the identity/model-sheet reference. This is the single source of truth for Yuki. Do not substitute an example image or the legacy reference.
- **Image generation without reference-image support:** Generate the image after copying the complete locked character description from `references/yuki-ip.md` into the prompt. Identity consistency may be lower, but do not burden the user with implementation details unless the result visibly drifts.
- **No image-generation capability:** Do not claim that an image was generated. Deliver a production-ready prompt using `references/prompt-template.md`; when the request involves multiple visuals or content analysis, also provide the shot list described in Step 2.

Each image should focus on only one core structure. The prompt must include:

- The aspect ratio and medium requested by the user; default to a 16:9 landscape body image or presentation visual
- Pure white background
- Black hand-drawn line art
- A small number of brief red/orange/blue handwritten annotations in the requested language
- Ample white space
- The locked Yuki as the central subject performing the action
- No PowerPoint slides, commercial illustrations, childish/cute styles, complex structures, or top-left corner-style titles

Before every generation containing the character:

- Read `references/yuki-ip.md` and copy its locked character description into the prompt.
- Include `assets/character-reference/yuki-master-model-sheet.png` as the character reference whenever the image tool supports reference inputs. Supplying the master sheet is mandatory when reference inputs are available.
- Treat the reference as an identity/model-sheet reference, not as a composition to copy.
- State that character identity has higher priority than scene complexity, pose novelty, or decorative detail.
- Select the closest pose on the master sheet as the anatomical starting point, then change only the limbs and posture needed for the requested action.
- Preserve the bear's face, proportions, cap construction, palette, and line style; vary only pose, action, expression within the allowed range, framing, and scene objects.
- Never use images under `assets/examples/` as character references; they contain historical variation and are for composition calibration only.

Do not replicate past examples. Examples are provided only to demonstrate style density, white space, color restraint, and how the recurring character participates in the concept. Existing compositions such as “conveyor belt breakpoints,” “pulling a string,” “material fish,” “stamp toolbox,” or “common pitfalls” must not be directly reused unless the user explicitly requests a replica. Reinvent a strange but valid metaphor for the current content.

### 4. Review and Iteration

Before presenting or saving a generated image, compare Yuki against `assets/character-reference/yuki-master-model-sheet.png` and apply the Character Identity Gate in `references/qa-checklist.md`. A failed identity gate is a rejected generation, not an acceptable variation. Regenerate before reviewing the broader composition.

After the identity gate passes, review the rest of `references/qa-checklist.md`. If any of the following issues arise, prioritize regenerating or making minor edits:

- Yuki is merely decorative
- The bear's face, body proportions, cap, or palette drift from the reference sheet
- The composition is too cluttered
- It looks too much like a flowchart or PowerPoint slide
- Too much text or severe typos
- Titles such as “Common Pitfalls,” “Flowchart,” or “System Architecture Diagram” appear in the top-left corner
- The art style is too cute, childish, or stiff
- The background is not a clean white background

### 5. Save and Deliver

If the user is working within a project or workspace, save the final image under that active workspace:

```text
<active-workspace>/assets/<article-slug>-illustrations/
```

Resolve this output path against the user's active project or workspace, not against the installed skill directory. Never save generated deliverables inside the skill package unless the user explicitly requests it.

Name the files in sequence:

```text
01-topic-name.png
02-topic-name.png
```

Keep the original generated files; do not overwrite existing assets unless the user explicitly requests a replacement.

## Delivery Guidelines

Pre-generation briefs should be short and precise. Post-generation deliverables must include:

- Number of images generated
- Purpose of each image
- Save path
- Which images are essential and which are optional

When generation is unavailable, replace the post-generation deliverable with the production-ready prompt or shot list and clearly label it as ready for use in an image-generation tool.

Avoid lengthy explanations of stylistic theory; let the images speak for themselves.
