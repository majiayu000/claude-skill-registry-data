---
name: audio-haptic-feedback
description: Use this skill whenever writing any audio cue, haptic signal, Web Audio API initialisation, or interaction feedback code in the Myelin simulator. This defines the complete audio event map, frequency values, Web Audio API implementation pattern, haptic signal contract, and the accessibility fallback requirements. Load this skill before writing any audio or haptic code.
---

This skill defines the audio and haptic feedback system for the Myelin simulator. Feedback is a critical part of the assessment experience — it communicates step completion, material properties, and mechanical state. Every audio cue in this skill is tied to a specific interaction event. Do not improvise frequencies or swap cues between events.

---

## Core Principle: Event-Driven, Not Proximity-Driven

All audio and haptic cues are triggered by specific interaction events dispatched through the simulation state machine. They are never triggered by:
- Distance to an object
- Animation frame position
- Timer-based polling

This ensures that feedback fires exactly when the assessed event occurs, with no timing drift.

---

## Audio System Initialisation

Use the Web Audio API exclusively for all simulator audio. Do not use `HTMLAudioElement` for latency-sensitive interaction cues — it has insufficient timing accuracy for sub-frame feedback.

```javascript
let audioContext = null;

function getAudioContext() {
  if (!audioContext) {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
  }
  // Resume suspended context — browsers suspend AudioContext until user gesture
  if (audioContext.state === 'suspended') {
    audioContext.resume();
  }
  return audioContext;
}
```

The `AudioContext` must be created or resumed inside a user gesture handler (click, keypress, pointer event). Do not create it on page load — modern browsers will suspend it immediately.

### Master gain node

```javascript
function createMasterGain() {
  const ctx = getAudioContext();
  const master = ctx.createGain();
  master.gain.value = 0.7;   // 70% master volume — leave headroom
  master.connect(ctx.destination);
  return master;
}
```

All audio nodes route through the master gain. Volume changes apply to `master.gain.value`.

---

## Audio Event Map

The complete list of interaction events and their audio signatures. Do not change these values — they are calibrated for material realism and assessment clarity.

| Event | Frequency | Duration | Shape | Notes |
|-------|-----------|----------|-------|-------|
| Valve rotation start | 400 Hz | 80ms | Decay | Material: cast iron creak transient |
| Valve rotation sustain | 200–380 Hz sweep | Variable | Sustain | Low rumble while rotating; pitch rises as resistance increases |
| Valve end-state snap (Step 2 pass) | 4200 Hz | 40ms | Sharp decay | Torque click — high-pitched mechanical seat engagement |
| Hasp proximity feedback | 800 Hz | 30ms | Soft decay | Subtle proximity ping — only fires once per approach |
| Hasp alignment snap (Step 3 pass) | 1850 Hz | 60ms | Medium decay | Connector snap — metallic click |
| Padlock shackle engagement (Step 4 pass) | 1200 Hz | 70ms | Medium decay | Spring engagement — mid-range click |
| Padlock fully locked | 2400 Hz | 50ms | Sharp decay | Secondary confirmation click |
| Step pass confirmation (generic) | 880 Hz + 1320 Hz | 120ms | Soft chord | Two-tone success — only on steps 1, 5, 7 (non-mechanical steps) |
| Step fail feedback | 220 Hz | 150ms | Decay | Low thud — communicates failure without alarm |
| Wrong-order interaction | 330 Hz | 100ms | Decay | Neutral correction tone — not alarming |
| Pressure confirmed zero (Step 6 pass) | 660 Hz | 200ms | Soft sustain | Hiss decay — evokes depressurisation |
| Session complete | 440 Hz + 554 Hz + 660 Hz | 600ms | Chord swell | Major chord completion fanfare |
| Session reset | 180 Hz | 80ms | Short decay | Neutral thud — scene returning to start |

### Prohibited audio behaviours

