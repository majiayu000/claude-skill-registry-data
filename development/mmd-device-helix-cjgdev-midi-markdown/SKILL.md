---
name: mmd-device-helix
description: Guide for using the Line 6 Helix Floor/LT/Rack device library in MMD files. Use when the user mentions Helix, Line 6 Helix guitar processor, Helix Floor, Helix LT, Helix Rack, or needs help with setlist/preset loading, 8-snapshot control, expression automation, footswitch control, or looper functionality.
---

# Line 6 Helix Floor/LT/Rack Usage Guide

Expert guidance for using the Helix device library in MIDI Markdown files.

## When to Use This Skill

Invoke this skill when working with:
- Line 6 Helix Floor, LT, or Rack guitar processors
- Helix preset and setlist management
- 8-snapshot control (full range)
- Helix expression pedal automation (EXP1, EXP2, EXP3)
- 11 footswitch control (FS1-5, FS7-11)
- Helix Looper functionality
- Command Center macros for external gear

## Quick Start

### Import the Library

```mml
@import "devices/helix.mmd"
```

### Basic Preset Loading

```mml
[00:00.000]
# Load Setlist 1 (CC32=0), Preset 6 (PC=5)
- helix_load 1 0 5

# Load preset and switch to snapshot
- helix_load_snapshot 1 0 5 2  # Setlist 1, Preset 6, Snapshot 3
```

### Snapshot Control

```mml
[00:00.000]
# Named snapshots (1-8)
- helix_snap_1 1
- helix_snap_2 1
- helix_snap_3 1

# Parameterized (0-7)
- helix_snapshot 1 3  # Snapshot 4
```

## Critical Firmware Timing Requirements

### Firmware 3.5x: Conservative Timing Required

**CRITICAL**: Add **350ms delay** after ALL Program Change messages before sending CC

```mml
# ❌ WRONG - No delay (firmware 3.5x)
[00:00.000]
- pc 1.10
- cc 1.69.2  # Snapshot might be ignored!

# ✅ CORRECT - Use helper with delays
[00:00.000]
- helix_load_snapshot 1 0 10 2  # Built-in 350ms delay
```

### Firmware 3.10+: Improved Timing

**Improvement**: CC69 (snapshot) messages are buffered during preset load

**Still recommended**: Use 350ms delay for safety with complex presets

### Firmware 3.80 (Current): Stable

**Known Issue**: MIDI Clock Rx doesn't apply on preset change

**Workaround**: Use Tap Tempo (CC64) after preset changes if tempo sync is critical

## Preset and Setlist Management

### Understanding Helix Addressing

**Structure**: 8 Setlists × 128 Presets = 1024 total presets

**Addressing**:
- CC0 (Bank MSB) + CC32 (Bank LSB) = Setlist selector
- CC32 values 0-7 select Setlists 1-8
- PC values 0-127 select Presets 1-128 within active setlist

### Complete Preset Load

```mml
[00:00.000]
# Load Setlist 3, Preset 20
- helix_load 1 2 19  # CC32=2, PC=19 (0-indexed)

# With specific snapshot
- helix_load_snapshot 1 2 19 3  # Snapshot 4

# Direct setlist selection
- helix_setlist 1 2  # Setlist 3

# Direct preset within current setlist
- helix_preset 1 19  # Preset 20
```

## Snapshot Control (8 Snapshots)

### Full 8-Snapshot Range

The Helix Floor/LT/Rack has **8 snapshots** (0-7), providing maximum flexibility for live performance.

```mml
[00:00.000]
# Named snapshots
- helix_snap_1 1  # Snapshot 1
- helix_snap_2 1  # Snapshot 2
- helix_snap_3 1  # Snapshot 3
- helix_snap_4 1  # Snapshot 4
- helix_snap_5 1  # Snapshot 5
- helix_snap_6 1  # Snapshot 6
- helix_snap_7 1  # Snapshot 7
- helix_snap_8 1  # Snapshot 8

# Parameterized
- helix_snapshot 1 7  # Snapshot 8
```

### 8-Snapshot Song Arrangement

```mml
[00:00.000]
- helix_load 1 0 5  # Load song preset

# Intro - Clean
- helix_snap_1 1

# Verse - Rhythm
[00:16.000]
- helix_snap_2 1

# Pre-Chorus - Add delay
[00:28.000]
- helix_snap_3 1

# Chorus - Drive + reverb
[00:32.000]
- helix_snap_4 1

# Bridge - Ambient
[00:48.000]
- helix_snap_5 1

# Solo - Lead tone
[01:04.000]
- helix_snap_6 1

# Breakdown - Clean + tremolo
[01:20.000]
- helix_snap_7 1

# Final chorus - Epic lead
[01:36.000]
- helix_snap_8 1
```

