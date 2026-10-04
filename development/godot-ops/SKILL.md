---
name: godot-ops
description: |
  MCP tool operations: run game, read errors, reload filesystem, iterate fixes.
  Use when testing, debugging, or running the build-test-fix loop.
  This is the "DevOps" skill for AI game generation.
  CRITICAL: Always use MCP tools, never raw curl. Always report progress.
---

# Operations — Build, Run, Fix Loop

## RULE: Always Use MCP Tools

Use `godot_reload_filesystem`, `godot_run_scene`, `godot_get_errors`, etc.
**NEVER use raw `curl http://localhost:6100/...`** — that bypasses MCP and means the plugin isn't loaded.

If MCP tools aren't available, stop and tell the user:
> "MCP tools not available. Start Claude Code with: `claude --plugin-dir /path/to/godot-ai-builder`"

## ⛔ RULE: MANDATORY Dock Logging (NEVER SKIP)

**The Godot dock panel is the user's PRIMARY progress monitor.** You MUST call `godot_log` before and after EVERY action — no exceptions. If you don't log, the user sees nothing happening and thinks the build is broken.

After EVERY action, report in TWO places:
1. **Terminal**: Print text for the user
2. **Godot dock**: Call `godot_log` so the Godot editor panel shows activity

```
godot_log("Reloading Godot filesystem...")
godot_log("Running game... checking for errors...")
godot_log("Found 2 errors. Fixing scripts/player.gd line 34...")
godot_log("✓ Error fixed. Retesting...")
godot_log("Game running. 0 errors. Phase 1 complete.")
```

**Rules:**
- Call `godot_log` BEFORE and AFTER every file write, every test, every error fix
- Call `godot_log` between every 2-3 other tool calls
- Call `godot_update_phase` at every phase start (in_progress) and end (completed)
- Aim for 3-5 `godot_log` calls per file write minimum
- MORE IS ALWAYS BETTER — the user wants constant activity in the dock

## ⛔ EXECUTION WATCHDOG (ANTI-STALL)

1. Keep terminal/dock updates short; no long `Thinking...` narratives.
2. Do not perform more than 3 non-mutating MCP calls in a row without a concrete progress step.
3. Concrete progress means: file edits, scene mutation, asset generation/application, scene run/stop, phase update, or quality scoring.
4. If blocked, output exactly `STALLED: <exact blocker>` and stop instead of looping.

## The Core Loop

After writing ANY game files, ALWAYS execute this loop immediately:

```
1. godot_reload_filesystem    → Editor sees new files
2. godot_run_scene            → Launch the game
3. (wait a moment)
4. godot_get_errors           → Check for problems
5. If errors: fix → go to 1
6. If clean: done!
```

## MCP Tool Reference

### godot_get_project_state
Call FIRST before any work. Returns:
- `editor_connected` (bool) — is Godot running with plugin?
- `project_name`, `main_scene`
- `files.scripts[]`, `files.scenes[]`, `files.assets[]`

### godot_reload_filesystem
Call after writing ANY file. The editor won't see changes until you do this.

### godot_run_scene
Run the game. Optional `scene_path` argument for a specific scene.
```json
{"scene_path": "res://scenes/main.tscn"}
```
Or omit for main scene:
```json
{}
```

### godot_stop_scene
Stop a running game. Call before running again.

### godot_get_errors
Returns:
```json
{
  "errors": [{"message": "...", "file": "res://...", "line": 42}],
  "warnings": [{"message": "...", "file": "res://...", "line": 10}]
}
```

### godot_parse_scene
Parse a .tscn file to understand its structure:
```json
{"scene_path": "res://scenes/main.tscn"}
```

### godot_generate_asset
Generate placeholder sprites:
```json
{"name": "player", "type": "character", "width": 32, "height": 32, "color": "#3399ff"}
```

### godot_scan_project_files
List all project files (works without editor running).

### godot_read_project_setting
Read from project.godot:
```json
{"key": "application/run/main_scene"}
```

### godot_list_addons
List curated add-ons from the internal catalog:
```json
{}
```
Optional filter:
```json
{"category": "polish_camera"}
```

