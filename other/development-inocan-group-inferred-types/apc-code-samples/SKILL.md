---
name: apc-code-samples
description: TypeScript and Node.js code samples for APC Mini MK2 development. Use when user needs "code example", "implementation", "easymidi", "@julusian/midi", "sample code", "how to implement", or wants working code for LED control, button handling, or MIDI communication.
---

# APC Mini MK2 Code Samples

Complete TypeScript/Node.js implementation examples for APC Mini MK2.

## Library Setup

### Using easymidi (Recommended for Rapid Development)

```bash
npm install easymidi
npm install -D @types/easymidi
```

```typescript
import easymidi from 'easymidi';

// List available MIDI devices
console.log('Inputs:', easymidi.getInputs());
console.log('Outputs:', easymidi.getOutputs());

// Connect to APC Mini MK2
const output = new easymidi.Output('APC mini mk2');
const input = new easymidi.Input('APC mini mk2');
```

### Using @julusian/midi (Recommended for Production)

```bash
npm install @julusian/midi
```

```typescript
import midi from '@julusian/midi';

// List available devices
const output = new midi.Output();
const input = new midi.Input();

console.log('Output ports:', output.getPortCount());
for (let i = 0; i < output.getPortCount(); i++) {
  console.log(`  ${i}: ${output.getPortName(i)}`);
}

// Open port by name
function openOutputByName(name: string): midi.Output {
  const out = new midi.Output();
  for (let i = 0; i < out.getPortCount(); i++) {
    if (out.getPortName(i).includes(name)) {
      out.openPort(i);
      return out;
    }
  }
  throw new Error(`Device "${name}" not found`);
}

const apcOutput = openOutputByName('APC mini');
```

## Basic LED Control

### Set Single Pad Color (easymidi)

```typescript
import easymidi from 'easymidi';

const output = new easymidi.Output('APC mini mk2');

// Set pad 0 to red at full brightness
output.send('noteon', {
  note: 0,
  velocity: 5,    // Red
  channel: 6      // 100% brightness
});

// Turn off pad
output.send('noteon', {
  note: 0,
  velocity: 0,
  channel: 0
});
```

### Set Single Pad Color (@julusian/midi)

```typescript
import midi from '@julusian/midi';

const output = new midi.Output();
output.openPort(0);

// Set pad 0 to red at full brightness
// Status byte: 0x96 = Note On, Channel 6
output.sendMessage([0x96, 0x00, 0x05]);

// Turn off pad
output.sendMessage([0x90, 0x00, 0x00]);
```

## Complete APC Mini MK2 Class

