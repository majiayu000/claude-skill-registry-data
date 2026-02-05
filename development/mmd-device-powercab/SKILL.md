---
name: mmd-device-powercab
description: Guide for using the Line 6 PowerCab Plus device library in MMD files. Use when the user mentions PowerCab, PowerCab Plus, Line 6 PowerCab, FRFR speaker, or needs help with speaker modeling, microphone simulation, IR loading, mode switching, or HF driver control for the PowerCab.
---

# Line 6 PowerCab Plus Usage Guide

Expert guidance for using the PowerCab Plus device library in MIDI Markdown files.

## When to Use This Skill

Invoke this skill when working with:
- Line 6 PowerCab Plus (112 Plus or 212 Plus models)
- PowerCab speaker model switching and microphone simulation
- FRFR flat mode and voicing control
- User IR (impulse response) management
- HF driver and trim control
- PowerCab preset management
- Integration with Helix via L6 Link or MIDI
- Live performance speaker automation
- Studio recording with PowerCab

## Quick Start

### Import the Library

```mml
@import "devices/line6_powercab.mmd"
```

### Basic Preset Loading

```mml
[00:00.000]
# Direct preset recall (PC 0-127 → Presets 000-127)
- powercab_preset 1 5

# Safe preset loading (workaround for first-switch bug)
- powercab_preset_safe 1 5
```

### Speaker Mode Quick Setup

```mml
[00:00.000]
# Switch to speaker mode and select model
- powercab_speaker_vintage 1   # Celestion Vintage 30
- powercab_mic_57 1            # SM57-style mic
- powercab_mic_standard 1      # 2 inches distance
```

### Pre-Built Amp-Speaker Pairings

```mml
[00:00.000]
# Complete setups with matched speaker + mic + distance
- powercab_fender_clean 1       # Jarvis speaker + 67 Cond mic
- powercab_marshall_crunch 1    # Green speaker + 57 Dynamic
- powercab_vox_jangle 1         # Essex speaker + 87 Cond
- powercab_modern_highgain 1    # Shade speaker + 421 Dynamic
```

## Critical Known Issues

### 1. First Preset Change Goes to Wrong Preset

**Problem**: First PC message after power-on may switch to incorrect preset

**Symptoms**:
- Preset change works, but loads different preset than requested
- Subsequent preset changes work correctly
- Issue only affects first switch after power cycle

**Workaround**:
```mml
# ❌ WRONG - Direct PC can fail on first switch
[00:00.000]
- pc 1.5

# ✅ CORRECT - Use safe helper with initialization delay
[00:00.000]
- powercab_preset_safe 1 5

# This expands to:
# [@]
# - cc 1.20.0    # Send mode CC first to init MIDI reception
# [+50ms]
# - pc 1.5       # Then send PC after delay
```

### 2. HF Driver Behavior Inconsistent Across Modes

**Problem**: HF Trim (CC5) has bugs and inconsistent behavior

**Symptoms**:
- HF driver remains active in modes where it should be disabled
- PowerCab Edit software UI doesn't reflect actual HF state
- Expression pedal control causes pops/clicks
- Behavior differs between Flat/FRFR, Speaker, and IR modes

**Functional Status**:
- ✅ Flat/FRFR mode: HF Trim works (tweeter control)
- ✅ IR mode: HF Trim works
- ❌ Speaker mode: HF driver should be disabled (baked into speaker models) but bug may keep it active

**Workaround**:
```mml
# ❌ WRONG - Expression pedal can cause pops/clicks
[00:00.000]
- cc 1.5.0
- cc 1.5.42
- cc 1.5.85

# ✅ CORRECT - Use explicit CC5 values per preset
[00:00.000]
- powercab_mode_flat 1
[+50ms]
- powercab_hf_neutral 1   # Value 100 = 0dB

# ✅ CORRECT - Use MIDI Instant Commands, not expression pedals
[00:04.000]
- powercab_hf_plus10 1    # Value 113 ≈ +10dB

# ✅ CORRECT - Disable in Speaker mode
[00:08.000]
- powercab_mode_speaker 1
[+50ms]
- powercab_hf_off 1       # Value 0 = completely off
```

