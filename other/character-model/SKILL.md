---
name: character-model
description: A procedural blocky humanoid for Three.js 0.187.0 WebGPU, built from boxes with hip, knee and shoulder joints, with a walk cycle, crouch and airborne poses driven by the walker's state. Use when a third-person character needs a visible body without model files. Ships character-model.js.
---

# Character model

Target: Three.js 0.187.0 WebGPU, `MeshStandardNodeMaterial`, flat shading. No model
files, no skinning, no animation clips: the figure is a small hierarchy of boxes and
the animation is three numbers per frame.

`scripts/character-model.js` exports `createCharacterModel(opts)` returning
`{ root, anchorHeight, height, setVisible, setTransform, update, setColors }`.

## Proportions

Everything is in studs of 0.3 m so the figure reads as a deliberate style, not a
failed realistic one.

| Part | Size (w × h × d) | Notes |
| --- | --- | --- |
| head | 1.25 × 1.25 × 1.25 studs | cube on the shoulders |
| torso | 2 × 2 × 1 studs | |
| arm | 1 × 2 × 1 studs | hangs from the shoulder joint |
| thigh, shin | 1 × 1 × 1 studs each | hip and knee joints |

Total height 6.25 studs = 1.875 m; the walker capsule is 1.8 m, so the head just
clears it. The orbit anchor is 45 % of the height from the feet (chest).

Joints are empty `Group`s at the shoulder line, the hips and the knees; the box meshes
hang below them so rotating a joint swings the limb from its top. The root's origin is
at the feet, on the ground.

## Animation

`update(dt, { speed, grounded, runSpeed })`, three numbers and a flag:

- **swing amplitude** eases toward `min(1, speed/runSpeed) × 0.85 rad` on the ground
  and toward 0 in the air, at 14 /s. Arms and legs swing in opposite phase; left and
  right in opposite phase.
- **phase** advances by `speed × 1.55 × dt`, so stride length is constant and the
  cadence follows speed. Nothing animates while standing.
- **lift** eases toward −1.1 rad when airborne: arms rise, legs trail. Landing eases
  back.
- **crouch** (0..1 from the walker's crouch blend): thighs rotate −0.62 rad, knees
  +1.15 rad, the torso tips 0.14 rad, arms 0.18 rad; the whole upper body drops by the
  planted-leg geometry so the feet stay on the ground. Swing is reduced by 30 %.
- A knee bends up to 0.45 rad extra on the trailing leg of each swing so the foot
  clears the ground.

That is enough to read as walking, running, jumping and sneaking from any distance
the camera uses.

## Placement

`setTransform(feetY, x, z, heading, crouchT)` once per frame from the walker:
feet at the capsule centre minus the capsule half height, heading from the wish
direction eased at 18 /s (the model turns to where it walks).

## Materials and colours

Three flat-shaded standard materials (shirt, skin, trousers) with roughness 1 and fog
enabled; `setColors({ shirt, skin, pants })` changes them. Flat shading keeps the box
edges crisp under any light. Keep the figure's materials shared across many figures:
with WebGPU, pipeline count is load time.

## Pitfalls

- Hide the model in first person; otherwise the camera sees the inside of the head.
- Do not scale the root for crouch; the pose handles it and keeps the feet planted.
- Cast and receive shadows on every box; a figure without a contact shadow floats.
