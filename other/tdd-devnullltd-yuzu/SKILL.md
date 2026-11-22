---
name: tdd
description: Apply Yuzu-specific test-driven development using tracer-bullet red-green-refactor cycles and the repo's Meson, gateway, proto, and ABI validation rules. Use when the user says `/tdd`, asks for TDD, red-green-refactor, or wants a feature/fix built test-first in Yuzu.
---

# TDD

Use behavior-first tests through public interfaces. Prefer integration-style seams that exercise real stores, REST handlers, gateway paths, plugin boundaries, or command dispatch contracts. Avoid tests coupled to private implementation.

## Before Red

- Read `CONTEXT.md` and relevant ADRs in `docs/adr/`.
- Identify the public interface and the project term for the behavior.
- List the smallest vertical behavior slice that proves value.
- Choose the narrowest validation path through `$yuzu-build`.
- Invoke `$yuzu-proto`, `$yuzu-plugin-abi`, `$yuzu-meson`, or `$yuzu-windows-msvc` if the slice crosses those boundaries.

## Cycle

1. Red: add one failing test for one observable behavior.
2. Green: implement only enough code to pass that test.
3. Verify: run the targeted suite with `meson test -C <builddir> --suite <suite> --print-errorlogs` or the relevant gateway command.
4. Repeat for the next behavior.
5. Refactor only while green.

Do not write all tests first. Use tracer bullets: one behavior, one test, one implementation.

## Yuzu Test Hygiene

- Use `yuzu::test::unique_temp_path(prefix)` or `TempDbFile` for C++ test temp files and SQLite DBs.
- Avoid hardcoded shared paths and clock/thread-hash uniqueness.
- For gateway EUnit, pass `--dir apps/yuzu_gw/test`.
- For direct Erlang isolation, remove the relevant `_build/test` tree or run in a fresh BEAM.
- For proto changes, include `buf lint proto` and `buf breaking proto --against '.git#subdir=proto,ref=origin/main'` when available.
- For plugin ABI changes, add descriptor/loader coverage and preserve stable C ABI compatibility.

## Done

Finish with the tests added, implementation green, targeted validation output summarized, and any broader `/test --quick` or governance follow-up called out.
