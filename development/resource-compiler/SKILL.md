---
name: resource-compiler
description: Compile Source 2 addon resources with the game's Resource Compiler on Windows — resolve the game installation from the Steam registry, pick the right inputs, run the compiler, locate the compiled outputs and diagnose build failures. Covers Panorama XML/CSS and SVG, textures, materials, models, particles, sounds and sound events, the raw images, meshes and audio they are built from, the order to compile them in, and Hammer map build workflows. Does not package a VPK or publish Workshop items.
license: MIT
---

# Source 2 Resource Compiler

Compile the user's existing source assets with the Resource Compiler shipped in the target game's
Workshop Tools. Do not limit discovery to XML and CSS — the installed game and compiler determine
which resource types and build options exist.

## The pipeline

```
Steam registry  →  libraryfolders.vdf  →  appmanifest_<appId>.acf
                                                   │
                                                   ▼
                                          installation root
                                        ┌──────────┴──────────┐
                        content\<game>_addons\ADDON     game\bin\win64\resourcecompiler.exe
                                   main.css  ──────── -i ────────▶  game\<game>_addons\ADDON
                                   main.xml                              main.vcss_c
                                                                         main.vxml_c
```

Four phases, each with a way to be wrong:

| Phase | Reference | The mistake it prevents |
|---|---|---|
| Find the game | [installation.md](references/installation.md) | Hardcoding a drive letter, or writing into the wrong installation |
| Pick the inputs | [resources.md](references/resources.md) | Handing the compiler a `.png` that belongs to a material |
| Compile | [compile.md](references/compile.md) | Compiling `_c` outputs, skipping dependencies, losing the working directory |
| Verify | [compile.md](references/compile.md) | Calling a zero exit code proof that the resource was built |

## The short version

```powershell
& $compiler -i $sourcePath
```

Absolute input path, PowerShell's call operator, run from the compiler's own directory, exit code
checked after every file. The full loop with its guards is in
[compile.md](references/compile.md).

## Rules that hold everywhere

- **Resolve the installation, do not assume it.** A Steam library sits on any drive under any
  folder name; only the `steamapps\...` tail is fixed. See
  [installation.md](references/installation.md).
- **`content/` is sources, `game/` is output.** A `content/` path in the request names the source
  tree — it is not an instruction to put compiled files there.
- **Inputs are definitions, not raw assets.** Pass `.css`, `.xml`, `.vmat`, `.vmdl`, `.vtex`,
  `.vsnd` and friends. A `.png`, `.dmx`, `.wav` or `.mp3` is an ingredient named inside one of
  those, an existing `_c` file is a product and never an input, and renaming a raw file to a
  compiled extension produces nothing usable. See [resources.md](references/resources.md).
- **Respect the requested scope.** Compile the resources asked for. No recursive addon sweeps,
  forced rebuilds, lighting bakes or packaging flags unless the task calls for them.
- **Inspect before writing.** Read existing files, and applicable repository instructions, before
  creating or replacing anything.
- **A bare `-i` is not a map build.** A full Hammer `.vmap` build spans geometry, visibility,
  physics, lighting, navigation and packaging.
- **Report honestly.** Compilation succeeding is not runtime validation, not a complete map build,
  not VPK packaging, and not Workshop publication.

## When a run fails

Read the compiler's own diagnostic and change something — the input, the arguments, or your
understanding of the resource type — before running again. Retrying an unchanged command is never
the fix. The symptom-to-cause table is in
[compile.md](references/compile.md), *Diagnose failures*.

Two failures that look worse than they are: a `skipped` result can mean the output was already
up to date, and a trailing `Leaked KeyValues blocks: <n>` accompanies successful runs too.

## Files

| File | Contents |
|---|---|
| [installation.md](references/installation.md) | Steam registry lookup, library roots, app IDs, `content/` vs `game/`, per-game addon directories, the compiler binary |
| [resources.md](references/resources.md) | Definitions vs raw assets, a worked addon tree, the per-type table, what a definition file looks like, compile order, Panorama naming |
| [compile.md](references/compile.md) | The compile loop, choosing inputs, Hammer builds, verification, source-to-output names, failure diagnosis |
