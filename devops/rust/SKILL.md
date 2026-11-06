---
name: rust
description: Create realistic procedural rust, oxidation and corrosion with Three.js TSL on WebGPU. Use for rails, exposed steel, machinery, pipes, bridges, containers, ships and old infrastructure.
---

# Rust and Corrosion

Target: Three.js 0.187.0, `three/webgpu` and TSL node materials from `three/tsl`; WebGPU only, no WebGL fallback, no GLSL strings.

Rust is a physical surface transformation, not merely an orange colour.

## Layer model

Think:

clean coating
-> scratched coating
-> exposed metal
-> oxidation
-> rust
-> heavier corrosion
-> pitting

The amount of each layer should be controlled by masks.

## Corrosion masks

Use plausible causes:

- exposed edges
- seams
- water traps
- damaged paint
- bolt interfaces
- joints
- lower sections
- drainage paths
- sheltered crevices

Avoid uniform procedural rust noise.

## Properties affected

Rust should influence several properties:

- base colour
- roughness
- normal
- specular response
- metallic response where appropriate

Heavily corroded regions should not retain the same smooth reflective appearance as pristine metal.

## Geometry vs shader

Use shader detail for small corrosion and surface variation.

Use actual geometry for major holes, deep flaking, broken edges and large missing material when it affects silhouette or close-up shape.

## Match corrosion to environment and maintenance

Corrosion should not automatically be extreme. Match it to the object's age, maintenance regime, humidity and exposure: a sealed, climate-controlled interior or a well-kept station shows little beyond scuffed edges and bolt stains; coastal, marine and abandoned settings show heavy rust, streaking and pitting.
