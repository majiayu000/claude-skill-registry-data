---
name: mmd-device-h90
description: Guide for using the Eventide H90 Harmonizer device library in MMD files. Use when the user mentions Eventide H90, H90 effects processor, H90 reverb/delay/modulation, or needs help with H90 program changes, HotSwitches, bypass control, expression automation, or firmware workarounds.
---

# Eventide H90 Harmonizer Usage Guide

Expert guidance for using the Eventide H90 device library in MIDI Markdown files.

## When to Use This Skill

Invoke this skill when working with:
- Eventide H90 Harmonizer effects processor
- H90 program loading and bypass control
- HotSwitch parameter snapshots
- H90 expression pedal automation
- Performance parameters (Freeze, Warp, Repeat, Infinity)
- Dual algorithm control (Preset A/B)
- Firmware 1.9.4+ PC+CC bug workarounds

## ⚠️ CRITICAL: Read This First

### Zero Default MIDI CC Assignments

**THE H90 HAS NO DEFAULT MIDI CC MAPPINGS!**

You **MUST manually configure** each CC mapping in:
- System Menu → MIDI → Global Control (on H90)
- OR H90 Control software

This library provides aliases for all parameters, but they won't work until you configure the CC assignments on your H90.

### Critical Firmware Bug (1.9.4+)

**FIRMWARE 1.9.4 AND LATER HAS A SEVERE BUG:**

Sending Program Change and Control Change messages simultaneously causes the H90 to **IGNORE ALL CC MESSAGES**.

**Symptoms**:
- PC + CC sent together → CC messages ignored
- Internal logs show "Ignoring inbound message" errors
- Makes MIDI switcher integration extremely problematic

**RECOMMENDED SOLUTION**:
Downgrade to firmware **1.8.6** for professional MIDI control applications.

Contact support@eventide.com to request firmware 1.8.6 and H90 Control v1.7.11.

**Trade-off**: Cannot use algorithms added after v1.8.6 (Aggravate, Sticky Tape)

**Workarounds if staying on 1.9.4+**:
```mml
# Add 100ms delay between PC and CC
[00:00.000]
- pc 2.10          # Load program
[+100ms]
- h90_program_active 2  # Now CC works

# Or use helper macros
- h90_load_with_bypass 2 10 127
- h90_load_with_hotswitch 2 10 1
```

## Quick Start

### Import the Library

```mml
@import "devices/eventide_h90.mmd"
```

### Basic Program Loading

```mml
[00:00.000]
# Load Program 10 (with PC Offset ON: 0-99)
- h90_program 2 10

# Or specify offset mode explicitly
- h90_program_offset 2 10      # PC Offset ON: 0-99
- h90_program_default 2 11     # PC Offset OFF: 1-100
```

### Program Navigation

```mml
[00:00.000]
# Increment to next program
- h90_increment 2

# Decrement to previous
- h90_decrement 2

# Increment and load immediately
- h90_inc_load 2

# Bank up/down (3 programs at a time)
- h90_bank_up 2
- h90_bank_down 2
```

## Configuration Requirements

### Before Using This Library

**YOU MUST configure CC mappings on your H90 first!**

1. Access: System Menu → MIDI → Global Control
2. For each parameter, assign a CC number
3. Either:
   - Update CC numbers in this library to match YOUR config
   - OR configure H90 to match recommended mappings below

### Recommended Global CC Mappings

