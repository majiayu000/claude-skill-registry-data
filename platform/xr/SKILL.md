---
name: xr
description: Extended reality (XR/MR) reality tech. Mixed reality and spatial computing across AR and VR capabilities.
license: Apache-2.0
metadata:
  trit: 0
  version: "1.0.0"
  bundle: reality-tech
---

# XR / MR (Extended or Mixed Reality)

Use when the user needs guidance across the AR/VR boundary: passthrough + world-locked content + immersive interaction.

Default to the umbrella skill `ar-vr-xr` unless the request is clearly AR-only (`ar`) or VR-only (`vr`).

Key concerns to surface:
- Comfort + locomotion choices
- Sensor privacy (camera, room mapping)
- Platform constraints (runtime, permissions, capability availability)
- Shared state correctness under faults: use `jepsen-testing`
- Device-specific guidance: `varjo-xr-4`
