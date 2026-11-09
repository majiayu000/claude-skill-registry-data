---
name: godot-build-shaders
description: Author Godot shaders and materials for the selected renderer with explicit resource ownership and target GPU budgets.
engines: [GODOT]
---

# Godot Build Shaders

## When to use

Author Godot shaders and materials for the selected renderer with explicit resource ownership and target GPU budgets. Apply this feature only to Godot-owned code and content.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh godot-build-shaders` before edits or tool launches. Continue only when the effective engine is `GODOT` and the skill is eligible. Skill selection never selects the engine. Honor validated task override evidence and its permitted isolated output scope.

Record exact Godot version, Forward+/Mobile/Compatibility renderer, target graphics platforms, project language for adapters, material conventions and texture/GPU budgets. Feature support must match the selected renderer.

## Workflow

1. Choose the correct shader type, including spatial, canvas_item, particles or sky as applicable. Declare render modes and pipeline stages intentionally; do not paste 3D shading assumptions into 2D canvas output.
2. Inspect UVs, normals, tangents, texture color semantics and import flags before authoring ShaderMaterial or selected visual shaders. Preserve source texture rights and record conversions.
3. Define uniforms and bounded runtime updates. ShaderMaterial resources can be shared; duplicate intentionally for per-object mutation or use supported instance uniforms on eligible nodes instead of changing every instance accidentally.
4. Implement transparency, depth, culling, shadows and screen/depth texture usage according to renderer/version support. Document requirements and approved alternatives rather than silently changing renderers.
5. Keep procedural motion and displacement inside declared bounds used by visibility/collision. Visual deformation must not independently decide collision or authoritative gameplay outcomes.
6. Measure overdraw, pass count, texture memory and shader cost on representative content. Quality tiers must retain silhouettes, required cues and accessible alternatives.
7. Release transient material/resources and restore owned parameters on interruption or scene exit. An effect must not leave shared global or resource state changed for unrelated objects.

## Verification

- Compile and inspect actual Godot output on the selected renderer; test close/far/grazing views and relevant lighting/backgrounds.
- Test shared versus per-instance parameters, resize and renderer-specific screen/depth effects, then run a target export.
- Capture target GPU/frame evidence and texture memory; headless shader parsing or source inspection cannot prove visual output.

## Output

Shader/material resources, import and uniform ownership rules, renderer compatibility notes, visual comparisons and target GPU measurements. Record environment, scope, expected and observed results, evidence paths, and blocked or not-run checks separately from passes.

## Boundaries

Do not switch renderers, add native shader plugins or assume Forward+ features work in Compatibility. Runtime parameter code follows the chosen project language. Independent services and tools retain their architecture contracts.

## References

- [Godot shading reference](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/index.html). Select the documentation matching the project release.
- [Godot ShaderMaterial](https://docs.godotengine.org/en/stable/classes/class_shadermaterial.html). Select the documentation matching the project release.

