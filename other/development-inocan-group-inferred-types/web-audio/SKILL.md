---
name: web-audio
description: Use when working with Web Audio API. Applies AudioContext management, signal routing, AudioWorklet patterns, and audio cleanup best practices.
version: "1.0.0"
---

# Web Audio Best Practices

Apply when building audio features with the Web Audio API.

**Documentation:** https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API

## AudioContext Management

### Singleton Pattern

Share a single AudioContext across the application:

```javascript
let ctx = null;

export function getAudioContext() {
  if (!ctx) {
    ctx = new (window.AudioContext || window.webkitAudioContext)();
  }
  return ctx;
}

export async function ensureRunning() {
  const audioCtx = getAudioContext();
  if (audioCtx.state === 'suspended') {
    await audioCtx.resume();
  }
  return audioCtx;
}
```

### iOS/Safari Unlock

AudioContext must be resumed after a user gesture on iOS:

```javascript
// Unlock on first user interaction
function unlockAudio() {
  ensureRunning().then(() => {
    document.removeEventListener('touchstart', unlockAudio);
    document.removeEventListener('click', unlockAudio);
  });
}

document.addEventListener('touchstart', unlockAudio, { once: true });
document.addEventListener('click', unlockAudio, { once: true });
```

## Signal Flow

### Basic Node Chain

```
Source → Gain → Filter → Destination
```

```javascript
const ctx = getAudioContext();

// Create nodes
const source = ctx.createBufferSource();
const gain = ctx.createGain();
const filter = ctx.createBiquadFilter();

// Connect chain (returns destination for chaining)
source.connect(gain).connect(filter).connect(ctx.destination);

// Configure nodes
gain.gain.value = 0.8;
filter.type = 'lowpass';
filter.frequency.value = 2000;

// Start playback
source.buffer = audioBuffer;
source.start();
```

### Parallel Routing (Dry/Wet Mix)

```
              ┌──→ Dry Gain ──────→┐
Source → Split│                    ├──→ Master → Destination
              └──→ Effect → Wet ──→┘
```

```javascript
// Dry/wet mix for reverb
const dryGain = ctx.createGain();
const wetGain = ctx.createGain();
const convolver = ctx.createConvolver();

source.connect(dryGain).connect(masterGain);
source.connect(convolver).connect(wetGain).connect(masterGain);

// Control mix (0 = dry, 1 = wet)
function setWetMix(amount) {
  dryGain.gain.value = 1 - amount;
  wetGain.gain.value = amount;
}
```

### Send/Return Pattern

```javascript
// Create reverb send
const reverbSend = ctx.createGain();
const reverb = ctx.createConvolver();
reverb.buffer = impulseResponse;

reverbSend.connect(reverb).connect(ctx.destination);

// Multiple sources can connect to the send
source1.connect(reverbSend);
source2.connect(reverbSend);

// Control send amount per source
const source1Send = ctx.createGain();
source1Send.gain.value = 0.3;  // 30% to reverb
source1.connect(source1Send).connect(reverbSend);
```

## AudioWorklet

### When to Use

- Real-time audio processing on audio thread
- Avoid main thread blocking for audio
- Sample-accurate timing
- Custom DSP algorithms

**Requires HTTPS** (or localhost for development).

### Processor (Runs on Audio Thread)

```javascript
// my-processor.js - Registered as AudioWorklet
class MyProcessor extends AudioWorkletProcessor {
  constructor() {
    super();
    this.phase = 0;
  }

  static get parameterDescriptors() {
    return [
      { name: 'frequency', defaultValue: 440, minValue: 20, maxValue: 20000 }
    ];
  }

  process(inputs, outputs, parameters) {
    const output = outputs[0];
    const frequency = parameters.frequency;

    for (let channel = 0; channel < output.length; channel++) {
      const outputChannel = output[channel];
      for (let i = 0; i < outputChannel.length; i++) {
        const freq = frequency.length > 1 ? frequency[i] : frequency[0];
        outputChannel[i] = Math.sin(this.phase);
        this.phase += (2 * Math.PI * freq) / sampleRate;
      }
    }

    return true;  // Keep processor alive
  }
}

registerProcessor('my-processor', MyProcessor);
```

### Main Thread Usage

```javascript
// Load and use the worklet
async function setupWorklet() {
  const ctx = getAudioContext();

  // Register processor module
  await ctx.audioWorklet.addModule('my-processor.js');

  // Create node
  const node = new AudioWorkletNode(ctx, 'my-processor');

  // Set parameters
  node.parameters.get('frequency').value = 880;

  // Communicate via MessagePort
  node.port.onmessage = (e) => {
    console.log('From worklet:', e.data);
  };
  node.port.postMessage({ command: 'start' });

  // Connect to output
  node.connect(ctx.destination);

  return node;
}
```

### Feature Detection & Fallback

```javascript
function isWorkletSupported() {
  return 'audioWorklet' in AudioContext.prototype &&
         (location.protocol === 'https:' || location.hostname === 'localhost');
}

async function createRecorder() {
  const ctx = getAudioContext();

  if (isWorkletSupported()) {
    // Modern path: AudioWorklet
    await ctx.audioWorklet.addModule('recorder-processor.js');
    return new AudioWorkletNode(ctx, 'recorder-processor');
  } else {
    // Fallback: ScriptProcessorNode (deprecated but widely supported)
    const processor = ctx.createScriptProcessor(4096, 1, 1);
    processor.onaudioprocess = (e) => {
      const samples = e.inputBuffer.getChannelData(0);
      // Process samples...
    };
    return processor;
  }
}
```

