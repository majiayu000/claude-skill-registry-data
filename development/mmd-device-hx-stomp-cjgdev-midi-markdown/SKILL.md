---
name: mmd-device-hx-stomp
description: Guide for using the Line 6 HX Stomp device library in MMD files. Use when the user mentions HX Stomp, HX Stomp guitar processor, or needs help with HX Stomp's 3-snapshot limitation, USB MIDI setup, All Bypass control, Mode switching, or workarounds for limited snapshots.
---

# Line 6 HX Stomp Usage Guide

Expert guidance for using the HX Stomp device library in MIDI Markdown files.

## When to Use This Skill

Invoke this skill when working with:
- Line 6 HX Stomp compact guitar processor
- HX Stomp's **3-snapshot limitation** (critical constraint)
- USB MIDI-only connectivity (no 5-pin DIN)
- All Bypass control (HX Stomp specific)
- Mode switching (Stomp/Scroll/Preset/Snapshot modes)
- Workarounds for 3-snapshot limitation
- 5 footswitch control

## Quick Start

### Import the Library

```mml
@import "devices/hx_stomp.mmd"
```

### Basic Preset Loading

```mml
[00:00.000]
# Load preset 5 (direct PC, no bank select needed)
- hxstomp_preset 1 5

# Load preset and switch to snapshot
- hxstomp_load_snapshot 1 5 2  # Preset 5, Snapshot 3
```

### Snapshot Control (3 Snapshots Only!)

```mml
[00:00.000]
# Named snapshots (1-3)
- hxstomp_snap_1 1
- hxstomp_snap_2 1
- hxstomp_snap_3 1

# Parameterized (0-2)
- hxstomp_snapshot 1 2  # Snapshot 3
```

## ⚠️ CRITICAL: 3-Snapshot Limitation

### The Biggest Constraint

**HX Stomp has ONLY 3 SNAPSHOTS (0-2)**

This is the single biggest limitation for live performance compared to:
- Full Helix: 8 snapshots
- HX Stomp XL: 4 snapshots
- HX Effects: 4 snapshots

### Impact on Live Performance

**Challenge**: Most songs have 4+ sections (intro, verse, chorus, bridge, solo, outro)

**3 snapshots is often not enough for:**
- Verse/chorus/bridge/solo arrangements
- Clean/crunch/drive/lead tone staging
- Complex dynamic songs

## Workarounds for 3-Snapshot Limitation

### Strategy 1: Use Preset Changes for Major Sections

Keep verse/chorus/bridge in **separate presets**, use snapshots for variations within sections.

```mml
[00:00.000]
# Intro preset
- hxstomp_preset 1 10

# Verse preset (3 snapshots for variations)
[00:16.000]
- hxstomp_preset 1 11
- hxstomp_snap_1 1  # Verse rhythm

[00:24.000]
- hxstomp_snap_2 1  # Verse lead fill

# Chorus preset
[00:32.000]
- hxstomp_preset 1 12
- hxstomp_snap_1 1  # Chorus rhythm

# Bridge preset
[00:48.000]
- hxstomp_preset 1 13
```

### Strategy 2: Hybrid Preset+Snapshot Workflow

Organize **presets by song**, use 3 snapshots for verse/chorus/bridge.

```mml
[00:00.000]
# Song 1 preset
- hxstomp_preset 1 20

# Use 3 snapshots for main sections
- hxstomp_snap_1 1  # Intro/Verse

[00:16.000]
- hxstomp_snap_2 1  # Chorus

[00:32.000]
- hxstomp_snap_3 1  # Bridge/Solo

# Song 2 preset
[01:00.000]
- hxstomp_song_change 1 21 0  # Load song 2, snapshot 1
```

### Strategy 3: Use Mode Switching for Flexibility

Switch to Snapshot mode temporarily, change snapshot, return to Stomp mode.

```mml
[00:00.000]
# Quick snapshot change with mode switching
- hxstomp_quick_snapshot 1 2

# This expands to:
# - Switch to Snapshot mode
# - Change to snapshot 3
# - Return to Stomp mode
```

### Strategy 4: Leverage All Bypass for Mute

Use All Bypass as a "mute" function between sections to cover preset changes.

```mml
[00:00.000]
# Change preset with mute coverage (no gap/pop)
- hxstomp_section_change_with_mute 1 15

# This expands to:
# - Mute all (bypass on)
# - Change preset
# - Wait for load
# - Un-mute (bypass off)
```

## HX Stomp Unique Features

### All Bypass Control

**Exclusive to HX Stomp/XL** (not on full Helix)

