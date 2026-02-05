---
name: unity-editor-operations
description: "Use this skill when operating Unity Editor. Supports creating/modifying GameObjects, transforms, materials, scenes, prefabs, lights, cameras, UI, and terrain via JSON commands. MUST invoke first to get correct command format before executing."
---

# Unity Editor Operations Skill

## Overview

This skill enables Unity Editor operations through JSON commands. Commands are sent via `send_message.py` to Unity Command Server and executed immediately with results returned.

**Architecture:**
```
Claude Code (this side - Agent)
  ↓ JSON command
send_message.py (WebSocket client)
  ↓ ws://127.0.0.1:8766
Unity Command Server (simple executor)
  ↓
CommandExecutor
  ↓
Unity Editor Operations
  ↓ JSON result
send_message.py
  ↓
Claude Code (receives result)
```

## Quick Start

### 1. Open Unity Command Server
In Unity Editor: `Tools > ClaudeAgent > Unity Command Server`

### 2. Send Command
```bash
python .claude/skills/unity-editor-operations/send_message.py '{"operation":"create_primitive","params":{"type":"sphere","name":"MySphere","color":"red"}}'
```

### 3. Check Result
```
✓ Connected to ws://127.0.0.1:8766/
📤 Sending: {"operation":"create_primitive",...}
⏳ Waiting for response (timeout: 10s)...

✓ Command executed successfully
   Time: 2025-11-25 18:00:00
```

## send_message.py Usage

Located at: `.claude/skills/unity-editor-operations/send_message.py`

```bash
python send_message.py '<json_command>'
```

**Features:**
- WebSocket connection to Unity Command Server
- 10 second timeout
- JSON result parsing and display
- Exit code: 0 (success) / 1 (failure)

**Response Format:**
```json
{
  "success": true,
  "result": { ... },
  "timestamp": "2025-11-25 12:00:00"
}
```

## JSON Command Format

```json
{
  "operation": "operation_name",
  "params": {
    "param1": "value1",
    "param2": "value2"
  }
}
```

## Common Parameters

### Space Parameters

Several operations support `position_space`, `rotation_space`, and `scale_space` parameters:

| Parameter | Values | Default |
|-----------|--------|---------|
| `position_space` | "local" / "world" | "world" if no parent, "local" if parent specified |
| `rotation_space` | "local" / "world" | "world" if no parent, "local" if parent specified |
| `scale_space` | "local" / "world" | "world" if no parent, "local" if parent specified |

**Applies to:** `create_primitive`, `create_empty`, `create_line`, `instantiate_prefab`, `create_terrain`

Result messages show which space was used: `Created sphere: MySphere (position: world, scale: local)`

## Supported Operations (60 total)

> **Looking up operation details**: Use `Grep "### operation_name" File.md -A 25` to retrieve only the specific operation section instead of reading the entire file. This reduces token consumption.

