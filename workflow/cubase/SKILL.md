---
name: cubase
description: "Configure Cubase MIDI Remote scripts, Expression Maps, and MixConsole workflows; investigate ASIO Guard and performance issues."
category: music
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["cubase", "steinberg", "midi-remote-api", "asio-guard", "expression-maps", "mixconsole", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Steinberg Cubase Pro Music Production AI Skill Guide (Claude)

## Overview & Engine Architecture
Steinberg Cubase Pro is a premier digital audio workstation (DAW) for professional scoring, music composition, MIDI sequencing, and multichannel audio mixing. Cubase operates on a 64-bit floating-point audio engine powered by **ASIO Guard (multi-threaded look-ahead buffering)**, native **VST3 hosting with plugin sandboxing**, **VariAudio 3** pitch/timing algorithms, **Expression Maps** for orchestral articulation routing, and an extensible **MIDI Remote JavaScript API (`midiremote_api`)**. Claude operates as a Principal Audio Systems Architect and Orchestral Scoring Technologist, specializing in **ASIO buffer latency calibration**, **MIDI Remote script authoring (JavaScript)**, **Expression Map schema design**, and **Control Room monitoring setup**.

### Cubase Pro Audio Engine & Control Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Cubase Pro Architecture                     │
│                                                             │
│  Presentation & Scoring Tier                                │
│  ├── Project Window & Key / Score / Drum Editors            │
│  ├── Expression Maps (Keyswitches, CC Chasing, Dynamics)    │
│  └── MixConsole (Channel Strips, VCA Faders, Control Room)  │
│                                                             │
│  Audio Engine & DSP Subsystem                               │
│  ├── 64-bit Float Audio Engine & ASIO Guard 2 Buffer Sizing │
│  ├── VariAudio 3 & AudioWarp Polyphonic Time-Stretch        │
│  └── VST3 Plugin Sandboxing & Blocklist Manager             │
│                                                             │
│  Hardware Remote & Scripting Core                           │
│  ├── Steinberg MIDI Remote JavaScript API (`midiremote_api`)│
│  └── Project Logical Editor (Rule-Based Macro Transformations│
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Steinberg MIDI Remote Scripting (JavaScript)**: Author clean, modular hardware controller drivers using `midiremote_api.makeDeviceDriver()` with surface elements (knobs, faders, buttons, displays).
2. **ASIO Guard & Latency Triage**: Resolve audio dropouts and real-time processing spikes by calibrating ASIO Guard levels (Low/Normal/High) and enabling the Steinberg Audio Power Scheme.
3. **Expression Map Design for Sample Libraries**: Construct structured Expression Map XML schemas linking musical notations (Staccato, Legato, Pizzicato) to sample keyswitches and MIDI CC curves (Spitfire, Vienna Symphonic, Orchestral Tools).
4. **Project Logical Editor (PLE) Automation**: Author complex Logical Editor presets to quantize note lengths, randomize velocities, and color-code orchestral stems.

---

## Production JavaScript Automation: Cubase MIDI Remote Controller Script

Save this script as `CustomController.js` inside `<CubasePrefs>/MIDI Remote/Driver Scripts/Local/VendorName/CustomController/`:

```javascript
// ==============================================================================
// Steinberg Cubase 13/14 MIDI Remote Script: Custom Hardware Driver
// Implements Transport Controls, Track 1 Fader, and Pan Knob via midiremote_api.
// ==============================================================================
var midiremote_api = require('midiremote_api_v1');

// 1. Create Device Driver
var deviceDriver = midiremote_api.makeDeviceDriver('VendorName', 'CustomController', 'AI Systems Engineering');

// 2. Configure MIDI Ports
var midiInput = deviceDriver.mPorts.makeMidiInput();
var midiOutput = deviceDriver.mPorts.makeMidiOutput();

deviceDriver.makeDetectionUnit().detectPortPair(midiInput, midiOutput)
    .expectInputNameEquals('CustomController IN')
    .expectOutputNameEquals('CustomController OUT');

// 3. Define Surface Elements
var surface = deviceDriver.mSurface;

var btnPlay = surface.makeButton(0, 0, 1, 1);
btnPlay.mSurfaceValue.mMidiBinding.setInputPort(midiInput).bindToControlChange(0, 114);

var btnStop = surface.makeButton(1, 0, 1, 1);
btnStop.mSurfaceValue.mMidiBinding.setInputPort(midiInput).bindToControlChange(0, 115);

var faderVolume = surface.makeFader(0, 1, 1, 3);
faderVolume.mSurfaceValue.mMidiBinding.setInputPort(midiInput).bindToControlChange(0, 7);

var knobPan = surface.makeKnob(0, 4, 1, 1);
knobPan.mSurfaceValue.mMidiBinding.setInputPort(midiInput).bindToControlChange(0, 10);

// 4. Map Surface Elements to Cubase Host Parameters
var page = deviceDriver.mMapping.makePage('Main Mix Page');

// Transport Controls
page.mHostAccess.mTransport.mValueSequences.mPlay.setBinding(page, btnPlay.mSurfaceValue);
page.mHostAccess.mTransport.mValueSequences.mStop.setBinding(page, btnStop.mSurfaceValue);

// Selected Track Volume & Pan
var selectedTrackChannel = page.mHostAccess.mTrackSelection.mMixerChannel;
selectedTrackChannel.mValue.mVolume.setBinding(page, faderVolume.mSurfaceValue);
selectedTrackChannel.mValue.mPan.setBinding(page, knobPan.mSurfaceValue);
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Audio Dropouts / ASIO Peak Overload During Playback** | Low ASIO buffer size or DPC latency spikes caused by CPU power throttling. | 1. In *Studio $\rightarrow$ Studio Setup $\rightarrow$ Audio System*, set **ASIO-Guard** to `High`.<br>2. Enable **Steinberg Audio Power Scheme** (prevents Windows CPU core parking).<br>3. Increase audio interface buffer to $256\text{ or }512\text{ samples}$. |
| **Cubase Hangs on Startup: `Initializing VST3 Plugins...`** | A 64-bit VST3 plugin threw an unhandled memory exception during startup scan. | 1. Launch Cubase in Safe Mode: Hold `Ctrl + Shift + Alt` (Windows) or `Cmd + Shift + Opt` (macOS) on launch.<br>2. Check **Disable Third-Party Plugins** $\rightarrow$ Check VST Plugin Manager Blocklist. |
| **Expression Map Fails to Switch Articulations** | Keyswitch note length is 0ms or MIDI chase did not send the initial articulation on playback start. | In Project $\rightarrow$ Expression Map Setup, set **Latch Mode** to `True` and enable **Chase MIDI Controllers** in Preferences. |
| **Control Room Output Muted / Red Speaker Icon** | Listen Bus (`L`) or Talkback enabled on a channel without assigned hardware outputs. | In MixConsole $\rightarrow$ Control Room tab, click **Clear All Solos / Listens** and verify Main Output monitor routing. |

---

## Command Line Syntax & Safe Mode Launch

```bash
# 1. Launch Cubase 14 in Safe Mode with Preference Overrides
"C:\Program Files\Steinberg\Cubase 14\Cubase14.exe" -safe

# 2. Launch Specific Project File Directly
"C:\Program Files\Steinberg\Cubase 14\Cubase14.exe" "C:\Projects\FilmScore_Cue01.cpr"
```

### Essential File Locations
- **Cubase User Preferences**: `%APPDATA%\Steinberg\Cubase 14_64\` (Windows) or `~/Library/Preferences/Cubase 14/` (macOS)
- **Plugin Blocklist**: `%APPDATA%\Steinberg\Cubase 14_64\Vst3xBlocklist.xml`
- **MIDI Remote Driver Scripts**: `%APPDATA%\Steinberg\Cubase 14_64\MIDI Remote\Driver Scripts\`

---

## Agent Operational Directive
> **MANDATORY**: For large orchestral templates with hundreds of virtual instruments, always enable ASIO Guard (set to High) and activate the Steinberg Audio Power Scheme to prevent real-time DPC latency dropouts.
