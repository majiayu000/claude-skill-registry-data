---
name: mixmi-mixer-architecture
description: Complete technical reference for the professional mixer system architecture, audio routing, recording implementation, and all internal mechanics
metadata:
  status: Active
  implementation: Alpha - Web Audio API + Tone.js
  last_updated: 2025-10-26
---

# mixmi Alpha - Mixer Architecture Deep Dive

> Complete technical reference for the professional mixer system architecture, audio routing, recording implementation, and all internal mechanics

## Overview

The mixmi Alpha professional mixer (`/mixer` page) is a dual-deck DJ interface built with:
- **Tone.js** for professional audio processing and effects
- **Web Audio API** for low-level audio routing
- **MediaRecorder API** for live mix recording
- **React Context** (MixerContext) for global state
- **Canvas API** for waveform visualization
- **requestAnimationFrame** for smooth playhead updates

**File:** `components/mixer/SimplifiedMixer.tsx` (68KB, 1800+ lines)

## Architecture Principles

### Design Philosophy

1. **Professional Audio Quality:** No quality loss, proper gain staging, clean signal flow
2. **Real-time Performance:** 60fps waveform updates, instant FX response
3. **Memory Safety:** Proper cleanup, no leaks, stable for extended sessions
4. **Modular Design:** Decks, FX, controls are independent, reusable components

### Key Constraints

- **Loop-only content:** Mixer accepts 8-bar loops only (no songs/EPs)
- **BPM range:** 60-200 BPM supported
- **Sync locked:** When sync enabled, both decks match master BPM
- **Fixed loop lengths:** 2, 4, 8, 16 bars only

## State Management

### SimplifiedMixerState Structure

```typescript
interface SimplifiedMixerState {
  deckA: DeckState;
  deckB: DeckState;
  masterBPM: number;              // Global tempo (default 120)
  crossfaderPosition: number;     // 0-100 (0=A only, 50=center, 100=B only)
  syncActive: boolean;            // Master sync on/off
}

interface DeckState {
  track: Track | null;            // Currently loaded track
  playing: boolean;               // Playback state
  audioState?: any;               // Tone.js player state
  audioControls?: any;            // Playback controls
  loading?: boolean;              // Track loading indicator
  loopEnabled: boolean;           // Loop on/off (default true)
  loopLength: number;             // 2, 4, 8, 16 bars
  loopPosition: number;           // Which loop section (0, 1, 2...)
  boostLevel: number;             // 0=off, 1=gentle (cyan), 2=aggressive (orange)
}
```

**State Persistence:**
- MixerContext provides global state accessible across pages
- localStorage backing for track collection
- Deck states reset on page refresh (intentional - fresh session each time)

## Audio Signal Flow

### Complete Routing Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         DECK A                                  │
│                                                                 │
│  Audio File (track.audioUrl)                                   │
│         ↓                                                       │
│  Tone.Player (playback, loop control)                          │
│         ↓                                                       │
│  Filter (lowpass 20kHz, adjustable cutoff)                     │
│         ↓                                                       │
│  Reverb (decay 2.0s, wet/dry mix)                              │
│         ↓                                                       │
│  Delay (8th note feedback, adjustable)                         │
│         ↓                                                       │
│  Deck Gain (volume control, boost levels)                      │
│         ↓                                                       │
└─────────┼───────────────────────────────────────────────────────┘
          │
          ├─────────────→ Crossfader (mixing)
          │                     ↓
┌─────────┼───────────────────────────────────────────────────────┐
│         ↓                                                       │
│  Deck Gain (volume control, boost levels)                      │
│         ↑                                                       │
│  Delay (8th note feedback, adjustable)                         │
│         ↑                                                       │
│  Reverb (decay 2.0s, wet/dry mix)                              │
│         ↑                                                       │
│  Filter (lowpass 20kHz, adjustable cutoff)                     │
│         ↑                                                       │
│  Tone.Player (playback, loop control)                          │
│         ↑                                                       │
│  Audio File (track.audioUrl)                                   │
│                                                                 │
│                         DECK B                                  │
└─────────────────────────────────────────────────────────────────┘
                          ↓
                   Master Gain
                          ↓
              AudioContext Destination (speakers)
                          ↓
         MediaStreamAudioDestinationNode (recording)
                          ↓
                  MediaRecorder
                          ↓
                  Recorded Blob (MP3)
