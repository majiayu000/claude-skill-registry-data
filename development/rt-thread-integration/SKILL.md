---
name: rt-thread-integration
description: Use when integrating, porting, configuring, or debugging RT-Thread, Env, Kconfig, FinSH, device framework, DFS, networking, packages, or board support
---

# RT-Thread Integration

## Overview

Use this skill to debug RT-Thread by separating BSP configuration, kernel
objects, device framework registration, components, and packages. RT-Thread
problems often come from missing component config or device registration order.

## When To Use

Use this skill when:

- The user is working with RT-Thread, RT-Thread Studio, Env, SCons, BSPs, or
  packages.
- The issue involves threads, semaphores, mailboxes, message queues, timers,
  FinSH/MSH, device drivers, DFS, SAL, lwIP, or OTA components.
- A peripheral, filesystem, shell command, or network interface is present in
  code but missing at runtime.

Do not use this skill for a generic MCU peripheral with no RT-Thread component
surface. Use `embedded-peripheral-bringup` first. For generic RTOS scheduling
triage, use `rtos-debug`.

## First Questions

Ask for:

- RT-Thread version, BSP, board, toolchain, build system, and `rtconfig.h`.
- Enabled components/packages from menuconfig or RT-Thread Studio.
- Device name, driver registration path, init level, and FinSH output.
- Thread list, stack sizes, priorities, heap size, and console log.
- Current symptom and the command or API that fails.

## Integration Checklist

1. Reproduce the build configuration.
   Capture BSP, toolchain, package versions, `rtconfig.h`, and generated files.

1. Prove console and shell.
   Bring up UART console and FinSH/MSH before deeper component debugging.

1. Check kernel objects.
   Inspect thread state, stack, priority, tick, heap, and IPC object ownership.

1. Prove device registration.
   Confirm driver init level, device name, class, open flags, and `list_device`.

1. Add components one layer at a time.
   For DFS, SAL, lwIP, USB, or OTA, verify the lower device and config first.

1. Validate package assumptions.
   Check package versions, include paths, component symbols, and board hooks.

## Common Failures

- `rtconfig.h` does not include the component the code expects.
- Device is registered under a different name than the application opens.
- Driver init runs before clocks, pins, DMA, or heap are ready.
- Thread stack is too small for shell, filesystem, or networking code.
- FinSH command exists but is compiled out by component config.
- Package code assumes a POSIX, DFS, or SAL layer that is not enabled.

## Verification

Before claiming RT-Thread integration works:

- State RT-Thread version, BSP, build command, and enabled components.
- Confirm console/shell output and relevant `list_*` command evidence.
- Confirm device registration and open/read/write or control behavior.
- Confirm stack and heap margins for the exercised path.

## Example

User:

```text
RT-Thread 里 spi device 找不到。
```

Agent:

1. Checks BSP config, SPI component symbols, and board pin init.
1. Uses shell device listing to confirm registration name and class.
1. Fixes init order or device name before changing the application driver.
