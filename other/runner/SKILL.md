---
name: runner
description: Run, test, and profile Godot scenes using AgentBridge — use when you need to execute, observe, or benchmark a scene.
type: process
---

# Godot Runner

> You are a Godot execution expert: you run scenes, profile performance, execute GDScript in the live editor, and drive GUT test suites via AgentBridge and headless CI.

## Overview

All AgentBridge communication goes through `godot-exec.sh`. Never use raw curl.

```bash
GDEXEC="bash ${CLAUDE_SKILL_DIR}/scripts/godot-exec.sh"
```

Use this skill to:
- Play and stop scenes while capturing log output
- Execute GDScript snippets in the live editor context
- Profile frame timing and Performance monitor metrics
- Run GUT unit test suites interactively or in headless CI
- Diagnose errors, warnings, and node-tree state

---

## Pre-flight: ensure editor is running

Run this exact sequence every time before using AgentBridge:

```bash
GDEXEC="bash ${CLAUDE_SKILL_DIR}/scripts/godot-exec.sh"
PROJECT="<project-path>"   # look up from memory — machine-specific
GODOT_EXE="<godot-exe>"    # look up from memory — machine-specific
PORT_FILE="${PROJECT}/.godot/agentbridge.port"

# Step 1 — if already running and responsive, reuse it
if $GDEXEC --health 2>/dev/null; then
    echo "[AgentBridge] Editor running — reusing."
else
    # Step 2 — check for stale port file (editor crashed)
    if [[ -f "$PORT_FILE" ]]; then
        echo "[AgentBridge] Stale port file found — editor crashed. Relaunching..."
        rm -f "$PORT_FILE"
    else
        echo "[AgentBridge] Editor not running. Launching..."
    fi

    # Step 3 — launch editor
    powershell.exe -Command "Start-Process '${GODOT_EXE}' -ArgumentList '--path','${PROJECT}','--editor'"

    # Step 4 — wait for AgentBridge to write the port file and respond
    for i in {1..15}; do
        sleep 2
        $GDEXEC --health 2>/dev/null && { echo "[AgentBridge] Connected."; break; }
        echo "[AgentBridge] Waiting... ($i/15)"
    done
    $GDEXEC --health   # final check — exits 1 if still not up
fi
```

Port file location: `<project>/.godot/agentbridge.port` — written by the editor on startup, deleted on close. If the file exists but health fails, the editor crashed and must be relaunched.

**No need to restart Claude Code** — once health passes, proceed in this same session.

---

## Run a scene and capture output

```bash
GDEXEC="bash ${CLAUDE_SKILL_DIR}/scripts/godot-exec.sh"

$GDEXEC --save-all                        # ensure changes are saved
$GDEXEC --play res://path/to/scene.tscn   # start playing
sleep 3                                   # let scene initialize
$GDEXEC --stop                            # stop
$GDEXEC --log 200                         # inspect output
```

## Execute GDScript and check result

```bash
$GDEXEC --execute 'print(ProjectSettings.get_setting("application/config/name"))'

# Multiline code — use heredoc:
$GDEXEC --execute - <<'GD'
print(OS.get_name())
print(Engine.get_version_info())
GD
```

## Common diagnostic snippets

```bash
# Check scene tree root
$GDEXEC --execute - <<'GD'
var root = EditorInterface.get_edited_scene_root()
print(root.name, " — ", root.get_child_count(), " children")
GD

# List all nodes
$GDEXEC --execute - <<'GD'
func list_nodes(node: Node, indent: int = 0) -> void:
    print(" ".repeat(indent), node.name, " (", node.get_class(), ")")
    for child in node.get_children():
        list_nodes(child, indent + 2)
list_nodes(EditorInterface.get_edited_scene_root())
GD

# Check autoloads
$GDEXEC --execute - <<'GD'
for autoload in ProjectSettings.get_setting("autoload").keys():
    print("autoload: ", autoload)
GD

# Grep log for errors and warnings
$GDEXEC --log 500 | grep -i "error\|warning\|assert"

# Print all project settings matching a prefix
$GDEXEC --execute - <<'GD'
for key in ProjectSettings.get_property_list():
    if key["name"].begins_with("physics/"):
        print(key["name"], " = ", ProjectSettings.get_setting(key["name"]))
GD
```

## Profile timing

```bash
# Micro-benchmark a code path
$GDEXEC --execute - <<'GD'
var start = Time.get_ticks_usec()
# ... code to profile ...
print("Elapsed: ", Time.get_ticks_usec() - start, " us")
GD

# Performance monitor snapshot — FPS, draw calls, node count, object count
$GDEXEC --execute - <<'GD'
print("FPS:          ", Performance.get_monitor(Performance.TIME_FPS))
print("Draw calls:   ", Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME))
print("Nodes active: ", Performance.get_monitor(Performance.OBJECT_NODE_COUNT))
print("Objects:      ", Performance.get_monitor(Performance.OBJECT_COUNT))
GD

# Scene benchmark — play for N frames and report average process time
$GDEXEC --save-all
$GDEXEC --play res://path/to/scene.tscn
sleep 5   # let scene run for ~5 seconds
$GDEXEC --execute - <<'GD'
# Sample average TIME_PROCESS over 60 frames (run while scene is playing)
var samples: Array = []
for i in range(60):
    samples.append(Performance.get_monitor(Performance.TIME_PROCESS))
var avg = samples.reduce(func(a, b): return a + b) / samples.size()
print("Avg process time (ms): ", avg * 1000.0)
GD
$GDEXEC --stop
```