```

### Signal Flow Details

**Per-Deck Chain:**
1. **Tone.Player:** Loads audio, handles playback rate (for BPM sync), loop points
2. **Filter:** Tone.Filter (lowpass), default 20kHz (wide open), FX control adjusts cutoff
3. **Reverb:** Tone.Reverb, 2.0s decay, wet/dry mix controlled by FX knob
4. **Delay:** Tone.FeedbackDelay, 8th note timing (synced to BPM), feedback adjustable
5. **Deck Gain:** Tone.Gain, controls volume + boost (gentle: 1.2x, aggressive: 1.5x)

**Crossfader Mixing:**
```typescript
const crossfaderGainA = (100 - crossfaderPosition) / 100;
const crossfaderGainB = crossfaderPosition / 100;

// Position 0:   A=1.0, B=0.0 (A only)
// Position 50:  A=0.5, B=0.5 (center)
// Position 100: A=0.0, B=1.0 (B only)
```

**Master Output:**
- Master gain node (overall volume)
- Splits to:
  - AudioContext.destination (speakers)
  - MediaStreamAudioDestinationNode (recording capture point)

## Audio Implementation Details

### Tone.js Integration

**Initialization:**
```typescript
import * as Tone from 'tone';

// Start audio context on user interaction (browser requirement)
const startAudio = async () => {
  await Tone.start();
  console.log('Audio context started');
};

// Create audio chain for deck
const createDeckAudioChain = (audioUrl: string) => {
  const player = new Tone.Player(audioUrl).toDestination();
  const filter = new Tone.Filter(20000, 'lowpass');
  const reverb = new Tone.Reverb(2.0);
  const delay = new Tone.FeedbackDelay('8n', 0.5);
  const gain = new Tone.Gain(1.0);

  player
    .connect(filter)
    .connect(reverb)
    .connect(delay)
    .connect(gain)
    .connect(crossfaderGain);

  return { player, filter, reverb, delay, gain };
};
```

**Playback Control:**
```typescript
// Play/pause
if (playing) {
  player.start();
} else {
  player.stop();
}

// Loop configuration
player.loop = true;
player.loopStart = loopPosition * loopDuration;
player.loopEnd = (loopPosition + 1) * loopDuration;

// BPM sync (adjust playback rate)
const ratio = masterBPM / track.bpm;
player.playbackRate = ratio;
```

### Loop Implementation

**Loop Timing Calculation:**
```typescript
// Calculate loop duration based on BPM and bar count
const beatsPerLoop = loopLength * 4;  // 4 beats per bar
const secondsPerBeat = 60 / bpm;
const loopDuration = beatsPerBeat * secondsPerBeat;

// Example: 8-bar loop at 120 BPM
// beatsPerLoop = 8 * 4 = 32 beats
// secondsPerBeat = 60 / 120 = 0.5 seconds
// loopDuration = 0.5 * 32 = 16 seconds
```

**Loop Position Control:**
```typescript
// Loop position = which 8-bar section to play
const setLoopPosition = (position: number) => {
  const startTime = position * loopDuration;
  const endTime = (position + 1) * loopDuration;

  player.loopStart = startTime;
  player.loopEnd = endTime;

  // If playing, seek to new position
  if (player.state === 'started') {
    player.seek(startTime);
  }
};

// Loop length selector (2, 4, 8, 16 bars)
const setLoopLength = (bars: number) => {
  const newDuration = (60 / bpm) * 4 * bars;
  player.loopEnd = player.loopStart + newDuration;
};
```

### BPM Sync Engine

**File:** `lib/mixerAudio.ts` - `SimpleLoopSync` class

**Core Logic:**
```typescript
class SimpleLoopSync {
  private masterBPM: number = 120;
  private deckAPlayer: Tone.Player | null = null;
  private deckBPlayer: Tone.Player | null = null;

  setMasterBPM(bpm: number) {
    this.masterBPM = bpm;
    this.syncAllDecks();
  }

  syncDeck(player: Tone.Player, originalBPM: number) {
    const ratio = this.masterBPM / originalBPM;
    player.playbackRate = ratio;
  }

  syncAllDecks() {
    if (this.deckAPlayer && deckATrack) {
      this.syncDeck(this.deckAPlayer, deckATrack.bpm);
    }
    if (this.deckBPlayer && deckBTrack) {
      this.syncDeck(this.deckBPlayer, deckBTrack.bpm);
    }
  }

  // Master BPM increment/decrement
  incrementBPM() {
    this.setMasterBPM(this.masterBPM + 1);
  }

