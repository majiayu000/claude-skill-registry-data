---
name: nix-eda-packaging
description: Use when packaging EDA or hardware toolchains in Nix (Yosys, OpenROAD, simulators, vendor tools) and hitting dlopen/plugin/runtime-path failures, or writing derivations and build phases for hardware tooling on aarch64-linux
---

# Nix EDA Packaging

## Overview

EDA tools are awkward Nix citizens: they dlopen plugins at runtime, expect data files at fixed paths, and ship as prebuilt binaries with bad assumptions about the filesystem. The temptation is to paper over each failure with a wrapper or a binary patch. The discipline is to fix the actual dependency so the package is honest about what it needs.

**Core principle:** Make the package's real dependencies explicit, don't disguise them. A `wrapProgram` that injects a path or a `patchelf` that rewrites an interpreter hides a missing dependency instead of declaring it, and it breaks the next person who builds on your package.

## When to Use

- Packaging Yosys, OpenROAD, a simulator, or a vendor EDA binary in Nix
- A tool fails at runtime to dlopen a plugin or find a shared library
- Writing derivations and build phases for hardware tooling
- Building/evaluating on aarch64-linux

## Don't Reach For The Hacks

These are the moves to avoid, and what they're hiding:

- **`wrapProgram` to inject `LD_LIBRARY_PATH` / plugin paths.** Hides a real missing runtime dependency. The library belongs in `buildInputs` and on the proper rpath, or the plugin belongs in a declared search path the program already honors.
- **`patchelf` to rewrite the interpreter or rpath by hand.** Hides a build that didn't link correctly. Fix the link, or for unbuildable prebuilt blobs use the proper mechanism (`autoPatchelfHook`) only as a last resort and only for genuinely closed binaries, not to dodge a dlopen issue in something you build from source.
- **`autoPatchelfHook` as a dlopen fix.** It patches `NEEDED` entries; it does not solve a runtime `dlopen("libfoo.so")` that searches a path you haven't set up. Reaching for it here means you're treating the wrong layer.

When a dlopen fails, find what the tool actually dlopens and at what path, then provide that path the way the tool expects (a real search path, a data dir, an env the program documents) rather than wrapping the binary.

## Build Phases: Strings, Not Shell-Var Helpers

When you need a custom build or install phase, write the phase as a build-phase string. Do not try to pass derivation outputs like `$out` through command-line-builder helpers (the `toCommandLineShellGNU`-style functions); `$out` is a shell variable that only exists at build time inside the phase, and threading it through a Nix-level argument builder produces the wrong thing.

```nix
# Right: $out is referenced inside the phase string, where it exists.
buildPhase = ''
  make PREFIX=$out -j$NIX_BUILD_CORES
'';

# Wrong: trying to bake $out into a CLI arg list at Nix eval time.
# $out is not defined then; the helper sees a literal or empty value.
```

## Platform Awareness

- The dev/build machine is aarch64-linux. Use that platform for `nix eval`/`nix build` and don't assume x86_64 in scripts or test invocations.
- If a tool genuinely lacks an aarch64 build, that is a real problem to solve (cross, emulation, or upstream fix), not something to mask.

## Red Flags

| Smell | Do instead |
|-------|------------|
| `wrapProgram --set LD_LIBRARY_PATH` to fix dlopen | Declare the dep; put the lib on rpath or the documented search path |
| Hand `patchelf` to fix a from-source build | Fix the link / buildInputs |
| `autoPatchelfHook` to solve a `dlopen` | Provide the runtime search path the tool expects |
| Threading `$out` through a CLI-arg helper | Reference `$out` inside the buildPhase string |
| Assuming x86_64 on the dev box | It's aarch64-linux |

## Midstall House Style

- No packaging hacks: no `wrapProgram`/`patchelf`/`autoPatchelfHook` to paper over dlopen issues. Fix the real dependency.
- Build phases use buildPhase strings; don't pass `$out` through `toCommandLineShellGNU`-style helpers.
- aarch64-linux is the dev platform. Write docs and comments in ASD-STE100 Simplified Technical English. No em dashes, no emoji.
