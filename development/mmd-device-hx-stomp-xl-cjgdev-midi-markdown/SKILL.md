---
name: mmd-device-hx-stomp-xl
description: Guide for using the Line 6 HX Stomp XL device library in MMD files. Use when the user mentions HX Stomp XL, Stomp XL processor, or needs help with 4-snapshot control, 8 footswitch control, USB MIDI setup, All Bypass, Mode switching, or comparison with HX Stomp and full Helix.
---

# Line 6 HX Stomp XL Usage Guide

Expert guidance for using the HX Stomp XL device library in MIDI Markdown files.

## When to Use This Skill

Invoke this skill when working with:
- Line 6 HX Stomp XL compact guitar processor
- 4-snapshot control (middle ground)
- 8 footswitch control (double HX Stomp)
- USB MIDI-only connectivity
- All Bypass control
- Mode switching
- Direct PC addressing (no bank select)

## Quick Start

### Import the Library

```mml
@import "devices/hx_stomp_xl.mmd"
```

### Basic Preset Loading

```mml
[00:00.000]
# Load preset 5 (direct PC, no bank select)
- hxstompxl_preset 1 5

# Load preset and switch to snapshot
- hxstompxl_load_snapshot 1 5 2  # Preset 5, Snapshot 3
```

### Snapshot Control (4 Snapshots)

```mml
[00:00.000]
# Named snapshots (1-4)
- hxstompxl_snap_1 1
- hxstompxl_snap_2 1
- hxstompxl_snap_3 1
- hxstompxl_snap_4 1

# Parameterized (0-3)
- hxstompxl_snapshot 1 3  # Snapshot 4
```

## The Middle Ground

### HX Stomp XL: Best of Both Worlds

**HX Stomp XL** strikes a balance between:
- ✅ HX Stomp's compact size
- ✅ Full Helix's capabilities

**Key Position**:
- Better than HX Stomp (4 vs 3 snapshots, 8 vs 5 footswitches)
- More compact than full Helix (smaller footprint)
- Same limitations as HX Stomp (USB only, single DSP)

## 4 Snapshots: Good Balance

### Sufficient for Most Songs

**HX Stomp XL has 4 snapshots** (0-3).

**Better than**: HX Stomp (3 snapshots) ✅
**Less than**: Full Helix (8 snapshots) ⚠️
**Same as**: HX Effects (4 snapshots)

**Why 4 is good**:
- Fits standard song structures: Verse/Chorus/Bridge/Solo
- Enables gain staging: Clean/Crunch/Drive/Lead
- Adequate for most live performances
- Better than HX Stomp's limiting 3 snapshots

```mml
[00:00.000]
# Named snapshots
- hxstompxl_snap_1 1  # Snapshot 1
- hxstompxl_snap_2 1  # Snapshot 2
- hxstompxl_snap_3 1  # Snapshot 3
- hxstompxl_snap_4 1  # Snapshot 4

# Parameterized
- hxstompxl_snapshot 1 2  # Snapshot 3
```

## 4-Snapshot Song Arrangements

### Pattern 1: Standard Song Structure

```mml
[00:00.000]
# Load song preset
- hxstompxl_preset 1 10

# Snapshot 1: Verse (clean/mild)
- hxstompxl_snap_1 1

# Snapshot 2: Chorus (driven/wet)
[00:16.000]
- hxstompxl_snap_2 1

# Snapshot 3: Bridge (ambient/different)
[00:32.000]
- hxstompxl_snap_3 1

# Snapshot 4: Solo (lead tone)
[00:48.000]
- hxstompxl_snap_4 1
```

### Pattern 2: Gain Staging

```mml
[00:00.000]
# Gain-based preset organization
- hxstompxl_gain_stages 1 15

# This demonstrates 4 gain stages:
# Snapshot 1: Clean
# Snapshot 2: Light crunch
# Snapshot 3: Medium drive
# Snapshot 4: High gain lead
```

### Pattern 3: Progressive Effects Build

```mml
[00:00.000]
- hxstompxl_preset 1 20

# Dry
- hxstompxl_snap_1 1

# Add delay
[00:08.000]
- hxstompxl_snap_2 1

# Add reverb
[00:16.000]
- hxstompxl_snap_3 1

# Full ambient (delay + reverb + modulation)
[00:24.000]
- hxstompxl_snap_4 1
```

## 8 Footswitches: Excellent Live Control

### Double the HX Stomp

**HX Stomp XL has 8 footswitches** (FS1-8).

**Comparison**:
- HX Stomp: 5 footswitches ❌
- HX Stomp XL: 8 footswitches ✅ (You are here)
- HX Effects: 6 footswitches ⚠️
- Helix Floor/LT: 11 footswitches ✅✅

**Why 8 is good**:
- Enough for most live scenarios
- Can control multiple effects per preset
- Progressive effect builds
- Real-time performance flexibility

```mml
[00:00.000]
# Toggle footswitches (ALWAYS toggle)
- line6_fs1 1
- line6_fs2 1
- line6_fs3 1
- line6_fs4 1
- line6_fs5 1
- line6_fs6 1
- line6_fs7 1
- line6_fs8 1
```

