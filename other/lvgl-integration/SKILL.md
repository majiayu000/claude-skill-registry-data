---
name: lvgl-integration
description: Use when integrating, porting, configuring, or debugging LVGL, littlevGL, display drivers, input devices, ticks, draw buffers, or embedded GUI performance
---

# LVGL Integration

## Overview

Use this skill to integrate LVGL by proving four porting contracts: display flush, input device read, tick/timebase, and memory/draw buffer configuration. UI bugs often come from driver timing or buffer ownership, not widget logic.

## When To Use

Use this skill when:

- The user wants to add or debug LVGL/littlevGL on an MCU or embedded Linux display.
- The issue involves blank screen, wrong colors, tearing, touch offset, slow refresh, memory faults, tick handling, or display flush callbacks.
- The project has display, touch, encoder, keypad, RTOS, or DMA/cache constraints.

Do not use this skill when the display hardware has no proven signal. Use `hardware-interface-debug` first.

## First Questions

Ask for:

- LVGL major version and target platform.
- Display controller, resolution, color format, interface, and framebuffer/draw buffer strategy.
- Input devices: touch, buttons, encoder, keypad, or none.
- Tick source and `lv_timer_handler` scheduling.
- RAM budget, heap policy, RTOS use, DMA/cache involvement.
- Current symptom and minimal screen test result.

## Integration Checklist

1. Bring up display flush.
   Fill the screen with solid colors before creating complex widgets.

1. Configure draw buffers.
   Buffer size, color format, stride, and cache/DMA policy must match the display path.

1. Provide a reliable tick.
   LVGL needs a monotonic tick and regular handler execution.

1. Add input after display.
   Touch/encoder/keypad should be calibrated and tested independently.

1. Bound memory.
   Configure heap, widget count, image assets, fonts, and buffers for the target RAM.

1. Verify refresh performance.
   Measure frame time, flush completion, and whether `lv_disp_flush_ready` is called correctly.

## Common Failures

- Blank screen because flush callback never calls ready.
- Wrong colors from RGB/BGR or 16-bit endian mismatch.
- Touch coordinates need rotation/calibration transform.
- UI freezes because `lv_timer_handler` is not called regularly.
- DMA reads stale cache lines or writes to non-DMA-capable memory.
- Fonts/images exceed flash or RAM budgets.

## Verification

Before claiming LVGL works:

- State LVGL version, resolution, color format, buffer size, and tick period.
- Confirm solid color flush, a label/button screen, and input event if applicable.
- Confirm `lv_timer_handler` schedule and flush-ready behavior.
- Confirm memory usage and DMA/cache policy when relevant.

## Example

User:

```text
LVGL 移植后屏幕花屏，触摸也偏。
```

Agent:

1. Asks for LVGL version, display controller, color format, buffer config, rotation, and touch driver.
1. Tests solid colors and flush-ready before widgets.
1. Calibrates touch transform after display orientation is correct.
