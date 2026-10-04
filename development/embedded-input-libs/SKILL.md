---
name: embedded-input-libs
description: Use when integrating, porting, configuring, or debugging embedded button/input libraries such as MultiButton or FlexibleButton
---

# Embedded Input Libs

## Overview

Use this skill for button and simple input libraries such as MultiButton and FlexibleButton. The key is to align scan period, debounce time, electrical polarity, event semantics, and callback context.

## When To Use

Use this skill when:

- The user wants to add or debug MultiButton, FlexibleButton, key scanning, long press, double click, or button event callbacks.
- Inputs bounce, trigger twice, miss long presses, fire in the wrong order, or behave differently across boards.

Do not use this skill for complex UI frameworks or touch/display systems. Use LVGL-related skills when UI event routing dominates.

## First Questions

Ask for:

- Library: MultiButton, FlexibleButton, or custom button helper.
- Button circuit: pull-up/pull-down, active level, GPIO mode, external RC, matrix, or direct GPIO.
- Scan period and where scanning runs: timer, main loop, RTOS task, or interrupt.
- Desired events: press, release, click, double click, long press, repeat, hold.
- Current symptom and logic analyzer or GPIO trace if available.

## Integration Checklist

1. Confirm electrical polarity.
   Active-low buttons with pull-ups are common; software level must match hardware.

1. Choose a stable scan period.
   Debounce and click timing depend on the scan tick being regular.

1. Keep callbacks lightweight.
   Button callbacks should post events or set flags, not block or write flash.

1. Define event semantics.
   Decide whether long press also emits click, whether double click suppresses single click, and when release fires.

1. Test with measured input.
   Compare software events with a logic analyzer or GPIO trace when behavior is unclear.

## Common Failures

- Wrong active level makes pressed and released inverted.
- Scan period jitter breaks double-click detection.
- Long press also triggers unwanted single click.
- Callback runs in timer/ISR context and blocks.
- Shared button state is accessed from multiple tasks without protection.

## Verification

Before claiming input handling works:

- State active level, scan period, debounce time, and callback context.
- Test press, release, click, long press, repeated press, and bounce.
- Confirm event order matches product expectations.
- Confirm no flash writes or blocking operations occur in unsafe context.

## Example

User:

```text
MultiButton 长按会同时触发单击。
```

Agent:

1. Asks for scan period, event configuration, active level, and expected semantics.
1. Checks whether single click is delayed until double/long decision is known.
1. Verifies event order with a controlled press-duration test.
