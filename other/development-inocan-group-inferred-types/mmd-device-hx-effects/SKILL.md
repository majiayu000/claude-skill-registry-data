---
name: mmd-device-hx-effects
description: Guide for using the Line 6 HX Effects device library in MMD files. Use when the user mentions HX Effects, HX Effects processor, effects-only processor, or needs help with 4-snapshot control, sequential preset addressing (banks), 5-pin DIN MIDI, or amp integration workflows.
---

# Line 6 HX Effects Usage Guide

Expert guidance for using the HX Effects device library in MIDI Markdown files.

## When to Use This Skill

Invoke this skill when working with:
- Line 6 HX Effects (effects-only processor)
- 4-snapshot control
- Sequential preset addressing (32 banks × 4 presets)
- 5-pin DIN MIDI connectivity (advantage over HX Stomp/XL)
- Amp integration workflows
- 6 footswitch control
- Effects-only applications (no amp/cab modeling)

## Quick Start

### Import the Library

```mml
@import "devices/hx_effects.mmd"
```

### Basic Preset Loading

```mml
[00:00.000]
# Load Bank 1 Preset A (PC = 0)
- hxfx_preset 1 0

# Load Bank 5 Preset C (PC = 18)
# Formula: ((5-1) × 4) + 2 = 18
- hxfx_preset 1 18

# Load preset and switch to snapshot
- hxfx_load_snapshot 1 18 2  # Preset 18, Snapshot 3
```

### Snapshot Control (4 Snapshots)

```mml
[00:00.000]
# Named snapshots (1-4)
- hxfx_snap_1 1
- hxfx_snap_2 1
- hxfx_snap_3 1
- hxfx_snap_4 1

# Parameterized (0-3)
- hxfx_snapshot 1 3  # Snapshot 4
```

## Key Differences from Other Helix Models

### HX Effects Unique Features

**✅ Effects-Only Processor**:
- No amp/cab modeling
- Focus on effects processing
- Integration with external amps

**✅ 5-Pin DIN MIDI**:
- Full MIDI In/Out/Thru
- Hardware daisy-chaining
- Lower jitter than USB
- Optical isolation
- **Advantage over HX Stomp/XL** (USB only)

**✅ Sequential Preset Addressing**:
- 32 Banks × 4 Presets (A-D)
- 128 presets total
- Intuitive bank organization
- No Bank Select needed

**⚠️ 4 Snapshots**:
- Better than HX Stomp (3)
- Less than full Helix (8)
- Good balance for most songs

**✅ 6 Footswitches**:
- FS1-6 available
- More than HX Stomp (5)
- Less than Helix Floor (11)

## Understanding Sequential Preset Addressing

### Addressing Formula

**Formula**: `PC = ((Bank - 1) × 4) + Preset_Offset`

Where **Preset_Offset**:
- A = 0
- B = 1
- C = 2
- D = 3

### Quick Reference Table

```
Bank 1:  PC 0-3     (Presets A-D)
Bank 2:  PC 4-7     (Presets A-D)
Bank 3:  PC 8-11    (Presets A-D)
Bank 4:  PC 12-15   (Presets A-D)
Bank 5:  PC 16-19   (Presets A-D)
Bank 10: PC 36-39   (Presets A-D)
Bank 32: PC 124-127 (Presets A-D)
```

### Calculation Examples

```
Bank 5 Preset C:
  ((5-1) × 4) + 2 = 16 + 2 = 18

Bank 10 Preset A:
  ((10-1) × 4) + 0 = 36 + 0 = 36

Bank 32 Preset D:
  ((32-1) × 4) + 3 = 124 + 3 = 127
```

## Preset Management

### Direct Preset Loading

```mml
[00:00.000]
# Load Bank 1 Preset A
- hxfx_preset 1 0

# Load Bank 1 Preset B
- hxfx_preset 1 1

# Load Bank 5 Preset C (calculate: ((5-1)×4)+2 = 18)
- hxfx_preset 1 18

# Load Bank 32 Preset D (last preset)
- hxfx_preset 1 127
```

