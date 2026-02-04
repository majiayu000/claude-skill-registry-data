---
name: polyphonic-synth
description: Create MIDI-controllable polyphonic synthesizers for Bice-Box. Provides templates with voice management, envelope generation, MIDI control setup, and oscillator/filter patterns for multi-voice synths.
---

# Polyphonic Synthesizer Development

Create MIDI-controllable polyphonic synthesizers for Bice-Box.

## Critical Rules

### ⚠️ FILENAME/DEFNAME MATCHING IS CRITICAL ⚠️
- **defName MUST EXACTLY match filename** (character for character!)
  - ✅ CORRECT: `synthtoy.sc` → `var defName = \synthtoy;`
  - ✅ CORRECT: `acid_bass.sc` → `var defName = \acid_bass;`
  - ❌ WRONG: `cool-synth.sc` → `var defName = \cool_synth;` (hyphen vs underscore!)

### Polyphonic-Specific Rules
- **numVoices MUST be > 1** (typically 8 or more for polyphony)
- **Pass numVoices to ~setupEffect** - Required for MIDI control
- **Voice arrays required** - `voice_freqs`, `voice_gates`, `voice_amps`
- **Robust indexing** - Use `if(numVoices > 1)` pattern for array access
- **Maximum 8 faders** fit on screen - prioritize important controls

## Polyphonic Synth Template

```supercollider
// shader: oscilloscope
(
    var defName = \synth_name;  // ← MUST match filename exactly!
    var numVoices = 8; // Maximum polyphony
    var specs = (
        // Your synth parameters (max 8 faders fit on screen)
        amp: ControlSpec(0, 1, 'lin', 0, 0.5, ""),
        filter_freq: ControlSpec(100, 8000, 'exp', 0, 2000, "Hz"),
        wave_type: ControlSpec(0, 2, 'lin', 1, 0, ""), // discrete values
        // ADSR envelope parameters
        attack: ControlSpec(0.001, 2.0, 'exp', 0, 0.01, "s"),
        decay: ControlSpec(0.001, 2.0, 'exp', 0, 0.1, "s"),
        sustain: ControlSpec(0.0, 1.0, 'lin', 0, 0.8, ""),
        release: ControlSpec(0.001, 4.0, 'exp', 0, 0.2, "s")
    );

    var def = SynthDef(defName, {
        // Standard parameters
        var out = \out.kr(0);
        var in_bus = \in_bus.kr(0);
        var analysis_out_bus = \analysis_out_bus.kr;

        // Your synth parameters
        var amp = \amp.kr(specs[\amp].default);
        var filter_freq = \filter_freq.kr(specs[\filter_freq].default);
        var wave_type = \wave_type.kr(specs[\wave_type].default);
        var attack = \attack.kr(specs[\attack].default);
        var decay = \decay.kr(specs[\decay].default);
        var sustain = \sustain.kr(specs[\sustain].default);
        var release = \release.kr(specs[\release].default);

        // Voice arrays - REQUIRED for polyphonic synths
        var voice_freqs = \voice_freqs.kr(Array.fill(numVoices, 440));
        var voice_gates = \voice_gates.kr(Array.fill(numVoices, 0));
        var voice_amps = \voice_amps.kr(Array.fill(numVoices, 0));

        // ALL other variables declared here!
        var voice_signals, mixed_voices, final_sig, mono_for_analysis;

        // Generate all voices
        voice_signals = Array.fill(numVoices, { |i|
            var freq, gate, vel_amp;
            var env, wave, voice_out;

            // When numVoices > 1, controls are multi-channel and must be indexed.
            // When numVoices == 1, they are single-channel and cannot be indexed.
            if(numVoices > 1) {
                freq = voice_freqs[i];
                gate = voice_gates[i];
                vel_amp = voice_amps[i];
            } {
                freq = voice_freqs;
                gate = voice_gates;
                vel_amp = voice_amps;
            };

            // ADSR envelope
            env = EnvGen.ar(Env.adsr(attack, decay, sustain, release), gate);

            // Your oscillator/wave generation here
            wave = Select.ar(wave_type, [
                SinOsc.ar(freq),    // 0 = sine
                Saw.ar(freq),       // 1 = saw
                Pulse.ar(freq, 0.5) // 2 = square
            ]);

            // Apply envelope and velocity
            voice_out = wave * env * vel_amp;
            voice_out;
        });

        // Mix all voices together
        mixed_voices = Mix.ar(voice_signals);

        // Apply your processing (filters, effects, etc.)
        final_sig = RLPF.ar(mixed_voices, filter_freq, 0.3);
        final_sig = final_sig * amp;

        // Outputs
        mono_for_analysis = final_sig;
        Out.ar(analysis_out_bus, mono_for_analysis);
        Out.ar(out, [final_sig, final_sig]);
    });
    def.add;
    "Effect SynthDef 'synth_name' (polyphonic) added".postln;

    // CRITICAL: Pass numVoices to ~setupEffect to enable MIDI control
    ~setupEffect.value(defName, specs, [], numVoices);
)
```

