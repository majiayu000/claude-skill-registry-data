---
license: Apache-2.0
name: app-sound-design
description: Design decisions for when and what sounds to use in web apps, mobile apps, and desktop native apps — plus how to create them with AI. Covers UI sound vocabulary (confirms, alerts, transitions, errors), platform conventions (iOS, macOS, Material), creating sounds with AI tools (ElevenLabs, AudioCraft, Stable Audio), Web Audio API for procedural sounds, haptic-audio pairing, and the psychology of satisfying vs. annoying UI sounds. Activate on 'app sounds', 'UI sounds', 'notification sound', 'sound design app', 'earcons', 'sonic branding', 'interaction sounds', 'feedback sounds', 'app audio', 'satisfying sounds'. NOT for professional audio engineering (use sound-engineer), Windows 3.1 retro sounds specifically (use win31-audio-design), music composition (use sound-engineer).
allowed-tools: Read,Write,Edit,Glob,Grep,WebSearch,WebFetch
metadata:
  category: Design & UX
  tags:
    - sound-design
    - UI-sounds
    - earcons
    - sonic-branding
    - Web-Audio-API
    - haptics
    - notification
    - interaction-design
    - AI-audio
  pairs-with:
    - skill: sound-engineer
      reason: Technical audio production when custom sounds need professional post-processing
    - skill: win31-audio-design
      reason: Retro sound palettes for themed UIs (WinDAGs, retro games)
    - skill: native-app-designer
      reason: Sound decisions are inseparable from native app interaction patterns
    - skill: ios-app-beauty
      reason: iOS sound design follows strict Apple HIG conventions
    - skill: motion-design-web
      reason: Animation and sound must be synchronized for polished micro-interactions
category: Design & Creative
tags:
  - app
  - sound
  - design
  - api
  - ai
  - ui
---

# App Sound Design

Makes the design decisions about **when**, **what**, and **how** sounds should appear in applications. This is not about audio engineering (that is **sound-engineer**) or retro sound effects (that is **win31-audio-design**). This skill answers the hardest question in UI sound: **should this interaction make a noise at all?** And if yes, what kind?

## When to Use

**Use for:**
- Deciding which interactions in a web or mobile app should have sound feedback
- Selecting appropriate sound characteristics for notifications, confirmations, errors
- Creating AI-generated UI sounds with ElevenLabs, AudioCraft, or Stable Audio
- Implementing procedural sounds with Web Audio API
- Pairing haptic feedback with audio on iOS/Android
- Establishing a sonic brand identity for a product
- Auditing an app's existing sound design for annoyance vs. helpfulness

**Do NOT use for:**
- Professional audio mixing/mastering -> use **sound-engineer**
- Windows 3.1 themed system sounds -> use **win31-audio-design**
- Music composition or soundtrack -> use **sound-engineer**
- Accessibility screen reader audio -> use **accessibility-expert**
- Game audio systems (3D positional, dynamic music) -> use **sound-engineer**

## The Fundamental Question: Should This Make a Sound?

```
Does the interaction need FEEDBACK?
|
+-- User initiated action (tap, click, submit)?
|   +-- Is the result visible on screen?
|   |   +-- YES and obvious --> Sound is OPTIONAL (often skip)
|   |   +-- YES but subtle --> Sound HELPS (gentle confirm)
|   |   +-- NO (background process) --> Sound RECOMMENDED
|   +-- Is the action destructive?
|       +-- YES --> Sound RECOMMENDED (distinct warning tone)
|       +-- NO --> Sound OPTIONAL
|
+-- System initiated event (notification, alert)?
|   +-- Is the user in the app?
|   |   +-- YES --> Subtle in-app sound
|   |   +-- NO --> Notification sound (follow OS conventions)
|   +-- Is it time-sensitive?
|       +-- YES --> More urgent/attention-grabbing sound
|       +-- NO --> Can be silent or ambient
|
+-- Ambient/atmospheric (background state)?
    +-- Does the app benefit from presence? --> Subtle ambient
    +-- Is the user working/focused? --> SILENCE
```

