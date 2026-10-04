---
name: sprite-fps
description: >
  Every sprite sheet in this game animates at 24fps, and drawn clips
  play at the speed they were drawn at. Applies whenever writing or
  reviewing animation code — pokemon sheets, effect and particle
  atlases, overworld characters — or converting a frame count into
  milliseconds.
---

**All sprites are 24fps.** A sheet's durations are counted in ticks, and one tick is `SPRITE_TICK` — `1000 / SPRITE_FPS` in [`src/canvas/sprite-sheet.ts`](../../../src/canvas/sprite-sheet.ts). Pokemon sheets, effect and particle atlases and overworld characters all count in that same tick.

## Rules

- **Never write a frame time as a literal.** `SPRITE_TICK * frames`, not `16.67 * frames`, `1000 / 60`, or a milliseconds figure worked out by hand. The same goes for tests: assert against `SPRITE_TICK`, or against the clip's own `length`/`duration`.
- **Do not confuse it with the battle clock.** The engine ticks at 60fps and its timings — cast windows, cooldowns, move delays — are unrelated. A sprite tick is about how a drawing was animated, not how the fight is simulated.
- **Clips play at their own speed by default.** A hand-drawn clip has a pace, and that pace is most of what it looks like. Play it and let it run.
- **Stretch only where something must line up.** A caster's throw is fitted to the window its move is in the air, so the gesture ends as the hit lands. That is the exception, not the habit.
- **Effects are never stretched.** A spark, a shockwave, a puff of smoke plays at its drawn speed. A beat's span says when the next beat starts and how long this one is drawn for; a span longer than the clip holds its last frame rather than slowing the clip down.
- **Looping clips repeat rather than stretch** — see `isLoopingCast`. Filling a long window with one slow pass reads as the game hanging.

## Why 24

These are hand-drawn animations of a few frames each. Run at the sixty a second the battle ticks at, a ten-frame clip is over in a sixth of a second and reads as a flicker. At 24 the same clip takes 833ms and reads as a movement.

## Converting

```ts
// Bad — a magic number, and wrong the moment the rate changes
sprite.advance(16.67 * 8);
expect(sprite.duration).toBeCloseTo(650);

// Good — counted in what the sheets are counted in
sprite.advance(SPRITE_TICK * 8);
expect(sprite.duration).toBeCloseTo(sprite.length * SPRITE_TICK);
```