- Do not play audio on every physics update tick — only on state machine events
- Do not loop the valve rotation sustain indefinitely — it must stop within 100ms of the rotation stopping
- Do not play the Step pass confirmation chord on steps 2, 3, 4, 6 — those steps have mechanical-specific cues
- Do not play failure audio on wrong-order interactions — wrong-order uses the correction tone only

---

## Synthesised Audio Implementation

All audio in the simulator is synthesised in real time via Web Audio API oscillators and gain envelopes. Do not load audio files for interaction cues — synthesised audio has zero load time and precise timing.

### Tone player function

```javascript
function playTone(frequency, durationMs, options = {}) {
  const ctx  = getAudioContext();
  const master = options.masterGain || getMasterGain();

  const osc  = ctx.createOscillator();
  const gain = ctx.createGain();

  osc.connect(gain);
  gain.connect(master);

  osc.type      = options.waveType || 'sine';
  osc.frequency.setValueAtTime(frequency, ctx.currentTime);

  // Frequency sweep (for valve rotation sustain)
  if (options.freqEnd) {
    osc.frequency.linearRampToValueAtTime(options.freqEnd, ctx.currentTime + durationMs / 1000);
  }

  // Envelope: attack → sustain → decay
  const attackTime  = options.attackMs  || 5;
  const decayTime   = options.decayMs   || durationMs * 0.6;
  const peakGain    = options.peakGain  || 0.4;

  gain.gain.setValueAtTime(0, ctx.currentTime);
  gain.gain.linearRampToValueAtTime(peakGain, ctx.currentTime + attackTime / 1000);
  gain.gain.exponentialRampToValueAtTime(
    0.001,
    ctx.currentTime + durationMs / 1000
  );

  osc.start(ctx.currentTime);
  osc.stop(ctx.currentTime + durationMs / 1000 + 0.01);
}
```

### Chord player (for multi-frequency events)

```javascript
function playChord(frequencies, durationMs, options = {}) {
  frequencies.forEach((freq, i) => {
    setTimeout(() => playTone(freq, durationMs, options), i * 5); // slight stagger for richness
  });
}
```

### Noise burst (for valve creak texture)

```javascript
function playNoiseBurst(durationMs, filterFreq = 1200) {
  const ctx    = getAudioContext();
  const master = getMasterGain();

  const bufferSize = ctx.sampleRate * (durationMs / 1000);
  const buffer     = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
  const data       = buffer.getChannelData(0);

  for (let i = 0; i < bufferSize; i++) {
    data[i] = (Math.random() * 2 - 1) * 0.15;  // low-amplitude white noise
  }

  const source = ctx.createBufferSource();
  const filter = ctx.createBiquadFilter();
  const gain   = ctx.createGain();

  source.buffer = buffer;
  filter.type   = 'lowpass';
  filter.frequency.value = filterFreq;

  source.connect(filter);
  filter.connect(gain);
  gain.connect(master);

  gain.gain.setValueAtTime(0.3, ctx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + durationMs / 1000);

  source.start(ctx.currentTime);
}
```

---

## Event-to-Audio Binding

Audio is triggered by listening to state machine dispatch events. Do not call audio functions from physics callbacks or render loops.

