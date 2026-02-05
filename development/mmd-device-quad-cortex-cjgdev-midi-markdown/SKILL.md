---
name: mmd-device-quad-cortex
description: Guide for using the Neural DSP Quad Cortex device library in MMD files. Use when the user mentions Quad Cortex, QC, Neural DSP guitar processor, or needs help with preset loading, scene switching, expression control, or stomp automation for the Quad Cortex.
---

# Neural DSP Quad Cortex Usage Guide

Expert guidance for using the Quad Cortex device library in MIDI Markdown files.

## When to Use This Skill

Invoke this skill when working with:
- Neural DSP Quad Cortex guitar processor
- Quad Cortex preset loading and scene switching
- QC expression pedal automation
- Stomp footswitch control
- Looper X control
- Quad Cortex MIDI timing issues
- Live performance automation for QC

## Quick Start

### Import the Library

```mml
@import "devices/quad_cortex.mmd"
```

### Basic Preset Loading

```mml
[00:00.000]
# Load Setlist 1, Group 0, Preset 5
- qc_load_preset 1 0 0 5

# Or use simplified version (first 128 presets)
- qc_load_preset_simple 1 0 5
```

### Scene Switching

```mml
[00:16.000]
# Switch to Scene B
- qc_scene_b 1

# Or use parameterized version
- qc_scene 1 1
```

## Critical Known Issues

### 1. Scene Switching Latency (100-130ms)

**Problem**: MIDI scene changes via CC#43 have significant latency in CorOS 2.0+

**Symptoms**:
- Scene changes lag behind backing tracks
- Timing sync issues in DAW automation

**Workarounds**:
```mml
# Workaround 1: Send scene change early (in DAW)
[00:15.900]  # 100ms before the beat
- qc_scene 1 2

# Workaround 2: Use expression swell to mask latency
[00:16.000]
- qc_scene_with_swell 1 2  # Fades expression to hide latency

# Workaround 3: Enable "Ignore Duplicate PC" in device settings
```

**System Recommendations**:
- Enable "Ignore Duplicate PC" in Quad Cortex MIDI Settings
- Use -50ms track delay compensation on MIDI tracks in DAW
- Send scene changes 1/16 note early

### 2. Rapid MIDI Messages Can Freeze Device

**Problem**: Sending rapid successive CC messages can freeze the device

**Critical**: ALWAYS add minimum 100ms delays between CC messages

**Safe Expression Automation**:
```mml
# ❌ WRONG - No delays, can freeze device
[00:00.000]
- cc 1.1.0
- cc 1.1.42
- cc 1.1.85
- cc 1.1.127

# ✅ CORRECT - Use safe helper with enforced delays
[00:00.000]
- qc_exp1_step_automation 1

# ✅ CORRECT - Use safe ramp helper
[00:00.000]
- qc_exp1_safe_ramp 1 0 127
```

### 3. MIDI Thru is Broken

**Problem**: When MIDI Thru is enabled, device stops sending its own MIDI messages

**Solution**:
- Keep MIDI Thru OFF
- Use external MIDI merger if you need to combine signals

### 4. Preset Loading Timing Requirements

**Critical**: Must wait 100ms between Bank/Setlist/PC messages

```mml
# ✅ CORRECT - qc_load_preset includes proper delays
[00:00.000]
- qc_load_preset 1 0 0 5

# This expands to:
# - cc 1.0.0      # Bank group
# [+100ms]
# - cc 1.32.0     # Setlist
# [+100ms]
# - pc 1.5        # Preset
```

**Never manually construct this sequence without delays!**

### 5. Expression Pedal MIDI Latency

**Problem**: CC#1/CC#2 have noticeable lag compared to physical pedals

**Recommendations**:
- ❌ Avoid MIDI for real-time wah or volume control
- ✅ Use physical expression pedals connected to EXP 1/2 jacks
- ✅ Use MIDI expression for slow parameter changes only
- ✅ Pre-programmed automation is acceptable

## Preset and Scene Management

### Complete Preset Load Sequence

