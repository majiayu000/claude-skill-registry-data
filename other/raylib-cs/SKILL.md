---
name: raylib-cs
description: Use when building desktop games in C# with Raylib-cs (raylib bindings for .NET) — project setup, game loop, procedural 3D models with toon shading, fonts with full glyph coverage including Japanese, screenshot and stats modes, deterministic benchmarks with xUnit, and single-file publishing for Windows and Linux. Also use when text shows as "?", frame rate numbers look implausible, or the published build misses native libraries.
---

# Raylib-cs (C# desktop games)

Default: current LTS .NET, the `Raylib-cs` NuGet package, simulation in a plain class library tested with xUnit, the game as a thin executable, `dotnet publish` self-contained per platform.

## Project shape

```text
Game.Core/      rules, entities, save data — no Raylib references
Game/           Program.cs, rendering, input, audio
Game.Tests/     xUnit: rules, saves, deterministic bench thresholds
```

Command-line switches on the executable make it scriptable:

- `--stats` prints real frame-time statistics (mean and worst over 1 s windows).
- `--screenshot <scene>` renders one named scene to a PNG and exits — for README images and visual review.
- `--bench` runs the simulation headless across seeds and prints the measured outcomes.

## Rendering

- Build models from meshes generated in code (`GenMeshCube`, cylinders, custom meshes) grouped into parts; keep one material per part type.
- Toon shading with a small custom shader (quantised lighting) and an outline pass (inverted hull); outlines only for nearby objects.
- Draw a 2D HUD after 3D with `BeginMode3D`/`EndMode3D` closed; use rounded rectangles and a clear text hierarchy.

## Fonts and non-ASCII text

1. Collect every code point used by UI strings, data tables (part names, dialogue) and generated names at start-up.
2. Load the font with exactly that set (`LoadFontEx(path, size, codepoints, count)`).
3. Choose a font file whose `cmap` covers all of them; check coverage in a unit test and fail the build if any glyph is missing.
4. `.ttc` collections: extract one face to a standalone `.ttf` before loading, because many loaders read only single fonts.

Without this, every unsupported character renders as `?`.

## Performance numbers you can trust

- Measure with a monotonic clock over many frames; report mean and minimum fps or the 99th-percentile frame time.
- Do not trust a single fps readout or numbers from remote or virtualised displays; note the environment next to every figure.

## Publishing

```bash
dotnet publish Game -c Release -r win-x64 --self-contained -p:PublishSingleFile=true
dotnet publish Game -c Release -r linux-x64 --self-contained -p:PublishSingleFile=true
```

Check that the native raylib library for each runtime is in the output (or embedded), and run the published binary on a clean machine.

## Verification loop

1. `dotnet build` with warnings as errors; `dotnet test` including glyph coverage and bench thresholds.
2. Run `--screenshot` for key scenes and look at the images.
3. Run `--stats` on the target machine and record the numbers with the hardware.

## Pitfalls

- **Unloading:** textures, models, shaders and fonts must be unloaded explicitly; leaks grow GPU memory across scene changes.
- **Coordinate systems:** raylib is right-handed with Y up; mixing in data from tools with Z up flips models.
- **Struct copies:** many Raylib-cs types are structs; modifying a copy (e.g. a camera stored in a property) has no effect.
- **Save migration:** version save files and migrate step by step; test each old version fixture.
