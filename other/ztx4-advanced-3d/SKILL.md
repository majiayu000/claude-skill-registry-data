---
name: ztx4-advanced-3d
description: "Deep implementation master for Advanced 3D / R3F / GPU with 33 targeted Codex skills, code, tests and no MCP. Additive to all existing Perfect_AI versions."
---

# Advanced 3D / R3F / GPU

Build real, bounded, device-aware 3D scenes with fallback and measurable GPU/resource behavior.

## Mandatory sequence
1. Define intended visual, camera framing, lighting and interaction in a scene contract.
2. Choose WebGL baseline; WebGPU is optional and requires installed-version and platform compatibility proof.
3. Budget triangles, draw calls, material variants, texture memory, overdraw, particle counts and shader iterations.
4. Provide low/medium/high quality tiers plus semantic non-WebGL content or image poster.
5. Dispose textures, geometries, controls, render targets and subscriptions; test resize, context loss and reduced motion.

## Skill routing
Choose only technique files needed for this project from `DEEP-IMPLEMENTATION-v2/references/advanced-3d.md`. Never indiscriminately load all 300+ skills into context.

## Runbook
Inputs: scene brief, geometry/asset rights, GPU tier assumptions, content and accessible fallback.

Implementation: prefer one R3F Canvas, useFrame delta clamp, stable geometry/material buffers; choose technique appropriate to GPU tier; bound shader steps and dispose resources.

Tests: WebGL2/no-WebGL, context loss, 320/390/1440px framing, reduced motion, renderer.info counters, assert no unbounded RAF allocation.

## Acceptance gates
1. No WebGL still presents important text, meaning and CTA.
2. Low GPU tier uses fewer geometry samples/passes/texture bytes and bounded frame budget.
3. Resize/unmount/context loss create no leaked buffers, RAF loops or subscriptions.

## Runnable assets
`extensions/DEEP-IMPLEMENTATION-v2/examples` and `tools` (installed main package). See `RUNBOOK-FA.md`.

## Sources
- [three](https://threejs.org/docs/)
- [r3f](https://r3f.docs.pmnd.rs/)
- [drei](https://drei.docs.pmnd.rs/)
- [wcag](https://www.w3.org/TR/WCAG22/)
