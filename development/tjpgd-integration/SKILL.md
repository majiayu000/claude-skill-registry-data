---
name: tjpgd-integration
description: Use when integrating, porting, or debugging TJpgDec, Tiny JPEG Decompressor, embedded JPEG decoding, MCU image assets, display callbacks, or memory-constrained rendering
---

# TJpgDec Integration

## Overview

Use this skill to integrate TJpgDec by proving the input callback, output callback, work buffer, color format, scaling, and display path. TJpgDec is small, but it still needs careful ownership of input streams and pixel blocks.

## When To Use

Use this skill when:

- The user wants JPEG decoding on MCUs, small displays, LVGL image pipelines, or resource-constrained embedded systems.
- The issue involves decode errors, wrong colors, cropped images, slow rendering, memory faults, or display block callbacks.
- The project stores JPEGs in flash, filesystem, SD card, OTA resources, or network streams.

Do not use this skill when the display driver itself is not proven. Use `lvgl-integration`, `u8g2-integration`, or `epd-integration` as appropriate.

## First Questions

Ask for:

- TJpgDec version or wrapper library, target MCU, RAM budget, and compiler.
- JPEG dimensions, subsampling, color format, progressive/baseline status, and asset source.
- Input storage path, read callback, seek/skip support, and chunk size.
- Output target: framebuffer, display flush, LVGL canvas, EPD buffer, or file.
- Current error code, work buffer size, and failing image sample.

## Integration Checklist

1. Validate the JPEG format.
   Confirm baseline JPEG support and reject unsupported progressive or oversized images.

1. Prove input callback semantics.
   Reads, skips, short reads, and EOF must match TJpgDec expectations.

1. Allocate the work buffer deliberately.
   Keep the buffer aligned and sized for the selected build and platform.

1. Match output color.
   Convert RGB/BGR, RGB565 endian, grayscale, and alpha assumptions at the output boundary.

1. Clip and scale safely.
   Handle destination rectangles, scaling factors, and display bounds before pushing pixels.

1. Test multiple asset shapes.
   Include tiny, wide, tall, odd-sized, and maximum-resolution images.

## Common Failures

- Using progressive JPEGs that the decoder does not support.
- Output callback writes past display or framebuffer bounds.
- RGB565 byte order is swapped.
- Input callback cannot skip bytes correctly for filesystem streams.
- Work buffer lives on a small task stack.
- Decoding blocks the UI or watchdog for too long.

## Verification

Before claiming JPEG decode works:

- State JPEG format limits, work buffer size, and output color format.
- Confirm one known-good image renders correctly.
- Confirm unsupported, truncated, and oversized images fail safely.
- Confirm display bounds and watchdog behavior.

## Example

User:

```text
TJpgDec 图片能解码但颜色不对。
```

Agent:

1. Checks output format, RGB/BGR order, and RGB565 endian.
1. Renders a small color-bar JPEG through the same callback.
1. Fixes conversion at the output boundary instead of changing asset data first.
