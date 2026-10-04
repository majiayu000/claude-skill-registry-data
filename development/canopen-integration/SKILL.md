---
name: canopen-integration
description: Use when integrating, configuring, or debugging CANopen nodes, object dictionaries, NMT, SDO, PDO, heartbeat, SYNC, EMCY, EDS/DCF files, or CANopenNode-style stacks
---

# CANopen Integration

## Overview

Use this skill to debug CANopen by separating raw CAN bring-up, node identity,
object dictionary, NMT state, SDO configuration, PDO mapping, heartbeat, and
application semantics. CANopen cannot work reliably until raw CAN timing works.

## When To Use

Use this skill when:

- The user is adding or debugging CANopen master/slave nodes, object
  dictionaries, EDS/DCF files, PDOs, SDOs, NMT, heartbeat, SYNC, or EMCY.
- The issue involves missing PDOs, SDO aborts, node state, heartbeat timeout,
  wrong COB-IDs, mapping errors, or network management.
- The implementation uses CANopenNode, a vendor stack, or a custom CANopen layer.

Do not use this skill for low-level CAN bit timing or transceiver bring-up. Use
`canbus-integration` first when raw CAN frames are not proven.

## First Questions

Ask for:

- CANopen stack, node ID, bitrate, raw CAN evidence, and network topology.
- Object dictionary entries, EDS/DCF, PDO mapping, COB-IDs, and NMT state.
- Master tool or peer node, SDO abort codes, heartbeat settings, and logs.
- Whether SYNC, TIME, EMCY, LSS, or boot-up messages are required.
- Exact frame capture from a CAN analyzer if available.

## Debug Workflow

1. Prove raw CAN.
   Confirm bitrate, sample point, transceiver, termination, and error counters.

1. Prove node identity.
   Check node ID, boot-up message, NMT state, heartbeat producer/consumer, and
   expected COB-IDs.

1. Validate object dictionary.
   Confirm index/subindex types, access rights, defaults, persistence, and
   application backing storage.

1. Debug SDO first.
   Use SDO reads/writes to verify OD entries before enabling PDO mapping.

1. Debug PDO mapping.
   Check mapping parameters, transmission type, inhibit/event timers, SYNC, and
   payload length.

1. Add safety behavior.
   Handle heartbeat loss, EMCY, bus-off recovery, and safe outputs explicitly.

## Common Failures

- Raw CAN works only at another bitrate or with missing termination.
- Node ID conflicts with another node or creates unexpected COB-IDs.
- OD type/access flags do not match the master expectation.
- PDO mapping is changed while the PDO is enabled.
- Heartbeat consumer timeout is shorter than realistic bus or boot timing.
- Application updates OD values without atomicity or endian consistency.

## Verification

Before claiming CANopen works:

- State bitrate, node ID, stack, NMT state, and object dictionary source.
- Confirm boot-up, heartbeat, and SDO read/write of key OD entries.
- Confirm PDO mapping and timing with a CAN trace.
- Confirm heartbeat timeout, EMCY, or bus-off behavior if safety-related.

## Example

User:

```text
CANopen 主站读 SDO 返回 abort。
```

Agent:

1. Captures the abort code, index/subindex, node ID, and COB-ID.
1. Checks OD type, access rights, and backing variable.
1. Verifies raw CAN and NMT state before changing application logic.
