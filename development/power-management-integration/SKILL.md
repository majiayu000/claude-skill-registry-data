---
name: power-management-integration
description: Use when integrating, porting, configuring, or debugging embedded PowerManagement libraries, power domains, sleep policies, device suspend/resume, or runtime PM frameworks
---

# PowerManagement Integration

## Overview

Use this skill for library/framework-level power management, not just one low-power symptom. Confirm the system's power states, device dependencies, suspend/resume ordering, wake sources, and measurement method before enabling automatic PM policies.

## When To Use

Use this skill when:

- The user mentions `PowerManagement`, PM framework, runtime PM, device suspend/resume, power domains, or system sleep policy.
- The project needs coordinated low-power behavior across drivers, RTOS tasks, clocks, and wake sources.
- Devices fail after resume, wake immediately, lose state, or consume too much current under a PM framework.

Do not use this skill for one-off current measurement without a PM framework. Use `low-power-debug` first.

## First Questions

Ask for:

- Power-management library/framework source and target MCU/RTOS.
- Power states: run, idle, sleep, stop, standby, deep sleep, off, or custom.
- Device list and dependencies: clocks, buses, sensors, radio, display, storage, and debug.
- Wake sources, retention requirements, and expected current.
- Existing suspend/resume hooks and current symptom.

## Integration Checklist

1. Define state model.
   Each power state needs entry conditions, exit sources, retained resources, and forbidden operations.

1. Build dependency order.
   Suspend children before parents and resume parents before children. Clocks and buses must wrap device hooks.

1. Separate policy from mechanism.
   Drivers expose capabilities; policy decides when to enter a state.

1. Verify wake source ownership.
   Wake flags must be read before clearing, and the responsible device should be identifiable.

1. Protect debug and recovery.
   Deep states may disconnect SWD/JTAG or UART; define a recovery path.

1. Measure with framework enabled.
   Compare current in each state and after resume, not only during entry.

## Common Failures

- Driver resumes before its bus or clock is restored.
- Wake flags are cleared before being logged.
- A task vetoes sleep forever but does not report why.
- Device state is not reinitialized after deep sleep.
- Debug probe keeps rails active and invalidates current measurements.

## Verification

Before claiming PM integration works:

- State power states, policy, device dependency order, and wake sources.
- Confirm at least one enter/resume cycle for the target state.
- Report current measurement setup and measured value if power is in scope.
- Confirm recovery/debug path after deep sleep.
- List devices without suspend/resume support.

## Example

User:

```text
接了 PowerManagement 框架后，睡眠能进但唤醒后 I2C 传感器读不到。
```

Agent:

1. Asks for PM state, I2C bus/device hooks, clock dependencies, and wake source.
1. Checks resume ordering and bus clock restoration.
1. Verifies repeated suspend/resume cycles with current and device-read evidence.
