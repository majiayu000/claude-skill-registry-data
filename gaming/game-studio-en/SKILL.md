---
name: game-studio-en
description: Browser game development workflow assistant. Trigger when users mention game design, prototyping, gameplay implementation, Phaser, Three.js, React Three Fiber, sprite pipelines, glTF assets, HUDs, menus, playtesting, browser-game QA, 2D, or 3D. Choose the right browser-game stack first, then provide implementation, asset, and validation paths.
license: MIT
packageType: instruction-skill
instructionOnly: true
---

# Game Studio English

## Overview

This skill guides browser-game work from concept, prototype, gameplay implementation, asset pipeline, HUD/menu design, and playtest QA into a practical delivery path.

Default to a 2D-first strategy: unless the user explicitly asks for 3D, WebGL, Three.js, or React Three Fiber, recommend Phaser + TypeScript + Vite. When the user clearly needs 3D, choose between plain Three.js and React Three Fiber based on the app host and state model.

## Use This Skill When

Use this skill when the user asks to:

- Design or break down a browser-game concept, core loop, or level rhythm
- Build Phaser 2D gameplay, sprites, tilemaps, platformers, tactics games, or top-down action
- Build Three.js, React Three Fiber, WebGL, 3D scenes, cameras, physics, or GLB loading
- Plan 2D sprite animation or 3D glTF / GLB asset pipelines
- Design HUDs, menus, overlays, pause screens, failure screens, or low-chrome 3D UI
- Run browser playtests, screenshot review, readability checks, performance checks, or WebGL QA

## Do Not Stay Here When

- If the user explicitly asks for native Unity, Unreal, Godot, or console-game workflows, explain that this skill covers browser games.
- If the user only wants image generation, asset retouching, or a single art image, route to an image or asset-generation workflow instead of a full game architecture.
- If the user only wants generic web accessibility, forms, dark mode, or UI quality review, use the web UI quality workflow.
- If the user explicitly requests Babylon.js or PlayCanvas, compare objectively, but do not make them the default path.

## Routing Rules

Classify the user's request first, then use the matching reference:

| User intent | Default path | Reference |
|---|---|---|
| Game prototype without explicit 3D, 2D, sprites, tilemaps, platformers, tactics | Phaser 2D | `references/2d-phaser.md` |
| Explicit 3D, WebGL, Three.js, plain TS/Vite | Three.js | `references/3d-runtime.md` |
| 3D inside a React app, shared React state, declarative scene composition | React Three Fiber | `references/3d-runtime.md` |
| Architecture, engine selection, input/state/save boundaries | Foundations | `references/foundations.md` |
| 2D sprites, animation strips, GLB, glTF, compression, collision, LOD | Assets | `references/assets.md` |
| HUDs, menus, overlays, playtesting, screenshots, readability, QA | UI / Playtest | `references/ui-playtest.md` |

## Default Workflow

1. Lock the game direction: player fantasy, core verbs, main failure states, target session length, input model, and platform constraints.
2. Choose the stack: default to Phaser 2D; choose Three.js or React Three Fiber only for explicit 3D work.
3. Define boundaries: simulation/rendering separation, input map, asset manifest, save/debug/performance boundaries.
4. Break down gameplay: core loop, entity state, collision/interaction, level or content configuration, win/loss conditions.
5. Plan assets in parallel: sprite sizes, anchors, animation frames; 3D model scale, naming, compression, collision proxies.
6. Design UI: prefer DOM HUDs, protect the playfield, and avoid putting text-heavy UI into canvas or WebGL.
7. Finish each increment with playtest QA: boot, main verbs, failure recovery, screenshots, viewport changes, performance, and WebGL checks.

## 2D Path

Use Phaser + TypeScript + Vite by default for 2D. Keep gameplay state outside Phaser scenes, and let scenes handle lifecycle, asset binding, cameras, and render objects. Use DOM overlays for HUDs, menus, pause screens, and text-heavy interaction.

For 2D requests, explain:

- Where game state lives and what scenes own
- How inputs map to gameplay actions
- How sprites, tilemaps, cameras, and collision are organized
- How the HUD layers over the canvas
- What the first playable prototype must validate

See `references/2d-phaser.md` for details.

## 3D Path

When the user clearly needs 3D, branch first:

- Plain TypeScript / Vite / non-React: use Three.js with direct render-loop and imperative scene control.
- 3D inside a React app: use React Three Fiber so the 3D scene works with React state and DOM UI.

The default 3D asset format is GLB or glTF 2.0. Define loading, camera, physics, postprocessing, and HUD boundaries before adding visual effects. Use low-chrome 3D UI: keep the center playfield clear and keep objectives, status, and prompts compact.

See `references/3d-runtime.md` for details.

## Asset Pipeline

For 2D sprites, start from an approved in-game seed frame, generate a full animation strip, normalize frames with one shared scale and anchor, then preview before shipping.

For 3D assets, clean the source file in a DCC tool, export GLB / glTF 2.0, optimize with glTF Transform, check pivots, scale, collision proxies, LOD, texture budgets, and runtime loading.

See `references/assets.md` for details.

## UI and Playtest

Put text-heavy UI in the DOM layer by default. During normal play, keep the center and lower-middle playfield clear, use one primary persistent HUD cluster, and keep secondary status compact. Playtests must verify clear main verbs, responsive feedback, pause/failure/recovery, and whether HUDs block gameplay across viewports.

See `references/ui-playtest.md` for details.

## Output Expectations

Return one or more of these outputs depending on the request:

- Stack choice and rationale
- Implementable directory structure and module boundaries
- Core gameplay loop, state machine, input map, or scene breakdown
- Asset specs, naming, anchors, compression, and acceptance checklist
- HUD / menu / overlay layout guidance
- Playtest QA checklist, reproduction steps, and severity-ranked issues

## Common Pitfalls

- Do not upgrade a project to 3D unless the user actually asks for 3D.
- Do not put all game state inside Phaser scenes or Three.js objects.
- Do not let UI block the core playfield, especially the center and lower-middle area.
- Do not generate sprite frames as unrelated one-off images; use full strips and normalize them together.
- Do not treat GLB files as final without checking scale, pivot, textures, and collision assumptions.
- Do not postpone playtesting until the end; each playable increment needs QA.

## References

- `references/foundations.md`: engine choice, architecture boundaries, input, save, debug, and performance boundaries
- `references/2d-phaser.md`: Phaser 2D structure, scenes, cameras, sprites, DOM HUDs
- `references/3d-runtime.md`: Three.js / React Three Fiber choice, 3D architecture, loaders, physics, performance
- `references/assets.md`: 2D sprite and 3D GLB / glTF asset pipelines
- `references/ui-playtest.md`: HUDs, menus, playfield protection, playtesting, and browser QA
