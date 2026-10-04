---
name: mcuboot-integration
description: Use when integrating, porting, configuring, or debugging MCUboot secure boot, image slots, swap modes, image signing, rollback, or bootloader upgrades on MCUs
---

# MCUboot Integration

## Overview

Use this skill to integrate MCUboot by proving the boot chain, flash map, image format, signing flow, and upgrade policy. Most failures come from slot geometry, trailer layout, or signing metadata mismatches rather than the application itself.

## When To Use

Use this skill when:

- The user wants to add MCUboot to Zephyr, Mynewt, NuttX, RIOT, Mbed OS, ESP-IDF, or a custom MCU platform.
- The issue involves image validation, swap, overwrite-only upgrade, rollback, confirm flags, serial recovery, or signed images.
- The project has dual slots, external flash, encrypted images, secure boot, or OTA requirements.

Do not use this skill for application-level firmware transfer alone. Use `ota-update-integration` first if the bootloader is already fixed and the issue is delivery. For generic bootloader jump/handoff debugging, use `bootloader-debug`.

## First Questions

Ask for:

- MCU/SoC, SDK/RTOS, boot flow, and current bootloader ownership.
- Flash layout: bootloader, primary slot, secondary slot, scratch, trailer, and external flash if used.
- Upgrade mode: swap, overwrite-only, direct-XIP, RAM-load, or serial recovery.
- Image signing method, key type, image version, and whether rollback prevention is needed.
- Current symptom and boot log from the bootloader.

## Integration Checklist

1. Freeze the flash map.
   Slot sizes, erase block size, alignment, scratch size, and trailer offsets must match the target flash.

1. Build a minimal signed image.
   Verify image header, TLVs, signature, version, and load address before enabling OTA.

1. Prove first boot.
   Boot one known-good image from the primary slot and record bootloader logs.

1. Prove upgrade behavior.
   Test pending, test, confirm, revert, and permanent upgrade paths for the selected mode.

1. Add recovery and brick protection.
   Keep serial recovery, debug access, watchdog policy, and factory image strategy clear.

1. Lock security policy last.
   Enable key protection, rollback counters, encryption, or anti-tamper only after the basic upgrade loop is repeatable.

## Common Failures

- Primary and secondary slots have different erase geometry or alignment.
- Signed image was built with the wrong header size, load address, or key.
- App never confirms the image, so MCUboot reverts on the next reset.
- Scratch area is too small for the largest erase sector.
- Bootloader and app disagree about vector table, stack pointer, or flash offset.
- Rollback protection is enabled before versioning and counter storage are proven.

## Verification

Before claiming MCUboot works:

- State flash layout, image mode, key type, and signing command.
- Confirm clean boot from primary slot.
- Confirm upgrade, confirm, and revert behavior with boot logs.
- Confirm recovery path and watchdog behavior during interrupted upgrade.

## Example

User:

```text
MCUboot 升级后总是回滚。
```

Agent:

1. Asks for flash layout, swap mode, signing command, image version, and boot log.
1. Checks whether the app calls image confirm after the self-test passes.
1. Verifies trailer flags and interrupted-upgrade behavior before changing OTA logic.
