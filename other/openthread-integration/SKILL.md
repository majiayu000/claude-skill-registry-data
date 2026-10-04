---
name: openthread-integration
description: Use when integrating, porting, configuring, or debugging OpenThread, Thread networking, radio platform abstraction, border routers, commissioning, or low-power mesh behavior
---

# OpenThread Integration

## Overview

Use this skill to integrate OpenThread by separating radio platform abstraction, dataset/commissioning state, IPv6 stack behavior, and low-power role configuration. Thread failures often require evidence from radio events and network dataset, not only application logs.

## When To Use

Use this skill when:

- The user wants OpenThread or Thread mesh networking on an MCU.
- The issue involves radio platform APIs, joining, commissioning, dataset, leader/router/child roles, sleepy end devices, IPv6, CoAP, or border routers.
- The target uses an 802.15.4 radio or RCP/NCP architecture.

Do not use this skill for generic Wi-Fi MQTT/TCP problems.

## First Questions

Ask for:

- Chip/radio, OpenThread version, architecture: SoC, RCP, NCP, or RTOS integration.
- Role: commissioner, joiner, router, sleepy end device, border router, or test node.
- Dataset, channel, PAN ID, network key policy, and commissioning method.
- Radio/platform logs, CLI output, packet capture, or ot-ctl output.
- Power mode and polling interval if low power is involved.

## Integration Checklist

1. Prove platform radio hooks.
   TX, RX, energy scan, channel change, timing, and radio interrupts must work.

1. Confirm dataset.
   Network name, channel, PAN ID, extended PAN ID, mesh-local prefix, and keys must match.

1. Validate role transitions.
   Observe disabled, detached, child, router, leader, or joined states.

1. Check IPv6 paths.
   Verify mesh-local addresses, routes, neighbor table, and border router prefixes.

1. Tune low power carefully.
   Sleepy devices need poll period, timeout, parent behavior, and current measurements.

## Common Failures

- Radio driver timestamps or ACK handling wrong.
- Nodes have mismatched datasets.
- Joiner credentials or commissioner state mismatch.
- Border router advertises wrong prefix or route.
- Sleepy child misses messages due to poll timeout.

## Verification

Before claiming OpenThread works:

- State architecture, radio, role, dataset identifiers, and OpenThread version.
- Confirm attach/join state and role.
- Confirm ping/UDP/CoAP or CLI communication across the mesh.
- Confirm low-power polling behavior if relevant.
- Confirm credentials were not exposed in logs.

## Example

User:

```text
OpenThread 设备一直 detached。
```

Agent:

1. Asks for dataset, role, radio platform, logs, and commissioner/joiner method.
1. Checks radio TX/RX and dataset match before application code.
1. Verifies role transition and mesh-local ping.
