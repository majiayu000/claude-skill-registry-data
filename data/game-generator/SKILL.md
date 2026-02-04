---
name: game-generator
description: Generate GameSpec JSON and Lua scripts for the AI Game Platform. Use when creating games, adding features like player movement, enemies, collectibles, or fixing Lua script issues. Supports FPS, 2D side-scrollers, and 3D platformers.
---

# Game Generator

Assists in generating valid GameSpec JSON + Lua scripts for the AI Game Platform.

## When to Use

- User requests a new game ("create a platformer game")
- User wants to add features ("add enemies that patrol")
- User wants to modify Lua scripts ("make the player jump higher")
- User asks about game mechanics ("how do I implement collectibles?")

## Instructions

### 1. Understand the Request

Identify the game type:
- **FPS**: First-person shooter with mouse look
- **2D Side-Scroller**: Horizontal movement, jumping
- **3D Platformer**: Top-down or angled view, WASD movement

### 2. Generate GameSpec Structure

```typescript
{
  "meta": { "title": "Game Title", "version": "1.0.0" },
  "players": { "min": 1, "max": 1, "spawn_points": [{ "x": 0, "y": 1, "z": 0 }] },
  "worlds": [{
    "id": "world-1",
    "name": "Main World",
    "environment": {
      "ambient_light": { "color": "#ffffff", "intensity": 0.5 },
      "directional_light": { "color": "#ffffff", "intensity": 1, "position": { "x": 10, "y": 10, "z": 10 } }
    },
    "objects": [/* GameObjects */]
  }],
  "scripts": [/* Lua scripts */]
}
```

### 3. Create GameObjects

Each GameObject needs:
- **Unique ID**: `"obj-player-1"`, `"obj-enemy-1"`
- **Transform**: position, rotation (radians), scale
- **Components**: mesh, light, or camera
- **Optional script_id**: Reference to Lua script

#### Mesh Component (Required for Visuals)

```json
{
  "type": "mesh",
  "properties": {
    "geometry": "box|sphere|plane|cylinder",
    "color": 0xff0000,
    "width": 1, "height": 1, "depth": 1,
    "hasCollision": true,
    "collisionShape": "box|sphere|auto",
    "isTrigger": false
  }
}
```

**IMPORTANT:** Set `hasCollision: true` for physics interaction!

#### Camera Component

```json
{
  "type": "camera",
  "properties": {
    "fov": 75,
    "isMainCamera": true,
    "usePointerLock": false  // true for FPS, false for 2D/platformer
  }
}
```

### 4. Write Lua Scripts

#### Essential Pattern for Transform Updates

```lua
function on_update(dt)
  -- ALWAYS use this pattern:
  local pos = gameobject.transform.position
  pos.x = pos.x + speed * dt
  gameobject.transform.position = pos  -- Must reassign!
end
```

#### Input Handling

```lua
function on_update(dt)
  if not input then return end  -- Optional safety check
  
  if input["w"] or input["arrowup"] then
    -- Move forward
  end
  if input[" "] then  -- Space key
    -- Jump
  end
end
```

**Available Keys:**
- `input["w"]`, `input["a"]`, `input["s"]`, `input["d"]`
- `input["arrowup"]`, `input["arrowdown"]`, `input["arrowleft"]`, `input["arrowright"]`
- `input[" "]` (space), `input["shift"]`, `input["control"]`

#### Jump with Edge Detection

```lua
local velocity_y = 0
local was_space_pressed = false

function on_update(dt)
  if not input then return end
  
  local is_space_pressed = input[" "] == true
  if is_grounded and is_space_pressed and not was_space_pressed then
    velocity_y = jump_force
  end
  was_space_pressed = is_space_pressed
  
  velocity_y = velocity_y + gravity * dt
  pos.y = pos.y + velocity_y * dt
end
```

#### Find Other GameObjects

```lua
function on_update(dt)
  local player = find_gameobject("Player")
  if player then
    local dx = player.transform.position.x - gameobject.transform.position.x
    -- Use dx for AI, camera following, etc.
  end
end
```

