---
name: yup-guide
description: >
  Step-by-step guide for building a YUP audio plugin from scratch. Use when the user
  asks "how do I create a YUP plugin", "set up a YUP project", "add parameters to my
  YUP plugin", "package my CLAP or VST3", or "how do I wire up AudioParameterHandle".
  Trigger on phrases like "create a YUP plugin", "YUP CMake setup", "yup_audio_plugin",
  "AudioParameterBuilder", "AudioParameterHandle", or "createPluginProcessor".
---

# YUP Audio Plugin - Build Guide

Five steps from empty folder to a working CLAP/VST3/standalone plugin. Do each step in order; skip none.

## Step 1 - Project setup (CMake + YUP)

- Add YUP as a git submodule or `FetchContent` target; disable examples/tests for plugin projects unless needed.
- Use `yup_audio_plugin (...)` to declare the plugin target.
- Set `TARGET_NAME`, `TARGET_VERSION`, `TARGET_APP_ID`, `TARGET_APP_NAMESPACE`, and `TARGET_CXX_STANDARD 20`.
- Set plugin metadata in the same call: `PLUGIN_ID`, `PLUGIN_NAME`, `PLUGIN_VENDOR`, `PLUGIN_VERSION`, `PLUGIN_DESCRIPTION`, `PLUGIN_IS_SYNTH`, and `PLUGIN_IS_MONO`.
- Enable only the formats you need: `PLUGIN_CREATE_CLAP`, `PLUGIN_CREATE_VST3`, `PLUGIN_CREATE_STANDALONE`.
- Link at least `yup::yup_gui` and `yup::yup_audio_processors` in `MODULES`.
- Add plugin sources to `${target_name}_shared`; the format targets link against that shared interface target.

## Step 2 - AudioProcessor skeleton

- Subclass `yup::AudioProcessor`.
- Construct it with a processor name and immutable `yup::AudioBusLayout`, e.g. stereo output:
  `AudioProcessor ("MyPlugin", yup::AudioBusLayout ({}, { yup::AudioBus ("main", yup::AudioBus::Audio, yup::AudioBus::Output, 2) }))`.
- Override `prepareToPlay (float sampleRate, int maxBlockSize)`, `releaseResources()`, `processBlock (yup::AudioSampleBuffer& audioBuffer, yup::MidiBuffer& midiBuffer)`, and `flush()`.
- In `prepareToPlay`: store sample rate, allocate worst-case scratch storage, initialise `AudioParameterHandle`s, and reset all filters, envelopes, oscillators, delay lines, MIDI/voice state, and smoothers.
- In `processBlock`: assume realtime constraints; no allocation, locks, `yup::String` formatting, logging, file/network access, or UI calls.
- Implement preset and state methods: `getCurrentPreset`, `setCurrentPreset`, `getNumPresets`, `getPresetName`, `setPresetName`, `loadStateFromMemory`, and `saveStateIntoMemory`.
- Export the plugin entry point:

```cpp
extern "C" yup::AudioProcessor* createPluginProcessor()
{
    return new MyPluginProcessor();
}
```

## Step 3 - Parameters via AudioParameterBuilder

- Add parameters in the processor constructor with `addParameter (...)`.
- Keep each `yup::AudioParameter::Ptr` as a processor member; parameter IDs must be stable and unique.
- Use `yup::AudioParameterBuilder().withID (...).withName (...).withRange (...).withDefault (...).withSmoothing (...).build()`.
- For audio-thread reads, construct a `yup::AudioParameterHandle` in `prepareToPlay` with the parameter and sample rate.
- In `processBlock`, call `handle.updateNextAudioBlock()` once per block, then use `getNextValue()` per sample or `skip (numSamples)` for block ramps.
- From the editor, wrap user drags with `beginChangeGesture()` and `endChangeGesture()`, and use `setValueNotifyingHost()` for host-visible parameter changes.
- For presets or state restore, prefer setting the real value with `setValue()` or `setNormalizedValue()` from a non-audio thread, then let the audio handle pick it up next block.

## Step 4 - Editor and UI

- Subclass `yup::AudioProcessorEditor`.
- Implement `isResizable()`, `getPreferredSize()`, `paint (yup::Graphics&)`, and `resized()`.
- The editor owns UI components; the processor must work correctly with no editor open.
- The editor may keep `AudioParameter::Ptr`s and poll values from a `yup::Timer` for display sync.
- Do not store a raw editor pointer in the processor. Use `hasEditor()` and `createEditor()` as the factory boundary.
- UI controls should notify parameters through gestures, e.g. slider drag start/end plus `setValueNotifyingHost()`.

## Step 5 - Build, test, package

- Configure: `cmake -B build -DCMAKE_BUILD_TYPE=Release -DYUP_BUILD_TESTS=OFF -DYUP_BUILD_EXAMPLES=OFF`
- Build: `cmake --build build --config Release`
- Validate the produced CLAP/VST3/standalone targets in at least one host.
- Test sample-rate changes, buffer-size changes, transport reset, preset recall, automation, MIDI timing, bypass/suspend/resume, and editor open/close.
- If the plugin reports latency or tail, override `getLatencySamples()` and `getTailSamples()` and verify hosts receive correct values.

## Common pitfalls

| Pitfall | Correct approach |
|---------|------------------|
| Reading raw `AudioParameter` values directly for smoothed DSP | Use `AudioParameterHandle` initialised in `prepareToPlay` |
| Forgetting `updateNextAudioBlock()` | Call it once at the top of each audio block before `getNextValue()` or `skip()` |
| Calling `setValueNotifyingHost()` from `processBlock` | Use it from UI/host-control paths; keep audio-thread changes local or lock-free |
| Allocating MIDI voices on note-on | Preallocate a bounded voice pool in `prepareToPlay` |
| Hard-coding stereo processing without matching `AudioBusLayout` | Declare the layout explicitly and guard channel access |
| Missing state methods | Implement `loadStateFromMemory` / `saveStateIntoMemory`; hosts depend on them for recall |
| Holding `getProcessLock()` from UI/background work | Keep state swaps short; the CLAP wrapper uses a try-lock around processing |
| Leaving state stale after `prepareToPlay` or `flush()` | Reset voices, smoothers, filter history, delay buffers, and pending MIDI unconditionally |

Use the `yup-review` skill to audit finished processor code for YUP-specific thread, parameter, wrapper, and bus-layout issues.
