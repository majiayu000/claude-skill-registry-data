---
name: reference-synthesis
description: Combine multiple inspiration sources into an original product-specific direction using a reference matrix, required transformations, AIgent pattern mapping, and an influence ledger.
---

# Reference Synthesis

Use this after Design DNA exists for two or more references.

## Principle

One source may influence one or two design dimensions. It must not silently determine the whole site.

Dimensions:

```text
structure
 typography
 material
 motion
 interaction
 media
```

## Command

```bash
node scripts/inspire.mjs compose \
  --brief design-intelligence/example-brief.json \
  --refs source-a,source-b,source-c
```

Override an assignment only when the user has a clear reason:

```bash
--assign structure:source-a,typography:source-b,motion:source-c
```

## Required synthesis

For each dimension, record:

- source
- extracted principle
- required transformation
- excluded source expression
- target-product reason

Then map the result to the smallest existing AIgent systems and runtimes.

## Do not copy

- source copy, claims, logos, marks, icons, photographs, video, 3D models, or audio
- exact section order
- exact typography pairing and scale
- exact animation timing, keyframes, camera path, or transition sequence
- source HTML, CSS, JavaScript, shaders, or private implementation

## Completion

Before implementation, produce:

- `reference-matrix.json`
- `influence-ledger.json`
- `DIRECTION.md`
- mapped AIgent patterns
- original asset briefs
- mobile and reduced-motion transformations
- originality-audit threshold

The design should feel intentionally informed by several references and unmistakably authored for the target product.
