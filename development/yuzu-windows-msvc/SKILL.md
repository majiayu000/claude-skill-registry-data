---
name: yuzu-windows-msvc
description: "Use the supported Yuzu Windows workflow: MSYS2 bash plus MSVC plus vcpkg. Use when handling Windows builds, `setup_msvc_env.sh`, `triplets/x64-windows.cmake`, Windows CI, or the Windows-specific protobuf and grpc linkage in root `meson.build`."
---

# Yuzu Windows MSVC

## Use The Supported Workflow

- Start in MSYS2 bash.
- Run `source ./setup_msvc_env.sh`.
- Meson resolves the gateway's Erlang/OTP itself; run `source scripts/ensure-erlang.sh` only before running `rebar3` or `erl` by hand.
- Use `build-windows` for local builds.
- Use `./scripts/setup.sh [--tests]` before `meson compile -C build-windows` unless the build directory already exists and only needs a reconfigure.

## Never Do These

- Do not use `vcvars64.bat`.
- Do not use Clang or `C:\Program Files\LLVM\bin`.
- Do not reuse Linux or WSL build directories for native Windows work.
- Do not replace the Windows protobuf and grpc wiring with Meson's `dependency(..., method: 'cmake')` path.

## Treat These Files As Load-Bearing

- `setup_msvc_env.sh`
- `docs/windows-build.md`
- root `meson.build`
- `triplets/x64-windows.cmake`
- `.github/workflows/ci.yml`

## Diagnose By Layer

- Toolchain missing: inspect the verification output from `setup_msvc_env.sh`.
- Debug versus release link mismatch: inspect `vcpkg_installed/x64-windows/lib` versus `vcpkg_installed/x64-windows/debug/lib`.
- CI-only failure: compare against the Windows workflow's `build-windows-ci` configure flags and PATH setup.
- Gateway failure: distinguish a hex.pm fetch flake from a Yuzu code failure before changing source.

## Validate

- Configure and compile `build-windows`.
- Run narrow Windows-relevant test suites first.
- If the task is CI-related, mirror `build-windows-ci` settings from `.github/workflows/ci.yml` before drawing conclusions.

## Invoke Sibling Skills

- Invoke `$yuzu-meson` for Meson graph edits.
- Invoke `$yuzu-build` for validation flow and suite selection.

## Read On Demand

- `docs/windows-build.md`
- `setup_msvc_env.sh`
- `meson.build`
- `triplets/x64-windows.cmake`
- `.github/workflows/ci.yml`
