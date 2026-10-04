---
name: godot-init
description: |
  Bootstrap a Godot 4 project from scratch or verify an existing project structure.
  Use when: starting a new game, initializing folder structure, configuring project.godot,
  or verifying a project is set up correctly.
---

# Project Initialization

## For New Projects

### 1. Create Directory Structure
```
scripts/
  autoload/
scenes/
assets/
  sprites/
  audio/
```

### 2. Create project.godot
```ini
; Engine configuration file (Godot 4.3+)

config_version=5

[application]
config/name="Game Name"
run/main_scene="res://scenes/main.tscn"
config/features=PackedStringArray("4.3")

[display]
window/size/viewport_width=1024
window/size/viewport_height=600
window/stretch/mode="canvas_items"

[input]
move_left={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":65,"key_label":0,"unicode":97)]
}
move_right={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":68,"key_label":0,"unicode":100)]
}
move_up={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":87,"key_label":0,"unicode":119)]
}
move_down={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":83,"key_label":0,"unicode":115)]
}
shoot={
"deadzone": 0.5,
"events": [Object(InputEventMouseButton,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"button_mask":1,"position":Vector2(0,0),"global_position":Vector2(0,0),"factor":1.0,"button_index":1,"canceled":false,"pressed":true,"double_click":false)]
}
jump={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":32,"key_label":0,"unicode":32)]
}
pause={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":4194305,"key_label":0,"unicode":0)]
}

[rendering]
textures/canvas_textures/default_texture_filter=0
```

### 3. Create Minimal Main Scene
Write `scenes/main.tscn`:
```
[gd_scene load_steps=2 format=3]
[ext_resource type="Script" path="res://scripts/main.gd" id="1"]
[node name="Main" type="Node2D"]
script = ExtResource("1")
```

Write `scripts/main.gd`:
```gdscript
extends Node2D

func _ready():
    print("Game started!")
```

### 4. Verify with MCP
After creating files:
1. `godot_reload_filesystem` — tell editor to scan
2. `godot_run_scene` — verify it launches
3. `godot_get_errors` — check for issues

## For Existing Projects

### Scan and Report
1. Call `godot_get_project_state`
2. Report: project name, main scene, file counts
3. Identify gaps (missing scripts/, scenes/ dirs, no main scene)
4. Fix issues

### Add Missing Structure
If directories don't exist, create them.
If project.godot is missing key settings, add them.
If no main scene: create one and set it.

## Pixel Art vs Smooth

- **Pixel art**: Set `rendering/textures/canvas_textures/default_texture_filter=0`
- **Smooth**: Set `rendering/textures/canvas_textures/default_texture_filter=1`

## Input Actions

Always create these standard actions (already in project.godot template above):
- `move_left` (A), `move_right` (D), `move_up` (W), `move_down` (S)
- `shoot` (Left Mouse Button)
- `jump` (Space)
- `pause` (Escape)

For genre-specific actions, add them to the `[input]` section following the same format.
