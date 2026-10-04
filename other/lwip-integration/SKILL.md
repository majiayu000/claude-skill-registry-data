---
name: lwip-integration
description: Use when integrating, porting, configuring, or debugging lwIP TCP/IP stack, netif drivers, memory pools, sys_arch, DHCP, TCP, UDP, or embedded networking issues
---

# lwIP Integration

## Overview

Use this skill to integrate lwIP by separating hardware Ethernet/Wi-Fi drivers, `netif` glue, memory pools, threading model, and protocol configuration. A successful port proves link, IP configuration, packet RX/TX, and resource stability under load.

## When To Use

Use this skill when:

- The user wants to add or debug lwIP on bare metal, FreeRTOS, RT-Thread, Zephyr, vendor SDKs, or custom network drivers.
- The issue involves `lwipopts.h`, `sys_arch`, `netif`, DHCP, TCP/UDP, pbufs, memory pools, packet loss, or hard faults in networking.
- The target uses Ethernet, Wi-Fi, PPP, SLIP, or a vendor network interface.

Do not use this skill when the physical link or board interface is not proven. Use `hardware-interface-debug` first for PHY, RMII/MII, clocks, or wiring issues. For FreeRTOS-native TCP/IP, use `freertos-plus-tcp-integration`. For MQTT over lwIP, use `mqtt-embedded-integration` after basic connectivity works.

## First Questions

Ask for:

- MCU/SoC, network interface, PHY/module, RTOS, and lwIP version.
- Driver source: vendor SDK, custom MAC driver, Wi-Fi module, or simulator.
- Threading model: NO_SYS raw API, tcpip_thread, socket/netconn API, or RTOS integration.
- `lwipopts.h`, memory sizes, pbuf pool settings, and enabled protocols.
- Current symptom: no link, no IP, DHCP timeout, ping fails, TCP stalls, memory exhaustion, or crash.
- Packet/log evidence: link status, IP address, ARP, ping, Wireshark, counters, or asserts.

## Integration Checklist

1. Confirm link before IP.
   Verify PHY/module link, MAC address, link callbacks, and carrier status before debugging DHCP or TCP.

1. Confirm `netif` glue.
   `netif_add`, input path, output path, MTU, flags, hostname, and link/status callbacks must match the driver.

1. Match threading model.
   Do not call raw API from arbitrary threads. Use tcpip callbacks or socket/netconn APIs according to configuration.

1. Size memory deliberately.
   Check `MEM_SIZE`, `MEMP_NUM_*`, `PBUF_POOL_SIZE`, TCP windows, mailbox sizes, and stack sizes.

1. Implement OS abstraction if needed.
   For RTOS ports, `sys_arch` must provide semaphores, mutexes, mailboxes, timeouts, and critical sections.

1. Verify with layered tests.
   Link, static IP, ARP, ping, UDP echo, TCP connect, sustained transfer, and reconnect.

## Common Failures

- DHCP fails because link callback never reports up.
- Ping fails because ARP output path or MAC address is wrong.
- TCP stalls because pbufs or mailboxes are exhausted.
- Random crashes from raw API calls outside tcpip_thread.
- Cache/DMA incoherency corrupts RX/TX buffers.
- Stack overflow in tcpip_thread or network driver task.

## Verification

Before claiming lwIP works:

- State interface, RTOS mode, API style, and IP configuration.
- Confirm link status, MAC address, IP address, gateway, and netmask.
- Confirm ping or UDP/TCP test with counters.
- Report memory pool usage or at least configured pool sizes.
- If DMA/cache is involved, state cache maintenance policy.

## Example

User:

```text
lwIP DHCP 一直拿不到 IP。
```

Agent:

1. Asks for PHY link status, `netif` setup, `lwipopts.h`, RTOS mode, and DHCP logs.
1. Confirms link callback and RX path before changing DHCP settings.
1. Tests static IP ping to separate driver/link problems from DHCP problems.