```mml
[00:00.000]
# Bypass all effects (global mute)
- hxstomp_all_bypass_on 1

# Un-bypass all
- hxstomp_all_bypass_off 1

# Parameterized
- hxstomp_all_bypass 1 127  # On
- hxstomp_all_bypass 1 0    # Off
```

**Use cases**:
- Tuning
- Muting during preset changes
- Emergency cutoff
- Silent guitar swaps

### Mode Switching

**Exclusive to HX Stomp/XL** (not on full Helix)

```mml
[00:00.000]
# Switch modes
- hxstomp_mode_stomp 1     # Stomp mode
- hxstomp_mode_scroll 1    # Scroll mode
- hxstomp_mode_preset 1    # Preset mode
- hxstomp_mode_snapshot 1  # Snapshot mode

# Cycle modes
- hxstomp_mode_next 1      # Next mode
- hxstomp_mode_prev 1      # Previous mode
```

## Preset Management

### Direct PC Addressing (Simplified)

**NO Bank Select needed!** HX Stomp uses direct PC 0-127 addressing.

This is **MUCH simpler** than full Helix (which requires CC0/CC32 + PC).

```mml
[00:00.000]
# Load preset 10 (just send PC 10)
- hxstomp_preset 1 10

# Load preset 127
- hxstomp_preset 1 127
```

**Preset capacity**: 128 presets total (PC 0-127)

## Footswitch Control

### 5 Footswitches Available

HX Stomp has **5 footswitches** (FS1-5).

```mml
[00:00.000]
# Toggle footswitches (ALWAYS toggle, can't force on/off)
- line6_fs1 1
- line6_fs2 1
- line6_fs3 1
- line6_fs4 1
- line6_fs5 1
```

**Important**: Like all Helix family, footswitches ALWAYS toggle. Cannot force on/off via MIDI.

## Expression Pedal Control

### 2 Expression Pedals

HX Stomp has **2 expression pedals** (EXP1, EXP2). No EXP3.

```mml
[00:00.000]
# Direct MIDI values
- line6_exp1 1 64
- line6_exp2 1 100

# With modulation
- line6_exp_swell 1 1 0 127       # Smooth EXP1 swell
- line6_exp_vibrato 1 1 64 3.0 20 # Vibrato effect
- line6_exp_envelope 1 1          # ADSR envelope
- line6_exp_ar 1 1 0.5 1.0        # AR envelope
```

## Looper Control

```mml
[00:00.000]
# Start recording
- line6_looper_start_recording 1

[+8s]
# Switch to playback
- line6_looper_playback 1

[+16s]
# Stop and exit
- line6_looper_stop_exit 1
```

All standard Helix looper functions available (from common library).

## USB MIDI Considerations

### NO 5-Pin DIN MIDI

**HX Stomp has USB MIDI ONLY** (no 5-pin DIN).

