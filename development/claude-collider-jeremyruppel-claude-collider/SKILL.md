---
name: claude-collider
description: Use when live coding music with SuperCollider via ClaudeCollider MCP server.
---

# SuperCollider Live Coding with ClaudeCollider

This skill enables live music synthesis using SuperCollider via the ClaudeCollider MCP server.

## Quick Reference

### Key Rules

1. **Drums need `\freq, 48`** - IMPORTANT Without it, drums sound wrong
2. **Use Pdef for rhythms** - Patterns that repeat
3. **Use Ndef for continuous** - Pads, drones, textures
4. **Symbols not strings** - `\kick` not `"kick"`
5. **Semicolons between statements** - No trailing semicolon
6. **NEVER Synth() inside Ndef** - Causes infinite spawning

---

# CC API Reference

The main entry point stored in `~cc`. Access subsystems via `~cc.synths`, `~cc.fx`, `~cc.midi`, `~cc.samples`, `~cc.recorder`, `~cc.state`.

## CC - Main Class

| Method                                   | Description                                             |
| ---------------------------------------- | ------------------------------------------------------- |
| `tempo(bpm)`                             | Get/set tempo in BPM                                    |
| `stop`                                   | Stop all Pdefs and Ndefs                                |
| `clear`                                  | Full reset: free all synths, patterns, effects, samples |
| `status`                                 | Get formatted status string                             |
| `reboot(device, numOutputs, onComplete)` | Restart the server                                      |

---

## ~cc.synths - Synth Definitions

27+ pre-built synths with `cc_` prefix.

| Method                | Description                         |
| --------------------- | ----------------------------------- |
| `list`                | Comma-separated list of synth names |
| `describe`            | Detailed descriptions with params   |
| `play(name, ...args)` | One-shot synth playback             |

### Usage

```supercollider
~cc.synths.play(\cc_kick, \freq, 48, \amp, 0.8);
```

---

## ~cc.fx - Effects System

18 built-in effects with routing, chaining, and sidechaining.

| Method                                               | Description                                |
| ---------------------------------------------------- | ------------------------------------------ |
| `load(name, slot)`                                   | Load effect (slot defaults to `fx_<name>`) |
| `set(slot, ...args)`                                 | Set effect parameters                      |
| `bypass(slot, bool)`                                 | Bypass/re-enable effect                    |
| `remove(slot)`                                       | Remove effect                              |
| `route(source, target)`                              | Route Pdef/Ndef to effect                  |
| `connect(from, to)`                                  | Chain effect output to another effect      |
| `sidechain(name, threshold, ratio, attack, release)` | Create sidechain compressor                |
| `routeTrigger(source, sidechainName, passthrough)`   | Route trigger to sidechain                 |
| `routeToOutput(source, channels)`                    | Route to hardware outputs                  |
| `list`                                               | Available effect names                     |
| `describe`                                           | Effect descriptions with params            |
| `status`                                             | Current effects and routing                |

### Usage

```supercollider
~cc.fx.load(\reverb);
~cc.fx.route(\bass, \fx_reverb);
~cc.fx.set(\fx_reverb, \mix, 0.5, \room, 0.9);
```

---

## ~cc.midi - MIDI Control

| Method                                                 | Description                           |
| ------------------------------------------------------ | ------------------------------------- |
| `listDevices`                                          | List available MIDI devices           |
| `connect(device, direction)`                           | Connect device (`\in` or `\out`)      |
| `connectAll`                                           | Connect all MIDI inputs               |
| `disconnect(direction)`                                | Disconnect (`\in`, `\out`, or `\all`) |
| `play(synthName, channel, mono, velToAmp, ccMappings)` | Play synth via MIDI                   |
| `stop`                                                 | Stop current MIDI synth               |
| `status`                                               | Get MIDI status                       |

### Usage

```supercollider
~cc.midi.connectAll;
~cc.midi.play(\lead, nil, false, true, (
  1: \cutoff,                           // CC1 -> cutoff
  74: (param: \res, range: [0.1, 0.9])  // CC74 -> res with range
));
```

---

## ~cc.samples - Sample Management

Samples from `~/.claudecollider/samples`.

| Method                  | Description                    |
| ----------------------- | ------------------------------ |
| `load(name)`            | Load sample buffer into memory |
| `at(name)`              | Get buffer (nil if not loaded) |
| `play(name, rate, amp)` | One-shot playback              |
| `free(name)`            | Free buffer                    |
| `reload`                | Rescan directory for new files |
| `names`                 | Array of sample names          |
| `list`                  | Comma-separated list           |

### Usage

```supercollider
~cc.samples.load(\kick);
~cc.samples.play(\kick, 1, 0.8);
Pdef(\samp, Pbind(\instrument, \cc_sampler, \buf, ~cc.samples.at(\kick), \dur, 1)).play
```

---

## ~cc.recorder - Audio Recording

Records to `~/.claudecollider/recordings`.

| Method            | Description                         |
| ----------------- | ----------------------------------- |
| `start(filename)` | Start recording (auto-names if nil) |
| `stop`            | Stop recording, returns path        |
| `status`          | Recording status                    |
| `isRecording`     | Boolean                             |

---

## ~cc.state - Bus Management

Named control/audio buses stored in current environment.

| Method                         | Description                           |
| ------------------------------ | ------------------------------------- |
| `bus(name, numChannels, rate)` | Get or create bus (also sets `~name`) |
| `setBus(name, value)`          | Set bus value                         |
| `getBus(name)`                 | Get bus by name                       |
| `freeBus(name)`                | Free bus                              |
| `clear`                        | Free all buses                        |

### Usage

```supercollider
~cc.state.bus(\cutoff, 1, \control);
~cc.state.setBus(\cutoff, 2000);
Synth(\cc_acid, [\cutoff, ~cutoff.asMap]);  // Map bus to param
```
