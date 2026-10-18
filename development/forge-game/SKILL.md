---
name: forge-game
description: "Forge: games — Canvas/WebGL/Phaser/Godot: game, browser game, gameplay, game loop, win/lose state, soft-lock, frame rate, collision, save load, playtest."
---

# Forge playbook — Games (browser · Godot)

A game is an **interactive-loop domain** — "done" means a human (or a driven browser session) can actually *play* it start-to-finish, not that a screen renders. HUD/menus and responsive layout defer to `forge-website` / `ui-boss`; this file governs the playable loop, stuck-state safety, input/viewport coverage, and honest playtest evidence. The core honesty rule: **never call a game playable without real evidence of a completed loop** (win *and* lose *and* restart reached). **Opt-in limit:** browser games can be driven + screenshotted directly with the `browser` tool; **Godot needs the Godot toolchain (editor/export), which is opt-in and owner-side** — if it isn't installed, mark export/clean-run steps not-run and report only what was actually driven.

## Hard rules (non-negotiable)
- **A genuinely playable loop.** The core loop runs end-to-end: input → state update → render → feedback, reaching a **win** and a **lose** condition and a working **restart**. Not a static mockup, not a title screen with a dead "Play" button.
- **No stuck / soft-lock states.** No dead-end where the player can't progress or restart; game-over and win are always reachable and recoverable; **pause/resume** works; input never stops responding. A soft-lock is a shipping-blocker, not a polish item.
- **Cross-viewport + declared inputs.** The canvas scales/letterboxes correctly at mobile **and** desktop sizes with no cut-off UI — or the game explicitly declares desktop-only. Every declared input method actually works (keyboard, mouse, touch, gamepad as appropriate; Godot: multiple resolutions/aspect ratios via a stretch mode).
- **Honor the dependency constraint.** If the brief says vanilla / no-framework / zero-dependency, honor it — no CDN pulls, self-contained assets. If the game ships as a Forge **artifact**, it must be self-contained under the artifact CSP (inline JS/CSS, assets as data URIs — no external hosts).
- **Runtime health.** Zero console errors during a full play session; a stable frame rate using a **delta-time** loop (`requestAnimationFrame` with elapsed time; a **fixed timestep** for physics) rather than assuming 60fps; and **cleanup on restart/scene change** — listeners, intervals, timers, and audio nodes are removed so replaying doesn't leak or double-fire.
- **Persistence works if promised.** If save/load or high-scores are in scope, they actually persist and restore correctly across reloads.
- **Real playtest evidence.** The loop is proven by actually playing it (or driving it via browser automation) with screenshots/recording showing win + lose + restart — evidence, never an assertion.

## Team (conditional)
Lead: `build-boss` (a game is implementation-heavy). HUD / menus / responsive canvas + visual quality: `ui-boss` (with `forge-website` for layout). QA: `test-boss` — drive the loop via `browser` automation (win / lose / restart reachable, no stuck states, cross-viewport, no console errors). Code review: `typescript-reviewer` for browser JS/TS (honest gap: **no dedicated Godot/GDScript reviewer agent exists** — Godot script review is `build-boss` + general review). Runtime efficiency (frame budget, asset weight): `seo-boss` (its non-web remit is runtime performance). `ml-engineer` / `data-scientist` only if the game has procedural-generation or ML-driven content (opt-in). Optional advisor: `codex-reviewer` on the core loop/state code.

## Skills / commands / MCP
`browser` is the key evidence tool — drive and screenshot the running browser game to produce real playtest proof (win/lose/restart, no console errors). `systematic-debugging` for stuck states, collision/physics bugs, and frame drops. `forge-website` for menus/HUD and a responsive canvas. Engine/API specifics via Context7 (Phaser, Godot/GDScript). **Opt-in:** the Godot editor/export toolchain is owner-side and not provisioned by Forge — browser games need no such dependency and can be driven directly.

## Fan-out & flow
L2 for a single-mechanic browser game; L3 for a multi-level / multi-system game (physics + AI + save/load + audio).
**Serial:** core loop (input→update→render) → win/lose/restart states → feedback/juice → cross-viewport + input coverage → playtest evidence.
**Parallel:** independent systems (rendering ∥ input ∥ audio ∥ level data) and independent levels/assets — independent once the game-state contract is fixed (the state model is the contract).

## Domain gates
- Core loop runs and **completes**: start → play → win AND lose → restart, all reachable; no soft-lock; pause/resume works.
- Canvas scales/letterboxes correctly at mobile + desktop sizes (or desktop-only is declared); every declared input method works.
- **Zero console errors** across a full session; stable frame rate via a delta-time loop (fixed timestep for physics); listeners/timers/audio cleaned up on restart (no leak, no double-fire).
- If a zero-dependency constraint was set, no external/CDN deps; self-contained (and CSP-safe if delivered as an artifact).
- Save/load / high-scores (if promised) persist and restore across reloads.
- Real playtest evidence attached (screenshots/recording of win + lose + restart) — not asserted.

## Ship-readiness (unique)
Playable loop proven end-to-end with **real playtest evidence** (win + lose + restart actually reached); no stuck states; works at mobile + desktop viewports and for every declared input; zero console errors; stable frame rate + cleaned-up listeners; the zero-dependency constraint honored if set; save/load verified if promised. If the game is a Godot project and the Godot toolchain wasn't available, mark export + clean-run as not-run and report only what was actually driven — don't imply an export that didn't happen. Advisory checklist; optionally run `codex-reviewer` on the core loop/state code — not a blocker.
