---
name: leeway-3d-game-asset-production
description: Engine-ready 3D asset production skill covering topology, LODs, collision, pivots, scale, normals/tangents, material budgets, texture budgets, batching, export and game-performance validation.
license: MIT
---
# LeeWay 3D Game Asset Production
## Target profile
Before optimization define engine/runtime, camera distance, platform class, target FPS, triangle/vertex budget, material/draw-call budget, texture/VRAM budget, collision requirements, animation needs and export format.
## Production
Validate topology → repair normals/tangents → establish pivot/origin/scale → collision → LOD chain → material/texture optimization → instancing/batching opportunities → export → re-import/engine validation.
## Quality tiers
LOW/STYLIZED, MID, HIGH, CINEMATIC are project profiles with explicit budgets; do not infer quality solely from polygon count.
## Verification
Check silhouette and shading at intended distances, collision behavior, LOD transitions, texture quality, frame/resource measurements and exported artifact integrity.