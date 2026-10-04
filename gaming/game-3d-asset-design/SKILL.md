---
name: game-3d-asset-design
description: Plan, create, optimize, import, export, and review game-ready 3D assets. Use when Codex is asked to work on props, environment pieces, modular kits, materials, textures, LODs, collision, pivots, scale, naming, asset budgets, Unity/Unreal/Godot imports, or production handoff for 3D game assets.
license: MIT
---

# Game 3D Asset Design

## Core Workflow

1. Identify the asset type, target engine, camera distance, platform, art style, interaction needs, and performance budget.
2. Define the asset's gameplay job before visual detail: cover, landmark, pickup, door, hazard, decoration, traversal object, UI object, or modular kit piece.
3. Set technical constraints early: real-world scale, pivot/origin behavior, collision type, material count, texture resolution, LOD needs, lightmap/secondary UV needs, naming rules, and export format.
4. Build from broad shape to game-ready delivery: blockout, approved silhouette, optimized mesh, UVs, materials/textures, collision, LODs, import test, and in-engine review.
5. Preserve source and output separation. Keep editable DCC files, high-poly sources, bake files, and engine-ready exports clearly named and stored.
6. Verify the asset inside the target engine or representative scene, not only in the modeling package.

## Asset Priorities

- Scale and units: work to the target engine's unit expectations and test with a known meter cube or player reference.
- Pivot and orientation: place pivots for actual use, such as doors rotating on hinges, props snapping to grids, and pickups centering cleanly.
- Mesh efficiency: use polygons where they affect silhouette, deformation, collision, lighting, or close-up readability.
- Materials and textures: minimize material slots, use power-of-two texture sizes where appropriate, preserve source texture files, and choose resolution based on on-screen size.
- Collision: provide simple collision for performance unless gameplay needs exact shape.
- LODs: author or generate LODs for assets seen at varied distances, and verify silhouette preservation.
- Naming and hierarchy: use descriptive, unique names without special characters; keep hierarchies as simple as practical.
- Modularity: align dimensions, pivots, trims, texel density, and snap rules for kit pieces.

## Deliverable Shape

For asset planning or review, provide:

- Asset purpose and gameplay role
- Style and reference notes
- Scale, pivot, collision, and snapping requirements
- Mesh, material, texture, and LOD budget targets
- Source/export file expectations
- Engine import settings and validation steps
- Risks, open questions, and follow-up asset tasks

## References

- Read `references/asset-pipeline-checklist.md` when preparing or reviewing any game-ready 3D asset.
