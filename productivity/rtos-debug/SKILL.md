---
name: rtos-debug
description: Use when debugging embedded RTOS scheduling, tasks, threads, stacks, priorities, mutexes, queues, interrupts, timers, or FreeRTOS, RT-Thread, Zephyr, ThreadX, or CMSIS-RTOS issues
---

# RTOS Debug

## Overview

Use this skill to debug RTOS problems by separating scheduler state, task stack health, synchronization, interrupt priority, timing, and resource ownership. Start from observable RTOS state before changing priorities or adding delays.

## When To Use

Use this skill when:

- Firmware uses FreeRTOS, RT-Thread, Zephyr, ThreadX, CMSIS-RTOS, or another embedded scheduler.
- The user reports deadlock, starvation, missed events, queue timeout, stack overflow, watchdog reset, priority inversion, or task not running.
- The issue involves ISR-to-task signaling, timers, semaphores, mutexes, message queues, or task notifications.

Do not use this skill before the target is known to boot and run at least some firmware. For RTOS-specific deep dives, prefer `freertos-kernel-debug`, `zephyr-integration`, or `rt-thread-integration` when the RTOS is identified.

## First Questions

Ask for:

- RTOS name/version and MCU/SoC.
- Symptom and when it occurs.
- Task list with priorities, stack sizes, and key responsibilities.
- Whether stack overflow checking, runtime stats, trace, or thread awareness is enabled.
- ISR sources involved and interrupt priorities.
- Logs, asserts, watchdog reason, or debugger task view.

## Workflow

1. Confirm the scheduler starts.
   Verify the system reaches scheduler start and at least one known task runs.

1. Capture task state.
   Collect task names, states, priorities, stack high water marks, CPU/runtime stats, and blocked objects.

1. Check stack and heap first.
   Stack overflow and heap exhaustion often masquerade as random RTOS failures.

1. Inspect synchronization.
   Identify which task owns each mutex, which queue is full/empty, and whether ISR-safe APIs are used from interrupts.

1. Check interrupt priority rules.
   Ensure ISR priorities are legal for RTOS API calls and do not starve the scheduler tick.

1. Replace guesses with probes.
   Use trace hooks, assertions, watermarks, counters, or event logs instead of adding arbitrary delays.

## Checks

- Stack high water mark for each task.
- Heap free/minimum ever free.
- Tick interrupt running at expected rate.
- Watchdog servicing task not starved.
- Mutex ownership and recursive/non-recursive mismatch.
- Queue length, item size, send/receive timeout.
- ISR uses correct `FromISR` APIs where required.
- Critical sections are short and bounded.
- Priority inversion protection exists where shared resources are used.

## Verification

Before claiming RTOS progress:

- State RTOS, scheduler status, task states, and stack/heap evidence.
- Identify the blocked or starving task and the object it waits on.
- State whether interrupt priorities are legal for RTOS API usage.
- Report any assertion, watchdog, or stack overflow hook evidence.

## Common Failures

- Raising task priority without knowing why it is blocked.
- Adding delays to hide races.
- Calling non-ISR-safe APIs from interrupts.
- Ignoring stack high water marks.
- Debugging a queue payload before confirming queue item size and ownership.

## Example

User:

```text
FreeRTOS 有个任务偶尔不跑，最后看门狗复位。
```

Agent:

1. Asks for task list, priorities, stack sizes, watchdog owner, and task states.
1. Checks high water marks, heap, tick, and blocked objects.
1. Verifies ISR priority and queue/mutex ownership before suggesting priority changes.
