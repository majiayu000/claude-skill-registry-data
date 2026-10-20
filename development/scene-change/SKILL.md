---
name: scene-change
description: Change the agent-office 3D scene at runtime — which wing, desk or room an agent uses, agent behavior and choreography, characters and animation playback, labels, lighting/render pipeline and quality presets, camera or walk controls. Use for any edit to packages/web/src/app/{building,seating,reservations,behavior,navigation,choreography,layout}.ts, packages/web/src/adapters/three/*, or shared/src/grouping.ts. For the Blender assets themselves use asset-change.
---

# Change the 3D scene

Rules: `SCENE.md`, `TESTING.md`, `PRIVACY_SECURITY.md` (text via `textContent`).

1. **Organization or positions?** Start in pure code, test-first (`packages/web/src/app/`):
   - who goes where → `packages/shared/src/grouping.ts` (+ `grouping.test.ts`)
   - which wing a provider gets, annexes, world anchors and the merged nav graph → `building.ts`
   - which desk an agent gets (topic → pod, subagents next to the parent, stable seats) → `seating.ts`
   - which room an agent goes to and when (meeting, booth, kitchen, lounge, cafe, ping-pong, arriving, leaving) → `behavior.ts` + `reservations.ts`
   - how it gets there (paths, timing, clip sequences, no snapping) → `navigation.ts` + `choreography.ts`
   - what the panel and tags say → `view-models.ts` (`activityLabel`, `data-activity`)
   - Positions come **only** from manifest anchors (`docs/graphics-contract.md`). If the building itself must change, that is `/asset-change`.
2. **Visuals** (`packages/web/src/adapters/three/*`): the scene implements the `SceneView` port — decisions stay in the controller and the pure modules. Load the Blender-built glbs and the character from `public/assets` (served under `app://renderer/assets/…` in production), reuse cached geometries and materials (clone per instance only for tinted materials, screens and LEDs), colors only from `STATUS_COLORS`, no allocations in `update()`, dispose on removal. Respect the quality preset passed to `setQuality` and the animation rules in `SCENE.md` (in-place clips, crossfades, `Walk` timeScale follows speed).
3. **Verify visually** with `/run-office`: the atrium, Main Street and each wing; agents sitting exactly at their seats, walking without foot sliding, rooms used as expected; labels not overlapping; light and dark mode; walk mode collisions. `make screenshots` captures the fixed camera bookmarks.
4. **Perf budget**: `make perf` (150 mock agents, FPS report; target ≥ 55 fps average at Medium). Interactively: with `make dev-mock` running, `curl -X POST -H "authorization: Bearer $(cat ~/.agent-office/token)" 'http://127.0.0.1:4317/api/mock?n=150'` and open `?stats` for FPS, draw calls and triangles.
5. UI or behavior change → add/adjust a spec in `packages/desktop/e2e/` (`building`, `behavior`, `quality`; assert on `data-activity` and panel text); run `make build test-ui`.
6. `make check`.

2D RPG mode: see `docs/2d-architecture.md`. The pure logic is in `web/src/app/pixel/*`, the Canvas2D drawing in `web/src/adapters/pixel/*`, the art in `assets/pixel/src` (`make pixel-assets`), and the floor plans come from `make assets-plan`. Check both modes with `pixel.spec.ts` and the existing 3D specs.
