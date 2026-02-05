---
name: mmd-writing
description: Write MIDI Markdown (MMD) files with correct syntax, timing paradigms, MIDI commands, and advanced features like loops, sweeps, random values, and modulation. Use when the user wants to create or edit .mmd files, needs help with MMD syntax, is implementing MIDI automation sequences, or is troubleshooting MMD validation errors.
---

# MMD Writing Skill

## Overview

This skill helps you write MIDI Markdown (MMD) files - a human-readable, text-based format for creating MIDI sequences and live performance automation. MMD supports all MIDI devices with device-specific libraries for Neural DSP Quad Cortex, Eventide H90, and Line 6 Helix family.

## Quick Start Template

Every MMD file starts with YAML frontmatter:

```mmd
---
title: "Song or Automation Name"
author: "Your Name"
midi_format: 1          # 0=single track, 1=multi-track sync
ppq: 480                # Resolution (pulses per quarter note)
default_channel: 1      # MIDI channel 1-16
default_velocity: 100   # Note velocity 0-127
tempo: 120              # BPM
time_signature: [4, 4]  # [numerator, denominator]
---

@import "devices/quad_cortex.mmd"  # Optional device library

@define MAIN_TEMPO 120

[00:00.000]
- tempo ${MAIN_TEMPO}
- marker "Start"

[00:01.000]
- note_on 1.C4 100 1b
```

## Core Concepts

### 1. Timing Systems (Choose One Per Event)

MMD supports four timing paradigms:

**Absolute Time** (mm:ss.milliseconds):
```mmd
[00:00.000]    # Start at 0 seconds
[00:01.500]    # 1.5 seconds
[01:23.250]    # 1 minute, 23.25 seconds
```

**Musical Time** (bars.beats.ticks):
```mmd
[1.1.0]        # Bar 1, beat 1, tick 0
[2.3.240]      # Bar 2, beat 3, tick 240
```
*Requires tempo and time_signature in frontmatter*

**Relative Timing** (delta from previous):
```mmd
[+500ms]       # 500 milliseconds after previous
[+1b]          # 1 beat after previous
[+2.0.0]       # 2 bars after previous
```

**Simultaneous** (same time as previous):
```mmd
[@]            # Execute at same time as previous event
```

### 2. Essential MIDI Commands

**Notes** (with automatic note-off):
```mmd
- note_on 1.C4 100 1b           # Channel.Note Velocity Duration
- note_on 1.60 127 500ms        # Using MIDI note number
- note_on 2.D#5 80 2b           # Sharps/flats supported
```

**Program Change** (load presets):
```mmd
- program_change 1.42           # Channel.Program (0-127)
- pc 1.5                        # Shorthand
```

**Control Change** (automation):
```mmd
- control_change 1.7.127        # Channel.Controller.Value
- cc 1.7.127                    # Shorthand (Volume max)
- cc 1.10.64                    # Pan center
- cc 1.11.100                   # Expression
```

**Common CC Numbers**:
- CC#1: Mod Wheel
- CC#7: Volume
- CC#10: Pan
- CC#11: Expression
- CC#64: Sustain Pedal
- CC#74: Filter Cutoff

**Pitch Bend**:
```mmd
- pitch_bend 1.0                # Center (no bend)
- pb 1.8192                     # Alternative center
- pb 1.+2000                    # Bend up
- pb 1.-4096                    # Bend down

# Pitch bend modulation (vibrato, sweeps, envelopes)
- pb 1.wave(sine, 8192, freq=5.5, depth=5)     # Vibrato
- pb 1.curve(-4096, 4096, ease-in-out)         # Pitch sweep
- pb 1.envelope(ar, attack=0.5, release=1.0)   # Pitch envelope
```

**Aftertouch/Pressure**:
```mmd
# Channel Pressure (monophonic aftertouch)
- channel_pressure 1.64
- cp 1.64                       # Shorthand

# Polyphonic Aftertouch (per-note pressure)
- poly_pressure 1.C4.80
- pp 1.C4.80                    # Shorthand

# Pressure modulation (swells, envelopes)
- cp 1.curve(0, 127, ease-in-out)              # Pressure swell
- cp 1.envelope(adsr, attack=0.2, decay=0.1, sustain=0.8, release=0.3)
- pp 1.60.wave(sine, 64, freq=3.0, depth=40)   # Per-note vibrato
```

