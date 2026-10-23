---
name: gameplay-recording-replay
description: "Build a deterministic gameplay record/replay test artefact for Unity, Unreal, or Godot - record a player session, save it to disk, replay it bit-for-bit, and assert that the resulting game state matches the original. Covers Unity Input System's InputEventTrace API (Enable / Disable / WriteTo / ReadFrom / Replay) for input-level capture, Unreal's Replay System (DemoRec / DemoPlay / DemoStop console commands plus DemoNetDriver + NetworkReplayStreamer, default storage at %LOCALAPPDATA%/{Project}/Saved/Demos) for replication-stream capture, and Godot's community-pattern deterministic-RNG + input-script replay since Godot ships no first-party replay system. Use when authoring a regression-test artefact for player-recorded sessions, building a netcode replay for spectator / esports, or producing reproducible bug repros for cert teams."
metadata:
  keywords: "replay, recording, input-trace, demonet, deterministic, regression, unity, unreal, godot, esports"
  version: "1.4.14"
---

# gameplay-recording-replay

## Overview

A **deterministic replay artefact** is a recorded session of
player input or replicated state that can be played back to
recreate the original game state. Three reasons games invest in
replays:

1. **Regression tests.** Record a scripted playthrough; replay it
   in CI; assert the final state matches the original. Catches
   physics drift, AI determinism breaks, save-format regressions.
2. **Bug repros.** Players record a session; QA replays it inside
   the build with the bug; cert teams attach the replay to the
   ticket.
3. **Esports / spectator / clip sharing.** Match replays surfaced
   in-product.

This is a **workflow** that produces, per engine, a working
record/replay setup plus a CI regression test that runs it. The
full per-engine record, replay, and CI code lives in
[references/engine-record-replay-apis.md](references/engine-record-replay-apis.md);
this file is the cross-engine decision surface.

The three engine surfaces differ:

