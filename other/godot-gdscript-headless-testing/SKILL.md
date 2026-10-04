---
name: godot-gdscript-headless-testing
description: >
  Run GDScript test suites from the command line with `godot --headless`, using a
  SceneTree/MainLoop runner script that exits non-zero on failure so CI can gate
  merges. Use when a Godot project needs unit tests without opening the editor,
  when wiring a CI job (GitHub Actions or similar) that must fail the build on a
  failing `.gd` test, or when a `godot --headless` invocation hangs, opens a
  window, or exits 0 despite failed assertions.
---

# Godot GDScript headless testing (4.x)

Run GDScript tests from the command line, without the editor GUI, and get a real
process exit code CI can act on. Targets **Godot 4.7** headless CLI.

## When to use

- Use when a Godot project has no testing addon installed and needs a fast way to
  verify GDScript logic (pure functions, resource loading, autoload state) from a
  terminal or CI pipeline.
- Use when wiring a CI job that must fail the build when a `.gd` test fails.
- Use when debugging why a `godot --headless` invocation hangs, opens a window, or
  exits 0 despite failing assertions.

**When *not* to use:** GDScript syntax or language features themselves →
`godot-gdscript`; export/build pipeline and platform templates → `godot-export`
(its own `--headless` use case, producing a binary, not running tests).

## Workflow

1. **Confirm the binary resolves headless.** Godot 4.x ships `--headless` built in
   (no export template needed); run `godot --headless --version` and confirm it
   prints a version string, not a GUI window.
2. **On a fresh checkout, import before running tests.** `.godot/` is normally not
   committed, so a clean checkout has no import cache: `class_name` types fail to
   resolve (`Identifier "X" not declared in the current scope`) and imported
   assets fail to load (`No loader found for resource: res://...`). Run
   `godot --headless --path <project_dir> --import` once first, in CI and locally.
3. **Write the runner as a `SceneTree` script, not a `Node` scene.** A `SceneTree`
   script's `_initialize()` runs once before any frame — enough for pure-logic
   tests and no `.tscn` required to launch.
4. **Track pass/fail counts yourself and call `quit(<code>)` explicitly. Do not use
   bare `assert()` to fail a test.** Godot does not turn the process exit code
   non-zero on `push_error()` by itself — the runner must count failures and call
   `quit(1)`. Worse, a failed `assert()` inside `_initialize()` (official/debug
   build) prints `SCRIPT ERROR: Assertion failed` and **stops execution before
   `quit()` runs**, so the process never exits and CI hangs until its own timeout.
   Use an `assert_eq()`-style helper that records the failure and keeps going.
5. **Invoke with `godot --headless --path <project_dir> --script res://<runner>.gd`**
   and read the **process exit code**, not just stdout, from the shell or CI step.
   `--script` accepts both a `res://`-relative path and an absolute filesystem
   path (e.g. a runner outside the project folder); either works.
6. **Redirect stdout and stderr to files when scripting the invocation from a
   wrapper shell** (PowerShell, some CI runners). `push_error()` output goes to
   stderr and can be dropped or reordered when only stdout is captured live.