  decrementBPM() {
    this.setMasterBPM(this.masterBPM - 1);
  }
}
```

**Sync Behavior:**
- When sync enabled: Both decks match master BPM via playback rate adjustment
- When sync disabled: Each deck plays at its original BPM
- BPM changes affect all synced decks instantly
- Range: 60-200 BPM (enforced by UI controls)

## Recording Architecture

### Recording Pipeline

**Setup:**
```typescript
// Create destination node for recording
const mixerDestination = Tone.context.createMediaStreamDestination();
masterGainNode.connect(mixerDestination);

// Create MediaRecorder
const mediaRecorder = new MediaRecorder(mixerDestination.stream, {
  mimeType: 'audio/webm;codecs=opus',
  audioBitsPerSecond: 128000
});

// Capture chunks
const audioChunks: BlobPart[] = [];
mediaRecorder.ondataavailable = (e) => {
  if (e.data.size > 0) {
    audioChunks.push(e.data);
  }
};

// Start recording
mediaRecorder.start();
```

**Stop & Download:**
```typescript
mediaRecorder.onstop = () => {
  const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
  const audioUrl = URL.createObjectURL(audioBlob);
  
  // Create download link
  const a = document.createElement('a');
  a.href = audioUrl;
  a.download = `mixmi_recording_${Date.now()}.webm`;
  a.click();
  
  // Cleanup
  URL.revokeObjectURL(audioUrl);
};

// Stop recording
mediaRecorder.stop();
```

### Recording Metadata

**Tracking Source Loops:**
```typescript
interface RecordingMetadata {
  recordedAt: Date;
  duration: number;
  masterBPM: number;
  sourceTracks: {
    deckA: {
      trackId: string;
      title: string;
      artist: string;
      bpm: number;
    } | null;
    deckB: {
      trackId: string;
      title: string;
      artist: string;
      bpm: number;
    } | null;
  };
  ipSplits?: {
    // Auto-calculated based on source tracks
    recipients: IPSplitRecipient[];
    totalPercentage: number;
  };
}
```

## FX System

### FX Component Architecture

**File:** `components/mixer/FX.tsx`

**Component Structure:**
```tsx
interface FXProps {
  isActive: boolean;
  label: string;
  ref?: React.RefObject<FXElement>;
}

const FX = forwardRef<FXElement, FXProps>((props, ref) => {
  const audioInputRef = useRef<GainNode | null>(null);
  const audioOutputRef = useRef<GainNode | null>(null);
  const filterRef = useRef<Tone.Filter | null>(null);
  const reverbRef = useRef<Tone.Reverb | null>(null);
  const delayRef = useRef<Tone.FeedbackDelay | null>(null);

  useImperativeHandle(ref, () => ({
    audioInput: audioInputRef.current,
    audioOutput: audioOutputRef.current,
    resetToDefaults: () => {
      // Reset all FX parameters
      if (filterRef.current) {
        filterRef.current.frequency.value = 20000;
      }
      if (reverbRef.current) {
        reverbRef.current.wet.value = 0;
      }
      if (delayRef.current) {
        delayRef.current.wet.value = 0;
      }
    }
  }));

  return (
    <div className="fx-controls">
      {/* Knobs for filter, reverb, delay */}
    </div>
  );
});
```

### FX Connection Strategy

**Retry Logic:**
```typescript
const connectDeckToFX = async (
  player: Tone.Player,
  fxRef: React.RefObject<FXElement>,
  retryCount = 0
): Promise<void> => {
  const maxRetries = 50;
  const retryDelay = 100; // ms

  if (!fxRef.current?.audioInput) {
    if (retryCount < maxRetries) {
      await new Promise(resolve => setTimeout(resolve, retryDelay));
      return connectDeckToFX(player, fxRef, retryCount + 1);
    } else {
      console.warn('FX connection failed after max retries');
      return;
    }
  }

  // Connect player to FX input
  player.connect(fxRef.current.audioInput);
  
  // Connect FX output to crossfader
  if (fxRef.current.audioOutput) {
    fxRef.current.audioOutput.connect(crossfaderGain);
  }
};
```

## Waveform Display

### Canvas Implementation

**File:** `components/mixer/WaveformDisplay.tsx`

**Rendering Logic:**
```typescript
const drawWaveform = (
  canvas: HTMLCanvasElement,
  audioBuffer: AudioBuffer,
  currentTime: number,
  duration: number
) => {
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  const width = canvas.width;
  const height = canvas.height;
  
  // Clear canvas
  ctx.clearRect(0, 0, width, height);
  
  // Draw waveform
  const data = audioBuffer.getChannelData(0);
  const step = Math.ceil(data.length / width);
  const amp = height / 2;
  
  ctx.beginPath();
  for (let i = 0; i < width; i++) {
    const min = Math.min(...data.slice(i * step, (i + 1) * step));
    const max = Math.max(...data.slice(i * step, (i + 1) * step));
    
    ctx.moveTo(i, amp * (1 + min));
    ctx.lineTo(i, amp * (1 + max));
  }
  ctx.strokeStyle = '#81E4F2';
  ctx.stroke();
  
  // Draw playhead
  const playheadX = (currentTime / duration) * width;
  ctx.beginPath();
  ctx.moveTo(playheadX, 0);
  ctx.lineTo(playheadX, height);
  ctx.strokeStyle = '#FFE4B5';
  ctx.lineWidth = 2;
  ctx.stroke();
};
```

**Animation Loop:**
```typescript
const animate = () => {
  if (playing && playerRef.current) {
    const currentTime = Tone.Transport.seconds % duration;
    currentTimeRef.current = currentTime;
    
    if (canvasRef.current && audioBufferRef.current) {
      drawWaveform(
        canvasRef.current,
        audioBufferRef.current,
        currentTime,
        duration
      );
    }
  }
  
  animationFrameRef.current = requestAnimationFrame(animate);
};
```

## Memory Management

### Critical Memory Fixes (Oct 23, 2025)

**Problem 1: Tone.js Objects Not Disposed**
```typescript
// BEFORE: Memory leak
const loadTrack = (track: Track) => {
  const player = new Tone.Player(track.audioUrl);
  setDeckAPlayer(player);  // ❌ Previous player never disposed
};

