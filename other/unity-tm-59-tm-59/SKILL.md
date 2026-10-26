---
name: unity
description: Use when building or optimising Unity projects (Unity 6, URP) — batch-mode builds and tests from the command line, streaming large worlds and 3D tiles, asset bundles, shader warm-up, diagnosing stutter and GPU-bound frames with the Profiler and frame timing, loading screens, and WebGL or desktop builds. Also use when a scene hitches after loading, frame rate collapses in dense areas, or builds work in the Editor but not in the player.
---

# Unity

Default: a Unity LTS release with URP, one graphics API per target chosen explicitly, builds and tests run in batch mode from scripts, measurements recorded with the hardware they were taken on.

## Automate the Editor

- Build and test from the command line so agents and CI can run them:
  ```bash
  Unity -batchmode -quit -projectPath . -executeMethod Build.Player -logFile build.log
  Unity -batchmode -projectPath . -runTests -testPlatform PlayMode -testResults results.xml
  ```
- Write `Build.Player` as an Editor script that sets scenes, target and options explicitly.
- Keep a regression harness: launch the player with arguments (location, camera path, duration), record frame times and screenshots, and compare with a stored baseline.
- One build at a time: the Editor locks the project; use a lock file in your scripts.

## Large worlds

- Split terrain and props into tiles/chunks (a few hundred metres) and load by distance; one huge mesh is never culled and is drawn in every shadow pass.
- Do not let terrain or distant buildings cast shadows; cull far objects beyond a set distance.
- Generate heavy content (procedural buildings, props) on worker threads, then create meshes on the main thread in small batches per frame.
- Keep big data outside the build and load it at runtime, so the player starts even when the data is missing.

## Stutter after loading

Most hitches are uploads and compilation, not your scripts:

1. **Shader variants:** collect the variants actually used (a development build can log them), store them in a `ShaderVariantCollection`, and warm them up behind the loading screen (`WarmUpProgressively` spreads the cost). Measure before and after — if warm-up time is tiny, the stutter is elsewhere.
2. **Texture and mesh uploads:** large textures (4K–8K) uploaded on the first frame they are visible cause long frames. Cap texture size for streamed content (e.g. 1024 or 512 px), and limit how many tiles load concurrently.
3. **Keep the loading screen up** until required content is resident, render a few frames behind it, then fade.

Find the cause with the Profiler (look for `Gfx.WaitForGfxCommandsFromMainThread`, `Shader.CreateGPUProgram`, `GC.Alloc` spikes) and a frame-time log of the first seconds after load (max and p99, not just average fps).

## GPU-bound frames

- Check CPU vs GPU frame time (`FrameTimingManager`). If GPU-bound, remove work: fewer shadow casters, shorter draw distance, simpler distant materials, fewer transparent layers.
- Disable one subsystem at a time with debug switches and measure; this isolates the costliest part faster than guessing.

## Verification loop

1. Batch build succeeds with zero errors; Edit and Play Mode tests pass.
2. The regression harness: every location loads, the character lands on ground, frame-time stats are within the baseline tolerance.
3. Inspect the screenshots, not only the numbers.

## Pitfalls

- **Editor numbers ≠ player numbers;** measure in a development or release player.
- **Changing graphics APIs** changes shader compilation and performance; pick one per platform and test with it.
- **Asset bundle rebuilds** can change GUIDs in `.meta` files; review `.meta` diffs and revert accidental changes.
- **Coordinates far from the origin** lose float precision (jitter, shader noise); keep the world near the origin or rebase.
- **`Resources` folders** bloat builds; prefer addressables or bundles for large content.