---

## The UI Sound Vocabulary

Every application needs sounds from these categories. Not all categories are required — most apps need 3-5.

### Tier 1: Essential (Most Apps Need These)

| Sound Type | Purpose | Character | Duration | Example |
|-----------|---------|-----------|----------|---------|
| **Confirm** | Action succeeded | Bright, rising pitch | 100-300ms | Slack message sent |
| **Error** | Action failed | Low, flat or descending | 200-400ms | Form validation fail |
| **Notification** | New information arrived | Distinctive, medium energy | 300-600ms | Slack incoming message |

### Tier 2: Polish (Apps That Care)

| Sound Type | Purpose | Character | Duration | Example |
|-----------|---------|-----------|----------|---------|
| **Transition** | Navigation between views | Subtle whoosh or tap | 50-150ms | iOS page turn |
| **Toggle** | Binary state change | Crisp click or snap | 50-100ms | Switch on/off |
| **Hover** | Mouse-over feedback | Barely audible tick | 20-50ms | Menu item hover |
| **Selection** | Item chosen from list | Soft pop or pluck | 50-150ms | Dropdown select |
| **Delete** | Destructive removal | Hollow thud or swoosh | 150-300ms | Trash action |

### Tier 3: Delight (Apps With Personality)

| Sound Type | Purpose | Character | Duration | Example |
|-----------|---------|-----------|----------|---------|
| **Achievement** | Milestone reached | Musical, celebratory | 500ms-2s | Duolingo lesson complete |
| **Ambient** | Background presence | Looping, atmospheric | Continuous | Noisli, Forest app |
| **Brand Sting** | App open/close | Iconic, memorable | 500ms-1.5s | Netflix ta-dum |
| **Easter Egg** | Hidden delight | Playful, unexpected | Variable | Konami code reward |

---

## Platform Conventions

### Apple (iOS / macOS)

Apple HIG mandates specific audio behaviors:

- **System sounds are sacred**: Never override or replace system alert sounds
- **Respect the silent switch**: If the physical mute switch is on, your app sounds STOP (except media playback)
- **Audio session categories matter**:
  - `ambient` — mixes with other audio, respects silent switch
  - `soloAmbient` — silences other audio, respects silent switch
  - `playback` — ignores silent switch (for media apps ONLY)
- **Haptics pair with sounds**: Use `UIImpactFeedbackGenerator` alongside audio

**Apple's Sound Characteristics:**
- Clean sine waves and filtered tones
- Minimal overtones (pure, not buzzy)
- Short decay (sounds do not linger)
- Consistent volume relative to system sounds

```swift
// iOS: Play a system sound
import AudioToolbox
AudioServicesPlaySystemSound(1057) // Standard keyboard click

// iOS: Haptic + custom sound
let generator = UIImpactFeedbackGenerator(style: .light)
generator.impactOccurred()
// Play your custom sound simultaneously
```

### Material Design (Android)

Google's sound design principles:

- **Functional first**: Sound should inform, not decorate
- **Subtle by default**: UI sounds should be quieter than media
- **Haptic-first on Android**: Prefer haptic feedback; add sound only when haptics are insufficient
- **Sound ON only when meaningful**: Default state should be silent for most interactions

**Material Sound Characteristics:**
- Short, crisp percussive sounds
- Subtle harmonic content (not pure sine waves)
- Slightly warmer than Apple (more mid-frequency)
- Designed to work on low-quality phone speakers

### Web Apps

Web has the WEAKEST sound conventions, which means more freedom but also more risk of annoyance.

- **Never autoplay sound** — browsers block it and users hate it
- **Require user gesture first**: Web Audio API requires a user interaction before playing
- **Provide volume control**: Always let users mute or adjust
- **Consider headphone users**: What sounds fine on laptop speakers may be jarring on headphones

