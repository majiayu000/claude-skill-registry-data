---
name: audio-ducking
description: Audio ducking implementation for voice-overs and announcements. Use when implementing message playback over music, announcement systems, or volume automation. Triggers on mentions of ducking, announcements, voice-over, messages, or promotional clips.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Audio Ducking for Announcements

## What is Ducking?

Ducking automatically lowers the music volume when an announcement or voice-over plays, then restores it after.

```
Volume
  100% ─────┐                           ┌─────
            │                           │
   15% ─────┴───────────────────────────┴─────
            ↑           ↑               ↑
          Attack     Message         Release
         (300ms)     Playing         (500ms)
```

## Audio Graph for Ducking

```
┌──────────────┐     ┌──────────────┐
│   Music      │────▶│  Music Bus   │──┐
│   Source     │     │  (ducked)    │  │
└──────────────┘     └──────────────┘  │   ┌──────────────┐   ┌─────────────┐
                                       ├──▶│  Master Bus  │──▶│ Destination │
┌──────────────┐     ┌──────────────┐  │   └──────────────┘   └─────────────┘
│   Message    │────▶│  Message Bus │──┘
│   Source     │     │  (full vol)  │
└──────────────┘     └──────────────┘
```

## Standard Parameters

```typescript
const DUCK_CONFIG = {
  duckLevel: 0.15,      // 15% of normal volume
  attackTime: 0.3,       // 300ms fade down
  holdTime: 0.1,         // 100ms minimum hold before release
  releaseTime: 0.5,      // 500ms fade back up
};
```

## Implementation

### DuckingController Class

```typescript
class DuckingController {
  private context: AudioContext;
  private musicBus: GainNode;
  private messageBus: GainNode;
  private isDucked: boolean = false;
  private config: DuckConfig;

  constructor(
    context: AudioContext,
    musicBus: GainNode,
    config: Partial<DuckConfig> = {}
  ) {
    this.context = context;
    this.musicBus = musicBus;
    this.config = { ...DUCK_CONFIG, ...config };

    // Create message bus
    this.messageBus = context.createGain();
    this.messageBus.connect(context.destination);
  }

  /**
   * Duck the music volume
   */
  duck(): void {
    if (this.isDucked) return;

    const now = this.context.currentTime;
    const targetTime = now + this.config.attackTime;

    // Cancel any pending automation
    this.musicBus.gain.cancelScheduledValues(now);

    // Exponential ramp sounds more natural than linear
    this.musicBus.gain.setValueAtTime(this.musicBus.gain.value, now);
    this.musicBus.gain.exponentialRampToValueAtTime(
      Math.max(this.config.duckLevel, 0.001), // Can't ramp to 0
      targetTime
    );

    this.isDucked = true;
  }

  /**
   * Restore music to full volume
   */
  release(): void {
    if (!this.isDucked) return;

    const now = this.context.currentTime;
    const holdEnd = now + this.config.holdTime;
    const releaseEnd = holdEnd + this.config.releaseTime;

    this.musicBus.gain.cancelScheduledValues(now);
    this.musicBus.gain.setValueAtTime(this.musicBus.gain.value, now);
    this.musicBus.gain.setValueAtTime(this.config.duckLevel, holdEnd);
    this.musicBus.gain.exponentialRampToValueAtTime(1.0, releaseEnd);

    this.isDucked = false;
  }

  /**
   * Play a message with automatic ducking
   */
  async playMessage(url: string): Promise<void> {
    // Duck the music
    this.duck();

    // Load and decode the message
    const response = await fetch(url);
    const arrayBuffer = await response.arrayBuffer();
    const audioBuffer = await this.context.decodeAudioData(arrayBuffer);

    // Create source and play
    const source = this.context.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(this.messageBus);

    return new Promise((resolve) => {
      source.onended = () => {
        source.disconnect();
        this.release();
        resolve();
      };

      source.start();
    });
  }
}
```

### Message Queue for Multiple Announcements

```typescript
interface QueuedMessage {
  url: string;
  priority: number;
}

class MessageQueue {
  private queue: QueuedMessage[] = [];
  private isPlaying: boolean = false;
  private duckingController: DuckingController;

  enqueue(message: QueuedMessage): void {
    this.queue.push(message);
    // Sort by priority (higher first)
    this.queue.sort((a, b) => b.priority - a.priority);
    this.processQueue();
  }

  private async processQueue(): Promise<void> {
    if (this.isPlaying || this.queue.length === 0) return;

    this.isPlaying = true;

    // Duck once for entire sequence
    this.duckingController.duck();

    while (this.queue.length > 0) {
      const message = this.queue.shift()!;

      // Play message (without extra duck/release)
      await this.playMessageAudio(message.url);

      // Small gap between messages
      await this.delay(100);
    }

    // Release after all messages
    this.duckingController.release();
    this.isPlaying = false;
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

## Scheduling Messages

### Time-Based Scheduling

```typescript
interface ScheduledMessage {
  id: string;
  messageId: string;
  playTime: string;        // "HH:mm"
  intervalMinutes?: number; // For recurring (every 30 min)
  daysOfWeek?: number[];   // 0=Sun, 1=Mon, etc.
}

class MessageScheduler {
  private schedules: ScheduledMessage[] = [];
  private checkInterval: number;

  start(): void {
    // Check every minute
    this.checkInterval = setInterval(() => {
      this.checkSchedules();
    }, 60000);
  }

  private checkSchedules(): void {
    const now = new Date();
    const currentTime = now.toTimeString().slice(0, 5); // "HH:mm"
    const currentDay = now.getDay();

    for (const schedule of this.schedules) {
      if (schedule.daysOfWeek && !schedule.daysOfWeek.includes(currentDay)) {
        continue;
      }

      if (schedule.playTime === currentTime) {
        this.playScheduledMessage(schedule);
      }
    }
  }
}
```

## Best Practices

1. **Use exponentialRamp** - Sounds more natural than linear
2. **Hold before release** - Prevents abrupt volume changes
3. **Queue multiple messages** - Don't interrupt mid-message
4. **Priority system** - Urgent announcements first
5. **Don't duck too low** - 15% maintains ambiance
6. **Smooth transitions** - 300-500ms feels natural
