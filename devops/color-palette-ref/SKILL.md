---
name: color-palette-ref
description: APC Mini MK2 color palette reference with velocity values and custom RGB via SysEx. Use when user asks about "color", "velocity value", "RGB", "palette", "brightness", "LED color", or needs to set specific colors on the APC Mini MK2.
---

# APC Mini MK2 Color Palette Reference

Complete reference for the 128-color velocity palette and custom RGB control.

## Primary Colors (Quick Reference)

| Color | Velocity | Hex | Approximate RGB |
|-------|----------|-----|-----------------|
| Off | 0 | 0x00 | - |
| White | 3 | 0x03 | #FFFFFF |
| Red | 5 | 0x05 | #FF0000 |
| Orange | 9 | 0x09 | #FF8000 |
| Yellow | 13 | 0x0D | #FFFF00 |
| Lime | 17 | 0x11 | #80FF00 |
| Green | 21 | 0x15 | #00FF00 |
| Mint | 29 | 0x1D | #00FF80 |
| Cyan | 33 | 0x21 | #00FFFF |
| Sky | 37 | 0x25 | #0080FF |
| Blue | 45 | 0x2D | #0000FF |
| Purple | 49 | 0x31 | #8000FF |
| Magenta | 53 | 0x35 | #FF00FF |
| Pink | 57 | 0x39 | #FF0080 |
| Hot Pink | 95 | 0x5F | #FF1493 |

## Extended Color Palette

### Reds (Velocity 1-8)
| Velocity | Hex | Description |
|----------|-----|-------------|
| 1 | 0x01 | Dark Red |
| 2 | 0x02 | Red-Orange Dark |
| 3 | 0x03 | White/Warm |
| 4 | 0x04 | Light Red |
| 5 | 0x05 | **Red** |
| 6 | 0x06 | Red-Orange |
| 7 | 0x07 | Orange-Red |
| 8 | 0x08 | Dark Orange |

### Oranges/Yellows (Velocity 9-16)
| Velocity | Hex | Description |
|----------|-----|-------------|
| 9 | 0x09 | **Orange** |
| 10 | 0x0A | Light Orange |
| 11 | 0x0B | Amber |
| 12 | 0x0C | Yellow-Orange |
| 13 | 0x0D | **Yellow** |
| 14 | 0x0E | Light Yellow |
| 15 | 0x0F | Pale Yellow |
| 16 | 0x10 | Yellow-Green |

### Greens (Velocity 17-28)
| Velocity | Hex | Description |
|----------|-----|-------------|
| 17 | 0x11 | Lime |
| 18 | 0x12 | Yellow-Green |
| 19 | 0x13 | Light Green |
| 20 | 0x14 | Pale Green |
| 21 | 0x15 | **Green** |
| 22 | 0x16 | Green Dark |
| 23 | 0x17 | Forest Green |
| 24 | 0x18 | Teal-Green |
| 25 | 0x19 | Sea Green |
| 26 | 0x1A | Aqua-Green |
| 27 | 0x1B | Turquoise |
| 28 | 0x1C | Cyan-Green |

### Cyans/Blues (Velocity 29-48)
| Velocity | Hex | Description |
|----------|-----|-------------|
| 29 | 0x1D | Mint |
| 30 | 0x1E | Aqua |
| 31 | 0x1F | Light Cyan |
| 32 | 0x20 | Pale Cyan |
| 33 | 0x21 | **Cyan** |
| 37 | 0x25 | Sky Blue |
| 41 | 0x29 | Light Blue |
| 45 | 0x2D | **Blue** |

### Purples/Magentas (Velocity 49-64)
| Velocity | Hex | Description |
|----------|-----|-------------|
| 49 | 0x31 | **Purple** |
| 50 | 0x32 | Violet |
| 51 | 0x33 | Lavender |
| 52 | 0x34 | Light Purple |
| 53 | 0x35 | **Magenta** |
| 54 | 0x36 | Pink-Magenta |
| 55 | 0x37 | Hot Pink |
| 56 | 0x38 | Deep Pink |
| 57 | 0x39 | Pink |

## Brightness Control via MIDI Channel

The same velocity color appears at different brightness levels:

| Channel | Brightness | Usage |
|---------|------------|-------|
| 0 | 10% | Very dim |
| 1 | 25% | Dim |
| 2 | 40% | Low |
| 3 | 55% | Medium-Low |
| 4 | 70% | Medium |
| 5 | 85% | High |
| 6 | 100% | **Full** (recommended) |

