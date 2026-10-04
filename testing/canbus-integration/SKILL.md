---
name: canbus-integration
description: Use when integrating, porting, configuring, or debugging CAN bus libraries, CANBus-Triple, MCP2515, CAN frames, bit timing, filters, or embedded automotive communication
---

# CANBus Integration

## Overview

Use this skill for embedded CAN bus libraries and CANBus-Triple style projects. CAN failures are often physical-layer, bit-timing, termination, transceiver, or filter problems before they are application protocol problems.

## When To Use

Use this skill when:

- The user mentions CAN, CANBus-Triple, MCP2515, SocketCAN, CANopen, J1939, UDS, OBD-II, ISO-TP, or automotive messages.
- Frames are missing, bus-off occurs, IDs are wrong, filters reject messages, or bit timing is unreliable.
- The task involves adapting a CAN example project or Arduino-style CAN platform to another board.

Do not use this skill when the target is only a generic UART/SPI issue with no CAN layer.

## First Questions

Ask for:

- CAN controller/transceiver and board, such as internal CAN, FDCAN, MCP2515, or CANBus-Triple.
- Bus speed, oscillator frequency, sample point, and whether CAN FD is involved.
- Wiring, termination, transceiver voltage, and whether another known-good node is present.
- Frame IDs, standard/extended format, filters, masks, and expected traffic.
- Library/project source and current error counters, bus state, or capture.

## Integration Checklist

1. Verify physical layer.
   Confirm CANH/CANL wiring, 120-ohm termination, common ground, transceiver enable/standby, and voltage compatibility.

1. Confirm bit timing.
   Controller clock, prescaler, segments, sample point, and bus speed must match the network.

1. Start with listen or loopback.
   Use internal loopback or listen-only mode before transmitting onto a live bus.

1. Configure filters deliberately.
   Disable filters temporarily or accept all frames to prove RX path before narrowing IDs.

1. Separate transport and protocol.
   First prove raw CAN frames, then add ISO-TP, UDS, OBD-II, J1939, or application decoding.

1. Protect live systems.
   Do not transmit on vehicle or production buses without explicit approval and a safe test plan.

## Common Failures

- Missing termination or wrong transceiver standby pin.
- MCP2515 oscillator frequency differs from library assumption.
- Standard versus extended ID mismatch.
- Filters silently drop expected frames.
- Bus-off caused by transmitting at wrong bit rate.
- SPI-to-CAN driver works in loopback but fails due to transceiver wiring.

## Verification

Before claiming CAN works:

- State controller, transceiver, bus speed, clock, ID format, and filter mode.
- Confirm physical termination and transceiver enable state.
- Confirm loopback or known-good RX before live TX.
- Report error counters, bus state, and captured frame evidence.
- State whether transmission on a live bus was skipped or explicitly approved.

## Example

User:

```text
CANBus-Triple 例程烧进去后收不到车上的 CAN 帧。
```

Agent:

1. Asks for bus speed, MCP2515 oscillator, termination, transceiver state, and expected IDs.
1. Tests listen-only or accept-all filters.
1. Confirms raw frames before decoding OBD-II or UDS traffic.