7. **Add a step timeout in CI.** Even with the `assert()` pitfall avoided, an
   `await` that never resolves (Pattern #2) hangs the runner forever; a
   `timeout-minutes` on the CI step is a backstop CI-side, not a substitute for
   backing every `await` with a timeout node.

## Patterns

### 1. Minimal SceneTree test runner with a real exit code

```gdscript
# res://test_runner.gd — run with:
#   godot --headless --path . --script res://test_runner.gd
extends SceneTree

var passed := 0
var failed := 0

func _initialize() -> void:
    test_add()
    print("Results: %d passed, %d failed" % [passed, failed])
    quit(1 if failed > 0 else 0)   # non-zero exit fails the CI step

func assert_eq(actual, expected, label: String) -> void:
    if actual == expected:
        passed += 1
    else:
        failed += 1
        push_error("FAIL %s: expected %s, got %s" % [label, expected, actual])

func test_add() -> void:
    assert_eq(2 + 2, 4, "test_add")
```

Verified against Godot 4.7.2: `godot --headless --path . --script
res://test_runner.gd` prints `Results: N passed, M failed` to stdout, routes
`push_error` lines to stderr, and returns process exit code `0` when
`failed == 0`, `1` otherwise.

### 2. Testing something that needs a frame, a timer, or a signal

```gdscript
extends SceneTree

var passed := 0
var failed := 0

func _initialize() -> void:
    await run_tests()
    print("Results: %d passed, %d failed" % [passed, failed])
    quit(1 if failed > 0 else 0)   # track and report failures here too

func assert_eq(actual, expected, label: String) -> void:
    if actual == expected:
        passed += 1
    else:
        failed += 1
        push_error("FAIL %s: expected %s, got %s" % [label, expected, actual])

func run_tests() -> void:
    # `root` is not inside the tree yet during _initialize(): a Timer started now
    # errors ("not inside the tree") and its `timeout` never fires. Wait one frame.
    await process_frame
    var timer_node := Timer.new()
    timer_node.one_shot = true   # default Timer restarts after timeout
    root.add_child(timer_node)
    timer_node.start(0.1)
    await timer_node.timeout
    # assertions here can rely on the node having been in the tree for a frame
    assert_eq(timer_node.is_stopped(), true, "timer_fires_once")
    timer_node.queue_free()
```

`_initialize()` may `await`, which is what makes this pattern work for anything
that needs a node to actually enter the tree, a timer to fire, or a signal to
emit — none of which happen before the engine has processed at least one frame.
Use the same `passed`/`failed` counter and `assert_eq()` helper as Pattern #1;
a version of this pattern that always calls `quit(0)` can never fail a build.

### 3. CI step (GitHub Actions) that gates on the exit code

```yaml
- name: Import project (populates .godot/ on a fresh checkout)
  run: godot --headless --path . --import
- name: Run GDScript tests
  timeout-minutes: 5
  run: godot --headless --path . --script res://test_runner.gd
```

The import step is required on a clean checkout — without it, `class_name` types
and imported resources fail to resolve. No extra flag is needed for the test
step itself: the runner already fails the job on a non-zero exit code from
`run:`; the discipline lives in the runner script's `quit()` call, not in the CI
configuration. `timeout-minutes` is a backstop against a hung `await` (see
Pitfalls), not a substitute for backing every `await` with a timeout node.

## Pitfalls

- **Script "does nothing" or opens the editor window** → missing `--headless`, or
  the script path is wrong. `--script` accepts a `res://`-relative path resolved
  against `--path <project_dir>`, and also an absolute filesystem path — both work.
- **`Identifier "X" not declared in the current scope`, or a resource fails to
  load, only on a fresh checkout** → `.godot/` (the import cache) is normally not
  committed, so `class_name` types and imported assets aren't resolved yet. Run
  `godot --headless --path <project_dir> --import` once before the test step.
- **A failed `assert()` hangs instead of failing the test** → in an official/debug
  build, a failed `assert()` inside `_initialize()` prints `SCRIPT ERROR:
  Assertion failed` and stops that function before it reaches `quit()` — the
  process never exits and CI waits until its own timeout. Use an `assert_eq()`
  counter (Pattern #1) instead of bare `assert()` in test runners.
- **Exit code stays 0 despite failed assertions** → the runner never called
  `quit(1)`, or (Pattern #2) it always calls `quit(0)` regardless of failures.
  Track failures yourself and call `quit()` explicitly with a code that reflects
  them; do not rely on `assert()` or `push_error()` alone to change the exit code.
- **`_initialize()` runs before nodes, timers, or signals exist** → logic that
  needs a frame to have processed must `await` a signal or a timer before
  asserting; see Pattern #2. `root` itself is not inside the tree yet, so a
  `Timer` added and started there errors and its `timeout` never fires (the
  runner hangs) — `await process_frame` first.
- **Output looks empty or out of order from a wrapper shell** → some shells
  (PowerShell in particular) can reorder or drop a native process's live
  stdout/stderr. Redirect both streams to files and read the files after the
  process exits, instead of trusting the live console.
- **Runner never terminates** → a `SceneTree` script keeps running until
  something calls `quit()`. A test that `await`s a signal that never fires hangs
  the job forever — always back an `await` with a timeout node as a fallback, and
  set `timeout-minutes` on the CI step as a backstop.

## Related skills

- `godot-gdscript` — the language syntax and node lifecycle this pattern's
  runner script itself uses.
- `godot-export` — headless CLI export/build, a different `--headless` use case.
