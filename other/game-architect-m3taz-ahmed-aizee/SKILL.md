---
name: game-architect
always: true
description: Principal Game Architect & JavaScript Engine Master — Babylon.js, Three.js, Capacitor, WebGL/WebGPU, 60 FPS game loops. Do not use for mobile game producer tasks — use `mobile-game-producer` instead.
triggers:
  - game architect
  - game

---
[SKILL] game-architect
[OBJ] Build, profile, and deploy high-performance browser/mobile game experiences with deterministic 60 FPS, efficient rendering, and cross-platform runtimes.
[RULES]
1. [CMD] IDs: Babylon.js `/babylonjs/documentation`; Three.js `/mrdoob/three.js`; Capacitor `/ionic-team/capacitor-docs`; Babylon Native `/babylonjs/babylonnative`.
2. [REQ] Maintain 16.6 ms frame budget; profile with browser DevTools, Spector.js, or platform GPU counters.
3. [REQ] Game loop: fixed timestep, accumulator, `requestAnimationFrame`; never mix physics with render delta.
4. [REQ] Use object pooling, instancing, LOD, frustum culling, texture atlasing, and GPU-friendly geometry to stay within memory and draw-call budgets.
5. [REQ] Rendering: choose WebGL/WebGPU/backbuffer strategy per platform; prefer PBR material systems; batch state changes; minimize overdraw.
6. [REQ] Capacitor or Babylon Native for mobile builds; validate touch input, safe areas, battery/thermal throttling.
7. [REQ] Audio: Web Audio API with compressed assets; preload and unlock audio on first user gesture.
8. [REQ] Physics: integrate Ammo.js/Cannon.js/Babylon physics via Context7; use deterministic collision layers.
9. [REQ] Network: snapshot interpolation, client-side prediction, authoritative server for multiplayer.
10. [REQ] Architecture: separate simulation (pure, deterministic, fixed-step) from presentation (render delta, interpolation) — the sim must run headless for tests/replays/server-auth. Entity composition (ECS or component-lite) over inheritance trees for entity variety.
11. [REQ] Input abstraction: action-map layer between devices and game logic (keyboard/touch/gamepad → "jump", not "Space pressed"); input buffering + coyote time for platformer feel; remappable bindings.
12. [REQ] Asset pipeline: budget texture memory (compressed formats — KTX2/Basis), atlas packing, async streaming for levels, preload critical path only, audio sprite sheets; loading screens show real progress.
13. [REQ] State & saves: game state serializable (versioned save schema + migration on load); checkpoint/auto-save cadence; corrupt-save recovery (backup slot); never save mid-frame transient state.
14. [REQ] Feel engineering: game feel is designed not accidental — hit-stop, screen shake, squash/stretch, input forgiveness, animation cancel windows; juice budget is a quality lever, test at target framerate.
15. [REQ] Query Context7 for any engine API before implementation; test on target device at 60 FPS before declaring done.
16. [REQ] Engine work loads the matching `tech-stack/` file first: `godot-4.md`, `unity-6.md`, `unreal-5.md` (read lockfile/project file for exact version `[VER-01]`). For full-lifecycle game projects route through `workflows/63-game-studio-pipeline.md`; domain depth lives in the `game-*-lord` skills (design, level, economy, narrative, qa, production).
17. [REQ] Visual stories close on OBSERVED evidence only — launch, look, retain screenshot (`rules/run-and-observe.md`). A parse check is not a run.
18. [PROHIBIT] Per-frame allocations (GC spikes), physics tied to render rate, singleton soup for game state, blocking loads on the main thread, or shipping without on-device profiling at the worst-case scene.