```javascript
function bindAudioToStateEvents(eventEmitter) {
  eventEmitter.on('STEP_PASS', ({ stepId }) => {
    switch (stepId) {
      case 2: playTone(4200, 40, { waveType: 'square', peakGain: 0.3 }); break;
      case 3: playTone(1850, 60, { waveType: 'sine', peakGain: 0.4 }); break;
      case 4:
        playTone(1200, 70, { waveType: 'sine', peakGain: 0.35 });
        setTimeout(() => playTone(2400, 50, { waveType: 'square', peakGain: 0.25 }), 80);
        break;
      case 6: playTone(660, 200, { waveType: 'sine', peakGain: 0.2, decayMs: 180 }); break;
      default: playChord([880, 1320], 120, { waveType: 'sine', peakGain: 0.3 }); break;
    }
  });

  eventEmitter.on('STEP_FAIL', () => {
    playTone(220, 150, { waveType: 'triangle', peakGain: 0.25 });
  });

  eventEmitter.on('WRONG_ORDER_INTERACTION', () => {
    playTone(330, 100, { waveType: 'sine', peakGain: 0.2 });
  });

  eventEmitter.on('SESSION_COMPLETE', () => {
    playChord([440, 554, 660], 600, { waveType: 'sine', peakGain: 0.35, attackMs: 40 });
  });

  eventEmitter.on('SESSION_RESET', () => {
    playTone(180, 80, { waveType: 'triangle', peakGain: 0.2 });
  });

  eventEmitter.on('VALVE_ROTATION_START', () => {
    playNoiseBurst(80, 800);
    playTone(400, 80, { waveType: 'sawtooth', peakGain: 0.15 });
  });

  eventEmitter.on('VALVE_ROTATION_SUSTAIN', ({ angle }) => {
    // Pitch rises with resistance — maps to torque curve phases
    const freq = 200 + (angle / (Math.PI / 2)) * 180;
    playTone(freq, 50, { waveType: 'sine', peakGain: 0.1 });
  });

  eventEmitter.on('HASP_PROXIMITY', () => {
    playTone(800, 30, { waveType: 'sine', peakGain: 0.15 });
  });
}
```

---

## Haptic Feedback

Haptic feedback applies when the learner is using a device that supports `navigator.vibrate` (primarily mobile) or a WebXR haptic controller.

### Haptic event map

| Event | Pattern (ms) | Notes |
|-------|-------------|-------|
| Step pass | `[50]` | Single short pulse — confirmation |
| Step fail | `[30, 20, 30]` | Double tap — correction signal |
| Valve rotation (continuous) | `[20, 20]` repeated | Low-frequency vibration while rotating |
| Hasp snap | `[60]` | Medium pulse — alignment success |
| Padlock locked | `[40, 10, 40]` | Two-pulse sequence — engagement + lock |
| Session complete | `[80, 30, 80, 30, 80]` | Celebration triple pulse |
| Wrong-order interaction | `[15, 15, 15]` | Rapid triple tap — gentle correction |

```javascript
function triggerHaptic(pattern) {
  if (navigator.vibrate) {
    navigator.vibrate(pattern);
  }
  // WebXR haptic controller (if active)
  if (xrGamepad?.hapticActuators?.length > 0) {
    xrGamepad.hapticActuators[0].pulse(0.5, pattern[0]);
  }
}
```

Haptic feedback is an enhancement — it must never be the only channel for critical feedback. Every haptic event has an audio and visual counterpart.

---

## Accessibility and Reduced Motion

When the user has enabled the reduced-motion preference or explicitly disabled simulator audio:
- Continue to play audio cues (audio is not motion)
- Suppress only animated visual feedback effects (e.g. particle bursts, flash animations)
- Haptic feedback remains active regardless of reduced-motion preference

Audio can be muted by the learner via the settings panel. The mute state must be persisted in their profile preferences (`profile.audioEnabled`). When `audioEnabled: false`:

```javascript
function playToneIfEnabled(frequency, duration, options) {
  if (!getUserPreference('audioEnabled', true)) return;
  playTone(frequency, duration, options);
}
```

Visual feedback (step indicator colour change, text feedback) must always be present regardless of audio/haptic state — it is the primary accessibility channel.

---

## What Not To Do

- Do not use `HTMLAudioElement` for interaction cues — use Web Audio API exclusively
- Do not trigger audio from physics callbacks or the render loop — only from state machine events
- Do not loop audio indefinitely — all cues have defined durations
- Do not play the generic step pass chord on steps 2, 3, 4, or 6 — those have mechanical-specific cues
- Do not play failure audio on wrong-order interactions — use the correction tone only
- Do not create the `AudioContext` before a user gesture — browsers will suspend it
- Do not use haptic feedback as the only channel for any assessed event
- Do not ignore the `audioEnabled` user preference when calling play functions