---

## Creating Sounds with AI

### ElevenLabs Sound Effects

Best for: Realistic, high-quality UI sounds with specific character descriptions.

```bash
# Generate a confirmation chime
curl -X POST "https://api.elevenlabs.io/v1/sound-generation" \
  -H "xi-api-key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Short bright upward chime, digital, clean sine wave, 200ms, UI confirmation sound",
    "duration_seconds": 0.5
  }'
```

**Effective prompts for ElevenLabs:**
- Confirm: "Short bright ascending two-note chime, clean digital, warm, 200ms"
- Error: "Low hollow thud with slight buzz, digital, 300ms, not harsh"
- Notification: "Gentle three-note xylophone melody, friendly, 400ms"
- Toggle: "Crisp mechanical click, plastic switch, 50ms"
- Delete: "Soft hollow swoosh moving downward, 200ms"
- Achievement: "Bright ascending arpeggio, sparkly, celebratory, 1 second"

### Meta AudioCraft (Open Source)

Best for: Developers who want full control and no API costs.

```python
from audiocraft.models import AudioGen
from audiocraft.data.audio import audio_write

model = AudioGen.get_pretrained('facebook/audiogen-medium')
model.set_generation_params(duration=0.5)

# Generate UI sounds
descriptions = [
    "short digital confirmation beep, ascending pitch, clean",
    "low error buzz, brief, not harsh, digital",
    "gentle notification chime, two notes, pleasant",
]

wav = model.generate(descriptions)
for i, w in enumerate(wav):
    audio_write(f'ui_sound_{i}', w.cpu(), model.sample_rate)
```

### Stable Audio Open

Best for: Longer ambient sounds, background textures, brand stings.

```python
import torch
from stable_audio_tools import get_pretrained_model
from stable_audio_tools.inference.generation import generate_diffusion_cond

model, model_config = get_pretrained_model("stabilityai/stable-audio-open-1.0")

# Generate ambient background
conditioning = [{
    "prompt": "calm ambient digital texture, warm low hum, suitable for productivity app background, loopable",
    "seconds_total": 10
}]
```

### Post-Processing Checklist

AI-generated sounds need cleanup before shipping:

1. **Trim silence** — remove leading/trailing dead air
2. **Normalize volume** — all UI sounds should be at consistent perceived loudness
3. **Fade in/out** — 5-10ms fade prevents clicking artifacts
4. **Compress dynamic range** — UI sounds should have consistent volume
5. **Export as WAV** (for native) or **OGG/MP3** (for web, under 50KB per sound)
6. **Test on target speakers** — phone speakers cut frequencies below 200Hz

---

## Web Audio API: Procedural Sounds

For web apps, generating sounds procedurally eliminates the need for audio files entirely. Smaller bundles, instant availability.

```typescript
class UISound {
  private ctx: AudioContext | null = null;

  private getContext(): AudioContext {
    if (!this.ctx) {
      this.ctx = new AudioContext();
    }
    return this.ctx;
  }

  /** Bright ascending confirmation */
  confirm(): void {
    const ctx = this.getContext();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.type = 'sine';
    osc.frequency.setValueAtTime(600, ctx.currentTime);
    osc.frequency.linearRampToValueAtTime(900, ctx.currentTime + 0.15);

    gain.gain.setValueAtTime(0.15, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.2);

    osc.start(ctx.currentTime);
    osc.stop(ctx.currentTime + 0.2);
  }

  /** Low descending error tone */
  error(): void {
    const ctx = this.getContext();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.type = 'triangle';
    osc.frequency.setValueAtTime(400, ctx.currentTime);
    osc.frequency.linearRampToValueAtTime(200, ctx.currentTime + 0.3);

    gain.gain.setValueAtTime(0.12, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.35);

    osc.start(ctx.currentTime);
    osc.stop(ctx.currentTime + 0.35);
  }

  /** Subtle click for toggles and selections */
  click(): void {
    const ctx = this.getContext();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.type = 'square';
    osc.frequency.setValueAtTime(800, ctx.currentTime);

    gain.gain.setValueAtTime(0.08, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.05);

    osc.start(ctx.currentTime);
    osc.stop(ctx.currentTime + 0.05);
  }

  /** Three-note notification melody */
  notify(): void {
    const ctx = this.getContext();
    const notes = [523, 659, 784]; // C5, E5, G5

    notes.forEach((freq, i) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, ctx.currentTime);

      const start = ctx.currentTime + i * 0.12;
      gain.gain.setValueAtTime(0, start);
      gain.gain.linearRampToValueAtTime(0.12, start + 0.02);
      gain.gain.exponentialRampToValueAtTime(0.001, start + 0.15);

      osc.start(start);
      osc.stop(start + 0.15);
    });
  }
}

// Usage
const sound = new UISound();
document.querySelector('#submit')?.addEventListener('click', () => sound.confirm());
```