### Named Bank 1 Shortcuts

```mml
[00:00.000]
# Commonly used first bank
- hxfx_bank1_a 1  # PC 0
- hxfx_bank1_b 1  # PC 1
- hxfx_bank1_c 1  # PC 2
- hxfx_bank1_d 1  # PC 3
```

### Load with Snapshot

```mml
[00:00.000]
# Load Bank 3 Preset B with Snapshot 3
# Bank 3 Preset B = ((3-1)×4)+1 = 9
- hxfx_load_snapshot 1 9 2  # PC 9, Snapshot 3
```

## Snapshot Control

### 4 Snapshots Available

HX Effects has **4 snapshots** (0-3), providing good flexibility.

**Better than**: HX Stomp (3 snapshots)
**Less than**: Full Helix (8 snapshots)
**Same as**: HX Stomp XL (4 snapshots)

```mml
[00:00.000]
# Named snapshots
- hxfx_snap_1 1  # Snapshot 1
- hxfx_snap_2 1  # Snapshot 2
- hxfx_snap_3 1  # Snapshot 3
- hxfx_snap_4 1  # Snapshot 4

# Parameterized
- hxfx_snapshot 1 2  # Snapshot 3
```

### 4-Snapshot Song Arrangements

**Pattern 1: Verse/Chorus/Bridge/Solo**

```mml
[00:00.000]
# Load song preset
- hxfx_preset 1 8  # Bank 3 Preset A

# Verse
- hxfx_snap_1 1

# Chorus
[00:16.000]
- hxfx_snap_2 1

# Bridge
[00:32.000]
- hxfx_snap_3 1

# Solo
[00:48.000]
- hxfx_snap_4 1
```

**Pattern 2: Dry → Subtle → Wet → Ambient**

```mml
[00:00.000]
- hxfx_preset 1 12  # Bank 4 Preset A

# Dry (minimal FX)
- hxfx_snap_1 1

# Subtle (light delay/reverb)
[00:08.000]
- hxfx_snap_2 1

# Wet (moderate FX)
[00:16.000]
- hxfx_snap_3 1

# Ambient (heavy FX)
[00:24.000]
- hxfx_snap_4 1
```

## Amp Integration

### HX Effects Excels at Amp Control

HX Effects is designed for integration with external amps via MIDI.

### Preset with Amp Channel Change

```mml
[00:00.000]
# Load HX Effects preset and switch amp channel
- hxfx_preset_with_amp 1 12 2
# Params: ch, preset, amp_channel

# This expands to:
# - Load HX Effects preset
# - Wait 350ms
# - Send PC to external amp (channel 2 by default)
```

### Snapshot with Amp Channel

```mml
[00:00.000]
# Change snapshot and amp channel simultaneously
- hxfx_snapshot_with_amp 1 2 3
# Params: ch, snapshot, amp_channel
```

### Snapshot with External Pedal

```mml
[00:00.000]
# Change snapshot and control external pedal
- hxfx_snapshot_with_pedal 1 2 71 127
# Params: ch, snapshot, pedal_cc, pedal_state
```

## 5-Pin DIN MIDI Advantages

### Why 5-Pin DIN is Better

**HX Effects has full 5-pin DIN MIDI** (unlike HX Stomp/XL).

**Advantages**:
1. ✅ Hardware MIDI Thru for daisy-chaining
2. ✅ Lower jitter for MIDI Clock (vs USB)
3. ✅ Optical isolation (no ground loops)
4. ✅ Standard controller compatibility
5. ✅ No computer/USB host required

### Typical MIDI Chain

```
MIDI Controller → HX Effects → External Amp → External Pedals
    (5-pin)          THRU          THRU             END
```

**Configuration**: Global Settings > MIDI/Tempo > MIDI Thru

