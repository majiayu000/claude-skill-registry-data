---
name: yuzu-meson
description: Maintain Yuzu's Meson build graph, source lists, dependency wiring, and platform conditionals. Use when editing any `meson.build`, adding or removing source files, changing dependencies, updating native or cross files, or adjusting CI build behavior.
---

# Yuzu Meson

## Scope The Change

- Read root `meson.build` and every affected subdirectory `meson.build` before editing.
- Treat Meson as the only project build system. Do not add project `CMakeLists.txt` files.
- Treat `.github/workflows/ci.yml`, `scripts/setup.sh`, and `meson/native/*` or `meson/cross/*` as part of the same build contract when toolchain expectations change.

## Keep The Graph Correct

- Add every new `.cpp` file to the correct target.
- Remove or rename files in the same edit as the code move.
- Keep `build_agent`, `build_server`, `build_tests` gating intact. `build_examples` gates ONLY the four decorative demo plugins (`example`, `chargen`, `procfetch`, `netprobe`) — a new real plugin's `subdir()` call goes unconditionally under `if build_agent`, never inside the `build_examples` block.
- Preserve `include_type: 'system'` on third-party dependencies.
- Use existing `host_machine.system()` patterns for conditional sources and flags.

## Preserve Platform Rules

- Preserve the macOS framework pattern in root `meson.build` when transport or HTTP dependencies change.
- Treat the Windows protobuf and grpc branch in root `meson.build` as load-bearing. Invoke `$yuzu-windows-msvc` instead of simplifying it opportunistically.
- Keep `scripts/setup.sh` aligned with any change that alters canonical build directories, triplets, or reconfigure behavior.

## Validate

- Reconfigure with `./scripts/setup.sh` or `meson setup --reconfigure`.
- Compile the affected build directory.
- Run the narrowest relevant test suites after the compile is clean.

## Read On Demand

- `meson.build`
- affected `*/meson.build`
- `scripts/setup.sh`
- `.github/workflows/ci.yml`
- `meson/native/*`
- `meson/cross/*`