```mml
[00:00.000]
# Full preset load (group 0, setlist 2, preset 10)
- qc_load_preset 1 0 2 10

# Simplified (first 128 presets)
- qc_load_preset_simple 1 2 10

# Preset + Scene combo
- qc_load_preset_scene 1 2 10 3  # Load preset 10, scene D
```

### Scene Control

```mml
[00:00.000]
# Named scenes (A-H)
- qc_scene_a 1
- qc_scene_b 1
- qc_scene_c 1

# Parameterized (0-7 for scenes A-H)
- qc_scene 1 3  # Scene D

# Scene change with expression swell (masks latency)
- qc_scene_with_swell 1 4  # Scene E with crossfade
```

## Stomp Footswitch Control

### Basic Footswitch Control

```mml
[00:00.000]
# Explicit on/off (64+ = active, 0-63 = bypass)
- qc_stomp_a_on 1
- qc_stomp_b_on 1

[00:08.000]
- qc_stomp_a_off 1

# Toggle mode (any value toggles)
- qc_stomp_c 1 127  # Toggles footswitch C
```

### Emergency Cutoff

```mml
[02:00.000]
# Bypass all footswitches (song ending)
- qc_all_stomps_off 1
```

## Expression Pedal Control

### Basic Expression

```mml
[00:00.000]
# Direct MIDI value (0-127)
- qc_exp1 1 64

# Percentage (0-100)
- qc_exp1_percent 1 50

# With modulation curves
- qc_exp1_swell 1 0 127       # Smooth swell with ease-in-out
- qc_exp1_fade_in 1            # 0 to 127 with exponential curve
- qc_exp1_fade_out 1           # 127 to 0 with logarithmic curve
```

### Advanced Expression Modulation

```mml
[00:00.000]
# Vibrato effect using wave modulation
- qc_exp1_vibrato 1 64 5.5 10  # Center=64, freq=5.5Hz, depth=10%

# Tremolo effect
- qc_exp1_tremolo 1 64 4.0 30  # Center=64, freq=4Hz, depth=30%

# ADSR envelope
- qc_exp1_envelope 1

# Attack-Release envelope
- qc_exp1_ar 1 0.5 1.0  # Attack=0.5s, Release=1.0s
```

## Looper X Control

### Basic Looper Workflow

```mml
[00:00.000]
# Open looper
- qc_looper_open 1

[+150ms]
# Start recording (momentary: send 127 then 0)
- qc_looper_record 1
[+100ms]
- qc_looper_stop 1

# Switch to playback
[+4s]
- qc_looper_play 1

# Close when done
[+8s]
- qc_looper_close 1
```

### Safe Looper Workflow

```mml
[00:00.000]
# Complete workflow with safe timing
- qc_looper_safe_workflow 1
```

### Looper Features

```mml
[00:00.000]
# Toggle features
- qc_looper_reverse 1      # Enable/disable reverse
- qc_looper_halfspeed 1    # Enable/disable half speed
- qc_looper_oneshot 1      # Enable/disable one shot
- qc_looper_undo 1         # Undo/redo

# Set quantize (0=off, 1-8=beats, 9=16 beats)
- qc_looper_quantize 1 4   # 4 beat quantize
```

## Tempo and Tuner

### Tempo Control

```mml
[00:00.000]
# MIDI value (0-127)
- qc_tempo 1 64

# BPM (40-300)
- qc_tempo_bpm 1 120
```

### Tuner Control

```mml
[00:00.000]
# Toggle tuner
- qc_tuner_on 1
[+5s]
- qc_tuner_off 1
```

## Mode Switching

```mml
[00:00.000]
# Switch modes
- qc_mode_preset 1    # Preset mode
- qc_mode_scene 1     # Scene mode
- qc_mode_stomp 1     # Stomp mode

# Temporary mode switch
- qc_temp_stomp_mode 1 35 0  # Switch to stomp, toggle FS A, return to preset
```

## Advanced Workflow Macros

### Complete Song Section Change