## Footswitch Control

### 6 Footswitches Available

HX Effects has **6 footswitches** (FS1-6).

```mml
[00:00.000]
# Toggle footswitches (ALWAYS toggle)
- line6_fs1 1
- line6_fs2 1
- line6_fs3 1
- line6_fs4 1
- line6_fs5 1
- line6_fs6 1
```

**Important**: Like all Helix family, footswitches ALWAYS toggle. Cannot force on/off via MIDI.

## Expression Pedal Control

### 2 Expression Pedals

HX Effects has **2 expression pedals** (EXP1, EXP2).

```mml
[00:00.000]
# Direct MIDI values
- line6_exp1 1 64
- line6_exp2 1 100

# With modulation
- line6_exp_swell 1 1 0 127       # Smooth swell
- line6_exp_vibrato 1 1 64 3.0 20 # Vibrato
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

## Command Center for Amp Integration

### Full Command Center Available

HX Effects has **full Command Center** (no CV/Ext Amp - effects only).

**Use cases**:
- Switch amp channels
- Control external pedals
- Sync external effects
- MIDI clock distribution

### Complete Amp Integration Example

```mml
[00:00.000]
# Song Section 1: Clean with ambient FX
- hxfx_preset 1 0          # Bank 1 Preset A
- hxfx_snap_1 1            # Clean snapshot

# Send amp to clean channel (example: Mesa Boogie on channel 2)
- pc 2.0                   # Amp clean channel

# Song Section 2: Crunch with delay
[00:16.000]
- hxfx_snap_2 1            # Delay snapshot
- pc 2.1                   # Amp crunch channel

# Song Section 3: High gain with reverb
[00:32.000]
- hxfx_snap_3 1            # Reverb snapshot
- pc 2.2                   # Amp lead channel

# Song Section 4: Solo with boost
[00:48.000]
- hxfx_snap_4 1            # Solo snapshot
- cc 2.71.127              # Engage external boost pedal
```

## 4-Snapshot Workflow Patterns

### Song Section Mapping

```mml
[00:00.000]
# Preset for Song 1
- hxfx_preset 1 8  # Bank 3 Preset A

# Snapshot 1: Verse FX
- hxfx_snap_1 1

# Snapshot 2: Chorus FX
[00:16.000]
- hxfx_snap_2 1

# Snapshot 3: Bridge FX
[00:32.000]
- hxfx_snap_3 1

# Snapshot 4: Solo FX
[00:48.000]
- hxfx_snap_4 1
```

### Wetness Progression

```mml
[00:00.000]
- hxfx_wetness_progression 1 12

# This demonstrates progressive wetness:
# Snapshot 1: Dry (minimal FX)
# Snapshot 2: Subtle (light delay/reverb)
# Snapshot 3: Wet (moderate FX mix)
# Snapshot 4: Ambient (heavy delay/reverb/mod)
```

## Firmware Timing Requirements

### Same as Other Helix Models

**Firmware 3.5x**: 350ms delay after PC
**Firmware 3.10+**: CC69 buffered, can reduce to 50ms
**Firmware 3.80**: Stable

See Helix skill for detailed timing guidance.

```mml
[00:00.000]
# ✅ CORRECT - Helper includes delay
- hxfx_load_snapshot 1 12 2

# ❌ WRONG - Manual without delay (firmware 3.5x)
- pc 1.12
- cc 1.69.2  # Might be ignored!
```

## Usage Examples

### Example 1: Load Specific Bank/Preset

```mml
[00:00.000]
# Bank 5 Preset C
# Calculate: ((5-1)×4)+2 = 18
- hxfx_preset 1 18
```

### Example 2: Song with Snapshots

```mml
[00:00.000]
# Bank 3 Preset A
- hxfx_preset 1 8

# Verse
- hxfx_snap_1 1

# Chorus
[00:16.000]
- hxfx_snap_2 1

# Bridge
[00:32.000]
- hxfx_snap_3 1

