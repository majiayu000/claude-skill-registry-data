---
name: thalarch-visual-qa
description: >
  Performs evidence-first visual QA for images, generated assets, screenshots,
  branding, image edits, diagrams, and implemented web/mobile UI. Use after any
  visual deliverable or when comparing a result with a reference/baseline. Verifies
  pixels and metadata rather than trusting prompts, source code, or creator reports,
  with a light aesthetic polish check for professional visual work.
---

# Thalarch Visual QA

The final pixels are the source of truth for visual claims.

## 1. Derive a visual checklist

Convert the user's visual requirements into checks such as:

- required subject/content;
- composition/framing;
- exact text;
- style/brand match;
- palette;
- dimensions/aspect ratio;
- alpha/transparency;
- crop/safe zones;
- elements that must be absent;
- invariants preserved from the baseline;
- responsive/runtime states.

Use `PASS`, `FAIL`, `UNVERIFIED`.

## 2. View the whole artifact first

Before zooming into details, inspect:

- hierarchy;
- balance;
- focal point;
- crop;
- readability;
- contrast;
- overall visual coherence;
- whether it obviously violates the requested direction.

For polished/professional work, also ask whether there is any obvious visual weakness that would
benefit from one small targeted improvement: weak focal hierarchy, awkward spacing/crop, unnecessary
clutter, or a brand/reference mismatch.

Do not turn this into a style blacklist. Gradients, glow, symmetry, bokeh, dramatic lighting, 3D,
minimalism, or decorative effects are valid when they work for the image.

Then inspect details.

## 3. Mechanical image probes

Use the bundled read-only scripts when relevant:

```text
python scripts/image_probe.py <image>
python scripts/image_compare.py <baseline> <candidate> --out <diff.png>
```

They can prove properties such as dimensions, format, alpha, and same-size pixel
change statistics. They cannot decide whether the design is beautiful.

## 4. Exact text

If exact visible copy matters:

- read the rendered text from the image itself;
- compare character-for-character with the required copy;
- inspect line breaks when layout matters;
- flag extra or hallucinated text.

Do not infer text accuracy from the generation prompt.

## 5. Image-edit preservation

For "change only X" edits:

1. compare against the original;
2. inspect requested region;
3. inspect several supposedly unchanged regions;
4. use a visual diff when dimensions align;
5. distinguish intended global effects from collateral drift.

Check for unintended changes to:
- identity;
- pose/geometry;
- framing;
- background;
- lighting;
- color grading;
- text/logo;
- texture/sharpness.

## 6. Artifact quality

Inspect for common generative/editing failures when relevant:

- malformed anatomy;
- duplicated objects;
- warped geometry;
- broken perspective;
- fake/garbled typography;
- halos and bad masks;
- inconsistent lighting/shadows;
- seams from compositing;
- unintended watermarks/logos;
- compression/upscale artifacts;
- banding;
- transparent-edge contamination.

Do not mechanically hunt for every category if it does not apply.

## 7. Brand review

For brand assets compare against the actual brand contract:

- mark integrity;
- color roles;
- typography character;
- spacing/safe area;
- shape language;
- imagery treatment;
- recognizability at small size.

Novelty is not automatically brand consistency.

## 8. Web/UI visual QA

For implemented UI, pair this skill with real browser/device evidence.

Compare screenshots against:
- design-system contract;
- reference/mockup if present;
- compact and desktop layouts;
- hover/focus/open states where visually meaningful;
- long text/empty/error states when relevant.

Check:
- hierarchy;
- rhythm;
- clipping;
- alignment;
- responsive reflow;
- image crops;
- typography;
- contrast;
- obvious accessibility regressions.

A generated mockup is not evidence of the implemented UI.

## 9. Annotated findings

When a visual defect is hard to describe precisely, create an annotated copy of
the screenshot/image with numbered callouts. Keep the original untouched.

Use the annotation only as evidence; fixes must target the actual source asset or
implementation.

## 10. Convergence rule

When a candidate fails:

- identify the smallest visual delta required;
- preserve all already-passing constraints;
- request one targeted edit pass;
- re-run only checks invalidated by that change plus a whole-image sanity check.

Do not restart the creative direction for a local defect. If the image is already strong and meets
the contract, a clean PASS is preferred over needless regeneration.

## Output

Return:

`Requirement | PASS / FAIL / UNVERIFIED | Evidence`

Then separate:
- blocking defects;
- optional polish;
- exact next edit, if another pass is necessary.

A clean pass is valid. Do not manufacture criticism.