### godot_install_addon
Install a catalog add-on (PoC baseline: Phantom Camera):
```json
{"addon_id": "phantom_camera"}
```

### godot_verify_addon
Verify required add-on files/signals:
```json
{"addon_id": "phantom_camera"}
```

### godot_apply_integration_pack
Apply curated pack with strict fail-loud behavior:
```json
{"pack_id": "pack_polish", "strict": true}
```
If this returns `rejected: true`, treat it as a hard blocker and fix integration before phase completion.

### godot_score_poc_quality
Score a PoC run and enforce iteration policy:
```json
{
  "benchmark_id": "poc_prompt_01",
  "iteration_count": 2,
  "max_iterations": 3,
  "hard_gates": {"zero_script_errors": true, "no_critical_warnings": true, "play_loop_complete": true, "controls_clear": true, "no_soft_lock": true, "quality_gates_passed": true},
  "anti_tutorial_visual_checks": {"named_art_direction": true, "palette_discipline": true, "silhouette_readability": true, "layering_depth": true, "feedback_clarity": true, "ui_theme_consistency": true, "no_raw_placeholder_feel": true},
  "scores": {"core_loop_fun": 4, "controls_game_feel": 4, "progression_variety": 4, "encounter_depth": 3, "visual_polish_cohesion": 4, "ux_onboarding_feedback": 4},
  "signature_moments": ["moment_1", "moment_2"]
}
```
Use verdict output:
- `go`: quality target met
- `needs_iteration`: fix `next_actions` and rerun
- `no_go`: max iterations reached, escalate to user

### godot_log (⚠️ MANDATORY — call constantly)
Send a message to the Godot dock panel. This is the user's ONLY way to see your progress in the Godot editor. You MUST call this tool constantly — before and after every file write, every test, every error fix, every decision, every phase transition. Aim for 3-5 calls per file write minimum.
```json
{"message": "Writing scripts/player.gd — WASD movement, mouse aim, shooting..."}
{"message": "✓ scripts/player.gd written — 85 lines"}
{"message": "ERROR in main.gd:15 — GameManager not found"}
{"message": "FIX: Registering GameManager autoload..."}
{"message": "✓ Error fixed. 0 errors remaining."}
```
Sub-agents should prefix with their name: `"[Agent: enemies] Writing enemy.gd..."`

## Error Resolution Patterns

### Using Detailed Errors (PREFERRED)

`godot_get_errors()` now returns **detailed error messages** with file paths, line numbers, and
actual error text via headless Godot validation. Always use these details to fix errors precisely.

**Error Fix Protocol:**
```
1. errors = godot_get_errors()      // Returns detailed messages with file + line
2. For each error:
   a. Read ONLY the specific lines around error.line (not the whole file)
   b. The error.message tells you EXACTLY what's wrong
   c. Fix the specific issue on that line
   d. Do NOT rewrite the whole file unless the error is architectural
3. godot_reload_filesystem()
4. errors = godot_get_errors()      // Verify fix
5. Repeat until zero errors
```

**Key principle**: Fix errors surgically. Read 5-10 lines around the error, not the whole file.
Rewriting a whole file to fix one typo is wasteful and introduces new bugs.

### Common GDScript Errors and Fixes

| Error Message | Cause | Fix |
|---|---|---|
| `Identifier "X" not found in base` | Missing autoload, wrong class name, or typo | Check autoload registration in project.godot, verify class_name spelling |
| `Invalid operands "X" and "Y"` | Type mismatch (int vs float, String vs int) | Cast types explicitly: `float(x)`, `str(x)`, `int(x)` |
| `Parser Error: Expected "X"` | Syntax error — missing colon, bracket, paren | Check line for missing `:` after if/for/func, unmatched brackets |
| `Cannot load source code from "X"` | File path wrong or file doesn't exist | Verify the .gd file exists at that path, check for typos in path |
| `Cyclic reference in "X"` | Two scripts import each other | Remove circular dependency — use signals or a shared autoload instead |
| `Could not find type "X" in base "Y"` | Using a class that hasn't been loaded or doesn't exist | Add `class_name` to the target script, or use `load()` to get the class |
| `Function "X" not found in base "Y"` | Calling a method that doesn't exist on that type | Call `godot_get_class_info("Y")` to check correct method names |
| `Too few arguments for "X"` | Missing required parameters in method call | Call `godot_get_class_info` to check correct method signature |
| `Signal "X" not found` | Connecting to a signal that doesn't exist | Check signal name spelling, verify the signal is declared in the class |
| `Cannot use "X" as a function` | Using a property as a function or vice versa | Check if `X` is a property (access without `()`) or method (call with `()`) |
| `Unexpected "Identifier" in class body` | Code outside of a function at the class level | Move the code inside a function (`_ready()`, `_process()`, etc.) |
| `The default value is incompatible with type` | Default parameter type doesn't match declaration | Fix the type annotation or the default value |