# Solo
[00:48.000]
- hxfx_snap_4 1
```

### Example 3: Expression Automation

```mml
[00:00.000]
# Smooth expression swell
- line6_exp_swell 1 1 0 127

[00:04.000]
# Vibrato effect
- line6_exp_vibrato 1 1 64 3.0 25
```

### Example 4: Amp Integration

```mml
[00:00.000]
# Load preset and switch amp channel
- hxfx_preset_with_amp 1 12 2

# Snapshot with amp change
[00:16.000]
- hxfx_snapshot_with_amp 1 2 3
```

## Common Mistakes and Fixes

### Mistake 1: Wrong PC Calculation

```mml
# ❌ WRONG - Forgot to subtract 1 from bank
# Bank 5 Preset C (incorrect: 5×4+2 = 22)
- hxfx_preset 1 22  # WRONG!

# ✅ CORRECT - Use formula: ((Bank-1)×4)+Offset
# Bank 5 Preset C = ((5-1)×4)+2 = 18
- hxfx_preset 1 18
```

### Mistake 2: Missing Delay After PC

```mml
# ❌ WRONG (firmware 3.5x)
[00:00.000]
- pc 1.12
- cc 1.69.2  # Ignored!

# ✅ CORRECT - Use helper
[00:00.000]
- hxfx_load_snapshot 1 12 2
```

### Mistake 3: Expecting More Than 4 Snapshots

```mml
# ❌ WRONG - HX Effects only has snapshots 0-3
- hxfx_snapshot 1 4  # ERROR!

# ✅ CORRECT - Use preset changes for more sections
- hxfx_preset 1 16  # Load different preset
```

## Comparison: HX Effects vs Others

### HX Effects (You Are Here)

- ⚠️ **4 snapshots** (good balance)
- ⚠️ **6 footswitches**
- ⚠️ **2 expression pedals**
- ✅ **5-pin DIN MIDI** (Thru enabled)
- ✅ **Effects-only** (amp integration focus)
- ✅ **Sequential addressing** (bank-based)
- ✅ Full Command Center

**Best for**:
- Effects processing with external amps
- MIDI hardware integration
- 5-pin DIN MIDI ecosystem
- Users who don't need amp/cab modeling

### HX Stomp/XL

- ❌ **USB MIDI only** (no 5-pin DIN)
- ✅ Amp/cab modeling included
- ⚠️ 3-4 snapshots (limited)

### Full Helix

- ✅ **8 snapshots** (maximum flexibility)
- ✅ **11 footswitches** (Floor/LT)
- ✅ **5-pin DIN MIDI**
- ✅ Amp/cab modeling
- ❌ Larger footprint
- ❌ More expensive

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Wrong preset loads | Double-check PC calculation: ((Bank-1)×4)+Offset |
| Snapshots don't switch | Add 350ms delay after PC (firmware 3.5x) |
| MIDI Thru doesn't work | Enable in Global Settings > MIDI/Tempo > MIDI Thru |
| Amp won't switch channels | Check amp's MIDI channel, ensure 5-pin cable connected |
| Footswitches don't work | HX Effects footswitches toggle only, can't force on/off |

## Reference

### Device Library Location
- Main: `devices/hx_effects.mmd`
- Common: `devices/line6_common.mmd` (imported automatically)

### Documentation
Official Manual: https://line6.com/support/manuals/hxeffects

### Firmware Version
3.80 (current as of library version)

## See Also

- [Helix Usage](../mmd-device-helix/SKILL.md) - Full Helix, 8 snapshots
- [HX Stomp Usage](../hx-stomp-usage/SKILL.md) - 3 snapshots, USB only
- [HX Stomp XL Usage](../hx-stomp-xl-usage/SKILL.md) - 4 snapshots, 8 footswitches
- [MMD Syntax Reference](../../spec.md)
- [Line 6 Common Library](../../devices/line6_common.mmd)
