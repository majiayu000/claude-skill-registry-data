---
name: csp-lua
description: CSP (Custom Shaders Patch) Lua API reference for Assetto Corsa modding. Use when working with ac.*, ui.*, render.*, physics.* APIs or any CSP Lua code.
---

# CSP Lua API Reference Skill

Use this skill when working with CSP (Custom Shaders Patch) Lua code for Assetto Corsa.

## Development Rules

**NEVER use shell commands or external tools** (`io.popen`, `os.execute`, etc.) to solve problems. CSP provides comprehensive APIs for most tasks.

Before implementing any functionality:
1. **Check `reference/lib.lua`** in this skill folder for existing CSP APIs
2. Use CSP's built-in functions (e.g., `io.scanDir` instead of `dir` command)
3. Only fall back to shell if absolutely no CSP API exists

## Key File System APIs

From `reference/lib.lua`:
- `io.scanDir(directory, "*.csv")` - List files matching a pattern
- `io.dirExists(path)` - Check if directory exists
- `io.fileExists(path)` - Check if file exists
- `io.fileSize(path)` - Get file size in bytes (-1 on error)
- `io.getAttributes(path)` - Get file attributes (fileSize, creationTime, lastWriteTime, etc.)

## Track Information

### `ac.getTrackID()`
Returns the track identifier string (e.g., "ks_brands_hatch-gp", "daytona").

```lua
local trackId = ac.getTrackID()
-- Returns: "ks_brands_hatch-gp"
```

**Note:** `ac.getSim().trackId` does NOT exist. Use `ac.getTrackID()` instead.

### `ac.getTrackDataFilename(filename)`
Returns the full path to a file in the track's data folder.

```lua
local path = ac.getTrackDataFilename('traffic.json')
```

### `ac.getSim()`
Returns `ac.StateSim` reference with information about the simulation state.

Key fields:
- `sim.dt` - Delta time in seconds (0 when paused, affected by replay speed)
- `sim.isPaused` - Simulation is paused
- `sim.isOnlineRace` - True if in an online session
- `sim.trackLengthM` - Track length in meters
- `sim.time` - Total time in milliseconds since AC started
- `sim.gameTime` - Total time in seconds since AC started
- `sim.sessionTimeLeft` - Remaining session time in ms
- `sim.currentSessionIndex` - 0-based session index
- `sim.rainIntensity` - Current rain intensity (0-1)
- `sim.roadGrip` - Current track grip (0-1)
- `sim.connectedCars` - Number of connected players (online)

### Spline & World Coordinates
- `ac.worldCoordinateToTrackProgress(vec3)` - Converts world position to spline position (0-1)
- `ac.trackProgressToWorldCoordinate(pos, linear)` - Converts spline position to world position
- `ac.getTrackSectorName(pos)` - Returns the name of the sector at given spline position

## Car Information

### `ac.getCar(index)`
Returns `ac.StateCar` for the specified car index (0 = player).

Key fields:
- `car.id` - Car identifier string
- `car.speedKmh` - Speed in km/h
- `car.splinePosition` - Position on track (0-1)
- `car.lapCount` - Number of completed laps
- `car.lapTimeMs` - Current lap time in milliseconds
- `car.bestLapTimeMs` - Best lap time in this session (ms)
- `car.gas` - Throttle (0-1)
- `car.brake` - Brake (0-1)
- `car.clutch` - Clutch (0-1, 1 = fully depressed)
- `car.steer` - Steering angle in degrees
- `car.gear` - Current gear (0 = N, -1 = R)
- `car.handbrake` - Handbrake (0-1)
- `car.isLapValid` - True if current lap is considered valid by AC
- `car.resetCounter` - Increments each time car is reset (teleported)
- `car.lastLapCutsCount` - Number of cuts in the last lap
- `car.collisionDepth` - Depth of current collision in meters
- `car.isInPitlane` - True if in pitlane area
- `car.racePosition` - Current position in session/race

### Car Events
- `ac.onTrackPointCrossed(carIndex, progress, callback)` - Triggered when car crosses a specific spline point
- `ac.onCarCollision(carIndex, callback)` - Triggered on collision
- `ac.onCarJumped(carIndex, callback)` - Triggered when car jumps

## Hotkeys

### `ac.ControlButton(name, defaults)`
Creates a bindable hotkey control.

```lua
local myButton = ac.ControlButton('ac-tracer/MyHotkey', {
    keyboard = { key = ui.KeyIndex.T, ctrl = true },
    gamepad = ac.GamepadButton.Y
})

-- Check if pressed this frame
if myButton:pressed() then ... end

-- Check if currently held
if myButton:down() then ... end

-- Render binding control in settings (UI function)
myButton:control(vec2(120, 0))
```

## Storage

### `ac.storage(layout, prefix)` - PREFERRED
Advanced persistent storage with default values and automatic synchronization. **This is the recommended approach.**

```lua
-- Define layout with defaults (at module level)
local config = ac.storage{
    showTraces = true,
    autoHide = false,
    hideSpeed = 20,
    colorOwn = rgb(0.2, 0.2, 0.2)
}

-- Access/Modify (automatically persists on assignment)
if ui.checkbox('Show traces', config.showTraces) then
    config.showTraces = not config.showTraces  -- Auto-saved!
end

config.hideSpeed = ui.slider('##speed', config.hideSpeed, 0, 100, 'Speed: %.0f')
```