// AFTER: Proper cleanup
const loadTrack = (track: Track) => {
  // Clean up previous track
  if (deckAPlayer) {
    deckAPlayer.stop();
    deckAPlayer.disconnect();
    deckAPlayer.dispose();
  }

  // Load new track
  const player = new Tone.Player(track.audioUrl);
  setDeckAPlayer(player);
};

// Component unmount cleanup
useEffect(() => {
  return () => {
    if (deckAPlayer) {
      deckAPlayer.stop();
      deckAPlayer.disconnect();
      deckAPlayer.dispose();
    }
    if (deckBPlayer) {
      deckBPlayer.stop();
      deckBPlayer.disconnect();
      deckBPlayer.dispose();
    }
  };
}, []);
```

**Problem 2: FX Retry Timeouts Leaked**
```typescript
// BEFORE: Timeouts created but never cleared
const connectFX = () => {
  setTimeout(() => {/* retry */}, 100);  // ❌ Leaked
};

// AFTER: Track and cleanup timeouts
const fxRetryTimeoutsRef = useRef<Set<NodeJS.Timeout>>(new Set());

const connectFX = () => {
  const timeout = setTimeout(() => {/* retry */}, 100);
  fxRetryTimeoutsRef.current.add(timeout);
  return timeout;
};

useEffect(() => {
  return () => {
    fxRetryTimeoutsRef.current.forEach(t => clearTimeout(t));
    fxRetryTimeoutsRef.current.clear();
  };
}, []);
```

**Problem 3: Animation Frame Not Canceled**
```typescript
// BEFORE: requestAnimationFrame never canceled
const animate = () => {
  requestAnimationFrame(animate);  // ❌ Runs forever
};

// AFTER: Track and cancel animation frame
const animationFrameRef = useRef<number | null>(null);

const animate = () => {
  animationFrameRef.current = requestAnimationFrame(animate);
};

useEffect(() => {
  animationFrameRef.current = requestAnimationFrame(animate);

  return () => {
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current);
    }
  };
}, []);
```

### Type Safety Improvements (Oct 23, 2025)

**Eliminated All 'any' Types:**
```typescript
// BEFORE: Type safety issues
const handleDrop = (item: any) => {  // ❌ any type
  const track = item.track;
};

// AFTER: Proper types
interface DropItem {
  track: IPTrack;
  sourceIndex?: number;
}

const handleDrop = (item: DropItem) => {  // ✅ Type-safe
  const track = item.track;
};
```

**FX Element Type:**
```typescript
// Custom type for FX component ref
interface FXElement extends HTMLDivElement {
  audioInput?: GainNode;
  audioOutput?: GainNode;
  resetToDefaults?: () => void;
}

const deckAFXRef = useRef<FXElement>(null);
```

## Keyboard Shortcuts

**Current Shortcuts:**
```typescript
// Playback
Space:     Play/Pause Deck A
Shift+Space: Play/Pause Deck B

