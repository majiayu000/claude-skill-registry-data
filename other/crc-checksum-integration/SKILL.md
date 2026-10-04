---
name: crc-checksum-integration
description: Use when implementing, verifying, or debugging CRC, checksum, hash-lite integrity checks, polynomial parameters, endian handling, or protocol frame validation in embedded systems
---

# CRC Checksum Integration

## Overview

Use this skill to integrate CRCs and checksums by making the exact algorithm parameters explicit. Most CRC bugs come from two sides using the same name for different init, reflection, xorout, byte order, or covered range.

## When To Use

Use this skill when:

- The user needs CRC-8, CRC-16, CRC-32, additive checksum, Fletcher, Adler, or protocol frame validation.
- The issue involves mismatched CRC values, boot image validation, Modbus, CAN, UART packets, storage records, or OTA packages.
- The target uses hardware CRC units, DMA, endian-sensitive protocols, or streaming updates.

Do not use this skill for cryptographic authentication. Use `mbedtls-integration`, `tinycrypt-integration`, or `micro-ecc-integration` when adversarial tampering matters.

## First Questions

Ask for:

- Algorithm name plus polynomial, width, init, refin, refout, xorout, and check value if known.
- Exact byte range covered, header/trailer inclusion, padding, and endian order.
- Whether the implementation is table-driven, bitwise, hardware accelerated, or streaming.
- Known-good sample input and expected output from the peer device or specification.
- Current mismatch and where it is observed.

## Integration Checklist

1. Write the full CRC tuple.
   Do not rely on names like CRC-16 unless the parameters are specified.

1. Verify with a golden vector.
   Test `123456789` or a protocol-provided frame before using live data.

1. Freeze byte coverage.
   Define start offset, length, skipped fields, padding, escaping, and final byte order.

1. Match streaming behavior.
   The incremental API must preserve state exactly across chunks and resets.

1. Compare hardware and software.
   Hardware CRC units often need byte reversal, word packing, or final xor handling.

1. Add negative tests.
   Flip one bit in payload and metadata to prove the check actually fails.

## Common Failures

- Wrong reflection settings for the named CRC variant.
- Including the CRC field itself in the covered range.
- Feeding words into a hardware CRC in host endian instead of wire order.
- Using a checksum where collision resistance or authenticity is required.
- Resetting incremental CRC state between chunks.
- Comparing printed hex values with opposite byte order.

## Verification

Before claiming the integrity check works:

- State the full CRC/checksum parameters and covered byte range.
- Confirm golden vector output.
- Confirm peer frame or stored-image sample matches.
- Confirm corrupted data is rejected.
- Confirm hardware and software paths match if both exist.

## Example

User:

```text
Modbus CRC 算出来总和设备不一样。
```

Agent:

1. Checks CRC-16/Modbus parameters, byte coverage, and low-byte-first output.
1. Runs a known Modbus frame golden vector.
1. Verifies the serial frame excludes the CRC field while computing.
