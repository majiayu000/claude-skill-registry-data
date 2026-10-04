---
name: thalarch-image-to-code
description: >
  Visual-fidelity workflow for translating screenshots, generated design references, mockups, or
  section comps into real frontend code. Use when matching a visual reference is central to
  acceptance. Extracts a measurable design contract before implementation and verifies the real
  browser result rather than treating the reference image or source code as proof.
---

# Thalarch Image to Code

Use this skill when **visual fidelity to an image/reference is a primary requirement**.

Do not force image-first design onto bug fixes, purely structural frontend work, or projects that
already provide a precise approved design system and implementation spec.

## 1. Classify every reference

Label each input before using it:

- `TARGET` — the implementation is expected to match this reference;
- `STYLE` — palette/typography/atmosphere inspiration only;
- `CONTENT` — image/asset that must be integrated;
- `BASELINE` — current implementation before redesign;
- `DETAIL` — closer reference for a section/component;
- `GENERATED CONCEPT` — a design proposal, not yet an approved implementation contract.

Never silently turn a moodboard/style image into an exact layout target.

## 2. Decide whether new design references help

When the user wants an open-ended, visually exceptional new site and image generation is available,
a visual-director pass may create section-level concept references before implementation.

Generate only when it materially improves art direction or extraction. Do not generate a mockup just
because the tool exists.

For multi-section concepts, prefer references large enough to inspect. If one giant board makes
text, spacing or components unreadable, create separate section/detail references rather than
shrinking everything into a collage.

Do not crop a tiny section from an unreadable board and call it a precise reference. When a detail
is ambiguous, create or request a clearer dedicated reference while preserving the same design
language.

## 3. Deep extraction before code

Treat the reference as evidence, not as a vibe.

Extract a compact **visual contract**:

- viewport/aspect assumptions;
- content hierarchy and section order;
- visible text/copy that is actually legible;
- typography character and relative scale;
- line breaks/wrapping/alignment;
- container/gutter/grid geometry;
- whitespace and section rhythm;
- component shapes/radii/borders;
- buttons/control hierarchy and visible states;
- palette and semantic roles;
- imagery crop/mask/treatment;
- icons and stroke/fill language;
- depth/shadow/texture/material;
- repeated motifs;
- responsive behavior that can be inferred vs behavior that remains unknown.

Mark observations `FACT`, `INFERENCE`, or `UNKNOWN` when precision matters.

If a critical detail is unreadable, do not invent it and later claim fidelity.

## 4. Reconcile with the real project

Before implementation inspect:

- current framework and versions;
- existing design tokens/components;
- fonts/assets already licensed/available;
- styling system;
- responsive breakpoints/conventions;
- accessibility requirements;
- existing behavior that must not be broken.

The target image does not authorize a framework rewrite or replacement of functional behavior.

If the reference conflicts with accessibility, product requirements, or a locked existing behavior,
resolve the conflict explicitly instead of blindly reproducing pixels.

## 5. Build from system → sections → details

Implement in an order that preserves coherence:

1. semantic tokens / type / containers;
2. page composition and major sections;
3. reusable components;
4. imagery and visual treatments;
5. responsive recomposition;
6. interactions/states;
7. detail polish.

Do not independently tune every section until each has a different spacing/radius/type language.

## 6. Fidelity checkpoints

Do not wait until the whole page is finished to inspect it.

At meaningful milestones:

- render the real page;
- capture a screenshot at the target viewport when browser tooling is available;
- compare to the reference/visual contract;
- identify the largest mismatch first;
- fix layout/hierarchy before micro-polish;
- rerender after material fixes.

Prioritize mismatch categories:

1. composition/section geometry;
2. typography/line wrapping;
3. spacing/alignment;
4. colors/material;
5. imagery crop;
6. component details;
7. micro-effects.

## 7. Responsive translation

A desktop reference rarely specifies mobile completely.

For each major element decide:

- preserve;
- stack;
- reorder;
- crop/reframe;
- collapse;
- replace interaction;
- hide only when content priority justifies it.

Verify at least compact and desktop sizes. If the reference is only one viewport, responsive choices
are design inferences and should be judged by the design contract rather than fake pixel parity.

## 8. Visual diff discipline

When deterministic screenshot comparison tooling exists, use it as a measurement aid.

Pixel diffs can identify drift but do not understand intent. Font rasterization, browser engines,
anti-aliasing and dynamic content can create harmless differences.

Combine diff evidence with independent visual review.

Do not claim “pixel perfect” unless the environment/reference actually supports that level of
repeatability and the measured tolerance is stated.

## 9. Image asset integration

When generated/custom artwork is part of the reference:

- review the asset independently before integration;
- preserve focal point across responsive crops;
- use correct dimensions/format/compression;
- provide meaningful alt behavior;
- do not substitute a low-resolution reference crop as the production asset.

## 10. Completion gate

A reference image, generated concept, or passing frontend build is not final evidence.

Completion requires, when tooling permits:

- real implemented page screenshots;
- target/reference side-by-side or measured comparison;
- compact + desktop review;
- primary interaction check;
- independent design/visual review;
- accessibility/runtime checks appropriate to the project.

Report remaining visual unknowns as `UNVERIFIED`.
