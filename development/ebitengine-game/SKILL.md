---
name: ebitengine-game
description: >
  Create, improve, debug and package playable 2D games in Go with Ebitengine
  (github.com/hajimehoshi/ebiten/v2). Use for Ebitengine game requests: game design
  translated into a complete loop, input, rendering, text, audio, scenes, gameplay
  tests and desktop, browser or mobile builds. Also use when fixing these systems
  in an existing Ebitengine game. Do not apply to unrelated Go software or
  engine-internal patches merely because they depend on Ebitengine.
---

# Ebitengine game

Deliver a game that is understandable, responsive and complete at the requested
scope. One request can include several internal build/play/refine passes. A
scaffold, successful build or attractive screenshot alone is not a finished game.
For a focused fix, preserve the project's design and limit the workflow to the
affected behavior.

The bundled starter targets **Ebitengine v2.10.5 / Go 1.25+**. This is a pinned
baseline, not a claim about the latest release. Keep an existing project's
versions unless an upgrade is needed and authorized. Check the pinned version's
public API before using newer or experimental APIs. References contain patterns
to adapt; only the bundled scripts and starter are executable deliverables.
Their checks do not validate every reference snippet.

## Delivery workflow

1. **Inspect and decide.** Read repository instructions, `go.mod`, the `RunGame`
   entrypoint and existing tests/assets. For new games, read
   [Design and quality](references/design-and-quality.md). Establish the player's
   goal, repeated decision, consequence, end/retry path, intended look, platform
   and supported input. Infer reasonable defaults; ask only for missing choices
   that materially change the product. Record a short brief and observable
   acceptance criteria in the project.
2. **Build a representative playable slice.** Make the central interaction and
   its feedback work with the intended controls and visual direction. Check the
   feel before expanding content. Keep scope small enough to finish; choose
   authored or procedural content based on the game, not the template. Calibrate
   content against actual player capabilities before multiplying levels. For an
   art set, establish shared perspective, scale, anchors and palette roles using
   [Assets and animation](references/assets-and-animation.md).
3. **Complete and refine.** Implement the promised start → play → outcome →
   retry/continue loop (or the appropriate persistent/sandbox loop). Refine
   hierarchy, animation, sound, difficulty and transitions in context. Read only
   the technical references needed for the selected systems. Fix discovered
   defects within this delivery rather than asking the user to iterate for you.
4. **Verify the product.** Test rules and important transitions, exercise real
   input, inspect representative rendered states, and build/run requested
   targets. Include failure/retry and boundary cases. A scripted demo cannot
   establish control feel; a silent audio sink cannot establish sound quality.
   For automated multi-step interactions, pair observed images with actual state
   at the same tick; see [Playtest diagnostics](references/playtest-diagnostics.md).
5. **Hand off.** Supply launch/build instructions, actual artifact paths and
   asset licences. State what was run and observed, what remains unverified,
   and any material limitations. Publishing, purchases and external uploads are
   separate actions within the user's requested scope.

## Starting a project

Resolve commands relative to this skill's directory, not the game's working
directory. Set `skill_dir` to the actual installed location, then for example:

```sh
python3 "$skill_dir/scripts/new_game.py" --out mygame \
  --module example.com/mygame --title "My Game"
cd mygame
go mod tidy
go test ./world/...
```

The starter demonstrates scenes, action input, text, sound, a camera, pause and
scripted capture using a small **platformer**. It is an integration example,
not a genre or architecture requirement. Replace its rules, controls, level,
presentation and scene flow to fit the brief; a puzzle or card game should not
inherit gravity, jumping, camera scrolling or a platformer HUD. Existing projects
rarely need a scaffold. `--ci` adds a workflow and tools; inspect its triggers,
targets and release behavior before enabling it.

## Loop and resource contracts

| Method | Responsibility | Important distinction |
| --- | --- | --- |
| `Update() error` | Sample actions, advance simulation, apply scene changes and trigger event audio | Default target is 60 fixed ticks/s. Catch-up updates, focus pauses and slow machines affect actual scheduling. |
| `Draw(screen *ebiten.Image)` | Render the state produced by updates | Calls are not one-to-one with ticks. Do not advance gameplay, consume input edges or start sounds here. Renderer-owned caches are separate from simulation state. |
| `Layout(outsideW, outsideH int) (int, int)` | Choose logical dimensions for rendering and input | Fixed and responsive designs are both valid. Account for small windows, aspect ratio and readability. |

- Express simulation durations in ticks or use an explicit fixed `dt`. At 60
  TPS, 30 ticks is 0.5 seconds of simulation time. `ActualTPS` is a diagnostic,
  not a delta. `SetTPS` changes the whole update clock; it is not a universal
  slow-motion control. Avoid `SyncWithFPS` for rules that require a fixed step.
- Return `ebiten.Termination` from `Update` for a clean stop. Other errors return
  from `RunGame`; propagate failures rather than hiding them.
- Load/decode images and font sources once; reuse offscreens and hot-path
  slices. Profile before making pooling or zero-allocation rules universal.
- Separate rules from device/GPU code where that makes them testable. A small
  game need not grow an ECS, scene stack or service layer without need.

## Essential Ebitengine choices

- **Input:** Map devices to actions in `Update`. Separate held/pressed/released;
  combine bindings before computing an action edge if that is the intended
  behavior. Standard gamepad mappings need an availability check and stick dead
  zones. Verify the advertised devices through menus and retry too.
  [Input](references/input.md).
