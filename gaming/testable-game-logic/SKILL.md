---
name: testable-game-logic
category: testing
description: Use when starting any game task, before writing tests - find out which editors and runners exist on this machine, keep gameplay rules in engine-independent classes with an injected clock and seeded RNG, and report exactly what could not run.
tech_stack: Game core
source: informed by Donchitos/Claude-Code-Game-Studios and the Unity, Godot, Unreal and Bevy test-runner docs; own wording
---
# Testable Game Logic

## Overview

You run headless on the user's machine. A web game or a Bevy crate can always be built and tested; a Unity, Unreal or Godot editor may or may not be installed, licensed and at the right version. The answer is the same in every engine: gameplay rules live in plain classes that a plain runner can drive, and engine callbacks are thin adapters that feed them input, time and randomness.

**Core principle:** If a rule can only be tested by pressing Play, it is in the wrong class. And a test you wrote but could not run is reported as exactly that — never as a pass.

## What can run here

Run these first, in one step, and keep the answers for the plan.

```sh
# Unity: the exact editor version the project pins
grep m_EditorVersion ProjectSettings/ProjectVersion.txt
ls "/Applications/Unity/Hub/Editor/" 2>/dev/null            # macOS
ls "$HOME/Unity/Hub/Editor/" 2>/dev/null                    # Linux
echo "$UNITY_PATH"
# macOS binary: /Applications/Unity/Hub/Editor/<ver>/Unity.app/Contents/MacOS/Unity
# Windows: C:\Program Files\Unity\Hub\Editor\<ver>\Editor\Unity.exe ; Linux: ~/Unity/Hub/Editor/<ver>/Editor/Unity

# Godot: binary and version must match config/features (major.minor); .NET projects need the .NET build
which godot godot4 2>/dev/null; godot --version 2>/dev/null
ls /Applications/Godot*.app/Contents/MacOS/ 2>/dev/null

# Unreal: EngineAssociation in the .uproject names the install
grep EngineAssociation *.uproject
ls "/Users/Shared/Epic Games/" 2>/dev/null                  # macOS; Windows: C:\Program Files\Epic Games\UE_5.x
# binary: <engine>/Engine/Binaries/<Mac|Win64|Linux>/UnrealEditor-Cmd

node -v; cargo --version; dotnet --version; python3 --version 2>/dev/null
```

Rules:
- Use only the editor whose version matches the pin. A different Unity or Unreal version re-imports and re-serializes the project; a different Godot minor rewrites `project.godot`.
- Never install or download an editor on your own initiative. Missing is a finding to report, not a problem to solve.
- Unity batchmode needs an activated licence; a licensing error in the log is "could not run", not a test failure of yours.
- First builds are slow (Unreal C++, Bevy, Unity import). Give `run_terminal` a long timeout, or run detached to `/tmp/tt-<task key>/<step>.log` and read the log.

## The layering

```
Rules (plain C# / GDScript RefCounted / C++ struct / TS module / Rust fn)   ← unit tests, any runner
   ↑ called by
Engine adapter (MonoBehaviour / Node / Actor component / Phaser scene / Bevy system)  ← engine tests
   ↑ wired in
Scenes, prefabs, Blueprints, data assets                                     ← looked at (game-visual-self-review)
```

The adapter reads input and `deltaTime`, calls the rule, and applies the result to the engine (transform, animation, UI event). It contains no `if` about game rules.

## Worked example (Unity, C#)

```csharp
// ❌ rule welded to the engine: untestable without Play mode, reads global time
public class Dash : MonoBehaviour {
    float _lastDash;
    void Update() {
        if (Input.GetKeyDown(KeyCode.Space) && Time.time - _lastDash > 1.5f) {
            _lastDash = Time.time;
            GetComponent<Rigidbody>().AddForce(transform.forward * 20, ForceMode.Impulse);
        }
    }
}

// ✅ rule in a plain class (assembly with noEngineReferences), time passed in
public sealed class Cooldown {
    readonly float _duration; float _remaining;
    public Cooldown(float duration) => _duration = duration;
    public bool IsReady => _remaining <= 0f;
    public void Tick(float dt) => _remaining = MathF.Max(0f, _remaining - dt);
    public bool TryConsume() { if (!IsReady) return false; _remaining = _duration; return true; }
}

[Test] public void TryConsume_WhileCoolingDown_ReturnsFalse() {
    var c = new Cooldown(1.5f);
    Assert.That(c.TryConsume(), Is.True);
    c.Tick(1.0f);
    Assert.That(c.TryConsume(), Is.False);
    c.Tick(0.5f);
    Assert.That(c.TryConsume(), Is.True);
}
```

