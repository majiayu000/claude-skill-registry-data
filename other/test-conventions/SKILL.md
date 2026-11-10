---
name: test-conventions
description: How tests are written in Iron Pipeline — acceptance tests per scenario, FsCheck properties, seeding GameState directly, the IRandom fixture, golden replays, GdUnit4 scene tests that never click through setup, no sleeps, no assertions on engine internals. Load before writing or reviewing any test.
---
# Test conventions (written once, used by every change)

## Layers
| Layer | Where | Naming |
|---|---|---|
| Acceptance (one per scenario) | `IronPipeline.Sim.Tests/<Area>/<Name>AcceptanceTests.cs` | `S<NN>_<Scenario>` |
| Property (invariants) | `IronPipeline.Sim.Tests/<Area>/<Name>PropertyTests.cs` | `<Invariant>` e.g. `SupplyIsConserved` |
| Golden replay | `tests/replays/<name>.replay` + hash | run by `IronPipeline.Tools replay` |
| Scene/UI wiring | `IronPipeline.Game/tests/` (GdUnit4, C#) | `<Scene>_<Behavior>` |

## Seed state, never play to it
Build the exact state a scenario needs directly. Until spec 0004 introduces `GameState` and the builders (`GameStateBuilder`, `UnitBuilder`, `MapBuilder` under `IronPipeline.Sim.Tests/Fixtures/`), construct value types and maps inline; once they exist, Givens map 1:1 to builder calls. A test never issues commands just to reach its starting position.

## Randomness
Once spec 0006 introduces `IRandom`, tests inject `new SeededRandom(1)`; a scenario that depends on a roll states the seed in its Given. Never use `System.Random` in tests.

## Oracles are numbers
An acceptance test asserts concrete expected values — a number from the Spec, an exact coordinate, an exact count, identity (`a == b`) — never a relative claim like "greater than before" or "not null" alone. Property tests assert invariants over generated inputs (FsCheck), bounded to realistic ranges.

## Golden replays
A replay is `seed + command log → final state hash`. Changing a hash on purpose requires a one-line reason in the PR ("Decisions made at the build gate") and the `save-and-replay-compat` reviewer's sign-off. Never regenerate hashes to make a test pass.

## Scene tests (GdUnit4)
- Construct state, hand it to the scene, assert on **emitted Commands/events and Sim queries** — never on Godot node trees, class names or pixel positions.
- Await signals, never `Task.Delay` / timers.
- One scene-test file per Features number so parallel work never edits the same file.
- Feel is not tested here; that's the playtest checklist.

## Refactor evidence
Every batch (behavior → test → green) leaves evidence of the refactor step: a `refactor:` commit, or a `no refactor: <reason>` line in the batch's commit body. Tests are frozen during the refactor. Reviewers check "refactor evidence present per batch".

## Smells that fail review
Sleeps · commanding through setup · asserting on engine internals · an acceptance test with only relative or null-check assertions · tests edited during a refactor step · a `[Fact]` that duplicates a property · scenario IDs that don't match the Features file · a batch with no refactor evidence.
