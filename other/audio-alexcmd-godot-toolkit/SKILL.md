---
name: audio
description: Godot audio developer — use when setting up sounds, music, spatial audio, audio buses, or randomized one-shots.
type: implementation
---

# Godot Audio

> You are an expert Godot audio programmer implementing production-quality sound systems in GDScript 4.x.

## Overview

Godot's audio system is built around `AudioStreamPlayer` nodes routed through named `AudioBus` channels configured in the Audio panel. All sounds must be routed through a named bus — never directly to Master. Use `AudioStreamRandomizer` for repeated one-shots, `AudioStreamPolyphonic` for layered concurrent sounds, `AudioStreamGenerator` for procedural audio, and `AudioStreamPlayer3D` for spatial audio with optional HRTF.

## Key Nodes & APIs

| Node / API | Purpose | Key Properties |
|---|---|---|
| `AudioStreamPlayer` | 2D/non-positional playback | `stream`, `bus`, `volume_db`, `pitch_scale` |
| `AudioStreamPlayer2D` | 2D positional audio | `max_distance`, `attenuation`, `bus` |
| `AudioStreamPlayer3D` | 3D positional audio | `max_distance`, `unit_size`, `panning_strength`, `bus` |
| `AudioStreamRandomizer` | Pool-based random one-shots | `add_stream()`, `playback_mode`, `random_pitch` |
| `AudioStreamPolyphonic` | Multiple concurrent streams (4.3+) | `polyphony` |
| `AudioStreamGenerator` | Procedural PCM audio | `mix_rate`, `buffer_length` |
| `AudioStreamGeneratorPlayback` | Push frames into generator | `push_frame(Vector2)`, `get_frames_available()` |
| `AudioServer` | Bus management & metering | `get_bus_peak_volume_left_db()`, `set_bus_volume_db()` |
| `AudioEffect` | Per-bus DSP effects | `AudioEffectReverb`, `AudioEffectCompressor`, `AudioEffectEQ` |
| `Area3D` | Reverb/bus override zones | `reverb_bus`, `audio_bus_override`, `audio_bus_name` |

## Bus Architecture

Every project uses a consistent bus tree. Create these buses in **Project > Audio Buses**:

```
Master
├── Music       ← looping background tracks, crossfades
├── SFX         ← one-shots, impacts, UI sounds
│   └── SFX_Reverb   ← wet send from SFX (optional)
├── Voice       ← dialogue, VO, narration
└── Ambience    ← environmental loops, wind, room tone
```

Routing rules:
- Set `AudioStreamPlayer.bus = "SFX"` (or appropriate bus name) on every player node.
- Apply `AudioEffectCompressor` on Master to control final loudness.
- Apply `AudioEffectReverb` on a send bus; use `AudioEffectSend` on SFX to route wet signal.
- Never play to Master directly — always name a child bus.

## Core Patterns

### Pattern 1 — Randomized One-Shot (footsteps, impacts)

```gdscript
# In the inspector: assign AudioStreamRandomizer to player.stream
# Add variants via AudioStreamRandomizer.add_stream()

@onready var player: AudioStreamPlayer = $AudioStreamPlayer

func play_footstep() -> void:
    # Randomize pitch slightly before each play to avoid machine-gun effect
    player.pitch_scale = randf_range(0.9, 1.1)
    player.play()
```

### Pattern 2 — Polyphonic Layered Sounds (Godot 4.3+)

```gdscript
# Assign AudioStreamPolyphonic to player.stream
# Set polyphony count (e.g. 8) on the resource

@onready var player: AudioStreamPlayer = $AudioStreamPlayer
var playback: AudioStreamPolyphonicPlayback

func _ready() -> void:
    player.play()
    playback = player.get_stream_playback() as AudioStreamPolyphonicPlayback

func play_impact(stream: AudioStream, volume_db: float = 0.0) -> void:
    if playback:
        playback.play_stream(stream, randf_range(0.9, 1.1), volume_db)
```

### Pattern 3 — Music Crossfade

```gdscript
@onready var track_a: AudioStreamPlayer = $TrackA
@onready var track_b: AudioStreamPlayer = $TrackB

var _active: AudioStreamPlayer

func _ready() -> void:
    track_a.bus = "Music"
    track_b.bus = "Music"
    _active = track_a

func crossfade_to(new_stream: AudioStream, duration: float = 2.0) -> void:
    var outgoing := _active
    var incoming := track_b if _active == track_a else track_a

    incoming.stream = new_stream
    incoming.volume_db = -80.0
    incoming.play()

    var tween := create_tween().set_parallel(true)
    tween.tween_property(outgoing, "volume_db", -80.0, duration)
    tween.tween_property(incoming, "volume_db", 0.0, duration)
    tween.chain().tween_callback(outgoing.stop)

    _active = incoming
```

### Pattern 4 — Procedural Audio via AudioStreamGenerator

```gdscript
@onready var player: AudioStreamPlayer = $AudioStreamPlayer

var playback: AudioStreamGeneratorPlayback
const MIX_RATE := 44100.0
var phase := 0.0

func _ready() -> void:
    var gen := AudioStreamGenerator.new()
    gen.mix_rate = MIX_RATE
    gen.buffer_length = 0.1
    player.stream = gen
    player.play()
    playback = player.get_stream_playback() as AudioStreamGeneratorPlayback

func _process(_delta: float) -> void:
    var frames := playback.get_frames_available()
    for i in frames:
        var sample := sin(phase * TAU)
        playback.push_frame(Vector2(sample, sample))
        phase = fmod(phase + 440.0 / MIX_RATE, 1.0)
```

### Pattern 5 — VU Meter via AudioServer

