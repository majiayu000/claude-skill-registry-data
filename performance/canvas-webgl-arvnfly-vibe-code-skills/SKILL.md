---
name: canvas-webgl
description: "HTML5 Canvas 2D and WebGL rendering, animation frames, buffer memory lifecycle, and offscreen workers."
---

# Canvas & WebGL Performance Protocol

High-framerate 2D and 3D graphics rendering in browser environments.

---

## 1. Render Loop & Animation Frames

1. Always drive animations via `requestAnimationFrame()`, never `setInterval()`.
2. Calculate delta time (`deltaTime = now - lastTime`) to decouple animation speed from screen refresh rates.

---

## 2. Memory & Buffer Disposal

- Explicitly dispose of textures, vertex buffers, and shaders when destroying canvas scenes to prevent GPU memory leaks.