**HF Trim Values**:
- Value 0 = OFF (completely disables HF driver)
- Value 100 = 0dB (neutral, default)
- Value 113 ≈ +10dB
- Resolution: +/-1dB ≈ Value +/-2
- Range: -96dB to +12dB

### 3. Parameter Changes Can Cause Pops/Clicks

**Problem**: Rapid CC messages or certain parameter transitions cause audible artifacts

**Solution**: Use 50-100ms spacing between MIDI messages

```mml
# ❌ WRONG - No delays, causes pops/clicks
[00:00.000]
- cc 1.20.1     # Mode = Speaker
- cc 1.22.0     # Speaker = Vintage
- cc 1.23.0     # Mic = 57

# ✅ CORRECT - Use safe timing with delays
[00:00.000]
- cc 1.20.1     # Mode = Speaker
[+50ms]
- cc 1.22.0     # Speaker = Vintage
[@]
- cc 1.23.0     # Mic = 57 (can be simultaneous with speaker)

# ✅ BEST - Use complete setup helper
[00:00.000]
- powercab_speaker_setup 1 0 0 2  # Mode + speaker + mic + distance
```

### 4. MIDI Clock Issues with Multiple HX Devices

**Problem**: Using HX Stomp + HX Effects simultaneously with PowerCab can cause MIDI clock conflicts

**Solution**:
- Use only one HX device for MIDI clock source
- Disable MIDI Clock Send on secondary HX device
- Or use dedicated MIDI controller instead of HX devices

### 5. Firmware 2.0+ Required for Full Features

**Critical**: PowerCab Plus firmware 2.0+ adds 7 additional speaker models (13 total)

**Firmware 1.x**: Only 6 speaker models (values 0-5)
**Firmware 2.0+**: 13 speaker models (values 0-12)

```mml
# These models require firmware 2.0+:
- powercab_speaker_natural 1    # Value 6 (HF Off mode)
- powercab_speaker_dino 1       # Value 7 (Cannabis Rex)
- powercab_speaker_lecto 1      # Value 8 (EV EVM 12L)
- powercab_speaker_herald 1     # Value 9 (G12H Heritage)
- powercab_speaker_brown 1      # Value 10 (G12 EVH)
- powercab_speaker_shade 1      # Value 11 (Mesa Black Shadow)
- powercab_speaker_jetson 1     # Value 12 (Jensen C12K)
```

**Check Firmware**: Line 6 Updater at https://line6.com/software/

## Operating Modes

PowerCab has three fundamental operating modes (CC20):

### Flat Mode (Value 0)

Full-range flat response (FRFR) for modelers.

```mml
[00:00.000]
# Basic flat mode
- powercab_mode_flat 1

# Complete FRFR setup
- powercab_flat_setup 1 0 100
# Params: channel, voicing (0=FRFR), hf_trim (100=0dB)

# Studio FRFR monitoring preset
- powercab_studio_frfr 1
```

**Voicing Options** (CC21, Flat mode only):
- Value 0: FRFR (full-range with HF driver)
- Value 1: LF Solo (woofer only, no EQ)
- Value 2: LF Flat (woofer only with flat EQ)

```mml
[00:00.000]
- powercab_voicing_frfr 1      # Full-range
- powercab_voicing_lf_solo 1   # Woofer only
- powercab_voicing_lf_flat 1   # Woofer with EQ
```

### Speaker Mode (Value 1)

Guitar speaker modeling with microphone simulation.

