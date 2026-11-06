---
name: paint
description: Create realistic painted surfaces with Three.js TSL on WebGPU. Use for trains, vehicles, signs, buildings, machinery and architecture.
---

# Paint

Target: Three.js 0.187.0, `three/webgpu` and TSL node materials from `three/tsl`; WebGPU only, no WebGL fallback, no GLSL strings.

Treat paint as a layered surface rather than a single colour.

## Layers

Conceptually:

substrate -> primer -> paint -> protective/clear layer -> wear/dirt

Not every object needs every layer explicitly, but the shader should model the important optical consequences.

## Controls

Consider:

- base colour
- roughness
- specular
- clearcoat
- clearcoat roughness
- fine surface normal
- colour variation
- fading
- scratches
- edge wear
- dirt

## Automotive/train paint

Painted train bodies can use a smooth coloured coating with moderate clearcoat and subtle roughness variation.

Avoid mirror-like paint unless the object is intentionally polished.

## Wear

Wear should be spatially meaningful:

- edges
- handles
- door areas
- maintenance access
- exposed lower sections
- high-contact surfaces

Scratches can expose primer or substrate where appropriate.

## Dirt

Dirt should accumulate in:

- seams
- recesses
- lower panels
- joints
- underbody areas

Do not apply uniform brown/grey noise.

## Signs

Painted signage should retain crisp lettering while allowing the sign substrate to age separately.