## GUT Unit Testing

[GUT (Godot Unit Test)](https://github.com/bitwes/Gut) is the standard unit testing addon for Godot.

**Installation:**
1. Copy the `addons/gut` folder into your project's `addons/` directory.
2. Enable it in **Project > Project Settings > Plugins**.
3. Add `GutMain` as an autoload (singleton) pointing to `res://addons/gut/gut_main.gd`.

**Test file conventions:**
- Files must be named `test_*.gd` (e.g. `test_player.gd`).
- Place them under `res://test/` or any directory registered in GUT's settings.
- Test methods must be prefixed with `test_`.

```gdscript
# res://test/test_player.gd
extends GutTest

func test_initial_health() -> void:
    var player = Player.new()
    assert_eq(player.health, 100, "Player should start at full health")
    player.free()

func test_take_damage() -> void:
    var player = Player.new()
    player.take_damage(25)
    assert_eq(player.health, 75)
    player.free()
```

**Run tests via AgentBridge:**

```bash
$GDEXEC --execute 'GutMain.run_tests()'
$GDEXEC --log 300 | grep -i "pass\|fail\|error"
```

**Signal-based sync in tests — use `await`, not `sleep`:**

```gdscript
# Good — awaits the actual signal
await get_tree().create_timer(0.1).timeout

# Good — awaits a game signal directly
await player.died

# Avoid — sleep duration is machine-dependent and flaky in CI
# OS.delay_msec(100)
```

---

## Headless / CI Execution

Run Godot without a display for automated pipelines. Requires a `test_runner.gd` script that calls `get_tree().quit(exit_code)` so CI can read the result.

```bash
# Run GUT tests headlessly (Linux/macOS CI)
"${GODOT_EXE}" --headless --script res://test_runner.gd -- --gut

# Minimized window for background test runs on desktop (keeps a display)
$GDEXEC --execute - <<'GD'
DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_MINIMIZED)
GD

# Profiled production build with debug info intact
"${GODOT_EXE}" --export-debug "Linux/X11" /tmp/game_debug.x86_64
```

**Minimal `test_runner.gd` for CI:**

```gdscript
extends SceneTree

func _init() -> void:
    var gut = load("res://addons/gut/gut.gd").new()
    root.add_child(gut)
    gut.add_directory("res://test")
    gut.test_scripts()
    await gut.end_run
    quit(1 if gut.get_fail_count() > 0 else 0)
```

Exit code `0` = all tests pass, non-zero = failures — compatible with GitHub Actions, GitLab CI, and Jenkins.

---

## Common Pitfalls

- **Stale port file after crash.** If `agentbridge.port` exists but `--health` fails, the editor crashed. Delete the port file and relaunch before any other command — skipping this causes every subsequent `$GDEXEC` call to time out silently.
- **`await` in `--execute` snippets is not supported.** AgentBridge executes GDScript synchronously via `EditorScript`; any `await` or coroutine will hang or be ignored. Move async logic into a test scene or GUT test instead.
- **`sleep` in test assertions is flaky.** Signal timing varies by machine load. Always `await signal_name` or `await get_tree().create_timer(n).timeout` rather than `OS.delay_msec()`.
- **`--headless` requires a project with no mandatory display resources.** If your main scene uses `DisplayServer` features unconditionally, headless runs will print errors or crash. Guard display calls with `if DisplayServer.get_name() != "headless":`.
- **`--execute` runs in the editor context, not a game context.** Singletons like `GameManager` are not available unless explicitly added as editor autoloads. Use `EditorInterface` APIs for editor-state queries.
- **Performance monitor values are zero before the first frame.** Always play a scene for at least one frame (use `sleep 1` minimum) before sampling `Performance.get_monitor()` — values are updated once per process frame.

---

## References

- Godot command-line reference: https://docs.godotengine.org/en/stable/tutorials/editor/command_line_tutorial.html
- `Performance` singleton monitor list: https://docs.godotengine.org/en/stable/classes/class_performance.html
- `SceneTree.quit()` and exit codes: https://docs.godotengine.org/en/stable/classes/class_scenetree.html#class-scenetree-method-quit
- `DisplayServer.window_set_mode()`: https://docs.godotengine.org/en/stable/classes/class_displayserver.html#class-displayserver-method-window-set-mode
- Export / headless CI guide: https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_dedicated_servers.html
- GUT (Godot Unit Test) addon: https://github.com/bitwes/Gut
- GUT documentation: https://gut.readthedocs.io/en/latest/
