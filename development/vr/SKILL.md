---
name: vr
description: Virtual reality (VR) reality tech. Locomotion, comfort defaults, controllers/hands, performance budgets, and interaction patterns.
license: Apache-2.0
metadata:
  trit: 0
  version: "1.0.0"
  bundle: reality-tech
---

# VR (Virtual Reality)

Use when the user is building an immersive VR experience (Quest/PCVR) in WebXR or OpenXR.

## Comfort Defaults

- Teleport locomotion + snap-turn
- No forced acceleration; no camera shake by default
- Stable horizon; keep UI readable and at comfortable depth

## Interaction Defaults

- Start with ray pointer + grab/select
- Use clear affordances: hover, highlight, haptics (when supported)

## Debug Checklist

- Confirm runtime (OpenXR) and controller profiles
- Validate action bindings and input mappings per device
- Measure on-device frame timing early

See also: `ar-vr-xr` for performance and privacy checklists.
