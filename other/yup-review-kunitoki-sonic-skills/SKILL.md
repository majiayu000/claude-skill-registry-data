---
name: yup-review
description: >
  Reviews YUP audio plugin code for YUP-specific correctness issues: AudioProcessor
  lifecycle, AudioParameterBuilder and AudioParameterHandle usage, editor gestures,
  AudioBusLayout handling, CLAP/VST3 wrapper contracts, state recall, and MIDI safety.
  Use when the user asks to review a YUP plugin, check a processBlock, audit parameter
  smoothing, or asks "is this YUP code safe?". Trigger when you see yup::AudioProcessor,
  yup_audio_plugin, AudioParameterBuilder, AudioParameterHandle, AudioProcessorEditor,
  or createPluginProcessor in the code.
---

# YUP Audio Plugin Review

YUP looks JUCE-like in places, but its plugin API has its own parameter handles, bus layout, editor contract, and wrapper behavior. Review those directly instead of applying APVTS rules.

## Step 0 - Run universal checks first

Invoke `audio-dsp-review` and `audio-numerics-review` before this skill. This skill adds YUP-specific checks on top; it does not replace realtime-safety or numerics reviews.

## Step 1 - Identify plugin structure

Locate the core classes and boundaries:
- `yup::AudioProcessor` - audio thread owns `processBlock`; wrapper/host code calls lifecycle, state, and preset methods
- `yup::AudioProcessorEditor` - UI/message thread only; never call from audio thread
- `yup::AudioParameter` - atomic scalar value plus listeners for host/UI notification
- `yup::AudioParameterHandle` - audio-thread smoothing/read path; initialise in `prepareToPlay`
- `yup::AudioBusLayout` - immutable I/O contract exposed to plugin wrappers
- `extern "C" yup::AudioProcessor* createPluginProcessor()` - plugin entry point used by wrappers

## Step 2 - Scan for YUP violations

| Violation | Where to look | Risk |
|-----------|--------------|------|
| `AudioParameterHandle` default-constructed and used before `prepareToPlay` | Members and `processBlock` | Null parameter assertion/crash; wrong smoothing state |
| Missing `handle.updateNextAudioBlock()` | `processBlock` | Automation and smoothing lag or never update |
| Recreating `AudioParameterHandle` in `processBlock` | Audio callback | Reinitialises smoothing and may add avoidable work/glitches |
| `setValueNotifyingHost()`, `beginChangeGesture()`, or `endChangeGesture()` from audio code | `processBlock`, MIDI handlers, DSP helpers | Listener/host notification path is not a realtime data path |
| Allocating voices, buffers, `MemoryBlock`, `String`, `std::vector`, or smart-pointer objects in `processBlock` | MIDI note-on, scratch buffers, metering | Heap traffic causes xruns |
| `YUP_DBG`, `Logger::writeToLog`, `File`, `URL`, JSON/XML, or string formatting in audio code | Debug and error paths | Logging/I/O/allocation on audio thread |
| Hard-coded channel pointers without layout checks | `getWritePointer(0/1)` and bus setup | Mono, sidechain, or unusual host layout crashes/corrupts audio |
| Mutating `MidiBuffer` while iterating it | MIDI loops | Iterator invalidation or unbounded allocation |
| `prepareToPlay` not resetting all DSP and note state | Lifecycle methods | Host reactivation leaves stale filter history, held notes, or ramps |
| `flush()` missing for synths/effects with tails or voices | CLAP reset handling | Host reset leaves hanging notes or stale delay/reverb tails |
| State load/save left unimplemented | `loadStateFromMemory`, `saveStateIntoMemory` | DAW session recall and presets fail |
| Long work under `getProcessLock()` or state swaps with no handoff | UI/state/background code | Processing may skip under CLAP try-lock or race under other wrappers |
| Editor stores raw processor-owned UI pointers or processor stores editor pointer | Editor/processor members | Dangling pointer when host closes editor |

## Step 3 - Check YUP API contracts

- Constructor: parameters are added once; IDs are unique and stable; bus layout matches `PLUGIN_IS_SYNTH` / `PLUGIN_IS_MONO` intent.
- `prepareToPlay`: allocates and resets all state; constructs handles with current sample rate; tolerates repeated calls.
- `processBlock`: reads smoothed parameters through handles; respects `audioBuffer.getNumSamples()` and actual channel count; clears or writes every output sample it owns.
- MIDI: consumes events in sample order; uses bounded voice/event storage; clears or rewrites outgoing MIDI deliberately.
- Editor: uses gesture begin/end around drags; calls `setValueNotifyingHost()` for user changes; polls parameter values with a timer using `dontSendNotification`.
- State/presets: serialises all host-visible parameters and preset data; validates memory before applying; does not assume state callbacks are the audio thread.
- Format wrappers: CLAP and VST3 builds are enabled only as needed; CLAP/VST3/standalone targets all link the same `${target_name}_shared` code.

## Step 4 - Write the review

```markdown
## YUP Plugin Review: `[file / class]`

### Verdict
[Safe | Has critical violations | Warnings only] - [one sentence summary]

### Critical Violations
**[Category]: [description]**
`file:line` - `offending code`
Why: [one sentence on YUP lifecycle/thread/API risk]
Fix: [concrete YUP-idiomatic suggestion]

### Warnings
[same format]

### What's Done Well
[correct patterns observed]

### Recommended Fixes (priority order)
1. ...
```

## Quick fix table

| Violation | Fix |
|-----------|-----|
| Direct unsmoothed parameter read for DSP | Keep `AudioParameter::Ptr`, initialise `AudioParameterHandle` in `prepareToPlay`, read via the handle |
| Missing gesture pairing | Call `beginChangeGesture()` on drag start and `endChangeGesture()` on drag end |
| UI value changes with `setValue()` | Use `setValueNotifyingHost()` for user edits so automation/host state is notified |
| Allocating voices on note-on | Preallocate voice slots and reuse them; reject/steal voices when full |
| Hard-coded stereo | Declare stereo in `AudioBusLayout` and guard `getNumChannels()` before channel access |
| Missing reset | Clear voices, delay lines, filters, smoothers, and pending MIDI in both `prepareToPlay` and `flush()` where relevant |
| Unimplemented state recall | Serialise parameters and presets into `MemoryBlock`; validate and apply from non-audio state callbacks |
| Audio-to-UI updates | Write scalars to atomics or a preallocated lock-free queue; have editor `Timer` poll them |

For full code examples and YUP-specific BAD/GOOD patterns, see `references/yup-violations.md`.
