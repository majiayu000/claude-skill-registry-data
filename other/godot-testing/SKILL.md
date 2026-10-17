---
name: godot-testing
category: testing
description: Use when writing or running Godot tests - gdUnit4 or GUT (whichever the repo has), unit tests on typed GDScript classes, scene runners for frames, physics, input and signals, headless CLI with --import first, reports and exit codes, and C# tests via gdUnit4Net or plain dotnet test.
tech_stack: Godot
source: informed by the gdUnit4 and GUT documentation and the Godot 4 command-line docs; own wording
---
# Godot Testing

## Overview

Godot has two mature test frameworks: **gdUnit4** (GDScript and C#, fluent assertions, scene runner, mocks) and **GUT** (GDScript, simple assertions, doubles). Use the one in `addons/`; if neither exists, add gdUnit4. Test plain typed classes directly; use a scene runner only for behaviour that needs frames, physics, input or the tree.

**Core principle:** Unit-test the class, scene-test the wiring, and run it headless with an exit code you read.

## gdUnit4

```gdscript
# res://test/combat/health_component_test.gd
class_name HealthComponentTest extends GdUnitTestSuite

func test_damage_beyond_health_clamps_to_zero() -> void:
    var health: HealthComponent = auto_free(HealthComponent.new())
    health.max_health = 50
    health.reset()

    health.damage(80)

    assert_int(health.current).is_equal(0)

func test_lethal_damage_emits_died() -> void:
    var health: HealthComponent = auto_free(HealthComponent.new())
    health.max_health = 10
    health.reset()
    monitor_signals(health)          # start collecting before the action, or an already-emitted signal is missed
    health.damage(10)
    await assert_signal(health).is_emitted("died")

func test_player_falls_onto_floor_and_is_grounded() -> void:
    var runner := scene_runner("res://test/scenes/flat_floor_with_player.tscn")
    await runner.simulate_frames(90)
    var player := runner.find_child("Player") as Player
    assert_bool(player.is_on_floor()).is_true()

func test_jump_action_leaves_the_ground() -> void:
    var runner := scene_runner("res://test/scenes/flat_floor_with_player.tscn")
    await runner.simulate_frames(30)
    runner.simulate_action_pressed("jump")
    await runner.simulate_frames(5)
    assert_float((runner.find_child("Player") as Player).velocity.y).is_less(0.0)
```

- `auto_free()` frees the object after the test; nodes added to the tree go through the runner or `add_child(auto_free(node))`.
- `mock(Class)` / `spy(instance)` with `verify(...)` exist — prefer real collaborators and fakes; assert outcomes, not calls.
- Parameterised tests: a default argument `test_parameters := [[...], [...]]`.

## GUT

```gdscript
# res://test/unit/test_inventory.gd
extends GutTest

var _inv: Inventory

func before_each() -> void:
    _inv = Inventory.new(4)

func test_add_beyond_stack_limit_overflows_to_next_slot() -> void:
    _inv.add(&"potion", 7, 5)
    assert_eq(_inv.slots[0].count, 5)
    assert_eq(_inv.slots[1].count, 2)

func test_enemy_death_emits_signal() -> void:
    var enemy: Enemy = add_child_autofree(preload("res://enemies/slime.tscn").instantiate())
    watch_signals(enemy.health)
    enemy.health.damage(9999)
    assert_signal_emitted(enemy.health, "died")
```

`simulate(node, frames, delta)` advances `_process`/`_physics_process` deterministically; `double(Script)` + `stub(...)` for doubles.

## Naming and layout

Follow the repository. Without a convention: `res://test/<area>/<thing>_test.gd` (gdUnit4) or `res://test/unit/test_<thing>.gd` (GUT), and test functions `test_<scenario>_<expected>`. Small dedicated test scenes under `res://test/scenes/`, never production levels.

## Running headless

```sh
mkdir -p /tmp/tt-<task key>
godot --headless --path . --import                       # builds the import and class_name caches; needed on a fresh checkout
# gdUnit4
godot --headless --path . -s addons/gdUnit4/bin/GdUnitCmdTool.gd --ignoreHeadlessMode \
      -a res://test -rd /tmp/tt-<task key>/gdunit > /tmp/tt-<task key>/gdunit.log 2>&1; echo "exit=$?"
# GUT
godot --headless --path . -s addons/gut/gut_cmdln.gd -gdir=res://test -ginclude_subdirs \
      -gjunit_xml_file=/tmp/tt-<task key>/gut.xml -gexit > /tmp/tt-<task key>/gut.log 2>&1; echo "exit=$?"
```

- gdUnit4 refuses `--headless` without `--ignoreHeadlessMode`, because Godot does not deliver input events in headless mode. Pure logic, signal, physics and frame tests run fine headless; tests that simulate input need a display — run them without `--headless` (or under `xvfb-run` on Linux) or report them as not run.
- gdUnit4 exit codes: 0 all passed, 100 failures, 101 warnings only. Its JUnit `results.xml` and HTML report land in the `-rd` directory. The `addons/gdUnit4/runtest.sh` wrapper does the same using `GODOT_BIN`.
- GUT: a `.gutconfig.json` in the project root is picked up by the CLI; `-gexit` makes it quit with a non-zero code on failure.
- A parse error in any script fails the import or the run before tests start — read the log for `SCRIPT ERROR` / `Parse Error`; zero tests run is not a pass.

## C# projects

- gdUnit4Net runs C# tests through `dotnet test` with a test adapter (it needs `GODOT_BIN` pointing at the .NET build of Godot).
- Rules in plain C# classes with no `Godot` namespace can live in a separate class library tested with ordinary xUnit/NUnit and `dotnet test` — this also runs when Godot is not installed (godot-csharp-and-gdextension).

## No Godot binary here

GDScript cannot run without the engine. Write the tests anyway, keep them small and obviously correct, and report: `NOT RUN: godot not found on PATH (project pins 4.7) — 3 gdUnit4 tests written in res://test/combat/`.

## Common Mistakes

- Skipping `--import` on a fresh checkout, then "Could not find type HealthComponent".
- Testing a rule through a whole level scene.
- Waiting with timers (`await get_tree().create_timer(1.0).timeout`) instead of simulating frames.
- Leaking nodes: `Node.new()` without `auto_free` / `autofree`, producing orphan warnings and cross-test pollution.

## Red Flags

- An input test reported as passing from a headless run (input events are not delivered there).
- No exit-code check after the CLI run.
- Tests that load production scenes and depend on their current layout.