## Expression Pedal Control

### Three Expression Pedals

Helix Floor/Rack models have **3 expression pedals** (EXP1, EXP2, EXP3).

```mml
[00:00.000]
# Direct MIDI values (0-127)
- line6_exp1 1 64   # From common library
- line6_exp2 1 100
- helix_exp3 1 80   # EXP3 is Helix-specific

# With modulation curves
- line6_exp_swell 1 1 0 127  # Smooth EXP1 swell
- helix_exp3_swell 1 0 127   # Smooth EXP3 swell
```

### Advanced Expression Modulation

```mml
[00:00.000]
# Vibrato effect
- line6_exp_vibrato 1 1 64 2.5 20
# Params: ch, exp_num, center, freq(Hz), depth(%)

# Tremolo effect
- line6_exp_tremolo 1 1 64 4.0 30

# ADSR envelope
- line6_exp_envelope 1 1

# Attack-Release envelope
- line6_exp_ar 1 1 0.5 1.0
```

## Footswitch Control

### 11 Footswitches Available

Full Helix models have **11 footswitches** (FS1-5, FS7-11). FS6 is reserved for internal use.

```mml
[00:00.000]
# Toggle footswitches (ALWAYS toggle, can't force on/off)
- line6_fs1 1
- line6_fs2 1
- line6_fs3 1
- line6_fs4 1
- line6_fs5 1
# FS6 is RESERVED
- line6_fs7 1
- line6_fs8 1
- line6_fs9 1
- line6_fs10 1
- line6_fs11 1
```

**Important**: Helix footswitches ALWAYS toggle. Cannot force on/off via MIDI.

## Looper Control

### Basic Looper Workflow

```mml
[00:00.000]
# Start recording
- line6_looper_start_recording 1

[+8s]
# Switch to playback
- line6_looper_playback 1

[+16s]
# Overdub
- line6_looper_overdub 1

[+24s]
# Stop and exit
- line6_looper_stop_exit 1
```

### Complete Looper Functions

```mml
[00:00.000]
# Record/Overdub/Play
- line6_looper_rec_play 1
- line6_looper_overdub 1
- line6_looper_playback 1

# Reverse and half speed
- line6_looper_reverse 1
- line6_looper_halfspeed 1

# Undo/redo
- line6_looper_undo 1

# Stop and clear
- line6_looper_stop_exit 1
```

## Tap Tempo

```mml
[00:00.000]
# Send 4 taps at 120 BPM (500ms intervals)
- line6_tap 1
[+500ms]
- line6_tap 1
[+500ms]
- line6_tap 1
[+500ms]
- line6_tap 1
```

## Command Center Macros

### Controlling External Gear

Command Center allows Helix to send MIDI to external devices.

```mml
[00:00.000]
# Load Helix preset and switch external amp channel
- helix_preset_with_amp_switch 1 0 5 2 10
# Params: ch, setlist, preset, amp_channel, delay_preset

# Load Helix preset, send PC to amp, PC to delay

# Snapshot change with external reverb mix
- helix_snapshot_with_reverb 1 3 64
# Params: ch, snapshot, reverb_mix_value
```

### Complete Song Section Macro

```mml
[00:00.000]
# Complete section: preset + snapshot + tempo
- helix_song_section 1 10 2 120
# Params: ch, section_preset, snapshot, tempo_bpm
```

## Common Workflow Patterns

### Song-Based Preset Organization

```mml
[00:00.000]
# Song 1: Load preset, use snapshots for sections
- helix_load 1 0 0  # Setlist 1, Preset 1

# Intro
- helix_snap_1 1

# Verse
[00:16.000]
- helix_snap_2 1

# Chorus
[00:32.000]
- helix_snap_3 1

# Solo
[00:48.000]
- helix_snap_4 1
```

### Setlist Organization Strategy

**Recommended**:
- Setlist 1: Covers/Standards
- Setlist 2: Originals Set 1
- Setlist 3: Originals Set 2
- Setlist 4-8: Special projects, recording, etc.

## Reserved CC Numbers

### Helix-Specific Reserved CCs

```
CC0   - Bank Select MSB
CC3   - Expression Pedal 3 (Helix Floor/Rack only)
CC32  - Bank Select LSB (Setlist selector)
CC64  - Tap Tempo
CC68  - Amp/Cab toggle
CC69  - Snapshot select
CC70-76 - Reserved for future use
```

All other CC numbers (4-31, 33-48, 77-127) are available for:
- Block bypass control (via MIDI Learn)
- Parameter control (via MIDI Learn)
- Custom assignments per preset

## Firmware-Specific Best Practices

### Firmware 3.5x

