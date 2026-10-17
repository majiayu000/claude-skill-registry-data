---
name: game-loop-and-time
category: gameplay
description: Use when writing anything that moves, animates, counts down or simulates - per-frame vs fixed-step callbacks per engine, the accumulator loop with interpolation, delta-scaled smoothing, pause and time scale, and determinism.
tech_stack: Game core
source: informed by Glenn Fiedler's Gaffer on Games articles (Fix Your Timestep) and the engines' own docs; own wording
---
# Game Loop and Time

## Overview

Two clocks run in every game: the render frame (variable, as fast as the machine allows) and the simulation step (fixed, so physics and rules behave the same everywhere). Most "it moves faster on my machine", tunnelling, jitter and desync bugs come from putting work on the wrong clock or forgetting to scale by the right delta.

**Core principle:** Simulate on a fixed step, render with interpolation, and scale every time-based value by the delta of the clock it runs on.

## Where each clock lives

| Engine | Per frame (variable) | Fixed step | Default fixed rate |
|---|---|---|---|
| Unity | `Update`, `LateUpdate` — `Time.deltaTime` | `FixedUpdate` — `Time.fixedDeltaTime` | 0.02 s (50 Hz) |
| Godot | `_process(delta)` | `_physics_process(delta)` | 60 ticks/s (`physics/common/physics_ticks_per_second`) |
| Unreal | `Tick(DeltaSeconds)` | physics substepping / async physics tick | project physics settings |
| Bevy | `Update` — `Res<Time>` | `FixedUpdate` — `Res<Time>` is `Time<Fixed>` there | 64 Hz |
| Phaser | `update(time, delta)` (ms) | Arcade physics' own step (`fps`, `fixedStep`) | 60 |
| PixiJS 8 | `ticker.add(t => …)` — `t.deltaMS` | your accumulator | — |
| three.js / Babylon.js | `setAnimationLoop` + `THREE.Timer` / `engine.getDeltaTime()` (ms) | your accumulator, or the physics plugin's | — |
| MonoGame | `Update(GameTime)` | `IsFixedTimeStep = true` (default) | 1/60 s |
| pygame | `dt = clock.tick(60) / 1000` | your accumulator | — |

Use the engine's fixed callback for physics and authoritative rules. Write your own loop only where the engine has none (web renderers, pygame, custom servers).

## The accumulator loop (web, pygame, servers)

```ts
const STEP = 1 / 60;
const MAX_FRAME = 0.25;           // clamp: a 3 s tab-switch must not run 180 steps
let acc = 0;
let last = performance.now();

function frame(now: number) {
  const frameTime = Math.min((now - last) / 1000, MAX_FRAME);
  last = now;
  acc += frameTime;
  while (acc >= STEP) {
    previous.copyFrom(current);   // keep the last state for interpolation
    simulate(current, STEP);      // rules + physics, fixed dt only
    acc -= STEP;
  }
  render(interpolate(previous, current, acc / STEP));
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
```

- Clamp the frame time, or one long frame triggers the "spiral of death" (more steps → longer frame → more steps).
- Render the blend of the last two simulation states; without it, a 60 Hz simulation on a 144 Hz display stutters.
- Engines with a fixed callback offer interpolation too: Unity `Rigidbody.interpolation = Interpolate`, Godot `physics/common/physics_interpolation` (2D since 4.3, 3D since 4.4), Bevy interpolation crates or a manual `Time<Fixed>::overstep_fraction()` blend.

## Scale by delta — including smoothing

```csharp
// ❌ frame-rate dependent: twice as fast at 120 FPS, crawls at 30
transform.position += velocity;
camera.position = Vector3.Lerp(camera.position, target, 0.1f);

// ✅ delta-scaled; exponential smoothing that reads the same at any frame rate
transform.position += velocity * Time.deltaTime;
float t = 1f - Mathf.Exp(-sharpness * Time.deltaTime);
camera.position = Vector3.Lerp(camera.position, target, t);
```

```gdscript
# ❌ counts frames: a 1 s cooldown is 0.42 s at 144 FPS
var frames_left := 60
func _process(_delta: float) -> void:
    frames_left -= 1

# ✅ counts seconds
var cooldown_left := 1.0
func _process(delta: float) -> void:
    cooldown_left = maxf(0.0, cooldown_left - delta)
```

Acceleration needs care too: `velocity += accel * dt; position += velocity * dt` (semi-implicit Euler) is stable at a fixed step and drifts at a variable one — another reason to simulate on the fixed clock.

## Pause, slow motion and UI time

- Time scale slows the game, not the menus: Unity `Time.timeScale` with UI on `Time.unscaledDeltaTime`; Godot `Engine.time_scale` with pause menus on `process_mode = PROCESS_MODE_ALWAYS`; Bevy `Time<Virtual>` (pausable, scalable) vs `Time<Real>`; Unreal `SetGlobalTimeDilation` with UI ticking while paused.
- `timeScale = 0` stops `FixedUpdate` in Unity — anything that must run while paused (menus, input polling for "unpause") cannot live there.
- Pause on focus loss (`visibilitychange` on the web, `OnApplicationPause`, `NOTIFICATION_APPLICATION_FOCUS_OUT`), and clamp the first delta after resuming.

## Determinism, when the design needs it

Replays, lockstep RTS and rollback netcode need the same inputs to produce the same state on every machine:

- Fixed step only; no variable `dt` reaches the simulation.
- One seeded RNG owned by the simulation; cosmetic effects use a separate generator so they cannot shift the sequence.
- No iteration over hash maps or sets whose order is unspecified (use sorted keys, `IndexMap`, or arrays); no wall-clock reads inside a step.
- Floating point differs across compilers, CPUs and WASM vs native — use fixed-point math or keep all peers on one build and platform.
- Test it: same seed + same input log → same state hash after N steps.

## Testing time-based code

```ts
it("covers the same distance at 30 and 60 steps per second", () => {
  const a = new Mover({ speed: 5 }); for (let i = 0; i < 60; i++) a.step(1 / 60);
  const b = new Mover({ speed: 5 }); for (let i = 0; i < 30; i++) b.step(1 / 30);
  expect(a.x).toBeCloseTo(5, 5);
  expect(b.x).toBeCloseTo(a.x, 5);
});
```

Inject `dt`; never sleep in a test. Engine tests advance frames explicitly (`yield return new WaitForFixedUpdate()`, `runner.simulate_frames(n)`, `app.update()` with a manual time strategy).

## Common Mistakes

- Moving a rigidbody by writing its transform in `Update`/`_process` — it fights the physics step and tunnels.
- Reading input in `FixedUpdate`: a key pressed between two steps is missed. Read in the frame callback, consume in the fixed one.
- Delta in milliseconds treated as seconds (Phaser, PixiJS `deltaMS`, Babylon `getDeltaTime()`).
- PixiJS `ticker.deltaTime` is a frame-scaled factor (≈1 at 60 FPS), not seconds.
- A constant lerp factor for camera smoothing.

## Red Flags

- `frameCount`, `% 60` or a frame counter used as a timer.
- `Time.time` / `performance.now()` inside a rule class.
- A physics fix done by raising the frame cap or relying on vsync.
