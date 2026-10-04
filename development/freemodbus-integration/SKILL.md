---
name: freemodbus-integration
description: Use when integrating, porting, configuring, or debugging FreeModbus RTU, ASCII, TCP, serial ports, timers, events, register callbacks, or Modbus protocol issues
---

# FreeModbus Integration

## Overview

Use this skill to integrate FreeModbus by proving the port layer first: serial/TCP transport, timing, event dispatch, and register callbacks. Modbus bugs are often timing, endian, addressing, or task-context problems rather than protocol logic.

## When To Use

Use this skill when:

- The user wants to add or debug FreeModbus RTU, ASCII, or TCP.
- The issue involves `portserial.c`, `porttimer.c`, `portevent.c`, register callbacks, CRC errors, timeouts, slave ID, function codes, or Modbus TCP/lwIP integration.
- A device does not respond, responds with exception codes, or has wrong register values.

Do not use this skill when the UART or network transport is not verified. Use serial or lwIP skills first if the lower layer is unknown.

## First Questions

Ask for:

- Mode: RTU, ASCII, TCP, master, slave, or gateway.
- MCU/RTOS/compiler and FreeModbus fork/version.
- Transport: UART/RS-485, TCP/lwIP, or custom.
- Baud, parity, stop bits, DE/RE control, slave ID, and timeout settings.
- Register map and callback code.
- Logic analyzer, serial capture, Modbus poll output, or exception codes.

## Integration Checklist

1. Prove transport timing.
   For RTU, verify baud, parity, stop bits, inter-frame gap, and RS-485 direction control.

1. Implement port files.
   Serial, timer, and event callbacks must match the target scheduler and ISR rules.

1. Confirm protocol mode.
   RTU, ASCII, and TCP have different framing, timing, and porting requirements.

1. Validate register callbacks.
   Holding/input/coils/discrete callbacks must map Modbus addresses to internal storage correctly.

1. Check address and endian assumptions.
   Modbus register numbering, zero-based offsets, word order, and byte order must be explicit.

1. Test one function at a time.
   Start with a simple read holding register before adding writes, coils, or TCP gateway logic.

## Common Failures

- RS-485 transmit enable timing cuts off the last byte.
- Timer tick is wrong, breaking RTU frame gap detection.
- Register addresses are off by one.
- Callback returns the wrong exception code or byte count.
- Modbus TCP works but RTU fails due to serial timing.
- Event handling blocks inside ISR or wrong task context.

## Verification

Before claiming FreeModbus works:

- State mode, role, slave ID, baud/network settings, and register map.
- Confirm one read and one write if writes are in scope.
- Confirm CRC or TCP framing is valid using capture/tool evidence.
- Confirm timeout and exception behavior.
- State RS-485 direction control and timer source when RTU is used.

## Example

User:

```text
FreeModbus RTU 能收到包但主站一直超时。
```

Agent:

1. Asks for UART settings, RS-485 DE/RE control, timer port, slave ID, and bus capture.
1. Checks frame gap timer and direction timing before register callbacks.
1. Verifies a single read holding register with known data.