---

## Haptic-Audio Pairing (Mobile)

On mobile, haptics and audio should be designed as a UNIT. The haptic arrives first (immediate physical feedback), the sound arrives second (confirmation and character).

### Pairing Guide

| Interaction | Haptic | Sound | Timing |
|------------|--------|-------|--------|
| Tap button | Light impact | Short click | Simultaneous |
| Toggle switch | Medium impact | Crisp snap | Haptic 10ms before sound |
| Pull-to-refresh | Selection tick during pull; notification on complete | Subtle stretch sound; confirm chime | Haptic leads by 20ms |
| Delete swipe | Heavy impact at threshold | Hollow swoosh | Haptic at commit point |
| Long press | Rigid continuous | Low building hum | Haptic starts with sound |
| Success | Success pattern (triple tap) | Ascending arpeggio | Aligned to beat |

### iOS Implementation

```swift
import UIKit
import AVFoundation

class FeedbackManager {
    static let shared = FeedbackManager()

    private let lightImpact = UIImpactFeedbackGenerator(style: .light)
    private let mediumImpact = UIImpactFeedbackGenerator(style: .medium)
    private let heavyImpact = UIImpactFeedbackGenerator(style: .heavy)
    private let notificationFeedback = UINotificationFeedbackGenerator()

    func tapConfirm() {
        lightImpact.impactOccurred()
        SoundPlayer.play(.confirm)
    }

    func errorShake() {
        notificationFeedback.notificationOccurred(.error)
        SoundPlayer.play(.error)
    }

    func deleteCommit() {
        heavyImpact.impactOccurred()
        SoundPlayer.play(.delete)
    }
}
```

---

## The Psychology of Satisfying Sounds

Why some UI sounds feel "right" and others feel "cheap":

### Satisfying Sound Properties

| Property | Why It Works | Example |
|----------|-------------|---------|
| **Pitch rises** | Signals progress, optimism, completion | Confirm chimes go UP |
| **Short decay** | Feels responsive and controlled | Nintendo menu sounds |
| **Harmonic richness** | Feels organic and warm | Slack's "knock" sound |
| **Consistent volume** | Feels professional and predictable | Apple system sounds |
| **Rhythmic alignment** | Feels intentional and designed | Duolingo's streak counter |

### Annoying Sound Properties

| Property | Why It Grates | Avoid |
|----------|--------------|-------|
| **Repetitive without variation** | Humans habituate, then are irritated | Same exact sound 100x/day |
| **Too loud relative to context** | Breaks concentration, startles | Notification sounds above -12dB |
| **Pure sine at high frequency** | Perceived as alarm, triggers anxiety | Any sound above 2kHz pure tone |
| **Long sustained notes** | Feels like something is wrong | Tones lasting >500ms for routine feedback |
| **Dissonant intervals** | Creates unconscious discomfort | Minor seconds or tritones in notifications |

### The Repetition Threshold

Any sound heard more than **~15 times per hour** becomes irritating regardless of how pleasant it initially was. Solutions:

1. **Vary subtly**: Randomize pitch by +/- 5%, or choose from 3-4 variants
2. **Reduce frequency**: After the 5th trigger, reduce volume by 30%
3. **Let users control**: Always provide per-sound-type mute toggles
4. **Silence by default**: Only enable sounds that users opt into

```typescript
// Subtle pitch variation to prevent habituation
function playWithVariation(baseFrequency: number): void {
  const variation = 1 + (Math.random() - 0.5) * 0.1; // +/- 5%
  const frequency = baseFrequency * variation;
  // ... use this frequency in your oscillator
}
```

---

## Sound Design Decision Matrix

| App Type | Confirm | Error | Notification | Transition | Ambient | Brand Sting |
|----------|---------|-------|-------------|------------|---------|-------------|
| Productivity (Notion) | Optional | Yes | Yes | Skip | Skip | Skip |
| Social (Slack) | Yes | Yes | Yes | Skip | Skip | Skip |
| Gaming | Yes | Yes | Yes | Yes | Yes | Yes |
| E-commerce | Skip | Yes | Yes | Skip | Skip | Optional |
| Creative tools | Yes | Yes | Optional | Yes | Optional | Optional |
| Health/meditation | Skip | Skip | Gentle | Yes | Yes | Yes |
| Finance/banking | Skip | Yes | Yes | Skip | Skip | Skip |
| Children's apps | Yes | Yes | Yes | Yes | Optional | Yes |

---

## Anti-Patterns

### Anti-Pattern: Sound on Every Click

Playing a sound on every button click, link tap, and scroll event creates an overwhelming audio assault. Reserve sounds for MEANINGFUL state changes, not routine navigation.

### Anti-Pattern: Autoplay Background Audio

Web apps that play ambient sound without user consent will be immediately closed. Always require explicit opt-in. Browsers actively block autoplay audio for good reason.

### Anti-Pattern: Skeuomorphic Sound Mismatch

Playing a typewriter click sound in a modern chat app creates cognitive dissonance unless the entire aesthetic is retro. Sound must match the visual design language.

### Anti-Pattern: No Mute Option

Every app with sound MUST have an easily discoverable mute control. Burying it 3 menus deep is nearly as bad as having no mute at all.

### Anti-Pattern: Identical Sounds for Different Events

Using the same chime for "message sent" and "message received" destroys the information value of sound. Each semantic category must have a distinct sound.

### Anti-Pattern: Notification Sound in Focused Contexts

Playing notification sounds while a user is in a full-screen editor, reading an article, or watching a video. Respect focus state and suppress non-critical audio.

### Anti-Pattern: Ignoring Hardware Diversity

A beautiful sound designed on studio monitors may be a harsh buzz on phone speakers. Always test on the cheapest speakers your users will have: phone speakers cut below 200Hz and boost 1-4kHz.

---

## Quality Checklist

- [ ] Every sound answers "why does this interaction need audio feedback?"
- [ ] Sound vocabulary mapped: which interactions get which sound type
- [ ] Platform conventions respected (iOS silent switch, Android haptic-first)
- [ ] Mute control discoverable within 1 tap/click
- [ ] All sounds under 500ms for routine feedback (longer only for achievements/brand)
- [ ] Consistent perceived volume across all UI sounds
- [ ] Sounds tested on phone speakers, laptop speakers, and headphones
- [ ] `prefers-reduced-motion` considered for audio (some users want minimal sensory input)
- [ ] Repetition threshold addressed (variation, volume reduction, or frequency limit)
- [ ] Sound files under 50KB each (web) or appropriately compressed (native)
- [ ] Web Audio API used with user gesture gate (no autoplay violations)
- [ ] Haptic-audio pairing designed as a unit on mobile
- [ ] Sounds match the visual design language (modern sounds for modern UI, retro for retro)
- [ ] At least 3 people have tested the sounds in context and not found them annoying
