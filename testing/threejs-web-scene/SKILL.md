---
name: threejs-web-scene
description: Build a production Three.js or React Three Fiber scene for a cinematic website when live geometry, shaders, lighting, or interaction are genuinely required.
---

# Three.js Web Scene

Do not start here. Confirm `model-viewer`, Spline, video, or a sequence cannot satisfy the requirement.

## Read

- `integrations/threejs/README.md`
- `creative-production/pipelines/web-3d-assets.md`
- `skills/web-3d-asset-pipeline/SKILL.md`

## Scene contract

Define:

- user interaction
- camera states
- object states
- lighting
- scroll relationship
- loading state
- error state
- reduced motion
- mobile fallback
- cleanup lifecycle

## Minimum implementation

- explicit renderer size
- bounded device pixel ratio
- color management
- asset loading progress
- resize handling
- pause when offscreen
- dispose geometry, materials, textures, and renderer
- semantic content outside the canvas
- keyboard-safe controls
- poster fallback

Use React Three Fiber only inside an existing React product. Do not add React to a static page solely for the renderer.

## Choreography

Use GSAP or Theatre.js only when the scene has coordinated approved beats. One system owns camera state.

## Verify

Test low-power mobile, reduced motion, WebGL failure, lost context, slow network, high-DPI screens, tab backgrounding, and page navigation.

A beautiful scene that makes the page unusable is a failed implementation.
