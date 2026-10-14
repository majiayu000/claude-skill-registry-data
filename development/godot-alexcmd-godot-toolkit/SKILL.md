---
name: godot
description: Godot 4.7 development entry point — lists all available godot:* skills and when to use each. Auto-injected when a project.godot file is detected.
---

# Godot Development Context

You are working on a **Godot 4.7** project with the **AgentBridge** module compiled in.

## AgentBridge — Shell Script Interface

All AgentBridge communication goes through `godot-exec.sh`. Never use raw curl.

```bash
GDEXEC="bash ${CLAUDE_SKILL_DIR}/../runner/scripts/godot-exec.sh"
```

| Command | Purpose |
|---|---|
| `$GDEXEC --health` | Check editor connection |
| `$GDEXEC --execute 'CODE'` | Run GDScript in the live editor |
| `$GDEXEC --execute - <<'GD'\n...\nGD` | Run multiline GDScript |
| `$GDEXEC --log [N]` | Read editor output log (default 100 lines) |
| `$GDEXEC --save-all` | Save all open scenes and scripts |
| `$GDEXEC --play [res://scene.tscn]` | Start playing a scene |
| `$GDEXEC --stop` | Stop the playing scene |
| `$GDEXEC --open res://scene.tscn` | Open a scene in the editor |

> **Availability**: AgentBridge is available when the Godot editor is running with the AgentBridge module compiled in. Run `$GDEXEC --health` to check. If the editor is not running, see `godot:runner` pre-flight for how to launch it and connect in the same session.
>
> **Port**: assigned randomly at startup. Written to `<project>/.godot/agentbridge.port`. Auto-detected by `godot-exec.sh` — no manual port management needed.

## Domain Skills — When to Use Each

| Skill | Use when |
|---|---|
| `godot:coder` | Writing any GDScript — classes, autoloads, methods |
| `godot:architect` | Designing scene hierarchy, autoload structure, resource patterns |
| `godot:debugger` | Encountering errors, crashes, or unexpected behavior |
| `godot:runner` | Running, testing, or profiling scenes |
| `godot:scene` | Adding, removing, or inspecting nodes programmatically |
| `godot:shader` | Writing spatial, canvas_item, or particle shaders |
| `godot:signals` | Designing event systems or connecting signals |
| `godot:ui` | Building Control-based UI, HUDs, menus |
| `godot:docs` | Looking up Godot 4.x API docs via Context7 |

## Process Skills — When to Use Each

| Skill | Use when |
|---|---|
| `godot:brainstorming` | Before implementing any new feature |
| `godot:writing-plans` | After brainstorming, before writing code |
| `godot:executing-plans` | Executing a written implementation plan |
| `godot:subagent-driven-development` | Tasks have independent subtasks for parallel work |
| `godot:systematic-debugging` | Debugging — always use instead of guessing |
| `godot:verification-before-completion` | Before claiming any work is done |
| `godot:requesting-code-review` | After completing a plan step |
| `godot:receiving-code-review` | When processing code review feedback |
| `godot:dispatching-parallel-agents` | Launching parallel subagents for independent work |
| `godot:using-git-worktrees` | Starting feature work needing isolation |
| `godot:finishing-a-development-branch` | When implementation is complete |
| `godot:writing-skills` | Creating new godot:* skills |

## Role Skills — When to Use Each

| Skill | Use when |
|---|---|
| `godot:gameplay` | Implementing player, input, game mechanics, state machines, save/load |
| `godot:graphics` | Setting up lighting, WorldEnvironment, post-processing, GI, reflection probes |
| `godot:environment` | Building game worlds — terrain, navigation mesh, occlusion, GridMap |
| `godot:vfx` | Creating particle effects, trails, impacts, screen effects |
| `godot:animation` | Working with AnimationPlayer, AnimationTree, blend spaces, IK |
| `godot:audio` | Setting up sounds, music, spatial audio, audio buses |
| `godot:physics` | Collision layers, joints, raycasts, physics bodies, PhysicsServer3D |
| `godot:ai` | NPC pathfinding, NavigationAgent3D, NPC behavior state machines |
| `godot:networking` | Multiplayer, RPC, scene replication, lobby systems |

## Godot 4.7 Quick Reference

### Node Lifecycle Order

`_init → _enter_tree → _ready → _process/_physics_process → _exit_tree → _notification(NOTIFICATION_PREDELETE)`

- `_init` — called when the object is constructed; no scene tree access yet
- `_enter_tree` — node has just been added to the scene tree; children may not be ready
- `_ready` — node and all children are in the scene tree and initialized
- `_process(delta)` — called every rendered frame; use for visual/input logic
- `_physics_process(delta)` — called every physics tick (default 60 Hz); use for movement and collisions
- `_exit_tree` — node is about to leave the scene tree; clean up connections here
- `_notification(NOTIFICATION_PREDELETE)` — object is about to be freed; last chance before destruction

### Key Singletons

| Singleton | Purpose |
|---|---|
| `Engine` | Engine version info, frames per second, time scale, editor detection (`Engine.is_editor_hint()`) |
| `OS` | Platform detection, environment variables, system paths, process execution |
| `Input` | Polling actions/axes, setting mouse mode, vibration, action mapping queries |
| `ProjectSettings` | Read/write project settings at runtime via string paths |
| `ResourceLoader` | Load resources from `res://`, check existence, load in background threads |
| `DisplayServer` | Window management, screen info, cursor control, virtual keyboard |
| `RenderingServer` | Low-level rendering API; create and manipulate render primitives directly |
| `PhysicsServer3D` | Low-level 3D physics API; manage bodies, shapes, and spaces directly |
| `NavigationServer3D` | Navigation mesh baking, agent management, path queries |
| `AudioServer` | Audio bus layout, bus effects, volume, and playback control |

### Important Project Settings Paths

Use these string keys with `ProjectSettings.get_setting()`:

- `"application/config/name"` — the project name as set in Project Settings
- `"display/window/size/viewport_width"` — base viewport width in pixels
- `"physics/3d/default_gravity"` — default gravity magnitude (m/s²) for 3D physics
- `"application/run/main_scene"` — `res://` path to the scene launched on game start

## When Things Go Wrong

- **Editor not responding** — run `$GDEXEC --health` to check the AgentBridge connection; see `godot:runner` pre-flight for how to launch the editor and establish a fresh connection
- **Script errors** — run `$GDEXEC --log 100 | grep ERROR` to filter the editor output log for error lines
- **Scene won't load** — verify the `res://` path spelling is exact (case-sensitive); use `ResourceLoader.exists("res://path/to/scene.tscn")` to confirm the file is visible to Godot
- **Node not found** — run `$GDEXEC --execute 'list_nodes(EditorInterface.get_edited_scene_root())'` to dump the current scene tree and find the correct node path

## References

- https://docs.godotengine.org/en/stable/ — official Godot documentation
- https://gdquest.com — tutorials and learning resources
- https://docs.godotengine.org/en/stable/classes/ — complete API class reference
