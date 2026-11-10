---
name: godot-presentation
description: Conventions for the Godot layer (IronPipeline.Game) — no rules here, pointy-top hex layout math, how scenes consume Sim state and events and submit Commands, project structure. Load before touching anything under src/IronPipeline.Game.
---
# Godot presentation layer

`src/IronPipeline.Game` renders `GameState` and turns input into `Command`s. **It contains no game rules.** If you find yourself computing legality, cost, damage or supply here, stop: that is a Sim query or Command.

## Talking to the Sim
- Hold one `GameState` in a `GameSession` node (autoload). Apply commands via `Rules.Apply`; replace the state; emit a Godot signal with the returned events.
- Views subscribe to events (`UnitMoved`, `CombatResolved`, …) and animate. They never diff state to guess what happened.
- Highlights (reachable hexes, valid targets) come from Sim queries (`Reachable`, `CanAttack`), not from UI-side math.
- Floats are fine here (positions, tweens, camera). They are never passed back into the Sim.

## Pointy-top layout (ADR 0004)
Size `s` = center-to-corner pixels.
```
x = s * (sqrt(3) * q + sqrt(3)/2 * r)
y = s * (3/2 * r)
corner_i = center + s * (cos(60°·i − 30°), sin(60°·i − 30°))   // i = 0..5
```
Pixel → hex: invert, then cube-round (same rounding as `HexCoord.LineTo`, implemented once in a `HexLayout` helper in the Game project).
Godot `TileMapLayer` with a `TileSet` of `tile_shape = Hexagon`, `tile_offset_axis = Horizontal` matches pointy-top; use it for terrain, draw units as counters on top.

## Project conventions
- `scenes/` one `.tscn` per screen or reusable view; `scripts/` the matching `partial class : Node…`.
- Counters are programmatic (`_Draw`) until the asset pipeline exists; never hand-place art.
- UI text comes from a `Strings` resource so later localisation is a data change.
- Export presets are named `Linux` and `Windows` (build.yml depends on it).

## Testing here
GdUnit4 (C#) scene tests for wiring only: scene loads, a click produces the expected Command, an event produces the expected highlight. Feel is tested by humans via the playtest checklist.