```typescript
import easymidi from 'easymidi';

interface PadOptions {
  brightness?: number;  // 0-6 for solid, 7-10 pulse, 11-15 blink
  color: number;        // 0-127 velocity
}

class APCMiniMK2 {
  private output: easymidi.Output;
  private input: easymidi.Input;

  constructor() {
    this.output = new easymidi.Output('APC mini mk2');
    this.input = new easymidi.Input('APC mini mk2');
  }

  // Pad control (0-63)
  setPad(pad: number, options: PadOptions): void {
    const channel = options.brightness ?? 6;
    this.output.send('noteon', {
      note: pad,
      velocity: options.color,
      channel
    });
  }

  setPadOff(pad: number): void {
    this.output.send('noteon', { note: pad, velocity: 0, channel: 0 });
  }

  // Set pad by coordinate (1-indexed)
  setPadAt(row: number, col: number, options: PadOptions): void {
    const note = (row - 1) * 8 + (col - 1);
    this.setPad(note, options);
  }

  // Custom RGB via SysEx
  setPadRGB(pad: number, r: number, g: number, b: number): void {
    const encode = (v: number) => [(v >> 7) & 0x01, v & 0x7F];
    const [rMSB, rLSB] = encode(r);
    const [gMSB, gLSB] = encode(g);
    const [bMSB, bLSB] = encode(b);

    this.output.send('sysex', [
      0xF0, 0x47, 0x7F, 0x4F, 0x24,
      0x00, 0x08,
      pad, pad,
      rMSB, rLSB, gMSB, gLSB, bMSB, bLSB,
      0xF7
    ]);
  }

  // Track buttons (100-107)
  setTrackButton(track: number, state: 'off' | 'on' | 'blink'): void {
    const note = 99 + track; // track 1 = note 100
    const velocity = state === 'off' ? 0 : state === 'on' ? 1 : 2;
    this.output.send('noteon', { note, velocity, channel: 0 });
  }

  // Scene buttons (112-119)
  setSceneButton(scene: number, state: 'off' | 'on' | 'blink'): void {
    const note = 111 + scene; // scene 1 = note 112
    const velocity = state === 'off' ? 0 : state === 'on' ? 1 : 2;
    this.output.send('noteon', { note, velocity, channel: 0 });
  }

  // Clear all LEDs
  clearAll(): void {
    // Clear pads
    for (let i = 0; i < 64; i++) {
      this.setPadOff(i);
    }
    // Clear track buttons
    for (let i = 1; i <= 8; i++) {
      this.setTrackButton(i, 'off');
    }
    // Clear scene buttons
    for (let i = 1; i <= 8; i++) {
      this.setSceneButton(i, 'off');
    }
  }

  // Event handlers
  onPadPress(callback: (pad: number, velocity: number) => void): void {
    this.input.on('noteon', (msg) => {
      if (msg.note < 64 && msg.velocity > 0) {
        callback(msg.note, msg.velocity);
      }
    });
  }

  onPadRelease(callback: (pad: number) => void): void {
    this.input.on('noteoff', (msg) => {
      if (msg.note < 64) {
        callback(msg.note);
      }
    });
  }

  onTrackButton(callback: (track: number, pressed: boolean) => void): void {
    this.input.on('noteon', (msg) => {
      if (msg.note >= 100 && msg.note <= 107) {
        callback(msg.note - 99, msg.velocity > 0);
      }
    });
  }

  onSceneButton(callback: (scene: number, pressed: boolean) => void): void {
    this.input.on('noteon', (msg) => {
      if (msg.note >= 112 && msg.note <= 119) {
        callback(msg.note - 111, msg.velocity > 0);
      }
    });
  }

  onFader(callback: (fader: number, value: number) => void): void {
    this.input.on('cc', (msg) => {
      if (msg.controller >= 48 && msg.controller <= 56) {
        callback(msg.controller - 47, msg.value);
      }
    });
  }

  close(): void {
    this.input.close();
    this.output.close();
  }
}

export { APCMiniMK2, PadOptions };
```

## Usage Examples

### Basic Pad Lighting

```typescript
const apc = new APCMiniMK2();

// Light pad 0 red
apc.setPad(0, { color: 5 });

// Light pad at row 3, column 4 green
apc.setPadAt(3, 4, { color: 21 });

// Light pad with pulse animation
apc.setPad(10, { color: 45, brightness: 9 }); // Blue, pulse 1/4

// Custom RGB
apc.setPadRGB(20, 255, 128, 0); // Orange
```

### Rainbow Pattern

```typescript
const apc = new APCMiniMK2();

const rainbowColors = [5, 9, 13, 21, 33, 45, 49, 53];

function showRainbow() {
  for (let row = 0; row < 8; row++) {
    for (let col = 0; col < 8; col++) {
      const note = row * 8 + col;
      const color = rainbowColors[(row + col) % 8];
      apc.setPad(note, { color });
    }
  }
}

showRainbow();
```

### Interactive Button Handler

```typescript
const apc = new APCMiniMK2();
const padStates = new Map<number, boolean>();

apc.onPadPress((pad, velocity) => {
  const isOn = padStates.get(pad) ?? false;

  if (isOn) {
    apc.setPadOff(pad);
    padStates.set(pad, false);
  } else {
    apc.setPad(pad, { color: 5 }); // Red
    padStates.set(pad, true);
  }
});

// Scene buttons control rows
apc.onSceneButton((scene, pressed) => {
  if (pressed) {
    const row = 9 - scene; // Scene 1 = Row 8
    for (let col = 0; col < 8; col++) {
      const note = (row - 1) * 8 + col;
      apc.setPad(note, { color: 21 }); // Green
    }
  }
});

// Fader controls brightness
let currentBrightness = 6;
apc.onFader((fader, value) => {
  if (fader === 9) { // Master fader
    currentBrightness = Math.floor(value / 127 * 6);
    console.log('Brightness:', currentBrightness);
  }
});
```

