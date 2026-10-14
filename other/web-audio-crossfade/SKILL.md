---
name: web-audio-crossfade
description: Web Audio API crossfading and gapless playback techniques. Use when implementing audio transitions, crossfades between tracks, or working on gapless playback. Triggers on mentions of crossfade, gapless, audio transitions, or track switching.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Web Audio API Crossfading

## The Gapless Problem

Browsers have inherent gaps between audio tracks:
- **Chrome/Firefox**: ~45ms gap (fundamental limitation)
- **Safari**: True gapless (no gap)

**Solution**: Use 35ms crossfades to mask the gap.

## Audio Graph for Crossfading

```
┌──────────────┐     ┌──────────────┐
│  Source A    │────▶│  Gain A      │──┐
│ (current)    │     │ (fade out)   │  │
└──────────────┘     └──────────────┘  │
                                       ▼
┌──────────────┐     ┌──────────────┐ ┌──────────────┐   ┌─────────────┐
│  Source B    │────▶│  Gain B      │─▶│  Music Bus   │──▶│ Destination │
│ (next)       │     │ (fade in)    │  │  (master)    │   │ (speakers)  │
└──────────────┘     └──────────────┘  └──────────────┘   └─────────────┘
```

## Implementation

### Basic Crossfade

```typescript
const CROSSFADE_DURATION = 0.035; // 35ms

class CrossfadeController {
  private context: AudioContext;
  private currentGain: GainNode;
  private nextGain: GainNode;

  crossfade(startTime: number): void {
    const endTime = startTime + CROSSFADE_DURATION;

    // Fade out current track
    this.currentGain.gain.setValueAtTime(1.0, startTime);
    this.currentGain.gain.linearRampToValueAtTime(0.0, endTime);

    // Fade in next track
    this.nextGain.gain.setValueAtTime(0.0, startTime);
    this.nextGain.gain.linearRampToValueAtTime(1.0, endTime);
  }
}
```

### Equal Power Crossfade (Smoother)

Linear crossfades have a volume dip in the middle. Equal power maintains perceived loudness:

```typescript
function equalPowerCrossfade(
  currentGain: GainNode,
  nextGain: GainNode,
  startTime: number,
  duration: number
): void {
  const steps = 10;
  const stepDuration = duration / steps;

  for (let i = 0; i <= steps; i++) {
    const t = startTime + (i * stepDuration);
    const progress = i / steps;

    // Equal power curve
    const fadeOut = Math.cos(progress * 0.5 * Math.PI);
    const fadeIn = Math.cos((1.0 - progress) * 0.5 * Math.PI);

    currentGain.gain.setValueAtTime(fadeOut, t);
    nextGain.gain.setValueAtTime(fadeIn, t);
  }
}
```

### Double-Buffer Pattern

Keep two track slots and alternate between them:

```typescript
class DoubleBufferPlayer {
  private slotA: TrackSlot;
  private slotB: TrackSlot;
  private activeSlot: 'A' | 'B' = 'A';

  async preloadNext(url: string): Promise<void> {
    const inactiveSlot = this.activeSlot === 'A' ? this.slotB : this.slotA;

    const response = await fetch(url);
    const arrayBuffer = await response.arrayBuffer();
    const audioBuffer = await this.context.decodeAudioData(arrayBuffer);

    inactiveSlot.buffer = audioBuffer;
    inactiveSlot.ready = true;
  }

  playNext(): void {
    const current = this.activeSlot === 'A' ? this.slotA : this.slotB;
    const next = this.activeSlot === 'A' ? this.slotB : this.slotA;

    if (!next.ready) {
      console.error('Next track not preloaded!');
      return;
    }

    // Schedule crossfade
    const now = this.context.currentTime;
    this.crossfade(current.gain, next.gain, now);

    // Start next track
    next.source = this.context.createBufferSource();
    next.source.buffer = next.buffer;
    next.source.connect(next.gain);
    next.source.start(now);

    // Stop current after fade
    current.source?.stop(now + CROSSFADE_DURATION);

    // Swap active slot
    this.activeSlot = this.activeSlot === 'A' ? 'B' : 'A';
  }
}
```

## Timing Considerations

### Use AudioContext.currentTime

Always use the audio clock, never JavaScript timers:

```typescript
// GOOD - sample-accurate
const now = this.context.currentTime;
this.scheduleCrossfade(now);

// BAD - imprecise
setTimeout(() => {
  this.crossfade();
}, 35);
```

### Preload Before Track Ends

Monitor playback position and preload the next track:

```typescript
const PRELOAD_THRESHOLD = 10; // seconds before end

function monitorPlayback(): void {
  const elapsed = this.context.currentTime - this.startTime;
  const remaining = this.duration - elapsed;

  if (remaining <= PRELOAD_THRESHOLD && !this.nextPreloaded) {
    this.preloadNext();
    this.nextPreloaded = true;
  }

  if (remaining <= CROSSFADE_DURATION && !this.crossfadeScheduled) {
    this.scheduleCrossfade(this.context.currentTime);
    this.crossfadeScheduled = true;
  }
}
```

## Common Pitfalls

1. **Using setTimeout** - Inaccurate, causes gaps
2. **Not preloading** - Decode takes time, causes gaps
3. **Linear crossfade** - Volume dip in middle
4. **Forgetting cleanup** - Disconnect old nodes to prevent memory leaks

## Cleanup

Always disconnect nodes when done:

```typescript
source.onended = () => {
  source.disconnect();
  gain.disconnect();
  // Clear references
  this.currentSource = null;
};
```