Example: Red at different brightness levels
```typescript
output.send('noteon', { note: 0, velocity: 5, channel: 0 }); // 10% red
output.send('noteon', { note: 0, velocity: 5, channel: 3 }); // 55% red
output.send('noteon', { note: 0, velocity: 5, channel: 6 }); // 100% red
```

## Animation Effects via MIDI Channel

| Channel | Effect | Rate |
|---------|--------|------|
| 7 | Pulse | 1/16 note |
| 8 | Pulse | 1/8 note |
| 9 | Pulse | 1/4 note |
| 10 | Pulse | 1/2 note |
| 11 | Blink | 1/24 note |
| 12 | Blink | 1/16 note |
| 13 | Blink | 1/8 note |
| 14 | Blink | 1/4 note |
| 15 | Blink | 1/2 note |

Example: Pulsing red
```typescript
output.send('noteon', { note: 0, velocity: 5, channel: 9 }); // Red pulse 1/4
```

## Custom RGB via SysEx

For precise color control beyond the 128-color palette:

### SysEx Message Format
```
F0 47 7F 4F 24 00 08 [pad] [pad] [R-MSB] [R-LSB] [G-MSB] [G-LSB] [B-MSB] [B-LSB] F7
```

### RGB Encoding Function
```typescript
function encodeRGB(value: number): [number, number] {
  // Split 8-bit value into MSB (bit 7) and LSB (bits 0-6)
  const msb = (value >> 7) & 0x01;
  const lsb = value & 0x7F;
  return [msb, lsb];
}
```

### Complete Custom RGB Function
```typescript
function setCustomRGB(
  output: Output,
  pad: number,
  r: number,
  g: number,
  b: number
) {
  const [rMSB, rLSB] = encodeRGB(r);
  const [gMSB, gLSB] = encodeRGB(g);
  const [bMSB, bLSB] = encodeRGB(b);

  output.send('sysex', [
    0xF0,                   // SysEx start
    0x47,                   // Akai manufacturer ID
    0x7F,                   // Device broadcast
    0x4F,                   // APC Mini MK2 product ID
    0x24,                   // RGB LED command
    0x00, 0x08,             // Length (8 bytes)
    pad, pad,               // Start/end pad (single pad)
    rMSB, rLSB,             // Red
    gMSB, gLSB,             // Green
    bMSB, bLSB,             // Blue
    0xF7                    // SysEx end
  ]);
}
```

### Range RGB (Multiple Pads)
```typescript
function setRangeRGB(
  output: Output,
  startPad: number,
  endPad: number,
  r: number,
  g: number,
  b: number
) {
  const [rMSB, rLSB] = encodeRGB(r);
  const [gMSB, gLSB] = encodeRGB(g);
  const [bMSB, bLSB] = encodeRGB(b);

  output.send('sysex', [
    0xF0, 0x47, 0x7F, 0x4F, 0x24,
    0x00, 0x08,
    startPad, endPad,       // Range of pads
    rMSB, rLSB,
    gMSB, gLSB,
    bMSB, bLSB,
    0xF7
  ]);
}
```

## Common Color Examples

```typescript
// Primary colors
setCustomRGB(output, 0, 255, 0, 0);     // Red
setCustomRGB(output, 1, 0, 255, 0);     // Green
setCustomRGB(output, 2, 0, 0, 255);     // Blue

// Secondary colors
setCustomRGB(output, 3, 255, 255, 0);   // Yellow
setCustomRGB(output, 4, 0, 255, 255);   // Cyan
setCustomRGB(output, 5, 255, 0, 255);   // Magenta

// Pastels
setCustomRGB(output, 6, 255, 182, 193); // Light Pink
setCustomRGB(output, 7, 173, 216, 230); // Light Blue

// Brand colors
setCustomRGB(output, 8, 29, 185, 84);   // Spotify Green
setCustomRGB(output, 9, 255, 69, 0);    // SoundCloud Orange
```

## Peripheral Button Colors

Track and Scene buttons have fixed colors:

| Button Type | LED Color | On Velocity | Blink Velocity |
|-------------|-----------|-------------|----------------|
| Track 1-8 | Red | 1 | 2 |
| Scene 1-8 | Green | 1 | 2 |

```typescript
// Track button on
output.send('noteon', { note: 100, velocity: 1, channel: 0 });

// Scene button blinking
output.send('noteon', { note: 112, velocity: 2, channel: 0 });
```
