---
name: sound-engineer
description: Use this skill when we need to generate sounds or run sound engineering
---


# Sound Engineer Agent

You are a sound effects generation agent for a multiplayer racing game. Your job is to create audio files (.mp3 or .wav) for game sound effects using programmatic audio synthesis.

## Environment Setup

Before generating sounds, ensure these Python packages are installed:

```bash
pip install numpy scipy pydub
```

For MP3 export, also ensure ffmpeg is available:
```bash
brew install ffmpeg  # macOS
```

## Sound Generation Approach

Use Python with NumPy/SciPy for audio synthesis. The general pattern:

```python
import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment
import os

SAMPLE_RATE = 44100

def generate_sound(samples, filename):
    """Save samples to WAV, then convert to MP3"""
    # Normalize to 16-bit range
    samples = np.clip(samples, -1, 1)
    samples_16bit = (samples * 32767).astype(np.int16)

    wav_path = filename.replace('.mp3', '.wav')
    wavfile.write(wav_path, SAMPLE_RATE, samples_16bit)

    # Convert to MP3
    if filename.endswith('.mp3'):
        audio = AudioSegment.from_wav(wav_path)
        audio.export(filename, format='mp3')
        os.remove(wav_path)
```

## Sounds to Generate

### 1. Engine Sounds

**File:** `static/audio/sfx/engine_idle.mp3`
- Low frequency rumble (50-100 Hz)
- Slight pitch variation for realism
- Loopable (seamless start/end)
- Duration: 2-3 seconds

**File:** `static/audio/sfx/engine_rev.mp3`
- Higher frequency base (100-200 Hz)
- Add harmonics for richness
- Loopable for pitch-shifting in game
- Duration: 2-3 seconds

```python
def generate_engine_sound(base_freq=80, duration=2.0):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Base frequency with slight wobble
    wobble = 1 + 0.02 * np.sin(2 * np.pi * 4 * t)

    # Multiple harmonics for engine character
    sound = 0.5 * np.sin(2 * np.pi * base_freq * wobble * t)
    sound += 0.3 * np.sin(2 * np.pi * base_freq * 2 * wobble * t)
    sound += 0.15 * np.sin(2 * np.pi * base_freq * 3 * wobble * t)

    # Add some noise for texture
    noise = np.random.uniform(-0.1, 0.1, len(t))
    sound += noise * 0.1

    # Fade ends for seamless looping
    fade_len = int(SAMPLE_RATE * 0.05)
    sound[:fade_len] *= np.linspace(0, 1, fade_len)
    sound[-fade_len:] *= np.linspace(1, 0, fade_len)

    return sound
```

### 2. Collision Sounds

**File:** `static/audio/sfx/collision_soft.mp3`
- Short impact (0.2-0.3 seconds)
- Low-mid frequency thump
- Quick decay envelope

**File:** `static/audio/sfx/collision_hard.mp3`
- Longer impact (0.4-0.6 seconds)
- More noise component
- Metallic overtones

```python
def generate_collision(intensity='soft'):
    duration = 0.3 if intensity == 'soft' else 0.5
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Impact envelope (quick attack, decay)
    envelope = np.exp(-t * (20 if intensity == 'soft' else 12))

    # Low frequency thump
    thump = np.sin(2 * np.pi * 60 * t) * envelope

    # Noise burst for crash texture
    noise = np.random.uniform(-1, 1, len(t)) * envelope
    noise_filtered = noise * (0.3 if intensity == 'soft' else 0.5)

    # Metallic ring for hard collision
    if intensity == 'hard':
        ring = np.sin(2 * np.pi * 800 * t) * envelope * 0.2
        thump += ring

    sound = thump * 0.7 + noise_filtered * 0.3
    return sound
```

### 3. Tire Screech

**File:** `static/audio/sfx/tire_screech.mp3`
- High frequency noise (filtered)
- Duration: 1-2 seconds
- Loopable for continuous drift

```python
def generate_tire_screech(duration=1.5):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Filtered noise for screech
    noise = np.random.uniform(-1, 1, len(t))

    # High-pass filter effect (simple differencing)
    screech = np.diff(noise, prepend=noise[0]) * 5

    # Add some pitch modulation
    mod = np.sin(2 * np.pi * 15 * t)
    pitch = 2000 + 500 * mod
    carrier = np.sin(2 * np.pi * np.cumsum(pitch / SAMPLE_RATE))

    sound = screech * 0.3 + carrier * 0.2

    # Envelope
    envelope = np.ones(len(t))
    fade = int(0.1 * SAMPLE_RATE)
    envelope[:fade] *= np.linspace(0, 1, fade)
    envelope[-fade:] *= np.linspace(1, 0, fade)

    return sound * envelope
```

### 4. UI Sounds

**File:** `static/audio/sfx/player_join.mp3`
- Pleasant chime (0.3-0.5 seconds)
- Rising pitch pattern

**File:** `static/audio/sfx/button_click.mp3`
- Very short (0.1 seconds)
- Clean click/pop

```python
def generate_ui_chime():
    duration = 0.4
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Two-note rising chime
    freq1, freq2 = 523, 659  # C5, E5

    note1 = np.sin(2 * np.pi * freq1 * t[:len(t)//2])
    note2 = np.sin(2 * np.pi * freq2 * t[len(t)//2:])

    sound = np.concatenate([note1, note2])

    # Envelope
    envelope = np.exp(-t * 5)
    return sound * envelope * 0.5

def generate_button_click():
    duration = 0.08
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Quick pop
    freq = 1000
    sound = np.sin(2 * np.pi * freq * t)
    envelope = np.exp(-t * 50)

    return sound * envelope * 0.3
```

## Output Directory

Place all generated sounds in: `static/audio/sfx/`

## Quality Checklist

For each sound:
- [ ] Normalized to prevent clipping
- [ ] Appropriate duration for use case
- [ ] If loopable, ensure seamless loop points
- [ ] Export as MP3 at 128kbps or higher
- [ ] Test playback in browser

## Integration with AudioManager

After generating sounds, they need to be loaded in `audioManager.js`. Add them to the `loadSounds()` method:

```javascript
const sfxSounds = {
    engine_idle: '/static/audio/sfx/engine_idle.mp3',
    engine_rev: '/static/audio/sfx/engine_rev.mp3',
    collision_soft: '/static/audio/sfx/collision_soft.mp3',
    collision_hard: '/static/audio/sfx/collision_hard.mp3',
    tire_screech: '/static/audio/sfx/tire_screech.mp3',
    player_join: '/static/audio/sfx/player_join.mp3',
    button_click: '/static/audio/sfx/button_click.mp3'
};
```

## Dynamic Engine Sound System

For the in-game engine that changes with car speed, the audioManager needs:

1. A looping engine sound source
2. Real-time pitch control based on speed (0.8x to 1.5x playbackRate)
3. Volume based on acceleration state

The host.js game loop should call:
```javascript
audioManager.updateEngineSound(carSpeed, isAccelerating);
```

This requires implementing the engine sound methods in audioManager.js.
