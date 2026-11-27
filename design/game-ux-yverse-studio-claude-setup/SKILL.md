---
name: game-ux
description: "Use when a game has first-person or follow camera, mouse look, HUD, menus or stiff idle NPCs: controls, camera, onboarding, NPC idle life, accessibility floor."
---

# Game UX: controls, camera, screen, people in the scene

Between `game-3d` (engine, assets, tests) and the web UI skills (`impeccable`, `ui-review`): how a player moves,
looks, is told what to do, and what people in the world do idle. Numbers marked [judgement] are tuned by eye;
change them when a playtest says so. Game Designer writes the answers into `design/GDD.md` (`## Controls`, HUD
wireframe in `design/UX.md`); Programmer builds §1 to §3; Playtester runs §5. HUD checks: game-camera screenshots at 390 and 1440 px
(`ui-review`, `design-critic`), `impeccable` for DOM overlays, `a11y-architect` for the accessibility pass.

## 1. Controls and camera

The floor every game ships with, plus its playtest checks: [`refs/controls-baseline.md`](refs/controls-baseline.md)
(the floor's settings and values live only there). One input layer (`src/input.ts`) turns keyboard, mouse, touch and gamepad into intents
(`move`, `look`, `interact`, `pause`); levels and rules read intents, never raw events.

- **First person:** yaw turns the body, pitch only the camera head, clamped to about -70 to +70 degrees (as
  `game-3d/starter/walkable-room.md`), roll never. Eye height 1.55 to 1.7 m, near 0.05. Draw no player body when the
  figure is not part of the story.
- **Mouse look:** Pointer Lock from a click, never on load; ask for `{ unadjustedMovement: true }` and catch the error
  to fall back to OS-adjusted deltas. Read `movementX`/`movementY`, no smoothing or acceleration. On
  `pointerlockchange` (Esc releases the lock) pause and show a "click to continue" panel; an iframe needs
  `allow-pointer-lock`. Where the lock is refused, drag-to-look with its own sensitivity is the fallback.
- **Move feel:** speed in baseline row 12, velocity eased and collision as in `walkable-room.md`, no head bob by
  default (an option, off; if on, at most 1 cm sway at 2 Hz [judgement]), no camera smoothing on the look.
- **Third person:** follow camera with a spring arm that shortens on the first hit
  (`game-3d/refs/gamedev-skills/camera-systems`); a hard cut resets the smoothing.
- **Game feel:** `game-3d/refs/gamedev-skills/game-feel` and the GDD's Feel lines; feedback inside 100 ms [judgement].
- **Settings:** one saved settings object (baseline row 7) with a unit test for load, save and clamp.

## 2. Screen and onboarding

- **First 60 seconds:** one visible goal in the world, a response to the first input in under 500 ms, no wall of text;
  the first action is the core verb. The 60 to 90 s window comes from vendor blogs, so the GDD sets the number and the
  Playtester measures it.
- **Prompts name the device in use** ("Click", "Tap" or the pad glyph) and read the key from the binding, never from copy.
- **Diegetic first:** a price on the stall, a goal as a marker in the world; a HUD is what is left, at the screen edges and out of the centre of view.
- **Panels:** one open at a time, Esc or a tap outside closes, pause always reachable (`game-3d` §2). UI text from keys, never baked into images.

## 3. People in the scene

A figure in a T-pose or one loop reads as a prop. Minimum per NPC [judgement, tune by playtest]:

- three or more idle clips, one every 4 to 10 s at a random start phase, so no two figures share a frame; breathing
  and blinking on top;
- head and eyes turn to the player inside about 4 m and look away after 2 to 3 s;
- a job loop for a role (a vendor straightens goods, counts money), a walk or wait loop for passers-by;
- crowds: instanced skinning, per-instance speed 0.8 to 1.2 [judgement] and phase (`game-3d/refs/crowds-and-lod.md`);
  0.6 m personal space [judgement], give way instead of overlapping (`game-3d/starter/learnings.md`);
- a vendor or companion reacts within 1 s when the player arrives, stops or leaves;
- the Playtester's 30 s watch: every NPC visibly does something (clip names from the hook).
- reaction ladder, zone mood, scenario points, sound from sources, spring layer and diegetic UI: `game-3d/refs/living-world.md`.

Test: the play hook exports each NPC's clip name and time; a unit test fails when two NPCs within 3 m share a clip and
a start time, or a clip plays longer than 12 s without a switch.

## 4. Accessibility

The floor is baseline rows 3, 4, 7 and 9 (Game Accessibility Guidelines, Basic tier); beyond it take the guidelines'
Intermediate list per game.

## 5. Test recipe

- Look math in a pure module with no renderer import (`applyLook(state, dx, dy, sens, invertY)` returns a new state,
  pitch clamped); Vitest covers clamp, invert, yaw wrap; idle choice takes the game's seeded RNG, never `Math.random`.
- Hooks: `window.__lookBy(dx, dy)` (deltas in mouse counts) and `render_game_to_text()` with yaw, pitch, position and
  NPC clips, so headless tests turn and walk without a pointer lock. A real lock is not verified in headless Chromium:
  the Playtester's blind pass uses the drag fallback and says so in `Not checked:`.
- Playtester checks: the table in the baseline, plus first reward and first goal inside the GDD's seconds.

## Sources (read 2026-11-12)

MDN Pointer Lock API; web.dev unadjusted mouse movement (https://web.dev/articles/disable-mouse-acceleration); the
controls sources are in the baseline. Onboarding window: vendor blogs only, not measured. No sourced numbers found for
NPC idle timing and gaze: §3 is our own [judgement].
