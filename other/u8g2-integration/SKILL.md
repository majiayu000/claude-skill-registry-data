---
name: u8g2-integration
description: Use when integrating, porting, configuring, or debugging U8g2 displays, OLED/LCD drivers, I2C/SPI callbacks, fonts, frame buffers, or monochrome embedded UI
---

# U8g2 Integration

## Overview

Use this skill to integrate U8g2 by proving display controller wiring, bus callbacks, reset timing, buffer mode, and font memory before debugging drawing code. Small display failures are usually port or bus issues first.

## When To Use

Use this skill when:

- The user wants U8g2/U8glib-style graphics on OLED/LCD modules.
- The issue involves blank display, wrong orientation, I2C/SPI failures, font size, page buffer mode, or slow refresh.
- The target uses SSD1306, SH1106, ST7565, ST7920, or similar small display controllers.

Do not use this skill for full GUI stacks like LVGL. Use `lvgl-integration` when widgets and input devices dominate.

## First Questions

Ask for:

- Display controller, resolution, interface, address/CS/DC/RST pins, and voltage level.
- MCU, driver/HAL, RTOS/bare-metal model, and U8g2 constructor/setup function.
- Buffer mode: full buffer, page buffer, or 1-page mode.
- Font, text language requirements, and flash/RAM budget.
- Current symptom and whether bus-level signals were measured.

## Integration Checklist

1. Confirm hardware path.
   Check power, reset, I2C/SPI wiring, address, CS/DC pins, and logic levels.

1. Select exact constructor.
   Controller, resolution, rotation, and interface must match the panel.

1. Implement bus callbacks.
   Byte and GPIO/delay callbacks must drive I2C/SPI and reset timing correctly.

1. Choose buffer mode.
   Full buffer is simpler but uses RAM; page mode needs correct drawing loop.

1. Test minimal draw.
   Draw a box or text with a small font before custom UI.

## Common Failures

- SH1106 panel treated as SSD1306.
- I2C address shifted incorrectly.
- Page buffer mode used without first/next page loop.
- Reset pin not toggled or delay too short.
- Font tables exceed flash budget.
- SPI DC/CS pins swapped or not controlled by callbacks.

## Verification

Before claiming U8g2 works:

- State controller, resolution, interface, pins, constructor, and buffer mode.
- Confirm bus scan or measured bus traffic when possible.
- Confirm minimal draw and orientation.
- Confirm RAM/flash impact of chosen buffer and fonts.

## Example

User:

```text
U8g2 驱动 OLED 一直黑屏。
```

Agent:

1. Asks for controller, constructor, I2C/SPI pins, reset pin, address, and buffer mode.
1. Checks hardware and bus callback before drawing code.
1. Tests a minimal box/text draw with the correct page loop.