## Loading Audio

### Fetch and Decode

```javascript
async function loadAudioBuffer(url) {
  const ctx = getAudioContext();

  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to load audio: ${response.status}`);
  }

  const arrayBuffer = await response.arrayBuffer();
  return ctx.decodeAudioData(arrayBuffer);
}

// Usage
const buffer = await loadAudioBuffer('/audio/sample.mp3');
const source = ctx.createBufferSource();
source.buffer = buffer;
source.connect(ctx.destination);
source.start();
```

### With Loading State

```javascript
async function loadWithProgress(url, onProgress) {
  const response = await fetch(url);
  const contentLength = response.headers.get('Content-Length');
  const total = parseInt(contentLength, 10);

  const reader = response.body.getReader();
  const chunks = [];
  let loaded = 0;

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    chunks.push(value);
    loaded += value.length;
    onProgress?.(loaded / total);
  }

  const arrayBuffer = new Uint8Array(loaded);
  let position = 0;
  for (const chunk of chunks) {
    arrayBuffer.set(chunk, position);
    position += chunk.length;
  }

  const ctx = getAudioContext();
  return ctx.decodeAudioData(arrayBuffer.buffer);
}
```

## Parameter Automation

### Smooth Value Changes

```javascript
const gain = ctx.createGain();

// BAD: Instant change causes clicks
gain.gain.value = 0;

// GOOD: Smooth ramp over 50ms
const now = ctx.currentTime;
gain.gain.setTargetAtTime(0, now, 0.05);

// Or linear ramp
gain.gain.linearRampToValueAtTime(0, now + 0.05);
```

### Scheduling

```javascript
const osc = ctx.createOscillator();

// Schedule frequency changes
const now = ctx.currentTime;
osc.frequency.setValueAtTime(440, now);
osc.frequency.linearRampToValueAtTime(880, now + 1);  // Slide to 880Hz over 1s
osc.frequency.setValueAtTime(440, now + 2);           // Jump back

// Schedule start/stop
osc.start(now);
osc.stop(now + 3);
```

## Cleanup

### Node Disposal

Always disconnect and dereference nodes when done:

```javascript
class AudioEffect {
  constructor(ctx) {
    this.ctx = ctx;
    this.source = null;
    this.gain = ctx.createGain();
    this.filter = ctx.createBiquadFilter();

    this.gain.connect(this.filter).connect(ctx.destination);
  }

  play(buffer) {
    // Stop previous if playing
    this.stop();

    this.source = this.ctx.createBufferSource();
    this.source.buffer = buffer;
    this.source.connect(this.gain);
    this.source.start();

    // Clean up when finished
    this.source.onended = () => {
      this.source?.disconnect();
      this.source = null;
    };
  }

  stop() {
    if (this.source) {
      this.source.stop();
      this.source.disconnect();
      this.source = null;
    }
  }

  dispose() {
    this.stop();
    this.filter.disconnect();
    this.gain.disconnect();
    this.filter = null;
    this.gain = null;
  }
}
```

### BufferSource Reuse

`AudioBufferSourceNode` is single-use. Create new ones for each playback:

```javascript
// BAD: Trying to reuse source
const source = ctx.createBufferSource();
source.buffer = buffer;
source.start();
source.start();  // Error! Already started

// GOOD: Create new source each time
function playSound(buffer) {
  const source = ctx.createBufferSource();
  source.buffer = buffer;
  source.connect(ctx.destination);
  source.start();
  source.onended = () => source.disconnect();
}
```

## Common Issues

### Click/Pop Prevention

```javascript
// Fade in/out to avoid clicks
function fadeIn(gainNode, duration = 0.05) {
  const now = gainNode.context.currentTime;
  gainNode.gain.setValueAtTime(0, now);
  gainNode.gain.linearRampToValueAtTime(1, now + duration);
}

function fadeOut(gainNode, duration = 0.05) {
  const now = gainNode.context.currentTime;
  gainNode.gain.setValueAtTime(gainNode.gain.value, now);
  gainNode.gain.linearRampToValueAtTime(0, now + duration);
}
```

### Timing Precision

```javascript
// BAD: JavaScript timing (imprecise)
setTimeout(() => source.start(), 1000);

// GOOD: Web Audio scheduling (sample-accurate)
source.start(ctx.currentTime + 1);
```

### Memory Leaks

```javascript
// BAD: Nodes accumulate without cleanup
function playNote() {
  const osc = ctx.createOscillator();
  osc.connect(ctx.destination);
  osc.start();
  osc.stop(ctx.currentTime + 0.5);
  // Oscillator never disconnected!
}

// GOOD: Clean up after playback
function playNote() {
  const osc = ctx.createOscillator();
  osc.connect(ctx.destination);
  osc.start();
  osc.stop(ctx.currentTime + 0.5);
  osc.onended = () => osc.disconnect();
}
```

## Avoid

- Creating multiple AudioContexts (use singleton)
- Setting gain.value directly during playback (use ramps)
- Forgetting to disconnect nodes (causes memory leaks)
- Using setTimeout for audio timing (use ctx.currentTime)
- Reusing AudioBufferSourceNode (create new each time)
- Forgetting iOS unlock (resume on user gesture)
- Skipping HTTPS for AudioWorklet (feature detection!)