Values can be: strings, numbers, booleans, vectors (vec2/vec3/vec4), colors (rgb/rgbm).

**Note:** Direct access `ac.storage[key] = value` only supports strings and requires manual serialization. Avoid this pattern - use the table-based approach instead.

### SDK Examples
See working examples in other CSP apps:
- `apps/lua/Radar/Radar.lua` - Simple config with checkboxes, sliders, colors
- `apps/lua/CSPDataLogger/CSPDataLogger.lua` - Basic boolean/number settings

## Logging & UI

### `ac.log(message)`
Writes to CSP log.

### `ac.setMessage(title, description)`
Shows a toast-style message in the game UI.

### `ac.lapTimeToString(ms, allowHours)`
Utility to format milliseconds into "M:SS.ms" format.

## UI & Windows

### Window Types

Prefer these wrappers over `ui.beginWindow` / `ui.endWindow` as they handle crashes gracefully and provide standard styling.

#### `ui.toolWindow(id, pos, size, noPadding, inputs, content)`
Standard app window with background. Best for main app windows.

```lua
function script.windowMain(dt)
    ui.toolWindow('MyAppMain', vec2(100, 100), vec2(400, 300), false, true, function()
        -- Window content here
        ui.text("Hello World")
    end)
end
```

#### `ui.transparentWindow(id, pos, size, noPadding, inputs, content)`
Window with no background. Best for HUD overlays or non-intrusive elements.

```lua
function script.windowHUD(dt)
    -- Transparent, pass-through inputs unless interactive
    ui.transparentWindow('MyAppHUD', vec2(0, 0), ui.windowSize(), true, false, function()
        ui.textColored("HUD Overlay", rgbm.colors.red)
    end)
end
```

### Layout Best Practices

#### Scrollable Areas (`ui.beginChild`)
Use child windows for scrollable content lists.

```lua
-- Reserve 30px at bottom for footer
ui.beginChild('ScrollableList', vec2(0, -30), false, ui.WindowFlags.None)
    for i = 1, 100 do
        ui.text("Item " .. i)
    end
ui.endChild()

-- Footer (pinned to bottom due to child height reservation)
ui.button("Close", vec2(-1, 0)) -- -1 width = full width
```

#### Grouping & Layout
- `ui.beginGroup()` / `ui.endGroup()`: Group items to treat them as one for hover checks or same-line layout.
- `ui.sameLine(offset, spacing)`: Place next item on the same horizontal line.
- `vec2(-1, 0)`: Use as size to fill remaining horizontal space.

#### Styling
Use `ui.pushFont`, `ui.pushStyleVar`, and `ui.pushStyleColor` to customize look, but ALWAYS pair with `ui.pop...`.

```lua
ui.pushFont(ui.Font.Title)
ui.text("Title")
ui.popFont()

ui.pushStyleVar(ui.StyleVar.Alpha, 0.5)
ui.button("Dimmed Button")
ui.popStyleVar()
```

## Settings Integration

### `ui.addSettings(params, callback)`
Registers a settings window accessible via the taskbar context menu or settings apps.

```lua
ui.addSettings({
    name = "My App Settings",
    id = "MyAppSettings",
    icon = ui.Icons.Settings,
    size = {
        default = vec2(400, 300),
        min = vec2(300, 200)
    }
}, function()
    ui.header("General Options")

    if ui.checkbox("Enable Feature", state.enabled) then
        state.enabled = not state.enabled
    end

    ui.separator()

    ui.header("Visuals")

    local newVal, changed = ui.slider("Opacity", state.opacity, 0, 1, "%.2f")
    if changed then state.opacity = newVal end

    ui.combo("Mode", state.mode, ui.ComboFlags.None, function()
        if ui.selectable("Mode A", state.mode == "A") then state.mode = "A" end
        if ui.selectable("Mode B", state.mode == "B") then state.mode = "B" end
    end)

    ui.text("Toggle Key:")
    ui.sameLine()
    myBindableHotkey:control(vec2(-1, 0))
end)
```

### Window Visibility & Management

Use `ac.getAppWindows()` to list all windows and check their status, and `ac.accessAppWindow()` to modify them.

#### `ac.getAppWindows()`
Returns an array of descriptors for all available windows.

```lua
local windows = ac.getAppWindows()
for _, w in ipairs(windows) do
    ac.log(string.format("Window: %s, Visible: %s", w.name, tostring(w.visible)))
end
```

#### `ac.accessAppWindow(windowName)`
Returns an `ac.AppWindowAccessor` for the specified window name.

```lua
local window = ac.accessAppWindow("ac-tracer/corners")
if window and window:valid() then
    window:setVisible(true)
end
```

#### `ac.setAppWindowVisible(appID, windowFilter, visible)`
Toggle windows that might be hidden or not yet initialized.

```lua
ac.setAppWindowVisible("ac-tracer", "telemetry", true)
```

## Full API Reference

For the complete API reference with all types, enums, and functions, read the file `reference/lib.lua` in this skill folder (17,000+ lines of type definitions and documentation).

## Scripts

### `scripts/logs.ps1`
View CSP logs filtered for ac-tracer entries.

```powershell
# Default: last 20 entries
.\.claude\skills\scripts\logs.ps1

# Last 50 entries
.\.claude\skills\scripts\logs.ps1 -l 50

# Only errors
.\.claude\skills\scripts\logs.ps1 -only ERROR

# Only warnings
.\.claude\skills\scripts\logs.ps1 -only WARN
```
