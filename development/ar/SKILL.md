---
name: ar
description: Augmented reality (AR) reality tech. Passthrough overlays, hit-test/anchors, occlusion, lighting, camera permissions, and safety.
license: Apache-2.0
metadata:
  trit: 0
  version: "1.0.0"
  bundle: reality-tech
---

# AR (Augmented Reality)

Use when the user is building AR on WebXR (immersive-ar) or native (ARKit/ARCore/OpenXR).

## Fast Defaults

- Prefer stable world-locked content; avoid screen-locked UI unless necessary
- Use clear permission prompts and visible camera-on indicators
- Start with: hit-test + placement + anchors + simple interaction

## AR Capability Checklist

- Plane / mesh detection
- Hit-test (placing content onto surfaces)
- Anchors (persistent placement)
- Occlusion (depth) and lighting estimation if available
- Safety boundaries (keep critical UI in view, avoid distraction)

## Debug Checklist

- Confirm session type (WebXR `immersive-ar`) or native runtime
- Verify tracking origin and world scale (1 unit = 1 meter)
- Confirm anchor lifetimes and relocalization handling

See also: `ar-vr-xr` for the full workflow and shared performance/comfort guidance.