**Implications**:
1. ❌ Cannot chain with non-USB MIDI gear without interface
2. ⚠️ USB MIDI has higher jitter than DIN (affects clock sync)
3. ❌ No MIDI Thru capability for hardware (can't daisy-chain)
4. ⚠️ Requires computer or USB MIDI host for most controllers
5. ❌ Ground loop isolation not possible without external USB isolator

**Recommended solutions for live use**:
- MIDI Solutions USB MIDI Host (converts USB to 5-pin DIN)
- Disaster Area MIDI Baby (direct USB-C to HX Stomp)
- Morningstar MC6 (USB-C compatible)

## Command Center

### Added in Firmware 3.00+

**Mandatory**: Firmware 3.00+ required for Command Center

Pre-3.00 firmware lacks Command Center entirely.

```mml
[00:00.000]
# Load preset and control external amp
- hxstomp_preset_with_amp 1 10 2
# Params: ch, preset, amp_channel

# Snapshot change with external pedal control
- hxstomp_snapshot_with_pedal 1 2 71 127
# Params: ch, snapshot, pedal_cc, pedal_value
```

## Complete Live Song Example

This demonstrates a song arrangement using HX Stomp's limitations cleverly.

```mml
[00:00.000]
# Song with 4 presets (major sections) + 3 snapshots (variations)

# INTRO - Clean preset
- hxstomp_preset 1 10
- hxstomp_snap_1 1  # Dry

[00:08.000]
- hxstomp_snap_2 1  # With reverb

# VERSE - Mild overdrive preset
[00:16.000]
- hxstomp_preset 1 11
[+350ms]
- hxstomp_snap_1 1  # Rhythm OD

[00:28.000]
- hxstomp_snap_2 1  # OD + delay (pre-chorus)

# CHORUS - High gain preset
[00:32.000]
- hxstomp_preset 1 12
[+350ms]
- hxstomp_snap_1 1  # Rhythm gain

[00:44.000]
- hxstomp_snap_2 1  # Lead gain + delay

# BRIDGE - Ambient preset
[01:16.000]
- hxstomp_preset 1 13
[+350ms]
- hxstomp_snap_1 1  # Clean + reverb

[01:24.000]
- hxstomp_snap_2 1  # Heavy reverb

# FINAL CHORUS - Back to high gain
[01:32.000]
- hxstomp_preset 1 12
[+350ms]
- hxstomp_snap_3 1  # Epic lead tone

# OUTRO - Return to clean
[01:56.000]
- hxstomp_preset 1 10
[+350ms]
- hxstomp_snap_2 1  # With reverb
```

## Firmware Timing Requirements

### Same as Full Helix

**Firmware 3.5x**: 350ms delay after PC
**Firmware 3.10+**: CC69 buffered, can reduce to 50ms
**Firmware 3.80**: Stable, use Tap Tempo for tempo sync

See Helix skill for detailed timing guidance.

## Common Mistakes and Fixes

### Mistake 1: Expecting More Than 3 Snapshots

```mml
# ❌ WRONG - HX Stomp only has snapshots 0-2
[00:00.000]
- hxstomp_snapshot 1 3  # ERROR! Only 0-2 available

# ✅ CORRECT - Use preset changes for additional sections
[00:00.000]
- hxstomp_preset 1 11  # Load different preset instead
```

### Mistake 2: Missing Delays After PC

```mml
# ❌ WRONG (firmware 3.5x)
[00:00.000]
- hxstomp_preset 1 10
- hxstomp_snapshot 1 2  # Ignored!

# ✅ CORRECT
[00:00.000]
- hxstomp_load_snapshot 1 10 2  # Built-in delay
```

### Mistake 3: Using USB for MIDI Clock

**USB MIDI has jitter issues for clock sync.**

Consider using external MIDI interface with 5-pin DIN output if clock sync is critical.

## Comparison: HX Stomp vs Others

### HX Stomp (You Are Here)

- ❌ **3 snapshots** (most limited)
- ❌ **5 footswitches**
- ⚠️ **2 expression pedals**
- ❌ **USB MIDI only**
- ❌ Single DSP path
- ⚠️ Limited Command Center
- ✅ **Smallest footprint**
- ✅ **All Bypass** (unique feature)
- ✅ **Mode switching** (unique feature)
- ✅ **Direct PC** (simpler addressing)

**Best for**:
- Simple songs (3 sections or less)
- Heavy preset-switching workflow
- Compact pedalboard setups
- Users who prioritize small size

### HX Stomp XL

- ⚠️ **4 snapshots** (better, but still limited)
- ⚠️ **8 footswitches** (double HX Stomp)
- ⚠️ **2 expression pedals**
- ❌ **USB MIDI only**
- ✅ All Bypass + Mode switching
- ✅ Direct PC addressing

**Best for**: Users needing more footswitches but not full Helix

### Helix Floor/LT/Rack

- ✅ **8 snapshots** (maximum flexibility)
- ✅ **11 footswitches**
- ✅ **3 expression pedals**
- ✅ **5-pin DIN MIDI**
- ✅ Dual DSP path
- ✅ Full Command Center
- ❌ Larger footprint

**Best for**: Complex songs, professional touring, maximum flexibility

## Reserved CC Numbers

```
CC69  - Snapshot select (0-2 only!)
CC70  - All Bypass (HX Stomp specific)
CC71  - Mode Switch (HX Stomp specific)
```

All other CCs available for MIDI Learn.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Only 3 snapshots isn't enough | Use preset changes for sections, snapshots for variations |
| Can't connect MIDI controller | Requires USB-C or USB MIDI Host adapter (no 5-pin DIN) |
| Preset changes have gaps/pops | Use All Bypass to mute during changes |
| Command Center doesn't work | Update to firmware 3.00+ (mandatory) |
| MIDI timing is sloppy | USB has jitter - use quality cable, avoid hubs |

## Reference

### Device Library Location
- Main: `devices/hx_stomp.mmd`
- Common: `devices/line6_common.mmd` (imported automatically)

### Documentation
Official Manual: https://line6.com/support/manuals/hxstomp

### Firmware Version
3.80 (current as of library version)

## See Also

- [Helix Usage](../mmd-device-helix/SKILL.md) - Full Helix, 8 snapshots
- [HX Stomp XL Usage](../hx-stomp-xl-usage/SKILL.md) - 4 snapshots, 8 footswitches
- [HX Effects Usage](../hx-effects-usage/SKILL.md) - Effects only, 4 snapshots
- [MMD Syntax Reference](../../spec.md)
- [Line 6 Common Library](../../devices/line6_common.mmd)