**13 Speaker Models** (CC22):
- 0: Vintage (Celestion Vintage 30)
- 1: Green (Celestion Greenback)
- 2: Cream (Celestion G12M-65)
- 3: Jarvis (Jensen P12Q - American clean)
- 4: Bayou (Eminence Swamp Thang - deep bass)
- 5: Essex (Blue Bell/Vox - bright jangly)
- 6: Natural (HF Off - natural response, firmware 2.0+)
- 7: Dino (Eminence Cannabis Rex, firmware 2.0+)
- 8: Lecto (EV EVM 12L - aggressive, firmware 2.0+)
- 9: Herald (Celestion G12H Heritage, firmware 2.0+)
- 10: Brown (Celestion G12 EVH, firmware 2.0+)
- 11: Shade (Mesa Black Shadow C90, firmware 2.0+)
- 12: Jetson (Jensen C12K - vintage American, firmware 2.0+)

```mml
[00:00.000]
# Named shortcuts (firmware 1.x - original 6)
- powercab_speaker_vintage 1
- powercab_speaker_green 1
- powercab_speaker_cream 1
- powercab_speaker_jarvis 1
- powercab_speaker_bayou 1
- powercab_speaker_essex 1

# Named shortcuts (firmware 2.0+ - additional 7)
- powercab_speaker_natural 1
- powercab_speaker_dino 1
- powercab_speaker_lecto 1
- powercab_speaker_herald 1
- powercab_speaker_brown 1
- powercab_speaker_shade 1
- powercab_speaker_jetson 1

# Or direct CC value
- cc 1.22.0   # Vintage
- cc 1.22.1   # Green
```

**16 Microphone Models** (CC23, affects XLR output only):

Dynamic Mics:
- 0: 57 Dynamic (SM57-style - industry standard)
- 1: 409 Dynamic (MD409-style - clear highs)
- 2: 421 Dynamic (MD421-style - versatile)
- 3: 30 Dynamic (PR30-style - extended lows)
- 4: 20 Dynamic (PR20-style - warm)
- 13: 112 Dynamic (D112-style - bass punchy)
- 14: 12 Dynamic (D12-style - vintage bass)
- 15: 7 Dynamic (SM7-style - broadcast smooth)

Ribbon Mics:
- 5: 121 Ribbon (R-121-style - smooth)
- 6: 160 Ribbon (M160-style - detailed)
- 7: 4038 Ribbon (Coles 4038 - vintage British)

Condenser Mics:
- 8: 414 Cond (C414-style - versatile)
- 9: 84 Cond (KM84-style - accurate)
- 10: 67 Cond (U67-style - vintage warmth)
- 11: 87 Cond (U87-style - studio standard)
- 12: 47 Cond (U47-style - classic warm)

```mml
[00:00.000]
# Named microphone shortcuts
- powercab_mic_57 1
- powercab_mic_421 1
- powercab_mic_121 1
- powercab_mic_87 1
- powercab_mic_47 1

# Or direct CC value
- cc 1.23.0   # 57 Dynamic
- cc 1.23.5   # 121 Ribbon
```

