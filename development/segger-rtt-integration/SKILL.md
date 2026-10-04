---
name: segger-rtt-integration
description: Use when integrating, configuring, or debugging SEGGER RTT logs, J-Link real-time terminal I/O, RTT control blocks, buffers, blocking modes, or embedded debug output
---

# SEGGER RTT Integration

## Overview

Use this skill to integrate SEGGER RTT as a low-intrusion debug channel. Prove the RTT control block, buffer configuration, J-Link connection, and blocking policy before relying on RTT logs in timing-sensitive firmware.

## When To Use

Use this skill when:

- The user wants SEGGER RTT logs or terminal input on an MCU.
- RTT Viewer/J-Link cannot find the control block, logs are missing, output blocks, or input commands fail.
- The task involves RTT buffers, up/down channels, blocking modes, J-Link, SystemView, or debug builds.

Do not use this skill when the debug probe cannot connect. Use architecture or flashing debug skills first.

## First Questions

Ask for:

- MCU/core, debug probe, J-Link software version, and IDE/toolchain.
- RTT source files/config and whether `SEGGER_RTT_Init()` is called.
- Output mode: blocking, no-block-skip, or no-block-trim.
- Buffer sizes and channels used.
- Whether caches, MPU, low power, or secure/non-secure memory are involved.

## Integration Checklist

1. Include RTT sources once.
   Avoid duplicate control blocks from multiple copies of RTT source.

1. Place control block in accessible RAM.
   J-Link must be able to locate and read the RTT control block.

1. Configure buffer policy.
   Blocking output can disturb real-time behavior; choose mode intentionally.

1. Verify host tooling.
   RTT Viewer, J-Link console, IDE plugin, or SystemView must attach to the correct target.

1. Handle cache and low power.
   Cacheable memory and deep sleep can hide or disrupt RTT buffers.

## Common Failures

- Control block optimized out or duplicated.
- RTT logs block because host is disconnected and blocking mode is used.
- Buffers too small for burst logs.
- J-Link scans wrong RAM region.
- Cache prevents host from seeing updated data on some cores.

## Verification

Before claiming RTT works:

- State probe, RTT source/config, buffer sizes, and blocking mode.
- Confirm host tool sees the control block.
- Confirm one output channel and one input channel if input is needed.
- Confirm behavior with host disconnected if product timing matters.

## Example

User:

```text
SEGGER RTT Viewer 连上了但没有日志。
```

Agent:

1. Asks for RTT config, init path, J-Link target, and map/control block placement.
1. Checks duplicate RTT sources and buffer mode.
1. Verifies a minimal early boot RTT print.
