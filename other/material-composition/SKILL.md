---
name: material-composition
description: Combine realistic TSL materials into coherent multi-material objects in Three.js WebGPU scenes. Use when an object (vehicle, building, machine) is made of several physically distinct surfaces.
---

# Material Composition

Target: Three.js 0.187.0, `three/webgpu` and TSL node materials from `three/tsl`; WebGPU only, no WebGL fallback, no GLSL strings.

Complex objects should be composed from physically distinct surfaces rather than forced into one universal shader.

## Typical object composition

A train might contain:

- painted aluminium/steel body
- glass windows
- rubber seals
- polished or brushed metal components
- dark underbody metal
- plastic interior components
- lights/emissive elements

A building might contain:

- concrete
- painted steel
- aluminium
- glass
- rubber seals
- weathered surfaces
- interior materials

## Separation rule

If two parts have different physical construction, give them separate material treatment where useful.

Do not create dozens of materials for negligible differences.

## Shared material vocabulary

Prefer reusable material constructors and parameter sets.

For example:

createPaintMaterial({ color, roughness, wear })
createGlassMaterial({ tint, roughness, thickness })
createMetalMaterial({ type, roughness, wear })
createRustMaterial({ severity, moisture })

## Consistency

Materials should agree with the geometry. A recessed panel should have believable roughness and dirt behaviour; a rubber seal should not behave like painted metal; glass should not be treated as opaque plastic.

## Performance

Reuse material graphs and textures where possible. Use the expensive effects on hero objects and simplified variants for distant repeated assets.
