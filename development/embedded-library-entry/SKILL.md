---
name: embedded-library-entry
description: Use when integrating, porting, configuring, or debugging third-party MCU embedded C libraries in bare-metal or RTOS projects
---

# Embedded Library Entry

## Overview

Use this skill as the entry point for MCU library integration work. Classify the library type, target platform, runtime model, resource limits, and required porting layer before routing to a specific library skill.

## When To Use

Use this skill when:

- The user wants to add, port, configure, or debug an embedded C library.
- The task involves MCU storage, logging, crash diagnosis, shell commands, filesystems, protocol stacks, UI, parsers, buttons, timers, queues, or state machines.
- The target may be bare metal, RTOS-based, or resource-constrained.

Do not use this skill when the problem is only board bring-up, flashing, serial logs, or architecture faults. Use the embedded debug skills first.

## First Questions

Ask only what is needed to route:

- Library name and version or source repository.
- Target MCU/SoC, compiler, and build system.
- Runtime model: bare metal, FreeRTOS, RT-Thread, Zephyr, Linux, or unknown.
- Memory/storage resources: RAM, flash, block device, filesystem, heap, stack, and whether dynamic allocation is allowed.
- Existing porting layer: file I/O, flash driver, UART, timebase, mutex, malloc, display, network, or shell transport.
- Current task: first integration, compile error, link error, runtime failure, performance issue, or data corruption.

## Routing Guide

**Storage & Filesystem**

| Library or task | Prefer |
| --- | --- |
| littlefs filesystem or block device | `littlefs-integration` |
| FatFs disk I/O, FAT/exFAT | `fatfs-integration` |
| FlashDB KV/time-series database | `flashdb-integration` |

**Logging & Diagnosis**

| Library or task | Prefer |
| --- | --- |
| EasyLogger output, filters, async logs | `easylogger-integration` |
| CmBacktrace Cortex-M crash backtrace | `cmbacktrace-integration` |
| SEGGER RTT logs, control block, J-Link I/O | `segger-rtt-integration` |

**Shell & CLI**

| Library or task | Prefer |
| --- | --- |
| letter-shell command shell | `letter-shell-integration` |
| nr_micro_shell tiny CLI | `nr-micro-shell-integration` |
| zoom-shell embedded console | `zoom-shell-integration` |

**Networking & Protocols**

| Library or task | Prefer |
| --- | --- |
| lwIP netif, DHCP, TCP, UDP | `lwip-integration` |
| FreeRTOS+TCP network driver, sockets | `freertos-plus-tcp-integration` |
| MQTT client, keepalive, QoS, TLS | `mqtt-embedded-integration` |
| FreeModbus RTU, ASCII, TCP | `freemodbus-integration` |
| OpenThread radio, mesh, commissioning | `openthread-integration` |
| CAN bus library, MCP2515, bit timing | `canbus-integration` |
| CANopen OD, NMT, SDO, PDO, heartbeat | `canopen-integration` |
| BLE GATT services, characteristics, MTU | `ble-gatt-integration` |

**UI & Display**

| Library or task | Prefer |
| --- | --- |
| LVGL display, input, tick, draw buffers | `lvgl-integration` |
| U8g2 monochrome display, fonts | `u8g2-integration` |
| E-paper EPD, busy timing, refresh modes | `epd-integration` |
| TJpgDec embedded JPEG decoding | `tjpgd-integration` |

**Security & Crypto**

| Library or task | Prefer |
| --- | --- |
| mbedTLS entropy, certificates, TLS handshake | `mbedtls-integration` |
| micro-ecc ECDH, ECDSA, keys, signatures | `micro-ecc-integration` |
| TinyCrypt AES, SHA, HMAC, ECC | `tinycrypt-integration` |

**Data & Serialization**

| Library or task | Prefer |
| --- | --- |
| cJSON, jsmn, inih parsers | `embedded-data-parsing-libs` |
| nanopb Protocol Buffers | `nanopb-integration` |
| CRC, checksum, integrity checks | `crc-checksum-integration` |

**USB & Transfer**

| Library or task | Prefer |
| --- | --- |
| TinyUSB device, host, CDC, MSC, HID | `tinyusb-integration` |
| XMODEM/YMODEM serial transfer, bootloader | `ymodem-xmodem-integration` |

**Boot & OTA**

| Library or task | Prefer |
| --- | --- |
| MCUboot secure boot, slots, signing | `mcuboot-integration` |
| OTA package, transport, rollback | `ota-update-integration` |

**Compression**

| Library or task | Prefer |
| --- | --- |
| miniz DEFLATE, zlib, ZIP | `miniz-integration` |
| heatshrink streaming compression | `heatshrink-integration` |

**DSP & ML**

| Library or task | Prefer |
| --- | --- |
| CMSIS-DSP math, FFT, filters | `cmsis-dsp-integration` |
| TinyMaix MCU inference, model loading | `tinymaix-integration` |

**Input, Timers & State Machines**

| Library or task | Prefer |
| --- | --- |
| MultiButton, FlexibleButton | `embedded-input-libs` |
| MultiTimer, software timers | `embedded-timing-libs` |
| Ring buffer, FIFO, MCU queues | `embedded-buffer-queue-libs` |
| State machine libraries | `embedded-state-machine-libs` |

**Frameworks & Patterns**

| Library or task | Prefer |
| --- | --- |
| PLOOC object-oriented C | `plooc-integration` |
| Avem event-driven components | `avem-integration` |
| Power management framework | `power-management-integration` |
| Embedded app examples adaptation | `embedded-app-example-libs` |

**Testing**

| Library or task | Prefer |
| --- | --- |
| Unity, Ceedling, CMock embedded C tests | `unity-ceedling-integration` |

**Fallback (not a library issue)**

| Symptom | Prefer |
| --- | --- |
| MCU flash, erase, verify failure | `mcu-flashing-debug` |
| UART transport or missing logs | `embedded-serial-log-debug` |
| RTOS task, mutex, queue, stack issue | `rtos-debug` |
| Board power, reset, pin, or signal issue | `hardware-interface-debug` |

## Workflow

1. Route by library responsibility.
   Identify whether the library depends on storage, UART, RTOS primitives, heap, timers, display, network, or flash erase/program operations.

1. Confirm platform contracts.
   Ask for the porting hooks the library expects and the project already provides.

1. Preserve data and flash.
   Formatting filesystems, erasing database partitions, wiping logs, or changing flash layout requires explicit user approval.

1. Keep integration minimal.
   Bring up one smallest working path before enabling optional features such as async logging, wear leveling stress tests, shell authentication, or compression.

1. Verify with a target-relevant scenario.
   A library compiles successfully only proves syntax. Require a read/write, log, shell command, or crash capture that exercises the port layer.

## Verification

Before moving to a specific library workflow:

- State the selected library skill and why.
- State target MCU/RTOS/compiler/build system if known.
- Identify required porting hooks and missing inputs.
- Confirm no data-destructive action has been recommended without approval.

## Common Failures

- Treating a library as portable because it compiles on desktop.
- Enabling all optional features before the minimal port works.
- Ignoring flash erase size, write alignment, and power-fail behavior.
- Debugging library logic before validating the porting layer.
- Assuming malloc, mutexes, time functions, or file APIs exist on bare metal.

## Example

User:

```text
我想在 STM32 项目里加 littlefs 保存配置。
```

Agent:

1. Routes to `littlefs-integration`.
1. Asks for flash layout, erase/program sizes, bad block assumptions, RTOS locking, and whether formatting is allowed.
1. Verifies mount, format-if-approved, file write, sync, reboot, and readback.
