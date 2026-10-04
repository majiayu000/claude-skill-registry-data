---
name: love2d-core
description: >
  Structure and debug a LÖVE (Love2D) game in Lua: the love.load/update/draw loop,
  delta-time movement, input, and screen states. Use when building a LÖVE 11.x game
  (main.lua, conf.lua, .love).
---

# LÖVE (Love2D) Core

Set up and debug the foundation of a LÖVE game in Lua: the callback loop, frame-rate-
independent movement, input, and screen states. Targets **LÖVE 11.5**.

## When to use

- Use when starting a LÖVE game, wiring up `main.lua`/`conf.lua`, or fixing the core loop,
  movement that runs at the wrong speed, input handling, or screen switching.
- Use when the workspace has `main.lua` calling `love.*`, a `conf.lua`, or a `.love` file.

**When *not* to use:** Lua *language* questions unrelated to LÖVE; physics bodies/joints
(LÖVE uses Box2D via `love.physics` — a separate concern); shader code (`love.graphics`
GLSL is its own topic). For cross-engine save/load patterns, use `save-systems`.

## Core workflow

1. **Confirm the entry points.** A LÖVE game runs `main.lua`; it should define
   `love.load()` (one-time setup), `love.update(dt)` (state), and `love.draw()` (rendering).
   Window/version setup goes in `conf.lua` (run *before* modules load).
2. **Pin the version.** Set `t.version = "11.5"` in `conf.lua` so LÖVE warns on mismatch.
3. **Drive all motion by `dt`** (delta time, in seconds) so speed is frame-rate independent.
4. **Handle input** two ways: polled (`love.keyboard.isDown` in `update`, for held keys) and
   event (`love.keypressed` callback, for discrete presses).
5. **Manage screens** (menu, game, pause) with a small state stack rather than a pile of
   `if` flags — see Patterns and `references/state-stack.md`.
6. **Run and observe.** Launch with `love .` from the project folder; verify the window,
   motion speed, and input on screen before assuming it works.

## Patterns

### 1. `main.lua` skeleton (the callback loop + input)

```lua
-- main.lua — LÖVE calls these callbacks for you. Colors are 0–1 in LÖVE 11.x.
function love.load()
    -- One-time setup. speed is in PIXELS PER SECOND, not per frame.
    player = { x = 100, y = 100, size = 40, speed = 220 }
    love.graphics.setBackgroundColor(0.1, 0.1, 0.12)
end

function love.update(dt)
    -- Polled input: good for continuous movement while a key is held.
    if love.keyboard.isDown("right") then player.x = player.x + player.speed * dt end
    if love.keyboard.isDown("left")  then player.x = player.x - player.speed * dt end
    if love.keyboard.isDown("down")  then player.y = player.y + player.speed * dt end
    if love.keyboard.isDown("up")    then player.y = player.y - player.speed * dt end
end

function love.draw()
    love.graphics.setColor(0.2, 0.8, 1.0)                 -- tint ON
    love.graphics.rectangle("fill", player.x, player.y, player.size, player.size)
    love.graphics.setColor(1, 1, 1)                       -- reset tint before text/images
    love.graphics.print("Arrow keys to move, Esc to quit", 10, 10)
end

function love.keypressed(key)
    -- Event input: fires once per physical press. Use for menus, jumps, toggles.
    if key == "escape" then love.event.quit() end
end
```

### 2. Frame-rate independence (the single most common bug)

```lua
-- RIGHT: scaled by dt → same real-world speed at 30 or 240 FPS.
player.x = player.x + player.speed * dt
-- WRONG: "pixels per frame" → moves twice as fast at double the frame rate.
player.x = player.x + player.speed
```

### 3. `conf.lua` (window + version; runs before `main.lua`)

```lua
-- conf.lua — must be its own file; love.conf will NOT run from main.lua.
function love.conf(t)
    t.version = "11.5"             -- the LÖVE version this game targets (string "X.Y")
    t.window.title  = "My LÖVE Game"
    t.window.width  = 800
    t.window.height = 600
    t.window.vsync  = 1            -- number since 11.0: 1 = on, 0 = off, -1 = adaptive
    t.window.resizable = false
    t.modules.physics = false      -- disable modules you don't use to trim startup/memory
end
```

### 4. Color is 0–1 in LÖVE 11.x (not 0–255)

```lua
-- LÖVE 11.x uses normalized floats. (Pre-11.0 code used 0–255 and will look wrong.)
love.graphics.setColor(1, 0, 0)                          -- opaque red
love.graphics.setColor(0.2, 0.8, 1.0, 0.5)               -- translucent cyan (alpha 0.5)
-- Need to convert old byte values? Use the helper instead of dividing by hand:
love.graphics.setColor(love.math.colorFromBytes(128, 234, 255))
```

### 5. Screen states (brief — full manager in references)

```lua
-- A screen is a table with optional :update(dt), :draw(), :keypressed(key).
-- Keep the active screen on a stack so pause/menu overlays are trivial to pop.
local Stack = require("state_stack")   -- see references/state-stack.md for the module
function love.load()              Stack.push(require("screens.menu")) end
function love.update(dt)          Stack.current():update(dt) end
function love.draw()              Stack.current():draw() end
function love.keypressed(key)     Stack.current():keypressed(key) end
```

## Pitfalls

- **Speed varies with FPS** → you forgot `* dt`. Every per-frame change to position, timers,
  or animation must be scaled by `dt`.
- **`love.conf` placed in `main.lua`** → it silently does nothing. It must live in `conf.lua`,
  which LÖVE runs *before* loading modules.
- **Colors washed out or invisible** → you used 0–255 values. In 11.x, `setColor(255,0,0)`
  clamps to white; use `setColor(1,0,0)` or `love.math.colorFromBytes`.
- **Everything tinted after one `setColor`** → color is global and persists across draws.
  Reset with `love.graphics.setColor(1, 1, 1)` before drawing text/images you want untinted.
- **Nothing happens on key release/repeat** → `love.keypressed(key, scancode, isrepeat)`
  fires on press (and OS key-repeat); use `love.keyreleased` for release, and check
  `isrepeat` if you must ignore held-key repeats.

## References

- For a complete push/pop screen-state manager (menu → game → pause, with delegated
  callbacks), read `references/state-stack.md`.

## Related skills

- `save-systems` — saving/loading game state (engine-agnostic).
- `input-systems` — rebindable, multi-device input architecture.
- `pygame-core` / `phaser-core` — the same loop concepts in other lightweight engines.