**Program Navigation** (CC#20-26):
```
CC#20 = Load (cue + toggle Act/Byp)
CC#21 = Increment
CC#22 = Decrement
CC#23 = Inc + Load
CC#24 = Dec + Load
CC#25 = Bank Up
CC#26 = Bank Down
```

**Active/Bypass** (CC#102-109):
```
CC#102 = P Act/Byp (toggle)
CC#103 = P Act/Byp (M) (momentary)
CC#104 = A Act/Byp (Preset A toggle)
CC#105 = A Act/Byp (M) (momentary)
CC#106 = B Act/Byp (Preset B toggle)
CC#107 = B Act/Byp (M) (momentary)
CC#108 = Insert 1 Act/Byp
CC#109 = Insert 2 Act/Byp
```

**System Functions** (CC#27, 30-33, 80):
```
CC#27 = Tuner (quirky toggle-only)
CC#80 = Tap Tempo
CC#30 = Mode Toggle
CC#31 = SELECT Mode
CC#32 = PERFORM Mode
CC#33 = BANK Mode
```

**HotSwitches** (CC#110-115):
```
CC#110 = HS1 (toggle)
CC#111 = HS1 (M) (momentary)
CC#112 = HS2 (toggle)
CC#113 = HS2 (M) (momentary)
CC#114 = HS3 (toggle)
CC#115 = HS3 (M) (momentary)
```

**Continuous Controls** (CC#11-17, 34-36, 84):
```
CC#11 = Expression Pedal
CC#12-17 = Quick Knobs 1-6
CC#34 = P HotKnob (Program)
CC#35 = A HotKnob (Preset A)
CC#36 = B HotKnob (Preset B)
CC#84 = P Mix (wet/dry)
```

**Performance Parameters** (CC#70-75):
```
CC#70-75 = PERFORM 1-6
```

## Active/Bypass Controls

### Understanding Toggle vs Momentary Modes

**Toggle Mode** (no "(M)"):
- Any CC value ≥64 toggles the state
- Each message toggles regardless of value
- Simpler for basic on/off control

**Momentary Mode** (with "(M)"):
- CC 0-63 = Force BYPASS state
- CC 64-127 = Force ACTIVE state
- Enables discrete on/off commands
- **Requires controller that sends single values only**

### Program-Level Bypass

```mml
[00:00.000]
# Toggle mode
- h90_program_bypass 2

# Momentary mode (discrete control)
- h90_program_active 2        # Force ACTIVE
- h90_program_bypass_force 2  # Force BYPASS
```

### Preset-Level Bypass

```mml
[00:00.000]
# Preset A controls
- h90_preset_a_bypass 2       # Toggle
- h90_preset_a_active 2       # Force active
- h90_preset_a_bypass_force 2 # Force bypass

# Preset B controls
- h90_preset_b_bypass 2
- h90_preset_b_active 2
- h90_preset_b_bypass_force 2
```

### Insert Loop Controls

```mml
[00:00.000]
# Toggle insert loops
- h90_insert1_bypass 2
- h90_insert2_bypass 2
```

## HotSwitch Control

### Basic HotSwitch Usage

HotSwitches are Program-level parameter snapshots. Only one HotSwitch can be active at a time.

```mml
[00:00.000]
# Toggle HotSwitch 1
- h90_hotswitch1 2

# Force HS1 active (momentary mode)
- h90_hotswitch1_active 2

# Force HS1 off
- h90_hotswitch1_off 2

# Same for HS2 and HS3
- h90_hotswitch2 2
- h90_hotswitch3 2
```

### HotSwitch Workflow Example

```mml
[00:00.000]
- h90_program 2 10

# Verse - base tone (no HotSwitch)
[00:16.000]
- h90_hotswitch1 2  # Chorus - engage HS1

[00:32.000]
- h90_hotswitch2 2  # Bridge - engage HS2

[00:48.000]
- h90_hotswitch1_off 2  # Back to base tone
```

## Expression and Continuous Controls

### Expression Pedal

```mml
[00:00.000]
# Direct MIDI value
- h90_expression 2 64

# Percentage
- h90_expression_percent 2 50

# Smooth swell with curve
- h90_expression_swell 2 0 127

# Fade effects
- h90_expression_fade_in 2
- h90_expression_fade_out 2
```

### Advanced Expression Modulation

```mml
[00:00.000]
# Vibrato with wave modulation
- h90_expression_vibrato 2 64 3.0 20
# Params: ch, center, freq(Hz), depth(%)

# ADSR envelope
- h90_expression_envelope 2

# Attack-Release envelope
- h90_expression_ar 2 0.5 1.0
# Params: ch, attack(s), release(s)
```

### Quick Knobs

```mml
[00:00.000]
# Control Quick Knobs 1-6
- h90_quick_knob1 2 100
- h90_quick_knob2 2 80
- h90_quick_knob3 2 64
```

### HotKnobs (Recommended Strategy)

**Eventide's Recommended Approach**:
1. Map algorithm parameters to HotKnob P per-Program
2. Map HotKnob P globally to one CC (e.g., CC#34)
3. Your expression pedal always sends CC#34
4. Different Programs respond with different parameter changes

```mml
[00:00.000]
# Program HotKnob (controls different params per-Program)
- h90_hotknob_program 2 64

# Preset-specific HotKnobs
- h90_hotknob_a 2 100
- h90_hotknob_b 2 80

# Smooth HotKnob automation
- h90_hotknob_program_swell 2 0 127
```

### Mix Control

```mml
[00:00.000]
# Direct value
- h90_mix 2 64

# Percentage (0% dry, 100% wet)
- h90_mix_percent 2 50

# Smooth transitions
- h90_mix_fade_in 2     # Dry to wet
- h90_mix_fade_out 2    # Wet to dry
- h90_mix_swell 2 0 127

# Tremolo effect (rhythmic wet/dry)
- h90_mix_tremolo 2 64 4.0 50
```

## Performance Parameters

### PERFORM 1-6

Performance Parameters are algorithm-specific functions:
- Prism Shift: Freeze
- Wormhole: Warp
- Delay algorithms: Repeat
- Reverb algorithms: Infinite, Freeze

```mml
[00:00.000]
# Direct control
- h90_perform1 2 127
- h90_perform2 2 100

# With modulation
- h90_perform1_swell 2 0 127
- h90_perform1_vibrato 2 64 2.0 30
- h90_perform1_envelope 2
```

## Gain Controls

```mml
[00:00.000]
# Input/Output gain (0-127)
- h90_program_in_gain 2 64
- h90_program_out_gain 2 100

# Output gain in dB (-24dB to +24dB)
- h90_program_out_gain_db 2 6  # +6dB

# Preset-specific gains
- h90_preset_a_in_gain 2 64
- h90_preset_a_out_gain 2 100
- h90_preset_b_in_gain 2 64
- h90_preset_b_out_gain 2 100
```

## System Functions

### Tuner Control

**QUIRK**: Tuner has unusual behavior!
- CC value 127 activates tuner
- CC value 0 does NOTHING
- Must send 127 again to deactivate (toggle-only)

```mml
[00:00.000]
# Activate tuner
- h90_tuner 2

# Deactivate tuner (send 127 again)
- h90_tuner 2
```

### Tap Tempo

```mml
[00:00.000]
- h90_tap_tempo 2
[+500ms]
- h90_tap_tempo 2
[+500ms]
- h90_tap_tempo 2
```

### Mode Switching

```mml
[00:00.000]
# Switch modes
- h90_mode_select 2   # SELECT mode
- h90_mode_perform 2  # PERFORM mode
- h90_mode_bank 2     # BANK mode
- h90_mode_toggle 2   # Toggle between modes
```

## Firmware 1.9.4+ Workarounds

### Safe Program Loading with CC

```mml
# ❌ WRONG - PC + CC together (firmware 1.9.4+ bug)
[00:00.000]
- pc 2.10
- cc 2.103.127  # This will be IGNORED!

# ✅ CORRECT - Use helper with delay
[00:00.000]
- h90_load_with_bypass 2 10 127

# ✅ CORRECT - Use helper for HotSwitch
[00:00.000]
- h90_load_with_hotswitch 2 10 1  # Load program, engage HS1

# ✅ CORRECT - Use helper for expression
[00:00.000]
- h90_load_with_expression 2 10 64
```

## Dual Algorithm Control

### Controlling Both Algorithm Paths

```mml
[00:00.000]
# Load dual reverb with balanced mix
- h90_dual_reverb_setup 2 10

# Serial FX chain with custom mix
- h90_serial_fx_chain 2 15 80

# A-only processing (bypass B)
- h90_a_only 2

# B-only processing (bypass A)
- h90_b_only 2

# Both active
- h90_both_active 2
```

## Delay Warping Workarounds

### Problem: Program Changes Cause Pitch/Time Warping

**Affected Algorithms**: Tape Echo, Head Space, Reverse delays

**Symptoms**: Audible pitch/time warping on delay trails during Program changes

**Solutions**:

```mml
# Solution 1: Crossfade to hide warping
[00:00.000]
- h90_program_change_crossfade 2 15
# Fades to dry, changes program, fades back to wet

# Solution 2: Fast crossfade
[00:00.000]
- h90_program_change_fast_crossfade 2 15

# Solution 3: Use HotSwitches within Program (no warping)
[00:00.000]
- h90_hotswitch_delay_transition 2 1  # Change delay via HS1

# Solution 4: Wait for spillover to complete
[00:00.000]
- h90_load_after_spillover 2 20  # Waits 5.5s for spillover
```

## Live Performance Initialization

```mml
[00:00.000]
# Initialize H90 for live performance
- h90_live_init 2 10

# This sets:
# - PERFORM Mode
# - Load starting program
# - Ensure active (not bypassed)
# - Reset expression to neutral
# - All HotSwitches off
```

## Known Issues and Limitations

### Issue 1: PC + CC Simultaneous Bug (Firmware 1.9.4+)

**Solution**: Downgrade to 1.8.6 OR add 100ms delays

### Issue 2: Insert Loop Latency

**Problem**: 5ms latency per A/D/A conversion

**Impact**: Insert loops = double conversion = noticeable delay

**Solution**: Run drives before H90 instead of in insert loops

### Issue 3: Power Supply Requirements

**Problem**: Insufficient current causes MIDI issues

**Solution**:
- Fender Engine Room 12V @ 375mA is INSUFFICIENT
- Use two 9V 500mA outputs with current doubler cable

### Issue 4: Program Loading Latency

**Problem**: 700ms to 2 seconds via MIDI PC

**Factors**:
- Spillover time settings
- DSP complexity

**Optimization**:
- Reduce spillover to minimum needed
- Load Programs outside spillover window

### Issue 5: Routing/Algorithm Limitations

**Cannot change via MIDI**:
- ❌ Series/parallel routing mode
- ❌ Insert/Dual global routing modes
- ❌ Individual Algorithm Presets
- ✅ Must create Programs with desired configurations

## Recommended Configuration Strategy

### Step 1: Start with Global Mappings

```
CC#102-109 = Bypass controls
CC#20-26   = Navigation
CC#27      = Tuner
CC#80      = Tap Tempo
CC#30-33   = Mode switching
CC#110-115 = HotSwitches
```

### Step 2: Add Expression Control

```
CC#11 = Expression Pedal → Map to HotKnob P globally
```

Configure HotKnob P per-Program for different parameters.

### Step 3: Add Performance Parameters

```
CC#70-75 = PERFORM 1-6 (algorithm-specific functions)
```

### Step 4: Add Quick Knobs if Needed

```
CC#12-17 = Quick Knobs 1-6
```

## Common Mistakes and Fixes

### Mistake 1: Sending PC + CC Together (Firmware 1.9.4+)

```mml
# ❌ WRONG
[00:00.000]
- pc 2.10
- h90_program_bypass 2  # IGNORED!

# ✅ CORRECT
[00:00.000]
- h90_load_with_bypass 2 10 127
```

### Mistake 2: Expecting Default CC Mappings

**The H90 has NO defaults!** You must configure everything.

### Mistake 3: Not Accounting for Spillover

```mml
# ❌ WRONG - Switching during spillover is slow
[00:00.000]
- pc 2.10
[+1s]  # Still in spillover window
- pc 2.11  # This will be SLOW

# ✅ CORRECT - Wait for spillover
[00:00.000]
- pc 2.10
[+6s]  # Outside spillover window
- pc 2.11  # This is faster
```

## Reference

### Device Library Location
`devices/eventide_h90.mmd`

### Documentation
- Official Manual: https://cdn.eventideaudio.com/manuals/h90/1.1/content/
- Eventide Website: https://www.eventideaudio.com/h90

### Firmware Version
1.8.6 (recommended for MIDI) / 1.9.4+ (latest, has PC+CC bug)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| CC messages ignored after PC | Firmware 1.9.4+ bug - add 100ms delay or downgrade to 1.8.6 |
| No MIDI control | Configure CC mappings in System Menu → MIDI → Global Control |
| Delay warping on Program change | Use crossfade helpers or HotSwitches |
| Slow Program loading | Reduce spillover time, wait outside spillover window |
| Tuner won't turn off | Quirky behavior - send CC#27 value 127 again |
| Power-related MIDI issues | Use proper power supply (not Fender Engine Room single output) |

## See Also

- [MMD Syntax Reference](../../spec.md)
- [Device Library Creation](../../docs/user-guide/device-libraries.md)
- [Modulation Guide](../../docs/user-guide/generative-music.md)
- [Timing System](../../docs/dev-guides/timing-system.md)
