---
name: juce-guide
description: >
  Step-by-step guide for building a JUCE audio plugin from scratch. Use when the user
  asks "how do I create a JUCE plugin", "set up a JUCE project", "add parameters to my
  JUCE plugin", "package my VST3", or "how do I wire up APVTS". Trigger on phrases like
  "create a JUCE plugin", "JUCE CMake setup", "AudioProcessor skeleton", "add APVTS
  parameters", or "codesign my plugin on macOS".
---

# JUCE Audio Plugin — Build Guide

Five steps from empty folder to distributable plugin. Do each step in order; skip none.

## Step 1 — Project setup (CMake + JUCE)

- Add JUCE as a git submodule or FetchContent target; call `add_subdirectory(JUCE)`.
- Use `juce_add_plugin(MyPlugin FORMATS VST3 AU Standalone ...)` to declare the plugin target.
- Set `PLUGIN_MANUFACTURER_CODE`, `PLUGIN_CODE`, `IS_SYNTH`, `NEEDS_MIDI_INPUT` in the same call.
- Link `juce::juce_audio_processors juce::juce_audio_utils juce::juce_dsp` to the target.

## Step 2 — AudioProcessor skeleton

- Subclass `juce::AudioProcessor`; override `prepareToPlay`, `releaseResources`, `processBlock`.
- In `prepareToPlay`: store `sampleRate` and `maximumBlockSize`, allocate internal buffers, reset all state (filters, envelopes, delay lines — unconditionally).
- In `processBlock`: read only pre-cached raw parameter pointers; never allocate, never call JUCE String ops or DBG().
- Implement `getStateInformation` / `setStateInformation` using `apvts.copyState()` and `apvts.replaceState()` with a `MemoryOutputStream` / `MemoryBlock`.

## Step 3 — Parameters via APVTS

- Declare a static `createParameterLayout()` method that returns `AudioProcessorValueTreeState::ParameterLayout`.
- Construct `apvts(*this, nullptr, "Parameters", createParameterLayout())` as a member.
- After constructing APVTS, cache raw pointers once: `gainParam = apvts.getRawParameterValue("Gain")`.
- In `processBlock`, dereference with `gainParam->load()` — no APVTS calls on the audio thread.
- Use `AudioProcessorValueTreeState::ParameterAttachment` (or `SliderAttachment`) in the editor, never in the processor.

## Step 4 — Editor and UI

- Subclass `juce::AudioProcessorEditor`; call `setSize(w, h)` in the constructor.
- Override `paint` for background / labels; override `resized` to lay out components with `setBounds`.
- Declare `juce::Slider` members; attach each via `juce::AudioProcessorValueTreeState::SliderAttachment`.
- Keep all UI state in the editor — the processor must function correctly with no editor open.
- The editor holds a reference to the processor (passed in constructor); never store a raw editor pointer in the processor.

## Step 5 — Build, test, package

- Configure: `cmake -B build -DCMAKE_BUILD_TYPE=Release`
- Build: `cmake --build build --config Release`
- Locate artefacts under `build/MyPlugin_artefacts/Release/`.
- macOS codesign: `codesign --deep --force --sign "Developer ID Application: ..." MyPlugin.vst3` then `spctl --assess --verbose MyPlugin.vst3`.
- Notarize for distribution: `xcrun notarytool submit MyPlugin.pkg --apple-id ... --wait`.
- Validate in a DAW host or use the JUCE `AudioPluginHost` utility (`extras/AudioPluginHost`).

## Common pitfalls

| Pitfall | Correct approach |
|---------|-----------------|
| Calling `apvts.getParameter()` in `processBlock` | Cache `getRawParameterValue()` once after APVTS construction |
| Allocating in `processBlock` | Allocate in `prepareToPlay` only |
| Not resetting state on `prepareToPlay` re-entry | Always reset unconditionally |
| Storing editor pointer in processor | Use `createEditor()` factory; processor owns no editor reference |
| Missing `JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR` | Add to every `AudioProcessor` and `AudioProcessorEditor` subclass |

Use the `juce-review` skill to audit finished processor code for thread-safety violations.
