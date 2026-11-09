---
name: babylonjs-build-scenes
description: Build Babylon.js engine, scene, asset-container and world lifecycles with explicit simulation and resource ownership.
engines: [BABYLONJS]
---

# Build Babylon.js Scenes

## When to use

Create game scenes, streamed environments or the Babylon engine/asset boundary.

## Engine and dependencies

Before edits or tool launches, run `resolve-engine.sh` and `resolve-skill.sh babylonjs-build-scenes`; require compatibility and honor task override scope. Read the locked Babylon package versions, engine contract, world conventions and budgets. Keep core/loaders/GUI packages compatible. Use project-hosted assets and decoders; do not install packages or introduce CDN globals implicitly.

## Workflow

1. Own `Engine` or selected `WebGPUEngine`, canvas, render loop and resize handling at the application boundary. Await required initialization, select backend capabilities explicitly and route context-loss/restoration failures visibly.
2. Give each `Scene` an enter/leave/dispose contract and active-camera policy. Map application entity IDs to nodes; meshes and observables must not become the only durable gameplay state. Avoid duplicate loops after remounts.
3. Register loaders and use the installed revision's asset-container API for independently owned bundles. Stage loaded containers before activation. Transition tokens reject stale asynchronous results; dispose abandoned bundles without touching retained shared assets.
4. Decide handedness, units, origin strategy, camera clipping and static/instanced/thin-instance use from actual content. Thin instances need an explicit index-to-entity mapping and update/bounds policy.
5. Keep save schemas and content IDs independent from scene serialization. A Babylon scene export can preserve authored presentation but does not automatically include application rules, AI state or migrations. For navigation, select the actual plugin/data source, coordinate conversion and movement adapter; never assume a navmesh or agent solver is included by selecting this skill.
6. Remove owned observable subscriptions; dispose containers, scenes and the owning engine at their distinct lifetime ends. Preserve reusable textures/materials until their final user is released.

## Output and verification

Deliver lifecycle and loading adapters, world identity rules and resource/budget evidence. Test failed imports, transition races, missing textures, multiple instances, repeated enter/exit and resize/visibility restoration. Record real browser/GPU behavior separately from state fixtures. Consult the [official asset-container implementation/API](https://github.com/BabylonJS/Babylon.js/blob/master/packages/dev/core/src/assetContainer.ts) at the host's pinned revision rather than assuming current master matches.
