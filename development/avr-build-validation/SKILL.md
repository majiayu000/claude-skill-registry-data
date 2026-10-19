---
name: avr-build-validation
description: Run reproducible metisa PlatformIO Nano and Mega builds and record toolchain, warnings, and memory usage.
---

# AVR Build Validation

## Use when

Firmware, PlatformIO dependencies, C++ helpers, or build configuration change for the supported AVR targets.

## Procedure

1. Read `AGENTS.md`, `docs/AI_WORKING_GUIDE.md`, and current target notes in `docs/mcu-port-project-workbook.md`.
2. Run `pio project config` if PlatformIO configuration changed.
3. Run `pio run -e nanoatmega328` and `pio run -e megaatmega2560`.
4. For a warning baseline, clean/build one environment at a time with `pio run -e <env> -t clean` followed by `pio run -e <env>`.
5. Record exact command, platform/framework/compiler versions, result, warnings, RAM, and flash. Distinguish clean from incremental builds.

## Constraints

- Build success is not electrical, motor-load, legal, or safety qualification.
- Do not flash a controller or attach motor power as part of this skill.
- Do not add local absolute library paths; dependencies belong in `platformio.ini`.
- Do not run the legacy feature matrix unless its required Linux/CMake/Arduino toolchain is present; do not delete or restore user files with Git commands.

## Done when

Both supported AVR build results are recorded, or each failure and its first actionable error is documented. Any unsupported target remains marked unsupported.