The adapter `DashAbility : MonoBehaviour` caches its `Rigidbody` in `Awake`, ticks the cooldown in `Update` with `Time.deltaTime`, and applies the impulse in `FixedUpdate` when an input flag is set — three lines with no rule in them.

## When the editor is missing

| Engine | Runs without the editor | How |
|---|---|---|
| Unity | Rules in an asmdef with `"noEngineReferences": true` | A throwaway `net8.0` NUnit project in `/tmp/tt-<task key>/` that compiles those sources: `<Compile Include="<repo>/Assets/Scripts/Core/**/*.cs" />`, then `dotnet test`. Commit the EditMode test in the repo either way. |
| Godot (C#) | Plain C# classes with no `Godot` namespace | A class-library project referenced by an xUnit/NUnit project, `dotnet test` |
| Godot (GDScript) | Nothing — GDScript needs the Godot binary | Write the gdUnit4/GUT test anyway and report it as not run |
| Unreal | Nothing — even pure C++ in a module needs the engine build | Write the Automation Spec anyway and report it as not run |
| Web, Bevy, MonoGame, pygame | Everything | Vitest, `cargo test`, `dotnet test`, `pytest` |

If the repository already has such a plain-runner project (a `Tests.Core.csproj`, a `logic/` crate), use it instead of a throwaway one.

## Time, randomness and input are parameters

- **Time:** rules take `dt` (or an `IClock`), never read `Time.time`, `OS.get_ticks_msec()`, `performance.now()` or `Instant::now()` themselves.
- **Randomness:** one seeded generator passed in — `new System.Random(seed)`, `RandomNumberGenerator` with `.seed`, a `mulberry32(seed)` in TS, `ChaCha8Rng::seed_from_u64(seed)` in Rust. A test fixes the seed; the game seeds from the clock or the save.
- **Input:** rules receive intents (`MoveIntent(x, y)`, `Jump`), not key codes. Rebinding then never touches a rule.

## Tests that games specifically need

- **Two-delta test** for anything time-based: run 1 s as 60×(1/60) and as 30×(1/30); assert the same result within tolerance (frame-rate-independence).
- **Determinism test** where replays, lockstep or rollback exist: same seed + same input log → same state hash after N steps.
- **Table-driven transition test** for every state machine (game-state-machines-and-ai).
- **Data invariant test** over every shipped data asset: no zero-weight drop table, no negative damage, every referenced ID exists (data-driven-gameplay-design).
- **Regression test** for every bug, watched failing before the fix.
- **Performance test** with a threshold that fails when exceeded, for a hot path you changed (game-performance-budget).

Naming follows the repository; without a convention: NUnit `Method_Scenario_Expected`, gdUnit4/GUT `test_<scenario>_<expected>`, Unreal `Project.System.Scenario`, Vitest/`cargo test` a sentence describing the behaviour.

## Reporting what could not run

One line per command in the closing message, verbatim:

```
NOT RUN: Unity 6000.3.2f1 not installed (Hub has 6000.0.40f1 only) — EditMode tests in Assets/Tests/EditMode/CooldownTests.cs written, not executed.
RAN: dotnet test /tmp/tt-T-42/core-tests → 12 passed, 0 failed (Core sources compiled without UnityEngine).
```

## Common Mistakes

- Testing a rule through a MonoBehaviour, Node or Actor because "that's where the code was".
- Reading global time or `Random` inside a rule, then fighting flaky tests.
- Running the tests in a mismatched editor version and committing the re-import churn.
- Calling a run "verified" when the headless editor exited on a licence error.

## Red Flags

- A rule class that imports `UnityEngine`, `Godot`, `Phaser` or `bevy::prelude` without needing it.
- A closing message with no `RAN:`/`NOT RUN:` accounting on an engine project.
- A test that only passes at one frame rate.
