---
name: zephyr-integration
description: Use when integrating, porting, configuring, or debugging Zephyr RTOS, west builds, devicetree overlays, Kconfig, drivers, threads, logging, networking, or board support
---

# Zephyr Integration

## Overview

Use this skill to debug Zephyr by separating board selection, devicetree, Kconfig,
driver binding, and runtime behavior. Zephyr issues usually come from build-time
configuration mismatches before they appear as firmware bugs.

## When To Use

Use this skill when:

- The user is working with Zephyr RTOS, `west`, boards, shields, samples, or
  custom board ports.
- The issue involves devicetree overlays, Kconfig symbols, drivers, threads,
  logging, flash partitions, networking, Bluetooth, or power management.
- A build succeeds but the device tree binding, generated config, or runtime
  device readiness is suspicious.

Do not use this skill for generic RTOS scheduling bugs with no Zephyr-specific
surface. Use `rtos-debug` or `freertos-kernel-debug` instead.

## First Questions

Ask for:

- Zephyr version, SDK/toolchain, `west` workspace layout, board, and sample/app.
- Full `west build` command, `prj.conf`, overlays, and board revision.
- Relevant devicetree node, binding, compatible string, alias, and chosen node.
- Generated `zephyr.dts`, `.config`, and the failing log or build error.
- Whether the issue is build-time, boot-time, driver probing, or runtime.

## Debug Workflow

1. Reproduce the build.
   Capture the exact `west build` command, board, app path, and pristine status.

1. Inspect generated artifacts.
   Check `build/zephyr/zephyr.dts`, `.config`, and generated headers before
   editing source code.

1. Prove devicetree binding.
   Confirm `status = "okay"`, `compatible`, pinctrl, clocks, interrupts,
   aliases, and chosen nodes.

1. Prove Kconfig selection.
   Verify symbols in `.config`, dependency chains, and whether another config
   file overrides the intended value.

1. Check device readiness.
   Use `device_is_ready()`, init priority, logging, and driver return codes.

1. Debug runtime behavior.
   Only after configuration is proven, inspect threads, stacks, work queues,
   interrupts, buffers, and subsystem-specific APIs.

## Common Failures

- Overlay targets the wrong board revision or node path.
- Kconfig symbol is set in `prj.conf` but silently unmet due to dependencies.
- Driver instance exists in devicetree but is disabled or lacks pinctrl/clocks.
- Code uses a device before its init priority has run.
- Stack sizes are too small for logging, networking, Bluetooth, or filesystem.
- A stale build directory hides changed devicetree or Kconfig input.

## Verification

Before claiming a Zephyr fix works:

- State Zephyr version, board, build command, overlay, and key Kconfig symbols.
- Confirm generated `zephyr.dts` and `.config` contain the intended values.
- Confirm driver readiness or subsystem initialization in logs.
- Confirm runtime behavior on hardware or in the selected emulator/simulator.

## Example

User:

```text
Zephyr 里 I2C sensor 一直 device not ready。
```

Agent:

1. Checks board, overlay, generated devicetree, and Kconfig dependencies.
1. Verifies the bus, sensor node, pinctrl, clocks, and init priority.
1. Only then inspects the sensor driver and read path.
