---
name: epd-integration
description: Use when integrating, porting, or debugging e-paper EPD displays, waveform initialization, SPI drivers, busy pins, partial refresh, ghosting, or low-power display updates
---

# EPD Integration

## Overview

Use this skill to integrate e-paper displays by proving power sequencing, reset, SPI commands, busy timing, framebuffer layout, waveform/LUT setup, and refresh mode. EPD failures are timing and panel-variant sensitive, so driver code must match the exact module.

## When To Use

Use this skill when:

- The user wants to add or debug e-paper/e-ink display panels on MCUs or embedded Linux.
- The issue involves blank screen, stuck busy pin, mirrored image, ghosting, partial refresh artifacts, slow refresh, or high sleep current.
- The project uses SPI, GPIO reset/DC/CS/busy pins, external boost power, partial update, deep sleep, or multiple color planes.

Do not use this skill for generic GUI widget logic. Use `lvgl-integration` or `u8g2-integration` after the panel refresh path is proven.

## First Questions

Ask for:

- Exact panel/module part number, resolution, color planes, controller IC, and vendor demo code.
- Pin mapping for SPI, CS, DC, reset, busy, panel power, and optional enable pins.
- SPI mode/speed, reset timing, init commands, LUT/waveform source, and refresh mode.
- Framebuffer format, bit order, rotation, and partial update area.
- Current symptom, busy pin behavior, and photos if visual output is wrong.

## Integration Checklist

1. Match the exact panel.
   Resolution, controller, LUT, color planes, and command set must match the purchased module.

1. Prove power and reset timing.
   Check panel power, reset pulse, busy pin level, and required delays before SPI commands.

1. Send a minimal pattern.
   Render full white, full black, and checkerboard before fonts or images.

1. Validate framebuffer layout.
   Confirm bit order, row stride, rotation, black/red planes, and RAM window commands.

1. Add refresh policy.
   Separate full refresh, partial refresh, deep sleep, and wake-up flows.

1. Measure low-power behavior.
   Confirm panel sleep command, rail shutdown, and MCU pin states after update.

## Common Failures

- Driver targets a similar-looking panel with different controller or LUT.
- Busy pin polarity is wrong or not waited long enough.
- SPI DC/CS timing is violated during command/data transitions.
- Image is mirrored because bit order or RAM direction is wrong.
- Partial refresh causes ghosting because periodic full refresh is missing.
- Deep sleep requires a full reinitialization before the next update.

## Verification

Before claiming EPD works:

- State exact panel, controller, resolution, color planes, and refresh mode.
- Confirm solid black, solid white, and checkerboard output.
- Confirm busy timing and full refresh completion.
- Confirm partial refresh limitations and deep-sleep current if relevant.

## Example

User:

```text
墨水屏偶尔 busy 一直不释放。
```

Agent:

1. Checks panel part number, busy polarity, reset timing, and power rails.
1. Compares init sequence with the vendor demo for the exact controller.
1. Tests full-refresh-only path before enabling partial refresh or sleep.
