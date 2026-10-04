---
name: esp-idf-integration
description: Use when integrating, configuring, or debugging ESP-IDF projects, components, sdkconfig, partition tables, bootloader, NVS, Wi-Fi, BLE, FreeRTOS, flash, or peripherals
---

# ESP-IDF Integration

## Overview

Use this skill to debug ESP-IDF by separating project configuration,
components, partition table, bootloader, flash settings, FreeRTOS behavior, and
subsystem logs. ESP-IDF failures are often visible in `sdkconfig` or boot logs.

## When To Use

Use this skill when:

- The user is working with ESP-IDF, `idf.py`, ESP32-family SoCs, components, or
  managed components.
- The issue involves `sdkconfig`, partition tables, NVS, Wi-Fi, BLE, OTA, flash
  mode/size, bootloader logs, heap, tasks, or peripheral drivers.
- The project differs between menuconfig, CMake components, and runtime logs.

Do not use this skill for generic FreeRTOS kernel bugs with no ESP-IDF surface.
Use `freertos-kernel-debug` instead.

## First Questions

Ask for:

- ESP-IDF version, target chip, module/board, toolchain, and `idf.py` command.
- `sdkconfig`, partition table, component layout, and dependency manifest.
- Boot log from reset through app start, including flash mode/size and reset
  reason.
- Subsystem involved: Wi-Fi, BLE, NVS, OTA, filesystem, peripheral, or power.
- Current error code, log tag, panic dump, heap info, or task snapshot.

## Debug Workflow

1. Reproduce the build and target.
   Confirm `IDF_TARGET`, `idf.py set-target`, clean build, flash, and monitor.

1. Inspect boot evidence.
   Read reset reason, bootloader version, flash parameters, partition table, and
   app image selection.

1. Verify configuration.
   Check `sdkconfig`, Kconfig options, component dependencies, and CMake target
   ownership.

1. Prove storage and partitions.
   For NVS, OTA, SPIFFS, FAT, or custom data, confirm partition labels, sizes,
   erase state, and encryption settings.

1. Debug subsystem state.
   Use ESP-IDF logs, error names, event loops, heap tracing, and task snapshots.

1. Handle production constraints.
   Treat secure boot, flash encryption, eFuse state, and OTA rollback as
   one-way or high-risk changes.

## Common Failures

- Built for one `IDF_TARGET` and flashed to another chip.
- Partition table label or size does not match application assumptions.
- NVS is full, version-incompatible, encrypted unexpectedly, or not erased.
- Wi-Fi/BLE event handling is missing or races initialization.
- Flash mode/frequency is unstable for the module.
- Secure boot or flash encryption is enabled before the recovery path is proven.

## Verification

Before claiming ESP-IDF behavior works:

- State ESP-IDF version, target, build/flash command, and partition table.
- Confirm boot log, reset reason, flash settings, and app start.
- Confirm subsystem logs and return codes for the exercised path.
- Confirm erase/reflash, OTA, or security implications when relevant.

## Example

User:

```text
ESP32 OTA 后启动到旧固件。
```

Agent:

1. Reads bootloader log, partition table, selected app, and OTA state.
1. Checks image validation, rollback flags, and app confirmation.
1. Fixes OTA state handling before touching Wi-Fi download code.
