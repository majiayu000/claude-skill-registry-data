---
name: easylogger-integration
description: Use when integrating, porting, configuring, or debugging EasyLogger output, filters, timestamps, colors, async logging, flash logging, or embedded log loss
---

# EasyLogger Integration

## Overview

Use this skill to integrate EasyLogger without making logs distort the system being debugged. Confirm output backend, timestamp source, concurrency, buffer policy, and log level before relying on logs as evidence.

## When To Use

Use this skill when:

- The user wants to add or debug EasyLogger in MCU, RTOS, or bare-metal firmware.
- Logs are missing, truncated, blocking, out of order, too slow, too verbose, or not timestamped correctly.
- The task involves `elog_port`, UART output, flash/file logging, filters, colors, async output, or runtime log levels.

Do not use this skill when the issue is raw UART capture quality. Use `embedded-serial-log-debug` first.

## First Questions

Ask for:

- Target MCU/RTOS/compiler and EasyLogger version or source.
- Output backend: UART, RTT, semihosting, file, flash, network, shell, or custom.
- Whether logs can block, allocate memory, or run in interrupt context.
- Timestamp source and desired format.
- Current `elog_cfg` and port functions if available.
- Symptom and sample log output.

## Integration Checklist

1. Bring up one output path.
   Prove a minimal blocking UART/RTT output works before enabling async, flash, or network logging.

1. Implement port functions deliberately.
   Output, lock/unlock, time, and optional color handling must match the target environment.

1. Set log levels and filters.
   Avoid enabling verbose logs globally on timing-sensitive firmware.

1. Decide concurrency policy.
   Use mutexes or critical sections when multiple tasks or ISRs can log.

1. Bound cost.
   Understand stack, heap, formatting, blocking time, and output bandwidth.

1. Preserve diagnostic value.
   Logs should include module, level, time, and enough context to correlate with faults or events.

## Porting Checks

- `elog_port_output` cannot deadlock if called from error paths.
- Lock implementation is safe before and after scheduler start.
- ISR logging policy is explicit: forbidden, buffered, or minimal.
- Timestamp source is initialized before first log or handles early boot.
- UART backend does not block forever if host is disconnected.
- Flash/file logging does not erase production data without approval.

## Common Failures

- Logs disappear because output port is not initialized before first log.
- System timing changes because logging blocks in a high-frequency path.
- Deadlock occurs because logger lock is used inside a locked driver.
- Timestamps are always zero because tick source starts after logger init.
- HardFault handler logs too much and corrupts stack or blocks.

## Verification

Before claiming EasyLogger works:

- State output backend, timestamp source, lock policy, and log level.
- Confirm one log from early init and one log after scheduler start if RTOS is used.
- Confirm logs are not lost or garbled at the chosen baud/backend speed.
- Confirm ISR/error-path logging policy.
- If persistent logging is enabled, confirm storage and erase policy.

## Example

User:

```text
EasyLogger 接上了，但 FreeRTOS 里偶尔日志乱序还卡住。
```

Agent:

1. Asks for backend, lock implementation, task/ISR logging paths, baud rate, and async setting.
1. Checks whether output blocks while holding a mutex.
1. Verifies task logs and ISR policy separately before changing log levels.
