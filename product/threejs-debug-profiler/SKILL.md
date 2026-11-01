---
name: threejs-debug-profiler
description: "Debug and profile Three.js browser games: blank canvases, render and runtime bugs, asset and audio loading, animation, resize, mobile input, plus performance profiling of draw calls, triangles, textures, memory, shader and post-processing cost, and bundle size."
---

> **CampusCove note.** Vendored from [majidmanzarpour/threejs-game-skills](https://github.com/majidmanzarpour/threejs-game-skills) @ 8286774, MIT (`_third-party/LICENSE-majidmanzarpour.txt`); only this note was added.
>
> Here: there is no `window.__THREE_GAME_DIAGNOSTICS__`; use the **C** key collision overlay and `getWorldCollisionStats()` (`game/collision/`), `renderer.info`, the HUD `XYZ` readout, and the socket/backend Docker logs. Reproduce through skill `playtest-game` (faked pointer lock, hidden-pane rAF caveat). The playbook mentions `threejs-3d-generator`, which is not installed: fix heavy assets in their Blender script instead. Production build check: `cd front && npm run build`.
>
> Advisory reference: CampusCove's own skills (`game-feature`, `blender-asset`, `playtest-game`, ...) win on any conflict.

# Three.js Debug Profiler

Find root causes and optimize measured bottlenecks without breaking playability.

Follow the changed behavior's scope. Reuse the lead's existing reproduction and evidence; verify the affected path after a fix. A passing focused check only needs broader testing when shared behavior changed or an unresolved risk warrants it. Return measurements and defects to the lead for the consolidated verification pass.

## Reference

`references/debug-playbook.md` — ordered triage for blank canvas, asset and audio loading, loop/animation/physics, input and mobile, the profiling sequence, and the `__THREE_GAME_DIAGNOSTICS__` shape. Read it when debugging or profiling anything non-obvious.

## Debug

Reproduce first, with the same command and URL the user had, and read the console, page, and network errors. Find the module that owns the failure (renderer, loop, camera, scene, assets, audio, input, physics, UI, or base path), fix the root cause there, and retest the exact broken path. The playbook's triage order covers the common causes, such as more than one active loop, a canvas whose display size doesn't match its drawing buffer, and wrong delta units.

## Profile

Profile the production preview when user-facing performance matters. Baseline one fixed scenario, classify the bottleneck (CPU, GPU draw, fragment, vertex, memory, or network), change one thing, and re-measure the same scenario, confirming visuals and playability held. The playbook lists the metrics to baseline and the optimizations in order of payoff.

## Report

Lead with the root cause or the measured bottleneck. Then files changed, baseline and post metrics, commands, screenshots, the broken path retested, and residual risks.
