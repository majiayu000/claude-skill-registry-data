---
name: game-dev
description: Build playable browser games (Babylon.js) end-to-end using the godogen
  production pipeline adapted to Manus. Use when the user wants to make, generate,
  rebuild, or substantially extend a web/browser game from a natural-language brief.
  Runs godogen's staged workflow (visual target, risk decomposition, scaffold, architecture,
  asset generation, implementation, visual verification) but hosts the game in a Manus
  WebDev project, replaces godogen's paid art CLIs (Gemini/Grok/Tripo3D) with Manus
  built-in image generation, and deploys through WebDev Publish instead of temporary
  links.
license: Complete terms in LICENSE.txt
---

# Game Dev

Build complete, playable Babylon.js browser games from a natural-language brief,
following the **godogen** production pipeline but running it natively inside Manus.

This skill keeps godogen's engine (Babylon.js) and its disciplined workflow, while
adapting three things to the Manus environment:
1. **Host shell** → a Manus **WebDev** React project (not godogen's bare Vite scaffold).
2. **Art** → Manus **built-in image generation** (`generate` mode), replacing godogen's paid Gemini/Grok/Tripo3D CLIs. The art step is **mandatory, never skipped**.
3. **Deploy** → **WebDev Publish** to `*.manus.space`. Temporary `expose` links are **forbidden** as the deliverable.

Layering principle to keep in mind throughout: **React = picture frame, Babylon = canvas, godogen game code = the painting.**

## Resources in this skill

- `references/manus-adaptations.md` — **read this first.** Exact rules for the WebDev host, the image-generation art step, screenshot verification, and WebDev deployment. Overrides godogen stage files where they conflict.
- `references/godogen-stages/*.md` — the unmodified godogen stage instructions (`visual-target`, `decomposer`, `architecture`, `scaffold`, `asset-planner`, `asset-gen`, `rembg`, `task-execution`, `quirks`, `scene-generation`, `capture`, plus `godogen-skill-overview.md`). Read each stage file only when you reach that stage. Treat them as the source of truth for *how a good game is built*; apply the Manus adaptations for *where it runs and how art/deploy happen*.
- `templates/GameCanvas.tsx` — the Babylon-in-React integration component (single full-screen canvas, lifecycle-safe). Drop into the WebDev project.

## Pipeline (godogen, adapted)

Follow these stages in order. On resume, if `PLAN.md` already exists in the project, read `PLAN.md`/`STRUCTURE.md`/`MEMORY.md`/`ASSETS.md` and skip to task execution.

1. **Set up the WebDev host.** `webdev_init_project` (scaffold `web-static`). `pnpm add @babylonjs/core` (add `@babylonjs/loaders` only for GLB). `webdev_restart_server`. Add `GameCanvas.tsx` from the template and make `<GameCanvas />` the sole content of the `/` route. See `references/manus-adaptations.md` §1 for the non-negotiable canvas/React lifecycle contract.
2. **Visual target.** Read `references/godogen-stages/visual-target.md`. Enter `generate` mode and produce a reference image defining art direction. Record it in `ASSETS.md`. (Art step is mandatory — see §2 of adaptations.)
3. **Decompose + risks.** Read `references/godogen-stages/decomposer.md`. Write `PLAN.md` with risk slices and verification criteria. Isolate high-risk features first (procedural generation/animation, sprite animation, vehicle physics, custom shaders, runtime geometry, dynamic navigation, complex cameras, pointer-lock, GLB import pipelines); everything else is main build.
4. **Architecture.** Read `references/godogen-stages/architecture.md`. Keep gameplay as plain TS classes under `client/src/game/` (GameWorld, Player, managers, etc.), framework-agnostic. Write `STRUCTURE.md`.
5. **Assets.** Read `references/godogen-stages/asset-planner.md` + `asset-gen.md` for *what* to plan, but generate via Manus `generate` mode (adaptations §2). Upload generated PNGs with `manus-upload-file --webdev` and use the returned `/manus-storage/...` URL as Babylon textures. Default to procedural meshes + generated textures; only use real GLB models if the user supplies a Tripo3D key. Maintain `ASSETS.md`.
6. **Implement.** Read `references/godogen-stages/task-execution.md`, `quirks.md`, and `scene-generation.md`. Build risk slices first, then the main build. Inner loop: edit `client/src/game/**` → HMR → screenshot → check.
7. **Verify (trust the picture).** Use `webdev_take_screenshot` against the WebDev preview (adaptations §3), not godogen's `capture.mjs`. Add a `?demo` deterministic AutoPilot so screenshots show real gameplay. Run `pnpm check`. If a requirement is not visible in a screenshot, it is unfinished. When code and picture disagree, trust the picture.
8. **Deploy via WebDev.** `webdev_save_checkpoint`, then direct the user to click **Publish** (adaptations §4). NEVER hand off a temporary `expose` link.

## Non-negotiable rules

- **Art is mandatory and uses Manus built-in image generation.** Never silently skip art or ship only flat placeholder colors. Procedural geometry is fine, but art direction must come from a generated reference and generated textures/assets.
- **Deployment is always WebDev Publish.** Temporary/proxy links are not an acceptable final deliverable.
- **Keep godogen context files** (`PLAN.md`, `STRUCTURE.md`, `MEMORY.md`, `ASSETS.md`) in the project root for fidelity and resumability.
- **Preserve godogen philosophy:** risk slices first, read stage files on demand, and verify visually.
- **Respect the Babylon-in-React contract** (init once, dispose on unmount, handle resize, guard StrictMode) — see template and adaptations §1.

## Quirks worth front-loading

- React 19 StrictMode mounts effects twice in dev → guard Babylon engine init with a ref flag, or you get two engines on one canvas.
- Do NOT commit large image assets into the WebDev project tree (deploy timeout). Always go through `manus-upload-file --webdev` and reference the returned URL.
- Import Babylon from deep module paths to keep the bundle small.
- Babylon needs a non-zero-size canvas; the full-screen `fixed inset-0` canvas in the template handles this. Call `engine.resize()` on window resize.
