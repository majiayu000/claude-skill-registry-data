---
name: letter-shell-integration
description: Use when integrating, porting, configuring, or debugging letter-shell command shells, UART shell transport, command registration, RTOS shell tasks, or embedded debug consoles
---

# letter-shell Integration

## Overview

Use this skill to integrate letter-shell as an embedded debug console safely. Prove the transport, shell task or polling loop, command registration, and authorization policy before exposing commands that modify flash, reset devices, or change production state.

## When To Use

Use this skill when:

- The user wants to add or debug letter-shell in MCU firmware.
- Shell input/output is missing, commands are not found, history/completion behaves wrong, or shell blocks the system.
- The task involves UART shell, RTT shell, RTOS shell task, command export macros, login/password, or runtime debug commands.

Do not use this skill when the serial port itself is not trustworthy. Use `embedded-serial-log-debug` first.

## First Questions

Ask for:

- Target MCU/RTOS/compiler and letter-shell version or source.
- Transport backend: UART, USB CDC, RTT, TCP, or custom.
- Runtime model: polling loop, interrupt-driven RX, DMA RX, or RTOS task.
- Existing shell config, command registration method, and linker section behavior.
- Whether shell is allowed in production builds.
- Commands that may be destructive, such as erase, reset, format, calibration, network write, or firmware update.

## Integration Checklist

1. Prove transport first.
   Confirm raw RX/TX works before debugging shell parsing.

1. Create one shell instance.
   Bind it to explicit read/write functions and initialize it once.

1. Decide scheduling model.
   Use a polling loop for simple bare-metal demos or a dedicated task/event-driven model for RTOS projects.

1. Register one harmless command.
   Start with `version`, `help`, or `status` before adding state-changing commands.

1. Confirm linker retention.
   If commands are exported through sections/macros, ensure the linker script and optimization settings keep them.

1. Add access control for risky commands.
   Commands that erase flash, format filesystems, reset devices, change boot config, or modify calibration require explicit user/product approval.

## Porting Checks

- UART/CDC/RTT output is non-blocking enough for the product.
- RX buffering handles backspace, line endings, paste bursts, and command length.
- Shell task stack is large enough for formatting and command handlers.
- Command handlers validate arguments and return useful errors.
- Shell does not run in interrupt context unless the library explicitly supports it.
- Production builds can disable or restrict debug commands.

## Common Failures

- Raw UART works but shell does not receive because RX callback is not connected to shell input.
- Commands disappear because linker garbage collection removed command sections.
- Shell blocks lower-priority tasks due to long output or blocking writes.
- Command handler crashes from unchecked arguments.
- Dangerous maintenance commands are exposed without authentication or build guards.

## Verification

Before claiming letter-shell works:

- State transport, scheduler model, shell instance, and command registration method.
- Confirm `help` or an equivalent harmless command works.
- Confirm one custom read-only command works.
- Confirm line ending, backspace, and invalid command behavior.
- Identify destructive commands and their guard policy.

## Example

User:

```text
想接 letter-shell，通过串口输入命令查看系统状态。
```

Agent:

1. Asks for UART backend, RTOS/bare-metal model, config, and command export method.
1. Verifies raw serial RX/TX first.
1. Registers a read-only `status` command and confirms `help` can list it.
1. Adds guardrails before exposing reset, erase, or format commands.
