---
name: debugger
description: Debug Godot issues using AgentBridge — use when encountering errors, unexpected behavior, or runtime crashes.
type: process
---

# Godot Debugger

> You are an expert Godot debugger who diagnoses engine errors, script faults, and runtime crashes using AgentBridge and GDScript introspection tools.

```bash
GDEXEC="bash ${CLAUDE_SKILL_DIR}/../runner/scripts/godot-exec.sh"
```

## Overview

This skill diagnoses Godot 4 issues using AgentBridge to execute GDScript inside the running editor. Always start with the log, narrow down with targeted snippets, and make one change at a time. Use the remote debugger, `breakpoint` keyword, `assert()`, and `print_stack()` to pinpoint the root cause before touching any code.

The remote debugger connects the editor to the running game via:
```
--remote-debug tcp://127.0.0.1:6007
```

## Diagnostic Workflow

1. **Get recent log** — always start here before doing anything else:
   ```bash
   $GDEXEC --log 200
   ```

2. **Inspect the scene tree root** — confirm the scene loaded and check child count:
   ```bash
   $GDEXEC --execute - <<'GD'
   var root = EditorInterface.get_edited_scene_root()
   if root:
       print("Root: ", root.name, " children: ", root.get_child_count())
   else:
       print("No scene open")
   GD
   ```

3. **Inspect a specific node path** — confirm a node exists and identify its type:
   ```bash
   $GDEXEC --execute - <<'GD'
   var root = EditorInterface.get_edited_scene_root()
   var node = root.get_node_or_null("Player/CollisionShape3D")
   print("Found: ", node != null)
   if node:
       print("Type: ", node.get_class())
   GD
   ```

4. **Check a method exists on a node** — verify the script interface before calling:
   ```bash
   $GDEXEC --execute - <<'GD'
   var root = EditorInterface.get_edited_scene_root()
   var player = root.get_node_or_null("Player")
   print("Has take_damage: ", player.has_method("take_damage"))
   GD
   ```

5. **Narrow down with `print_stack()`** — add to any GDScript function to see the call chain at runtime. Place inline where the fault occurs:
   ```gdscript
   func take_damage(amount: int) -> void:
       print_stack()
       health -= amount
   ```

6. **Use `assert()` for invariant checking** — fires only in debug builds, stripped in release:
   ```gdscript
   assert(amount > 0, "take_damage called with non-positive amount")
   ```

7. **Trigger the editor debugger at a specific line** — use the `breakpoint` keyword; execution pauses in the editor debugger when reached:
   ```gdscript
   func _ready() -> void:
       breakpoint  # editor pauses here during Play
       setup_player()
   ```

8. **Re-read the log after every fix** — confirm the error is gone, not just suppressed:
   ```bash
   $GDEXEC --log 50
   ```

## Diagnostic Snippets

**Snippet 1 — List all nodes in scene tree with their types:**
```bash
$GDEXEC --execute - <<'GD'
func list_nodes(node: Node, depth: int = 0) -> void:
    print(" ".repeat(depth * 2), node.name, " [", node.get_class(), "]")
    for child in node.get_children():
        list_nodes(child, depth + 1)

var root = EditorInterface.get_edited_scene_root()
if root:
    list_nodes(root)
GD
```

**Snippet 2 — Dump all properties of a node:**
```bash
$GDEXEC --execute - <<'GD'
var root = EditorInterface.get_edited_scene_root()
var node = root.get_node_or_null("Player")
if node:
    for prop in node.get_property_list():
        if prop["usage"] & PROPERTY_USAGE_EDITOR:
            print(prop["name"], " = ", node.get(prop["name"]))
GD
```