### Progressive Effect Build Example

```mml
[00:00.000]
# Start with basic tone
- hxstompxl_all_bypass_off 1

# Add compression
[00:04.000]
- line6_fs1 1  # Toggle FS1 (compressor)

# Add delay
[00:08.000]
- line6_fs2 1  # Toggle FS2 (delay)

# Add reverb
[00:12.000]
- line6_fs3 1  # Toggle FS3 (reverb)

# Add modulation
[00:16.000]
- line6_fs4 1  # Toggle FS4 (chorus/phaser)

# Add drive
[00:20.000]
- line6_fs5 1  # Toggle FS5 (overdrive)
```

## HX Stomp XL Unique Features

### All Bypass Control

**Same as HX Stomp** (not on full Helix).

```mml
[00:00.000]
# Bypass all effects (global mute)
- hxstompxl_all_bypass_on 1

# Un-bypass all
- hxstompxl_all_bypass_off 1

# Parameterized
- hxstompxl_all_bypass 1 127  # On
- hxstompxl_all_bypass 1 0    # Off
```

**Use cases**:
- Tuning
- Muting during preset changes
- Emergency cutoff
- Silent guitar swaps

### Mode Switching

**Same as HX Stomp** (not on full Helix).

```mml
[00:00.000]
# Switch modes
- hxstompxl_mode_stomp 1     # Stomp mode
- hxstompxl_mode_scroll 1    # Scroll mode
- hxstompxl_mode_preset 1    # Preset mode
- hxstompxl_mode_snapshot 1  # Snapshot mode

# Cycle modes
- hxstompxl_mode_next 1      # Next mode
- hxstompxl_mode_prev 1      # Previous mode
```

## Preset Management

### Direct PC Addressing (Simplified)

**NO Bank Select needed!** Same as HX Stomp.

HX Stomp XL uses direct PC 0-127 addressing (simpler than full Helix).

```mml
[00:00.000]
# Load preset 10
- hxstompxl_preset 1 10

# Load preset 127
- hxstompxl_preset 1 127

# Load with snapshot
- hxstompxl_load_snapshot 1 10 2  # Preset 10, Snapshot 3
```

**Preset capacity**: 128 presets total (PC 0-127)

## Expression Pedal Control

### 2 Expression Pedals

HX Stomp XL has **2 expression pedals** (EXP1, EXP2). No EXP3.

```mml
[00:00.000]
# Direct MIDI values
- line6_exp1 1 64
- line6_exp2 1 100

# With modulation
- line6_exp_swell 1 1 0 127       # Smooth swell
- line6_exp_vibrato 1 1 64 3.0 20 # Vibrato effect
- line6_exp_envelope 1 1          # ADSR envelope
- line6_exp_ar 1 1 0.5 1.0        # AR envelope
```

## Looper Control

```mml
[00:00.000]
# Full looper workflow
- line6_looper_start_recording 1
[+8s]
- line6_looper_playback 1
[+16s]
- line6_looper_stop_exit 1
```

All standard Helix looper functions available (from common library).

## Command Center

### Enhanced vs HX Stomp

**HX Stomp XL has enhanced Command Center** vs regular HX Stomp.

More footswitch assignments available due to 8 footswitches.

```mml
[00:00.000]
# Load preset and control external amp
- hxstompxl_preset_with_amp 1 10 2
# Params: ch, preset, amp_channel

# Snapshot + external gear control
- hxstompxl_snapshot_with_external 1 2 71 127
# Params: ch, snapshot, ext_cc, ext_value
```

## USB MIDI Considerations

### NO 5-Pin DIN MIDI

**Same limitation as HX Stomp** (USB MIDI only).

**Implications**:
1. ❌ Cannot chain with non-USB MIDI gear without interface
2. ⚠️ USB MIDI has higher jitter than DIN (affects clock sync)
3. ❌ No MIDI Thru capability for hardware
4. ⚠️ Requires computer or USB MIDI host for most controllers
5. ❌ Ground loop isolation not possible without external USB isolator

**Recommended solutions**:
- MIDI Solutions USB MIDI Host (USB to 5-pin DIN)
- Disaster Area MIDI Baby (direct USB-C)
- Morningstar MC6 (USB-C compatible)

## Complete Song Example

```mml
[00:00.000]
# Standard 4-part song with HX Stomp XL

# Load song preset
- hxstompxl_preset 1 5

# INTRO - Clean
- hxstompxl_snap_1 1

# VERSE - Rhythm
[00:16.000]
- hxstompxl_snap_2 1

# Pre-chorus build (use footswitch)
[00:28.000]
- line6_fs2 1  # Add delay

# CHORUS - Drive + reverb
[00:32.000]
- hxstompxl_snap_3 1

# BRIDGE - Ambient
[00:48.000]
- hxstompxl_snap_4 1

# SOLO - Lead tone (back to snapshot 3 with modifications)
[01:04.000]
- hxstompxl_snap_3 1
- line6_fs5 1  # Engage boost

# FINAL CHORUS
[01:36.000]
- hxstompxl_snap_3 1
```