**Mic Distance** (CC24, 0-22 = 1"-12" in 0.5" increments):

```mml
[00:00.000]
# Named distance shortcuts
- powercab_mic_close 1      # 1 inch (value 0)
- powercab_mic_standard 1   # 2 inches (value 2)
- powercab_mic_balanced 1   # 3 inches (value 4)
- powercab_mic_moderate 1   # 6 inches (value 10)
- powercab_mic_far 1        # 12 inches (value 22)

# Direct value (calculation: distance = 1 + value × 0.5)
- cc 1.24.0   # 1 inch
- cc 1.24.2   # 2 inches
- cc 1.24.10  # 6 inches
- cc 1.24.22  # 12 inches

# Dynamic distance sweep (e.g., during solo)
- powercab_mic_dist_sweep 1 2 10  # Sweep 2" to 6"
```

**Complete Speaker Setup**:

```mml
[00:00.000]
# Manual setup
- powercab_mode_speaker 1
[+50ms]
- powercab_speaker_vintage 1
[@]
- powercab_mic_57 1
[@]
- powercab_mic_standard 1

# Or use complete setup helper
- powercab_speaker_setup 1 0 0 2
# Params: channel, speaker (0-12), mic (0-15), distance (0-22)
```

### IR Mode (Value 2)

User-loaded impulse responses (128 slots).

```mml
[00:00.000]
# Basic IR mode
- powercab_mode_ir 1
[+50ms]
- powercab_ir 1 10   # Load IR from slot 10

# Complete IR setup with filters
- powercab_ir_setup 1 25 30 90
# Params: channel, IR slot (0-127), low cut, high cut

# IR bank shortcuts (user convention)
- powercab_ir_clean 1 5      # Clean IRs (0-20)
- powercab_ir_crunch 1 25    # Crunch IRs (21-40)
- powercab_ir_highgain 1 45  # High-gain IRs (41-60)
- powercab_ir_user 1 75      # User/3rd-party (61-127)
```

**IR Mode EQ** (only functional in IR mode):

```mml
[00:00.000]
# Adjustable filters for tone shaping
- powercab_ir_lowcut 1 20   # High-pass filter
- powercab_ir_highcut 1 100 # Low-pass filter
```

**Note**: IRs must be loaded via USB using PowerCab Edit software. SysEx upload NOT supported.

## Volume and Routing Controls

### Master Volume (Most Important for Live)

```mml
[00:00.000]
# Direct volume (0-127)
- powercab_volume 1 90

# Smooth volume fade
- powercab_volume_fade 1 90 100
# Params: channel, start, end
```

### Input Volume and Levels

```mml
[00:00.000]
# Input 1 volume (100=0dB, 0=mute, 127=+12dB)
- powercab_input1_vol 1 100

# Input 1 level: Line or Instrument
- powercab_input1_line 1    # Line level (+4dB)
- powercab_input1_inst 1    # Instrument level

# Input 2 volume and level
- powercab_input2_vol 1 100
- powercab_input2_line 1
- powercab_input2_inst 1

# Input 2 mode (Normal/Monitor/USB)
- powercab_input2_normal 1
- powercab_input2_monitor 1
- powercab_input2_usb 1

# Link Input 1 & 2 gain controls together
- powercab_link_inputs_on 1
- powercab_link_inputs_off 1
```

### Preset Level (Per-Preset Volume Trim)

```mml
[00:00.000]
# Balance volume across different presets
- powercab_preset_level 1 100
```

## HF Driver / High Frequency Control

**CRITICAL**: HF Trim controls compression driver gain (high-frequency tweeter).

**Known Bugs**: HF driver behavior inconsistent across modes. See issue #2 above.

**Functional Only** in Flat/FRFR and IR modes. Speaker mode disables HF driver (speaker models have baked-in high-freq response).

```mml
[00:00.000]
# HF Trim levels
- powercab_hf_off 1       # Value 0 = completely off
- powercab_hf_neutral 1   # Value 100 = 0dB (neutral)
- powercab_hf_plus10 1    # Value 113 ≈ +10dB

# Direct value
- powercab_hf_trim 1 100  # 0-127

# Smooth HF Trim transition (use with caution - potential pops/clicks)
- powercab_hf_swell 1 100 113
```

**Recommendation**: Use MIDI Instant Commands for HF control, NOT expression pedals, to avoid pops/clicks.

## USB Audio and Digital Processing

### USB Audio Mode

Affects signal sent to DAW via USB interface.

```mml
[00:00.000]
# Normal mode: Dry signal (unprocessed)
- powercab_usb_normal 1

# Processed mode: Applies PowerCab DSP
- powercab_usb_processed 1
```

### Low Cut Filter

80Hz high-pass filter, only affects speaker output (not XLR or L6 Link).

```mml
[00:00.000]
# Enable/disable Low Cut
- powercab_lowcut_on 1
- powercab_lowcut_off 1
```

## LED Ring Color (Visual Preset ID)

Visual identification on front panel for stage use.

```mml
[00:00.000]
# Named color shortcuts
- powercab_led_off 1
- powercab_led_white 1
- powercab_led_red 1
- powercab_led_blue 1
- powercab_led_green 1
- powercab_led_yellow 1
- powercab_led_cyan 1
- powercab_led_magenta 1

# Direct value (0=Off, 1-18=White, 19-36=Red, etc.)
- powercab_led 1 64
```

## PowerCab 212 Plus: Dual Speaker Control

PowerCab 212 Plus has dual 12" speakers with independent control. These CCs only functional on 212 Plus, ignored on 112 Plus.

```mml
[00:00.000]
# Speaker 1 (physical left) independent controls
- powercab212_speaker1 1 0     # Speaker model (0-12)
- powercab212_mic1 1 0         # Mic model (0-15)
- powercab212_dist1 1 2        # Mic distance (0-22)

# Pre-built stereo combinations
- powercab212_dual_vintage 1        # Both speakers = Vintage 30
- powercab212_dual_green 1          # Both speakers = Greenback
- powercab212_mix_vintage_green 1   # Mixed: Vintage + Greenback
```

## Classic Amp-Speaker Pairings

Pre-matched combinations with speaker + mic + distance:

```mml
[00:00.000]
# Fender clean: Jarvis speaker + 67 Cond mic at 3"
- powercab_fender_clean 1

# Marshall crunch: Green speaker + 57 Dynamic at 2"
- powercab_marshall_crunch 1

# Vox jangle: Essex speaker + 87 Cond mic at 4"
- powercab_vox_jangle 1

# Modern high-gain: Shade speaker + 421 Dynamic at 1"
- powercab_modern_highgain 1

# Vintage rock: Cream speaker + 121 Ribbon at 3"
- powercab_vintage_rock 1
```

## Live Performance Presets

Quick changes with LED color identification:

```mml
[00:00.000]
# Verse: Balanced, natural tone
- powercab_live_verse 1

# Chorus: Aggressive, forward tone
- powercab_live_chorus 1

# Solo: Prominent, detailed tone
- powercab_live_solo 1
```

## Studio Recording Setups

```mml
[00:00.000]
# Studio FRFR monitoring (uncolored)
- powercab_studio_frfr 1

# Speaker sim for tube amp recording
- powercab_studio_speaker_sim 1
```

## Integration Methods

### Method 1: Helix + PowerCab via L6 Link

**Best for**: Simplest integration, lowest latency, single-cable connection

**Requirements**:
- Helix firmware 2.80+
- PowerCab firmware 2.0+
- 110Ω XLR cable (AES/EBU)

**Connection**:
```
Helix L6 LINK OUT → PowerCab L6 LINK IN
```

**Setup**:
- Set PowerCab MIDI channel to match Helix (default 1)
- Helix presets automatically sync PowerCab presets
- Use Helix Command Center to send CC messages per snapshot

**Example**:
```mml
# In Helix Command Center:
# Snapshot 1: Send CC22=3 (Jarvis speaker)
# Snapshot 2: Send CC22=1 (Green speaker)
```

### Method 2: Helix + PowerCab via MIDI DIN

**Best for**: Independent of audio routing, works with any modeler

**Connection**:
```
Helix MIDI OUT → PowerCab MIDI IN (5-pin DIN)
```

**Example**:
```mml
# Helix Command Center Instant Commands
[00:00.000]
# Snapshot 1 sends:
- cc 1.22.3   # Jarvis speaker

[00:16.000]
# Snapshot 2 sends:
- cc 1.22.1   # Green speaker
```

### Method 3: Third-Party MIDI Controller

**Compatible**: Morningstar MC6, RJM Mastermind, Disaster Area, Boss, etc.

**Best for**: Dedicated PowerCab control, multi-device rigs

**Connection**:
```
Controller MIDI OUT → PowerCab MIDI IN
```

**Example**:
```mml
# Program footswitches:
# FS1 = PC 0 (Preset 000)
# FS2 = PC 1 (Preset 001)
# FS3 = CC 22 value 0 (Vintage speaker)
# FS4 = CC 22 value 1 (Green speaker)
```

### Method 4: Stereo PowerCab Pair (Daisy-Chain)

**Best for**: Stereo rigs, dual-amp setups

**Connection**:
```
Controller → PowerCab #1 MIDI IN → PowerCab #2 MIDI IN
```

**Setup**:
- Both units on same MIDI channel
- Enable MIDI Thru on PowerCab #1
- L6 Link auto-splits stereo (left → #1, right → #2)

**Example**:
```mml
[00:00.000]
# Both units respond to same message
- powercab_preset 1 5

# For stereo effects:
- powercab_speaker_vintage 1
```

### Method 5: Tube Amp + PowerCab

**Best for**: Hybrid tube amp + digital control

**Connection**:
```
Tube amp speaker out → PowerCab INPUT 1 (Line level)
PowerCab XLR OUT → FOH/Recording interface
```

**Setup**:
- Set PowerCab to Speaker mode for cab simulation
- XLR output to PA/recording (mic simulation applied)
- Speaker output used as backline monitor
- MIDI controller switches models per song

**Example**:
```mml
[00:00.000]
# Song 1: Fender-style clean
- powercab_input1_line 1
[@]
- powercab_fender_clean 1

[00:16.000]
# Song 2: Marshall crunch
- powercab_marshall_crunch 1
```

## Dual Amp Technique with Helix

Coordinate PowerCab speaker changes with Helix snapshots:

```mml
[00:00.000]
# Verse: Fender amp model + Jarvis speaker
- powercab_dual_amp_clean 1

[00:16.000]
# Chorus: Marshall amp model + Green speaker
- powercab_dual_amp_crunch 1
```

**Helix Setup**:
- Snapshot 1: Fender amp model
- Snapshot 2: Marshall amp model
- Command Center sends PowerCab speaker changes via CC22

## Common Mistakes and Fixes

### Mistake 1: Direct PC on First Switch

```mml
# ❌ WRONG - May load wrong preset on first switch
[00:00.000]
- pc 1.5

# ✅ CORRECT - Use safe helper
[00:00.000]
- powercab_preset_safe 1 5
```

### Mistake 2: No Delays Between Parameter Changes

```mml
# ❌ WRONG - Causes pops/clicks
[00:00.000]
- cc 1.20.1
- cc 1.22.0
- cc 1.23.0

# ✅ CORRECT - Use safe timing
[00:00.000]
- cc 1.20.1
[+50ms]
- cc 1.22.0
[@]
- cc 1.23.0

# ✅ BEST - Use complete setup helper
[00:00.000]
- powercab_speaker_setup 1 0 0 2
```

### Mistake 3: Using Expression Pedals for HF Trim

```mml
# ❌ WRONG - Causes pops/clicks
[00:00.000]
- cc 1.5.0
- cc 1.5.42
- cc 1.5.85

# ✅ CORRECT - Use discrete Instant Commands
[00:00.000]
- powercab_hf_neutral 1
[00:04.000]
- powercab_hf_plus10 1
```

### Mistake 4: Expecting Speaker Models 6-12 on Firmware 1.x

```mml
# ❌ WRONG - Requires firmware 2.0+
- powercab_speaker_natural 1   # Value 6
- powercab_speaker_dino 1      # Value 7

# ✅ CORRECT - Update firmware or use models 0-5
- powercab_speaker_vintage 1   # Value 0
- powercab_speaker_green 1     # Value 1
```

## Emergency Reset

```mml
[00:00.000]
# Reset to safe known state (Flat FRFR)
- powercab_reset_safe 1

# This sets:
# - Mode = Flat
# - Voicing = FRFR
# - HF Trim = 0dB (neutral)
# - Volume = 100 (0dB reference)
# - Input 1 Vol = 100
# - Input 1 Level = Line
# - LED = White
```

## Recommended Practices

### 1. Gain Staging

- Set modeler to Line Level output (+4dB), not instrument level
- Aim for PowerCab input LED to "tickle amber" at peaks (healthy signal)
- Don't vary input gain during performance—use strong steady signal
- Adjust stage volume via CC7 (Master Volume) or CC28 (Preset Level)

### 2. Preset Organization

- Match PowerCab preset numbers to Helix preset numbers for simple sync
- Or organize by speaker type (0-9 = Vintage, 10-19 = Green, etc.)
- Or organize by song (one or more presets per song)
- Use LED ring colors (CC29) for visual preset ID on stage

### 3. Timing and Sequencing

- Allow 50-100ms between MIDI messages for complex sequences
- Send mode-change CCs (CC20, CC21) BEFORE Program Change
- Use [@] (simultaneous timing) for CCs that should change together
- Use [+50ms] relative timing for sequential operations

### 4. Live Performance

- Create backup connection method (analog if using L6 Link, vice versa)
- Test all presets at venue volume before show
- Use consistent naming across devices (Helix preset 1 = PowerCab preset 1)
- Enable MIDI Thru when daisy-chaining multiple PowerCab units
- Disable PC Send to prevent feedback loops with external controller

### 5. Studio Recording

- Use Flat FRFR mode for uncolored monitoring while tracking
- Use Speaker mode + XLR output for direct recording with cab simulation
- Use IR mode for custom/third-party impulse responses
- Enable USB Processed mode to send PowerCab-processed signal to DAW
- Load IRs via PowerCab Edit software (USB connection required)

## Model Compatibility

| Model | MIDI Capability | Notes |
|-------|----------------|-------|
| PowerCab 112 Plus | Full MIDI (all features) | Single 12" speaker, mono |
| PowerCab 212 Plus | Full MIDI + CC102-104 | Dual 12" speakers, stereo |
| PowerCab 112/212 (non-Plus) | NO MIDI | Plus designation essential |
| PowerCab CL (112/212) | Limited MIDI | Only CC7, CC68-71, no PC |

**CRITICAL**: "Plus" designation required for full MIDI control. Non-Plus models have NO MIDI capability.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| First preset change goes to wrong preset | Use `powercab_preset_safe` alias with initialization delay |
| HF driver inconsistent behavior | Send explicit CC5 values per preset, avoid expression pedals |
| Pops/clicks when changing parameters | Use 50-100ms spacing ([+50ms] timing) between messages |
| MIDI not responding | Check channel match, verify PC Receive enabled in Global Settings |
| L6 Link not working | Update firmware (Helix 2.80+, PowerCab 2.0+), use 110Ω cable |
| Volume drop via L6 Link | Adjust Helix output +10dB or PowerCab input CC1 +10dB |
| Speaker models 6-12 missing | Update PowerCab Plus firmware to 2.0+ via Line 6 Updater |
| MIDI clock conflicts | Use only one HX device for MIDI clock, disable on others |

## Reference

### Device Library Location
`devices/line6_powercab.mmd`

### Documentation
- Official Manual: https://line6.com/support/manuals/powercab
- PowerCab Edit Software: https://line6.com/software/
- Firmware Updates: Line 6 Updater at https://line6.com/software/
- Community Forums: https://line6.com/support/forum/93-powercab/

### MIDI Implementation
- 29 Control Change assignments (CC1-7, CC20-31, CC102-104, CC111)
- 128 Program Change presets (PC 0-127)
- Default MIDI Channel: 1 (configurable 1-16, plus Omni mode)
- Connections: 5-pin DIN MIDI IN/OUT/THRU, USB MIDI, L6 Link (digital XLR)

### Firmware Version
PowerCab Plus firmware 2.0+ recommended for full 13 speaker models

## See Also

- [MMD Syntax Reference](../../spec.md)
- [Device Library Creation](../../docs/user-guide/device-libraries.md)
- [Helix Usage](../mmd-device-helix/SKILL.md)
- [HX Stomp Usage](../hx-stomp-usage/SKILL.md)
- [Timing System](../../docs/dev-guides/timing-system.md)
