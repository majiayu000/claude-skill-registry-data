---
name: webgpu-render-pipeline
description: Use when writing or debugging real-time rendering (WebGPU or a three.js/Babylon scene) — structure the frame as explicit named passes and pick the right altitude (raw WebGPU vs scene-graph engine) before writing shader code.
stacks: [node]
domains: [web, game]
phases: [dev]
tags: [rendering, webgpu, threejs, babylon, shaders, graphics]
scope: kit
---
**When to use.** New renderer, new render feature, or a graphics bug. *Why:* rendering bugs are
stage-local; an explicit pass structure lets the agent reason about one stage instead of a monolith.

**Procedure.**
1. Decide altitude: raw WebGPU for bespoke/compute-heavy; three.js/Babylon for "load glTF, light, orbit." Justify the choice in one line.
2. Lay out passes: upload → (depth pre-pass) → shade → post. Name them.
3. Feature-detect WebGPU; provide a WebGL fallback or a clear unsupported state.
4. **Done when:** it renders at target FPS on the reference device (state the number + device), and each pass is separately toggleable for debugging.

**Knowledge:** KNOWLEDGE-LIBRARY.md §A2. **Example:** the WebGPU frame-loop skeleton there.
