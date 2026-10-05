---
name: easel
description: Use when invoking the top-level `easel` dispatcher to discover or run Easel sequence-analysis subcommands from the HMMER toolchain.
disable-model-invocation: true
user-invocable: true
---

# easel

Top-level front end for the Easel utility collection shipped with HMMER. The binary advertises a dispatcher-style interface where `easel -h` shows overall help, `easel <cmd> -h` shows command help, and `easel <cmd> ...` runs a specific subcommand.

## Quick Start

- **Command:** `easel <cmd> [args...]`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/easel`
- **Observed upstream identity:** `easel: little utilities for biological sequence analysis`

## When To Use This Tool

- Inspecting which Easel helper commands are available on the current machine
- Launching a specific Easel subcommand through the umbrella `easel` executable
- Working with HMMER-adjacent sequence/alignment helper utilities instead of calling lower-level binaries directly
- Verifying whether the local Easel install is runnable before building downstream workflows around it

## Common Patterns

```bash
# Show top-level help summary
easel -h
```

```bash
# Show version
easel --version
```

```bash
# Ask a specific Easel subcommand for help
easel <cmd> -h
```

## Recommended Workflow

1. Start with `easel -h` to confirm the dispatcher runs and to enumerate available subcommands.
2. Drill into a concrete helper with `easel <cmd> -h` before wiring it into a pipeline.
3. Only rely on the umbrella entry point after confirming the current environment can satisfy its shared-library dependencies.
4. If the dispatcher is broken locally, fall back to inspecting the environment and HMMER/Easel installation before assuming the subcommands themselves are missing.

## Guardrails

- In this workspace, `easel -h` and `easel --version` both fail immediately with `error while loading shared libraries: libopenblas.so.0`, so runtime verification is currently blocked by a missing OpenBLAS library.
- `readelf -d` shows the binary requires `libgsl.so.25`, `libopenblas.so.0`, and `libmpi.so.40`, with an rpath of `$ORIGIN/../lib`.
- The binary strings still expose the expected interface: `easel -h`, `easel --version`, `easel <cmd> -h`, and `easel <cmd> [<args>...]`.
- Treat this skill as a dispatcher-level reference, not as proof that any specific Easel subcommand is usable in the current environment.