```mml
# ✅ Add 350ms after ALL PC messages
[00:00.000]
- pc 1.10
[+350ms]
- cc 1.69.2  # Now snapshot will work

# ✅ Add 100ms between rapid CC messages
[00:00.000]
- cc 1.51.64
[+100ms]
- cc 1.52.80

# ✅ Use snapshot-based workflow to avoid PC delays
```

### Firmware 3.10+

```mml
# ✅ CC69 is buffered - can reduce delays to +50ms
[00:00.000]
- pc 1.10
[+50ms]
- cc 1.69.2

# ✅ Still recommend +350ms for safety with complex presets
```

### Firmware 3.80 (Current)

```mml
# ✅ Use Tap Tempo after preset changes if tempo sync critical
[00:00.000]
- pc 1.10
[+350ms]
- line6_tap 1  # Sync tempo
```

## Connection Recommendations

### 5-Pin DIN MIDI vs USB

**Helix Floor/LT/Rack has both:**
- 5-pin DIN MIDI (In/Out/Thru)
- USB MIDI

**For MIDI Clock (sync)**:
- ✅ **Prefer 5-pin DIN** - lower jitter, more reliable
- ❌ USB MIDI has higher jitter

**For general control**:
- Either works fine
- USB is more convenient for DAW integration

**For live performance**:
- 5-pin DIN is more robust
- Easier hardware daisy-chaining
- Optical isolation (no ground loops)

## Common Mistakes and Fixes

### Mistake 1: No Delay After PC (Firmware 3.5x)

```mml
# ❌ WRONG
[00:00.000]
- pc 1.10
- cc 1.69.2  # Ignored!

# ✅ CORRECT
[00:00.000]
- helix_load_snapshot 1 0 10 2  # Built-in delay
```

### Mistake 2: Trying to Force Footswitch On/Off

```mml
# ❌ WRONG - Footswitches always toggle
[00:00.000]
- cc 1.51.0    # Trying to force off
- cc 1.51.127  # Trying to force on

# ✅ CORRECT - Use toggle commands
[00:00.000]
- line6_fs1 1  # Toggles state
```

### Mistake 3: Using USB MIDI for Clock

```mml
# ⚠️ SUBOPTIMAL - USB has jitter
# Use 5-pin DIN for MIDI Clock instead
```

## Comparison: Helix vs HX Models

### Helix Floor/LT/Rack (You Are Here)

- ✅ **8 snapshots** (maximum flexibility)
- ✅ **11 footswitches** (Floor/LT)
- ✅ **3 expression pedals** (Floor/Rack)
- ✅ **5-pin DIN MIDI** (hardware chaining)
- ✅ Dual DSP path
- ✅ Full Command Center
- ❌ Larger footprint

### HX Stomp XL

- ⚠️ **4 snapshots** (good for most songs)
- ⚠️ **8 footswitches** (adequate)
- ⚠️ **2 expression pedals**
- ❌ **USB MIDI only** (no 5-pin DIN)
- ❌ Single DSP path
- ✅ Command Center (enhanced vs HX Stomp)
- ✅ Smaller footprint

### HX Stomp

- ❌ **3 snapshots** (limited)
- ❌ **5 footswitches** (limited)
- ⚠️ **2 expression pedals**
- ❌ **USB MIDI only**
- ❌ Single DSP path
- ⚠️ Limited Command Center
- ✅ Smallest footprint

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Snapshots don't switch | Add 350ms delay after PC (firmware 3.5x) or use 3.10+ |
| Footswitches don't work | Helix footswitches toggle only, can't force on/off |
| Expression is glitchy | Send smooth CC curves, check MIDI rate limiting |
| MIDI timing is sloppy | Use 5-pin DIN instead of USB for clock |
| Preset changes ignored | Check MIDI Base Channel in Global Settings |
| Tempo doesn't sync on PC | Use Tap Tempo (CC64) after preset change (firmware 3.80) |

## Reference

### Device Library Location
- Main: `devices/helix.mmd`
- Common: `devices/line6_common.mmd` (imported automatically)

### Documentation
- Official Manual: https://line6.com/support/manuals/helix
- Firmware Notes: https://line6.com/software/reaper-extension

### Firmware Version
3.80 (current as of library version)

## See Also

- [HX Stomp Usage](../hx-stomp-usage/SKILL.md) - 3 snapshots, USB only
- [HX Stomp XL Usage](../hx-stomp-xl-usage/SKILL.md) - 4 snapshots, 8 footswitches
- [HX Effects Usage](../hx-effects-usage/SKILL.md) - Effects only, 4 snapshots
- [MMD Syntax Reference](../../spec.md)
- [Line 6 Common Library](../../devices/line6_common.mmd)
- [Modulation Guide](../../docs/user-guide/generative-music.md)
