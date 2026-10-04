---
name: ota-update-integration
description: Use when designing, integrating, testing, or debugging OTA firmware update flows, package formats, transport, rollback, versioning, or power-fail safety on embedded devices
---

# OTA Update Integration

## Overview

Use this skill to build OTA updates as a full pipeline: package creation, transport, staging, validation, activation, rollback, and observability. OTA is only reliable when every reset point is defined.

## When To Use

Use this skill when:

- The user wants firmware updates over HTTP, MQTT, BLE, LoRa, cellular, USB, SD card, or a custom protocol.
- The issue involves partial downloads, checksum failures, signature validation, resume, rollback, version checks, or update state machines.
- The target uses MCUboot, a vendor bootloader, A/B partitions, recovery mode, or external flash staging.

Do not use this skill for bootloader internals. Use `mcuboot-integration` when the image activation or swap logic itself is failing. For generic bootloader jump/handoff debugging, use `bootloader-debug`.

## First Questions

Ask for:

- Target device, RTOS/Linux stack, bootloader, flash layout, and update storage.
- Transport, package format, manifest fields, compression, encryption, and signing policy.
- Version policy, compatibility rules, rollback/factory reset behavior, and update trigger.
- Power-fail expectations and whether updates must resume after reset.
- Logs from download, validation, activation, and first boot.

## Integration Checklist

1. Define the update contract.
   The manifest should include target identity, version, size, hash, signature, compatibility, and install mode.

1. Separate download from activation.
   Store the image safely, verify it, then mark it pending only after all bytes and metadata are valid.

1. Make reset points explicit.
   Document what happens during download, after validation, after activation, and during first boot.

1. Verify authenticity and integrity.
   Use hash checks for corruption and signatures for trust. Do not treat transport TLS as a replacement for image signing.

1. Prove rollback.
   The device must recover from bad images, failed self-tests, power loss, and interrupted transfers.

1. Add operational visibility.
   Log update ID, version, byte count, validation result, boot decision, and final status.

## Common Failures

- Package metadata does not bind the image to the intended hardware or firmware family.
- Download success is treated as install success.
- The update state is stored in RAM or a non-atomic flash record.
- Power loss corrupts the staging slot or leaves ambiguous flags.
- Delta update logic has no full-image recovery path.
- TLS is enabled but image signatures and rollback policy are missing.

## Verification

Before claiming OTA works:

- State transport, package fields, bootloader policy, and flash layout.
- Confirm successful update and version transition.
- Confirm bad signature/hash rejection.
- Confirm power loss handling at download, validation, activation, and first boot.
- Confirm rollback or recovery path.

## Example

User:

```text
设备 OTA 偶尔升级后变砖。
```

Agent:

1. Maps each persistent OTA state and reset point.
1. Reproduces power loss during download, mark-pending, swap, and first boot.
1. Fixes atomic state storage or rollback policy before optimizing transfer speed.
