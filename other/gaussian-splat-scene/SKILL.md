---
name: gaussian-splat-scene
description: Use when integrating captured 3D scenes (Gaussian splats / radiance fields / photogrammetry of real spaces) into the app — load, depth-sort, and budget splats, and author toward the glTF KHR_gaussian_splatting path.
stacks: [node]
domains: [web, game]
phases: [dev]
tags: [rendering, gaussian-splatting, 3dgs, gltf, neural-rendering]
scope: kit
---
**When to use.** Rendering real captured spaces (a likely NotHomeWrecker need). *Why:* splats are
point data with different perf and lighting rules than meshes; naïve integration tanks FPS.

**Procedure.**
1. Load via a maintained viewer (GaussianSplats3D for three.js, native for Babylon); don't write a splat rasterizer from scratch.
2. Budget by splat count + VRAM; use static textures not per-frame instance buffers; GPU depth-sort.
3. Handle splat-vs-mesh depth/blend order if mixing with lit geometry.
4. **Done when:** target scene holds target FPS with correct depth ordering; export/author path is glTF-compatible.

**Knowledge:** KNOWLEDGE-LIBRARY.md §A2 (3DGS paper, Babylon/three.js splat docs, KHR extension).
