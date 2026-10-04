---
name: embedded-timing-libs
description: Use when integrating, porting, configuring, or debugging embedded software timer libraries such as MultiTimer, timeout schedulers, or tick-based callback timers
---

# Embedded Timing Libs

## Overview

Use this skill for lightweight software timer libraries such as MultiTimer. The agent should confirm tick source, callback context, time units, wraparound behavior, and scheduler frequency before relying on timer callbacks.

## When To Use

Use this skill when:

- The user wants to add or debug MultiTimer, software timers, timeout lists, periodic callbacks, or one-shot timers.
- Timers drift, fire too early/late, stop firing, fire repeatedly, or break across tick overflow.

Do not use this skill for hardware PWM/timer peripheral bring-up. Use `embedded-peripheral-bringup` for register-level timer issues.

## First Questions

Ask for:

- Timer library and target runtime.
- Tick source and frequency.
- Callback context: main loop, RTOS task, ISR, or scheduler hook.
- Time units used by the library and application.
- Number of timers and longest expected uptime.
- Whether callbacks may start/stop other timers.

## Integration Checklist

1. Confirm tick monotonicity.
   Timer logic needs a stable increasing timebase or explicit wraparound handling.

1. Match units.
   Milliseconds, ticks, microseconds, and RTOS ticks must not be mixed silently.

1. Define callback context.
   Timer callbacks must not block if they run in ISR or scheduler critical context.

1. Test one-shot and periodic behavior.
   Verify start, stop, restart, and callback ordering.

1. Test wraparound.
   Use simulated ticks or shortened counters to prove overflow behavior.

## Common Failures

- Tick function returns seconds while timer expects milliseconds.
- Callback blocks in interrupt context.
- Timer list is modified while iterating without protection.
- Drift accumulates because periodic timers restart from callback time instead of scheduled time.
- Wraparound breaks after long uptime.

## Verification

Before claiming timer integration works:

- State tick source, frequency, unit, callback context, and protection strategy.
- Confirm one-shot, periodic, cancel, restart, and wraparound behavior.
- Confirm callback execution time is acceptable.
- Confirm timer operations are safe from ISR/task contexts in use.

## Example

User:

```text
MultiTimer 定时回调偶尔不准。
```

Agent:

1. Asks for tick source, units, callback context, and scheduling frequency.
1. Checks unit conversion and whether callbacks block.
1. Tests periodic drift and tick wraparound with a small counter.