- **Rendering:** `GeoM` operations apply in call order. Pixel art needs deliberate
  sampling/scaling; smooth art needs suitable filtering and antialiased geometry.
  Preserve layer order while batching; sharing a sheet does not guarantee one
  command. Custom final-screen transforms need matching pointer conversion.
  [Rendering](references/rendering.md).
- **Text/UI:** Preserve suitable existing bitmap/atlas text rendering. For new
  outline-font code, use `text/v2` and parse font sources once. Include fonts
  covering the shipped scripts and their licences. Measure actual strings and
  verify focus, long text and target-size readability. [Text/UI](references/text-and-ui.md).
- **Audio:** One `audio.Context` per process. Match sample rate and PCM format:
  `DecodeF32` does not resample; `DecodeWithSampleRate` returns 16-bit PCM.
  Overlapping effects need independent players or a voice pool; bound concurrency
  for dense events. Resume browser audio after a gesture. [Audio](references/audio.md).
- **Systems:** Tweens, particles, shake, physics and map loaders are optional
  tools supporting the central interaction. [Gameplay systems](references/gameplay-systems.md).
- **State:** Queue external callbacks for `Update`, make reset/retry clear,
  separate gameplay and cosmetic randomness, test saves if persistence is
  promised. [Architecture/testing](references/architecture-and-testing.md).

## Verification

Run commands from the game directory; retain `go.mod` and `go.sum`. Use repository
build flags; `-buildvcs=false` below avoids depending on surrounding Git metadata.

```sh
go vet ./...
go test ./world/...   # starter's GPU-independent rules
python3 "$skill_dir/scripts/check_ebitengine.py" .
go build -buildvcs=false -o game .
```

Run the checker after changing loop/input/audio code or reviewing old APIs. It is
a read-only, text-based advisory scan: inspect warnings in context. `--json`
returns the shared checker schema; `--strict` fails on warnings and `--max-issues N`
limits the report without changing totals. Deprecated APIs are warnings, not
proof of a broken build. A clean result proves neither API correctness nor
quality. Run other relevant package tests too; on Linux, tests that initialize
graphics need `xvfb-run -a`.

The checker cannot infer Go receiver types. Ambiguous `.At()` calls in `Update`/`Draw`
are informational notes, not warnings: ordinary grid/map lookups are fine; verify
whether the receiver is actually an `ebiten.Image` before treating it as a GPU
readback. `ReadPixels()` remains a warning. Notes never fail `--strict`; JSON adds
`note_count` and `notes` to the shared schema. `--max-issues` caps warnings and notes
together, showing warnings first while retaining both totals.

For the starter, capture with `-demo -shot frame.png -shot-tick 240`. On Linux,
use a virtual display and, if needed, null audio without changing HOME:

```sh
audio_config=$(mktemp)
printf 'pcm.!default { type null }\n' > "$audio_config"
ALSA_CONFIG_PATH="$audio_config" xvfb-run -a ./game \
  -demo -shot frame.png -shot-tick 240
rm "$audio_config"
```

Open the PNG. Inspect more states as needed: first play, a busy/difficult moment,
failure and outcome. Adapt scripted actions/capture points after changing the
game; the template demo no longer proves anything about a different loop.
For deeper input/replay tests, v2.10's opt-in VM may help (see
[Architecture/testing](references/architecture-and-testing.md)).

Build only promised targets, for example:

```sh
GOOS=windows GOARCH=amd64 go build -buildvcs=false -o game.exe .
GOOS=js GOARCH=wasm go build -buildvcs=false -o game.wasm .
```

Cross-compilation establishes buildability, not runtime support. Run browser
builds over HTTP and inspect console/input/audio when they are a target. Native
SDKs, store bindings and cgo dependencies can add requirements beyond
Ebitengine's pure-Go desktop backend.

## Compose within this catalog

This skill owns Ebitengine/Go APIs. For portable design concerns, pair it with
the relevant installed discipline (for example `game-ui-ux`, `game-feel`,
`create-game-assets`, `input-systems`, `performance-optimization` or
`save-systems`), genre or shipping workflow. Bind the
engine slots to this skill's references, not another engine's example code.
Load only what the task needs; the complete folder also works on its own.

## Read as needed

- [Design and quality](references/design-and-quality.md): brief, genre choices,
  complete loop, presentation and playtest acceptance; for new games/redesigns.
- [Project and builds](references/project-and-builds.md): desktop, WASM and mobile.
- [Rendering](references/rendering.md), [input](references/input.md),
  [text/UI](references/text-and-ui.md), [audio](references/audio.md).
- [Assets and animation](references/assets-and-animation.md): when making or
  importing an art set; shared visual rules, scale, pivots and sprite-sheet QA.
- [Playtest diagnostics](references/playtest-diagnostics.md): when scripting
  interactions or reproducing failures; controlled ticks, state/image evidence.
- [Architecture/testing](references/architecture-and-testing.md) and
  [gameplay systems](references/gameplay-systems.md): state, saves, animation,
  collision and optional rigid bodies. [Tiled maps](references/tilemaps.md) covers
  a constrained loader only when the game uses Tiled.
- [Networking](references/networking.md): only for requested online play.
- [Publishing/platforms](references/publishing-and-platforms.md),
  [monetization](references/monetization.md), [CI/release](references/ci-and-release.md):
  only for requested distribution/integration work.

If available, Ebitengine's repository skills `writing-kage-shaders` and
`run-ebitengine-app-headless` provide version-specific advanced workflows. Other
game-design/store skills are optional supplements; this skill remains usable
without an external skill catalog.
