---
name: csharp
description: Use when building C# applications on modern .NET — command-line tools with System.CommandLine, desktop games with Raylib-cs, xUnit tests, self-contained single-file publishing for Windows and Linux, and save-file versioning. Also use when text renders as "?" boxes, when frame rates differ between machines, or when a published executable fails on another PC.
---

# C# on .NET

Default: the current LTS .NET SDK, nullable reference types on, warnings as errors, xUnit, `dotnet publish` self-contained.

## Setup

1. `dotnet new console -n App` and `dotnet new xunit -n App.Tests`; add both to a solution.
2. In the project file: `<Nullable>enable</Nullable>`, `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>`, `<ImplicitUsings>enable</ImplicitUsings>`.
3. Pin the SDK with `global.json` so CI and every machine build with the same compiler.
4. A machine without admin rights can install the SDK per user with the official `dotnet-install` script; put it on `PATH` only where it is used.

## Command-line tools

- Use `System.CommandLine` for parsing; it gives help, validation and tab completion.
- Keep the core logic in a library project and the CLI as a thin layer; test the library.
- Return non-zero exit codes on failure; write data to stdout and messages to stderr.

## Desktop games with Raylib-cs

- Separate the simulation (plain classes, deterministic, testable with xUnit) from drawing.
- Measure frame time with a real clock over a window (e.g. 1 s) and report mean and worst; a single fps number hides stutter. Add a `--stats` flag rather than guessing.
- Provide a headless mode (`--bench`, `--screenshot <scene>`) so balance and images can be produced without playing.
- Load fonts with the exact set of code points the UI uses (collect them from all string tables at start-up). Loading only ASCII makes every Japanese or accented character render as `?`.
- Font collections (`.ttc`) cannot be passed directly to loaders that expect a single font; extract the face you need first, then verify every required glyph exists in its `cmap`.

## Persistence

- Give save data a version number and migrate forward step by step (`v1 → v2 → v3`). Test each migration with a stored fixture of the old format.
- Write saves atomically (temp file + `File.Move(..., overwrite: true)`).

## Publishing

```bash
dotnet publish -c Release -r win-x64 --self-contained -p:PublishSingleFile=true
dotnet publish -c Release -r linux-x64 --self-contained -p:PublishSingleFile=true
```

- Self-contained avoids "install the runtime first" support issues; check the output size and keep it in the release notes.
- Native libraries (raylib) must be present for each runtime identifier; test the published binary on a clean machine or VM.

## Verification loop

1. `dotnet build` with zero warnings.
2. `dotnet test` — unit tests plus a deterministic benchmark (fixed seed → known outcome ranges).
3. Run the published binary, not `dotnet run`, before release.

## Pitfalls

- **Culture-sensitive formatting:** `double.Parse` and `ToString()` follow the OS locale. Use `CultureInfo.InvariantCulture` for files and protocols.
- **`async void`** swallows exceptions except in event handlers.
- **Floating-point determinism** differs across platforms and JIT settings; do not rely on bit-identical physics for replays across machines without fixed-point or careful ordering.
- **Disposing native resources:** textures, sounds and fonts from native libraries are not garbage-collected promptly; unload them explicitly.
- **WSL or remote desktops** may render through a software path; measure performance on the target hardware before tuning.