```mml
[00:00.000]
# Load preset, scene, and set expression
- qc_song_section 1 2 10 3 100
# Params: channel, setlist, preset, scene, exp1_value
```

### DAW Initialization

```mml
[00:00.000]
# Configure QC for DAW control
- qc_daw_init 1

# This enables:
# - Ignore Duplicate PC
# - Stomp mode
# - Closes Gig View
# - Disables tuner
```

## Connection Recommendations

### MIDI Connection Best Practices

**Preferred**: 5-pin DIN MIDI cables
- More reliable than USB MIDI
- Lower latency
- Better isolation

**If using both**:
- Disconnect USB when using DIN to prevent conflicts
- Turn off MIDI Thru when using with DAWs

**DAW Integration**:
- Disable MIDI Timecode (MTC) to prevent random preset changes
- Disable MIDI Chase for CC messages
- Enable "Ignore Duplicate PC" in Quad Cortex
- Use specific MIDI channels, not "All"

## Common Mistakes and Fixes

### Mistake 1: Rapid CC Updates Without Delays

```mml
# ❌ WRONG - Can freeze device
[00:00.000]
- cc 1.1.0
- cc 1.1.32
- cc 1.1.64
- cc 1.1.96
- cc 1.1.127

# ✅ CORRECT - Use safe helper
[00:00.000]
- qc_exp1_safe_ramp 1 0 127
```

### Mistake 2: Scene Change Without Latency Compensation

```mml
# ❌ WRONG - Will be late
[00:16.000]
- qc_scene 1 2

# ✅ CORRECT - Send early or use crossfade
[00:15.900]  # 100ms early
- qc_scene 1 2

# Or use crossfade helper
[00:16.000]
- qc_scene_with_swell 1 2
```

### Mistake 3: Missing Delays in Preset Load

```mml
# ❌ WRONG - Manual sequence without delays
[00:00.000]
- cc 1.0.0
- cc 1.32.2
- pc 1.10

# ✅ CORRECT - Use helper with built-in delays
[00:00.000]
- qc_load_preset 1 0 2 10
```

## Performance Tips

### Reliability Checklist

✅ Enable "Ignore Duplicate PC" in device settings
✅ Use MIDI DIN cables instead of USB for live performance
✅ Turn off MIDI Thru on the device
✅ Add 100ms spacing between all CC messages
✅ Keep firmware updated but test before gigs
✅ Use safe expression automation aliases

### Mode Strategy

**Recommended**: Stay in Stomp Mode
- Use CC#43 for scene changes even while in Stomp Mode
- Creates "8x8 hybrid" control (8 stomps × 8 scenes)
- Use temporary mode switching for specific needs

### Expression Strategy

**Connect physical expression pedals directly**:
- Avoid MIDI CC#1/CC#2 for real-time wah/volume
- Use MIDI expression for slow parameter changes only
- Always include timing delays between expression updates
- Use `qc_exp1_safe_ramp` and similar helpers

## Reference

### Device Library Location
`devices/quad_cortex.mmd`

### Documentation
- Official MIDI Spec: https://support.neuraldsp.com/hc/en-us/articles/360014480320-MIDI-Specification
- MIDI PC Calculator: https://support.neuraldsp.com/help/quad-cortex-midi-pc-calculator

### Firmware Version
CorOS 3.2.1 (as of library version 1.0.0)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Scene changes are late | Enable "Ignore Duplicate PC", send early, or use crossfade |
| Device freezes with CC | Add 100ms delays, use safe automation helpers |
| Expression pedal is laggy | Use physical pedals, not MIDI CC |
| Preset won't load | Check timing delays (100ms minimum) |
| MIDI conflicts | Disable MIDI Thru, use specific channels |
| Random preset changes | Disable MIDI Timecode in DAW |

## See Also

- [MMD Syntax Reference](../../spec.md)
- [Device Library Creation](../../docs/user-guide/device-libraries.md)
- [Timing System](../../docs/dev-guides/timing-system.md)
- [Modulation Guide](../../docs/user-guide/generative-music.md)
