---
name: visual-reference-to-code
description: "Turn a screenshot, generated design reference, or visual brief into a polished responsive interface through measurable visual analysis, implementation, and screenshot comparison. Use when the user asks for this reference-driven workflow or needs a detailed visual-fidelity pass without replacing the installed image-to-code skill. Turkish triggers: ekran görüntüsünü veya tasarımı koda çevir, görsel referanstan arayüz yap."
---

# Image to Code

Create interfaces from visual evidence, not generic UI defaults. Preserve the existing project's stack and design system, then close the gap with rendered comparisons.

## Entry Modes

Choose the lightest mode that fits the request:

1. **Reference recreation** — the user supplied screenshots or a design. Do not generate a replacement; analyze the supplied source.
2. **Image-first exploration** — the user wants a new visually ambitious design and an image-generation tool is available. Generate focused references before coding.
3. **Brief-to-code** — no visual tool is available or the task is mostly structural. Build from a written art-direction brief, then render and refine.

Never claim an image was generated or inspected unless the active host actually provided that capability and the image was viewed.

## Guardrails

- Inspect the repository, framework, routes, components, tokens, assets, and tests before editing.
- Preserve requested content, brand, accessibility, and functionality. A reference image is not permission to copy third-party trademarks or copyrighted assets.
- Do not add packages, fonts, paid assets, analytics, or external image services without authorization.
- Do not overwrite unrelated work. Keep changes small and reversible.
- Use placeholders only when the source asset is unavailable, and label them.
- Treat text rendered inside generated design images as visual scaffolding; use real HTML text in the implementation.

## 1. Define the Visual Contract

Capture:

- target route/component and viewport priorities;
- audience and primary action;
- content hierarchy and required copy;
- brand constraints and existing design tokens;
- reference assets and their permitted use;
- acceptance criteria: fidelity, responsiveness, interaction, accessibility, performance.

Write a compact direction before generating or coding:

```text
Mood:
Composition:
Typography:
Color/material:
Hero focus:
Section rhythm:
Motion:
Avoid:
```

Do not default to centered dark heroes, endless cards, nested rounded containers, tiny pills, glassmorphism, or repeated left-text/right-image sections unless the brief supports them.

## 2. Create or Select References

### Supplied reference

Use the highest-resolution source available. Inspect it directly. If several screenshots describe different breakpoints or states, map each one.

### Generated reference

Generate only when it materially reduces design ambiguity. Prefer one readable full-page direction plus separate high-resolution references for visually dense sections. Do not squeeze many sections into a tiny contact sheet.

The generation prompt should specify:

- page type and real content hierarchy;
- viewport/aspect ratio;
- grid, spacing, section count, and focal point;
- typography character without requesting unlicensed font replicas;
- palette, material, lighting, illustration/photo direction;
- practical controls and states;
- what to avoid;
- no device mockup, browser chrome, watermark, or illegible microcopy unless explicitly wanted.

Generate a small number of meaningfully different options. Select against the contract; do not generate variants indefinitely.

## 3. Analyze Before Coding

Extract measurable evidence:

| Layer | Record |
|---|---|
| Canvas | viewport, max width, margins, fold |
| Grid | columns, gutters, alignment anchors |
| Type | hierarchy, approximate sizes, line lengths, weights |
| Spacing | recurring increments, section gaps, density |
| Color | background/surface/text/accent roles and contrast |
| Shape | radii, borders, shadows, dividers |
| Media | aspect ratios, crop behavior, focal points |
| Interaction | hover, focus, active, expanded, loading, error |
| Responsive | elements that stack, hide, reorder, or resize |

Separate facts from inference. Do not invent invisible interactions or exact pixel values. Use a consistent token set derived from recurring patterns.

## 4. Map the Implementation

Identify:

- reusable page shell and section boundaries;
- semantic HTML landmarks;
- data-driven repeated content;
- existing components to reuse or extend;
- assets to create, optimize, or substitute;
- responsive breakpoints based on layout failure, not arbitrary device names.

Keep component boundaries aligned with real behavior and reuse. Avoid one component per decorative fragment and avoid one monolithic page component.

## 5. Implement Fidelity in the Right Order

1. semantic structure and content;
2. page width, grid, section rhythm, and fold;
3. typography and color tokens;
4. media sizing and crop behavior;
5. controls, states, and accessibility;
6. decorative details and motion.

Use CSS variables or the project's token system for repeated values. Keep motion optional and respect `prefers-reduced-motion`. Maintain visible keyboard focus, logical tab order, usable hit targets, sufficient contrast, correct labels, and meaningful alt text.

For generated imagery, use the actual asset file and preserve a stable local reference. Do not crop a low-resolution overview into section art when a dedicated asset is needed.

## 6. Render, Compare, Correct

Use the project's test/browser tooling to capture the implementation at target viewports. Compare side by side with the source.

Correct in this order:

1. layout geometry and missing content;
2. typography scale and wrapping;
3. spacing and alignment;
4. color/contrast and media crop;
5. borders, shadows, radii, and micro-interactions.

Run at least one narrow mobile and one desktop viewport when the interface is responsive. Test overflow, long text, keyboard navigation, reduced motion, loading/error/empty states, and console errors where relevant.

Do not stop at "looks close." Record remaining mismatches and why they are acceptable or blocked.

## Completion Report

Report:

- entry mode and source references used;
- files changed and assets added;
- viewports and states checked;
- build/typecheck/test results;
- accessibility and performance checks;
- deliberate deviations and unresolved asset/licensing issues.

## Quality Gate

- [ ] The source was actually inspected or the lack of a visual tool was stated.
- [ ] The design follows a coherent visual contract instead of generic patterns.
- [ ] Layout, type, and spacing were measured before detail polishing.
- [ ] The implementation preserves the project stack and design system.
- [ ] Mobile, desktop, keyboard, and reduced-motion behavior were checked.
- [ ] Final screenshots were compared with the source and mismatches were addressed.