**Snippet 3 — Check object count for memory leak detection:**
```bash
$GDEXEC --execute - <<'GD'
var obj_count = Performance.get_monitor(Performance.OBJECT_COUNT)
var node_count = Performance.get_monitor(Performance.OBJECT_NODE_COUNT)
var orphan_count = Performance.get_monitor(Performance.OBJECT_ORPHAN_NODE_COUNT)
print("Objects: ", obj_count)
print("Nodes: ", node_count)
print("Orphan nodes: ", orphan_count)
GD
```

**Snippet 4 — Verify a resource path resolves:**
```bash
$GDEXEC --execute - <<'GD'
var path = "res://assets/player.tres"
print("Exists: ", ResourceLoader.exists(path))
print("Type: ", ResourceLoader.get_resource_type(path))
GD
```

**Snippet 5 — Inspect signal connections on a node:**
```bash
$GDEXEC --execute - <<'GD'
var root = EditorInterface.get_edited_scene_root()
var node = root.get_node_or_null("Player")
if node:
    for sig in node.get_signal_list():
        var connections = node.get_signal_connection_list(sig["name"])
        if connections.size() > 0:
            print("Signal: ", sig["name"], " -> ", connections)
GD
```

**Snippet 6 — Dump memory snapshot to file:**
```bash
$GDEXEC --execute - <<'GD'
OS.dump_memory_to_file("user://memory.txt")
print("Memory snapshot written to: ", OS.get_user_data_dir(), "/memory.txt")
GD
```

**Snippet 7 — Send a custom profiler event via EngineDebugger:**
```gdscript
# In your game script — visible in the editor's Debugger > Profiler tab
EngineDebugger.send_message("my_profiler:event", ["damage_applied", 42])
```

**Snippet 8 — Guard editor-only code with Engine.is_editor_hint():**
```gdscript
func _ready() -> void:
    if Engine.is_editor_hint():
        return  # skip runtime setup when previewing in editor
    setup_gameplay()
```

## Error Categories

| Error Type | How to Identify | How to Fix |
|---|---|---|
| GDScript Error | Log shows file path and line number, e.g. `res://scripts/player.gd:42` | Open the file at the reported line; check variable types, method names, and signal signatures |
| Engine Error | Log shows C++ origin like `servers/physics_3d/...` or `modules/...`; no GDScript file reference | Check the Godot engine source or docs for the internal error code; often caused by invalid node state or uninitialized resources |
| Resource Error | Log shows `Failed to load resource` or `null` return from `load()` | Verify the `res://` path is correct and the file exists; check `.import` files are not stale; re-import via Project > Reimport |
| Null Reference | `Invalid get index ... on base Nil` in log | Use `get_node_or_null()` and guard with `if node:` before access; check node path spelling and scene tree order |
| Signal Error | `Error: Can't connect to non-existing signal` | Verify signal name with `get_signal_list()` snippet; confirm emitter node is the correct type |
| Type Mismatch | `Invalid operands to operator` or `Cannot assign ... to variable of type` | Add explicit type annotations; use `is` keyword to check type before casting |

## Common Pitfalls

- **Log flooding from `_physics_process`** — `print()` inside `_physics_process` or `_process` fires 60 times per second. A single print statement generates thousands of log lines, buries real errors, and skews all performance measurements. Remove all `print()` calls from process callbacks before profiling.

- **Fixing symptoms instead of reading the log** — changing code before reading the full error message wastes iterations. The log line number and error text almost always point directly to the cause. Always run `$GDEXEC --log 200` first.

- **Shotgun fixing** — making multiple changes at once makes it impossible to know which change resolved or introduced an issue. Apply exactly one change per iteration, then verify with the log.

- **`breakpoint` left in production code** — the `breakpoint` keyword is not stripped in release builds by default. Search for all `breakpoint` occurrences before shipping and remove them or guard with `if OS.is_debug_build():`.

- **`assert()` masking bugs in release** — `assert()` is stripped in release builds. Logic that only runs inside an assert (e.g., function calls with side effects) will silently disappear in production. Only use `assert()` for invariant checks, never for control flow.

