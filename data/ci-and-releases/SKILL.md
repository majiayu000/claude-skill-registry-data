---
name: ci-and-releases
description: A lightweight checklist for CI, toolchain bumps, and version/release hygiene for the ComputationalPaths Lean 4 project (Lake + lean-action CI).
---

# CI & Releases

This skill provides a repeatable checklist for keeping the repo green on CI and preparing small “release-like” changes (toolchain bump, version bump, dependency updates).

## CI mental model

CI is essentially “clean checkout + `lake build`”. Keep changes compatible with:
- current toolchain in `lean-toolchain`
- dependencies pinned by `lake-manifest.json`
- the project’s “zero-warning” expectations (treat warnings as failures to fix immediately)

## Local verification (Windows)

From the Lean project root (`computational_paths/`):

```powershell
.\lake.cmd build
.\lake.cmd exe computational_paths
```

If you suspect stale artifacts:

```powershell
.\lake.cmd clean
.\lake.cmd build
```

## Version bump checklist

This repo exposes a version string:
- `ComputationalPaths/Basic.lean` defines `libraryVersion`
- `Main.lean` prints it via the executable

When bumping version:
1. Update `ComputationalPaths/Basic.lean` (`libraryVersion`)
2. Run `.\lake.cmd build`
3. Run `.\lake.cmd exe computational_paths` and confirm the output
4. If the bump is user-visible, update `README.md` (or add a short changelog note)

## Toolchain bump checklist

When updating `lean-toolchain`:
1. Edit `lean-toolchain`
2. Run `.\lake.cmd build`
3. If dependencies need repinning, run `lake update` and re-build
4. Ensure CI config still matches expectations (`.github/workflows/*`)

## Dependency update checklist

If updating deps (manifest changes):
1. Run `lake update`
2. Build (`.\lake.cmd build`)
3. Fix any breakage by updating imports/lemmas or pinning versions back as needed

