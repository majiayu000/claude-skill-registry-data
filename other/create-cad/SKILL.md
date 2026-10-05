---
name: create-cad
description: Create and validate one dimensioned parametric CAD part, returning STEP as the primary artifact rather than a render-only image. Use for manufacturable mechanical geometry with explicit dimensions and constraints; do not use for concept renders, floor plans, architecture, diagrams, or artistic 3D imagery.
---
# Create CAD

## Catalog

- Display name: Create CAD
- Categories: Layout & Design, Utility
- Status: Ready
- Route label: STEP-first parametric CAD workflow
- Tone: slate
- Short description: Create and validate one parametric CAD part, returning STEP as the primary artifact rather than a render-only image.

## What this skill does

- Builds dimension-driven part geometry and exports a real STEP model with reproducible source.
- Inspects bounding box, volume, topology and named features; preview imagery is secondary evidence.

## How to use

Provide units, dimensions, functional features, tolerances, references and required exports.

#### Example

```text
Create a STEP-first L bracket: 80×50×5 mm, two 6 mm base holes, one 8 mm upright slot, 3 mm fillets.
```

## Workflow

1. Extract a unit-explicit feature specification and flag missing functional dimensions.
2. Create reproducible parametric source with a STEP-capable kernel; never fake CAD with an image model.
3. Export STEP first, then optional mesh formats; render preview only from generated geometry.
4. Re-open STEP and verify dimensions, bounding box, volume, features and manifold geometry.

## User-facing output

- Media type: One STEP model plus preview
- Default quantity: 1
- Content per image: One validated parametric part
- Default layout: Source-preserving or dimension-defined format
- Model policy: STEP-first parametric CAD workflow
- Downstream use: Mechanical design handoff, not engineering certification
