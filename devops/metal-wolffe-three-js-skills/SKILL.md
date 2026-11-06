---
name: metal
description: Create realistic procedural metal materials with Three.js TSL on WebGPU. Use for trains, rails, machinery, structures, vehicles, pipework and industrial infrastructure.
---

# Metal

Target: Three.js 0.187.0, `three/webgpu` and TSL node materials from `three/tsl`; WebGPU only, no WebGL fallback, no GLSL strings.

## Physical categories

Distinguish:

- painted metal
- bare aluminium
- stainless steel
- polished steel
- cast iron
- machined metal
- brushed metal
- galvanised metal
- oxidised metal
- weathered structural steel

Do not use one generic metallic material for everything.

## Core response

Control:

- metalness
- roughness
- specular response
- base colour
- normal variation
- anisotropy where appropriate
- clearcoat only when a coating physically exists

Brushed metal should have directional anisotropic response.

## Surface variation

Use subtle procedural variation for:

- machining marks
- brushing
- fine scratches
- oxidation
- dirt
- fingerprints
- edge wear

Variation should be correlated with physical causes.

## Wear

Exposed edges can show more wear. Recesses can accumulate dirt. High-contact areas can become polished. Horizontal exposed surfaces can collect deposits.

Do not apply uniform random noise.

## Scale

Large structural metal should have broad, restrained variation. Close-up machined components can have finer detail.

## Train/rail guidance

Train exterior: usually coated/painted metal rather than bare metal.

Rails: steel with directional wear, polishing and environmental oxidation.

Underbody: darker, rougher, dirtier metal with higher variation.
