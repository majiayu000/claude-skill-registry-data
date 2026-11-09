---
name: threejs-build-controls
description: Implement Three.js picking, camera controls and browser input adapters with explicit player, modal and pointer ownership.
engines: [THREEJS]
---

# Build Three.js Controls

## When to use

Add picking, camera interaction, first-person input, touch gestures or controller actions around a Three.js runtime.

## Engine and dependencies

Before edits or tool launches, run `resolve-engine.sh` and `resolve-skill.sh threejs-build-controls`; require compatibility and honor task override scope. Inspect the locked Three.js revision, selected controls addon, browser capabilities and action contract. Use host packages; add no implicit CDN, physics implementation or dependency.

## Workflow

1. Convert keyboard, pointer, touch and gamepad events into actions for the assigned local player. Simulation consumes snapshots or queued edges; DOM callbacks do not directly move authoritative bodies.
2. Calculate pointer coordinates from the actual canvas/viewport bounding rectangle. Use `Raycaster.setFromCamera`, explicit pick layers and bounded candidates; map results, including `instanceId`, to stable gameplay identity. Update world matrices before queries when transforms changed outside rendering.
3. Select `OrbitControls`, `MapControls`, `PointerLockControls`, or a project controller. Match addon and core revisions. Update damping when enabled; dispose controls/listeners at ownership end. Avoid simultaneous camera writers.
4. Distinguish camera drag from click, pointer capture from pointer lock, and world input from modal UI. Clear held actions after blur, pointer cancellation, capture loss, disconnect and scene change. Browser lock/fullscreen needs a user gesture and denial handling.
5. Apply dead zones and rebinding in the action layer. Controller haptics need capability checks, player/device ownership, bounded duration, intensity settings and cancellation; unavailable output cannot alter gameplay. Mobile vibration is not universally available.

## Output and verification

Deliver the input adapter, pick mapping and teardown. Check scaled/offset canvases, split viewports, overlapping UI, drag cancellation, rebind prompts, focus restoration, reconnect and rejected haptic calls. Verify movement across frame rates. Automation proves event routing; physical-device tests prove tactile output. Use the [Raycaster API](https://threejs.org/docs/pages/Raycaster.html) and [OrbitControls API](https://threejs.org/docs/pages/OrbitControls.html) matching the project revision.