// BPM
ArrowUp:   Increment Master BPM (+1)
ArrowDown: Decrement Master BPM (-1)

// Sync
S:         Toggle Sync

// Recording
R:         Start/Stop Recording

// Loop
L:         Toggle Loop (Deck A)
Shift+L:   Toggle Loop (Deck B)

// Loop Position
[: Previous Loop Position (Deck A)
]: Next Loop Position (Deck A)

// Crossfader
A: Crossfader to Deck A (position 0)
B: Crossfader to Deck B (position 100)
C: Crossfader to Center (position 50)
```

**Implementation:**
```typescript
useEffect(() => {
  const handleKeyPress = (e: KeyboardEvent) => {
    // Ignore if typing in input
    if (e.target instanceof HTMLInputElement) return;

    switch (e.key) {
      case ' ':
        e.preventDefault();
        if (e.shiftKey) {
          toggleDeckB();
        } else {
          toggleDeckA();
        }
        break;

      case 'ArrowUp':
        e.preventDefault();
        incrementBPM();
        break;

      case 'ArrowDown':
        e.preventDefault();
        decrementBPM();
        break;

      case 's':
      case 'S':
        toggleSync();
        break;

      case 'r':
      case 'R':
        isRecording ? stopRecording() : startRecording();
        break;

      // ... other shortcuts
    }
  };

  document.addEventListener('keydown', handleKeyPress);
  return () => document.removeEventListener('keydown', handleKeyPress);
}, [/* dependencies */]);
```

## Known Issues & Limitations

### Current Issues

1. **Recording Format:** WebM/Opus not universally supported (need MP3 encoding)
2. **No Upload:** Recordings download only, not saved to Supabase
3. **FX Automation:** No automation lanes, manual FX control only
4. **No EQ:** Basic filter only, no 3-band EQ
5. **No Beat Matching:** Manual BPM sync only, no auto-beat detection
6. **Single Crossfader Curve:** Linear only, no curve options

### Future Enhancements

**High Priority:**
1. **MP3 Recording:** Convert WebM to MP3 using lamejs or similar
2. **Upload to Supabase:** Save recordings as new tracks
3. **Remix Metadata:** Track source loops, auto-calculate IP splits
4. **Waveform Preview:** Visual preview before download

**Medium Priority:**
1. **3-Band EQ:** Low/Mid/High per deck
2. **Additional FX:** Flanger, phaser, distortion
3. **FX Automation:** Record FX parameter changes
4. **Cue Points:** Mark points in loops for quick jumps
5. **Beat Grid:** Visual beat alignment

**Low Priority:**
1. **MIDI Support:** Control mixer with MIDI controllers
2. **Multiple Crossfader Curves:** Fast cut, slow cut options
3. **Advanced Loop Modes:** Reverse, half-speed, double-speed
4. **Spectrum Analyzer:** Frequency visualization

## Troubleshooting Guide

### Common Issues

**Problem: No audio playback**
```typescript
// Solution: Ensure AudioContext started
await Tone.start();

// Check browser autoplay policy
// User interaction required before audio starts
```

**Problem: Sync not working**
```typescript
// Check: Is sync engine receiving BPM updates?
handleBPMChange(newBPM) {
  setMasterBPM(newBPM);
  syncEngine.setMasterBPM(newBPM);  // ← Must call this!
}
```

**Problem: Recording produces no file**
```typescript
// Check: Is master gain connected to destination?
masterGain.connect(mixerDestinationRef.current);

// Check: MediaRecorder state
console.log(mediaRecorderRef.current?.state);  // Should be "recording"
```

**Problem: FX not working**
```typescript
// Check: Are FX refs connected?
console.log(deckAFXRef.current?.audioInput);  // Should be GainNode

// Check: FX retry logic completing?
// Look for console warnings: "FX connection failed for deck A"
```

**Problem: Waveform not updating**
```typescript
// Check: Is animation frame running?
console.log(animationFrameRef.current);  // Should be number (frame ID)

// Check: Are refs being updated?
console.log(deckACurrentTimeRef.current);  // Should match playback time
```

## Related Skills

- **mixmi-component-library** - UI components (SimplifiedDeck, WaveformDisplay, etc.)
- **mixmi-payment-flow** - Smart contract integration for remix payments
- **mixmi-user-flows** - Mixer usage flows and user journeys
- **mixmi-design-patterns** - Visual design patterns for new features