```gdscript
func get_bus_level_db(bus_name: String) -> float:
    var idx := AudioServer.get_bus_index(bus_name)
    if idx < 0:
        return -80.0
    return AudioServer.get_bus_peak_volume_left_db(idx, 0)

func _process(_delta: float) -> void:
    var sfx_db := get_bus_level_db("SFX")
    # Map -80..0 dB to 0..1 for a progress bar
    $VUMeter.value = inverse_lerp(-80.0, 0.0, sfx_db)
```

### Pattern 6 — Area3D Reverb Zone

```gdscript
# In the scene: Area3D with CollisionShape3D children
# In the inspector on Area3D:
#   audio_bus_override = true
#   audio_bus_name = "SFX_Reverb"   ← bus with AudioEffectReverb applied
#   reverb_bus = "SFX_Reverb"
#   reverb_amount = 0.6
#   reverb_uniformity = 0.8

func setup_reverb_zone(area: Area3D, bus: String, amount: float) -> void:
    area.audio_bus_override = true
    area.audio_bus_name = bus
    area.reverb_bus = bus
    area.reverb_amount = amount
```

## Common Pitfalls

- **Leaving `max_distance` at default on `AudioStreamPlayer3D`.** The default is very large; set it explicitly (e.g. `20.0`) or sounds will audibly pop in and out at wrong distances.
- **Calling `stop()` to pause and resume.** `stop()` resets the playback position. Use `stream_paused = true` / `stream_paused = false` to pause without losing position.
- **Playing sounds directly to the Master bus.** This bypasses all mix routing and makes per-category volume control impossible. Always assign a named child bus.
- **Not calling `player.play()` before fetching `AudioStreamPolyphonicPlayback`.** `get_stream_playback()` returns `null` until `play()` has been called; cache the result after calling `play()`.
- **Forgetting to set `polyphony` on `AudioStreamPolyphonic`.** The default may be 1, which defeats the purpose. Set it to match the maximum expected concurrent voices (typically 4–16).
- **Using `AudioStreamRandomizer.random_pitch` at max range.** Large pitch ranges cause obvious chipmunk/slowdown artifacts; keep the range tight (0.9–1.1) unless intentionally stylized.

## Performance

**Polyphony limits**
- Budget a maximum of 24–32 concurrent `AudioStreamPlayer` nodes actively playing at once on desktop; 16 on mobile.
- Prefer `AudioStreamPolyphonic` over spawning many player nodes — it reuses a single player and avoids node tree overhead.
- Use `AudioStreamRandomizer` to pool streams instead of instantiating new players per event.

**Streaming vs preload**
- Preload (default) short clips under ~2 seconds (SFX, one-shots): `preload("res://sfx/hit.wav")`. Keeps latency near zero.
- Stream music and long ambient loops via `load()` or by enabling `AudioStreamOggVorbis.loop` — keeps RAM low.
- Never preload large OGG music tracks; they inflate memory significantly.

**Bus count**
- Keep the bus tree to 8 buses or fewer for typical games. Each bus adds mix overhead.
- Bypass (`bus_bypass`) inactive buses (e.g. disable the Voice bus when there is no dialogue) to reclaim CPU.
- Avoid chains longer than 3 sends (player → SFX → SFX_Reverb → Master); extra hops add latency.

**HRTF spatial audio**
- Enable per-player: `AudioStreamPlayer3D.panning_strength` controls stereo/HRTF width (0 = mono, 1 = full).
- HRTF is CPU-intensive; limit it to the 4–6 most important 3D sources per frame.
- Tag active streams for profiling: `AudioServer.set_enable_tagging_used_audio_streams(true)` (debug builds only).

## Anti-Patterns

| Wrong | Right |
|---|---|
| `player.stop()` then `player.play()` to "pause" | `player.stream_paused = true` to pause, `false` to resume |
| `AudioStreamPlayer.bus = "Master"` | Route to a named child bus: `"SFX"`, `"Music"`, etc. |
| Spawn a new `AudioStreamPlayer` node per sound event | Use `AudioStreamPolyphonic` or `AudioStreamRandomizer` |
| Preloading a 10-minute OGG music track | Load/stream it at runtime; only preload short clips |
| Hardcoding `volume_db = 0.0` everywhere | Expose volume through `AudioServer.set_bus_volume_db()` per bus |
| Leaving `AudioStreamPlayer3D.max_distance` at default | Set an explicit distance appropriate to the sound's range |

## References

- [AudioStreamPlayer — Godot Docs](https://docs.godotengine.org/en/stable/classes/class_audiostreamplayer.html)
- [AudioStreamPlayer3D — Godot Docs](https://docs.godotengine.org/en/stable/classes/class_audiostreamplayer3d.html)
- [AudioServer — Godot Docs](https://docs.godotengine.org/en/stable/classes/class_audioserver.html)
- [AudioStreamPolyphonic — Godot Docs](https://docs.godotengine.org/en/stable/classes/class_audiostreampolyphonic.html)
- [AudioStreamGenerator — Godot Docs](https://docs.godotengine.org/en/stable/classes/class_audiostreamgenerator.html)
- [AudioStreamRandomizer — Godot Docs](https://docs.godotengine.org/en/stable/classes/class_audiostreamrandomizer.html)
- [Audio buses — Godot Docs](https://docs.godotengine.org/en/stable/tutorials/audio/audio_buses.html)
- [Spatial audio — Godot Docs](https://docs.godotengine.org/en/stable/tutorials/audio/audio_streams.html)
- [Area3D (audio properties) — Godot Docs](https://docs.godotengine.org/en/stable/classes/class_area3d.html)

## Delegate to

| Task | Skill |
|---|---|
| Scene/node setup | `godot:scene` |
| GDScript audio control | `godot:coder` |
| Signal connections | `godot:signals` |
| API lookup | `godot:docs` |
