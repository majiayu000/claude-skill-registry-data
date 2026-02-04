---
name: led-mapping-guide
description: Visual guide for APC Mini MK2 LED and button mapping. Use when user needs to know "which button", "pad location", "LED position", "coordinate to note", "note to coordinate", or wants to understand the physical layout of the controller.
---

# APC Mini MK2 LED Mapping Guide

Visual reference for button positions and their corresponding MIDI note numbers.

## Physical Layout Overview

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│  [SHIFT]                              [SCENE 1-8]   │
│                                         112-119     │
│  ┌───┬───┬───┬───┬───┬───┬───┬───┐    ┌───┐       │
│  │56 │57 │58 │59 │60 │61 │62 │63 │    │112│ Row 8  │
│  ├───┼───┼───┼───┼───┼───┼───┼───┤    ├───┤       │
│  │48 │49 │50 │51 │52 │53 │54 │55 │    │113│ Row 7  │
│  ├───┼───┼───┼───┼───┼───┼───┼───┤    ├───┤       │
│  │40 │41 │42 │43 │44 │45 │46 │47 │    │114│ Row 6  │
│  ├───┼───┼───┼───┼───┼───┼───┼───┤    ├───┤       │
│  │32 │33 │34 │35 │36 │37 │38 │39 │    │115│ Row 5  │
│  ├───┼───┼───┼───┼───┼───┼───┼───┤    ├───┤       │
│  │24 │25 │26 │27 │28 │29 │30 │31 │    │116│ Row 4  │
│  ├───┼───┼───┼───┼───┼───┼───┼───┤    ├───┤       │
│  │16 │17 │18 │19 │20 │21 │22 │23 │    │117│ Row 3  │
│  ├───┼───┼───┼───┼───┼───┼───┼───┤    ├───┤       │
│  │ 8 │ 9 │10 │11 │12 │13 │14 │15 │    │118│ Row 2  │
│  ├───┼───┼───┼───┼───┼───┼───┼───┤    ├───┤       │
│  │ 0 │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │    │119│ Row 1  │
│  └───┴───┴───┴───┴───┴───┴───┴───┘    └───┘       │
│   C1  C2  C3  C4  C5  C6  C7  C8                   │
│                                                     │
│  ┌───┬───┬───┬───┬───┬───┬───┬───┐                │
│  │100│101│102│103│104│105│106│107│  [TRACK 1-8]   │
│  └───┴───┴───┴───┴───┴───┴───┴───┘                │
│                                                     │
│  ════════════════════════════════  [FADERS 1-9]    │
│   F1  F2  F3  F4  F5  F6  F7  F8  F9(Master)       │
│  CC48 CC49 CC50 CC51 CC52 CC53 CC54 CC55 CC56      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Pad Grid Mapping (Notes 0-63)

8x8 RGB pad matrix with full color support:

| Row | Col 1 | Col 2 | Col 3 | Col 4 | Col 5 | Col 6 | Col 7 | Col 8 |
|-----|-------|-------|-------|-------|-------|-------|-------|-------|
| 8 | 56 | 57 | 58 | 59 | 60 | 61 | 62 | 63 |
| 7 | 48 | 49 | 50 | 51 | 52 | 53 | 54 | 55 |
| 6 | 40 | 41 | 42 | 43 | 44 | 45 | 46 | 47 |
| 5 | 32 | 33 | 34 | 35 | 36 | 37 | 38 | 39 |
| 4 | 24 | 25 | 26 | 27 | 28 | 29 | 30 | 31 |
| 3 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 |
| 2 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
| 1 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |

## Coordinate Conversion Functions

```typescript
// Convert (row, column) to MIDI note (1-indexed coordinates)
function coordToNote(row: number, col: number): number {
  return (row - 1) * 8 + (col - 1);
}

// Convert MIDI note to (row, column) (1-indexed)
function noteToCoord(note: number): { row: number; col: number } {
  return {
    row: Math.floor(note / 8) + 1,
    col: (note % 8) + 1
  };
}

// Convert (x, y) to MIDI note (0-indexed coordinates)
function xyToNote(x: number, y: number): number {
  return y * 8 + x;
}

// Convert MIDI note to (x, y) (0-indexed)
function noteToXY(note: number): { x: number; y: number } {
  return {
    x: note % 8,
    y: Math.floor(note / 8)
  };
}
```

## Track Buttons (Notes 100-107)

Bottom row, single-color **red** LEDs:

| Button | Track 1 | Track 2 | Track 3 | Track 4 | Track 5 | Track 6 | Track 7 | Track 8 |
|--------|---------|---------|---------|---------|---------|---------|---------|---------|
| Note | 100 | 101 | 102 | 103 | 104 | 105 | 106 | 107 |
| Hex | 0x64 | 0x65 | 0x66 | 0x67 | 0x68 | 0x69 | 0x6A | 0x6B |

Velocity values:
- `0` = Off
- `1` = On
- `2` = Blink

## Scene Launch Buttons (Notes 112-119)

Right column, single-color **green** LEDs:

| Button | Scene 1 | Scene 2 | Scene 3 | Scene 4 | Scene 5 | Scene 6 | Scene 7 | Scene 8 |
|--------|---------|---------|---------|---------|---------|---------|---------|---------|
| Note | 112 | 113 | 114 | 115 | 116 | 117 | 118 | 119 |
| Hex | 0x70 | 0x71 | 0x72 | 0x73 | 0x74 | 0x75 | 0x76 | 0x77 |
| Row | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 |

Velocity values:
- `0` = Off
- `1` = On
- `2` = Blink

## Special Buttons

| Button | Note | Hex | LED |
|--------|------|-----|-----|
| Shift | 122 | 0x7A | None |

## LED Types by Region

| Region | Notes | LED Type | Colors |
|--------|-------|----------|--------|
| Pad Grid | 0-63 | RGB | 128 palette + custom RGB |
| Track | 100-107 | Single | Red only |
| Scene | 112-119 | Single | Green only |

## Common Patterns

### Light entire row
```typescript
function lightRow(output: Output, row: number, velocity: number) {
  for (let col = 0; col < 8; col++) {
    const note = (row - 1) * 8 + col;
    output.send('noteon', { note, velocity, channel: 6 });
  }
}
```

### Light entire column
```typescript
function lightColumn(output: Output, col: number, velocity: number) {
  for (let row = 0; row < 8; row++) {
    const note = row * 8 + (col - 1);
    output.send('noteon', { note, velocity, channel: 6 });
  }
}
```

### Light diagonal
```typescript
function lightDiagonal(output: Output, velocity: number) {
  for (let i = 0; i < 8; i++) {
    const note = i * 8 + i;
    output.send('noteon', { note, velocity, channel: 6 });
  }
}
```

### Clear all pads
```typescript
function clearAllPads(output: Output) {
  for (let note = 0; note < 64; note++) {
    output.send('noteon', { note, velocity: 0, channel: 0 });
  }
}
```
