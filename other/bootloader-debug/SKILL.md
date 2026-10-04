---
name: bootloader-debug
description: Use when debugging embedded bootloaders, application jumps, vector table offsets, firmware upgrade flow, OTA state, image validation, rollback, or boot selection failures
---

# Bootloader Debug

## Overview

Use this skill to debug bootloader and application handoff problems without destroying recovery paths. Verify memory layout, image metadata, vector table, stack pointer, reset handler, validation, and rollback state before reflashing or erasing boot regions.

## When To Use

Use this skill when:

- A bootloader cannot start an application or jumps to the wrong image.
- OTA/upgrade succeeds but the new firmware does not boot.
- The issue involves image headers, checksums, signatures, slots, rollback, vector table relocation, or boot pins.
- The user mentions MCUboot, U-Boot, vendor bootloader, IAP, DFU, app offset, or recovery mode.

Do not use this skill for ordinary application crashes after a confirmed clean handoff; use `embedded-fault-debug`. For MCUboot-specific slot/signing/swap issues, use `mcuboot-integration`. For OTA delivery pipeline issues, use `ota-update-integration`.

## First Questions

Ask for:

- Chip/board and bootloader type.
- Memory map: bootloader, app slot, scratch, config, NVM, and backup areas.
- Image format and validation: raw binary, HEX, signed image, checksum, metadata header.
- Upgrade state: active slot, pending, confirmed, rollback, recovery, or unknown.
- Logs from bootloader and application if available.
- Whether recovery access still works.

## Workflow

1. Protect recovery.
   Do not erase bootloader, recovery slot, calibration, or persistent upgrade state without explicit approval.

1. Confirm memory layout.
   Compare linker script, flash programming address, image header, and bootloader slot configuration.

1. Validate handoff basics.
   For MCU apps, check initial SP and reset handler at the application offset. For Linux boot, check kernel, device tree, rootfs, and bootargs.

1. Check image decision logic.
   Inspect version, checksum/signature, pending/confirmed flags, rollback counters, and slot priority.

1. Trace the jump.
   Halt before handoff, inspect target SP/PC, vector table relocation, interrupts, clocks, caches, and peripheral state.

1. Ask before destructive recovery.
   Erasing slots, clearing flags, disabling signature checks, or rewriting boot config requires approval.

## MCU Handoff Checks

- Application offset matches linker origin.
- Vector table word 0 is valid RAM stack pointer.
- Vector table word 1 is valid reset handler address.
- VTOR or equivalent vector relocation is set when required.
- Interrupts are disabled or cleaned up before jump.
- MSP/PSP is set correctly for the application.
- Caches, MPU, clock tree, and peripherals left by bootloader are expected by app.

## Upgrade And Rollback Checks

- Image header is at the offset the bootloader expects.
- Length, checksum, signature, and version fields match.
- Pending/confirmed flags reflect intended state.
- Rollback reason is logged before clearing it.
- Power-fail update path preserves at least one bootable image.

## Verification

Before claiming progress:

- State bootloader type, memory map, active slot, and application offset.
- Report whether image validation passed or which check failed.
- Report target SP/PC for app handoff when MCU-based.
- State whether recovery remains available.
- List destructive operations skipped or awaiting approval.

## Common Failures

- Flashing the app at flash base when the bootloader expects an offset.
- Forgetting vector table relocation.
- Clearing rollback flags before recording why rollback happened.
- Disabling validation to "test quickly" without preserving recovery.
- Leaving interrupts or peripherals active across app jump.

## Example

User:

```text
Bootloader 能跑，但跳 app 后死掉。
```

Agent:

1. Asks for memory map, app offset, linker script, boot log, and image header.
1. Checks app vector table SP/PC at the slot offset.
1. Verifies VTOR, interrupts, stack setup, and image validation before reflashing.
