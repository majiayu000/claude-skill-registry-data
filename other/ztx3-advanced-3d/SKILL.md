---
name: ztx3-advanced-3d
description: "Advanced 3D / React Three Fiber — select, implement, audit and test advanced 3d for production Codex frontend work, with responsive and accessibility checks."
---

# Advanced 3D / React Three Fiber

Select a stable renderer by device: Three.js WebGL as proven baseline; only opt into WebGPU/TSL when validated against installed R3F version, browser support and fallback. Separate rendering simulation from the DOM accessibility layer. Own frame lifecycle and resource disposal. Estimate draw calls, transparency sorting, shader cost, texture residency and battery use before selecting effects.

## Workflow

1. Record explicit project requirements, business goal, content and accepted test budget.
2. Read `references/HANDBOOK.md` and pick precise technique Skill files, not the entire catalog.
3. Implement smallest meaningful working baseline, then add incremental enhancements.
4. Measure or inspect result with real devices and produce fallback.
5. Report verified/untested results. No MCP, no destructive overwrites.

## Core obligations

Implement a tiny baseline scene, evaluate bounds/LOD, then add the technique under a budget; add poster fallback and explicit disposal.

Run WebGL context loss/restoration, compare desktop/mobile frustum and inspect renderer.info.

## References

- `references/HANDBOOK.md` — full architecture and 17 deep techniques.
- Refer to `ztx3-<technique>` Skill for focused implementation and acceptance.