### Sequencer-Style Animation

```typescript
const apc = new APCMiniMK2();

let currentStep = 0;
const BPM = 120;
const stepTime = (60 / BPM) * 1000 / 4; // 16th notes

function animate() {
  // Clear previous step
  const prevStep = (currentStep - 1 + 8) % 8;
  for (let row = 0; row < 8; row++) {
    apc.setPadOff(row * 8 + prevStep);
  }

  // Light current step
  for (let row = 0; row < 8; row++) {
    apc.setPad(row * 8 + currentStep, { color: 5 }); // Red
  }

  currentStep = (currentStep + 1) % 8;
}

setInterval(animate, stepTime);

// Cleanup on exit
process.on('SIGINT', () => {
  apc.clearAll();
  apc.close();
  process.exit();
});
```

### Gradient Fill

```typescript
function fillGradient(apc: APCMiniMK2, startR: number, startG: number, startB: number,
                      endR: number, endG: number, endB: number) {
  for (let i = 0; i < 64; i++) {
    const t = i / 63;
    const r = Math.round(startR + (endR - startR) * t);
    const g = Math.round(startG + (endG - startG) * t);
    const b = Math.round(startB + (endB - startB) * t);
    apc.setPadRGB(i, r, g, b);
  }
}

// Red to Blue gradient
fillGradient(apc, 255, 0, 0, 0, 0, 255);
```

## Error Handling

```typescript
import easymidi from 'easymidi';

function connectToAPC(): { input: easymidi.Input; output: easymidi.Output } | null {
  const inputs = easymidi.getInputs();
  const outputs = easymidi.getOutputs();

  const inputName = inputs.find(n => n.includes('APC mini'));
  const outputName = outputs.find(n => n.includes('APC mini'));

  if (!inputName || !outputName) {
    console.error('APC Mini MK2 not found');
    console.log('Available inputs:', inputs);
    console.log('Available outputs:', outputs);
    return null;
  }

  try {
    const input = new easymidi.Input(inputName);
    const output = new easymidi.Output(outputName);
    console.log('Connected to APC Mini MK2');
    return { input, output };
  } catch (error) {
    console.error('Failed to connect:', error);
    return null;
  }
}
```

## TypeScript Interfaces

```typescript
// Color definitions
const Colors = {
  OFF: 0,
  WHITE: 3,
  RED: 5,
  ORANGE: 9,
  YELLOW: 13,
  LIME: 17,
  GREEN: 21,
  MINT: 29,
  CYAN: 33,
  SKY: 37,
  BLUE: 45,
  PURPLE: 49,
  MAGENTA: 53,
  PINK: 57,
} as const;

type ColorName = keyof typeof Colors;

// Brightness/Animation channels
const Channels = {
  DIM_10: 0,
  DIM_25: 1,
  DIM_40: 2,
  DIM_55: 3,
  DIM_70: 4,
  DIM_85: 5,
  FULL: 6,
  PULSE_16: 7,
  PULSE_8: 8,
  PULSE_4: 9,
  PULSE_2: 10,
  BLINK_24: 11,
  BLINK_16: 12,
  BLINK_8: 13,
  BLINK_4: 14,
  BLINK_2: 15,
} as const;

type ChannelName = keyof typeof Channels;

// Button states
type ButtonState = 'off' | 'on' | 'blink';

// Note mappings
const Notes = {
  PAD_MIN: 0,
  PAD_MAX: 63,
  TRACK_MIN: 100,
  TRACK_MAX: 107,
  SCENE_MIN: 112,
  SCENE_MAX: 119,
  SHIFT: 122,
} as const;

export { Colors, Channels, Notes, ColorName, ChannelName, ButtonState };
```
