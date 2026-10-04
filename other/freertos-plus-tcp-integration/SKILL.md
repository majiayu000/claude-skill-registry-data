---
name: freertos-plus-tcp-integration
description: Use when integrating, porting, configuring, or debugging FreeRTOS+TCP networking, network interface drivers, buffer management, DHCP, sockets, or embedded TCP/IP issues
---

# FreeRTOS+TCP Integration

## Overview

Use this skill to integrate FreeRTOS+TCP by proving the network interface driver, buffer management, IP task, and socket behavior separately. Most failures come from driver callbacks, buffer ownership, or task priority/stack sizing.

## When To Use

Use this skill when:

- The user wants FreeRTOS+TCP on an MCU.
- The issue involves network interface porting, DHCP, ARP, sockets, buffer descriptors, IP task, DNS, or TCP/UDP stalls.
- The project uses FreeRTOS tasks and FreeRTOS+TCP APIs instead of lwIP.

Do not use this skill for lwIP projects. Use `lwip-integration` instead.

## First Questions

Ask for:

- MCU/SoC, PHY/module, MAC driver, FreeRTOS version, and FreeRTOS+TCP version.
- Network interface source and buffer allocation scheme.
- Static IP/DHCP config, MAC address, gateway, DNS, and hostname.
- IP task priority/stack, driver task/ISR model, and heap size.
- Current symptom and network logs/counters.

## Integration Checklist

1. Prove link and MAC.
   Confirm PHY link, MAC address, RX/TX interrupts, and descriptor rings.

1. Configure buffer management.
   Choose and size network buffers intentionally; track leaks and ownership.

1. Verify IP task health.
   IP task stack, priority, event queue, and timer behavior must be stable.

1. Test layers.
   Link, ARP, ping, UDP, TCP connect, DNS, DHCP, and reconnect separately.

1. Check thread rules.
   Use FreeRTOS+TCP APIs from valid task contexts and avoid unsafe ISR use.

## Common Failures

- Network buffers leak after RX error paths.
- IP task stack is too small.
- MAC DMA cache maintenance is missing.
- DHCP fails because link state is not reported correctly.
- Socket timeouts are treated as fatal connection state.

## Verification

Before claiming FreeRTOS+TCP works:

- State driver, buffer scheme, IP config, IP task priority/stack, and heap.
- Confirm link, IP address, ping, UDP/TCP test, and reconnect behavior.
- Report buffer usage/leak evidence if available.
- Confirm cache/DMA handling when relevant.

## Example

User:

```text
FreeRTOS+TCP DHCP 成功但 TCP 连接会卡死。
```

Agent:

1. Asks for socket code, IP task stack, buffer scheme, driver logs, and heap stats.
1. Checks buffer ownership and IP task health before protocol logic.
1. Verifies UDP and TCP separately.