### GameObject Operations
| Operation | Description |
|-----------|-------------|
| `create_primitive` | [Create sphere, cube, etc.](GameObject.md#create_primitive) ※VGM: markers only |
| `create_empty` | [Create empty GameObject](GameObject.md#create_empty) |
| `delete_gameobject` | [Delete by path/name](GameObject.md#delete_gameobject) |
| `set_active` | [Set active state](GameObject.md#set_active) |
| `tag` | [Get/set tag (unified)](GameObject.md#tag) |
| `create_tag` | [Create new tag in project](GameObject.md#create_tag) |
| `delete_tag` | [Delete custom tag from project](GameObject.md#delete_tag) |
| `find_gameobject` | [Find and return info](GameObject.md#find_gameobject) |
| `set_name` | [Rename](GameObject.md#set_name) |
| `set_parent` | [Set parent-child relationship](GameObject.md#set_parent) |
| `duplicate_gameobject` | [Duplicate](GameObject.md#duplicate_gameobject) |
| `look_at` | [Orient towards target](GameObject.md#look_at) |
| `create_line` | [Create line between two points](GameObject.md#create_line) |

### Transform Operations
| Operation | Description |
|-----------|-------------|
| `transform` | [Get/set position, rotation, scale (unified)](Transform.md#transform) |

### Component Operations
| Operation | Description |
|-----------|-------------|
| `add_component` | [Add component](Component.md#add_component) |
| `remove_component` | [Remove component](Component.md#remove_component) |
| `get_component` | [Get component info](Component.md#get_component) |
| `set_component_property` | [Set property value](Component.md#set_component_property) |
| `get_components` | [List all components](Component.md#get_components) |
| `set_object_reference` | [Set GameObject/Component reference](Component.md#set_object_reference) |

### Material Operations
| Operation | Description |
|-----------|-------------|
| `material` | [Get/set material properties (unified)](Material.md#material) |
| `create_material` | [Create new material](Material.md#create_material) |

### Scene Operations
| Operation | Description |
|-----------|-------------|
| `open_scene` | [Open scene](Scene.md#open_scene) |
| `save_scene` | [Save scene](Scene.md#save_scene) |
| `create_scene` | [Create new scene](Scene.md#create_scene) |
| `get_scene_hierarchy` | [Get hierarchy structure](Scene.md#get_scene_hierarchy) |
| `get_active_scene` | [Get active scene info](Scene.md#get_active_scene) |

### Asset Operations
| Operation | Description |
|-----------|-------------|
| `create_asset` | [Create text asset](Asset.md#create_asset) |
| `delete_asset` | [Delete asset](Asset.md#delete_asset) |
| `get_asset` | [Get asset info](Asset.md#get_asset) |
| `import_asset` | [Re-import asset](Asset.md#import_asset) |
| `refresh_assets` | [Refresh AssetDatabase](Asset.md#refresh_assets) |
| `copy_asset` | [Copy asset](Asset.md#copy_asset) |
| `import_package` | [Import .unitypackage file](Asset.md#import_package) |
| `list_assets` | [List assets in folder](Asset.md#list_assets) |

### Prefab Operations
| Operation | Description |
|-----------|-------------|
| `create_prefab` | [Create from GameObject](Prefab.md#create_prefab) |
| `instantiate_prefab` | [Instantiate into scene](Prefab.md#instantiate_prefab) |
| `open_prefab` | [Open in edit mode](Prefab.md#open_prefab) |
| `save_prefab` | [Save prefab](Prefab.md#save_prefab) |

### Debugging Operations
| Operation | Description |
|-----------|-------------|
| `logs` | [Get console logs (unified: all, errors, statistics)](Debugging.md#logs) |
| `clear_logs` | [Clear console logs](Debugging.md#clear_logs) |

### Light Operations
| Operation | Description |
|-----------|-------------|
| `create_light` | [Create light](Light.md#create_light) |
| `light` | [Get/set light properties (unified)](Light.md#light) |

### Camera Operations
| Operation | Description |
|-----------|-------------|
| `create_camera` | [Create camera](Camera.md#create_camera) |
| `camera` | [Get/set camera properties (unified)](Camera.md#camera) |

### Screenshot Operations
| Operation | Description |
|-----------|-------------|
| `capture_scene_view` | [Capture scene screenshot](Screenshot.md#capture_scene_view) |

### UI Operations
| Operation | Description |
|-----------|-------------|
| `create_canvas` | [Create canvas](UI.md#create_canvas) |
| `create_ui` | [Create UI elements (button, text, image, panel, inputfield, scrollview)](UI.md#create_ui) |
| `ui` | [Get/set UI properties (unified)](UI.md#ui) |

### Editor Operations
| Operation | Description |
|-----------|-------------|
| `execute_menu_item` | [Execute menu item](Editor.md#execute_menu_item) |
| `get_editor_state` | [Get editor state](Editor.md#get_editor_state) |
| `get_selection` | [Get selected objects](Editor.md#get_selection) |
| `set_selection` | [Select object](Editor.md#set_selection) |
| `playmode` | [Play mode control (play/stop/pause/resume)](Editor.md#playmode) |

### Animator Operations
| Operation | Description |
|-----------|-------------|
| `create_animator_controller` | [Create AnimatorController asset](Animator.md#create_animator_controller) |
| `create_animator_element` | [Create state/layer/parameter/transition/blend_tree](Animator.md#create_animator_element) |
| `delete_animator_element` | [Delete state/layer/parameter/transition](Animator.md#delete_animator_element) |
| `animator_element` | [Get/set state/layer/parameter/blend_tree properties](Animator.md#animator_element) |
| `animator` | [Runtime parameter value get/set](Animator.md#animator) |

### Terrain Operations
| Operation | Description |
|-----------|-------------|
| `create_terrain` | [Create terrain](Terrain.md#create_terrain) |
| `add_terrain_layer` | [Add texture layer](Terrain.md#add_terrain_layer) |
| `terrain_height` | [Get/set/paint terrain height (unified)](Terrain.md#terrain_height) |
| `terrain_texture` | [Fill/paint terrain texture (unified)](Terrain.md#terrain_texture) |

### ProBuilder Operations
| Operation | Description |
|-----------|-------------|
| `create_probuilder_shape` | [Create procedural 3D mesh (stair, door, curved_stair, arch, pipe, cone, prism)](ProBuilder.md#create_probuilder_shape) |

### Visual Guide Modeling Operations
| Operation | Description |
|-----------|-------------|
| `create_fitted` | [Create geometry fitted to vertex positions](VisualGuideModeling.md#create_fitted) ※VGM: geometry |

## Batch Operations (Meta-Operation)

Execute multiple commands in a single request for better performance.
This is not a new Unity operation, but a wrapper to execute existing 59 operations in batch.

### Batch Format

```json
{
  "operation": "batch",
  "params": {
    "commands": [
      {"operation": "create_primitive", "params": {"type": "sphere", "name": "Ball", "color": "red"}},
      {"operation": "transform", "params": {"path": "Ball", "position": [0, 2, 0]}},
      {"operation": "create_light", "params": {"type": "point", "color": "yellow"}}
    ]
  }
}
```

### Batch Features

| Feature | Description |
|---------|-------------|
| Max commands | 20 per batch |
| Execution order | Sequential (array order) |
| Error handling | Stops on first error, remaining cancelled |
| Undo | All commands in one Undo group (single Ctrl+Z) |
| Nested batch | Not allowed |

### Batch Response

```json
{
  "success": true,
  "results": [
    {"index": 0, "success": true, "result": "Created sphere: Ball"},
    {"index": 1, "success": true, "result": "Set Ball position to (0,2,0)"},
    {"index": 2, "success": true, "result": "Created point light"}
  ],
  "summary": {
    "total": 3,
    "succeeded": 3,
    "failed": 0,
    "cancelled": 0
  }
}
```

### Batch Error Response

When a command fails, remaining commands are cancelled:

```json
{
  "success": false,
  "results": [
    {"index": 0, "success": true, "result": "Created sphere: Ball"},
    {"index": 1, "success": false, "error": "GameObject not found: MissingObj"},
    {"index": 2, "success": false, "error": "Cancelled: previous command failed"}
  ],
  "summary": {
    "total": 3,
    "succeeded": 1,
    "failed": 1,
    "cancelled": 1
  }
}
```

### When to Use Batch

- Creating multiple related objects
- Setting up a scene with multiple elements
- Any operation requiring 3+ sequential commands
- Performance-critical operations (reduces window activation overhead)

## Best Practices

### Script Generation: Local File Creation

**For C# scripts, create files locally using Claude Code's Write tool instead of WebSocket commands.**

This approach is recommended because:
- **Faster execution**: No WebSocket round-trip required
- **Easier debugging**: Scripts can be read/modified directly
- **No JSON escaping**: Avoid complex string escaping issues
- **Full IDE support**: Syntax highlighting and IntelliSense during creation

**Workflow:**
1. Create the .cs file locally using Write tool at `Assets/YourFolder/YourScript.cs`
2. Call `refresh_assets` to make Unity detect the new file:
   ```bash
   python send_message.py '{"operation":"refresh_assets","params":{}}'
   ```
3. Unity will automatically compile the script
4. Use `logs` with `filter: "errors"` to check for compilation errors if needed

**Example script structure:**
```csharp
using UnityEngine;

public class MyBehavior : MonoBehaviour
{
    void Update()
    {
        // Your code here
    }
}
```

### Always Verify Scene State

Before and after operations, use `get_scene_hierarchy` to confirm the current state:

```bash
# Check scene before operations
python send_message.py '{"operation":"get_scene_hierarchy","params":{"max_depth":2}}'

# Perform operations...

# Verify changes after operations
python send_message.py '{"operation":"get_scene_hierarchy","params":{}}'
```

**Why this matters:**
- Same-named objects may exist at different hierarchy levels
- Batch delete may miss objects (e.g., root `Cube0` vs `Cubes/Cube0`)
- Confirms all intended changes were applied

### Recommended Workflow

1. **Get scene state** - Understand current hierarchy before changes
2. **Plan operations** - Identify exact paths for objects to modify
3. **Execute commands** - Use batch for multiple related operations
4. **Verify results** - Check scene hierarchy to confirm changes
5. **Clean up** - Delete any unintended objects

## Examples

```bash
# Create object
python send_message.py '{"operation":"create_primitive","params":{"type":"sphere","name":"Ball","color":"red","position":[0,1,0]}}'

# Query scene
python send_message.py '{"operation":"get_scene_hierarchy","params":{"max_depth":3}}'

# Modify object
python send_message.py '{"operation":"transform","params":{"path":"Ball","position":[5,0,0],"rotation":[0,45,0]}}'

# Batch operations (max 20 commands)
python send_message.py '{"operation":"batch","params":{"commands":[
  {"operation":"create_primitive","params":{"type":"cube","name":"Floor","scale":[10,0.1,10]}},
  {"operation":"create_primitive","params":{"type":"sphere","name":"Ball","color":"red","position":[0,1,0]}}
]}}'
```

## Server Information

| Item | Value |
|------|-------|
| URL | ws://127.0.0.1:8766 |
| Protocol | WebSocket + JSON |
| Timeout | 10 seconds |
| Unity Window | Tools > ClaudeAgent > Unity Command Server |

## Troubleshooting

### Connection Refused
1. Open Unity Editor
2. Open: `Tools > ClaudeAgent > Unity Command Server`
3. Verify status is "Running" (green)

### Timeout (10s)
- Check Unity Console for errors
- Command may be taking too long
- Restart Command Server

### Command Failed
- Check operation name (case-sensitive)
- Verify parameter names
- See category-specific .md files for details
- Errors are returned as-is (no fallback)

### Unknown Parameter Warning
If you use an invalid or misspelled parameter name, the command will still execute but include a warning:

```
Created sphere: MySphere
[WARNING] Unknown parameters ignored: positon, colr
```

This helps identify typos (e.g., `positon` instead of `position`) without failing the command. The warning appears after the result message.

### Connection Lost After refresh_assets
The `refresh_assets` operation may cause a temporary WebSocket disconnection:

**Symptoms:**
- Commands immediately after `refresh_assets` fail with connection errors
- Server status shows "Reconnecting..."

**Cause:**
`AssetDatabase.Refresh()` can trigger a domain reload when new scripts are detected, which restarts the Unity Command Server.

**Solution:**
1. Wait a moment (1-2 seconds) after `refresh_assets` before sending the next command
2. If connection fails, retry the command once
3. The server automatically restarts after domain reload - no manual restart needed

**Note:** This behavior only occurs when `refresh_assets` detects new or modified scripts that require recompilation. Asset-only changes (textures, prefabs, etc.) do not trigger domain reload.
