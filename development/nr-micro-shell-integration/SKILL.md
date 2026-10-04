---
name: nr-micro-shell-integration
description: Use when integrating, porting, configuring, or debugging nr_micro_shell command consoles, UART shell input, command tables, or tiny embedded CLI behavior
---

# nr_micro_shell Integration

## Overview

Use this skill to integrate nr_micro_shell as a compact command console. Keep the first port minimal: verified character I/O, one read-only command, bounded buffers, and explicit handling for destructive commands.

## When To Use

Use this skill when:

- The user wants a tiny shell/CLI on an MCU and mentions nr_micro_shell.
- Commands are not recognized, input is garbled, completion/history fails, or shell processing blocks firmware.
- The target needs a lower-footprint alternative to larger embedded shells.

Do not use this skill when raw UART is not proven. Use `embedded-serial-log-debug` first.

## First Questions

Ask for:

- Target MCU/RTOS/compiler and nr_micro_shell version/source.
- Transport: UART, USB CDC, RTT, TCP, or custom stream.
- Polling, interrupt, DMA, or task-based input model.
- Command table/registration approach.
- Maximum command length, argument count, and stack/RAM budget.
- Whether shell is enabled in production builds.

## Integration Checklist

1. Verify raw I/O.
   Confirm single-character RX/TX before attaching shell parsing.

1. Configure buffers.
   Set command line, history, and output buffers within RAM limits.

1. Register one safe command.
   Start with `help`, `version`, or `status`.

1. Validate argument parsing.
   Commands must reject missing, too many, or invalid arguments.

1. Bound output.
   Avoid long blocking output that starves watchdogs or RTOS tasks.

1. Guard risky commands.
   Reset, erase, format, calibration, flash writes, or network writes need build guards or authentication.

## Common Failures

- RX callback stores characters but shell process function is never called.
- Command table is not linked or is optimized out.
- Backspace/newline behavior mismatches terminal settings.
- Long command output blocks system timing.
- Debug shell remains enabled in production without restrictions.

## Verification

Before claiming nr_micro_shell works:

- State transport, scheduling model, buffer sizes, and command registration method.
- Confirm raw RX/TX, `help`, one custom read-only command, invalid command, and argument error behavior.
- Confirm risky commands are absent, disabled, or guarded.

## Example

User:

```text
想用 nr_micro_shell 做一个串口调试命令行。
```

Agent:

1. Asks for UART path, scheduler model, buffer size, and production policy.
1. Verifies raw serial, then registers `status`.
1. Tests command parsing and guards destructive commands.
