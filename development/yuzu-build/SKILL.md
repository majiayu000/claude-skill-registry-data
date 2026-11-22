---
name: yuzu-build
description: Configure, compile, and test Yuzu with the repo's canonical Meson entrypoints and per-OS build directories. Use when validating code changes, selecting test suites, reconfiguring a build directory, or recovering from host/builddir mismatches on Linux, macOS, or Windows.
---

# Yuzu Build

## Start Here

- Use `./scripts/setup.sh` unless the user explicitly wants raw `meson setup`.
- Use canonical build directories: `build-linux`, `build-windows`, and `build-macos`.
- Use `--tests` when the task needs `meson test`.
- If `scripts/setup.sh` reports that a build directory came from another host, re-run with `--wipe` or a different build directory instead of forcing reuse.

## Choose The Path

- On Linux, run `./scripts/setup.sh [--tests]` and then `meson compile -C build-linux`.
- On macOS, run `./scripts/setup.sh [--tests]` and then `meson compile -C build-macos`.
- On Windows, invoke `$yuzu-windows-msvc` first and then use `build-windows`.
- Meson resolves the gateway's Erlang/OTP (28.4 or later 28.x) at configure, for the gateway custom target and its tests; source `scripts/ensure-erlang.sh` only before running `rebar3` or `erl` by hand.

## Choose Tests

- Read `tests/meson.build` to map the change to a suite.
- Prefer targeted suites first: `agent`, `server`, `echo`, `proto`, and `docs`.
- Run `meson test -C <builddir> --suite <suite> --print-errorlogs`.
- Expand to broader coverage only when the change crosses multiple areas or the targeted suite fails unexpectedly.

## Invoke Sibling Skills

- Invoke `$yuzu-meson` for any `meson.build`, dependency, or source-list change.
- Invoke `$yuzu-proto` for any `.proto`, codegen, or gateway proto mirror change.
- Invoke `$yuzu-plugin-abi` for SDK or plugin boundary changes.
- Invoke `$yuzu-windows-msvc` for any Windows, MSVC, or vcpkg issue.

## Read On Demand

- `scripts/setup.sh`
- `tests/meson.build`
- `scripts/run-tests.sh`
- `docs/windows-build.md`