### Cascading Error Pattern

When an **autoload** or **base class** has an error, ALL scripts that reference it will also
show errors. This is the most common source of "10 scripts all broken" situations.

**How to identify**: Multiple scripts show the same error about a missing identifier that
matches an autoload name (e.g., `GameManager`, `AudioManager`).

**Fix protocol**:
1. Find the ROOT script (the autoload or base class with the actual error)
2. Fix ONLY that script
3. `godot_reload_filesystem()` + `godot_get_errors()`
4. Most cascading errors will disappear
5. Fix any remaining errors individually

### "Cannot preload resource"
**Cause**: Script uses `preload()` for a file that doesn't exist yet.
**Fix**: Replace `preload()` with `load()` in the script.

### "Invalid call to function 'X' in base 'Y'"
**Cause**: Calling a method that doesn't exist on that node type.
**Fix**: Check the node type. Call `godot_get_class_info("Y")` to get correct API. Common mistake: calling physics methods on wrong body type.

### "Identifier 'X' not declared in current scope"
**Cause**: Using a variable/function that doesn't exist.
**Fix**: Check spelling, check if it's defined in the right scope, check imports. If X is an autoload, verify it's in project.godot [autoload] section.

### Scene parse errors
**Cause**: Malformed .tscn file.
**Fix**: Check `load_steps` count, parent paths, quote formatting.
**Better**: Rewrite as programmatic scene (script builds nodes in `_ready()`).

### "Node not found: 'X'"
**Cause**: `$NodeName` references a node that doesn't exist in the tree.
**Fix**: Either the node isn't created yet (use `@onready` or build in `_ready()`), or it has a different name. Call `godot_get_scene_tree()` to verify actual node names.

### Collision not working
**Cause**: Layer/mask mismatch.
**Fix**: Use `set_collision_layer_value()` and `set_collision_mask_value()` to be explicit. Check:
- Bullets (Area2D): layer must be set, mask must include enemy layer
- Area2D.body_entered: only fires for CharacterBody2D/RigidBody2D/StaticBody2D
- Area2D.area_entered: only fires for other Area2Ds

## Setting Main Scene

After generating a game, always set the main scene:

**Via project.godot** (edit the file directly):
```ini
[application]
run/main_scene="res://scenes/main.tscn"
```

**Via MCP**: The `godot_reload_filesystem` will pick up the change.

## Preflight Checklist

Before running:
- [ ] All scripts have correct `extends` (CharacterBody2D, Area2D, Node2D, etc.)
- [ ] All `load()` paths point to files that exist
- [ ] Collision layers/masks are set
- [ ] Groups are assigned (`"player"`, `"enemies"`, etc.)
- [ ] Main scene is set in project.godot
- [ ] `godot_reload_filesystem` was called

## When Godot Editor Is Not Connected

If `godot_get_project_state` shows `editor_connected: false`:
1. File operations still work (Write tool writes directly)
2. `godot_scan_project_files` still works (reads filesystem)
3. `godot_parse_scene` still works (reads .tscn files)
4. `godot_generate_asset` still works (creates SVG/PNG files)
5. BUT: `godot_run_scene`, `godot_stop_scene`, `godot_get_errors`, `godot_reload_filesystem` will fail

Tell the user: "Please open the Godot editor and enable the AI Game Builder plugin, then try again."
