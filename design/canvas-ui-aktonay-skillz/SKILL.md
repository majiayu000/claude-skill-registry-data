---
name: canvas-ui
description: >
  Live WebGL/WebGPU shaders running over interactive HTML DOM elements via HTML-in-Canvas.
  Text remains selectable, links and forms stay fully clickable while being distorted or refracted.
license: MIT
---

# Canvas UI Skill

Use this skill when building creative, immersive web experiences with real-time shader distortion, refraction, or liquid effects without sacrificing accessibility, text selection, or form interactivity.

## Core Concepts

Traditional WebGL canvas implementations replace HTML with a static raster texture, which destroys accessibility, hyperlinks, and input fields.
**Canvas UI** renders live DOM elements directly to canvas textures via `CanvasRenderingContext2D.drawElement()`:
- Text is 100% selectable by the user.
- Inputs, buttons, and hyperlinks remain interactive.
- WebGL fragment shaders apply real-time ripple, chromatic aberration, or glass refraction over the rendered HTML.

## Safe Fallback Pattern
Always include a graceful fallback for browsers without `drawElement` support:
```javascript
if ('drawElement' in CanvasRenderingContext2D.prototype) {
  // Mount WebGL shader pipeline
} else {
  // Render standard CSS backdrop-filter and DOM elements
}
```
