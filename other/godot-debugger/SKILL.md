---
name: godot-debugger
description: |
  Diagnose runtime bugs, visual glitches, and unexpected behavior in Godot games
  by inspecting the live game via MCP tools. Adaptive — routes to different
  diagnostic paths based on symptoms. Triggers on: debug, why is, not working,
  broken, crash, glitch, wrong, investigate, diagnose
---

# Godot Debugger

Diagnose and fix Godot game issues using godot-mcp-pro runtime inspection tools.

## Prerequisites
- Godot editor open with project loaded
- godot-mcp-pro server connected
- For runtime debugging: scene must be playable

## Step 1: Classify the Symptom

| Symptom | Branch | Key Tools |
|---------|--------|-----------|
| Error in output, crash, script exception | **A: Crash/Error** | get_editor_errors, read_script, validate_script |
| Something looks wrong visually | **B: Visual Glitch** | get_game_screenshot, get_game_node_properties, capture_frames |
| Game logic doesn't work as expected | **C: Logic Bug** | execute_game_script, monitor_properties, analyze_signal_flow |
| Low FPS, stuttering, lag | **D: Performance** | get_performance_monitors, analyze_scene_complexity |
| Nothing happens at all | **E: Silent Failure** | get_collision_info, find_signal_connections, get_scene_tree |

## Branch A: Crash / Error

1. `mcp__godot-mcp-pro__get_editor_errors` — read all error messages
2. Parse the error:
   - **Script error with line number:** `mcp__godot-mcp-pro__read_script` the file, identify the line
   - **Null reference / Invalid get index:** `mcp__godot-mcp-pro__get_scene_tree` — check if node exists at expected path. Common: node renamed, not yet in tree, accessed before `_ready()`
   - **Type error:** Check Godot 4.6 strict typing rules (see common-bugs.md). `mcp__godot-mcp-pro__validate_script` to verify syntax
   - **Resource not found:** `mcp__godot-mcp-pro__search_files` to find actual resource path
3. Suggest fix with exact code change
4. After fix: `mcp__godot-mcp-pro__validate_script` to confirm compilation

## Branch B: Visual Glitch

1. `mcp__godot-mcp-pro__play_scene` if not running, then `mcp__godot-mcp-pro__get_game_screenshot`
2. Analyze the screenshot for clues
3. `mcp__godot-mcp-pro__get_game_scene_tree` — check hierarchy, visibility, ordering
4. `mcp__godot-mcp-pro__get_game_node_properties` on suspect nodes:
   - `visible` property
   - `modulate` / `self_modulate`
   - `transform` / `global_transform`
   - `z_index` (2D ordering)
   - `material` assignments
5. If shader issue: `mcp__godot-mcp-pro__read_shader` + `mcp__godot-mcp-pro__get_shader_params`
6. If particle issue: `mcp__godot-mcp-pro__get_particle_info` — check AABB, emission settings
7. If intermittent: `mcp__godot-mcp-pro__capture_frames` over multiple frames
8. Identify root cause and suggest fix

## Branch C: Logic Bug

1. `mcp__godot-mcp-pro__play_scene` then `mcp__godot-mcp-pro__execute_game_script`:
   ```gdscript
   var player = get_tree().get_first_node_in_group("player")
   return {"health": player.health, "state": player.current_state, "pos": player.global_position}
   ```
2. `mcp__godot-mcp-pro__monitor_properties` — track suspect variables over N frames
3. `mcp__godot-mcp-pro__analyze_signal_flow` — map signal connections
4. `mcp__godot-mcp-pro__find_signal_connections` — verify specific wiring
5. `mcp__godot-mcp-pro__assert_node_state` — test hypotheses:
   ```
   property: "health", operator: ">", value: 0
   ```
6. Narrow down: is the data wrong, the signal not firing, or the condition incorrect?
7. `mcp__godot-mcp-pro__read_script` to confirm the bug in code
8. Suggest fix

## Branch D: Performance

1. `mcp__godot-mcp-pro__get_performance_monitors` — FPS, physics time, draw calls, memory, node count
2. Identify bottleneck:
   - **Low FPS + high draw calls:** Too many visible objects
   - **Low FPS + high physics time:** Complex collision shapes or too many physics bodies
   - **Low FPS + high memory:** Resource leaks, oversized textures
   - **Stuttering:** GC pauses, large instantiations, file I/O on main thread
3. `mcp__godot-mcp-pro__analyze_scene_complexity` — node counts, nesting, type distribution
4. `mcp__godot-mcp-pro__get_game_scene_tree` with type filters — find heavy subtrees
5. Recommend specific optimizations:
   - Draw calls: MultiMeshInstance3D, merge static meshes, LOD
   - Physics: simplify shapes (box/capsule over trimesh), reduce body count
   - Memory: compress textures, mipmaps, unload unused resources
   - Stuttering: preload resources, object pools, defer heavy work

## Branch E: Silent Failure

1. `mcp__godot-mcp-pro__get_editor_errors` — suppressed warnings
2. `mcp__godot-mcp-pro__get_scene_tree` — verify node IS in the scene tree
3. `mcp__godot-mcp-pro__find_signal_connections` — check expected signals wired
4. `mcp__godot-mcp-pro__get_collision_info` — check layer/mask (very common cause)
5. `mcp__godot-mcp-pro__execute_game_script` — manually call the expected function:
   ```gdscript
   var node = get_node("/root/Main/Enemy")
   node.take_damage(10)
   return {"health_after": node.health}
   ```
6. Trace the chain: Input -> Signal -> Method -> Effect. Find the broken link.

## Iteration Strategy

- Don't give up after one pass. If first hypothesis is wrong, try next branch.
- `mcp__godot-mcp-pro__get_output_log` for context beyond errors.
- `mcp__godot-mcp-pro__clear_output` before reproducing for clean logs.
- Screenshot before AND after fixes to confirm resolution.

## Common Gotchas

- **Collision layers:** `1 << (N-1)` bitmask, NOT raw numbers. #1 cause of "bullets pass through."
- **Godot 4.6 typing:** `:=` with Variant-returning functions causes parse errors. Use `: Type =`.
- **RID leaks:** Manually created resources not attached to nodes won't be freed.

## Project Conventions
Check the project's .claude/skills/ and CLAUDE.md for project-specific debugging context such as collision layer conventions, entity system patterns, and known project gotchas.
