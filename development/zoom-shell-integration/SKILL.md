---
name: zoom-shell-integration
description: Use when integrating, porting, configuring, or debugging an embedded zoom-shell style command console, UART CLI, command parser, or tiny MCU shell
---

# zoom-shell Integration

## Overview

Use this skill when the user explicitly means an embedded `zoom-shell` style MCU command console. Because the name is ambiguous, first confirm this is an embedded shell library, not the Zoom desktop application or a security research reverse shell.

## When To Use

Use this skill when:

- The user mentions `zoom-shell` in the context of MCU firmware, serial CLI, UART shell, or embedded command parsing.
- A tiny shell has missing commands, broken argument parsing, blocking output, or unreliable serial input.
- The task involves command tables, help output, bounded buffers, terminal line endings, or production debug command guards.

Do not use this skill for Zoom meeting apps, desktop automation, reverse shells, or non-embedded security research.

## First Questions

Ask for:

- The exact `zoom-shell` repository or source package.
- Target MCU, compiler, RTOS/bare-metal runtime, and serial transport.
- Input model: polling, interrupt RX, DMA RX, RTOS queue, USB CDC, RTT, or TCP.
- Command registration method and current command list.
- Maximum command length, argument count, and stack/RAM limits.
- Whether shell commands are allowed in production firmware.

## Integration Checklist

1. Confirm the library identity.
   Verify the user-provided source is an embedded shell and not an unrelated Zoom project.

1. Prove raw transport.
   Check RX/TX before debugging shell parsing.

1. Configure bounded buffers.
   Command line, argument list, history, and output buffers must fit RAM and reject overflow.

1. Register one read-only command.
   Start with `help`, `version`, or `status`.

1. Validate argument parsing.
   Test missing arguments, extra arguments, invalid numbers, and long input.

1. Guard dangerous commands.
   Reset, erase, format, firmware update, calibration, and production-data commands need build guards or explicit authorization.

## Common Failures

- Wrong library selected because `zoom-shell` name was ambiguous.
- Shell receives characters but parser is not pumped from the main loop or task.
- Newline/backspace handling mismatches terminal settings.
- Command buffers overflow on pasted input.
- Debug commands remain enabled in release builds.

## Verification

Before claiming zoom-shell integration works:

- State source repository/package, transport, scheduling model, and buffer limits.
- Confirm raw RX/TX, `help`, one custom read-only command, invalid command, and long input handling.
- Confirm dangerous commands are absent, disabled, or guarded.

## Example

User:

```text
想把 zoom-shell 接到串口里做调试命令。
```

Agent:

1. Confirms the source is an embedded shell library.
1. Verifies raw UART RX/TX.
1. Registers `status` and tests invalid/long commands before adding write commands.