- **Orphan nodes causing memory leaks** — nodes created with `Node.new()` that are never added to the tree or freed accumulate silently. Monitor `Performance.OBJECT_ORPHAN_NODE_COUNT` periodically and call `node.queue_free()` or `node.free()` when done.

## Performance Diagnostics

Use `Performance.get_monitor()` to read live engine metrics without opening the editor GUI.

**Frame timing:**
```bash
$GDEXEC --execute - <<'GD'
print("FPS: ", Performance.get_monitor(Performance.TIME_FPS))
print("Frame time (ms): ", Performance.get_monitor(Performance.TIME_PROCESS) * 1000.0)
print("Physics time (ms): ", Performance.get_monitor(Performance.TIME_PHYSICS_PROCESS) * 1000.0)
GD
```

**Memory usage:**
```bash
$GDEXEC --execute - <<'GD'
print("Static memory: ", Performance.get_monitor(Performance.MEMORY_STATIC) / 1048576.0, " MB")
print("Static memory peak: ", Performance.get_monitor(Performance.MEMORY_STATIC_MAX) / 1048576.0, " MB")
print("Message buffer: ", Performance.get_monitor(Performance.MEMORY_MESSAGE_BUFFER_MAX))
GD
```

**Object counts (leak detection):**
```bash
$GDEXEC --execute - <<'GD'
print("Objects: ", Performance.get_monitor(Performance.OBJECT_COUNT))
print("Resources: ", Performance.get_monitor(Performance.OBJECT_RESOURCE_COUNT))
print("Nodes: ", Performance.get_monitor(Performance.OBJECT_NODE_COUNT))
print("Orphan nodes: ", Performance.get_monitor(Performance.OBJECT_ORPHAN_NODE_COUNT))
GD
```

**Render stats:**
```bash
$GDEXEC --execute - <<'GD'
print("Draw calls: ", Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME))
print("Objects drawn: ", Performance.get_monitor(Performance.RENDER_TOTAL_OBJECTS_IN_FRAME))
print("Video memory: ", Performance.get_monitor(Performance.RENDER_VIDEO_MEM_USED) / 1048576.0, " MB")
GD
```

## Anti-Patterns

| Wrong | Right |
|---|---|
| Change code until the error disappears | Read the full log first, identify the exact line and error type |
| `print()` inside `_process` to trace values | Use `breakpoint` or the editor Debugger watch panel |
| Fix three things at once after a crash | Fix one thing, verify with log, repeat |
| Use `assert(some_func())` for side effects | Call the function separately; use assert only for pure condition checks |
| Leave `breakpoint` in merged code | Search and remove all `breakpoint` keywords before committing |
| Ignore orphan node count growing over time | Monitor `OBJECT_ORPHAN_NODE_COUNT` and audit `Node.new()` call sites |
| Call editor-only APIs in `_ready()` unconditionally | Guard with `if Engine.is_editor_hint(): return` |

## References

- GDScript error reference: https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html
- Debugger panel: https://docs.godotengine.org/en/stable/tutorials/editor/debugger/overview.html
- Remote debugger: https://docs.godotengine.org/en/stable/tutorials/editor/debugger/overview.html#remote-debugger
- `assert()` docs: https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html#assert-keyword
- `breakpoint` docs: https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html#breakpoint
- `print_stack()` docs: https://docs.godotengine.org/en/stable/classes/class_@gdscript.html#class-gdscript-method-print-stack
- Performance monitors: https://docs.godotengine.org/en/stable/classes/class_performance.html
- `EngineDebugger` API: https://docs.godotengine.org/en/stable/classes/class_enginedebugger.html
- `OS.dump_memory_to_file()`: https://docs.godotengine.org/en/stable/classes/class_os.html#class-os-method-dump-memory-to-file
- Profiling with Godot: https://docs.godotengine.org/en/stable/tutorials/performance/using_the_profiler.html