**Meta Events**:
```mmd
- tempo 120                     # Set BPM
- time_signature 4/4            # Set time signature
- marker "Chorus"               # Add marker
- text "Performance note"       # Add text event
```

### 3. Advanced Features

**Variables**:
```mmd
@define MAIN_TEMPO 120
@define VERSE_PRESET 10

[00:00.000]
- tempo ${MAIN_TEMPO}
- pc 1.${VERSE_PRESET}

# With expressions
@define NEXT_PRESET ${VERSE_PRESET + 1}
```

**Loops** (eliminate repetition):
```mmd
@loop 4 times at [00:00.000] every 1b
  - note_on 1.C4 100 0.5b
@end

# Drum pattern
@loop 16 times at [1.1.0] every 1b
  - note_on 10.C1 100 0.1b      # Kick
  - note_on 10.D1 80 0.1b       # Snare
@end
```

**Sweeps** (smooth automation):
```mmd
# Volume fade in
@sweep from [00:00.000] to [00:04.000] every 100ms
  - cc 1.7 ramp(0, 127)
@end

# With curve types
@sweep from [1.1.0] to [5.1.0] every 8t
  - cc 1.74 ramp(0, 127, exponential)
@end
```

Ramp types: `linear`, `exponential`, `logarithmic`, `ease-in`, `ease-out`, `ease-in-out`

**Random Values** (humanization & generative music):
```mmd
# Random velocity (60-100)
- note_on 1.C4 random(70,100) 0.5b

# Random note selection
- note_on 1.random(C3,C5) 80 0.5b

# Random CC values
- cc 1.74.random(50,90)

# In loops for variation
@loop 8 times at [00:16.000] every 0.25b
  - cc 1.74.random(40,100)
@end
```

**Supported in**: velocity, note ranges (with note names), CC values, beat durations
**NOT supported in**: timing expressions, @define values, numeric note IDs

**Modulation** (curves, waves, envelopes):

*Bezier Curves* - Smooth parameter transitions:
```mmd
- cc 1.74.curve(0, 127, ease-out)        # Natural filter opening
- cc 1.7.curve(0, 100, ease-in)          # Volume fade-in
- cc 1.11.curve(0, 127, ease-in-out)     # Expression swell
```

*Waveforms (LFO)* - Periodic modulation:
```mmd
- cc 1.1.wave(sine, 64, freq=5.0, depth=10)      # Vibrato
- cc 1.7.wave(sine, 100, freq=4.0, depth=30)     # Tremolo
- cc 1.74.wave(triangle, 64, freq=0.5, depth=60) # Filter sweep
```

*Envelopes* - Dynamic parameter shaping:
```mmd
- cc 1.74.envelope(adsr, attack=0.5, decay=0.3, sustain=0.7, release=1.0)
- cc 1.74.envelope(ar, attack=0.01, release=0.2)
- cc 1.74.envelope(ad, attack=0.02, decay=0.5)
```

**Device Libraries** (high-level control):
```mmd
@import "devices/quad_cortex.mmd"
@import "devices/eventide_h90.mmd"

# Use readable aliases instead of raw MIDI
- cortex_load 1.2.0.5       # Load setlist 2, scene 0, preset 5
- h90_preset 2.20           # Load H90 preset 20
```

Available: `quad_cortex`, `eventide_h90`, `helix`, `hx_stomp`, `hx_effects`, `hx_stomp_xl`

**Custom Aliases**:
```mmd
@alias my_preset pc.{ch}.{preset} "Load preset"

# Usage
- my_preset 1.42

# Multi-command alias
@alias cortex_load {ch}.{setlist}.{group}.{preset} "Full preset load"
  - cc {ch}.32.{setlist}
  - cc {ch}.0.{group}
  - pc {ch}.{preset}
@end

# With defaults and enums
@alias volume_set {ch}.{value=100} "Set volume"
  - cc {ch}.7.{value}
@end

@alias routing {ch}.{mode=series:0,parallel:1} "Set routing"
  - cc {ch}.85.{mode}
@end
```