## Key Concepts

### Voice Management
- **numVoices** - Total polyphony (e.g., 8 voices = 8 simultaneous notes)
- **voice_freqs** - Frequency for each voice (set by MIDI)
- **voice_gates** - Gate signal (1 = note on, 0 = note off)
- **voice_amps** - Velocity (0.0-1.0 based on MIDI velocity)

### Array Indexing Pattern
```supercollider
// Robust indexing for multi-voice compatibility
if(numVoices > 1) {
    freq = voice_freqs[i];
    gate = voice_gates[i];
    vel_amp = voice_amps[i];
} {
    freq = voice_freqs;
    gate = voice_gates;
    vel_amp = voice_amps;
};
```

### Envelope Generation
```supercollider
// ADSR envelope (Attack, Decay, Sustain, Release)
env = EnvGen.ar(Env.adsr(attack, decay, sustain, release), gate);

// Alternative envelopes
env = EnvGen.ar(Env.perc(attack, release), gate);  // Percussive
env = EnvGen.ar(Env.asr(attack, sustain, release), gate);  // ASR
```

### Voice Mixing
```supercollider
// Mix all voices to mono
mixed_voices = Mix.ar(voice_signals);

// Normalize to prevent clipping with many voices
final_sig = mixed_voices / numVoices.sqrt;
```

## MCP Workflow

**Recommended workflow for polyphonic synths:**

1. **Test syntax** - Validate code during development
   ```
   mcp__bice-box__test_supercollider_code(scCode: "your code here")
   ```
   **Important**: Ensure `numVoices > 1` in your code!

2. **Create/update** - Save your synth with MIDI support
   ```
   mcp__bice-box__create_or_update_audio_effect(
       effectName: "my_synth",
       scCode: "your code here",
       makeActive: true
   )
   ```
   **Critical**: Code must include `~setupEffect.value(defName, specs, [], numVoices)`

3. **Activate and connect MIDI**
   ```
   mcp__bice-box__set_current_effect(effectName: "my_synth")
   ```
   - Connect your MIDI keyboard
   - Play notes to test polyphony
   - Verify all voices are working

4. **Adjust parameters** - Fine-tune envelope and filters
   ```
   mcp__bice-box__set_effect_parameters(params: {
       attack: 0.05,
       release: 1.2,
       filter_freq: 3000
   })
   ```

5. **Debug** - Check for voice allocation issues
   ```
   mcp__bice-box__read_logs(lines: 100, filter: "voice")
   ```

## Common Oscillator Types

```supercollider
// Basic waveforms
SinOsc.ar(freq)           // Sine wave
Saw.ar(freq)              // Sawtooth
Pulse.ar(freq, width)     // Pulse/square wave
LFTri.ar(freq)            // Triangle wave

// Advanced oscillators
Blip.ar(freq, numHarmonics)  // Bandlimited pulse train
VarSaw.ar(freq, 0, width)    // Variable sawtooth
PMOsc.ar(carFreq, modFreq, modIndex)  // Phase modulation
```

## Filter Examples

```supercollider
// Low-pass filters
LPF.ar(sig, freq)                    // Simple low-pass
RLPF.ar(sig, freq, rq)              // Resonant low-pass
MoogFF.ar(sig, freq, gain)          // Moog-style ladder filter
DFM1.ar(sig, freq, res, gain)       // Digital filter

// Multi-mode filters
SVF.ar(sig, freq, res, lowpass: 1)  // State variable filter
```

## Modulation Techniques

```supercollider
// LFO modulation
var lfo = SinOsc.kr(lfoRate);
freq = baseFreq * (1 + (lfo * lfoDepth));

// Envelope modulation
var filterEnv = EnvGen.ar(Env.perc(0.01, 0.5), gate);
cutoff = baseFreq * (1 + (filterEnv * envAmount));

// Velocity modulation
final_sig = wave * env * vel_amp * amp;
```

## Parameter Design Tips

- **Keep it focused** - Max 8 faders, choose most expressive parameters
- **Priority order**: Envelope (ADSR) → Filter → Oscillator → FX
- **Typical essential params**:
  - Attack, Decay, Sustain, Release (4 faders)
  - Filter frequency, Filter resonance (2 faders)
  - Master amp, Oscillator character (2 faders)
- **Combine when possible**: Use discrete switches for wave types instead of continuous params

## Testing Checklist

- [ ] numVoices > 1 in code
- [ ] `~setupEffect.value()` includes numVoices parameter
- [ ] Filename matches defName exactly
- [ ] All voices play when pressing multiple keys
- [ ] Envelope releases properly when keys released
- [ ] No voice stealing issues (increase numVoices if needed)
- [ ] Filter responds to parameter changes
- [ ] No CPU spikes (check Task Manager/Activity Monitor)
