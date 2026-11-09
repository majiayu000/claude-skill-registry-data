---
name: unity-build-materials
description: Author Unity materials and shaders for the selected render pipeline with explicit variants, import settings, and GPU budgets.
engines: [UNITY]
---

# Unity Build Materials

## When to use

Author Unity materials and shaders for the selected render pipeline with explicit variants, import settings, and GPU budgets. Use this feature only for Unity-owned project code and assets.

## Activation and prerequisites

Run `commands/resolve-engine.sh` and `commands/resolve-skill.sh unity-build-materials` before edits or tool launches. Continue only when the effective engine is `UNITY` and this skill is eligible. A requested skill never selects its engine. Honor the resolved task override evidence and permitted output scope when an isolated prototype is selected.

Identify exact Unity version, Built-in/URP/HDRP selection, renderer settings, target graphics APIs, color space, lighting mode, texture budgets and shader-authoring approach. Match installed pipeline and Shader Graph package versions.

## Workflow

1. Audit material slots, mesh attributes, texture semantics and import settings before editing shaders. Verify normal map interpretation, sRGB versus linear data, alpha mode and tangent conventions against source art.
2. Use the selected pipeline's supported shader path: ShaderLab/HLSL, Shader Graph or an existing authored shader. Read [shader authoring and variants](references/shader-authoring.md) for graph targets, custom functions and reflected node APIs. Renderer configuration and explicit pipeline migrations belong to the rendering owner.
3. Choose opaque, cutout or blended rendering from visibility requirements. Record depth writes, sorting, shadow behavior, double-sided cost and overdraw rather than fixing artifacts through arbitrary queue changes.
4. Own material lifetime explicitly. Understand sharedMaterial versus per-renderer material instances; use MaterialPropertyBlock where appropriate to avoid unbounded instance creation while checking compatibility with the project's batching strategy.
5. Define bounded keywords, variants and runtime parameter updates. Retain required variants for player builds and test stripping behavior instead of relying only on Editor preview compilation.
6. Implement effects against project GPU and memory budgets, including texture sizes, mipmaps, sampler use, vertex cost and transparency. Quality tiers must preserve gameplay readability and accessible cue alternatives.
7. Use representative lit scenes and the selected render backend to compare output, then document any unsupported platform feature with an explicit approved fallback.

## Verification

- Compile in the actual Editor and selected player target, checking shader errors, pink materials, stripped variants and graphics API differences.
- Review close, distant and grazing-angle views under relevant lighting; test instancing/batching, alpha edges and texture streaming behavior.
- Use Frame Debugger and target-device profiling for draw calls, overdraw and GPU cost; screenshots alone do not establish frame budgets.

## Output

Materials/shaders and import changes, pipeline/version compatibility notes, variant and resource ownership policy, reference captures and target GPU measurements. Record environment, expected and observed results, evidence paths, and blocked or not-run checks separately from passes.

## Boundaries

Do not silently change render pipelines, download art or add effect middleware. A headless or non-graphics run cannot certify visual shader correctness. Engine guidance applies to engine-owned code; independent services retain their architecture contracts.

## References

- [Unity render pipelines](https://docs.unity3d.com/6000.0/Documentation/Manual/render-pipelines.html). Use the documentation matching the installed project version.
- [MaterialPropertyBlock](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/MaterialPropertyBlock.html). Use the documentation matching the installed project version.

