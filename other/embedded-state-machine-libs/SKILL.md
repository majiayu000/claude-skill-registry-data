---
name: embedded-state-machine-libs
description: Use when integrating, designing, configuring, or debugging embedded StateMachine libraries, finite state machines, event transitions, or MCU state-driven workflows
---

# Embedded State Machine Libs

## Overview

Use this skill for embedded state machine libraries and hand-written finite state machines. The core is to make states, events, transitions, side effects, and invalid transitions explicit and verifiable.

## When To Use

Use this skill when:

- The user wants to add or debug a StateMachine library or event-driven MCU workflow.
- The issue involves wrong transitions, stuck states, reentrancy, event loss, timeout handling, or unclear state ownership.
- Firmware has modes such as idle, init, run, error, recovery, upgrade, sleep, or calibration.

Do not use this skill for RTOS scheduling issues unless the state machine is the primary abstraction.

## First Questions

Ask for:

- State machine library or custom implementation.
- State list, event list, and current failing transition.
- Whether transitions run in ISR, task, main loop, or callback context.
- Whether timeouts, retries, or external interrupts drive events.
- Expected behavior for invalid events.

## Integration Checklist

1. Define states and events.
   Names should reflect system meaning, not implementation steps.

1. Separate transition from action.
   Make it clear what changes state and what side effects run because of the transition.

1. Define invalid event behavior.
   Ignore, log, assert, error transition, or recovery must be explicit.

1. Guard reentrancy.
   Avoid nested transitions unless the library explicitly supports them.

1. Add observability.
   Log state transitions, current state, event source, and error transitions.

1. Test transition table.
   Validate normal path, invalid events, timeout events, and recovery path.

## Common Failures

- Event emitted from ISR directly mutates state unsafely.
- Timeout event races with success event.
- State transition has hidden side effects that fail halfway.
- Invalid events are silently ignored in safety-critical flows.
- State names mirror functions instead of product behavior.

## Verification

Before claiming state-machine behavior works:

- State the state list, event list, transition rules, and invalid-event policy.
- Confirm normal, timeout, error, and recovery transitions.
- Confirm event source and reentrancy strategy.
- Confirm transition logging or trace output exists for debugging.

## Example

User:

```text
设备升级状态机偶尔卡在 downloading。
```

Agent:

1. Asks for states, events, timeout handling, and transition logs.
1. Checks whether success/error/timeout events race.
1. Verifies recovery transitions and invalid event behavior.
