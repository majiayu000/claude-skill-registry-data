---
name: ymodem-xmodem-integration
description: Use when integrating, porting, configuring, or debugging XMODEM or YMODEM serial transfer, bootloader firmware update, CRC, packet timeout, or flash-write flows
---

# YMODEM XMODEM Integration

## Overview

Use this skill for serial file-transfer protocols in bootloaders or maintenance consoles. Separate transport reliability, packet parsing, CRC/checksum, flash layout, and update safety before writing firmware to flash.

## When To Use

Use this skill when:

- The user wants to add or debug XMODEM/YMODEM firmware update over UART, USB CDC, or shell.
- Transfers timeout, abort, fail CRC, write wrong file size, brick after update, or hang at `C`/NAK negotiation.
- The task involves bootloader app download, serial protocol state machines, packet size, CRC16, SOH/STX/EOT/CAN, or flash programming.

Do not use this skill for general serial logging. Use `embedded-serial-log-debug` first if RX/TX is unreliable.

## First Questions

Ask for:

- Protocol: XMODEM, XMODEM-CRC, XMODEM-1K, YMODEM, or YMODEM batch.
- Transport, baud, flow control, timeout, and terminal sender tool.
- Bootloader/application flash layout and maximum image size.
- CRC/checksum mode and packet size.
- Whether current firmware/recovery image must be preserved.
- Current transfer log or packet trace.

## Integration Checklist

1. Prove serial transport.
   Verify raw RX/TX at the target baud before protocol debugging.

1. Implement protocol states explicitly.
   Negotiation, header, data packets, ACK/NAK, EOT, CAN abort, retry limit, and timeout should be visible in logs.

1. Validate file metadata.
   For YMODEM, parse filename and size. Reject images larger than the allowed slot.

1. Write flash safely.
   Erase only the intended slot, program aligned chunks, verify CRC/hash, and preserve bootloader/recovery areas.

1. Commit update last.
   Mark the image bootable only after full transfer and verify succeed.

1. Test abort and power loss.
   Ensure failed transfers do not leave the product without a bootable image.

## Common Failures

- Sender uses checksum mode while receiver expects CRC mode.
- Packet sequence number or complement validation is skipped.
- 1K packets overflow a small receive buffer.
- Flash erase starts before image size and slot are validated.
- EOT handling completes before final flash sync/verify.
- Failed transfer marks a bad image as bootable.

## Verification

Before claiming transfer/update works:

- State protocol variant, sender tool, baud, packet size, timeout, and flash slot.
- Confirm successful transfer, CRC/hash, flash verify, and boot decision.
- Confirm oversize image rejection.
- Confirm cancel/timeout behavior.
- Confirm recovery path after interrupted transfer.

## Example

User:

```text
Bootloader 用 YMODEM 升级，传完后 app 起不来。
```

Agent:

1. Asks for protocol variant, sender tool, app offset, image size, CRC, and boot log.
1. Checks slot bounds and flash verify before app jump.
1. Confirms image is marked bootable only after full verify succeeds.