#### Collision Callbacks

```lua
function on_collision(other)
  -- Solid collision (walls, floor)
  if other.name == "Wall" then
    print("Hit wall")
  end
end

function on_trigger_enter(other)
  -- Trigger collision (items, goals)
  if other.name == "Coin" then
    print("Collected!")
  end
end
```

### 5. Common Patterns

#### 2D Side-Scroller Player

```lua
local velocity_y = 0
local gravity = -15
local jump_force = 7
local move_speed = 5
local is_grounded = false
local was_space_pressed = false

function on_update(dt)
  if not input then return end
  
  local pos = gameobject.transform.position
  
  -- Horizontal movement
  if input["arrowleft"] or input["a"] then
    pos.x = pos.x - move_speed * dt
  end
  if input["arrowright"] or input["d"] then
    pos.x = pos.x + move_speed * dt
  end
  
  -- Jump
  local is_space_pressed = input[" "] == true
  if is_grounded and is_space_pressed and not was_space_pressed then
    velocity_y = jump_force
    is_grounded = false
  end
  was_space_pressed = is_space_pressed
  
  -- Gravity
  velocity_y = velocity_y + gravity * dt
  pos.y = pos.y + velocity_y * dt
  
  -- Ground check
  if pos.y <= 0.6 then
    pos.y = 0.6
    velocity_y = 0
    is_grounded = true
  end
  
  gameobject.transform.position = pos
end
```

#### FPS Mouse Look

```lua
local rotation_y = 0
local mouse_sensitivity = 0.002

function on_update(dt)
  if mouse_movement then
    rotation_y = rotation_y - mouse_movement.x * mouse_sensitivity
  end
  
  gameobject.transform.rotation.y = rotation_y
end
```

**Camera must have:** `"usePointerLock": true`

#### Enemy Patrol

```lua
local patrol_distance = 3
local start_x = 0
local direction = 1
local speed = 2

function on_start()
  start_x = gameobject.transform.position.x
end

function on_update(dt)
  local pos = gameobject.transform.position
  pos.x = pos.x + direction * speed * dt
  
  if pos.x > start_x + patrol_distance then direction = -1 end
  if pos.x < start_x - patrol_distance then direction = 1 end
  
  gameobject.transform.position = pos
end
```

#### Collectible Item

```lua
local rotation_speed = 3
local collected = false

function on_update(dt)
  if collected then
    gameobject.transform.position.y = -100  -- Hide
    return
  end
  
  local rot = gameobject.transform.rotation
  rot.y = rot.y + rotation_speed * dt
  gameobject.transform.rotation = rot
end

function on_trigger_enter(other)
  if other.name == "Player" and not collected then
    collected = true
    print("Collected!")
  end
end
```

## Checklist

Before generating GameSpec:

- [ ] All GameObjects have unique IDs
- [ ] Main camera exists with `isMainCamera: true`
- [ ] Camera has correct `usePointerLock` (true for FPS, false for 2D)
- [ ] Lights are configured (ambient + directional/point)
- [ ] Collision objects have `hasCollision: true`
- [ ] Triggers have `isTrigger: true`
- [ ] Script IDs reference existing ScriptDefinitions
- [ ] Lua scripts use correct Transform update pattern
- [ ] Input handling includes safety check `if not input then return end`

## Common Mistakes to Avoid

1. ❌ `gameobject.transform.position.x = x + 1` → ✅ Use local variable pattern
2. ❌ Forgetting `hasCollision: true` → Objects pass through each other
3. ❌ `usePointerLock: true` for 2D games → Breaks keyboard input
4. ❌ Jump without edge detection → Continuous jumping
5. ❌ Not multiplying by `dt` → Frame-rate dependent movement

## Reference

For detailed API reference, see:
- [Lua API Documentation](../../../docs/lua-api.md)
- [GameSpec Type Definitions](../../../lib/types/gamespec.ts)
- [Template Examples](../../../lib/templates/)