## Firmware Timing Requirements

### Same as Other Helix Models

**Firmware 3.5x**: 350ms delay after PC
**Firmware 3.10+**: CC69 buffered, can reduce to 50ms
**Firmware 3.80**: Stable

See Helix skill for detailed timing guidance.

## Common Mistakes and Fixes

### Mistake 1: Expecting More Than 4 Snapshots

```mml
# ❌ WRONG - Only snapshots 0-3 available
- hxstompxl_snapshot 1 4  # ERROR!

# ✅ CORRECT - Use preset changes for more sections
- hxstompxl_preset 1 11
```

### Mistake 2: Missing Delays After PC

```mml
# ❌ WRONG (firmware 3.5x)
[00:00.000]
- hxstompxl_preset 1 10
- hxstompxl_snapshot 1 2  # Ignored!

# ✅ CORRECT - Use helper
[00:00.000]
- hxstompxl_load_snapshot 1 10 2
```

### Mistake 3: Using USB for MIDI Clock

**USB MIDI has jitter issues for clock sync.**

Consider external MIDI interface with 5-pin DIN if clock sync is critical.

## Comparison: HX Stomp XL vs Others

### HX Stomp

- ❌ **3 snapshots** (very limited)
- ❌ **5 footswitches** (limited)
- ⚠️ **2 expression pedals**
- ❌ **USB MIDI only**
- ✅ Smallest footprint
- ✅ All Bypass + Mode switching
- ✅ Direct PC addressing

**Best for**: Ultra-compact setups, simple songs

### HX Stomp XL (You Are Here)

- ⚠️ **4 snapshots** (good balance) ✅
- ⚠️ **8 footswitches** (excellent) ✅
- ⚠️ **2 expression pedals**
- ❌ **USB MIDI only**
- ✅ Compact footprint (larger than HX Stomp)
- ✅ All Bypass + Mode switching
- ✅ Direct PC addressing
- ✅ Enhanced Command Center

**Best for**: Most live performers, good balance of size vs capabilities

### HX Effects

- ⚠️ **4 snapshots** (same as Stomp XL)
- ⚠️ **6 footswitches** (less than Stomp XL)
- ⚠️ **2 expression pedals**
- ✅ **5-pin DIN MIDI** (advantage!)
- ✅ Effects-only (amp integration)
- ❌ No amp/cab modeling

**Best for**: Effects with external amps, 5-pin DIN ecosystem

### Helix Floor/LT/Rack

- ✅ **8 snapshots** (maximum flexibility)
- ✅ **11 footswitches** (Floor/LT)
- ✅ **3 expression pedals** (Floor/Rack)
- ✅ **5-pin DIN MIDI**
- ✅ Dual DSP path
- ✅ Full Command Center
- ❌ Large footprint
- ❌ More expensive

**Best for**: Professional touring, complex songs, maximum flexibility

## Sweet Spot Analysis

### Why HX Stomp XL is the "Sweet Spot"

**Advantages**:
1. ✅ **4 snapshots** - sufficient for most songs
2. ✅ **8 footswitches** - excellent live control
3. ✅ Compact size - pedalboard-friendly
4. ✅ Affordable - less than full Helix
5. ✅ Direct addressing - simpler than full Helix

**Trade-offs**:
1. ⚠️ USB only - no 5-pin DIN (but works for most)
2. ⚠️ Single DSP - limits simultaneous effects
3. ⚠️ No EXP3 - but 2 is usually enough

**Conclusion**: Best choice for most guitarists who want:
- More than HX Stomp's limitations
- Less than full Helix's size/cost
- Good balance of features vs portability

## Reserved CC Numbers

```
CC69  - Snapshot select (0-3)
CC70  - All Bypass
CC71  - Mode Switch
```

All other CCs available for MIDI Learn.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| 4 snapshots not enough | Consider full Helix (8) or use preset changes |
| Can't connect MIDI controller | Requires USB-C or USB MIDI Host (no 5-pin DIN) |
| Preset changes have gaps | Use All Bypass to mute during changes |
| MIDI timing is sloppy | USB has jitter - use quality cable, avoid hubs |
| Need more footswitches | Consider full Helix (11 footswitches) |

## Reference

### Device Library Location
- Main: `devices/hx_stomp_xl.mmd`
- Common: `devices/line6_common.mmd` (imported automatically)

### Documentation
Official Manual: https://line6.com/support/manuals/hxstompxl

### Firmware Version
3.80 (current as of library version)

## See Also

- [Helix Usage](../mmd-device-helix/SKILL.md) - Full Helix, 8 snapshots, 11 footswitches
- [HX Stomp Usage](../hx-stomp-usage/SKILL.md) - 3 snapshots, 5 footswitches
- [HX Effects Usage](../hx-effects-usage/SKILL.md) - 4 snapshots, 5-pin DIN
- [MMD Syntax Reference](../../spec.md)
- [Line 6 Common Library](../../devices/line6_common.mmd)
