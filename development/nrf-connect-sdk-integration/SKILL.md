---
name: nrf-connect-sdk-integration
description: Use when integrating, configuring, or debugging Nordic nRF Connect SDK, Zephyr-based nRF projects, BLE, SoftDevice Controller, Partition Manager, DFU, or nRF drivers
---

# nRF Connect SDK Integration

## Overview

Use this skill to debug nRF Connect SDK by combining Zephyr evidence with
Nordic-specific layers: board files, Partition Manager, Bluetooth controller,
DFU, security, and nrfx drivers. NCS issues often span multiple generated files.

## When To Use

Use this skill when:

- The user is working with nRF Connect SDK, nRF52/nRF53/nRF54/nRF91, VS Code
  extension, `west`, or Zephyr-based Nordic samples.
- The issue involves BLE, SoftDevice Controller, MCUboot, DFU, Partition
  Manager, TF-M, modem, nrfx, or board overlays.
- The app behavior depends on generated partitions, child images, or multi-core
  images such as network core firmware.

Do not use this skill for Zephyr-only boards with no Nordic-specific stack. Use
`zephyr-integration` instead.

## First Questions

Ask for:

- NCS version, Zephyr revision, SoC, board, sample/app, and build command.
- `prj.conf`, overlays, Partition Manager output, child images, and sysbuild use.
- Bluetooth role, controller settings, security/pairing, and connection logs.
- DFU/MCUboot setup, image slots, signing, and boot logs if update-related.
- Current build error, runtime log, fault dump, or radio behavior.

## Debug Workflow

1. Freeze SDK and build shape.
   Confirm NCS version, board target, sysbuild, child images, and pristine build.

1. Inspect generated files.
   Check `.config`, `zephyr.dts`, Partition Manager output, and image manifests.

1. Prove board and driver config.
   Verify pins, clocks, regulators, nrfx drivers, and Nordic-specific Kconfig.

1. Debug BLE by layer.
   Separate host APIs, controller config, advertising, connection parameters,
   security, GATT, and radio coexistence.

1. Debug DFU by image chain.
   Check MCUboot, signing, slot layout, image confirmation, and rollback state.

1. Handle multi-core devices explicitly.
   For nRF53/nRF54, verify network core image, IPC, and core-specific logs.

## Common Failures

- Partition Manager output differs from the assumed flash layout.
- Child image config overrides the parent app's assumptions.
- BLE controller options do not match role, PHY, or connection count.
- Network core firmware is missing or built from stale configuration.
- DFU image is signed correctly but not confirmed after first boot.
- TF-M or secure partition settings are changed without matching memory layout.

## Verification

Before claiming NCS integration works:

- State NCS version, board, build mode, and generated partition layout.
- Confirm `.config`, `zephyr.dts`, and child image evidence.
- Confirm BLE/DFU/modem logs for the exercised path.
- Confirm multi-core image status when using nRF53/nRF54 class devices.

## Example

User:

```text
nRF5340 BLE 广播不出来。
```

Agent:

1. Checks NCS version, board target, child images, and network core firmware.
1. Verifies Bluetooth host/controller config and generated logs.
1. Tests a Nordic sample before changing application GATT code.