| Engine | Recording surface | Stability of public docs |
|---|---|---|
| Unity | Input System's `InputEventTrace` (input-level) | Public - [com.unity.inputsystem@1.8 API](https://docs.unity3d.com/Packages/com.unity.inputsystem@1.8/api/UnityEngine.InputSystem.LowLevel.InputEventTrace.html) |
| Unreal | Replay System (replication-stream level) - `DemoRec` / `DemoPlay` / `DemoStop` | Public - [Replays in Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/replays-in-unreal-engine) |
| Godot | No first-party replay - community pattern: deterministic RNG seed + recorded `InputEvent` script | Community - Godot documentation does not ship a replay subsystem [author opinion, per [docs.godotengine.org](https://docs.godotengine.org/en/stable/)] |

Composes with:

- `unity-test-framework`,
  `unreal-automation-system`,
  `godot-gut-tests` - the host test
  framework the replay runs inside.
- `multiplayer-state-machine-coverage` - 
  Unreal's Replay system shares `NetworkReplayStreamer` with its
  multiplayer stack; multiplayer fixtures can replay captured
  sessions.
- `platform-cert-overview-reference` - 
  replays are evidence artefacts for cert (Xbox **XR-003** title
  quality, attaching a repro to a CFR).

## When to use

- Producing a deterministic regression test for a story
  playthrough / level traversal / damage script.
- Building an in-product replay feature (spectator mode, instant
  replay, clip sharing).
- Producing reproducible repro artefacts for cert teams.
- Investigating a determinism regression - "this build diverges
  from the previous build's replay at frame 4823."

## How to use

1. **Lock determinism first** for the capture level you need -
   fix the Step 1 sources of non-determinism (fixed timestep,
   seeded RNG, synchronous loads) before recording anything.
2. **Pick the capture level** from the Step 2 per-engine contract
   table - Unity and Godot capture input (which needs determinism);
   Unreal captures the replication stream (which does not).
3. **Record and replay** with the engine's API - full working
   code in
   [references/engine-record-replay-apis.md](references/engine-record-replay-apis.md).
4. **Choose the assertion model** (final-state hash, per-checkpoint,
   or per-frame) and wire the replay into a CI regression test
   (Step 3).
5. **Embed a build hash + replay-format version** in the replay
   header so CI can tell a real regression from a stale replay
   (Step 4).

## Inputs

Gather before walking the workflow:

| Input | Where | Why |
|---|---|---|
| Engine + version | Project | Determines which API surface applies |
| Determinism baseline | Game design - is fixed-tick physics on? RNG seeded? AI deterministic? | Replays only work when the game's per-frame outputs are functions of (state + input) |
| Recording scope | Input-only? Full replication stream? | Trades off file size against determinism guarantees |
| Target storage location | `Application.persistentDataPath`, `%LOCALAPPDATA%/<Project>/Saved/Demos`, etc. | Where replay files land |
| Replay length budget | Seconds / minutes | InputEventTrace buffer sizing |
| Assertion model | Final-state hash? Per-frame? Checkpoint-only? | Drives the test harness shape |

## Workflow

### Step 1 - Establish determinism

Replays are worthless if the game is non-deterministic. Before
any recording work, lock down:

| Source of non-determinism | Lock-down |
|---|---|
| Variable timestep / `Time.deltaTime` | Run physics on `FixedUpdate` (Unity) / `TickGroup` (Unreal) with a fixed delta |
| Unseeded `Random` | Seed every RNG at session start; record the seed in the replay header |
| Async load timing | Force synchronous load during replay (`SceneManager.LoadScene` sync; `AssetRegistry::Tick` to drain) |
| Multithreaded game logic | Pin to one thread or commit to ordered consumption of results |
| Frame-rate-dependent FX | Tag visual-only systems and skip them in headless replay runs |

If you can't lock determinism, replay can still be useful as a
**visual debug** artefact, but it won't drive regression assertions.

### Step 2 - Record and replay per engine

Each engine captures at a different level, with a different
determinism contract. Pick the row that matches your engine, then
lift the working record + replay code from
[references/engine-record-replay-apis.md](references/engine-record-replay-apis.md).

| Engine | Capture level | Default storage | Determinism contract |
|---|---|---|---|
| Unity | Input events (`InputEventTrace`, buffer-sized) | `Application.persistentDataPath` / repo `test/` | Needs Step 1 - replay reproduces input; state matches only if the sim is a pure function of state + input |
| Unreal | Replication stream (`DemoNetDriver` + `NetworkReplayStreamer`) | `%LOCALAPPDATA%/<Project>/Saved/Demos` | Reconstructs the server's streamed view - does **not** require local determinism |
| Godot | Input events + RNG seed (community pattern) | `FileAccess` path of choice | Same contract as Unity - needs Step 1 |

The key split: **input-level replay (Unity, Godot) depends on
determinism; replication-stream replay (Unreal) does not**, because
the Unreal simulation already ran on the server and the replay just
re-streams its output. This is why Unreal replays handle full
multiplayer matches while Unity/Godot replays are for pinned
single-player.

### Step 3 - Wire replays as CI regression assertions

Per engine, the CI loop is:

1. Check the replay file into the repo under `test/replays/`.
2. CI job loads the build, plays the replay, hashes the final
   game state.
3. Compare the hash against the baseline (also in repo).
4. Mismatch → CI fails the build.

The per-engine harness code (Unity `[UnityTest]` PlayMode fixture,
Unreal `LatentIt` latent command, Godot GUT fixture) is in
[references/engine-record-replay-apis.md](references/engine-record-replay-apis.md).

### Step 4 - Define a fail-safe for replay drift

Real-world replays drift when:

- The game build version changed and the replay was recorded
  against an earlier version.
- A non-deterministic source slipped in (new async loader, new
  particle system using `Random`).
- The save format changed.

The harness must distinguish **bug-in-build** from
**replay-stale**. Encode the build hash + replay format version
in the replay header; CI rejects replays whose `replay_format <
current_format`, then either re-records (acceptable for visual
replays) or fails the build (regression test replays).

## Worked example - Unity speedrun regression

Inputs:

- **Engine:** Unity 6.0, Input System v1.8.
- **Determinism:** Physics at `FixedUpdate`, 60 Hz; RNG seeded
  from replay header; AI scripted via deterministic state
  machines.
- **Recording scope:** Input-only via InputEventTrace.
- **Storage:** `Assets/Tests/Replays/level1.trace` (committed to
  the repo).
- **Length budget:** 90 s - fits comfortably in 4 MB buffer
  (`recordFrameMarkers = true` per the
  [API page](https://docs.unity3d.com/Packages/com.unity.inputsystem@1.8/api/UnityEngine.InputSystem.LowLevel.InputEventTrace.html)).
- **Assertion:** SHA-256 hash of `GameStateRoot.Serialize()` at
  T=90 s.

Step 1 - physics on FixedUpdate, RNG seeded from replay header,
async loads forced synchronous in headless mode.

Step 2 - recorder MonoBehaviour creates `InputEventTrace`, enables
on level start, writes to `level1.trace` on first level completion.

Step 3 - CI fixture (UTF `[UnityTest]`) reads the trace, replays
it, hashes the final `GameStateRoot`, compares to the baseline
hash committed in `Assets/Tests/Baselines/level1.hash`.

Step 4 - replay header includes `replay_format = 2` and
`build_hash = <git-sha>`. CI fails the build with a clear "replay
stale" message when format < 2 rather than silently passing.

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Recording input without seeding RNG | Replay diverges by frame ~30 | Step 1 - every RNG seeded; seed in replay header |
| `InputEventTrace` without `Dispose()` | Memory leak per [API page](https://docs.unity3d.com/Packages/com.unity.inputsystem@1.8/api/UnityEngine.InputSystem.LowLevel.InputEventTrace.html) - "must be disposed of … or they will leak memory on the unmanaged (C++) memory heap" | Always `using` / `Dispose()` |
| `InputEventTrace` without `recordFrameMarkers = true` | Replay reissues events back-to-back instead of respecting timing per [API page](https://docs.unity3d.com/Packages/com.unity.inputsystem@1.8/api/UnityEngine.InputSystem.LowLevel.InputEventTrace.html) | Set `recordFrameMarkers = true` before `Enable()` |
| Comparing per-frame state instead of checkpoints | False-positive failures from float-precision drift | Hash at coarse-grained checkpoints (every N seconds or per level) |
| Treating Unreal replays as deterministic input replays | They're replication-stream replays - different determinism contract per [Replays page](https://dev.epicgames.com/documentation/en-us/unreal-engine/replays-in-unreal-engine) | Document the contract; don't assume input-level determinism |
| Storing replay format version implicitly | Replay-stale failures get misdiagnosed as bugs | Embed `replay_format` + `build_hash` in the header |
| Replays committed without their baselines | Asserting nothing | Commit `replay.trace` + `baseline.hash` as a pair |
| Replays > 30 min in CI | Replay run time dominates total job time | Split into checkpointed mini-replays |
| Replay scrubbing in test fixtures | Many engines don't expose deterministic scrubbing for tests | Linear playback only in regression fixtures; scrubbing is a feature, not a test surface |
| Replays storing PII | Saved player names / chat messages in attached repros | Strip PII from replay headers before sharing |

## Limitations

- **Input-level replay (Unity) and replication-stream replay
  (Unreal) are different contracts.** Unity replays depend on
  determinism; Unreal replays reconstruct the server's view and
  do not. Don't conflate them in a multi-engine team.
- **Godot has no first-party replay system** per the
  [Godot documentation home](https://docs.godotengine.org/en/stable/);
  the community pattern in Step 2 is sufficient for deterministic
  single-player but doesn't generalise to multiplayer.
- **Unreal replays bloat with high-bandwidth replication.** The
  `.replay` file under
  [`%LOCALAPPDATA%/<Project>/Saved/Demos`](https://dev.epicgames.com/documentation/en-us/unreal-engine/recording-replays-in-unreal-engine)
  grows with replicated-property volume - large open-world games
  produce GB-scale replays. Use checkpoint-only replays for
  long sessions.
- **Build-version coupling.** Replays recorded against build N
  rarely play correctly on build N+1 if the netcode / save
  format changed. Treat the replay file as a build-pinned
  artefact.
- **No public common exit-code definition** for replay-failed
  states in either Unity or Unreal - parse the test framework's
  result file (UTF NUnit XML or Unreal automation JSON) for the
  failure detail, don't rely on engine exit code.
- **No assertion API on Unreal `DemoNetDriver` replay completion**
  in public docs - the spec / latent-command harness must poll
  the demo time and time-out. See
  [Replays in Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/replays-in-unreal-engine).
- **PII in replays.** Player chat, gamertags (per Microsoft
  [XR-046](https://learn.microsoft.com/en-us/gaming/gdk/_content/gc/policies/console/certification-requirements)
  modern-gamertag display rules), and inventory data can land
  inside replay attachments - strip before sharing with
  cert / publisher.

## References

- Unity Input System `InputEventTrace` API -
  [com.unity.inputsystem@1.8](https://docs.unity3d.com/Packages/com.unity.inputsystem@1.8/api/UnityEngine.InputSystem.LowLevel.InputEventTrace.html).
- Replays in Unreal Engine -
  [dev.epicgames.com](https://dev.epicgames.com/documentation/en-us/unreal-engine/replays-in-unreal-engine);
  recording + storage in
  [Recording Replays](https://dev.epicgames.com/documentation/en-us/unreal-engine/recording-replays-in-unreal-engine),
  scrubbing in
  [Playing Back Replays](https://dev.epicgames.com/documentation/en-us/unreal-engine/playing-back-replays-in-unreal-engine).
- Godot documentation home (no first-party replay subsystem) -
  [docs.godotengine.org](https://docs.godotengine.org/en/stable/).
- Microsoft gamertag display / cert rules -
  [certification-requirements](https://learn.microsoft.com/en-us/gaming/gdk/_content/gc/policies/console/certification-requirements).
- Full per-engine record, replay, and CI-assertion code (with
  their citations):
  [references/engine-record-replay-apis.md](references/engine-record-replay-apis.md).
- Host test frameworks:
  `unity-test-framework`,
  `unreal-automation-system`,
  `godot-gut-tests`.
- Netcode neighbour:
  `multiplayer-state-machine-coverage`.
- Cert evidence:
  `platform-cert-overview-reference`.
