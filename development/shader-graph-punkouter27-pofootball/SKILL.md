---
name: shader-graph
description: "ShaderGraph — custom function nodes, sub-graphs, keyword-driven variants, master stack outputs, common patterns for URP effects."
globs: ["**/*.shadergraph", "**/*.shadersubgraph"]
---

# ShaderGraph

## Overview

ShaderGraph is Unity's visual shader editor. Node-based, works with URP and HDRP. Generates HLSL shader code from the graph.

## Master Stack Outputs

### Vertex Stage
- Position (object/world/absolute world)
- Normal (object/tangent)

### Fragment Stage (URP Lit)
- Base Color, Normal (Tangent), Metallic, Smoothness, Emission, Ambient Occlusion, Alpha

### Fragment Stage (URP Unlit)
- Base Color, Alpha

## Custom Function Nodes

### Inline (small functions)
```hlsl
// In Custom Function node, Type: String
void MyFunction_float(float3 In, out float3 Out)
{
    Out = In * 2.0;
}
```

### External File (complex functions)
Create `.hlsl` file in project:
```hlsl
// Assets/Shaders/MyFunctions.hlsl
void TriplanarMapping_float(
    float3 Position, float3 Normal, float Sharpness,
    UnityTexture2D Tex, UnitySamplerState Sampler,
    out float4 Color)
{
    float3 blend = pow(abs(Normal), Sharpness);
    blend /= dot(blend, 1.0);

    float4 xProj = SAMPLE_TEXTURE2D(Tex, Sampler, Position.yz);
    float4 yProj = SAMPLE_TEXTURE2D(Tex, Sampler, Position.xz);
    float4 zProj = SAMPLE_TEXTURE2D(Tex, Sampler, Position.xy);

    Color = xProj * blend.x + yProj * blend.y + zProj * blend.z;
}
```

Reference in Custom Function node: Source = Asset, File = MyFunctions.hlsl

## Keywords (Shader Variants)

- **Boolean Keyword:** toggle features on/off per material
- **Enum Keyword:** select between N options
- Use `shader_feature` (stripped if unused) not `multi_compile` (always included)
- Use `shader_feature_local` for material-only keywords

Keep total variant count **under 1000** per shader.

## Common Patterns

### Dissolve Effect
1. Sample noise texture (Gradient Noise or texture)
2. Compare noise value to "Dissolve Amount" property (Step or SmoothStep)
3. Multiply with Alpha output
4. Add emission at dissolve edge (edge = small range above threshold)

### Fresnel / Rim Lighting
1. Fresnel Effect node (View Direction, Normal)
2. Multiply by color
3. Add to Emission

### Scrolling UV (Water, Lava)
1. Time node → Multiply by scroll speed
2. Add to UV coordinates
3. Sample texture with modified UVs

### Vertex Displacement (Wind, Waves)
1. Object Position + Time → noise function
2. Multiply by displacement amount
3. Add to Vertex Position output

### Outline (Inverted Hull Method)
Two-pass: Pass 1 = normal render, Pass 2 = vertex-expanded back faces with solid color.
(Requires custom Renderer Feature in URP or ShaderGraph with two materials.)

## Sub-Graphs

Reusable node groups. Create for common operations:
- Triplanar mapping
- Tiling and offset with rotation
- Blend modes (overlay, multiply, screen)
- Parallax mapping

## Performance Tips

- Minimize texture samples per fragment
- Use `half` precision where possible (set in graph settings)
- Avoid branching (use lerp/step instead)
- Fewer keywords = fewer variants = faster build times
- Preview variant count in Shader Inspector