**Comments**:
```mmd
# Single line comment

## Section header (H2 style)

- pc 1.5    # Inline comment

/*
  Multi-line comment block
*/

// C-style comment
```

## Common Patterns

See [EXAMPLES.md](EXAMPLES.md) for comprehensive pattern library including:
- Drum patterns (GM drum map on channel 10)
- Chord progressions
- Volume automation (fades, swells)
- Expression pedal automation
- Humanized hi-hat patterns
- Generative ambient pads

## Validation Rules

**Critical Rules** (avoid these errors):

1. ✅ **Always start with timing marker**
   ```mmd
   [00:00.000]
   - note_on 1.C4 100 1b
   ```

2. ✅ **Timing must increase monotonically**
   ```mmd
   [00:05.000]
   - note_on 1.C4 100 1b
   [00:10.000]  # Must be after 00:05.000
   - note_on 1.D4 100 1b
   ```

3. ✅ **MIDI value ranges**
   - Values: 0-127
   - Channels: 1-16
   - Notes: 0-127 (C-1 to G9)
   - Pitch bend: -8192 to +8191 or 0 to 16383

4. ✅ **No random() in timing or @define**
   ```mmd
   # ❌ Wrong
   [00:08.random(-10,10)]
   @define VEL random(40,60)

   # ✅ Correct
   [00:08.000]
   - note_on 1.C4 random(40,60) 1b
   ```

## Best Practices

1. **Use musical timing for music** - Adjusts with tempo changes
2. **Use variables for reusable values** - Easier to maintain
3. **Add comments and markers** - Improves readability
4. **Use loops to avoid repetition** - Cleaner, more maintainable
5. **Import device libraries** - More readable than raw MIDI
6. **Validate before compiling** - Catch errors early

## Workflow

```bash
# 1. Write MMD file
# 2. Validate syntax
mmdc validate song.mmd

# 3. Inspect events
mmdc inspect song.mmd

# 4. Compile to MIDI
mmdc compile song.mmd -o output.mid

# 5. Test playback
mmdc play song.mmd --port 0
```

## Additional Resources

- **REFERENCE.md** - Complete syntax reference and detailed explanations
- **EXAMPLES.md** - Pattern library with working examples
- **spec.md** - Complete MMD language specification (in project root)
- **examples/** - 49 working example files organized by category
- **docs/user-guide/** - User documentation
- **docs/dev-guides/** - Developer implementation guides

## Related Skills

- **mmd-cli** - For compiling, validating, playing MMD files, and managing device libraries
- **mmd-device-library** - For creating custom device libraries
- **mmd-debugging** - For troubleshooting MMD files

## Quick Syntax Reference

| Element | Syntax | Example |
|---------|--------|---------|
| Timing (absolute) | `[mm:ss.ms]` | `[00:30.500]` |
| Timing (musical) | `[bar.beat.tick]` | `[4.2.240]` |
| Timing (relative) | `[+duration]` | `[+500ms]`, `[+1b]` |
| Timing (simultaneous) | `[@]` | `[@]` |
| Note on | `note_on ch.note vel dur` | `note_on 1.C4 100 1b` |
| Control change | `cc ch.controller.value` | `cc 1.7.127` |
| Program change | `pc ch.program` | `pc 1.42` |
| Pitch bend | `pb ch.value` | `pb 1.8192` |
| Channel pressure | `cp ch.value` | `cp 1.64` |
| Poly pressure | `pp ch.note.value` | `pp 1.C4.80` |
| Variable | `@define NAME value` | `@define TEMPO 120` |
| Variable use | `${NAME}` | `${TEMPO}` |
| Loop | `@loop N times...@end` | See above |
| Sweep | `@sweep from...to...@end` | See above |
| Random | `random(min,max)` | `random(60,100)` |
| Import | `@import "path"` | `@import "devices/..."` |

For complete documentation, see the additional resource files in this skill directory.
