---
name: unreal-build-materials
description: Author Unreal materials and instances with selected rendering features, bounded shader permutations, and target GPU verification.
engines: [UNREAL]
---

# Unreal Build Materials

## When to use

Author Unreal materials and instances with selected rendering features, bounded shader permutations, and target GPU verification. Use this feature for Unreal-owned game code and content.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh unreal-build-materials` before edits or tool launches. Continue only when the effective engine is `UNREAL` and `compatible: true`. Skill selection never selects the engine. Honor any validated task override and its permitted isolated output scope.

Read Unreal version, rendering path, target feature levels/RHIs, material/shader budgets, texture conventions and selected advanced features. Do not assume desktop rendering capabilities on mobile or change project shading settings implicitly.

## Workflow

1. Inspect mesh attributes, material slots, texture imports and source art intent. Define texture color semantics, normal/tangent conventions, UV channels and physical response before changing the graph.
2. Author actual Material and Material Instance assets using the supported Editor workflow. Choose blend mode, shading model, domain and sidedness deliberately; these affect passes, shadows, lighting and platform support.
3. Expose bounded parameters and choose static switches only where variants justify compilation/cook cost. Use Material Instance Constants for authored variation and owned Dynamic Material Instances for runtime values.
4. Keep material updates lifecycle-bound and avoid creating a fresh dynamic instance every tick. Shared parameter collections require a world-level owner so local effects cannot overwrite unrelated actor state.
5. Evaluate translucency, masked edges, world-position offset, depth and post-process effects against readability and visibility requirements. Renderer-specific features need explicit target support and a reviewed quality alternative.
6. Profile shader complexity, overdraw, texture streaming, draw calls and memory on representative content. Set measured platform material/LOD budgets rather than relying only on Editor shader preview.
7. Compile and cook the selected targets, inspect warnings and retain required permutations. Missing shaders or unsupported feature levels must fail the acceptance check rather than becoming an undocumented fallback.
8. Read the [material production reference](references/material-production.md) for parameter API ownership, deformation bounds, Substrate/virtual-texture selection and reproducible GPU comparisons.

## Verification

- Review lit/unlit diagnostics, close/far/grazing views, shadow behavior and representative lighting conditions in real Unreal.
- Test runtime parameter restoration, shared-versus-owned instances and scene transitions for unintended cross-object changes.
- Capture target GPU metrics and packaged material output; NullRHI or headless compilation does not prove visual correctness.

## Output

Native material/instance assets, parameter ownership and permutation policy, platform compatibility notes, comparison captures and GPU budget evidence. Record environment, scope, expected and observed results, evidence paths, and blocked or not-run checks separately from passes.

## Boundaries

Do not adopt optional shading systems, marketplace assets or plugins without selection. Native material graphs require genuine engine authoring and validation. Independent tools and services retain their own architecture contracts.

## References

- [Unreal materials](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-materials). Match the documentation version to the project.
- [Material instances](https://dev.epicgames.com/documentation/en-us/unreal-engine/instanced-materials-in-unreal-engine). Match the documentation version to the project.
- [Material production](references/material-production.md): rendering assumptions, runtime parameters and measured acceptance.

